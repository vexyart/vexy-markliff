#!/usr/bin/env bash
#
# Vexy Markliff Developer Setup Script
# One-command setup for new developers
#
# Usage: ./scripts/dev-setup.sh [options]
# Options:
#   --no-pre-commit    Skip pre-commit hook installation
#   --no-vscode        Skip VS Code setup
#   --ci               CI mode (minimal interactive prompts)
#
# this_file: scripts/dev-setup.sh

set -euo pipefail

# Color output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PYTHON_VERSION="${PYTHON_VERSION:-3.12}"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_DIR="${PROJECT_ROOT}/.venv"

# Parse arguments
INSTALL_PRE_COMMIT=true
INSTALL_VSCODE=true
CI_MODE=false

while [[ $# -gt 0 ]]; do
  case $1 in
    --no-pre-commit)
      INSTALL_PRE_COMMIT=false
      shift
      ;;
    --no-vscode)
      INSTALL_VSCODE=false
      shift
      ;;
    --ci)
      CI_MODE=true
      shift
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Functions
log_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

log_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

log_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

log_error() {
    echo -e "${RED}❌ $1${NC}"
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Header
echo ""
echo "======================================"
echo "  Vexy Markliff Developer Setup 🚀"
echo "======================================"
echo ""

# Step 1: Check system requirements
log_info "Checking system requirements..."

# Check OS
OS="$(uname -s)"
case "${OS}" in
    Linux*)     OS_TYPE=Linux;;
    Darwin*)    OS_TYPE=Mac;;
    CYGWIN*|MINGW*|MSYS*) OS_TYPE=Windows;;
    *)          OS_TYPE="UNKNOWN:${OS}"
esac

log_info "Detected OS: ${OS_TYPE}"

# Step 2: Install UV if not present
if ! command_exists uv; then
    log_info "Installing UV package manager..."

    if [[ "${OS_TYPE}" == "Windows" ]]; then
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.cargo/bin:$PATH"
    fi

    if command_exists uv; then
        log_success "UV installed successfully"
    else
        log_error "Failed to install UV"
        exit 1
    fi
else
    log_success "UV already installed ($(uv --version))"
fi

# Step 3: Set up Python environment
log_info "Setting up Python ${PYTHON_VERSION} environment..."

cd "${PROJECT_ROOT}"

# Install Python version
uv python install "${PYTHON_VERSION}"

# Create virtual environment
if [[ ! -d "${VENV_DIR}" ]]; then
    uv venv --python "${PYTHON_VERSION}"
    log_success "Virtual environment created"
else
    log_success "Virtual environment already exists"
fi

# Step 4: Install dependencies
log_info "Installing project dependencies..."

# Install all dependencies including dev and docs
uv sync --all-extras --dev

log_success "Dependencies installed"

# Step 5: Install pre-commit hooks
if [[ "${INSTALL_PRE_COMMIT}" == "true" ]]; then
    log_info "Setting up pre-commit hooks..."

    if command_exists pre-commit; then
        uv run pre-commit install
        uv run pre-commit install --hook-type pre-push
        log_success "Pre-commit hooks installed"
    else
        uv pip install pre-commit
        uv run pre-commit install
        uv run pre-commit install --hook-type pre-push
        log_success "Pre-commit installed and configured"
    fi
else
    log_info "Skipping pre-commit installation"
fi

# Step 6: Run initial quality checks
log_info "Running initial quality checks..."

# Format code
log_info "Formatting code..."
uv run ruff format src/ tests/ || true

# Run linting
log_info "Running linter..."
uv run ruff check src/ tests/ --fix || true

# Run type checking
log_info "Running type checker..."
uv run mypy src/vexy_markliff --ignore-missing-imports || true

# Step 7: Run tests
log_info "Running test suite..."
uv run pytest tests/ -v --maxfail=5 || log_warning "Some tests failed - this is expected during development"

# Step 8: Check import performance
log_info "Checking import performance..."
IMPORT_TIME=$(uv run python -c "
import time
start = time.perf_counter()
import vexy_markliff
end = time.perf_counter()
print(f'{(end-start)*1000:.1f}')
")
log_success "Package import time: ${IMPORT_TIME}ms"

# Step 9: Set up VS Code (optional)
if [[ "${INSTALL_VSCODE}" == "true" ]] && command_exists code; then
    log_info "Setting up VS Code..."

    # Install recommended extensions
    code --install-extension ms-python.python 2>/dev/null || true
    code --install-extension ms-python.vscode-pylance 2>/dev/null || true
    code --install-extension charliermarsh.ruff 2>/dev/null || true
    code --install-extension ms-python.mypy-type-checker 2>/dev/null || true

    log_success "VS Code extensions installed"
fi

# Step 10: Create local configuration
log_info "Creating local development configuration..."

# Create .env file if it doesn't exist
if [[ ! -f "${PROJECT_ROOT}/.env" ]]; then
    cat > "${PROJECT_ROOT}/.env" << EOF
# Local development environment variables
VEXY_MARKLIFF_DEBUG=true
VEXY_MARKLIFF_LOG_LEVEL=DEBUG
VEXY_MARKLIFF_CACHE_DIR=${HOME}/.cache/vexy-markliff
EOF
    log_success "Created .env file"
else
    log_success ".env file already exists"
fi

# Step 11: Display helpful information
echo ""
echo "======================================"
echo "  Setup Complete! 🎉"
echo "======================================"
echo ""
echo "Quick Start Commands:"
echo ""
echo "  Run tests:"
echo "    ${GREEN}uv run pytest tests/${NC}"
echo ""
echo "  Run specific test:"
echo "    ${GREEN}uv run pytest tests/test_file.py::test_name${NC}"
echo ""
echo "  Format code:"
echo "    ${GREEN}uv run ruff format .${NC}"
echo ""
echo "  Lint code:"
echo "    ${GREEN}uv run ruff check . --fix${NC}"
echo ""
echo "  Type check:"
echo "    ${GREEN}uv run mypy src/${NC}"
echo ""
echo "  Run CLI:"
echo "    ${GREEN}uv run vexy-markliff --help${NC}"
echo ""
echo "  Build package:"
echo "    ${GREEN}uv build${NC}"
echo ""
echo "  Update dependencies:"
echo "    ${GREEN}uv lock --upgrade${NC}"
echo ""
echo "  Performance monitor:"
echo "    ${GREEN}uv run python scripts/performance_monitor.py${NC}"
echo ""
echo "  Quality dashboard:"
echo "    ${GREEN}uv run python scripts/quality_dashboard.py${NC}"
echo ""
echo "Documentation:"
echo "  - README.md: Project overview"
echo "  - CONTRIBUTING.md: Contribution guidelines"
echo "  - DEV_README.md: Developer documentation"
echo "  - ARCHITECTURE_ANALYSIS.md: Codebase structure"
echo ""
echo "Happy coding! 🚀"
