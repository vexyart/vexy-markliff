#!/usr/bin/env python3
"""
Performance profiling script for vexy-markliff import times.
Identifies heavy imports that could benefit from lazy loading.
"""

import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def profile_import(module_name: str) -> float:
    """Profile the import time of a module."""
    start_time = time.perf_counter()
    try:
        __import__(module_name)
        end_time = time.perf_counter()
        return end_time - start_time
    except ImportError:
        return 0.0


def main():
    """Profile import times for key modules."""

    # Key modules to profile
    modules_to_profile = [
        "vexy_markliff",
        "vexy_markliff.cli",
        "vexy_markliff.config",
        "vexy_markliff.core.parser",
        "vexy_markliff.core.converter",
        "vexy_markliff.core.element_classifier",
        "vexy_markliff.core.format_style",
        "vexy_markliff.core.skeleton_generator",
        "vexy_markliff.models.xliff",
        "vexy_markliff.utils.validation",
        "vexy_markliff.utils.logging",
        "vexy_markliff.utils.text",
        # Heavy external dependencies
        "markdown_it",
        "lxml",
        "pydantic",
        "fire",
        "rich",
        "loguru",
    ]

    import_times = []

    for module in modules_to_profile:
        import_time = profile_import(module)
        import_times.append((module, import_time))

    # Sort by time (slowest first)
    import_times.sort(key=lambda x: x[1], reverse=True)

    for module, import_time in import_times[:10]:
        if import_time > 0:
            pass

    # Total import time
    sum(time for _, time in import_times if time > 0)

    # Recommendations
    slow_imports = [m for m, t in import_times if t > 0.010]  # >10ms
    if slow_imports:
        for module in slow_imports[:5]:
            pass
    else:
        pass


if __name__ == "__main__":
    main()
