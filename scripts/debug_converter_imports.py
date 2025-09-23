#!/usr/bin/env python3
"""
Debug which specific import in converter module is slow.
"""

import os
import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def time_import(_description: str, import_func):
    """Time an import function."""
    start_time = time.perf_counter()
    try:
        result = import_func()
        end_time = time.perf_counter()
        duration = end_time - start_time
        return result, duration
    except Exception:
        return None, 0.0


def clear_modules():
    """Clear all vexy_markliff modules from cache."""
    modules_to_clear = [m for m in sys.modules if m.startswith("vexy_markliff")]
    for module in modules_to_clear:
        del sys.modules[module]


def main():
    """Debug converter module imports."""

    # Ensure OTEL environment is set
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"

    # Test individual imports from converter module
    test_imports = [
        ("models.xliff", lambda: __import__("vexy_markliff.models.xliff", fromlist=[""])),
        ("utils.fallback", lambda: __import__("vexy_markliff.utils.fallback", fromlist=[""])),
        ("utils.validation", lambda: __import__("vexy_markliff.utils.validation", fromlist=[""])),
        ("full converter module", lambda: __import__("vexy_markliff.core.converter", fromlist=[""])),
    ]

    for name, import_func in test_imports:
        clear_modules()
        time_import(f"Import {name}", import_func)


if __name__ == "__main__":
    main()
