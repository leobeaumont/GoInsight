.PHONY: help setup activate clean

VENV=.venv
PYTHON=python3
REQUIRED_PYTHON=3.12.3

help:
	@echo "Available targets:"
	@echo "  make setup     - Check Python version, create venv, upgrade pip, install deps"
	@echo "  make activate  - Show how to activate the venv"
	@echo "  make clean     - Remove venv"

setup:
	@echo "Checking Python version..."
	@version=`$(PYTHON) --version 2>&1 | awk '{print $$2}'`; \
	if [ "$$version" != "$(REQUIRED_PYTHON)" ]; then \
		echo "Python version must be $(REQUIRED_PYTHON), but found $$version"; \
		exit 1; \
	fi
	@echo "Python version is $(REQUIRED_PYTHON)"
	@echo "Creating virtual environment in $(VENV)..."
	$(PYTHON) -m venv $(VENV)
	@echo "Upgrading pip inside virtual environment..."
	$(VENV)/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	$(VENV)/bin/pip install -r requirements.txt
	@echo "Setup complete!"
	@echo "Please run: source $(VENV)/bin/activate"

clean:
	rm -rf $(VENV)
	@echo "Removed virtual environment"
