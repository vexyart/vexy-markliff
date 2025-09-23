# Contributing to Vexy Markliff

Thank you for your interest in contributing to Vexy Markliff! This guide will help you get started.

## Quick Start for Contributors

### Prerequisites

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) for dependency management
- Git

### Development Setup

#### Automated Setup (Recommended)

The fastest way to get started is with our automated setup script:

```bash
git clone https://github.com/your-org/vexy-markliff.git
cd vexy-markliff
python scripts/setup-dev.py
```

This script will:
- ✅ Set up Python virtual environment with uv
- ✅ Install all development dependencies
- ✅ Configure pre-commit hooks
- ✅ Install pre-push git hooks
- ✅ Create development scripts

#### Manual Setup

If you prefer manual setup:

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-org/vexy-markliff.git
   cd vexy-markliff
   ```

2. **Set up development environment**
   ```bash
   # Install uv if you haven't already
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Create virtual environment and install dependencies
   uv venv --python 3.12
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv sync --dev
   ```

3. **Install pre-commit hooks**
   ```bash
   uv run pre-commit install
   ```

### Development Workflow

#### Using Make Commands (Recommended)

We provide convenient Make commands for all common tasks:

```bash
# Run tests
make test              # Full test suite with coverage
make test-fast         # Quick tests without coverage
make test-watch        # Watch mode (re-run on file changes)

# Code quality
make lint              # Check code style
make lint-fix          # Fix code style issues
make format            # Format code
make type-check        # Run type checking
make security          # Security scanning
make quality           # Run all quality checks

# Development shortcuts
make dev               # Quick check (lint + fast tests)
make ci                # Simulate full CI pipeline
```

#### Using Python Scripts

Alternative to Make commands:

```bash
# Test runners
python scripts/test.py           # Tests with coverage
python scripts/test.py fast      # Fast tests
python scripts/test.py watch     # Watch mode

# Quality checks
python scripts/quality.py        # All quality checks
```

#### Manual Commands

If you prefer running commands directly:

```bash
# Testing
uv run pytest                              # Basic tests
uv run pytest --cov=vexy_markliff         # With coverage
uv run pytest-watch                       # Watch mode

# Code quality
uv run ruff check src/vexy_markliff tests  # Linting
uv run ruff check --fix                    # Auto-fix issues
uv run mypy src/vexy_markliff              # Type checking
uv run bandit -r src/vexy_markliff         # Security scan
```

## Project Structure

```
vexy-markliff/
├── src/vexy_markliff/          # Main package
│   ├── core/                   # Core conversion logic
│   │   ├── converter.py        # Main VexyMarkliff class
│   │   ├── parser.py          # Markdown/HTML parsing
│   │   └── ...
│   ├── models/                 # Pydantic data models
│   ├── utils/                  # Utility functions
│   ├── config.py              # Configuration management
│   └── cli.py                 # Command-line interface
├── tests/                      # Test suite
├── docs/                       # Documentation
└── examples/                   # Usage examples
```

## Contributing Guidelines

### 1. Code Style

- Follow PEP 8 style guidelines
- Use type hints for all functions and methods
- Write descriptive docstrings with examples
- Keep functions under 20 lines when possible
- Maximum line length: 120 characters

### 2. Testing Requirements

- **All new code must have tests** (minimum 80% coverage)
- Write both unit tests and integration tests
- Include edge cases and error conditions
- Use descriptive test names: `test_function_when_condition_then_result`

### 3. Documentation

- Add docstrings with practical examples
- Update CHANGELOG.md for user-facing changes
- Include type information in docstrings
- Add examples for complex functionality

### 4. Git Workflow

```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes and commit
git add .
git commit -m "feat: add new feature description"

# Push and create pull request
git push origin feature/your-feature-name
```

### 5. Commit Message Format

Use conventional commits:

- `feat:` - New features
- `fix:` - Bug fixes
- `docs:` - Documentation changes
- `test:` - Test additions/modifications
- `refactor:` - Code refactoring
- `style:` - Code style changes

## Common Development Tasks

### Adding a New Validation Function

1. **Create the function** in `src/vexy_markliff/utils/validation.py`
2. **Add comprehensive tests** in `tests/test_validation_comprehensive.py`
3. **Update docstring** with examples
4. **Run tests** to ensure coverage

Example:
```python
def validate_custom_field(value: Any, field_name: str) -> str:
    """Validate custom field input.

    Examples:
        >>> validate_custom_field("valid_value", "field")
        'valid_value'

        >>> validate_custom_field(123, "field")  # doctest: +SKIP
        ValidationError: field must be a string
    """
    # Implementation here
```

### Adding a New Converter Method

1. **Add method** to `VexyMarkliff` class in `src/vexy_markliff/core/converter.py`
2. **Write comprehensive docstring** with examples
3. **Add validation** and error handling
4. **Create tests** in `tests/test_converter.py`
5. **Update CLI** if needed in `src/vexy_markliff/cli.py`

### Debugging Tips

- Use `--verbose` flag with CLI commands for detailed logging
- Enable debug logging: `VEXY_LOG_LEVEL=DEBUG`
- Use `pytest -xvs` for detailed test output
- Check `WORK.md` for recent development notes

## Getting Help

- Check existing [issues](https://github.com/your-org/vexy-markliff/issues)
- Read the [documentation](docs/)
- Review [examples](examples/) for usage patterns
- Ask questions in discussions

## Code Review Process

1. Ensure all tests pass and coverage is maintained
2. Verify code follows style guidelines
3. Check that documentation is updated
4. Confirm backwards compatibility
5. Review for security implications

Thank you for contributing to Vexy Markliff! 🚀
