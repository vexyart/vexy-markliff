---
this_file: CHANGELOG.md
---

# Changelog

## Unreleased
### Added
- Package initializer now exposes `__version__`, `Config`, `process_data`, and `main` at the top level.
- Deterministic summary logic implemented for `process_data` with debug logging hooks.
- Expanded pytest coverage covering success, error, and debug scenarios.
- Hatch environments now set `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1` for deterministic test runs.

### Testing
- `2025-09-23`: `python -m pytest -xvs` → 5 passed, coverage 89% (line).

### Documentation
- Updated README Python API example to reflect the current helper functions.
- Introduced WORK.md to document manual test results.
- README highlights running tests via `uvx hatch run test`.
