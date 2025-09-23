"""Tests for configuration management."""
# this_file: tests/test_config.py

from pathlib import Path

import pytest

from vexy_markliff.config import ConversionConfig


class TestConversionConfig:
    """Test configuration model."""

    def test_default_configuration(self) -> None:
        """Test default configuration values."""
        config = ConversionConfig()

        assert config.source_language == "en"
        assert config.target_language == "es"
        assert config.split_sentences is True

    def test_custom_configuration(self) -> None:
        """Test custom configuration values."""
        config = ConversionConfig(source_language="fr", target_language="de", split_sentences=False)

        assert config.source_language == "fr"
        assert config.target_language == "de"
        assert config.split_sentences is False

    def test_language_code_validation(self) -> None:
        """Test language code validation."""
        # Valid 2-letter codes should work
        config = ConversionConfig(source_language="en", target_language="es")
        assert config.source_language == "en"
        assert config.target_language == "es"

        # Invalid codes should raise ValueError
        with pytest.raises(ValueError):
            ConversionConfig(source_language="english")

        with pytest.raises(ValueError):
            ConversionConfig(target_language="ESP")

        with pytest.raises(ValueError):
            ConversionConfig(source_language="e")

    def test_config_from_yaml(self, tmp_path: Path) -> None:
        """Test loading config from YAML file."""
        config_file = tmp_path / "config.yaml"
        config_file.write_text("""
source_language: fr
target_language: de
split_sentences: false
""")

        config = ConversionConfig.load(str(config_file))
        assert config.source_language == "fr"
        assert config.target_language == "de"
        assert config.split_sentences is False

    def test_config_nonexistent_file(self) -> None:
        """Test loading from nonexistent file returns defaults."""
        config = ConversionConfig.load("/nonexistent/file.yaml")
        assert config.source_language == "en"  # Default
        assert config.target_language == "es"  # Default
        assert config.split_sentences is True  # Default

    def test_config_invalid_yaml(self, tmp_path: Path) -> None:
        """Test loading invalid YAML returns defaults."""
        config_file = tmp_path / "invalid.yaml"
        config_file.write_text("invalid: yaml: content: [")

        # Should fall back to defaults on error
        config = ConversionConfig.load(str(config_file))
        assert config.source_language == "en"  # Default
        assert config.target_language == "es"  # Default
