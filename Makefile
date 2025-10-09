.PHONY: help setup clean docs

# Virtual environement
VENV=.venv
PYTHON=python3

# Documentation
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build
HTMLDIR       = $(BUILDDIR)/html
INDEXFILE     = $(HTMLDIR)/index.html

help:
	@echo "Available targets:"
	@echo "  make setup     - Check Python version, create venv, upgrade pip, install deps, build docs"
	@echo "  make docs      - Open docs"
	@echo "  make clean     - Remove venv and docs"

setup: $(BUILDDIR)
	@echo "Setup complete!"
	@echo "######################################"
	@echo "# Please run:                        #"
	@echo "#     source $(VENV)/bin/activate      #"
	@echo "#                                    #"
	@echo "######################################"

$(BUILDDIR): $(VENV)
	@echo "Building documentation..."
	$(VENV)/bin/$(SPHINXBUILD) -b html $(SOURCEDIR) $(HTMLDIR)

$(VENV):
	@echo "Creating virtual environment in $(VENV)..."
	$(PYTHON) -m venv $(VENV)
	@echo "Upgrading pip inside virtual environment..."
	$(VENV)/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	$(VENV)/bin/pip install -r requirements.txt

clean:
	rm -rf $(VENV) $(BUILDDIR)
	@echo "Removed virtual environment"

docs:
	@echo "Opening documentation..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(INDEXFILE); \
	elif command -v open > /dev/null; then \
		open $(INDEXFILE); \
	else \
		echo "Please open $(INDEXFILE) manually."; \
	fi