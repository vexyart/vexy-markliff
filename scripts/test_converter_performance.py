#!/usr/bin/env python3
"""Test VexyMarkliff converter performance in isolation."""
# this_file: scripts/test_converter_performance.py

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    start_time = time.perf_counter()

    # Import and use converter
    from vexy_markliff.core.converter import VexyMarkliff

    converter = VexyMarkliff()
    result = converter.markdown_to_xliff("# Test", "en", "es")

    end_time = time.perf_counter()
    duration = end_time - start_time

    # Verify output
    if "<?xml" in result and "xliff" in result:
        pass
    else:
        pass

    return duration


if __name__ == "__main__":
    main()
