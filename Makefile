.PHONY: help setup clean docs get-model

# Virtual environement
VENV=.venv
PYTHON=python3
REQUIRED_PYTHON=3.12.3

# Documentation
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build
HTMLDIR       = $(BUILDDIR)/html
INDEXFILE     = $(HTMLDIR)/index.html

# Katago model
MODEL_DIR = models
MODEL_FILE = $(MODEL_DIR)/katago.zip
MODEL_URL = https://github.com/lightvector/KataGo/releases/download/v1.16.3/katago-v1.16.3-cuda12.1-cudnn8.9.7-linux-x64.zip

help:
	@echo "Available targets:"
	@echo "  make setup     - Check Python version, create venv, upgrade pip, install deps, build docs"
	@echo "  make docs      - Open docs"
	@echo "  make get-model - Download model"
	@echo "  make clean     - Remove venv, docs and models"

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
	@echo "Building documentation..."
	$(VENV)/bin/$(SPHINXBUILD) -b html $(SOURCEDIR) $(HTMLDIR)
	@echo "Setup complete!"
	@echo "######################################"
	@echo "# Please run:                        #"
	@echo "#     source $(VENV)/bin/activate      #"
	@echo "#                                    #"
	@echo "######################################"

clean:
	rm -rf $(VENV) $(BUILDDIR) $(MODEL_DIR)
	@echo "Removed .venv, doc builds and models"

docs:
	@echo "Opening documentation..."
	@if [ "$$OS" = "Windows_NT" ]; then \
		start $(INDEXFILE); \
	elif command -v xdg-open > /dev/null; then \
		xdg-open $(INDEXFILE); \
	elif command -v open > /dev/null; then \
		open $(INDEXFILE); \
	else \
		echo "Please open $(INDEXFILE) manually."; \
	fi

get-model: $(MODEL_FILE)

$(MODEL_FILE):
	mkdir -p $(MODEL_DIR)
	curl -L -o $(MODEL_FILE) $(MODEL_URL)