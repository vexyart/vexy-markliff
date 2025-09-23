#!/usr/bin/env python3
"""Debug which import path the converter is actually taking."""
# this_file: scripts/debug_converter_path.py

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def debug_import_step(_step_name: str, import_func):
    """Debug an import step with timing."""
    start_time = time.perf_counter()
    try:
        result = import_func()
        end_time = time.perf_counter()
        duration = end_time - start_time
        return result, duration, True
    except Exception:
        end_time = time.perf_counter()
        duration = end_time - start_time
        return None, duration, False


def main():
    # Step 1: Try isolated models directly
    def test_isolated():
        from vexy_markliff.models._xliff_isolated import XLIFFDocument

        return XLIFFDocument

    isolated_class, isolated_time, isolated_success = debug_import_step("Import isolated XLIFFDocument", test_isolated)

    # Step 2: Test the converter helper function
    def test_helper():
        from vexy_markliff.core.converter import _get_xliff_document_class

        return _get_xliff_document_class()

    helper_class, helper_time, helper_success = debug_import_step("Get XLIFFDocument via helper function", test_helper)

    # Step 3: Check which class we actually get
    if helper_success and helper_class:
        if (
            helper_class.__module__ == "vexy_markliff.models._xliff_isolated"
            or helper_class.__module__ == "vexy_markliff.models.xliff"
        ):
            pass
        else:
            pass

    # Step 4: Test full converter import (without usage)
    def test_converter_import():
        from vexy_markliff.core.converter import VexyMarkliff

        return VexyMarkliff

    converter_class, import_time, import_success = debug_import_step("Import VexyMarkliff class", test_converter_import)

    # Step 5: Test converter instantiation
    def test_converter_init():
        if converter_class:
            return converter_class()
        return None

    converter_instance, init_time, init_success = debug_import_step("Instantiate VexyMarkliff", test_converter_init)

    # Step 6: Test first method call (this triggers XLIFFDocument import)
    def test_first_call():
        if converter_instance:
            return converter_instance.markdown_to_xliff("# Test", "en", "es")
        return None

    result, call_time, call_success = debug_import_step("First converter method call", test_first_call)

    # Analysis
    total_time = 0
    if isolated_success:
        total_time += isolated_time
    if helper_success:
        total_time += helper_time
    if import_success:
        total_time += import_time
    if init_success:
        total_time += init_time
    if call_success:
        total_time += call_time

    # Identify bottleneck
    times = []
    if isolated_success:
        times.append(("Isolated import", isolated_time))
    if helper_success:
        times.append(("Helper function", helper_time))
    if import_success:
        times.append(("Converter import", import_time))
    if init_success:
        times.append(("Instantiation", init_time))
    if call_success:
        times.append(("Method call", call_time))

    if times:
        max(times, key=lambda x: x[1])


if __name__ == "__main__":
    main()
