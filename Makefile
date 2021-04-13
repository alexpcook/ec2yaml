.PHONY: test

default: test

test:
	PYTHONPATH=./src pytest
