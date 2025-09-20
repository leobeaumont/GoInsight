# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'GoInsight'
copyright = '2025, Beaumont Léo, Chambriard Léopold, Chouki Mouad, Disdier Jordan, Garrana Simon, Miranda-Gonzales Marcelo, Roubertou Amaury'
author = 'Beaumont Léo, Chambriard Léopold, Chouki Mouad, Disdier Jordan, Garrana Simon, Miranda-Gonzales Marcelo, Roubertou Amaury'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc']

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']

import os
import sys
sys.path.insert(0, os.path.abspath('../src'))  # adjust if your code is in src/
