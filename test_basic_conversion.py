#!/usr/bin/env python3
"""Basic test of core conversion functionality after radical simplification."""

import sys

sys.path.insert(0, "src")

from vexy_markliff.core.converter import VexyMarkliff


def test_basic_markdown_to_xliff():
    """Test basic Markdown to XLIFF conversion."""
    converter = VexyMarkliff()

    # Simple Markdown content
    markdown_content = """# Hello World

This is a simple paragraph with **bold** text.

- Item 1
- Item 2
"""

    try:
        # Convert to XLIFF
        converter.markdown_to_xliff(markdown_content, "en", "es")
        return True
    except Exception:
        return False


def test_basic_html_to_xliff():
    """Test basic HTML to XLIFF conversion."""
    converter = VexyMarkliff()

    # Simple HTML content
    html_content = """<h1>Hello World</h1>
<p>This is a simple paragraph with <strong>bold</strong> text.</p>
<ul>
  <li>Item 1</li>
  <li>Item 2</li>
</ul>"""

    try:
        # Convert to XLIFF
        converter.html_to_xliff(html_content, "en", "fr")
        return True
    except Exception:
        return False


def test_round_trip():
    """Test round-trip conversion (Markdown → XLIFF → Markdown)."""
    converter = VexyMarkliff()

    original_markdown = "# Test Title\n\nThis is a test paragraph."

    try:
        # Convert to XLIFF
        xliff = converter.markdown_to_xliff(original_markdown, "en", "de")

        # Convert back to Markdown
        converter.xliff_to_markdown(xliff)

        return True
    except Exception:
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    results = []
    results.append(test_basic_markdown_to_xliff())
    results.append(test_basic_html_to_xliff())
    results.append(test_round_trip())

    if all(results):
        sys.exit(0)
    else:
        sys.exit(1)
