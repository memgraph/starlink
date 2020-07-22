PYTHON=python3

# Runs a full installation
install:
	poetry install

# Runs the entire test suite and generates coverage report
test:
	poetry run python -m pytest

.PHONY: test install

.DEFAULT_GOAL := test
