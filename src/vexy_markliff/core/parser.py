"""HTML and Markdown parsing utilities - simplified for core functionality."""
# this_file: src/vexy_markliff/core/parser.py

from typing import Any, Dict, List

import markdown_it
from lxml import etree, html

from vexy_markliff.exceptions import ParsingError, ValidationError
from vexy_markliff.utils import get_logger, normalize_whitespace

logger = get_logger(__name__)


class MarkdownParser:
    """Simple parser for Markdown content using markdown-it-py."""

    def __init__(self) -> None:
        """Initialize the Markdown parser."""
        # Initialize with CommonMark preset
        self.md = markdown_it.MarkdownIt("commonmark", {"breaks": True, "html": True})
        # Enable tables and strikethrough
        self.md.enable(["table", "strikethrough"])

    def parse(self, content: str) -> dict[str, Any]:
        """Parse Markdown content into structured format.

        Args:
            content: Markdown content to parse

        Returns:
            Structured representation of the content

        Raises:
            ParsingError: If parsing fails
        """
        if not content or not content.strip():
            msg = "Content cannot be empty"
            raise ValidationError(msg)

        try:
            # Parse to HTML first
            html_content = self.md.render(content)

            # Then parse HTML for structure
            html_parser = HTMLParser()
            return html_parser.parse(html_content)

        except Exception as e:
            logger.error(f"Markdown parsing failed: {e}")
            msg = f"Failed to parse Markdown content: {e}"
            raise ParsingError(msg)

    def reconstruct(self, structured_content: dict[str, Any]) -> str:
        """Reconstruct Markdown from structured content.

        Args:
            structured_content: Structured content to reconstruct

        Returns:
            Reconstructed Markdown content

        Raises:
            ParsingError: If reconstruction fails
        """
        try:
            # Convert structured content back to HTML first
            html_parser = HTMLParser()
            return html_parser.reconstruct(structured_content)

            # For now, return HTML as Markdown conversion is complex
            # This could be enhanced with html2text or similar

        except Exception as e:
            logger.error(f"Markdown reconstruction failed: {e}")
            msg = f"Failed to reconstruct Markdown: {e}"
            raise ParsingError(msg)


class HTMLParser:
    """Simple parser for HTML content using lxml."""

    def __init__(self) -> None:
        """Initialize the HTML parser."""
        pass

    def parse(self, content: str) -> dict[str, Any]:
        """Parse HTML content into structured format.

        Args:
            content: HTML content to parse

        Returns:
            Structured representation of the content

        Raises:
            ParsingError: If parsing fails
        """
        if not content or not content.strip():
            msg = "Content cannot be empty"
            raise ValidationError(msg)

        try:
            # Parse HTML content
            doc = html.fromstring(content)

            # Extract translatable segments
            segments = self._extract_segments(doc)

            return {"segments": segments, "structure": self._extract_structure(doc)}

        except Exception as e:
            logger.error(f"HTML parsing failed: {e}")
            msg = f"Failed to parse HTML content: {e}"
            raise ParsingError(msg)

    def reconstruct(self, structured_content: dict[str, Any]) -> str:
        """Reconstruct HTML from structured content.

        Args:
            structured_content: Structured content to reconstruct

        Returns:
            Reconstructed HTML content

        Raises:
            ParsingError: If reconstruction fails
        """
        try:
            # Reconstruct HTML from segments and structure
            segments = structured_content.get("segments", [])
            structured_content.get("structure", {})

            # Simple reconstruction - can be enhanced
            html_parts = []
            for segment in segments:
                if segment.get("translatable", True):
                    html_parts.append(f"<p>{segment['content']}</p>")
                else:
                    html_parts.append(segment["content"])

            return "\n".join(html_parts)

        except Exception as e:
            logger.error(f"HTML reconstruction failed: {e}")
            msg = f"Failed to reconstruct HTML: {e}"
            raise ParsingError(msg)

    def _extract_segments(self, element) -> list[dict[str, Any]]:
        """Extract translatable segments from HTML element.

        Args:
            element: HTML element to process

        Returns:
            List of translatable segments
        """
        segments = []

        # Process text content
        if element.text and element.text.strip():
            text = normalize_whitespace(element.text)
            if text:
                segments.append(
                    {
                        "content": text,
                        "translatable": True,
                        "element": element.tag if hasattr(element, "tag") else "text",
                    }
                )

        # Process child elements
        for child in element:
            segments.extend(self._extract_segments(child))

            # Process tail text
            if child.tail and child.tail.strip():
                text = normalize_whitespace(child.tail)
                if text:
                    segments.append({"content": text, "translatable": True, "element": "text"})

        return segments

    def _extract_structure(self, element) -> dict[str, Any]:
        """Extract document structure for skeleton preservation.

        Args:
            element: HTML element to process

        Returns:
            Structure information
        """
        return {
            "tag": element.tag if hasattr(element, "tag") else "document",
            "attributes": dict(element.attrib) if hasattr(element, "attrib") else {},
            "children_count": len(element) if hasattr(element, "__len__") else 0,
        }
