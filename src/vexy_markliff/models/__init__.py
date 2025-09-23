"""Data models for vexy-markliff.

This module contains Pydantic data models for XLIFF documents and translation units.
"""
# this_file: src/vexy_markliff/models/__init__.py

from typing import TYPE_CHECKING

# Use lazy imports to avoid importing heavy Pydantic models during package init
if TYPE_CHECKING:
    from vexy_markliff.models.xliff import TranslationUnit, XLIFFDocument, XLIFFFile


def __getattr__(name: str):
    """Lazy import attributes to avoid performance bottlenecks."""
    if name == "TranslationUnit":
        from vexy_markliff.models.xliff import TranslationUnit

        return TranslationUnit
    if name == "XLIFFDocument":
        from vexy_markliff.models.xliff import XLIFFDocument

        return XLIFFDocument
    if name == "XLIFFFile":
        from vexy_markliff.models.xliff import XLIFFFile

        return XLIFFFile
    msg = f"module '{__name__}' has no attribute '{name}'"
    raise AttributeError(msg)


__all__ = [
    "TranslationUnit",
    "XLIFFDocument",
    "XLIFFFile",
]
