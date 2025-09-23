#!/usr/bin/env python3
"""
Test if the version import issue is caused by the main __init__.py
"""

import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def time_import(description: str, import_func):
    """Time an import function."""
    start_time = time.perf_counter()
    try:
        result = import_func()
        end_time = time.perf_counter()
        duration = end_time - start_time
        return result, duration
    except Exception:
        return None, 0.0


def main():
    """Test different ways of importing version to isolate the issue."""

    # Test 1: Direct file import
    def direct_import():
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "__version__", project_root / "src" / "vexy_markliff" / "__version__.py"
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.__version__

    # Test 2: Regular package import
    def package_import():
        from vexy_markliff.__version__ import __version__

        return __version__

    # Test 3: Check if the main package is already imported
    def check_main_package():
        return "vexy_markliff" in sys.modules

    # Run tests
    result1, time1 = time_import("Direct file import", direct_import)

    result2, time2 = time_import("Regular package import", package_import)

    if time2 > time1 * 10:  # If package import is >10x slower
        pass


if __name__ == "__main__":
    main()
