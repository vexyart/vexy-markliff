#!/usr/bin/env python3
"""Simple CLI for vexy-markliff - focused on core conversion commands only."""
# this_file: src/vexy_markliff/cli.py

import sys
from pathlib import Path

import fire

from vexy_markliff.core.converter import VexyMarkliff


class VexyMarkliffCLI:
    """Simple CLI for Vexy Markliff conversion tools.

    Provides bidirectional conversion between Markdown/HTML and XLIFF 2.1 format.
    """

    def __init__(self):
        """Initialize CLI with converter."""
        self.converter = VexyMarkliff()

    def md2xliff(self, input_file: str, output_file: str, source_lang: str = "en", target_lang: str = "es") -> None:
        """Convert Markdown file to XLIFF format.

        Args:
            input_file: Path to input Markdown file
            output_file: Path to output XLIFF file
            source_lang: Source language code (default: en)
            target_lang: Target language code (default: es)
        """
        self._convert_file(input_file, output_file, "markdown", source_lang, target_lang)

    def html2xliff(self, input_file: str, output_file: str, source_lang: str = "en", target_lang: str = "es") -> None:
        """Convert HTML file to XLIFF format.

        Args:
            input_file: Path to input HTML file
            output_file: Path to output XLIFF file
            source_lang: Source language code (default: en)
            target_lang: Target language code (default: es)
        """
        self._convert_file(input_file, output_file, "html", source_lang, target_lang)

    def xliff2md(self, input_file: str, output_file: str) -> None:
        """Convert XLIFF file back to Markdown format.

        Args:
            input_file: Path to input XLIFF file
            output_file: Path to output Markdown file
        """
        self._convert_file(input_file, output_file, "xliff_to_markdown")

    def xliff2html(self, input_file: str, output_file: str) -> None:
        """Convert XLIFF file back to HTML format.

        Args:
            input_file: Path to input XLIFF file
            output_file: Path to output HTML file
        """
        self._convert_file(input_file, output_file, "xliff_to_html")

    def _convert_file(
        self,
        input_file: str,
        output_file: str,
        conversion_type: str,
        source_lang: str | None = None,
        target_lang: str | None = None,
    ) -> None:
        """Common conversion logic for all formats.

        Args:
            input_file: Path to input file
            output_file: Path to output file
            conversion_type: Type of conversion to perform
            source_lang: Source language code (for to-XLIFF conversions)
            target_lang: Target language code (for to-XLIFF conversions)
        """
        try:
            # Check input file exists
            input_path = Path(input_file)
            if not input_path.exists():
                sys.exit(1)

            # Read input file
            with open(input_file, encoding="utf-8") as f:
                content = f.read()

            # Perform conversion based on type
            if conversion_type == "markdown":
                output_content = self.converter.markdown_to_xliff(content, source_lang, target_lang)
            elif conversion_type == "html":
                output_content = self.converter.html_to_xliff(content, source_lang, target_lang)
            elif conversion_type == "xliff_to_markdown":
                output_content = self.converter.xliff_to_markdown(content)
            elif conversion_type == "xliff_to_html":
                output_content = self.converter.xliff_to_html(content)
            else:
                msg = f"Unknown conversion type: {conversion_type}"
                raise ValueError(msg)

            # Ensure output directory exists
            output_path = Path(output_file)
            output_path.parent.mkdir(parents=True, exist_ok=True)

            # Write output file
            with open(output_file, "w", encoding="utf-8") as f:
                f.write(output_content)

        except Exception:
            sys.exit(1)


def main():
    """Main CLI entry point."""
    fire.Fire(VexyMarkliffCLI)


if __name__ == "__main__":
    main()
