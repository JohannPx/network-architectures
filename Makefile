PY ?= python3
DOCS ?= docs
OUT ?= build

.PHONY: setup build build-offline clean watch

setup:
	$(PY) -m pip install -r scripts/requirements.txt     # ⟶ TAB au début

build:
	$(PY) scripts/process.py --docs $(DOCS) --out $(OUT)  # ⟶ TAB

build-offline:
	$(PY) scripts/process.py --docs $(DOCS) --out $(OUT) --offline  # ⟶ TAB

clean:
	rm -rf $(OUT)                                        # ⟶ TAB

# Rebuild auto (nécessite watchdog)
watch:
	$(PY) -m watchdog.cli.watchmedo shell-command \
	  --patterns="*.md" --recursive \
	  --command='$(PY) scripts/process.py --docs $(DOCS) --out $(OUT)' $(DOCS)   # ⟶ TAB
