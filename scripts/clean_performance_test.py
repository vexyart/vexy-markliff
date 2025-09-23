#!/usr/bin/env python3
"""Clean performance test with fresh Python processes."""
# this_file: scripts/clean_performance_test.py

import subprocess
import sys
from pathlib import Path


def test_in_fresh_process(test_code: str) -> tuple[float, str]:
    """Run test code in a fresh Python process and measure time."""
    src_path = Path(__file__).parent.parent / "src"

    full_code = f"""
import sys
import time
sys.path.insert(0, "{src_path}")

start_time = time.perf_counter()
try:
    {test_code}
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"SUCCESS:{{duration:.3f}}")
except Exception as e:
    end_time = time.perf_counter()
    duration = end_time - start_time
    print(f"ERROR:{{duration:.3f}}:{{e}}")
"""

    result = subprocess.run([sys.executable, "-c", full_code], check=False, capture_output=True, text=True)

    output = result.stdout.strip()
    if output.startswith("SUCCESS:"):
        return float(output.split(":")[1]), "SUCCESS"
    if output.startswith("ERROR:"):
        parts = output.split(":", 2)
        return float(parts[1]), f"ERROR: {parts[2] if len(parts) > 2 else 'Unknown'}"
    return 999.0, f"UNKNOWN: {output}"


def main():
    """Run clean performance tests."""

    # Test 1: VexyMarkliff converter access (should use optimized path)
    converter_test = """
from vexy_markliff.core.converter import VexyMarkliff
converter = VexyMarkliff()
result = converter.markdown_to_xliff("# Test", "en", "es")
assert "<?xml" in result
"""

    converter_time, converter_status = test_in_fresh_process(converter_test)

    # Test 2: Direct original XLIFF import (for comparison)
    xliff_test = """
from vexy_markliff.models.xliff import XLIFFDocument
doc = XLIFFDocument()
doc.add_file("test", "en", "es")
doc.add_unit("test", "unit1", "Hello")
result = doc.to_xml()
assert "<?xml" in result
"""

    xliff_time, xliff_status = test_in_fresh_process(xliff_test)

    # Test 3: Direct isolated XLIFF import
    isolated_test = """
from vexy_markliff.models._xliff_isolated import XLIFFDocument
doc = XLIFFDocument()
doc.add_file("test", "en", "es")
doc.add_unit("test", "unit1", "Hello")
result = doc.to_xml()
assert "<?xml" in result
"""

    isolated_time, isolated_status = test_in_fresh_process(isolated_test)

    # Analysis

    if "SUCCESS" in converter_status:
        if converter_time < 0.1:
            pass
        else:
            pass

    if "SUCCESS" in xliff_status:
        pass

    if "SUCCESS" in isolated_status:
        pass

    # Determine which path the converter is actually using
    if "SUCCESS" in converter_status and "SUCCESS" in isolated_status and "SUCCESS" in xliff_status:
        if abs(converter_time - isolated_time) < 0.1 or abs(converter_time - xliff_time) < 0.1:
            pass
        else:
            pass

    if converter_time < 1.9:
        ((1.9 - converter_time) / 1.9) * 100


if __name__ == "__main__":
    main()
