#!/usr/bin/env python3
"""
Test the effectiveness of our import isolation solution.
"""

import os
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


def clear_module_cache():
    """Clear vexy_markliff modules from cache."""
    modules_to_clear = [m for m in sys.modules if m.startswith("vexy_markliff")]
    for module in modules_to_clear:
        del sys.modules[module]


def test_isolation_effectiveness():
    """Test if our import isolation prevents OTEL slowdown."""

    # Ensure OTEL environment is set (the problematic condition)
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"

    # Test 1: Import config module directly (should be slow)
    clear_module_cache()

    def import_config_direct():
        import vexy_markliff.config

        return vexy_markliff.config

    result1, time1 = time_import("Direct config import (should be slow)", import_config_direct)

    # Test 2: Import using our isolation utility
    clear_module_cache()

    def import_config_isolated():
        from vexy_markliff.utils.import_isolation import import_with_isolation

        return import_with_isolation("vexy_markliff.config")

    result2, time2 = time_import("Isolated config import (should be fast)", import_config_isolated)

    # Test 3: Import main package with lazy loading (should use isolation)
    clear_module_cache()

    def import_main_package():
        import vexy_markliff

        # Trigger lazy loading of config
        return vexy_markliff.ConversionConfig

    result3, time3 = time_import("Main package with lazy loading", import_main_package)

    # Calculate improvements
    if time1 > 0 and time2 > 0:
        improvement = ((time1 - time2) / time1) * 100

        if improvement > 50 or improvement > 20:
            pass
        else:
            pass

    if time1 > 0 and time3 > 0:
        ((time1 - time3) / time1) * 100


if __name__ == "__main__":
    test_isolation_effectiveness()
