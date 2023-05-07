.PHONY: linters test test-all

linters:
	mypy
	flake8 party_calc tests

test:
	pytest

test-all: linters test
