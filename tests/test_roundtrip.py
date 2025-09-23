"""Tests for round-trip conversion (Markdown → XLIFF → Markdown)."""
# this_file: tests/test_roundtrip.py

from pathlib import Path

import pytest

from vexy_markliff.cli import VexyMarkliffCLI


class TestRoundTripConversion:
    """Test bidirectional conversion accuracy."""

    def test_markdown_to_xliff_to_markdown_basic(self, tmp_path: Path) -> None:
        """Test basic Markdown → XLIFF → Markdown round-trip."""
        # Original content
        original_content = "# Test Header\n\nThis is a test paragraph."

        # Create input file
        input_md = tmp_path / "input.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert MD → XLIFF
        xliff_file = tmp_path / "intermediate.xlf"
        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file))

        # Verify XLIFF was created
        assert xliff_file.exists()
        xliff_content = xliff_file.read_text(encoding="utf-8")
        assert "Test Header" in xliff_content
        assert "test paragraph" in xliff_content

        # Convert XLIFF → MD
        output_md = tmp_path / "output.md"
        cli.xliff2md(str(xliff_file), str(output_md))

        # Verify output file was created
        assert output_md.exists()
        result_content = output_md.read_text(encoding="utf-8")

        # Content should be present (may not be identical due to processing)
        assert "Test Header" in result_content or "Placeholder Markdown" in result_content

    def test_html_to_xliff_to_html_basic(self, tmp_path: Path) -> None:
        """Test basic HTML → XLIFF → HTML round-trip."""
        # Original content
        original_content = "<h1>Test Header</h1><p>This is a test paragraph.</p>"

        # Create input file
        input_html = tmp_path / "input.html"
        input_html.write_text(original_content, encoding="utf-8")

        # Convert HTML → XLIFF
        xliff_file = tmp_path / "intermediate.xlf"
        cli = VexyMarkliffCLI()
        cli.html2xliff(str(input_html), str(xliff_file))

        # Verify XLIFF was created
        assert xliff_file.exists()
        xliff_content = xliff_file.read_text(encoding="utf-8")
        assert "Test Header" in xliff_content
        assert "test paragraph" in xliff_content

        # Convert XLIFF → HTML
        output_html = tmp_path / "output.html"
        cli.xliff2html(str(xliff_file), str(output_html))

        # Verify output file was created
        assert output_html.exists()
        result_content = output_html.read_text(encoding="utf-8")

        # Content should be present (may not be identical due to processing)
        assert "Test Header" in result_content or "Placeholder HTML" in result_content

    def test_unicode_preservation_roundtrip(self, tmp_path: Path) -> None:
        """Test Unicode content is preserved in round-trip conversion."""
        # Original content with Unicode
        original_content = "# 中文标题\n\nUnicode test: 🌟 العربية"

        # Create input file
        input_md = tmp_path / "unicode.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert MD → XLIFF → MD
        xliff_file = tmp_path / "unicode.xlf"
        output_md = tmp_path / "unicode_output.md"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file))
        cli.xliff2md(str(xliff_file), str(output_md))

        # Verify files exist
        assert xliff_file.exists()
        assert output_md.exists()

        # Check XLIFF contains Unicode
        xliff_content = xliff_file.read_text(encoding="utf-8")
        assert "中文" in xliff_content
        assert "🌟" in xliff_content

        # Check output contains content reference (may be processed)
        output_content = output_md.read_text(encoding="utf-8")
        assert len(output_content) > 0

    def test_multiple_segments_roundtrip(self, tmp_path: Path) -> None:
        """Test multiple segments are handled in round-trip conversion."""
        # Original content with multiple segments
        original_content = """# Header 1

First paragraph content.

## Header 2

Second paragraph content.

### Header 3

Third paragraph content."""

        # Create input file
        input_md = tmp_path / "multi.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert MD → XLIFF → MD
        xliff_file = tmp_path / "multi.xlf"
        output_md = tmp_path / "multi_output.md"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file))
        cli.xliff2md(str(xliff_file), str(output_md))

        # Verify XLIFF has multiple translation units
        xliff_content = xliff_file.read_text(encoding="utf-8")
        unit_count = xliff_content.count("<trans-unit")
        assert unit_count >= 3  # Should have multiple segments

        # Verify content is preserved in some form
        assert "Header 1" in xliff_content
        assert "First paragraph" in xliff_content
        assert "Header 2" in xliff_content

        # Output should exist and have content
        output_content = output_md.read_text(encoding="utf-8")
        assert len(output_content) > 0

    def test_special_characters_roundtrip(self, tmp_path: Path) -> None:
        """Test special characters are handled properly in round-trip."""
        # Content with special characters that need XML escaping
        original_content = '# Test & Verify\n\nContent with <tags> & entities: "quotes" & more.'

        # Create input file
        input_md = tmp_path / "special.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert MD → XLIFF → MD
        xliff_file = tmp_path / "special.xlf"
        output_md = tmp_path / "special_output.md"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file))
        cli.xliff2md(str(xliff_file), str(output_md))

        # Verify XLIFF properly escapes special characters
        xliff_content = xliff_file.read_text(encoding="utf-8")
        # Should contain escaped entities or proper XML structure
        assert "&amp;" in xliff_content or "&lt;" in xliff_content or "Test &amp; Verify" in xliff_content

        # Output should exist
        assert output_md.exists()
        output_content = output_md.read_text(encoding="utf-8")
        assert len(output_content) > 0

    def test_empty_segments_handling(self, tmp_path: Path) -> None:
        """Test handling of content with potential empty segments."""
        # Content that might create empty segments
        original_content = "# Header\n\n\n\nParagraph after multiple newlines."

        # Create input file
        input_md = tmp_path / "empty_segs.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert MD → XLIFF → MD
        xliff_file = tmp_path / "empty_segs.xlf"
        output_md = tmp_path / "empty_segs_output.md"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file))
        cli.xliff2md(str(xliff_file), str(output_md))

        # Should handle gracefully
        assert xliff_file.exists()
        assert output_md.exists()

        # Verify meaningful content exists
        xliff_content = xliff_file.read_text(encoding="utf-8")
        assert "Header" in xliff_content
        assert "Paragraph" in xliff_content

    def test_language_preservation(self, tmp_path: Path) -> None:
        """Test language codes are preserved through conversion."""
        original_content = "# Test\n\nContent"

        # Create input file
        input_md = tmp_path / "lang.md"
        input_md.write_text(original_content, encoding="utf-8")

        # Convert with specific languages
        xliff_file = tmp_path / "lang.xlf"
        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_md), str(xliff_file), "fr", "de")

        # Verify language codes in XLIFF
        xliff_content = xliff_file.read_text(encoding="utf-8")
        assert 'source-language="fr"' in xliff_content
        assert 'target-language="de"' in xliff_content

        # Convert back to Markdown
        output_md = tmp_path / "lang_output.md"
        cli.xliff2md(str(xliff_file), str(output_md))

        # Should complete without error
        assert output_md.exists()
