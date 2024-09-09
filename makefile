# Variables
VENV=venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip
BLACK=$(VENV)/bin/black
FLAKE8=$(VENV)/bin/flake8
PYTEST=$(VENV)/bin/pytest

# Phony targets (these targets don't correspond to files)
.PHONY: all install format lint test clean docs

# Default target: install dependencies
all: install

# Install dependencies in virtual environment
install: $(VENV)/bin/activate

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	$(PIP) install -r requirements.txt
	touch $(VENV)/bin/activate

# Format code with Black
format:
	$(BLACK) .

# Lint code with Flake8
lint:
	$(FLAKE8) .

# Run tests with pytest
test:
	$(PYTEST)

# Build the Sphinx documentation
docs:
	cd docs && $(MAKE) html

# Clean up virtual environment and other generated files
clean:
	rm -rf $(VENV)
	find . -type d -name '__pycache__' -exec rm -r {} +
	find . -type f -name '*.pyc' -delete
