"""Simple configuration for vexy-markliff."""
# this_file: src/vexy_markliff/config.py

from pathlib import Path
from typing import Optional


class ConversionConfig:
    """Simple configuration for conversion operations.

    Simplified to avoid heavy Pydantic imports for better startup performance.
    """

    def __init__(self, source_language: str = "en", target_language: str = "es", split_sentences: bool = True):
        """Initialize configuration with validation.

        Args:
            source_language: Source language code (2-letter lowercase)
            target_language: Target language code (2-letter lowercase)
            split_sentences: Whether to split sentences for translation units
        """
        # Validate language codes
        for lang_code, field_name in [(source_language, "source_language"), (target_language, "target_language")]:
            if not (len(lang_code) == 2 and lang_code.isalpha() and lang_code.islower()):
                msg = f"Invalid {field_name}: {lang_code}. Must be 2-letter lowercase code."
                raise ValueError(msg)

        self.source_language = source_language
        self.target_language = target_language
        self.split_sentences = split_sentences

    @classmethod
    def load(cls, config_path: str | None = None) -> "ConversionConfig":
        """Load configuration from optional YAML file.

        Args:
            config_path: Optional path to YAML configuration file.
                        If None or file doesn't exist, uses defaults.

        Returns:
            ConversionConfig instance with loaded or default values
        """
        if config_path:
            config_file = Path(config_path)
            if config_file.exists():
                try:
                    import yaml

                    with open(config_file, encoding="utf-8") as f:
                        config_data = yaml.safe_load(f) or {}
                    return cls(**config_data)
                except Exception:
                    pass  # Fall back to defaults if any error

        return cls()  # Return default configuration
