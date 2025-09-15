# Usage: python3 scripts/process.py [--docs docs] [--out build]
# - Parcourt les .md, convertit les blocs ```mermaid``` en PNG (cache par hash),
# - écrit des .md "nettoyés" dans build/temp,
# - génère les PDF via Pandoc + XeLaTeX.

import argparse
import base64
import hashlib
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    requests = None

MERMAID_BLOCK_RE = re.compile(
    r"(^|\n)```mermaid\n(.*?)\n```",
    flags=re.DOTALL | re.IGNORECASE,
)


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


def ensure_dirs(*paths: Path):
    for p in paths:
        p.mkdir(parents=True, exist_ok=True)


def have_cmd(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def render_mermaid_to_png(code: str, out_path: Path, offline_preferred: bool = False) -> None:
    """
    Stratégie multi-backend :
    1) mmdc (offline) si dispo et demandé/préféré
    2) Kroki (HTTP POST /mermaid/png)
    3) mermaid.ink (GET)
    Lève une exception si tous échouent.
    """
    last_err = None

    # 1) mmdc (offline)
    if offline_preferred and have_cmd("mmdc"):
        try:
            # mmdc demande un fichier d'entrée
            tmp = out_path.with_suffix(".mmd")
            tmp.write_text(code, encoding="utf-8")
            subprocess.run([
                "mmdc", "-i", str(tmp), "-o", str(out_path), "-b", "transparent", "-q", "100",
            ], check=True)
            tmp.unlink(missing_ok=True)
            return
        except Exception as e:
            last_err = e

    # 2) Kroki
    if requests is not None:
        try:
            url = "https://kroki.io/mermaid/png"
            r = requests.post(url, data=code.encode("utf-8"), timeout=30)
            r.raise_for_status()
            out_path.write_bytes(r.content)
            return
        except Exception as e:
            last_err = e

    # 3) mermaid.ink
    try:
        # mermaid.ink attend un deflate+base64 URL-safe; on tente simple base64 utf-8 (compat mermaid.ink non-compressé)
        # Pour une meilleure compat, on pourrait deflater; la plupart des serveurs acceptent aussi du b64 brut.
        b64 = base64.urlsafe_b64encode(code.encode("utf-8")).decode("ascii")
        ink_url = f"https://mermaid.ink/img/{b64}"
        if requests is None:
            raise RuntimeError("'requests' non installé pour mermaid.ink")
        r = requests.get(ink_url, timeout=30)
        r.raise_for_status()
        out_path.write_bytes(r.content)
        return
    except Exception as e:
        last_err = e

    raise RuntimeError(f"Échec rendu Mermaid pour {out_path.name}: {last_err}")


def replace_mermaid_with_images(md_text: str, png_dir: Path, rel_img_prefix: str, offline_preferred: bool) -> str:
    def _repl(match: re.Match) -> str:
        code = match.group(2).strip()
        h = sha1(code)[:16]
        png_name = f"mermaid_{h}.png"
        png_path = png_dir / png_name
        if not png_path.exists():
            render_mermaid_to_png(code, png_path, offline_preferred=offline_preferred)
        # Chemin RELATIF dans le MD pour portabilité
        return f"\n![diagram]({rel_img_prefix}/{png_name})\n"

    return MERMAID_BLOCK_RE.sub(_repl, md_text)


def run_pandoc(src_md: Path, out_pdf: Path, resource_path: Path, main_font: str = "Noto Sans", mono_font: str = "Noto Sans Mono"):
    cmd = [
        "pandoc",
        str(src_md),
        "--from=markdown+emoji",
        "--to=pdf",
        f"--resource-path={resource_path}",
        "--pdf-engine=xelatex",
        "-V", f"mainfont={main_font}",
        "-V", f"monofont={mono_font}",
        "-V", "geometry:margin=2.2cm",
        "-V", "colorlinks=true",
        "-V", "linkcolor=blue",
        "-o", str(out_pdf),
    ]
    subprocess.run(cmd, check=True)


def process_all(docs_dir: Path, build_dir: Path, offline_preferred: bool):
    png_dir = build_dir / "png"
    temp_dir = build_dir / "temp"
    pdf_dir = build_dir / "pdf"
    ensure_dirs(png_dir, temp_dir, pdf_dir)

    md_files = sorted(list(docs_dir.rglob("*.md")))
    if not md_files:
        print(f"Aucun .md trouvé sous {docs_dir}")
        return

    for md in md_files:
        rel = md.relative_to(docs_dir)
        cleaned_md = temp_dir / rel
        cleaned_md.parent.mkdir(parents=True, exist_ok=True)

        text = md.read_text(encoding="utf-8")
        text2 = replace_mermaid_with_images(text, png_dir, rel_img_prefix=str(Path("..") / "png" if cleaned_md.parent != temp_dir else Path("png")), offline_preferred=offline_preferred)
        cleaned_md.write_text(text2, encoding="utf-8")

        out_pdf = (pdf_dir / rel).with_suffix(".pdf")
        out_pdf.parent.mkdir(parents=True, exist_ok=True)
        print(f"→ Pandoc: {rel} → {out_pdf.relative_to(pdf_dir)}")
        run_pandoc(cleaned_md, out_pdf, resource_path=png_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--docs", default="docs", type=str, help="Dossier des sources .md")
    ap.add_argument("--out", default="build", type=str, help="Dossier de sortie (png/temp/pdf)")
    ap.add_argument("--offline", action="store_true", help="Privilégier le rendu Mermaid offline (mmdc) si dispo")
    args = ap.parse_args()

    docs_dir = Path(args.docs).resolve()
    build_dir = Path(args.out).resolve()

    try:
        process_all(docs_dir, build_dir, offline_preferred=args.offline)
        print("OK ✅")
    except subprocess.CalledProcessError as e:
        print("Erreur d'exécution:", e, file=sys.stderr)
        sys.exit(e.returncode or 1)
    except Exception as e:
        print("Erreur:", e, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
