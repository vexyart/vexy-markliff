---
this_file: DEPENDENCIES.md
---

# Dependencies - Minimal Set

## Core Dependencies (6 packages only)

### 1. **fire** (>=0.7.1)
- **Purpose**: CLI command interface
- **Why chosen**: Simple, clean CLI creation from Python functions
- **Essential for**: Command-line interface

### 2. **lxml** (>=6.0.2)
- **Purpose**: XML/HTML processing
- **Why chosen**: Fast, robust XML/HTML parsing with full XPath support
- **Essential for**: HTML parsing and XLIFF XML generation

### 3. **markdown-it-py** (>=3.0.0)
- **Purpose**: Markdown parsing
- **Why chosen**: Fast, CommonMark compliant, Python-native
- **Essential for**: Converting Markdown to HTML/tokens

### 4. **pydantic** (>=2.11.9)
- **Purpose**: Data validation and models
- **Why chosen**: Type safety, automatic validation
- **Essential for**: XLIFF models and configuration

### 5. **pyyaml** (>=6.0.2)
- **Purpose**: YAML configuration support
- **Why chosen**: Standard YAML parsing
- **Potentially removable**: Could make config optional

### 6. **rich** (>=14.1.0)
- **Purpose**: Enhanced CLI output
- **Why chosen**: Better terminal formatting
- **Potentially removable**: Could use basic print statements

## Development Dependencies (Minimal)

### Testing
- **pytest** (>=8.3.4): Testing framework
- **pytest-cov** (>=6.0.0): Coverage reporting
- **coverage[toml]** (>=7.6.12): Coverage measurement

### Code Quality
- **ruff** (>=0.9.7): Fast linting and formatting
- **mypy** (>=1.15.0): Type checking

## Optimization Opportunities

### Phase 2 Reduction Candidates:
1. **pyyaml**: Make configuration optional (default values only)
2. **rich**: Replace with basic print statements for CLI

### Target State:
- Could potentially reduce to 4 core dependencies (fire, lxml, markdown-it-py, pydantic)
- Would achieve ultimate minimalism while maintaining core functionality
