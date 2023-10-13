all: build/my-languages.so

vendor/tree-sitter-regex/src/parser.c:
	git submodule init

# It's ok if the name is .so on MacOS too, the tool builds a dynlib with an universal name
build/my-languages.so: vendor/tree-sitter-regex/src/parser.c
	poetry run ./build-parser.py

test:
	poetry run pytest --cov

clean:
	rm regexes.yaml
	rm -rf build
