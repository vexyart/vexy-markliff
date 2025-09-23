"""Tests for core CLI functionality."""
# this_file: tests/test_cli_enhanced.py

from pathlib import Path

import pytest

from vexy_markliff.cli import VexyMarkliffCLI


class TestCLICommands:
    """Tests for the 4 core CLI commands."""

    def test_md2xliff_success(self, tmp_path: Path) -> None:
        """Test successful Markdown to XLIFF conversion."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test Markdown\n\nThis is a test.", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file), "en", "es")

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert '<xliff version="2.1"' in content
        assert "en" in content
        assert "es" in content

    def test_html2xliff_success(self, tmp_path: Path) -> None:
        """Test successful HTML to XLIFF conversion."""
        input_file = tmp_path / "test.html"
        input_file.write_text("<h1>Test HTML</h1><p>This is a test.</p>", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.html2xliff(str(input_file), str(output_file), "en", "es")

        assert output_file.exists()
        content = output_file.read_text(encoding="utf-8")
        assert '<xliff version="2.1"' in content

    def test_xliff2md_success(self, tmp_path: Path) -> None:
        """Test successful XLIFF to Markdown conversion."""
        input_file = tmp_path / "test.xlf"
        input_file.write_text(
            '<?xml version="1.0"?><xliff version="2.1"><file id="1"><unit id="1"><segment><source>Test</source></segment></unit></file></xliff>',
            encoding="utf-8",
        )

        output_file = tmp_path / "output.md"

        cli = VexyMarkliffCLI()
        cli.xliff2md(str(input_file), str(output_file))

        assert output_file.exists()

    def test_xliff2html_success(self, tmp_path: Path) -> None:
        """Test successful XLIFF to HTML conversion."""
        input_file = tmp_path / "test.xlf"
        input_file.write_text(
            '<?xml version="1.0"?><xliff version="2.1"><file id="1"><unit id="1"><segment><source>Test</source></segment></unit></file></xliff>',
            encoding="utf-8",
        )

        output_file = tmp_path / "output.html"

        cli = VexyMarkliffCLI()
        cli.xliff2html(str(input_file), str(output_file))

        assert output_file.exists()

    def test_input_file_not_found(self) -> None:
        """Test error when input file doesn't exist."""
        cli = VexyMarkliffCLI()

        # Should exit with error code 1
        with pytest.raises(SystemExit) as exc_info:
            cli.md2xliff("nonexistent.md", "output.xlf")
        assert exc_info.value.code == 1

    def test_directory_creation(self, tmp_path: Path) -> None:
        """Test automatic directory creation for output files."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test", encoding="utf-8")

        output_file = tmp_path / "nested" / "dir" / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        assert output_file.exists()
        assert output_file.parent.exists()

    def test_unicode_handling(self, tmp_path: Path) -> None:
        """Test proper UTF-8 encoding handling."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test 中文 العربية\n\nUnicode: 🌟", encoding="utf-8")

        output_file = tmp_path / "output.xlf"

        cli = VexyMarkliffCLI()
        cli.md2xliff(str(input_file), str(output_file))

        content = output_file.read_text(encoding="utf-8")
        # Verify Unicode content is preserved
        assert "中文" in content
        assert "العربية" in content or "\\u" in content  # May be encoded
        assert "🌟" in content or "\\U" in content  # May be encoded

    def test_main_entry_point(self) -> None:
        """Test main entry point function exists."""
        from vexy_markliff.cli import main

        assert callable(main)
