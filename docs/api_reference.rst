Vexy Markliff API Reference
===========================

This section provides comprehensive API documentation for all modules, classes, and functions
in the Vexy Markliff package, with practical examples and integration patterns.

.. contents:: Table of Contents
   :local:
   :depth: 3

Quick Start Guide
-----------------

Core Components Overview
~~~~~~~~~~~~~~~~~~~~~~~~~

The Vexy Markliff package provides these main components:

* :class:`~vexy_markliff.core.converter.VexyMarkliff` - Main conversion orchestrator
* :class:`~vexy_markliff.config.ConversionConfig` - Configuration management
* :class:`~vexy_markliff.cli.VexyMarkliffCLI` - Command-line interface
* Processing modules for HTML/Markdown parsing and XLIFF generation

Basic Usage Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from vexy_markliff import VexyMarkliff
    from vexy_markliff.config import ConversionConfig

    # Basic conversion
    converter = VexyMarkliff()
    markdown = "# Welcome\n\nHello **world**!"
    xliff = converter.markdown_to_xliff(markdown, "en", "es")

    # With custom configuration
    config = ConversionConfig(split_sentences=True, preserve_whitespace=False)
    converter = VexyMarkliff(config)
    xliff = converter.markdown_to_xliff(markdown, "en", "fr")

Complete Workflow Example
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from pathlib import Path
    from vexy_markliff import VexyMarkliff
    from vexy_markliff.config import ConversionConfig

    # Load configuration from file
    config = ConversionConfig.from_file(Path("config.yaml"))
    converter = VexyMarkliff(config)

    # Convert Markdown to XLIFF
    with open("document.md", "r") as f:
        markdown_content = f.read()

    xliff_content = converter.markdown_to_xliff(
        markdown_content, source_lang="en", target_lang="es"
    )

    # Save XLIFF output
    with open("document.xlf", "w") as f:
        f.write(xliff_content)

    # Round-trip conversion back to Markdown
    restored_markdown = converter.xliff_to_markdown(xliff_content)

Core Modules
------------

Main Converter
~~~~~~~~~~~~~~

.. automodule:: vexy_markliff
   :members:
   :undoc-members:
   :show-inheritance:

**Key Features:**

* Package-level convenience functions for common operations
* Main entry point for conversion workflows
* Integration with configuration and CLI systems

Converter Engine
~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.converter
   :members:
   :undoc-members:
   :show-inheritance:

**Performance Features:**

* LRU caching for language validation (up to 256 entries)
* Pre-compiled regex patterns for optimal processing speed
* Generator-based segment extraction for memory efficiency
* Consolidated validation functions to minimize overhead

**Integration Points:**

* Uses :class:`~vexy_markliff.core.parser.MarkdownParser` and :class:`~vexy_markliff.core.parser.HTMLParser`
* Integrates with :class:`~vexy_markliff.core.element_classifier.HTMLElementClassifier`
* Leverages validation utilities from :mod:`~vexy_markliff.utils.validation`

Configuration
-------------

.. automodule:: vexy_markliff.config
   :members:
   :undoc-members:
   :show-inheritance:

**Configuration Examples:**

Basic Configuration:

.. code-block:: python

    from vexy_markliff.config import ConversionConfig, ConversionMode, StorageMode

    # Default configuration
    config = ConversionConfig()
    print(f"Source: {config.source_language}, Target: {config.target_language}")

    # Custom configuration with all options
    config = ConversionConfig(
        source_language="fr",
        target_language="de",
        mode=ConversionMode.TWO_DOC,  # or "two-doc"
        storage=StorageMode.BOTH,     # or "both"
        markdown_extensions=["tables", "footnotes", "task_lists"],
        split_sentences=True,
        preserve_whitespace=True,
        max_file_size_mb=100
    )

YAML Configuration File:

.. code-block:: yaml

    # config.yaml
    source_language: en
    target_language: es
    mode: one-doc              # one-doc | two-doc
    storage: source            # source | target | both
    markdown_extensions:
      - tables
      - footnotes
      - task_lists
      - strikethrough
    split_sentences: true
    preserve_whitespace: false
    max_file_size_mb: 50

Loading and Saving Configuration:

.. code-block:: python

    from pathlib import Path
    from vexy_markliff.config import ConversionConfig

    # Load from YAML file
    config = ConversionConfig.from_file(Path("config.yaml"))

    # Modify and save
    config.target_language = "fr"
    config.to_file(Path("updated-config.yaml"))

    # Validate file paths securely
    safe_path = config.validate_file_path(Path("./safe/file.txt"))

Environment Variable Support:

.. code-block:: python

    import os
    from vexy_markliff.config import load_config_with_env_override

    # Set environment variables
    os.environ["VEXY_SOURCE_LANG"] = "de"
    os.environ["VEXY_TARGET_LANG"] = "en"
    os.environ["VEXY_MODE"] = "two-doc"

    # Load with environment overrides
    config = load_config_with_env_override()  # Uses env vars
    config = load_config_with_env_override(Path("base-config.yaml"))  # File + env

CLI Interface
-------------

.. automodule:: vexy_markliff.cli
   :members:
   :undoc-members:
   :show-inheritance:

**CLI Usage Examples:**

Basic Conversion Commands:

.. code-block:: bash

    # Convert Markdown to XLIFF
    vexy-markliff md2xliff document.md document.xlf --source-lang en --target-lang es

    # Convert HTML to XLIFF
    vexy-markliff html2xliff page.html page.xlf --source-lang en --target-lang fr

    # Convert XLIFF back to Markdown
    vexy-markliff xliff2md translated.xlf result.md

    # Convert XLIFF back to HTML
    vexy-markliff xliff2html translated.xlf result.html

Advanced CLI Options:

.. code-block:: bash

    # Use configuration file
    vexy-markliff --config my-config.yaml md2xliff source.md output.xlf

    # Enable verbose logging with log file
    vexy-markliff --verbose --log-file debug.log md2xliff document.md document.xlf

    # Dry run mode (validate without writing files)
    vexy-markliff md2xliff document.md document.xlf --dry-run

    # Show help for specific command
    vexy-markliff md2xliff --help

Programmatic CLI Usage:

.. code-block:: python

    from vexy_markliff.cli import VexyMarkliffCLI

    # Initialize CLI with options
    cli = VexyMarkliffCLI(verbose=True, log_file="debug.log")

    # Convert files programmatically
    cli.md2xliff("document.md", "document.xlf", "en", "es")

    # Use dry run mode
    cli_dry = VexyMarkliffCLI(dry_run=True)
    cli_dry.md2xliff("test.md", "test.xlf", "en", "fr")  # Validates but doesn't write

Parser Modules
--------------

HTML and Markdown Parser
~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.parser
   :members:
   :undoc-members:
   :show-inheritance:

**Markdown Parsing Examples:**

.. code-block:: python

    from vexy_markliff.core.parser import MarkdownParser

    parser = MarkdownParser()

    # Parse Markdown to structured data
    markdown_content = """
    # Main Title

    This is a paragraph with **bold** and *italic* text.

    ## Subsection

    - List item 1
    - List item 2 with [link](https://example.com)

    ```python
    # Code block example
    print("Hello, world!")
    ```
    """

    result = parser.parse(markdown_content)
    print("Tokens:", len(result['tokens']))
    print("HTML output:", result['html'][:100] + "...")
    print("Metadata:", result.get('metadata', {}))

    # Direct HTML rendering
    html_output = parser.render_html(markdown_content)

**HTML Parsing Examples:**

.. code-block:: python

    from vexy_markliff.core.parser import HTMLParser

    parser = HTMLParser()

    html_content = """
    <html>
    <body>
        <h1 class="title">Document Title</h1>
        <p>Paragraph with <strong class="highlight">emphasis</strong>.</p>
        <ul>
            <li>First item</li>
            <li>Second item with <a href="link.html">link</a></li>
        </ul>
        <div class="content">
            <p>Another paragraph.</p>
        </div>
    </body>
    </html>
    """

    result = parser.parse(html_content)
    print("Root element:", result['tree'].tag)
    print("Text elements found:", len(result['elements']))
    print("Extracted text:", result['text'][:100] + "...")

    # Access parsed tree for advanced processing
    tree = result['tree']
    paragraphs = tree.xpath('//p')
    for i, p in enumerate(paragraphs):
        print(f"Paragraph {i+1}: {p.text}")

**Plugin Configuration for Markdown:**

.. code-block:: python

    from vexy_markliff.core.parser import MarkdownParser

    # Parser with all supported plugins
    parser = MarkdownParser(
        plugins=[
            "tables",        # GitHub-style tables
            "footnotes",     # Footnote support
            "task_lists",    # - [ ] Task lists
            "strikethrough", # ~~strikethrough~~
            "front_matter",  # YAML front matter
            "containers"     # Custom containers
        ]
    )

    # Test advanced features
    advanced_md = """
    ---
    title: "Test Document"
    author: "Test Author"
    ---

    # Document with Advanced Features

    | Column 1 | Column 2 |
    |----------|----------|
    | Data 1   | Data 2   |

    - [x] Completed task
    - [ ] Pending task

    ~~Strikethrough text~~

    Here's a footnote[^1].

    [^1]: This is the footnote content.
    """

    result = parser.parse(advanced_md)
    print("Front matter:", result.get('front_matter', {}))
    print("HTML with tables:", 'table' in result['html'])

Element Classification
~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.element_classifier
   :members:
   :undoc-members:
   :show-inheritance:

**Element Classification Examples:**

.. code-block:: python

    from vexy_markliff.core.element_classifier import HTMLElementClassifier, ElementCategory

    classifier = HTMLElementClassifier()

    # Classify different HTML elements
    elements_to_test = [
        "p", "div", "section", "article",    # Block elements
        "strong", "em", "a", "span",         # Inline elements
        "img", "br", "hr", "input",          # Void elements
        "table", "tr", "td", "th",           # Table elements
        "ul", "ol", "li",                    # List elements
        "form", "button", "select",          # Form elements
        "video", "audio", "source",          # Media elements
        "script", "style", "meta",           # Non-translatable elements
    ]

    for element in elements_to_test:
        category = classifier.classify(element)
        xliff_repr = classifier.get_xliff_representation(element)
        segmentation = classifier.get_segmentation_strategy(element)

        print(f"{element:8} -> {category.name:12} | XLIFF: {xliff_repr:11} | Segment: {segmentation}")

    # Example output:
    # p        -> FLOW_TEXT    | XLIFF: unit        | Segment: sentence
    # div      -> SECTIONING  | XLIFF: group       | Segment: element
    # strong   -> INLINE      | XLIFF: marker      | Segment: preserve
    # img      -> VOID        | XLIFF: placeholder | Segment: preserve

**Processing Strategy Examples:**

.. code-block:: python

    # Check element processing requirements
    def analyze_element(element_name):
        classifier = HTMLElementClassifier()

        return {
            'category': classifier.classify(element_name),
            'xliff_type': classifier.get_xliff_representation(element_name),
            'is_translatable': classifier.is_translatable_unit(element_name),
            'is_group': classifier.is_group_element(element_name),
            'is_inline': classifier.is_inline_element(element_name),
            'is_void': classifier.is_void_element(element_name),
            'preserve_whitespace': classifier.requires_whitespace_preservation(element_name),
            'extract_attributes': classifier.should_extract_attributes(element_name),
            'important_attrs': classifier.get_important_attributes(element_name),
            'segmentation': classifier.get_segmentation_strategy(element_name)
        }

    # Analyze different element types
    for element in ["p", "div", "strong", "img", "table", "code"]:
        analysis = analyze_element(element)
        print(f"\n{element.upper()} element analysis:")
        for key, value in analysis.items():
            print(f"  {key}: {value}")

**Custom Element Handling:**

.. code-block:: python

    # Example of how elements are processed based on classification
    def process_element_by_type(element_name, content, attributes):
        classifier = HTMLElementClassifier()
        xliff_type = classifier.get_xliff_representation(element_name)

        if xliff_type == "unit":
            # Create translation unit for translatable elements
            return create_translation_unit(element_name, content, attributes)
        elif xliff_type == "group":
            # Create group for structural elements
            return create_group_element(element_name, attributes)
        elif xliff_type == "marker":
            # Create inline marker for formatting elements
            return create_mrk_element(element_name, content, attributes)
        elif xliff_type == "placeholder":
            # Create placeholder for void elements
            return create_ph_element(element_name, attributes)
        elif xliff_type == "skeleton":
            # Add to skeleton for non-translatable elements
            return add_to_skeleton(element_name, content, attributes)

    # Note: These helper functions would be implemented using
    # the actual XLIFF generation modules

Format Style Handling
~~~~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.format_style
   :members:
   :undoc-members:
   :show-inheritance:

Inline Element Handling
~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.inline_handler
   :members:
   :undoc-members:
   :show-inheritance:

Structure Handling
~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.structure_handler
   :members:
   :undoc-members:
   :show-inheritance:

Skeleton Generation
~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.core.skeleton_generator
   :members:
   :undoc-members:
   :show-inheritance:

Data Models
-----------

Document Pair Models
~~~~~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.models.document_pair
   :members:
   :undoc-members:
   :show-inheritance:

XLIFF Models
~~~~~~~~~~~~

.. automodule:: vexy_markliff.models.xliff
   :members:
   :undoc-members:
   :show-inheritance:

Utilities
---------

Logging
~~~~~~~

.. automodule:: vexy_markliff.utils.logging
   :members:
   :undoc-members:
   :show-inheritance:

Text Processing
~~~~~~~~~~~~~~~

.. automodule:: vexy_markliff.utils.text
   :members:
   :undoc-members:
   :show-inheritance:

Validation
~~~~~~~~~~

.. automodule:: vexy_markliff.utils.validation
   :members:
   :undoc-members:
   :show-inheritance:

Exceptions
----------

.. automodule:: vexy_markliff.exceptions
   :members:
   :undoc-members:
   :show-inheritance:

Examples with Doctests
----------------------

The following examples demonstrate how to use the API and include executable doctests:

Basic Configuration
~~~~~~~~~~~~~~~~~~~

.. doctest::

   >>> from vexy_markliff.config import ConversionConfig
   >>> config = ConversionConfig()
   >>> config.source_language
   'en'
   >>> config.target_language
   'es'

HTML Element Classification
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. doctest::

   >>> from vexy_markliff.core.element_classifier import HTMLElementClassifier
   >>> classifier = HTMLElementClassifier()
   >>> classifier.classify_element("p")
   <ElementType.FLOW_TEXT: 'flow_text'>
   >>> classifier.classify_element("strong")
   <ElementType.INLINE: 'inline'>

Format Style Serialization
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. doctest::

   >>> from vexy_markliff.core.format_style import FormatStyleSerializer
   >>> serializer = FormatStyleSerializer()
   >>> attrs = {"class": "highlight", "id": "main"}
   >>> serialized = serializer.serialize_attributes(attrs)
   >>> "class=highlight" in serialized
   True
