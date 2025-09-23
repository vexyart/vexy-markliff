"""Test suite for vexy_markliff."""
# this_file: tests/test_package.py

from __future__ import annotations

import pytest

from vexy_markliff import VexyMarkliff, __version__


def test_version_is_exposed() -> None:
    """Package exposes version metadata."""
    assert __version__
    assert isinstance(__version__, str)
    assert len(__version__) > 0


def test_main_converter_can_be_imported() -> None:
    """Main VexyMarkliff converter can be imported and instantiated."""
    converter = VexyMarkliff()
    assert converter is not None


def test_basic_markdown_to_xliff_conversion() -> None:
    """Basic Markdown to XLIFF conversion works."""
    converter = VexyMarkliff()
    markdown = "# Hello World\n\nThis is a test."

    # This should not raise an exception
    xliff = converter.markdown_to_xliff(markdown, "en", "es")
    assert xliff is not None
    assert isinstance(xliff, str)
    assert len(xliff) > 0
    assert "xliff" in xliff.lower()


def test_basic_html_to_xliff_conversion() -> None:
    """Basic HTML to XLIFF conversion works."""
    converter = VexyMarkliff()
    html = "<h1>Hello World</h1><p>This is a test.</p>"

    # This should not raise an exception
    xliff = converter.html_to_xliff(html, "en", "es")
    assert xliff is not None
    assert isinstance(xliff, str)
    assert len(xliff) > 0
    assert "xliff" in xliff.lower()


def test_empty_content_raises_validation_error() -> None:
    """Empty content raises appropriate validation error."""
    from vexy_markliff.exceptions import ValidationError

    converter = VexyMarkliff()

    with pytest.raises(ValidationError):
        converter.markdown_to_xliff("", "en", "es")

    with pytest.raises(ValidationError):
        converter.html_to_xliff("", "en", "es")


def test_invalid_language_codes_raise_validation_error() -> None:
    """Invalid language codes raise appropriate validation error."""
    from vexy_markliff.exceptions import ValidationError

    converter = VexyMarkliff()
    content = "# Test"

    with pytest.raises(ValidationError):
        converter.markdown_to_xliff(content, "invalid", "es")

    with pytest.raises(ValidationError):
        converter.markdown_to_xliff(content, "en", "invalid")
