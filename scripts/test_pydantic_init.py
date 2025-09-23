#!/usr/bin/env python3
"""
Test if Pydantic initialization is affected by OTEL environment.
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


def main():
    """Test Pydantic initialization timing."""

    # Ensure OTEL environment is set
    os.environ["OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE"] = "delta"

    # Test 1: First model definition
    def test_first_model():
        from pydantic import BaseModel, Field

        class FirstModel(BaseModel):
            id: str = Field(..., description="Test field")

        # Create an instance to trigger initialization
        return FirstModel(id="test")

    time_execution("First Pydantic model definition + instantiation", test_first_model)

    # Test 2: Second model definition (should be fast)
    def test_second_model():
        from pydantic import BaseModel, Field

        class SecondModel(BaseModel):
            name: str = Field(..., description="Another test field")

        return SecondModel(name="test")

    time_execution("Second Pydantic model definition + instantiation", test_second_model)

    # Test 3: Third model definition (should also be fast)
    def test_third_model():
        from pydantic import BaseModel, Field

        class ThirdModel(BaseModel):
            value: int = Field(..., description="Integer field")

        return ThirdModel(value=42)

    time_execution("Third Pydantic model definition + instantiation", test_third_model)


if __name__ == "__main__":
    main()
