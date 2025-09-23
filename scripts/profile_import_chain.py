#!/usr/bin/env python3
"""
Detailed profiling script to isolate the exact import causing the 6-second delay.
"""

import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def profile_individual_import(module_name: str) -> float:
    """Profile the import time of a single module."""
    start_time = time.perf_counter()
    try:
        __import__(module_name)
        end_time = time.perf_counter()
        return end_time - start_time
    except ImportError:
        return 0.0


def main():
    """Profile each import step in the vexy_markliff chain."""

    # Profile step by step imports to isolate the slow one
    imports_to_test = [
        "vexy_markliff.__version__",
        "vexy_markliff.exceptions",
        "vexy_markliff.config",
        "vexy_markliff.models.xliff",
        "vexy_markliff.utils.validation",
        "vexy_markliff.utils.logging",
        "vexy_markliff.utils.fallback",
        "vexy_markliff.core.converter",
        "vexy_markliff.cli",
        "vexy_markliff.vexy_markliff",  # This one might be the culprit
    ]

    total_time = 0
    slow_imports = []

    for module in imports_to_test:
        import_time = profile_individual_import(module)
        total_time += import_time
        if import_time > 0.050:  # >50ms is considered slow
            slow_imports.append((module, import_time))

    if slow_imports:
        for module, _time_taken in slow_imports:
            pass

    # Test the main vexy_markliff import last
    profile_individual_import("vexy_markliff")


if __name__ == "__main__":
    main()
