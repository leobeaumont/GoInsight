.PHONY: help setup clean docs get-model opt-model run-model tests check-python

# Virtual environement
VENV=.venv
PYTHON=python3
MIN_PYTHON_VERSION=3.7

# Documentation
SPHINXBUILD   = sphinx-build
SOURCEDIR     = docs
BUILDDIR      = docs/_build
HTMLDIR       = $(BUILDDIR)/html
INDEXFILE     = $(HTMLDIR)/index.html

# Katago model
MODEL_DIR = model
MODEL_FILE = $(MODEL_DIR)/katago.zip
MODEL_URL = https://github.com/lightvector/KataGo/releases/download/v1.16.3/katago-v1.16.3-eigen-linux-x64.zip
NEURALNET_DIR = neuralnet
NEURALNET_FILE = $(NEURALNET_DIR)/g170e-b10c128-s1141046784-d204142634.bin.gz
NEURALNET_URL = https://katagoarchive.org/g170/neuralnets/g170e-b10c128-s1141046784-d204142634.bin.gz
CONFIG_FILE = $(MODEL_DIR)/default_gtp.cfg
BENCHMARK_OUT = $(MODEL_DIR)/benchmark_output.txt
OS := $(shell uname)

help:
	@echo "Available targets:"
	@echo "  make setup     - Check python version, create venv, upgrade pip, install deps, build docs"
	@echo "  make docs      - Open docs"
	@echo "  make tests     - Run tests"
	@echo "  make get-model - Download model"
	@echo "  make opt-model - Optimise model for your device (this will take a few minutes)"
	@echo "  make run-model - Start a gtp session with the model"
	@echo "  make clean     - Remove venv, docs, model and logs"

setup:  $(BUILDDIR)
	@echo "Setup complete!"
	@echo "######################################"
	@echo "# Please run:                        #"
	@echo "#     source $(VENV)/bin/activate      #"
	@echo "#                                    #"
	@echo "######################################"

check-python:
	@echo "Checking python version ..."; \
	PYTHON_VERSION=$$($(PYTHON) -c 'import sys; print(".".join(map(str, sys.version_info[:3])))'); \
	echo "Python version: $$PYTHON_VERSION"; \
	REQUIRED=$(MIN_PYTHON_VERSION); \
	CURRENT_MAJOR=$$(echo $$PYTHON_VERSION | cut -d. -f1); \
	CURRENT_MINOR=$$(echo $$PYTHON_VERSION | cut -d. -f2); \
	REQUIRED_MAJOR=$$(echo $$REQUIRED | cut -d. -f1); \
	REQUIRED_MINOR=$$(echo $$REQUIRED | cut -d. -f2); \
	if [ $$CURRENT_MAJOR -lt $$REQUIRED_MAJOR ] || ([ $$CURRENT_MAJOR -eq $$REQUIRED_MAJOR ] && [ $$CURRENT_MINOR -lt $$REQUIRED_MINOR ]); then \
		echo "Python $$REQUIRED or higher is required. Found $$PYTHON_VERSION."; \
		exit 1; \
	fi

$(BUILDDIR): $(VENV)
	@echo "Building documentation..."
	$(VENV)/bin/$(SPHINXBUILD) -b html $(SOURCEDIR) $(HTMLDIR)

$(VENV): check-python
	@echo "Creating virtual environment in $(VENV)..."
	$(PYTHON) -m venv $(VENV)
	@echo "Upgrading pip inside virtual environment..."
	$(VENV)/bin/pip install --upgrade pip
	@echo "Installing dependencies..."
	$(VENV)/bin/pip install -r requirements.txt

clean:
	rm -rf $(VENV) $(BUILDDIR) $(MODEL_DIR) $(NEURALNET_DIR) gtp_logs
	@echo "Removed .venv, doc builds, model and logs"
	@if [ "$$(uname)" = "Darwin" ]; then \
		echo "Uninstalling KataGo via Homebrew..."; \
		brew uninstall katago; \
	fi

docs:
	@echo "Opening documentation..."
	@if command -v xdg-open > /dev/null; then \
		xdg-open $(INDEXFILE); \
	elif command -v open > /dev/null; then \
		open $(INDEXFILE); \
	else \
		echo "Please open $(INDEXFILE) manually."; \
	fi

get-model: $(MODEL_FILE) $(NEURALNET_FILE)
	@echo "Model ready !" 

$(MODEL_FILE):
	mkdir -p $(MODEL_DIR)
	curl -L -o $(MODEL_FILE) $(MODEL_URL)
	unzip -d $(MODEL_DIR) $(MODEL_FILE)
	@if [ "$$(uname)" = "Darwin" ]; then \
		if command -v brew >/dev/null 2>&1; then \
			echo "Homebrew already installed."; \
		else \
			echo "Homebrew not installed, you will need to install it manually to continue."; \
		fi; \
		echo "You are on macOS, installing KataGo via Homebrew..."; \
		brew install katago; \
	fi

$(NEURALNET_FILE):
	mkdir -p $(NEURALNET_DIR)
	curl -L -o $(NEURALNET_FILE) $(NEURALNET_URL)

opt-model: $(BENCHMARK_OUT)
	@echo "Benchmark done!"
	@optimal_threads=$$(grep "(recommended)" $(BENCHMARK_OUT) | sed -E 's/.*numSearchThreads = *([0-9]+).*/\1/'); \
	line_num=$$(grep -n "^numSearchThreads" $(CONFIG_FILE) | cut -d: -f1); \
	sed -i "$${line_num}s/.*/numSearchThreads = $${optimal_threads}/" $(CONFIG_FILE); \
	echo "Changed number of search threads to $${optimal_threads}, optimisation done!"
	
$(BENCHMARK_OUT): $(MODEL_FILE) $(NEURALNET_FILE)
	@echo "Starting benchmark procedure, this will take a while... (crtl + C to cancel)"
	@sleep 5
	@if [ "$$(uname)" = "Darwin" ]; then \
		katago benchmark -model $(NEURALNET_FILE) -config $(CONFIG_FILE) | tee $(MODEL_DIR)/benchmark_output.txt; \
	else \
		$(MODEL_DIR)/katago benchmark -model $(NEURALNET_FILE) -config $(CONFIG_FILE) | tee $(MODEL_DIR)/benchmark_output.txt; \
	fi

run-model: $(MODEL_FILE) $(NEURALNET_FILE)
	@echo "Starting KataGo..."
	@if [ "$$(uname)" = "Darwin" ]; then \
		katago gtp -model '$(NEURALNET_FILE)' -config '$(CONFIG_FILE)'; \
	else \
		$(MODEL_DIR)/katago gtp -model $(NEURALNET_FILE) -config $(CONFIG_FILE); \
	fi

tests:
	$(VENV)/bin/python3 -m pytest -v