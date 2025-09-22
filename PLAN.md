# Vexy Markliff Development Plan

---
this_file: PLAN.md
---

## Project Overview

Vexy Markliff is a Python package and Fire CLI tool for bidirectional conversion between Markdown/HTML and XLIFF 2.1 format, enabling high-fidelity localization workflows. The system provides two conversion modes: one-document mode for single-source workflows and two-document mode for parallel source-target alignment.

**Project Scope (One Sentence):** Fetch Markdown/HTML, convert to XLIFF (and back) with selectable storage modes for source/target text.

## Active Quality Sprint (Q1 2025)

### Objectives
- Harden the public package surface so that importing `vexy_markliff` provides stable version metadata and exposes the core helpers needed by early adopters.
- Replace placeholder processing logic with a deterministic, well-tested summary routine that demonstrates the data flow without overcommitting to full conversion features.
- Backfill targeted unit tests to lock the behaviour, catch regressions, and document expected outcomes.

### Tasks (Completed 2025-09-23)
1. **Package Initializer Hardening** — Implemented; README documents exposed helpers, tests validate package metadata.
2. **Process Pipeline Skeleton** — `process_data` now provides deterministic summaries, robust error handling, and CLI demo alignment.
3. **Testing & Telemetry Foundations** — Test suite expanded, WORK.md/CHANGELOG.md updated, logging behaviour verified under debug mode.

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


...

## Immediate Quality Tasks

1. **Automate pytest isolation** — Completed by configuring Hatch environments to export `PYTEST_DISABLE_PLUGIN_AUTOLOAD=1`.
2. **Document standard test invocation** — README now directs developers to `uvx hatch run test` as the default workflow.
3. **Monitor summary logic coverage** — Ongoing; capture new edge cases as they arise during future development.

## Technical Architecture

### Core Components

1. **Parser Layer**
   - `markdown-it-py` with `mdit-py-plugins` for Markdown processing
   - `lxml` for HTML/XML parsing and generation
   - Custom HTML → AST → XLIFF extraction pipeline

2. **XLIFF Engine**
   - XLIFF 2.1 Core compliance with Format Style module support
   - Uses `fs:fs` and `fs:subFs` attributes for HTML element preservation
   - External skeleton file management for structure preservation

3. **Conversion Pipeline**
   ```
   Markdown ─┐             ┌─► XLIFF 2.1 ─┐
             ├─► HTML ─► AST ├─► Units    ├─► Merge ─► HTML ─┬─► Markdown
   HTML ─────┘             └─► Skeleton ─┘                 │
                                                        (optional)
   ```

4. **CLI Interface**
   - Fire-based command interface
   - Rich terminal output for user feedback
   - Configuration file support (YAML)

### Package Dependencies

#### Core Dependencies
- **markdown-it-py** (880 stars): Fast CommonMark parser with plugin support
- **mdit-py-plugins**: Essential extensions (tables, footnotes, front-matter, task lists)
- **lxml** (2813 stars): Robust XML/HTML parsing and generation with XPath support
- **fire**: Simple CLI interface generation
- **pydantic**: Data validation and settings management
- **rich**: Enhanced terminal output and progress indicators

#### Optional Dependencies
- **nltk** or **spacy**: Advanced sentence splitting for segmentation
- **pathlib**: Modern file path handling (built-in Python 3.4+)

#### Development Dependencies
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting
- **pytest-mock**: Mocking utilities
- **ruff**: Linting and formatting
- **mypy**: Type checking

## Implementation Plan

### Phase 1: Foundation & Core Architecture

#### 1.1 Project Structure Setup
- [x] Initialize project with `uv init`
- [ ] Set up modern Python package structure
- [ ] Configure pyproject.toml with dependencies
- [ ] Establish testing framework with pytest
- [ ] Set up CI/CD pipeline with GitHub Actions

#### 1.2 Core Data Models (Pydantic)
- [ ] `XLIFFDocument` model with XLIFF 2.1 schema validation
- [ ] `Unit` and `Segment` models with Format Style attributes
- [ ] `SkeletonFile` model for external structure storage
- [ ] `ConversionConfig` model for configuration management
- [ ] `TwoDocumentPair` model for parallel document handling

#### 1.3 HTML Parser Implementation
- [ ] HTML element classification system following docs/510-512 specs
- [ ] Format Style attribute serialization with escaping rules
- [ ] Skeleton generation with placeholder system (`###u1###`)
- [ ] Inline element handling (`<mrk>`, `<ph>` generation)
- [ ] Complex structure preservation (tables, forms, media)

### Phase 2: XLIFF 2.1 Engine

#### 2.1 XLIFF Generation
- [ ] XLIFF 2.1 Core document structure generation
- [ ] Format Style module implementation (`fs:fs`, `fs:subFs`)
- [ ] External skeleton file management
- [ ] `originalData` handling for placeholders
- [ ] Namespace management and validation

#### 2.2 Content Extraction Rules
- [ ] Block-level element handling (paragraphs, headings, lists)
- [ ] Inline element preservation with `<mrk>` wrapping
- [ ] Void element handling with `<ph>` placeholders
- [ ] Table and form preservation with `xml:space="preserve"`
- [ ] Intelligent segmentation (respect `<s>`, split `<p>` by sentences)

#### 2.3 Round-trip Reconstruction
- [ ] Skeleton merging with translated content
- [ ] Format Style attribute reconstruction to HTML
- [ ] Placeholder resolution from `originalData`
- [ ] Structure validation and integrity checks

### Phase 3: Markdown Integration

#### 3.1 Markdown Parser Setup
- [ ] Configure markdown-it-py with selected plugins
- [ ] Front-matter handling (YAML/TOML preservation)
- [ ] Extension support (tables, footnotes, task lists, strikethrough)
- [ ] HTML passthrough for mixed content

#### 3.2 Markdown → HTML → XLIFF Pipeline
- [ ] Deterministic HTML rendering from Markdown
- [ ] Metadata preservation for round-trip reconstruction
- [ ] Reference link definition handling
- [ ] Code fence and inline code preservation

#### 3.3 XLIFF → HTML → Markdown Pipeline
- [ ] HTML reconstruction from XLIFF with skeleton
- [ ] Markdown syntax restoration using preserved metadata
- [ ] Link reference recreation
- [ ] Front-matter restoration

### Phase 4: Conversion Modes

#### 4.1 One-Document Mode
- [ ] Source-only storage (`<source>` elements only)
- [ ] Target-only storage (`<target>` elements only)
- [ ] Both storage (`<source>` and `<target>` elements)
- [ ] Configuration-driven mode selection

#### 4.2 Two-Document Mode
- [ ] Parallel document loading and parsing
- [ ] Structural alignment algorithm (headings, lists, paragraphs)
- [ ] Sentence-level alignment within matched structures
- [ ] Divergence detection and fallback handling
- [ ] Alignment quality reporting

### Phase 5: CLI Interface

#### 5.1 Core Commands
- [ ] `md2xliff` - Markdown to XLIFF conversion
- [ ] `html2xliff` - HTML to XLIFF conversion
- [ ] `xliff2md` - XLIFF to Markdown conversion
- [ ] `xliff2html` - XLIFF to HTML conversion
- [ ] `batch-convert` - Bulk processing with parallel execution

#### 5.2 Configuration System
- [ ] YAML configuration file support
- [ ] Environment variable overrides
- [ ] CLI argument precedence handling
- [ ] Configuration validation and defaults

#### 5.3 User Experience
- [ ] Rich progress indicators for long operations
- [ ] Detailed error reporting with suggestions
- [ ] Verbose mode with debug logging
- [ ] Dry-run mode for validation

### Phase 6: Quality Assurance & Testing

#### 6.1 Test Suite Development
- [ ] Unit tests for all core functions (>80% coverage)
- [ ] Integration tests for full conversion pipelines
- [ ] Round-trip fidelity tests (Markdown → XLIFF → Markdown)
- [ ] Edge case handling (malformed input, large files)
- [ ] Performance benchmarks (10k-line documents <10s)

#### 6.2 Validation Framework
- [ ] XLIFF 2.1 schema validation against official XSD
- [ ] Format Style module compliance checking
- [ ] HTML5 fragment validation for generated snippets
- [ ] Markdown CommonMark compliance verification

#### 6.3 Sample Data & Fixtures
- [ ] CommonMark test suite integration
- [ ] Real-world document samples (technical docs, blogs, wikis)
- [ ] Complex HTML structures (tables, forms, media)
- [ ] Multilingual content examples

### Phase 7: Documentation & Distribution

#### 7.1 Documentation
- [ ] API documentation with docstring generation
- [ ] CLI usage guide with examples
- [ ] Configuration reference
- [ ] Integration patterns and best practices
- [ ] Troubleshooting guide

#### 7.2 Package Distribution
- [ ] PyPI package publication
- [ ] GitHub releases with changelog
- [ ] Docker container for isolated execution
- [ ] Homebrew formula for macOS

## Technical Specifications

### File Structure
```
vexy-markliff/
├── src/vexy_markliff/
│   ├── __init__.py
│   ├── cli.py              # Fire CLI interface
│   ├── config.py           # Configuration management
│   ├── core/
│   │   ├── converter.py    # Main conversion orchestrator
│   │   ├── parser.py       # HTML/Markdown parsing
│   │   ├── xliff.py        # XLIFF 2.1 generation/parsing
│   │   └── skeleton.py     # Skeleton file management
│   ├── models/
│   │   ├── xliff.py        # Pydantic XLIFF models
│   │   ├── config.py       # Configuration models
│   │   └── alignment.py    # Two-document alignment models
│   └── utils/
│       ├── html_rules.py   # HTML element handling rules
│       ├── markdown.py     # Markdown-specific utilities
│       └── validation.py   # XLIFF/HTML validation
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── fixtures/
│   └── performance/
├── docs/                   # Specification documents (already exists)
├── examples/              # Sample conversions
├── pyproject.toml
├── README.md
└── CHANGELOG.md
```

### Configuration Schema
```yaml
# vexy-markliff.yaml
source_language: en
target_language: es
mode: one-doc  # one-doc | two-doc
storage: source  # source | target | both
extensions:
  - tables
  - footnotes
  - task_lists
  - strikethrough
split_sentences: true
skeleton_dir: ./skeletons
preserve_whitespace: true
output_format: xliff  # xliff | html | markdown
validation:
  xliff_schema: true
  html_fragments: true
```

### Performance Targets
- **Conversion Speed**: 10,000-line Markdown document in <10 seconds
- **Memory Usage**: <100MB for typical documents (<1MB source)
- **Round-trip Fidelity**: 100% for supported Markdown/HTML constructs
- **Test Coverage**: Minimum 80% line coverage
- **Startup Time**: CLI commands start in <500ms

## Risk Assessment & Mitigation

### Technical Risks
1. **XLIFF 2.1 Complexity**: Format Style module edge cases
   - *Mitigation*: Comprehensive test suite against official spec
2. **Round-trip Fidelity**: Markdown syntax variations
   - *Mitigation*: Metadata preservation strategy, extensive fixtures
3. **Performance**: Large document processing
   - *Mitigation*: Streaming processing, memory profiling, benchmarks

### Ecosystem Risks
1. **Dependency Stability**: markdown-it-py, lxml updates
   - *Mitigation*: Pin versions, compatibility testing
2. **XLIFF Tool Compatibility**: CAT tool variations
   - *Mitigation*: Test against major tools (SDL Trados, MemoQ, Phrase)

### User Experience Risks
1. **Configuration Complexity**: Too many options
   - *Mitigation*: Sensible defaults, progressive disclosure
2. **Error Messages**: Cryptic failures
   - *Mitigation*: User-friendly error handling, suggestions

## Success Criteria

### Functional Requirements
- [x] Bidirectional Markdown ↔ XLIFF 2.1 conversion
- [x] Bidirectional HTML ↔ XLIFF 2.1 conversion
- [x] One-document and two-document modes
- [x] Format Style module compliance
- [x] External skeleton file support
- [x] Round-trip fidelity preservation

### Quality Requirements
- [ ] 100% round-trip fidelity for supported constructs
- [ ] XLIFF 2.1 schema validation compliance
- [ ] CommonMark specification compliance
- [ ] >80% test coverage
- [ ] Performance targets met

### Usability Requirements
- [ ] Simple CLI interface for common tasks
- [ ] Clear error messages and recovery suggestions
- [ ] Comprehensive documentation
- [ ] Integration examples for common workflows

## Timeline Estimate

**Total Duration**: 8-12 weeks (assuming 20-30 hours/week)

- **Phase 1-2** (Foundation + XLIFF): 3-4 weeks
- **Phase 3** (Markdown Integration): 2 weeks
- **Phase 4** (Conversion Modes): 1-2 weeks
- **Phase 5** (CLI Interface): 1 week
- **Phase 6** (Testing & QA): 2-3 weeks
- **Phase 7** (Documentation): 1 week

## Post-Launch Roadmap

### Version 1.1 Enhancements
- [ ] Advanced segmentation rules (linguistic boundaries)
- [ ] Translation Memory integration hooks
- [ ] Batch processing optimization
- [ ] Plugin system for custom HTML elements

### Version 1.2 Extensions
- [ ] reStructuredText support
- [ ] AsciiDoc support
- [ ] Translation validation rules
- [ ] Quality assurance reporting

### Enterprise Features
- [ ] REST API for service integration
- [ ] Database backend for large-scale processing
- [ ] Multi-format pipeline orchestration
- [ ] Translation workflow automation

This plan provides a comprehensive roadmap for developing Vexy Markliff while maintaining focus on the core goal of reliable, high-fidelity Markdown/HTML ↔ XLIFF 2.1 conversion.
