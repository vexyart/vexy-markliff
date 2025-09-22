---
this_file: TODO.md
---

# Vexy Markliff TODO

## Active Quality Sprint (Q1 2025)
- [ ] Automate disabling of third-party pytest plugins so test runs require no manual environment overrides.

### Completed (2025-09-23)
- Package initializer now re-exports `__version__`, `Config`, `process_data`, and `main`.
- `process_data` exposes deterministic summary logic and CLI demo is aligned.
- Pytest coverage expanded; documentation refreshed (WORK.md, CHANGELOG).

## Phase 1: Foundation & Core Architecture

### 1.1 Project Structure Setup
- [ ] Set up modern Python package structure
- [ ] Configure pyproject.toml with dependencies
- [ ] Establish testing framework with pytest
- [ ] Set up CI/CD pipeline with GitHub Actions

### 1.2 Core Data Models (Pydantic)
- [ ] Create `XLIFFDocument` model with XLIFF 2.1 schema validation
- [ ] Create `Unit` and `Segment` models with Format Style attributes
- [ ] Create `SkeletonFile` model for external structure storage
- [ ] Create `ConversionConfig` model for configuration management
- [ ] Create `TwoDocumentPair` model for parallel document handling

### 1.3 HTML Parser Implementation
- [ ] Implement HTML element classification system following docs/510-512 specs
- [ ] Implement Format Style attribute serialization with escaping rules
- [ ] Implement skeleton generation with placeholder system (`###u1###`)
- [ ] Implement inline element handling (`<mrk>`, `<ph>` generation)
- [ ] Implement complex structure preservation (tables, forms, media)

## Phase 2: XLIFF 2.1 Engine

### 2.1 XLIFF Generation
- [ ] Implement XLIFF 2.1 Core document structure generation
- [ ] Implement Format Style module (`fs:fs`, `fs:subFs`)
- [ ] Implement external skeleton file management
- [ ] Implement `originalData` handling for placeholders
- [ ] Implement namespace management and validation

### 2.2 Content Extraction Rules
- [ ] Implement block-level element handling (paragraphs, headings, lists)
- [ ] Implement inline element preservation with `<mrk>` wrapping
- [ ] Implement void element handling with `<ph>` placeholders
- [ ] Implement table and form preservation with `xml:space="preserve"`
- [ ] Implement intelligent segmentation (respect `<s>`, split `<p>` by sentences)

### 2.3 Round-trip Reconstruction
- [ ] Implement skeleton merging with translated content
- [ ] Implement Format Style attribute reconstruction to HTML
- [ ] Implement placeholder resolution from `originalData`
- [ ] Implement structure validation and integrity checks

## Phase 3: Markdown Integration

### 3.1 Markdown Parser Setup
- [ ] Configure markdown-it-py with selected plugins
- [ ] Implement front-matter handling (YAML/TOML preservation)
- [ ] Implement extension support (tables, footnotes, task lists, strikethrough)
- [ ] Implement HTML passthrough for mixed content

### 3.2 Markdown → HTML → XLIFF Pipeline
- [ ] Implement deterministic HTML rendering from Markdown
- [ ] Implement metadata preservation for round-trip reconstruction
- [ ] Implement reference link definition handling
- [ ] Implement code fence and inline code preservation

### 3.3 XLIFF → HTML → Markdown Pipeline
- [ ] Implement HTML reconstruction from XLIFF with skeleton
- [ ] Implement Markdown syntax restoration using preserved metadata
- [ ] Implement link reference recreation
- [ ] Implement front-matter restoration

## Phase 4: Conversion Modes

### 4.1 One-Document Mode
- [ ] Implement source-only storage (`<source>` elements only)
- [ ] Implement target-only storage (`<target>` elements only)
- [ ] Implement both storage (`<source>` and `<target>` elements)
- [ ] Implement configuration-driven mode selection

### 4.2 Two-Document Mode
- [ ] Implement parallel document loading and parsing
- [ ] Implement structural alignment algorithm (headings, lists, paragraphs)
- [ ] Implement sentence-level alignment within matched structures
- [ ] Implement divergence detection and fallback handling
- [ ] Implement alignment quality reporting

## Phase 5: CLI Interface

### 5.1 Core Commands
- [ ] Implement `md2xliff` - Markdown to XLIFF conversion
- [ ] Implement `html2xliff` - HTML to XLIFF conversion
- [ ] Implement `xliff2md` - XLIFF to Markdown conversion
- [ ] Implement `xliff2html` - XLIFF to HTML conversion
- [ ] Implement `batch-convert` - Bulk processing with parallel execution

### 5.2 Configuration System
- [ ] Implement YAML configuration file support
- [ ] Implement environment variable overrides
- [ ] Implement CLI argument precedence handling
- [ ] Implement configuration validation and defaults

### 5.3 User Experience
- [ ] Implement Rich progress indicators for long operations
- [ ] Implement detailed error reporting with suggestions
- [ ] Implement verbose mode with debug logging
- [ ] Implement dry-run mode for validation

## Phase 6: Quality Assurance & Testing

### 6.1 Test Suite Development
- [ ] Write unit tests for all core functions (>80% coverage)
- [ ] Write integration tests for full conversion pipelines
- [ ] Write round-trip fidelity tests (Markdown → XLIFF → Markdown)
- [ ] Write edge case handling tests (malformed input, large files)
- [ ] Write performance benchmarks (10k-line documents <10s)

### 6.2 Validation Framework
- [ ] Implement XLIFF 2.1 schema validation against official XSD
- [ ] Implement Format Style module compliance checking
- [ ] Implement HTML5 fragment validation for generated snippets
- [ ] Implement Markdown CommonMark compliance verification

### 6.3 Sample Data & Fixtures
- [ ] Integrate CommonMark test suite
- [ ] Create real-world document samples (technical docs, blogs, wikis)
- [ ] Create complex HTML structures (tables, forms, media)
- [ ] Create multilingual content examples

## Phase 7: Documentation & Distribution

### 7.1 Documentation
- [ ] Generate API documentation with docstring generation
- [ ] Write CLI usage guide with examples
- [ ] Write configuration reference
- [ ] Write integration patterns and best practices
- [ ] Write troubleshooting guide

### 7.2 Package Distribution
- [ ] Publish PyPI package
- [ ] Create GitHub releases with changelog
- [ ] Create Docker container for isolated execution
- [ ] Create Homebrew formula for macOS

## Critical Dependencies to Add

### Core Dependencies
- [ ] Add markdown-it-py
- [ ] Add mdit-py-plugins (front-matter, footnotes, task-lists, tables, strikethrough)
- [ ] Add lxml
- [ ] Add fire
- [ ] Add pydantic
- [ ] Add rich

### Optional Dependencies
- [ ] Add nltk or spacy for sentence splitting
- [ ] Add pathlib (built-in Python 3.4+)

### Development Dependencies
- [ ] Add pytest
- [ ] Add pytest-cov
- [ ] Add pytest-mock
- [ ] Add ruff
- [ ] Add mypy

## Immediate Next Steps
- [ ] Export package version from `vexy_markliff/__init__.py` so the public API exposes `__version__`, `Config`, and `process_data`.
- [ ] Disable third-party pytest plugin auto-loading inside the test suite for deterministic runs.
- [ ] Replace the placeholder `process_data` implementation with a simple normalization workflow and add unit coverage.
- [ ] Run `uv add markdown-it-py mdit-py-plugins lxml fire pydantic rich`
- [ ] Run `uv add --dev pytest pytest-cov pytest-mock ruff mypy`
- [ ] Create basic project structure under `src/vexy_markliff/`
- [ ] Write first unit test for HTML parsing
- [ ] Implement basic XLIFF document model with Pydantic
