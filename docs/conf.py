# Configuration file for the Sphinx documentation builder.
# this_file: docs/conf.py

import os
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path("../src").resolve()))

# -- Project information -----------------------------------------------------

project = "Vexy Markliff"
copyright = "2025, Vexy Markliff Developers"  # noqa: A001
author = "Vexy Markliff Developers"
release = "1.2.2"
version = "1.2.2"

# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.coverage",
    "sphinx.ext.mathjax",
    "sphinx.ext.ifconfig",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
    "sphinx.ext.napoleon",  # Google/NumPy style docstrings
    "sphinx.ext.autosummary",  # Generate summary tables
    "autoapi.extension",  # Auto-generate API docs
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

language = "en"

# -- Autodoc configuration --------------------------------------------------

autodoc_default_options = {
    "members": True,
    "member-order": "bysource",
    "special-members": "__init__",
    "undoc-members": True,
    "exclude-members": "__weakref__",
}

# Automatically generate summary pages
autosummary_generate = True

# -- AutoAPI configuration --------------------------------------------------

autoapi_type = "python"
autoapi_dirs = ["../src/vexy_markliff"]
autoapi_root = "api"
autoapi_add_toctree_entry = False
autoapi_keep_files = True
autoapi_python_class_content = "both"
autoapi_member_order = "bysource"

# Generate API documentation for all modules
autoapi_generate_api_docs = True

# -- Napoleon configuration -------------------------------------------------

napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output ------------------------------------------------

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

html_theme_options = {
    "canonical_url": "",
    "analytics_id": "",
    "logo_only": False,
    "display_version": True,
    "prev_next_buttons_location": "bottom",
    "style_external_links": False,
    "vcs_pageview_mode": "",
    "style_nav_header_background": "white",
    # Toc options
    "collapse_navigation": True,
    "sticky_navigation": True,
    "navigation_depth": 4,
    "includehidden": True,
    "titles_only": False,
}

html_title = f"{project} {version} Documentation"
html_short_title = f"{project} {version}"

# -- Options for intersphinx extension --------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://docs.pydantic.dev/latest/", None),
    "lxml": ("https://lxml.de/apidoc/", None),
}

# -- Options for todo extension ---------------------------------------------

todo_include_todos = True

# -- Doctest configuration --------------------------------------------------

doctest_global_setup = """
import sys
sys.path.insert(0, '../src')
from vexy_markliff import *
"""

# -- Coverage configuration -------------------------------------------------

coverage_show_missing_items = True
coverage_write_headline = False
coverage_skip_undoc_in_source = True
