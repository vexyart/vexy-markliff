"""Simple exceptions for vexy-markliff."""
# this_file: src/vexy_markliff/exceptions.py


class VexyMarkliffError(Exception):
    """Base exception for all vexy-markliff errors."""

    pass


class ValidationError(VexyMarkliffError):
    """Raised when validation fails."""

    pass


class ConversionError(VexyMarkliffError):
    """Raised when conversion fails."""

    pass


class ParsingError(VexyMarkliffError):
    """Raised when parsing fails."""

    pass


class FileOperationError(VexyMarkliffError):
    """Raised when file operations fail."""

    pass


class ConfigurationError(VexyMarkliffError):
    """Raised when configuration is invalid."""

    pass
