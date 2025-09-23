"""Tests for CLI error handling."""
# this_file: tests/test_cli_errors.py

from pathlib import Path

import pytest

from vexy_markliff.cli import VexyMarkliffCLI


class TestCLIErrorHandling:
    """Tests for CLI error conditions."""

    def test_nonexistent_input_file(self) -> None:
        """Test error when input file doesn't exist."""
        cli = VexyMarkliffCLI()

        with pytest.raises(SystemExit) as exc_info:
            cli.md2xliff("nonexistent.md", "output.xlf")
        assert exc_info.value.code == 1

    def test_conversion_exception_handling(self, tmp_path: Path, monkeypatch) -> None:
        """Test that conversion errors are handled gracefully."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test", encoding="utf-8")

        cli = VexyMarkliffCLI()

        # Mock the converter to raise an exception
        def mock_markdown_to_xliff(*args, **kwargs):
            msg = "Conversion error"
            raise Exception(msg)

        monkeypatch.setattr(cli.converter, "markdown_to_xliff", mock_markdown_to_xliff)

        with pytest.raises(SystemExit) as exc_info:
            cli.md2xliff(str(input_file), str(tmp_path / "output.xlf"))
        assert exc_info.value.code == 1

    def test_write_permission_error(self, tmp_path: Path) -> None:
        """Test handling of write permission errors."""
        input_file = tmp_path / "test.md"
        input_file.write_text("# Test", encoding="utf-8")

        # Create a read-only directory
        readonly_dir = tmp_path / "readonly"
        readonly_dir.mkdir()
        readonly_dir.chmod(0o444)

        cli = VexyMarkliffCLI()

        try:
            with pytest.raises(SystemExit) as exc_info:
                cli.md2xliff(str(input_file), str(readonly_dir / "output.xlf"))
            assert exc_info.value.code == 1
        finally:
            readonly_dir.chmod(0o755)  # Restore permissions for cleanup
