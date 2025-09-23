"""Pytest configuration and fixtures for vexy-markliff tests."""
# this_file: tests/conftest.py

from pathlib import Path
from typing import Any

import pytest

from vexy_markliff.core.parser import HTMLParser, MarkdownParser
from vexy_markliff.models.xliff import XLIFFDocument


@pytest.fixture
def markdown_parser() -> MarkdownParser:
    """Provide a configured MarkdownParser instance."""
    return MarkdownParser(enable_plugins=True)


@pytest.fixture
def html_parser() -> HTMLParser:
    """Provide an HTMLParser instance."""
    return HTMLParser()


@pytest.fixture
def sample_markdown_simple() -> str:
    """Provide simple Markdown content."""
    return """# Hello World

This is a simple paragraph with **bold** and *italic* text.

- Item 1
- Item 2
- Item 3"""


@pytest.fixture
def sample_markdown_complex() -> str:
    """Provide complex Markdown content with multiple features."""
    return """---
title: Test Document
author: John Doe
tags: [test, fixture]
---

# Main Title

## Introduction

This is a paragraph with **bold**, *italic*, and ***bold italic*** text.
It also has `inline code` and a [link](https://example.com).

### Features

- Task lists
- Tables
- Footnotes[^1]
- Code blocks

## Task List

- [x] Completed task
- [ ] Incomplete task
- [x] Another completed task

## Data Table

| Column A | Column B | Column C |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
| Value 4  | Value 5  | Value 6  |

## Code Example

```python
def hello_world():
    print("Hello, World!")
    return 42
```

## Blockquote

> This is a blockquote.
> It can span multiple lines.
>
> And have multiple paragraphs.

[^1]: This is a footnote content.

:::note
This is a note container with important information.
:::"""


@pytest.fixture
def sample_html_simple() -> str:
    """Provide simple HTML content."""
    return """<div>
    <h1>Hello World</h1>
    <p>This is a simple paragraph with <strong>bold</strong> and <em>italic</em> text.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
        <li>Item 3</li>
    </ul>
</div>"""


@pytest.fixture
def sample_html_complex() -> str:
    """Provide complex HTML content."""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test Document</title>
</head>
<body>
    <header>
        <h1 id="main-title">Main Title</h1>
        <nav>
            <a href="#intro">Introduction</a>
            <a href="#features">Features</a>
        </nav>
    </header>

    <main>
        <section id="intro">
            <h2>Introduction</h2>
            <p class="lead">This is a paragraph with <strong>bold</strong>,
            <em>italic</em>, and <strong><em>bold italic</em></strong> text.</p>
        </section>

        <section id="features">
            <h2>Features</h2>
            <table class="data-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Status</th>
                        <th>Priority</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>HTML Parsing</td>
                        <td>Complete</td>
                        <td>High</td>
                    </tr>
                    <tr>
                        <td>XLIFF Generation</td>
                        <td>In Progress</td>
                        <td>High</td>
                    </tr>
                </tbody>
            </table>
        </section>

        <form action="/submit" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <button type="submit">Submit</button>
        </form>
    </main>

    <footer>
        <p>&copy; 2025 Test Document</p>
    </footer>
</body>
</html>"""


@pytest.fixture
def xliff_document_empty() -> XLIFFDocument:
    """Provide an empty XLIFF document."""
    return XLIFFDocument(version="2.1", src_lang="en", tgt_lang="es")


@pytest.fixture
def xliff_document_with_file() -> XLIFFDocument:
    """Provide an XLIFF document with a file."""
    doc = XLIFFDocument(version="2.1", src_lang="en", tgt_lang="es")
    doc.add_file(
        file_id="file1",
        source_lang="en",
        target_lang="es",
        original="test.md",
    )
    return doc


@pytest.fixture
def xliff_document_with_units() -> XLIFFDocument:
    """Provide an XLIFF document with translation units."""
    doc = XLIFFDocument(version="2.1", src_lang="en", tgt_lang="es")
    doc.add_file(
        file_id="file1",
        source_lang="en",
        target_lang="es",
        original="test.md",
    )

    # Add some translation units
    doc.add_unit(
        file_id="file1",
        unit_id="u1",
        source="Hello World",
        target="Hola Mundo",
    )

    doc.add_unit(
        file_id="file1",
        unit_id="u2",
        source="This is a test",
        target="Esto es una prueba",
    )

    return doc


@pytest.fixture
def document_segment_factory() -> Any:
    """Provide a factory for creating DocumentSegment instances."""

    def factory(
        segment_id: str = "seg1",
        content: str = "Test content",
        segment_type: str = "paragraph",
        level: int = 0,
        metadata: dict[str, Any] | None = None,
    ) -> DocumentSegment:
        return DocumentSegment(
            id=segment_id,
            content=content,
            type=segment_type,
            level=level,
            metadata=metadata or {},
        )

    return factory


@pytest.fixture
def two_document_pair_factory() -> Any:
    """Provide a factory for creating TwoDocumentPair instances."""

    def factory(
        source_lang: str = "en",
        target_lang: str = "es",
        source_content: str = "Hello World",
        target_content: str = "Hola Mundo",
        source_format: str = "markdown",
        target_format: str = "markdown",
    ) -> TwoDocumentPair:
        return TwoDocumentPair(
            source_lang=source_lang,
            target_lang=target_lang,
            source_content=source_content,
            target_content=target_content,
            source_format=source_format,
            target_format=target_format,
        )

    return factory


@pytest.fixture
def sample_files_dir(tmp_path: Path) -> Path:
    """Create a temporary directory with sample files."""
    # Create sample Markdown file
    md_file = tmp_path / "sample.md"
    md_file.write_text("""# Sample Document

This is a sample Markdown document for testing.

## Features

- Bullet point 1
- Bullet point 2
- Bullet point 3

| Column 1 | Column 2 |
|----------|----------|
| Data 1   | Data 2   |
""")

    # Create sample HTML file
    html_file = tmp_path / "sample.html"
    html_file.write_text("""<html>
<body>
    <h1>Sample Document</h1>
    <p>This is a sample HTML document for testing.</p>
    <ul>
        <li>Item 1</li>
        <li>Item 2</li>
    </ul>
</body>
</html>""")

    # Create sample XLIFF file
    xliff_file = tmp_path / "sample.xlf"
    xliff_file.write_text("""<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.1" xmlns="urn:oasis:names:tc:xliff:document:2.1" srcLang="en" trgLang="es">
    <file id="f1" original="sample.md">
        <unit id="u1">
            <segment>
                <source>Sample Document</source>
                <target>Documento de Muestra</target>
            </segment>
        </unit>
    </file>
</xliff>""")

    return tmp_path


@pytest.fixture
def parallel_documents() -> tuple[str, str]:
    """Provide parallel source and target documents for alignment testing."""
    source = """# Introduction

This is the first paragraph of the introduction.

This is the second paragraph with more details.

## Features

The system has the following features:
- Feature one
- Feature two
- Feature three

## Conclusion

This concludes our document."""

    target = """# Introducción

Este es el primer párrafo de la introducción.

Este es el segundo párrafo con más detalles.

## Características

El sistema tiene las siguientes características:
- Característica uno
- Característica dos
- Característica tres

## Conclusión

Esto concluye nuestro documento."""

    return source, target


# Fixtures from deleted test_data_generators module removed for simplification
