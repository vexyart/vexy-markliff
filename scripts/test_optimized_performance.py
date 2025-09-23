#!/usr/bin/env python3
"""Test performance of optimized models and converter access."""
# this_file: scripts/test_optimized_performance.py

import os
import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def time_operation(operation_name: str, operation_func):
    """Time an operation and report results."""
    start_time = time.perf_counter()
    try:
        result = operation_func()
        end_time = time.perf_counter()
        duration = end_time - start_time
        return result, duration, True
    except Exception:
        end_time = time.perf_counter()
        duration = end_time - start_time
        return None, duration, False


def main():
    """Test performance optimizations."""

    # Test 1: Isolated XLIFF models
    def test_isolated_models():
        from vexy_markliff.models._xliff_isolated import XLIFFDocument

        doc = XLIFFDocument()
        doc.add_file("test", "en", "es")
        doc.add_unit("test", "unit1", "Hello world")
        return doc.to_xml()

    isolated_result, isolated_time, isolated_success = time_operation(
        "Isolated XLIFF models import + usage", test_isolated_models
    )

    # Test 2: Original XLIFF models for comparison
    def test_original_models():
        from vexy_markliff.models.xliff import XLIFFDocument

        doc = XLIFFDocument()
        doc.add_file("test", "en", "es")
        doc.add_unit("test", "unit1", "Hello world")
        return doc.to_xml()

    original_result, original_time, original_success = time_operation(
        "Original XLIFF models import + usage", test_original_models
    )

    # Test 3: VexyMarkliff converter access (first time)
    def test_converter_first_access():
        from vexy_markliff.core.converter import VexyMarkliff

        converter = VexyMarkliff()
        return converter.markdown_to_xliff("# Test", "en", "es")

    converter_result, converter_time, converter_success = time_operation(
        "VexyMarkliff converter first access", test_converter_first_access
    )

    # Test 4: VexyMarkliff converter access (second time - should be cached)
    def test_converter_second_access():
        from vexy_markliff.core.converter import VexyMarkliff

        converter = VexyMarkliff()
        return converter.markdown_to_xliff("# Test 2", "en", "es")

    cached_result, cached_time, cached_success = time_operation(
        "VexyMarkliff converter second access (cached)", test_converter_second_access
    )

    # Test 5: Multiple converter instances (should all use cached classes)
    def test_multiple_converters():
        from vexy_markliff.core.converter import VexyMarkliff

        converters = []
        for i in range(5):
            converter = VexyMarkliff()
            result = converter.markdown_to_xliff(f"# Test {i}", "en", "es")
            converters.append((converter, result))
        return converters

    multiple_result, multiple_time, multiple_success = time_operation(
        "Multiple converter instances (5x)", test_multiple_converters
    )

    # Performance Analysis

    if isolated_success and original_success:
        ((original_time - isolated_time) / original_time) * 100

    if converter_success:
        if cached_success:
            ((converter_time - cached_time) / converter_time) * 100

    if multiple_success:
        multiple_time / 5

    # Success metrics

    if converter_success:
        if converter_time < 0.1:
            pass
        else:
            pass

    if cached_success:
        if cached_time < 0.1:
            pass
        else:
            pass

    # Verify output quality
    if isolated_success and original_success:
        if "<?xml" in isolated_result and "xliff" in isolated_result:
            pass
        if isolated_result == original_result:
            pass
        else:
            pass


if __name__ == "__main__":
    main()
