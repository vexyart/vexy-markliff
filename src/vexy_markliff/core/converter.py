"""Main conversion orchestrator - simplified for core functionality only."""
# this_file: src/vexy_markliff/core/converter.py

from typing import TYPE_CHECKING

from vexy_markliff.exceptions import ConversionError, ValidationError
from vexy_markliff.utils import get_logger, validate_language_code

if TYPE_CHECKING:
    from vexy_markliff.config import ConversionConfig

logger = get_logger(__name__)


class VexyMarkliff:
    """Core converter for bidirectional Markdown/HTML ↔ XLIFF conversion.

    Provides simple, reliable conversion between Markdown/HTML and XLIFF 2.1 format
    with round-trip fidelity and XLIFF compliance.
    """

    def __init__(self, config=None):
        """Initialize converter with optional configuration.

        Args:
            config: ConversionConfig instance or None for defaults
        """
        self.config = config

    def markdown_to_xliff(self, content: str, source_lang: str = "en", target_lang: str = "es") -> str:
        """Convert Markdown content to XLIFF 2.1 format.

        Args:
            content: Markdown content as string
            source_lang: Source language code (ISO 639-1)
            target_lang: Target language code (ISO 639-1)

        Returns:
            XLIFF 2.1 compliant XML string

        Raises:
            ValidationError: If content or language codes are invalid
            ConversionError: If conversion fails
        """
        if not content or not content.strip():
            msg = "Content cannot be empty"
            raise ValidationError(msg)

        if not validate_language_code(source_lang):
            msg = f"Invalid source language code: {source_lang}"
            raise ValidationError(msg)

        if not validate_language_code(target_lang):
            msg = f"Invalid target language code: {target_lang}"
            raise ValidationError(msg)

        try:
            # Import dependencies only when needed
            from vexy_markliff.core.parser import MarkdownParser
            from vexy_markliff.models.xliff import XLIFFDocument

            # Parse Markdown to structured content
            parser = MarkdownParser()
            parsed_content = parser.parse(content)

            # Create XLIFF document
            xliff_doc = XLIFFDocument(source_lang=source_lang, target_lang=target_lang, content=parsed_content)

            return xliff_doc.to_xml()

        except Exception as e:
            logger.error(f"Markdown to XLIFF conversion failed: {e}")
            msg = f"Failed to convert Markdown to XLIFF: {e}"
            raise ConversionError(msg)

    def html_to_xliff(self, content: str, source_lang: str = "en", target_lang: str = "es") -> str:
        """Convert HTML content to XLIFF 2.1 format.

        Args:
            content: HTML content as string
            source_lang: Source language code (ISO 639-1)
            target_lang: Target language code (ISO 639-1)

        Returns:
            XLIFF 2.1 compliant XML string

        Raises:
            ValidationError: If content or language codes are invalid
            ConversionError: If conversion fails
        """
        if not content or not content.strip():
            msg = "Content cannot be empty"
            raise ValidationError(msg)

        if not validate_language_code(source_lang):
            msg = f"Invalid source language code: {source_lang}"
            raise ValidationError(msg)

        if not validate_language_code(target_lang):
            msg = f"Invalid target language code: {target_lang}"
            raise ValidationError(msg)

        try:
            # Import dependencies only when needed
            from vexy_markliff.core.parser import HTMLParser
            from vexy_markliff.models.xliff import XLIFFDocument

            # Parse HTML to structured content
            parser = HTMLParser()
            parsed_content = parser.parse(content)

            # Create XLIFF document
            xliff_doc = XLIFFDocument(source_lang=source_lang, target_lang=target_lang, content=parsed_content)

            return xliff_doc.to_xml()

        except Exception as e:
            logger.error(f"HTML to XLIFF conversion failed: {e}")
            msg = f"Failed to convert HTML to XLIFF: {e}"
            raise ConversionError(msg)

    def xliff_to_markdown(self, xliff_content: str) -> str:
        """Convert XLIFF content back to Markdown format.

        Args:
            xliff_content: XLIFF 2.1 XML content as string

        Returns:
            Reconstructed Markdown content

        Raises:
            ValidationError: If XLIFF content is malformed
            ConversionError: If conversion fails
        """
        if not xliff_content or not xliff_content.strip():
            msg = "XLIFF content cannot be empty"
            raise ValidationError(msg)

        try:
            # Import dependencies only when needed
            from vexy_markliff.core.parser import MarkdownParser
            from vexy_markliff.models.xliff import XLIFFDocument

            # Parse XLIFF document
            xliff_doc = XLIFFDocument.from_xml(xliff_content)

            # Convert back to Markdown
            parser = MarkdownParser()
            return parser.reconstruct(xliff_doc.content)

        except Exception as e:
            logger.error(f"XLIFF to Markdown conversion failed: {e}")
            msg = f"Failed to convert XLIFF to Markdown: {e}"
            raise ConversionError(msg)

    def xliff_to_html(self, xliff_content: str) -> str:
        """Convert XLIFF content back to HTML format.

        Args:
            xliff_content: XLIFF 2.1 XML content as string

        Returns:
            Reconstructed HTML content

        Raises:
            ValidationError: If XLIFF content is malformed
            ConversionError: If conversion fails
        """
        if not xliff_content or not xliff_content.strip():
            msg = "XLIFF content cannot be empty"
            raise ValidationError(msg)

        try:
            # Import dependencies only when needed
            from vexy_markliff.core.parser import HTMLParser
            from vexy_markliff.models.xliff import XLIFFDocument

            # Parse XLIFF document
            xliff_doc = XLIFFDocument.from_xml(xliff_content)

            # Convert back to HTML
            parser = HTMLParser()
            return parser.reconstruct(xliff_doc.content)

        except Exception as e:
            logger.error(f"XLIFF to HTML conversion failed: {e}")
            msg = f"Failed to convert XLIFF to HTML: {e}"
            raise ConversionError(msg)
