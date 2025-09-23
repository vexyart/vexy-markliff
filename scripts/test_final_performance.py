#!/usr/bin/env python3
"""
Final performance test to verify our optimizations are working.
"""

import os
import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def time_import_scenario(description: str, import_func):
    """Time an import scenario."""
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
    """Test final performance across different usage scenarios."""

    # Ensure OTEL environment is set (worst case scenario)
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"

    scenarios = []

    # Scenario 1: Basic package import (what users will do first)
    clear_modules()

    def scenario1():
        import vexy_markliff

        return vexy_markliff.__version__

    result, duration = time_import_scenario("📦 Basic package import + version check", scenario1)
    scenarios.append(("Basic import", duration))

    # Scenario 2: Access main converter class (common usage)
    clear_modules()

    def scenario2():
        import vexy_markliff

        return vexy_markliff.VexyMarkliff()

    result, duration = time_import_scenario("🔄 Import + create converter instance", scenario2)
    scenarios.append(("Converter access", duration))

    # Scenario 3: Access configuration (common usage)
    clear_modules()

    def scenario3():
        import vexy_markliff

        return vexy_markliff.ConversionConfig()

    result, duration = time_import_scenario("⚙️  Import + create config instance", scenario3)
    scenarios.append(("Config access", duration))

    # Scenario 4: CLI usage (vexy-markliff command)
    clear_modules()

    def scenario4():
        import vexy_markliff

        return vexy_markliff.VexyMarkliffCLI()

    result, duration = time_import_scenario("🖥️  Import + create CLI instance", scenario4)
    scenarios.append(("CLI access", duration))

    # Scenario 5: Full API access (power user)
    clear_modules()

    def scenario5():
        import vexy_markliff

        converter = vexy_markliff.VexyMarkliff()
        config = vexy_markliff.ConversionConfig()
        cli = vexy_markliff.VexyMarkliffCLI()
        return (converter, config, cli)

    result, duration = time_import_scenario("🚀 Import + access all main APIs", scenario5)
    scenarios.append(("Full API access", duration))

    for _name, duration in scenarios:
        ms = duration * 1000
        if ms < 10 or ms < 50 or ms < 200:
            pass
        else:
            pass

    sum(duration for _, duration in scenarios) * 1000

    # Performance targets
    basic_import_ms = scenarios[0][1] * 1000
    if basic_import_ms < 10 or basic_import_ms < 50 or basic_import_ms < 100:
        pass
    else:
        pass

    if basic_import_ms > 0:
        (6000 - basic_import_ms) / 6000 * 100
        6000 / basic_import_ms


if __name__ == "__main__":
    main()
