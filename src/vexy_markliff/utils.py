"""Essential utility functions for vexy-markliff.

This module contains only the truly essential utility functions that are shared
between multiple core modules. Every function here must be simple, pure, and
directly support the core conversion functionality.
"""
# this_file: src/vexy_markliff/utils.py

import logging
import re
from pathlib import Path
from typing import List


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text.

    Args:
        text: Input text string

    Returns:
        Text with normalized whitespace
    """
    return re.sub(r"\s+", " ", text.strip())


def validate_language_code(code: str) -> bool:
    """Validate ISO 639-1 language code.

    Args:
        code: Language code to validate

    Returns:
        True if valid ISO 639-1 code
    """
    return len(code) == 2 and code.isalpha() and code.islower()


def validate_file_path(path: str) -> bool:
    """Validate file path exists and is readable.

    Args:
        path: File path to validate

    Returns:
        True if path exists and is readable
    """
    return Path(path).exists() and Path(path).is_file()


def split_sentences_simple(text: str) -> list[str]:
    """Simple sentence splitting for translation units.

    Args:
        text: Text to split into sentences

    Returns:
        List of sentences
    """
    # Simple sentence splitting - can be enhanced later if needed
    sentences = re.split(r"[.!?]+\s*", text.strip())
    # Remove empty strings and strip whitespace
    return [s.strip() for s in sentences if s.strip()]


def get_logger(name: str) -> logging.Logger:
    """Get a simple logger instance.

    Args:
        name: Logger name

    Returns:
        Logger instance
    """
    return logging.getLogger(name)


def setup_logging(level: str = "INFO") -> None:
    """Setup basic logging configuration.

    Args:
        level: Logging level
    """
    logging.basicConfig(
        level=getattr(logging, level.upper()), format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
