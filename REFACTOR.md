# Refactoring Plan: Slimming Down Vexy-Markliff

## Project Overview

Vexy Markliff is a Python package and Fire CLI tool for bidirectional conversion between Markdown/HTML and XLIFF 2.1 format, enabling high-fidelity localization workflows. The system provides two conversion modes: one-document mode for single-source workflows and two-document mode for parallel source-target alignment.

**Project Scope (One Sentence):** Fetch Markdown/HTML, convert to XLIFF (and back) with selectable storage modes for source/target text.

## Resources for you to consult

@docs/500-intro.md
@docs/502-htmlattr.md
@docs/510-prefs-html0.md
@docs/511-prefs-html1.md
@docs/512-prefs-html2.md
@docs/513-prefs-md.md
@docs/520-var.md
@docs/530-vexy-markliff-spec.md

---

@docs/540-extras.md
@external/901-xliff-spec-core-21.xml
@external/executablebooks-markdown-it-py.md
@external/executablebooks-markdown-it-py folder
@external/mdit-py-plugins folder
@external/Xliff-AI-Translator folder
@external/translate-toolkit folder



## Executive Summary

The current implementation of Vexy Markliff suffers from significant bloat, particularly in the `src/vexy_markliff/utils` directory, which contains over 25 files dedicated to enterprise-level features such as caching, backup/recovery, diagnostics, memory management, resilience, security scanning, and advanced validation. These features add unnecessary complexity, increase dependencies, degrade performance (e.g., via heavy initialization and monitoring overhead), and violate the principle of simplicity for a specialized conversion tool.

**Core Objective**: Radically trim the package to focus exclusively on bidirectional conversion between Markdown/HTML and XLIFF 2.1, preserving round-trip fidelity, XLIFF compliance, and basic segmentation/skeleton management. Leverage built-in Python libraries (e.g., `logging`, `pathlib`) and well-maintained packages (e.g., `markdown-it-py`, `lxml`, `nltk` for segmentation) to eliminate custom utilities. Target: Reduce source files from ~50 to <15, eliminate the `utils` folder, achieve <200 lines per file, and improve startup time by 80%+.

**Key Principles**:
- **Build vs. Buy**: Replace custom code with packages where possible (e.g., no custom cache—use `functools.lru_cache` if truly needed for hotspots).
- **Minimalism**: If a feature isn\'t directly tied to conversion fidelity or compliance, delete it.
- **Verification**: Maintain 80%+ test coverage on core functionality; remove tests for deleted features.
- **Performance**: Eliminate heavy imports (e.g., opentelemetry, pydantic overhead for non-models); use lazy loading and streaming where applicable.

**Estimated Impact**:
- Codebase size: Reduce by 70-80% (from ~10k+ LOC to ~2-3k).
- Dependencies: Trim from 20+ to 8-10 core ones.
- Maintainability: Single-purpose files, no deep nesting, flat structure.

## Problem Analysis

**What are we solving and why?** The bloat from enterprise features slows the tool and adds debt. Trimming focuses on core conversion.

**Constraints**: Preserve compliance, API, fidelity.

**Solution Options**:
1. Rewrite: Clean but risky.
2. Pruning: Balanced, chosen.

**Edge Cases**: Large files, complex structures, invalid input—handle with tests.

**Test Strategy**: Baseline, E2E round-trip, coverage.

## Current Audit

Core: Keep core/, models/, cli.py—simplify.
Bloat: Delete utils/* (27 files).
Tests: Keep core, delete bloat.

## Phases

1. **Preparation**: Run tests, audit usages (grep).
2. **Deletion**: rm utils, replace with stdlib (logging, etc.).
3. **Optimization**: Integrate nltk for segmentation if custom; lru_cache.
4. **Testing**: Expand round-trip tests, verify performance.
5. **Docs**: Update README, deps, changelog.

## Packages to Use
- lxml: XML/XLIFF.
- markdown-it-py: MD parsing.
- nltk: Sentence split (add if needed).
- functools: Caching.
- logging: Stdlib.
- pydantic: Config only.

## Verification Checklist
- ✓ Tests pass.
- ✓ Coverage >80%.
- ✓ No utils folder.
- ✓ Files <200 lines.
- ✓ Faster init.

## 1. Philosophy & Goals

The current `vexy-markliff` package is over-engineered with numerous "enterprise-grade" features that are unnecessary for a command-line conversion utility. This refactoring plan aims to radically simplify the codebase to achieve the following goals:

-   **Focus:** The package should do one thing and do it well: **bidirectional conversion between Markdown/HTML and XLIFF 2.1.**
-   **Simplicity:** Drastically reduce the codebase size and complexity. Eliminate abstractions, managers, and non-core features.
-   **Performance:** Improve startup time and processing speed by removing complex layers of indirection, caching, and monitoring.
-   **Maintainability:** Make the code easier to understand, test, and maintain by relying on standard Python libraries and a minimal set of high-quality dependencies.

The guiding principle is: **If it's not essential for the core conversion task, remove it.**

## 2. Core Dependencies to Keep

We will rely on a minimal set of well-vetted libraries for the core logic:

-   **`lxml`**: For robust and performant XML/HTML parsing and serialization.
-   **`markdown-it-py`**: For flexible and fast Markdown parsing.
-   **`pydantic`**: For data validation and settings management (in a simplified form).
-   **`python-fire`**: For the command-line interface.
-   **`rich`**: For CLI output.
-   **Python Standard Library**: `os`, `pathlib`, `re`, `logging`, `dataclasses`, etc.

All other non-essential runtime dependencies should be removed.

## 3. Radical Simplification: The `utils` Massacre

The `src/vexy_markliff/utils` directory is the primary source of bloat and will be almost entirely eliminated.

| Module to Remove                      | Justification                                                                                                   | Replacement Strategy                                                                                             |
| ------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------- |
| `advanced_validation.py`              | Overkill. Core validation can be handled by `pydantic` and basic checks.                                        | Use `pydantic` for data models. Use simple functions for path validation (`os.path.exists`).                     |
| `backup_recovery.py`                  | A CLI tool should not manage its own backups or transactions. This is the user's responsibility.                | **Remove completely.** Users can use version control or simple file copies if they need backups.                 |
| `batch_processor.py`                  | Concurrency adds significant complexity for a task that is typically I/O bound on a single file.                  | **Remove completely.** Process files serially. Users can script parallel execution in the shell if needed.       |
| `cache.py`                            | Caching adds complexity and potential for stale data. For a CLI tool, performance gains are negligible.         | **Remove completely.** Operations should be fast enough without caching.                                         |
| `config_migration.py`                 | Unnecessary for a simple tool. If the config changes, users can update their file.                              | **Remove completely.** Use a simple `pydantic` model for config. Breaking changes will be noted in the changelog. |
| `coverage_analyzer.py`                | This is a development/CI tool, not a runtime library feature.                                                   | **Remove completely.** Keep coverage analysis in CI scripts (`ci.yml`).                                          |
| `dependency_manager.py`               | Over-engineering. Dependencies should be managed by `uv` and defined in `pyproject.toml`.                        | **Remove completely.**                                                                                           |
| `diagnostics.py` / `enhanced_diagnostics.py` | Excessive. Standard logging and clear error messages are sufficient.                                      | **Remove completely.** Use Python's standard `logging` module and custom exceptions.                             |
| `doc_generator.py`                    | This is a development tool, not a runtime library feature.                                                      | **Remove completely.** Documentation should be written manually or with standard tools like Sphinx.              |
| `error_intelligence.py`               | Extreme over-engineering. Standard `try...except` blocks and clear exceptions are sufficient.                   | **Remove completely.**                                                                                           |
| `fallback.py`                         | Adds complexity. Dependencies should be required, not optional with fallbacks.                                  | **Remove completely.** Declare all necessary dependencies in `pyproject.toml`.                                   |
| `i18n.py`                             | Internationalizing a developer tool's own messages is unnecessary complexity.                                   | **Remove completely.** Use English for all logs and messages.                                                    |
| `import_isolation.py` / `pydantic_init.py` | A workaround for a problem (slow OTEL instrumentation) that won't exist after this refactoring.             | **Remove completely.** The simplified app will have fast startup times naturally.                                |
| `logging.py`                          | Custom logger is not needed.                                                                                    | Use the standard `logging` module or `loguru` if it's desired for simplicity.                                    |
| `memory_management.py` / `resource_manager.py` | Extreme over-engineering for a file conversion tool. The OS handles memory management.                  | **Remove completely.** If a file is too large, the tool can fail with a `MemoryError`.                           |
| `plugins.py`                          | A plugin architecture is a massive source of complexity and is not required for the core mission.               | **Remove completely.**                                                                                           |
| `profiles.py`                         | Configuration profiles are an unnecessary abstraction. Users can have multiple config files if needed.          | **Remove completely.** A single, simple configuration file is sufficient.                                        |
| `progress.py`                         | Progress bars are nice but can be handled by `rich` directly if needed.                                         | **Remove completely.** Use `rich.progress` directly in the CLI if progress indication is desired.                |
| `quality_metrics.py`                  | A development/CI tool.                                                                                          | **Remove completely.** Keep quality checks in CI scripts.                                                        |
| `resilience.py`                       | Circuit breakers and retries are for distributed systems, not a local file converter.                           | **Remove completely.**                                                                                           |
| `security.py`                         | Overkill. `lxml` has built-in protection against XXE. Basic path validation is enough.                          | **Remove completely.** Rely on `lxml`'s security features and basic `os.path` checks.                             |
| `test_stabilization.py`               | A development/testing utility.                                                                                  | **Remove completely.** Test stability should be handled by writing good tests, not runtime helpers.              |
| `text.py`                             | The functions here are trivial.                                                                                 | Move any truly essential text helper (e.g., `normalize_whitespace`) to a single `utils.py` file.                 |
| `type_safety.py`                      | `pydantic` and standard Python type hints are sufficient.                                                       | **Remove completely.** Rely on `mypy` for static analysis and `pydantic` for runtime model validation.           |
| `validation.py`                       | Redundant with `pydantic` and `advanced_validation.py`.                                                         | **Remove completely.** Use `pydantic` for data models.                                                           |

## 4. Proposed New Structure

The new structure will be significantly flatter and simpler.

```
src/
└── vexy_markliff/
    ├── core/
    │   ├── __init__.py
    │   ├── converter.py      # Core conversion logic
    │   └── parser.py         # HTML/Markdown parsing logic
    ├── __init__.py
    ├── cli.py                # Fire-based CLI
    ├── config.py             # Single Pydantic config model
    ├── exceptions.py         # Custom exceptions
    └── utils.py              # A *single* file for truly shared, simple helper functions
```

## 5. Refactoring Execution Plan

This will be a destructive and reconstructive process.

1.  **Branch:** Create a new branch `refactor/simplify`.
2.  **Delete:**
    -   Delete the entire `src/vexy_markliff/utils` directory.
    -   Delete the entire `tests` directory related to the `utils` modules.
    -   Delete `converter_lite.py`, `_xliff_fast.py`, `_xliff_isolated.py`, `_config_fast.py` and other "performance" variations. There should be one simple, clear implementation.
3.  **Create `src/vexy_markliff/utils.py`:** Create a new, empty file. It should only be populated with functions that are simple, pure, and truly shared between other modules.
4.  **Rewrite `config.py`:**
    -   Create a single `pydantic.BaseModel` for configuration.
    -   Remove all profiles, migration, and backward compatibility logic.
    -   The config should be loaded directly from a single `vexy-markliff.yaml` file if it exists.
5.  **Refactor `core/` modules:**
    -   Go through `converter.py`, `parser.py`, and other core files.
    -   Remove all imports from the old `utils` directory.
    -   Replace functionality with direct calls to standard libraries or the new `utils.py`.
    -   Eliminate any logic related to caching, resilience, plugins, etc.
6.  **Refactor `cli.py`:**
    -   Simplify the CLI commands. Remove any commands related to the deleted features (profiles, diagnostics, etc.).
    -   The CLI should primarily expose the conversion functions.
7.  **Rewrite Tests:**
    -   Write new, simple tests that target the core conversion logic.
    -   Focus on input/output validation. Test a variety of Markdown and HTML structures.
    -   Ensure tests are fast and reliable. Delete all tests for the removed `utils` features.
8.  **Update `pyproject.toml`:**
    -   Remove all dependencies that are no longer needed.
9.  **Review and Merge:**
    -   Thoroughly review the simplified codebase to ensure it meets the goals of the refactoring.
    -   Run all tests and linters.
    -   Merge the branch.
