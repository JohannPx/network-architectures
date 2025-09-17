import argparse
import base64
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import requests

# --- Détection des blocs Mermaid ---
MERMAID_BLOCK = re.compile(
    r"(^|\n)```mermaid\s*\n(.*?)\n```", re.DOTALL | re.IGNORECASE)
# --- Extraction du premier H1 ---
H1_RE = re.compile(r"^\s*#\s+(.+?)\s*$", re.MULTILINE)


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def ensure_dirs(*paths: Path):
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def render_mermaid_png_online(code: str) -> bytes:
    """
    Rendu PNG via services gratuits :
      1) mermaid.ink  2) kroki.io (fallback)
    """
    # mermaid.ink
    try:
        b64 = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
        url = f"https://mermaid.ink/img/{b64}"
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        if r.content and r.headers.get("content-type", "").startswith("image/"):
            return r.content
    except Exception:
        pass
    # kroki.io
    try:
        url = "https://kroki.io/mermaid/png"
        r = requests.post(url, data=code.encode("utf-8"), timeout=30)
        r.raise_for_status()
        if r.content:
            return r.content
    except Exception as e:
        raise RuntimeError(f"Échec de rendu Mermaid en ligne: {e}")

    raise RuntimeError(
        "Impossible d'obtenir une image Mermaid depuis les services en ligne.")


def replace_mermaid_with_images(md_text: str, png_dir: Path, rel_img_prefix: str, md_stem: str) -> str:
    """
    Remplace chaque bloc ```mermaid ... ``` par ![diagram](build/png/<md>_mermaid[_{n}].png)
    - 1er diagramme du fichier : <md>_mermaid.png
    - suivants : <md>_mermaid_2.png, _3.png, ...
    """
    out = []
    last = 0
    idx = 0
    for m in MERMAID_BLOCK.finditer(md_text):
        out.append(md_text[last:m.start()])
        code = m.group(2).strip()
        idx += 1
        png_name = f"{md_stem}_mermaid.png" if idx == 1 else f"{md_stem}_mermaid_{idx}.png"
        png_path = png_dir / png_name
        if not png_path.exists():
            png_path.write_bytes(render_mermaid_png_online(code))
        out.append(f"\n![diagram]({rel_img_prefix}/{png_name})\n")
        last = m.end()
    out.append(md_text[last:])
    return "".join(out)


def extract_h1_title(md_text: str) -> tuple[str | None, str]:
    """
    Renvoie (title, body_without_first_h1).
    Si un H1 existe, on l'extrait comme titre ET on le supprime du corps (pas de doublon).
    """
    m = H1_RE.search(md_text)
    if not m:
        return None, md_text
    title = m.group(1).strip()
    start, end = m.span()
    body = (md_text[:start] + md_text[end:]).lstrip("\n")
    return title, body


def default_title_for(md_path: Path) -> str:
    return (md_path.stem.replace("_", " ").strip()) or "Document"


def run_pandoc(input_md: Path, output_pdf: Path, resource_path: Path, title: str):
    """
    Conversion Markdown → PDF via Pandoc (LuaLaTeX).
    - Images inline (pas de flottants)
    - Titre = 1er H1 (le H1 est retiré du corps)
    - Aucune numérotation de pages (pagestyle=empty + \pagenumbering{gobble})
    """
    cmd = [
        "pandoc",
        str(input_md),
        "--from=markdown+emoji-implicit_figures",
        "--to=pdf",
        f"--resource-path={resource_path}",
        "--pdf-engine=lualatex",
        "-V", "mainfont=Noto Sans",
        "-V", "monofont=Noto Sans Mono",
        "-V", "geometry:margin=2.2cm",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-V", "pagestyle=empty",                   # désactive les en-têtes/pieds standard
        # supprime toute numérotation
        "--variable", r"header-includes=\pagenumbering{gobble}",
        "--variable", "graphics:yes",
        "--variable", "fig-pos=H",
        "--metadata", f"title={title}",
        "-o", str(output_pdf),
    ]
    subprocess.run(cmd, check=True)


def process_all(docs_dir: Path, build_dir: Path):
    png_dir = build_dir / "png"
    temp_dir = build_dir / "temp"
    pdf_dir = build_dir / "pdf"

    ensure_dirs(png_dir, temp_dir, pdf_dir)

    md_files = sorted(docs_dir.rglob("*.md"))
    if not md_files:
        print(f"Aucun .md trouvé dans {docs_dir}")
        return

    for md in md_files:
        md_stem = md.stem
        rel = md.relative_to(docs_dir)
        cleaned_md = temp_dir / rel
        cleaned_md.parent.mkdir(parents=True, exist_ok=True)

        raw = md.read_text(encoding="utf-8")

        # 1) Titre = 1er H1; retrait du H1 du corps
        title, body_wo_h1 = extract_h1_title(raw)
        if not title:
            title = default_title_for(md)
            body_wo_h1 = raw

        # 2) Mermaid -> PNG (images inline), nommage simple basé sur le nom du MD
        rel_prefix = str(
            Path("..") / "png" if cleaned_md.parent != temp_dir else Path("png"))
        replaced = replace_mermaid_with_images(
            body_wo_h1, png_dir=png_dir, rel_img_prefix=rel_prefix, md_stem=md_stem
        )

        # 3) Si doc vide, injecter un titre minimal pour éviter "No pages of output"
        if not replaced.strip():
            replaced = f"# {title}\n"

        cleaned_md.write_text(replaced, encoding="utf-8")

        # 4) Sortie PDF à plat : build/pdf/<nom>.pdf (pas d’arbo source)
        out_pdf = pdf_dir / (md_stem + ".pdf")
        out_pdf.parent.mkdir(parents=True, exist_ok=True)

        print(f"→ Pandoc: {md} → {out_pdf}")
        run_pandoc(cleaned_md, out_pdf, resource_path=png_dir, title=title)

    print("OK ✅")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs", type=str,
                    help="Dossier des sources .md")
    ap.add_argument("--out",  default="build", type=str,
                    help="Dossier de sortie (png/temp/pdf)")
    args = ap.parse_args()

    docs_dir = Path(args.docs).resolve()
    build_dir = Path(args.out).resolve()

    try:
        process_all(docs_dir, build_dir)
    except subprocess.CalledProcessError as e:
        print("Erreur d'exécution Pandoc:", e, file=sys.stderr)
        sys.exit(e.returncode or 1)
    except Exception as e:
        print("Erreur:", e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
