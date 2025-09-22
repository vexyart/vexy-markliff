"""Top-level package for vexy_markliff."""
# this_file: src/vexy_markliff/__init__.py

from .__version__ import __version__
from .vexy_markliff import Config, main, process_data

__all__ = [
    "__version__",
    "Config",
    "main",
    "process_data",
]
