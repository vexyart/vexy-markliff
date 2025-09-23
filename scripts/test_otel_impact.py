#!/usr/bin/env python3
"""
Test if OpenTelemetry environment variables are causing slow imports.
"""

import os
import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def time_config_import(description: str):
    """Time config import with current environment."""

    # Clear any cached modules
    modules_to_clear = [m for m in sys.modules if m.startswith("vexy_markliff")]
    for module in modules_to_clear:
        del sys.modules[module]

    start_time = time.perf_counter()
    try:
        import vexy_markliff.config

        end_time = time.perf_counter()
        return end_time - start_time
    except Exception:
        return 0.0


def main():
    """Test impact of OpenTelemetry environment variables."""

    # Show current environment
    otel_vars = [k for k in os.environ if k.startswith("OTEL_")]
    logfire_vars = [k for k in os.environ if "LOGFIRE" in k.upper()]

    for var in otel_vars:
        pass

    for var in logfire_vars:
        pass

    if not otel_vars and not logfire_vars:
        pass

    # Test with current environment
    time1 = time_config_import("Config import WITH OTEL env")

    # Test without OTEL variables
    original_env = {}
    for var in otel_vars + logfire_vars:
        original_env[var] = os.environ.pop(var, None)

    time2 = time_config_import("Config import WITHOUT OTEL env")

    # Restore environment
    for var, value in original_env.items():
        if value is not None:
            os.environ[var] = value

    if time1 > time2 * 2:
        pass


if __name__ == "__main__":
    main()
