#!/usr/bin/env python3
"""Import performance benchmark script for vexy-markliff.

this_file: scripts/benchmark_imports.py

This script measures import times for various modules to track
performance improvements and detect regressions.
"""

import importlib
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


def time_import(module_name: str) -> tuple[float, str | None]:
    """Time the import of a module.

    Args:
        module_name: Name of module to import

    Returns:
        Tuple of (import_time_seconds, error_message)
    """
    # Clear module cache to get accurate timing
    if module_name in sys.modules:
        del sys.modules[module_name]

    start = time.time()
    try:
        importlib.import_module(module_name)
        end = time.time()
        return end - start, None
    except Exception as e:
        end = time.time()
        return end - start, str(e)


def main():
    """Run import benchmarks."""

    modules = [
        # Core package
        "vexy_markliff",
        # Core modules (optimized with lazy imports)
        "vexy_markliff.core.parser",
        "vexy_markliff.core.element_classifier",
        "vexy_markliff.core.format_style",
        "vexy_markliff.core.skeleton_generator",
        "vexy_markliff.core.inline_handler",
        "vexy_markliff.core.structure_handler",
        # Models (optimized with Pydantic v2)
        "vexy_markliff.models.xliff",
        "vexy_markliff.models.document_pair",
        # Utilities
        "vexy_markliff.utils.logging",
        "vexy_markliff.utils.validation",
        # Configuration (with YAML dependency)
        "vexy_markliff.config",
        # Exception handling
        "vexy_markliff.exceptions",
    ]

    results = []
    total_time = 0

    for module in modules:
        import_time, error = time_import(module)
        results.append((module, import_time, error))
        if not error:
            total_time += import_time

        "ERROR" if error else f"{import_time * 1000:.1f}ms"

        if error:
            pass

    # Performance targets and warnings
    slow_modules = [(m, t) for m, t, e in results if not e and t > 0.1]  # >100ms
    if slow_modules:
        for _module, _import_time in slow_modules:
            pass

    failed_modules = [(m, e) for m, t, e in results if e]
    if failed_modules:
        for _module, _error in failed_modules:
            pass

    if not slow_modules and not failed_modules:
        pass


if __name__ == "__main__":
    main()
