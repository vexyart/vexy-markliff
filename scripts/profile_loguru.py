#!/usr/bin/env python3
"""
Test if loguru is the cause of slow logging imports.
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
    """Test loguru import time."""

    # Test loguru import
    def import_loguru():
        from loguru import logger

        return logger

    # Test standard logging
    def import_logging():
        import logging

        return logging

    result1, time1 = time_import("Standard logging", import_logging)
    result2, time2 = time_import("Loguru import", import_loguru)

    if time2 > 50:  # If loguru takes >50ms
        pass


if __name__ == "__main__":
    main()
