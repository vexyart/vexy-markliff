#!/usr/bin/env python3
"""
Trace all imports that happen when loading config module.
"""

import importlib.util
import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


class ImportTracer:
    """Trace imports with timing."""

    def __init__(self):
        self.import_times = []
        self.original_import = __builtins__.__import__

    def start(self):
        """Start tracing imports."""
        __builtins__.__import__ = self._traced_import

    def stop(self):
        """Stop tracing imports."""
        __builtins__.__import__ = self.original_import

    def _traced_import(self, name, globals=None, locals=None, fromlist=(), level=0):
        """Traced import function."""
        start_time = time.perf_counter()
        try:
            result = self.original_import(name, globals, locals, fromlist, level)
            end_time = time.perf_counter()
            duration = end_time - start_time

            # Only track significant imports
            if duration > 0.001:  # >1ms
                self.import_times.append((name, duration * 1000))

            return result
        except Exception:
            end_time = time.perf_counter()
            duration = end_time - start_time
            self.import_times.append((f"{name} (FAILED)", duration * 1000))
            raise


def main():
    """Trace config module imports."""

    tracer = ImportTracer()
    tracer.start()

    start_time = time.perf_counter()
    try:
        import vexy_markliff.config
    finally:
        tracer.stop()

    end_time = time.perf_counter()
    (end_time - start_time) * 1000

    # Sort by duration
    tracer.import_times.sort(key=lambda x: x[1], reverse=True)

    for _name, _duration in tracer.import_times[:10]:
        pass

    # Look for specific heavy imports
    heavy_imports = [item for item in tracer.import_times if item[1] > 50]
    if heavy_imports:
        for _name, _duration in heavy_imports:
            pass


if __name__ == "__main__":
    main()
