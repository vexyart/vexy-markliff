#!/usr/bin/env python3
"""
Development environment setup script for vexy-markliff.

This script automatically configures the development environment with all necessary
tools, dependencies, and pre-commit hooks.
"""

import os
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, check: bool = True, cwd: Path | None = None) -> subprocess.CompletedProcess:
    """Run a command and return the result."""
    result = subprocess.run(cmd, shell=True, check=check, capture_output=True, text=True, cwd=cwd)
    if result.stdout:
        pass
    if result.stderr and result.returncode != 0:
        pass
    return result


def check_command_exists(cmd: str) -> bool:
    """Check if a command exists in PATH."""
    try:
        subprocess.run(cmd, shell=True, capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def main():
    """Main setup function."""

    # Get project root
    project_root = Path(__file__).parent.parent
    os.chdir(project_root)

    # Step 1: Check prerequisites

    prerequisites = {
        "python3 --version": "Python 3.8+",
        "git --version": "Git",
        "uv --version": "uv (Python package manager)",
    }

    missing_prereqs = []
    for cmd, name in prerequisites.items():
        if not check_command_exists(cmd):
            missing_prereqs.append(name)
        else:
            pass

    if missing_prereqs:
        if "uv" in missing_prereqs:
            pass
        sys.exit(1)

    # Step 2: Set up Python environment

    # Initialize uv project if needed
    if not (project_root / "uv.lock").exists():
        run_command("uv init --no-readme")

    # Install dependencies
    run_command("uv sync")

    # Install development dependencies
    dev_deps = [
        "pytest>=7.0.0",
        "pytest-cov>=4.0.0",
        "pytest-mock>=3.10.0",
        "mypy>=1.5.0",
        "ruff>=0.1.0",
        "pre-commit>=3.0.0",
        "bandit>=1.7.0",
        "black>=23.0.0",
        "isort>=5.12.0",
    ]

    for dep in dev_deps:
        run_command(f"uv add --dev {dep}")

    # Step 3: Set up pre-commit hooks

    # Create pre-commit config if it doesn't exist
    precommit_config = project_root / ".pre-commit-config.yaml"
    if not precommit_config.exists():
        precommit_content = """
# See https://pre-commit.com for more information
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files
      - id: check-merge-conflict
      - id: debug-statements

  - repo: https://github.com/psf/black
    rev: 23.7.0
    hooks:
      - id: black
        language_version: python3

  - repo: https://github.com/pycqa/isort
    rev: 5.12.0
    hooks:
      - id: isort

  - repo: https://github.com/charliermarsh/ruff-pre-commit
    rev: v0.0.280
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.5.1
    hooks:
      - id: mypy
        additional_dependencies: [types-PyYAML]

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: [--skip, B101]
""".strip()
        precommit_config.write_text(precommit_content)

    # Install pre-commit hooks
    run_command("uv run pre-commit install")

    # Step 4: Set up git hooks

    # Create pre-push hook
    hooks_dir = project_root / ".git" / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    prepush_hook = hooks_dir / "pre-push"
    prepush_content = """#!/bin/bash
# Pre-push hook to run tests and checks before pushing

echo "🔍 Running pre-push checks..."

# Run tests
echo "🧪 Running tests..."
if ! uv run pytest --tb=short; then
    echo "❌ Tests failed. Push aborted."
    exit 1
fi

# Run type checking
echo "🔍 Running type checking..."
if ! uv run mypy src/vexy_markliff --ignore-missing-imports; then
    echo "❌ Type checking failed. Push aborted."
    exit 1
fi

# Run linting
echo "🧹 Running linting..."
if ! uv run ruff check src/vexy_markliff tests; then
    echo "❌ Linting failed. Push aborted."
    exit 1
fi

echo "✅ All pre-push checks passed!"
"""

    prepush_hook.write_text(prepush_content)
    prepush_hook.chmod(0o755)  # Make executable

    # Step 5: Create development shortcuts

    # Create convenient scripts directory
    scripts_dir = project_root / "scripts"
    scripts_dir.mkdir(exist_ok=True)

    # Test runner script
    test_script = scripts_dir / "test.py"
    test_content = """#!/usr/bin/env python3
\"\"\"Quick test runner with options.\"\"\"
import subprocess
import sys

def main():
    args = sys.argv[1:]
    if not args:
        # Default: run all tests with coverage
        cmd = ["uv", "run", "pytest", "--cov=vexy_markliff", "--cov-report=term-missing"]
    elif args[0] == "fast":
        # Fast: run tests without coverage
        cmd = ["uv", "run", "pytest", "--tb=short"]
    elif args[0] == "watch":
        # Watch: run tests on file changes
        cmd = ["uv", "run", "pytest-watch", "--clear"]
    else:
        # Pass through arguments
        cmd = ["uv", "run", "pytest"] + args

    subprocess.run(cmd)

if __name__ == "__main__":
    main()
"""
    test_script.write_text(test_content)
    test_script.chmod(0o755)

    # Quality check script
    quality_script = scripts_dir / "quality.py"
    quality_content = """#!/usr/bin/env python3
\"\"\"Run all quality checks.\"\"\"
import subprocess
import sys

def run_check(name: str, cmd: list[str]) -> bool:
    print(f"🔍 {name}...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"   ✅ {name} passed")
        return True
    else:
        print(f"   ❌ {name} failed:")
        print(f"      {result.stdout}")
        print(f"      {result.stderr}")
        return False

def main():
    checks = [
        ("Type checking", ["uv", "run", "mypy", "src/vexy_markliff", "--ignore-missing-imports"]),
        ("Linting", ["uv", "run", "ruff", "check", "src/vexy_markliff", "tests"]),
        ("Security scan", ["uv", "run", "bandit", "-r", "src/vexy_markliff"]),
        ("Tests", ["uv", "run", "pytest", "--tb=short"]),
    ]

    failed = []
    for name, cmd in checks:
        if not run_check(name, cmd):
            failed.append(name)

    if failed:
        print(f"\\n❌ Failed checks: {', '.join(failed)}")
        sys.exit(1)
    else:
        print(f"\\n✅ All quality checks passed!")

if __name__ == "__main__":
    main()
"""
    quality_script.write_text(quality_content)
    quality_script.chmod(0o755)

    # Step 6: Verify installation

    verification_checks = [
        (
            "Import package",
            ["uv", "run", "python", "-c", "import vexy_markliff; print(f'✅ Version: {vexy_markliff.__version__}')"],
        ),
        ("Run basic test", ["uv", "run", "python", "-m", "pytest", "tests/", "-k", "test_", "--tb=no", "-q"]),
    ]

    for name, cmd in verification_checks:
        result = run_command(" ".join(cmd), check=False)
        if result.returncode == 0:
            pass
        else:
            pass

    # Step 7: Setup summary


if __name__ == "__main__":
    main()
