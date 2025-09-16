PY ?= python3
DOCS ?= docs
OUT ?= build

.PHONY: setup build clean watch

setup:
	$(PY) -m pip install -r scripts/requirements.txt

# Build: rend les Mermaid en PNG (services en ligne), remplace dans le MD, puis Pandoc → PDF
build:
	$(PY) scripts/process.py --docs $(DOCS) --out $(OUT)

clean:
	rm -rf $(OUT)

# Rebuild auto (nécessite watchdog installé)
watch:
	$(PY) -m watchdog.cli.watchmedo shell-command \
	  --patterns="*.md" --recursive \
	  --command='$(PY) scripts/process.py --docs $(DOCS) --out $(OUT)' $(DOCS)
