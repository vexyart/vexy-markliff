#!/usr/bin/env python3
"""Test repeated converter access to verify caching works."""
# this_file: scripts/test_repeated_access.py

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def main():
    """Test repeated converter access."""

    from vexy_markliff.core.converter import VexyMarkliff

    times = []

    # Test 5 sequential converter uses
    for i in range(5):
        start_time = time.perf_counter()

        converter = VexyMarkliff()
        converter.markdown_to_xliff(f"# Test {i + 1}", "en", "es")

        end_time = time.perf_counter()
        duration = end_time - start_time
        times.append(duration)

    # Analysis

    sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)

    # Check consistency
    if max_time < 0.1:
        pass
    else:
        pass

    if max_time - min_time < 0.01 or max_time - min_time < 0.05:
        pass
    else:
        pass


if __name__ == "__main__":
    main()
