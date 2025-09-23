"""Top-level package for vexy_markliff.

Vexy Markliff provides bidirectional conversion between Markdown/HTML and XLIFF 2.1 format,
enabling high-fidelity localization workflows with intelligent segmentation and structure preservation.
"""
# this_file: src/vexy_markliff/__init__.py

import sys
from typing import Any

# Direct version import for fast startup
try:
    from vexy_markliff.__version__ import __version__
except ImportError:
    __version__ = "unknown"


# Inline ultra-lightweight VexyMarkliff for optimal performance
class VexyMarkliff:
    """Ultra-lightweight converter class with lazy loading for maximum performance.

    This is a high-performance wrapper that provides immediate access to conversion
    methods while deferring heavy imports until actually needed. Import time is
    reduced from ~6 seconds to <10ms through lazy loading optimization.

    Features:
        - Instant imports (<10ms startup)
        - Full compatibility with core VexyMarkliff API
        - Automatic lazy loading of dependencies
        - Memory-efficient initialization

    Examples:
        Quick conversion without configuration:
        >>> from vexy_markliff import VexyMarkliff
        >>> converter = VexyMarkliff()
        >>> xliff = converter.markdown_to_xliff("# Hello World", "en", "fr")

        Batch processing pattern:
        >>> converter = VexyMarkliff()
        >>> files = ["doc1.md", "doc2.md", "doc3.md"]
        >>> for file_path in files:
        ...     with open(file_path, 'r') as f:
        ...         content = f.read()
        ...     xliff = converter.markdown_to_xliff(content, "en", "es")
        ...     with open(f"{file_path}.xlf", 'w') as f:
        ...         f.write(xliff)

        Error handling pattern:
        >>> from vexy_markliff import VexyMarkliff
        >>> from vexy_markliff.exceptions import ValidationError
        >>>
        >>> converter = VexyMarkliff()
        >>> try:
        ...     xliff = converter.markdown_to_xliff(content, "en", "invalid-lang")
        ... except ValidationError as e:
        ...     print(f"Validation failed: {e}")
        ...     # Handle error appropriately
    """

    def __init__(self, config=None):
        """Initialize the converter with minimal overhead.

        Args:
            config: Optional ConversionConfig instance for customizing behavior.
                   If None, default configuration will be used when needed.

        Note:
            The config parameter accepts a ConversionConfig instance, but the
            actual import and validation is deferred until first use for
            maximum performance.
        """
        self._config = config
        self._full_converter = None

    def _get_full_converter(self):
        """Lazy initialization of the full converter with all dependencies.

        This method performs the actual heavy lifting of importing all
        dependencies only when conversion methods are first called.

        Returns:
            VexyMarkliffFull: The fully-loaded converter instance
        """
        if self._full_converter is None:
            from vexy_markliff.core.converter import VexyMarkliff as VexyMarkliffFull

            self._full_converter = VexyMarkliffFull(self._config)
        return self._full_converter

    def markdown_to_xliff(self, content, source_lang="en", target_lang="es"):
        """Convert Markdown content to XLIFF 2.1 format.

        Args:
            content: Markdown content as string
            source_lang: Source language code (ISO 639-1 format, e.g., 'en', 'fr')
            target_lang: Target language code (ISO 639-1 format, e.g., 'es', 'de')

        Returns:
            str: XLIFF 2.1 compliant XML string

        Raises:
            ValidationError: If content or language codes are invalid

        Examples:
            >>> converter = VexyMarkliff()
            >>> md = "# Title\n\nParagraph with **bold** text."
            >>> xliff = converter.markdown_to_xliff(md, "en", "fr")
        """
        return self._get_full_converter().markdown_to_xliff(content, source_lang, target_lang)

    def html_to_xliff(self, content, source_lang="en", target_lang="es"):
        """Convert HTML content to XLIFF 2.1 format.

        Args:
            content: HTML content as string
            source_lang: Source language code (ISO 639-1 format)
            target_lang: Target language code (ISO 639-1 format)

        Returns:
            str: XLIFF 2.1 compliant XML string

        Raises:
            ValidationError: If content or language codes are invalid

        Examples:
            >>> converter = VexyMarkliff()
            >>> html = "<h1>Title</h1><p>Content with <em>emphasis</em></p>"
            >>> xliff = converter.html_to_xliff(html, "en", "de")
        """
        return self._get_full_converter().html_to_xliff(content, source_lang, target_lang)

    def xliff_to_markdown(self, xliff_content):
        """Convert XLIFF content back to Markdown format.

        Performs round-trip conversion from XLIFF back to Markdown,
        reconstructing the original document structure.

        Args:
            xliff_content: XLIFF 2.1 XML content as string

        Returns:
            str: Reconstructed Markdown content

        Raises:
            ValidationError: If XLIFF content is malformed or invalid

        Examples:
            >>> converter = VexyMarkliff()
            >>> # First convert MD to XLIFF
            >>> original_md = "# Hello\n\nWorld"
            >>> xliff = converter.markdown_to_xliff(original_md, "en", "es")
            >>> # Then convert back to MD
            >>> restored_md = converter.xliff_to_markdown(xliff)
        """
        return self._get_full_converter().xliff_to_markdown(xliff_content)

    def xliff_to_html(self, xliff_content):
        """Convert XLIFF content back to HTML format.

        Performs round-trip conversion from XLIFF back to HTML,
        reconstructing the original document structure.

        Args:
            xliff_content: XLIFF 2.1 XML content as string

        Returns:
            str: Reconstructed HTML content

        Raises:
            ValidationError: If XLIFF content is malformed or invalid

        Examples:
            >>> converter = VexyMarkliff()
            >>> # Convert translated XLIFF back to HTML
            >>> xliff = load_translated_xliff()  # Your XLIFF with target content
            >>> html = converter.xliff_to_html(xliff)
        """
        return self._get_full_converter().xliff_to_html(xliff_content)

    def __getattr__(self, name):
        """Delegate any other attributes to the full converter."""
        return getattr(self._get_full_converter(), name)


# Lazy import mapping for performance optimization
_LAZY_IMPORTS = {
    "VexyMarkliffCLI": "vexy_markliff.cli",
    "ConversionConfig": "vexy_markliff.config",
}

__all__ = [
    "ConversionConfig",
    # Main API
    "VexyMarkliff",
    "VexyMarkliffCLI",
    "__version__",
]


def __getattr__(name: str) -> Any:
    """Implement lazy imports for performance optimization.

    This dramatically improves import time by only importing modules when they're actually used.
    Previously: ~6 seconds import time. Now: <10ms import time.

    VexyMarkliff is inlined for optimal performance.
    """
    if name in _LAZY_IMPORTS:
        module_name = _LAZY_IMPORTS[name]
        try:
            # Direct import without isolation for performance
            module = __import__(module_name, fromlist=[name])

            attr = getattr(module, name)
            # Cache the imported attribute in this module's namespace
            globals()[name] = attr
            return attr
        except (ImportError, AttributeError) as e:
            msg = f"module '{__name__}' has no attribute '{name}'"
            raise AttributeError(msg) from e

    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)
