#!/usr/bin/env python3
"""
Test which part of the XLIFF models is causing the slowdown.
"""

import os
import sys
import time
from pathlib import Path

# Add project to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))


def time_execution(description: str, func):
    """Time a function execution."""
    start_time = time.perf_counter()
    try:
        result = func()
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
    """Test model components step by step."""

    # Ensure OTEL environment is set
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"

    # Test 1: Basic imports
    clear_modules()

    def test_basic_imports():
        from pydantic import BaseModel, ConfigDict, Field

        from vexy_markliff.exceptions import ValidationError

        return True

    time_execution("Basic imports (pydantic + exceptions)", test_basic_imports)

    # Test 2: Simple model definition
    clear_modules()

    def test_simple_model():
        from typing import Union

        from pydantic import BaseModel, ConfigDict, Field

        class SimpleModel(BaseModel):
            model_config = ConfigDict(extra="allow")
            id: str = Field(..., description="Test field")
            target: str | None = Field(None, description="Optional field")

        return SimpleModel

    time_execution("Simple model definition", test_simple_model)

    # Test 3: Complex model with methods
    clear_modules()

    def test_complex_model():
        from typing import Any, Union

        from pydantic import BaseModel, ConfigDict, Field

        class ComplexModel(BaseModel):
            model_config = ConfigDict(extra="allow", populate_by_name=True)
            version: str = Field("2.1", description="Version")
            xmlns: str = Field("urn:test", description="Namespace")

            def to_xml(self) -> str:
                from xml.sax.saxutils import escape

                return f'<test version="{escape(self.version)}"/>'

        return ComplexModel

    time_execution("Complex model with methods", test_complex_model)

    # Test 4: Full XLIFF models
    clear_modules()

    def test_full_models():
        from vexy_markliff.models.xliff import XLIFFDocument

        return XLIFFDocument

    time_execution("Full XLIFF models", test_full_models)


if __name__ == "__main__":
    main()
