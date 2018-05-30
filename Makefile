.PHONY: docs tests

docs:
	pandoc -f gfm -t rst docs/README.md > README.rst

tests:
	python -m pytest
