.PHONY: build clean

build:
	python3 scripts/process.py --docs docs --out build

clean:
	rm -rf build
	mkdir -p build/png build/pdf build/temp
