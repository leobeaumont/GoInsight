.PHONY: help setup clean docs get-model opt-model

# Virtual environement
VENV=.venv
PYTHON=python3

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
NEURALNET_FILE = $(NEURALNET_DIR)/kata1-b28c512nbt-adam-s11165M-d5387M.bin.gz
NEURALNET_URL = https://media.katagotraining.org/uploaded/networks/models/kata1/kata1-b28c512nbt-adam-s11165M-d5387M.bin.gz
CONFIG_FILE = $(MODEL_DIR)/default_gtp.cfg
BENCHMARK_OUT = $(MODEL_DIR)/benchmark_output.txt

help:
	@echo "Available targets:"
	@echo "  make setup     - Check Python version, create venv, upgrade pip, install deps, build docs"
	@echo "  make docs      - Open docs"
	@echo "  make get-model - Download model"
	@echo "  make opt-model - Optimise model for your device (this command has a very long runtime ~30mins)"
	@echo "  make clean     - Remove venv, docs, model and logs"

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
	rm -rf $(VENV) $(BUILDDIR) $(MODEL_DIR) $(NEURALNET_DIR) gtp_logs
	@echo "Removed .venv, doc builds, model and logs"

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

get-model: $(MODEL_FILE) $(NEURALNET_FILE)
	@echo "Model ready !"

$(MODEL_FILE):
	mkdir -p $(MODEL_DIR)
	curl -L -o $(MODEL_FILE) $(MODEL_URL)
	unzip -d $(MODEL_DIR) $(MODEL_FILE)

$(NEURALNET_FILE):
	mkdir -p $(NEURALNET_DIR)
	curl -L -o $(NEURALNET_FILE) $(NEURALNET_URL)

opt-model: $(BENCHMARK_OUT)
	@echo "Benchmark done!"
	@optimal_threads=$$(grep "(recommended)" $(BENCHMARK_OUT) | sed -E 's/.*numSearchThreads = *([0-9]+).*/\1/'); \
	sed -i "332s/.*/numSearchThreads = $${optimal_threads}/" $(CONFIG_FILE); \
	echo "Changed number of search threads to $${optimal_threads}, optimisation done!"
	
$(BENCHMARK_OUT): $(MODEL_FILE) $(NEURALNET_FILE)
	@echo "Starting benchmark procedure, this will take a while... (crtl + C to cancel)"
	@sleep 5
	$(MODEL_DIR)/katago benchmark -model $(NEURALNET_FILE) -config $(CONFIG_FILE) | tee $(MODEL_DIR)/benchmark_output.txt