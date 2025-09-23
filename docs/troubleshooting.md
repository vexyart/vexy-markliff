---
this_file: docs/troubleshooting.md
---

# Vexy Markliff Troubleshooting Guide

This guide covers common issues and their solutions when using Vexy Markliff for Markdown/HTML to XLIFF conversion.

## Quick Diagnostics

Run the debug command to check your environment:

```bash
vexy-markliff debug
```

This will verify dependencies, configuration, and common issues.

## Common Issues and Solutions

### 1. Import and Installation Issues

#### "ModuleNotFoundError: No module named 'vexy_markliff'"

**Cause**: Package not installed or wrong environment.

**Solutions**:
```bash
# Install with uv (recommended)
uv add vexy-markliff

# Or with pip
pip install vexy-markliff

# Verify installation
python -c "import vexy_markliff; print(vexy_markliff.__version__)"
```

#### "ImportError: cannot import name 'VexyMarkliff'"

**Cause**: Outdated package version or corrupted installation.

**Solutions**:
```bash
# Reinstall package
pip uninstall vexy-markliff
pip install vexy-markliff

# Or force reinstall
pip install --force-reinstall vexy-markliff
```

### 2. File Processing Issues

#### "FileNotFoundError: No such file or directory"

**Cause**: Input file doesn't exist or incorrect path.

**Solutions**:
```bash
# Check file exists
ls -la input.md

# Use absolute path
vexy-markliff md2xliff /full/path/to/input.md output.xlf

# Check current directory
pwd
```

#### "PermissionError: Permission denied"

**Cause**: Insufficient permissions to read input or write output.

**Solutions**:
```bash
# Check file permissions
ls -la input.md output_directory/

# Fix permissions
chmod 644 input.md
chmod 755 output_directory/

# Run with appropriate user permissions
sudo chown $USER:$USER input.md
```

#### "ValidationError: File size exceeds maximum"

**Cause**: Input file is too large for processing.

**Solutions**:
```bash
# Check file size
du -h large_file.md

# Split large files
split -l 1000 large_file.md part_

# Increase size limit in config
echo "max_file_size: 500.0" > config.yaml
vexy-markliff md2xliff --config config.yaml input.md output.xlf
```

### 3. Language Code Issues

#### "ValidationError: Invalid language code format"

**Cause**: Language code doesn't follow ISO standards.

**Solutions**:
```bash
# Use standard language codes
vexy-markliff md2xliff input.md output.xlf --source-lang en --target-lang es

# Valid formats:
# - Two-letter: en, es, fr, de
# - With region: en-US, es-ES, fr-CA
# - With script: zh-Hans, zh-Hant

# Check valid codes
vexy-markliff validate --help
```

#### "Language code case sensitivity issues"

**Cause**: Incorrect case for region codes.

**Solutions**:
```bash
# Correct case (language lowercase, region uppercase)
--source-lang en-US  # ✓ Correct
--source-lang en-us  # ✗ Wrong
--source-lang EN-US  # ✗ Wrong
```

### 4. Conversion Issues

#### "Empty XLIFF output generated"

**Cause**: No translatable content found in source.

**Solutions**:
```bash
# Check source content
cat input.md

# Common causes:
# - File contains only code blocks
# - File contains only images/links
# - File is empty or whitespace only

# Add translatable text
echo "# Sample Header\n\nSome translatable text." > input.md
```

#### "Markdown formatting lost in conversion"

**Cause**: Complex formatting not supported or configuration issue.

**Solutions**:
```yaml
# Create config.yaml with all extensions
markdown:
  extensions:
    - tables
    - footnotes
    - task_lists
    - strikethrough
  html_passthrough: true
```

```bash
# Use enhanced configuration
vexy-markliff md2xliff --config config.yaml input.md output.xlf
```

#### "HTML elements not preserved"

**Cause**: HTML passthrough disabled or security filtering.

**Solutions**:
```yaml
# Enable HTML passthrough in config
markdown:
  html_passthrough: true
  preserve_raw_html: true
```

### 5. Configuration Issues

#### "Configuration file not found"

**Cause**: Config file path incorrect or doesn't exist.

**Solutions**:
```bash
# Create default config
vexy-markliff config init

# Check config file location
ls -la vexy-markliff.yaml

# Specify config explicitly
vexy-markliff md2xliff --config /path/to/config.yaml input.md output.xlf
```

#### "Invalid configuration syntax"

**Cause**: YAML syntax error in configuration file.

**Solutions**:
```bash
# Validate configuration
vexy-markliff config validate

# Check YAML syntax
python -c "import yaml; yaml.safe_load(open('config.yaml'))"

# Common YAML issues:
# - Tabs instead of spaces
# - Incorrect indentation
# - Missing colons
```

### 6. Performance Issues

#### "Conversion takes too long"

**Cause**: Large files or inefficient processing.

**Solutions**:
```bash
# Process smaller chunks
split -l 500 large.md chunk_
for file in chunk_*; do
    vexy-markliff md2xliff "$file" "${file}.xlf"
done

# Use batch processing
vexy-markliff batch-convert *.md --output-dir xliff/

# Monitor performance
time vexy-markliff md2xliff input.md output.xlf
```

#### "High memory usage"

**Cause**: Large documents or memory leaks.

**Solutions**:
```bash
# Monitor memory usage
top -p $(pgrep -f vexy-markliff)

# Reduce memory usage
echo "max_file_size: 50.0" > config.yaml

# Process files individually instead of batch
```

### 7. CLI Usage Issues

#### "Command not found: vexy-markliff"

**Cause**: Package not in PATH or not installed globally.

**Solutions**:
```bash
# Use as module
python -m vexy_markliff md2xliff input.md output.xlf

# Add to PATH (if using uv)
export PATH="$HOME/.local/bin:$PATH"

# Check installation location
which vexy-markliff
pip show vexy-markliff
```

#### "Fire CLI errors or unexpected behavior"

**Cause**: Incorrect command syntax or parameter issues.

**Solutions**:
```bash
# Use proper Fire CLI syntax
vexy-markliff md2xliff input.md output.xlf --source-lang=en --target-lang=es

# Not: --source-lang en (missing =)

# Get help for specific commands
vexy-markliff md2xliff --help
vexy-markliff --help
```

### 8. Development and Testing Issues

#### "Tests failing after changes"

**Cause**: Code changes broke existing functionality.

**Solutions**:
```bash
# Run full test suite
uvx hatch test

# Run specific tests
python -m pytest tests/test_converter.py -v

# Check test coverage
python -m pytest --cov=src/vexy_markliff

# Debug failing tests
python -m pytest tests/test_failing.py -xvs
```

#### "Import performance issues"

**Cause**: Heavy module imports affecting startup time.

**Solutions**:
```bash
# Check import time
python -c "import time; start=time.time(); import vexy_markliff; print(f'Import: {(time.time()-start)*1000:.1f}ms')"

# Should be < 50ms for good performance
# If slower, check for circular imports or heavy dependencies
```

## Environment-Specific Issues

### Windows Issues

#### "Path separator issues"

```cmd
# Use forward slashes or escape backslashes
vexy-markliff md2xliff input.md output.xlf
vexy-markliff md2xliff input.md output\\output.xlf

# Or use raw strings in Python
path = r"C:\Users\Name\Documents\file.md"
```

### macOS Issues

#### "Permission denied on system directories"

```bash
# Don't install in system Python
# Use homebrew Python or virtual environments
brew install python
python3 -m venv venv
source venv/bin/activate
pip install vexy-markliff
```

### Linux Issues

#### "Library dependencies missing"

```bash
# Install required system libraries
sudo apt-get update
sudo apt-get install python3-dev libxml2-dev libxslt-dev

# Or on CentOS/RHEL
sudo yum install python3-devel libxml2-devel libxslt-devel
```

## Performance Optimization

### Best Practices for Large Files

1. **Split large documents**:
   ```bash
   # Split by lines
   split -l 1000 large.md chunk_

   # Split by size
   split -b 1M large.md chunk_
   ```

2. **Use batch processing**:
   ```bash
   vexy-markliff batch-convert *.md --output-dir results/
   ```

3. **Optimize configuration**:
   ```yaml
   performance:
     max_file_size: 100.0  # MB
     enable_caching: true
     parallel_processing: true
   ```

### Memory Management

1. **Monitor usage**:
   ```bash
   /usr/bin/time -v vexy-markliff md2xliff large.md output.xlf
   ```

2. **Limit memory**:
   ```bash
   ulimit -m 1048576  # Limit to 1GB
   ```

## Getting Help

### Debug Information

Always include this information when reporting issues:

```bash
# System information
vexy-markliff debug

# Version information
vexy-markliff version

# Configuration
vexy-markliff config show

# Test with minimal example
echo "# Test\n\nSample text." > test.md
vexy-markliff md2xliff test.md test.xlf --verbose
```

### Log Files

Enable verbose logging for debugging:

```bash
# Enable debug logging
vexy-markliff md2xliff input.md output.xlf --verbose --log-file debug.log

# Check log file
tail -f debug.log
```

### Common Error Patterns

| Error Message | Common Cause | Quick Fix |
|---------------|--------------|-----------|
| `FileNotFoundError` | Wrong file path | Check path with `ls` |
| `PermissionError` | File permissions | Use `chmod` or `sudo` |
| `ValidationError` | Invalid input | Check format with `file` |
| `ImportError` | Missing dependencies | Reinstall package |
| `UnicodeDecodeError` | File encoding | Specify encoding |
| `MemoryError` | File too large | Split file or increase memory |

## Advanced Troubleshooting

### Debug Mode

Run in debug mode for detailed output:

```python
import logging
logging.basicConfig(level=logging.DEBUG)

from vexy_markliff import VexyMarkliff
converter = VexyMarkliff()
# ... rest of code with debug output
```

### Custom Error Handling

```python
from vexy_markliff import VexyMarkliff
from vexy_markliff.exceptions import ValidationError, FileOperationError

try:
    converter = VexyMarkliff()
    result = converter.markdown_to_xliff(content, "en", "es")
except ValidationError as e:
    print(f"Validation failed: {e}")
    # Handle validation issues
except FileOperationError as e:
    print(f"File operation failed: {e}")
    # Handle file issues
except Exception as e:
    print(f"Unexpected error: {e}")
    # Handle unexpected issues
```

### Testing Your Setup

Create a test script to verify everything works:

```python
#!/usr/bin/env python3
"""Test Vexy Markliff installation and basic functionality."""

def test_installation():
    try:
        import vexy_markliff
        print(f"✓ Vexy Markliff {vexy_markliff.__version__} installed")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False

def test_basic_conversion():
    try:
        from vexy_markliff import VexyMarkliff

        converter = VexyMarkliff()
        test_md = "# Test\n\nThis is a test document."

        result = converter.markdown_to_xliff(test_md, "en", "es")

        if result and "<xliff" in result:
            print("✓ Basic conversion works")
            return True
        else:
            print("✗ Conversion failed - no XLIFF output")
            return False

    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Vexy Markliff setup...")

    if test_installation() and test_basic_conversion():
        print("\n🎉 Everything looks good!")
    else:
        print("\n❌ Issues found. Check troubleshooting guide.")
```

Save as `test_setup.py` and run:

```bash
python test_setup.py
```

This guide should help you resolve most common issues. For additional help, check the project documentation or file an issue on GitHub.
