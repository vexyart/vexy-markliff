#!/usr/bin/env python3
"""
Markdown to XLIFF Workflow Example

This script demonstrates a practical workflow for converting Markdown
files to XLIFF format for translation, including round-trip processing.

Usage:
    python markdown_to_xliff_workflow.py
"""
# this_file: examples/markdown_to_xliff_workflow.py

import tempfile
from pathlib import Path

from vexy_markliff.core.element_classifier import HTMLElementClassifier
from vexy_markliff.core.format_style import FormatStyleSerializer
from vexy_markliff.core.parser import HTMLParser, MarkdownParser
from vexy_markliff.models.xliff import TranslationUnit, XLIFFDocument, XLIFFFile


def create_sample_markdown() -> str:
    """Create sample Markdown content for demonstration."""
    return """---
title: "Getting Started with Localization"
author: "Translation Team"
date: "2025-09-23"
---

# Introduction to Localization

Welcome to our comprehensive guide on **software localization**. This document
will help you understand the key concepts and best practices.

## What is Localization?

Localization (often abbreviated as *l10n*) is the process of adapting software
applications to different languages, regions, and cultures. It goes beyond
simple translation to include:

- Cultural adaptation of content
- Date and time format adjustments
- Currency and number format changes
- Legal and regulatory compliance

![Localization Process](images/localization-flow.png "Overview of the localization workflow")

## Benefits of Proper Localization

> "Localization is not just translation—it's about creating a native experience
> for your users in their own language and culture."
> — Localization Expert

### Key Advantages

1. **Increased Market Reach**
   Access new markets and customer segments effectively.

2. **Improved User Experience**
   Users feel more comfortable with native-language interfaces.

3. **Higher Conversion Rates**
   Studies show 75% of consumers prefer buying in their native language.

### Implementation Checklist

- [ ] Conduct market research for target locales
- [x] Set up internationalization framework
- [ ] Prepare content for translation
- [x] Choose appropriate CAT tools
- [ ] Test localized versions thoroughly

## Code Examples

Here's a simple example of internationalized code:

```python
# Good: Using localization keys
welcome_message = _("welcome_user", user_name=username)

# Bad: Hard-coded strings
welcome_message = f"Welcome, {username}!"
```

## Technical Considerations

When implementing localization, consider these technical aspects:

| Aspect | Consideration | Example |
|--------|---------------|---------|
| Text Expansion | Some languages require 30-50% more space | German compound words |
| RTL Languages | Right-to-left text direction | Arabic, Hebrew |
| Character Encoding | Use UTF-8 consistently | Unicode support |

## Conclusion

Effective localization requires careful planning and attention to detail.
For more information, visit our [documentation site](https://docs.example.com)
or contact us at <support@example.com>.

---

*This guide is part of our localization best practices series.*
"""


def demonstrate_markdown_parsing():
    """Show how to parse Markdown content."""

    parser = MarkdownParser()
    sample_md = create_sample_markdown()

    # Parse the Markdown
    result = parser.parse(sample_md)

    # Show front matter
    if result["front_matter"]:
        for _key, _value in result["front_matter"].items():
            pass

    return result


def demonstrate_html_analysis():
    """Analyze the generated HTML for XLIFF processing."""

    # Get HTML from Markdown parsing
    markdown_result = demonstrate_markdown_parsing()
    html_content = markdown_result["html"]

    # Parse HTML
    html_parser = HTMLParser()
    html_result = html_parser.parse(html_content)

    # Analyze elements for XLIFF classification
    classifier = HTMLElementClassifier()

    element_stats = {}
    for element in html_result["elements"]:
        tag_name = element["tag"]
        xliff_type = classifier.get_xliff_representation(tag_name)

        if xliff_type not in element_stats:
            element_stats[xliff_type] = []
        element_stats[xliff_type].append(tag_name)

    for _xliff_type, tags in element_stats.items():
        list(set(tags))

    return html_result


def create_sample_xliff():
    """Create a sample XLIFF document."""

    # Create XLIFF document
    xliff_doc = XLIFFDocument(version="2.1", src_lang="en", tgt_lang="es")

    # Create file
    xliff_file = XLIFFFile(id="markdown_sample", original="sample.md")

    # Add translation units
    units = [
        TranslationUnit(id="title", source="Introduction to Localization", target="Introducción a la Localización"),
        TranslationUnit(
            id="welcome",
            source="Welcome to our comprehensive guide on **software localization**.",
            target="Bienvenido a nuestra guía completa sobre **localización de software**.",
            fs_fs="p",
            fs_subfs="class,intro",
        ),
        TranslationUnit(
            id="definition",
            source=(
                "Localization (often abbreviated as *l10n*) is the process of adapting software "
                "applications to different languages, regions, and cultures."
            ),
            target=(
                "La localización (frecuentemente abreviada como *l10n*) es el proceso de adaptar "
                "aplicaciones de software a diferentes idiomas, regiones y culturas."
            ),
            fs_fs="p",
        ),
        TranslationUnit(
            id="quote",
            source=(
                "Localization is not just translation—it's about creating a native experience "
                "for your users in their own language and culture."
            ),
            target=(
                "La localización no es solo traducción—se trata de crear una experiencia nativa "
                "para sus usuarios en su propio idioma y cultura."
            ),
            fs_fs="blockquote",
        ),
    ]

    # Add units to file
    for unit in units:
        xliff_file.add_unit(unit)

    # Add file to document
    xliff_doc.add_file(xliff_file)

    # Show sample unit details
    units[1]  # Welcome message

    return xliff_doc


def save_and_process_files():
    """Demonstrate saving and processing files."""

    # Create temporary directory for demo files
    with tempfile.TemporaryDirectory(prefix="vexy_markliff_demo_") as temp_dir:
        temp_path = Path(temp_dir)

        # Save sample Markdown file
        md_file = temp_path / "sample.md"
        md_content = create_sample_markdown()
        md_file.write_text(md_content, encoding="utf-8")

        # Process Markdown to HTML
        parser = MarkdownParser()
        result = parser.parse(md_content)

        html_file = temp_path / "sample.html"
        html_file.write_text(result["html"], encoding="utf-8")

        # Create XLIFF document
        create_sample_xliff()

        # Note: In a real implementation, we would have a to_xml() method
        # For demo purposes, we'll show the structure
        xliff_file = temp_path / "sample.xlf"

        # Simulate XLIFF XML content
        xliff_xml = """<?xml version="1.0" encoding="UTF-8"?>
<xliff version="2.1" srcLang="en" trgLang="es" xmlns="urn:oasis:names:tc:xliff:document:2.1">
  <file id="markdown_sample" original="sample.md">
    <unit id="title">
      <segment>
        <source>Introduction to Localization</source>
        <target>Introducción a la Localización</target>
      </segment>
    </unit>
    <unit id="welcome" fs:fs="p" fs:subFs="class,intro" xmlns:fs="urn:oasis:names:tc:xliff:fs:2.0">
      <segment>
        <source>Welcome to our comprehensive guide on **software localization**.</source>
        <target>Bienvenido a nuestra guía completa sobre **localización de software**.</target>
      </segment>
    </unit>
    <!-- Additional units would be here -->
  </file>
</xliff>"""

        xliff_file.write_text(xliff_xml, encoding="utf-8")

        # Show file sizes
        for file_path in [md_file, html_file, xliff_file]:



def demonstrate_format_style_features():
    """Show Format Style module features."""

    serializer = FormatStyleSerializer()

    # Test complex attribute scenarios
    test_cases = [
        {"name": "Simple attributes", "attrs": {"class": "highlight", "id": "content"}},
        {
            "name": "Attributes with special characters",
            "attrs": {"href": "https://example.com?param=value&other=data", "title": "Click here, please!"},
        },
        {"name": "Boolean and empty attributes", "attrs": {"disabled": "", "checked": "", "data-value": "test"}},
        {
            "name": "Complex formatting",
            "attrs": {"style": "color: red; font-weight: bold;", "data-config": "option1,option2,option3"},
        },
    ]

    for test_case in test_cases:
        attrs = test_case["attrs"]

        # Serialize
        serialized = serializer.serialize_attributes(attrs)

        # Deserialize
        serializer.deserialize_attributes(serialized)

    # Test inline serialization
    inline_result = serializer.serialize_inline_attributes("a", {"href": "https://example.com", "target": "_blank"})

    tag, attrs = serializer.deserialize_inline_attributes(inline_result)


def main():
    """Run the complete workflow demonstration."""

    try:
        # Run all demonstrations
        demonstrate_markdown_parsing()
        demonstrate_html_analysis()
        create_sample_xliff()
        save_and_process_files()
        demonstrate_format_style_features()

    except Exception:
        raise


if __name__ == "__main__":
    main()
