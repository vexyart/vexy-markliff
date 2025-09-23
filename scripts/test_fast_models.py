#!/usr/bin/env python3
"""Test the ultra-fast dataclass models performance."""
# this_file: scripts/test_fast_models.py

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def test_fast_models():
    """Test fast dataclass models import and usage."""

    start_time = time.perf_counter()

    # Import fast models
    from vexy_markliff.models._xliff_fast import XLIFFDocument

    import_time = time.perf_counter()

    # Use the models
    doc = XLIFFDocument()
    doc.add_file("test", "en", "es")
    doc.add_unit("test", "unit1", "Hello world")
    result = doc.to_xml()

    end_time = time.perf_counter()

    import_time - start_time
    end_time - import_time
    total_duration = end_time - start_time

    # Verify output
    if "<?xml" in result and "xliff" in result and "Hello world" in result:
        return total_duration
    return None


def test_converter_with_fast_models():
    """Test converter using fast models."""

    start_time = time.perf_counter()

    # Import and use converter (should use fast models via helper)
    from vexy_markliff.core.converter import VexyMarkliff

    converter = VexyMarkliff()
    result = converter.markdown_to_xliff("# Test", "en", "es")

    end_time = time.perf_counter()
    duration = end_time - start_time

    # Verify output
    if "<?xml" in result and "xliff" in result:
        return duration
    return None


def main():
    """Run all fast model tests."""

    # Test 1: Direct fast models
    fast_time = test_fast_models()

    # Test 2: Converter with fast models
    converter_time = test_converter_with_fast_models()

    # Analysis

    if fast_time is not None:
        if fast_time < 0.05 or fast_time < 0.1:
            pass
        else:
            pass

    if converter_time is not None:
        if converter_time < 0.1:
            pass
        else:
            pass

    # Show improvement
    baseline = 1.9  # Previous performance
    if converter_time is not None:
        ((baseline - converter_time) / baseline) * 100


if __name__ == "__main__":
    main()
