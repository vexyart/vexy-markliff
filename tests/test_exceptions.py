"""Tests for custom exceptions."""
# this_file: tests/test_exceptions.py

import pytest

from vexy_markliff.exceptions import (
    ConfigurationError,
    ConversionError,
    FileOperationError,
    ParsingError,
    ValidationError,
    VexyMarkliffError,
)


class TestExceptions:
    """Test custom exception classes."""

    def test_base_exception(self) -> None:
        """Test base VexyMarkliffError."""
        exc = VexyMarkliffError("Base error")
        assert str(exc) == "Base error"
        assert isinstance(exc, Exception)

    def test_validation_error(self) -> None:
        """Test ValidationError."""
        exc = ValidationError("Invalid value")
        assert str(exc) == "Invalid value"
        assert isinstance(exc, VexyMarkliffError)

    def test_conversion_error(self) -> None:
        """Test ConversionError."""
        exc = ConversionError("Conversion failed")
        assert str(exc) == "Conversion failed"
        assert isinstance(exc, VexyMarkliffError)

    def test_parsing_error(self) -> None:
        """Test ParsingError."""
        exc = ParsingError("Parse failed")
        assert str(exc) == "Parse failed"
        assert isinstance(exc, VexyMarkliffError)

    def test_file_operation_error(self) -> None:
        """Test FileOperationError."""
        exc = FileOperationError("File not found")
        assert str(exc) == "File not found"
        assert isinstance(exc, VexyMarkliffError)

    def test_configuration_error(self) -> None:
        """Test ConfigurationError."""
        exc = ConfigurationError("Invalid config")
        assert str(exc) == "Invalid config"
        assert isinstance(exc, VexyMarkliffError)

    def test_exception_hierarchy(self) -> None:
        """Test that all custom exceptions inherit from VexyMarkliffError."""
        exceptions = [
            ValidationError("test"),
            ConversionError("test"),
            ParsingError("test"),
            FileOperationError("test"),
            ConfigurationError("test"),
        ]

        for exc in exceptions:
            assert isinstance(exc, VexyMarkliffError)
            assert isinstance(exc, Exception)
