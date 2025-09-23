#!/usr/bin/env python3
"""
Detailed profiling of config module imports to identify bottlenecks.
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


def profile_config_dependencies():
    """Profile each dependency of the config module."""

    # Test config module dependencies in order
    deps_to_test = [
        "os",
        "re",
        "enum",
        "pathlib",
        "typing",
        "yaml",
        "pydantic",
        "vexy_markliff.exceptions",
        "vexy_markliff.utils.logging",
    ]

    import_times = []
    total_time = 0

    for dep in deps_to_test:
        import_time = profile_individual_import(dep)
        import_times.append((dep, import_time))
        total_time += import_time

    # Find slow imports
    slow_imports = [(name, time_taken) for name, time_taken in import_times if time_taken > 0.050]
    if slow_imports:
        for _name, _time_taken in slow_imports:
            pass

    # Test the config module itself
    profile_individual_import("vexy_markliff.config")


if __name__ == "__main__":
    profile_config_dependencies()
