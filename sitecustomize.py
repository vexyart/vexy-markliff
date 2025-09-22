"""Python startup hook to keep pytest runs deterministic."""
# this_file: sitecustomize.py

import os

os.environ.setdefault("PYTEST_DISABLE_PLUGIN_AUTOLOAD", "1")
