"""Test suite for vexy_markliff."""
# this_file: tests/test_package.py

from __future__ import annotations

import logging

import pytest

from vexy_markliff import Config, __version__, process_data


def test_version_and_config_are_exposed() -> None:
    """Package exposes metadata and core helpers at the top level."""

    assert __version__
    assert Config(name="sample", value="demo")


def test_process_data_when_values_then_returns_summary() -> None:
    """process_data normalises values and reports summary statistics."""

    config = Config(name="summary", value="baseline", options={"mode": "count"})
    result = process_data([" alpha ", "beta", "alpha"], config=config)

    assert result["items"] == ["alpha", "beta", "alpha"]
    assert result["summary"] == {"total": 3, "unique": 2}
    assert result["count"] == 3
    assert result["unique"] == 2
    assert result["frequency"] == {"alpha": 2, "beta": 1}
    assert result["config"] == {
        "name": "summary",
        "value": "baseline",
        "options": {"mode": "count"},
    }


def test_process_data_when_not_list_then_raises_type_error() -> None:
    """Non-list inputs are rejected to keep behaviour predictable."""

    with pytest.raises(TypeError) as exc:
        process_data({"alpha": 1})  # type: ignore[arg-type]

    assert "data must be provided as a list" in str(exc.value)


def test_process_data_when_empty_inputs_then_raises_value_error() -> None:
    """Empty or blank-only inputs raise a descriptive error."""

    with pytest.raises(ValueError) as exc:
        process_data([" ", "\n\t"])

    assert "at least one non-empty item" in str(exc.value)


def test_process_data_when_debug_enabled_then_logs(caplog: pytest.LogCaptureFixture) -> None:
    """Debug flag elevates logging level and emits helpful diagnostics."""

    with caplog.at_level(logging.DEBUG):
        process_data([1, 1, 2], debug=True)

    assert any("Debug mode enabled" in message for message in caplog.messages)
