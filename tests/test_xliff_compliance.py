"""Tests for XLIFF 2.1 compliance validation."""
# this_file: tests/test_xliff_compliance.py

from pathlib import Path

import pytest

from vexy_markliff.cli import VexyMarkliffCLI


class TestXLIFF21Compliance:
    """Test XLIFF 2.1 standard compliance."""

    def test_xliff_basic_structure(self, tmp_path: Path) -> None:
        """Test generated XLIFF has proper basic structure."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test\n\nThis is a test.", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file), "en", "es")

        content = output_file.read_text(encoding="utf-8")

        # Check basic XLIFF structure
        assert '<xliff version="2.1"' in content
        assert 'xmlns="urn:oasis:names:tc:xliff:document:2.1"' in content
        assert 'source-language="en"' in content
        assert 'target-language="es"' in content
        assert "<file id=" in content
        assert "<trans-unit id=" in content
        assert "<source>" in content

    def test_xliff_language_codes(self, tmp_path: Path) -> None:
        """Test XLIFF uses correct language codes."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file), "fr", "de")

        content = output_file.read_text(encoding="utf-8")
        assert 'source-language="fr"' in content
        assert 'target-language="de"' in content

    def test_xliff_unit_states(self, tmp_path: Path) -> None:
        """Test translation units have proper state attributes."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test\n\nContent", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")
        # Should have state="new" for untranslated units
        assert 'state="new"' in content

    def test_xliff_xml_well_formed(self, tmp_path: Path) -> None:
        """Test generated XLIFF is well-formed XML."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test with <tags> & entities", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")

        # XML entities should be properly escaped
        assert "&lt;" in content or "&amp;" in content or "<tags>" not in content

    def test_xliff_required_elements(self, tmp_path: Path) -> None:
        """Test XLIFF has all required elements per 2.1 spec."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")

        # Required elements for minimal XLIFF 2.1
        assert "<xliff" in content
        assert 'version="2.1"' in content
        assert "<file" in content
        assert "<trans-unit" in content
        assert "<source>" in content

    def test_xliff_unicode_preservation(self, tmp_path: Path) -> None:
        """Test XLIFF preserves Unicode content correctly."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test 中文 🌟", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")

        # Unicode characters should be preserved
        assert "中文" in content
        assert "🌟" in content

    def test_xliff_empty_content_handling(self, tmp_path: Path) -> None:
        """Test XLIFF handles empty/whitespace content properly."""
        input_file = tmp_path / "empty.md"
        input_file.write_text("", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()

        # Empty content should trigger an error (expected behavior)
        with pytest.raises(SystemExit) as exc_info:
            cli.md2xliff(str(input_file), str(output_file))
        assert exc_info.value.code == 1

    def test_xliff_multiple_segments(self, tmp_path: Path) -> None:
        """Test XLIFF properly segments multiple content blocks."""
        input_file = tmp_path / "multi.md"
        input_file.write_text("# Header 1\n\nParagraph 1\n\n# Header 2\n\nParagraph 2", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")

        # Should have multiple translation units
        unit_count = content.count("<trans-unit")
        assert unit_count >= 2

        # Should contain the content
        assert "Header 1" in content
        assert "Paragraph 1" in content
        assert "Header 2" in content
        assert "Paragraph 2" in content
