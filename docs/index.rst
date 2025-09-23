Vexy Markliff Documentation
============================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   quickstart
   user_guide
   api_reference
   examples
   contributing


Overview
--------

Vexy Markliff is a Python package and CLI tool for bidirectional conversion between
Markdown/HTML and XLIFF 2.1 format, enabling high-fidelity localization workflows.

Key Features
------------

* **Bidirectional Conversion**: Seamless Markdown ↔ XLIFF and HTML ↔ XLIFF conversion
* **XLIFF 2.1 Compliant**: Full compliance with OASIS XLIFF 2.1 standard
* **Format Style Module**: Preserves HTML attributes and structure using fs:fs and fs:subFs
* **ITS 2.0 Support**: Native integration with W3C Internationalization Tag Set
* **Flexible Modes**: One-document and two-document translation workflows
* **Round-trip Fidelity**: Lossless Markdown → XLIFF → Markdown conversion
* **Intelligent Segmentation**: Smart sentence splitting for translation units
* **Skeleton Management**: External skeleton files for document structure preservation
* **Rich CLI**: Comprehensive command-line interface built with Fire
* **Modern Python**: Type hints, Pydantic models, and async support

Quick Start
-----------

Installation::

    pip install vexy-markliff

Basic usage::

    # Convert Markdown to XLIFF
    vexy-markliff md2xliff document.md document.xlf

    # Convert HTML to XLIFF
    vexy-markliff html2xliff page.html page.xlf

    # Convert XLIFF back to Markdown
    vexy-markliff xliff2md translated.xlf result.md

Python API usage:

.. doctest::

    >>> from vexy_markliff import VexyMarkliff
    >>> converter = VexyMarkliff()
    >>> # Example will be added when core functionality is complete

Documentation Sections
-----------------------

* **Quick Start**: Get up and running quickly with basic examples
* **User Guide**: Comprehensive guide to using Vexy Markliff
* **API Reference**: Complete API documentation with examples
* **Examples**: Real-world usage examples and patterns
* **Contributing**: Guidelines for contributing to the project

Supported Formats
------------------

**Markdown Elements:**

* CommonMark compliant base
* Tables (GitHub Flavored Markdown)
* Task lists and strikethrough
* Footnotes and front matter
* Raw HTML passthrough

**HTML Elements:**

* All HTML5 structural elements
* Text content elements (p, h1-h6, etc.)
* Inline formatting (strong, em, a, etc.)
* Tables with complex structures
* Forms, inputs, and media elements

**XLIFF Features:**

* XLIFF 2.1 Core compliance
* Format Style (fs) module for attribute preservation
* ITS 2.0 metadata support
* Translation unit notes and preserve space handling
* External skeleton files and inline element protection

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
