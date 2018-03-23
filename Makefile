.PHONY: docs tests

docs:
	pandoc -f markdown_github -t rst docs/README.md > README.rst

tests:
	python -m pytest
