# nkscraper Documentation

https://funadaya13.github.io/nkscraper/

### ドキュメント作成手順

<pre>
mkdir docs-workspace
sphinx-quickstart docs-workspace
</pre>
conf.py の修正
<pre>
# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'nksraper'
copyright = '2023, funadaya13'
author = 'funadaya13'
release = '0.1.0'
version = '0.1.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',   # ソースコード読み込み用
    'sphinx.ext.napoleon',  # docstring パース用
    'sphinx_rtd_theme',     # Read the Docs テーマ
]

templates_path = ['_templates']


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

</pre>

<pre>
sphinx-apidoc -f -e -o docs-workspace/source nkscraper
sphinx-build -a docs-workspace/source docs-workspace/build
</pre>
