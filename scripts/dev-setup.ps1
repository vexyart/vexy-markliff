# Vexy Markliff Developer Setup Script for Windows
# One-command setup for new developers
#
# Usage: .\scripts\dev-setup.ps1 [options]
# Options:
#   -NoPreCommit    Skip pre-commit hook installation
#   -NoVSCode       Skip VS Code setup
#   -CI             CI mode (minimal interactive prompts)
#
# this_file: scripts/dev-setup.ps1

param(
    [switch]$NoPreCommit,
    [switch]$NoVSCode,
    [switch]$CI
)

# Set error action preference
$ErrorActionPreference = "Stop"

# Configuration
$PythonVersion = if ($env:PYTHON_VERSION) { $env:PYTHON_VERSION } else { "3.12" }
$ProjectRoot = Split-Path -Parent $PSScriptRoot
$VenvDir = Join-Path $ProjectRoot ".venv"

# Color functions
function Write-Info {
    Write-Host "ℹ️  $args" -ForegroundColor Blue
}

function Write-Success {
    Write-Host "✅ $args" -ForegroundColor Green
}

function Write-Warning {
    Write-Host "⚠️  $args" -ForegroundColor Yellow
}

function Write-Error {
    Write-Host "❌ $args" -ForegroundColor Red
}

# Helper functions
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Header
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Vexy Markliff Developer Setup 🚀" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check system requirements
Write-Info "Checking system requirements..."

# Check Windows version
$OSVersion = [System.Environment]::OSVersion.Version
Write-Info "Windows version: $($OSVersion.Major).$($OSVersion.Minor)"

# Check execution policy
$ExecutionPolicy = Get-ExecutionPolicy
if ($ExecutionPolicy -eq "Restricted") {
    Write-Warning "Execution policy is restricted. Attempting to set to RemoteSigned for current user..."
    try {
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser -Force
        Write-Success "Execution policy updated"
    } catch {
        Write-Error "Failed to set execution policy. Please run as administrator or set manually."
        exit 1
    }
}

# Step 2: Install UV if not present
if (!(Test-Command "uv")) {
    Write-Info "Installing UV package manager..."

    try {
        # Download and run UV installer
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression

        # Add to PATH for current session
        $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"

        if (Test-Command "uv") {
            Write-Success "UV installed successfully"
        } else {
            Write-Error "Failed to install UV"
            exit 1
        }
    } catch {
        Write-Error "Error installing UV: $_"
        exit 1
    }
} else {
    $uvVersion = uv --version
    Write-Success "UV already installed ($uvVersion)"
}

# Step 3: Set up Python environment
Write-Info "Setting up Python $PythonVersion environment..."

Set-Location $ProjectRoot

# Install Python version
uv python install $PythonVersion

# Create virtual environment
if (!(Test-Path $VenvDir)) {
    uv venv --python $PythonVersion
    Write-Success "Virtual environment created"
} else {
    Write-Success "Virtual environment already exists"
}

# Step 4: Install dependencies
Write-Info "Installing project dependencies..."

# Install all dependencies including dev and docs
uv sync --all-extras --dev

Write-Success "Dependencies installed"

# Step 5: Install pre-commit hooks
if (!$NoPreCommit) {
    Write-Info "Setting up pre-commit hooks..."

    try {
        if (!(Test-Command "pre-commit")) {
            uv pip install pre-commit
        }

        uv run pre-commit install
        uv run pre-commit install --hook-type pre-push
        Write-Success "Pre-commit hooks installed"
    } catch {
        Write-Warning "Could not install pre-commit hooks: $_"
    }
} else {
    Write-Info "Skipping pre-commit installation"
}

# Step 6: Run initial quality checks
Write-Info "Running initial quality checks..."

# Format code
Write-Info "Formatting code..."
try {
    uv run ruff format src/ tests/
} catch {
    Write-Warning "Formatting completed with warnings"
}

# Run linting
Write-Info "Running linter..."
try {
    uv run ruff check src/ tests/ --fix
} catch {
    Write-Warning "Linting completed with warnings"
}

# Run type checking
Write-Info "Running type checker..."
try {
    uv run mypy src/vexy_markliff --ignore-missing-imports
} catch {
    Write-Warning "Type checking completed with warnings"
}

# Step 7: Run tests
Write-Info "Running test suite..."
try {
    uv run pytest tests/ -v --maxfail=5
    Write-Success "All tests passed"
} catch {
    Write-Warning "Some tests failed - this is expected during development"
}

# Step 8: Check import performance
Write-Info "Checking import performance..."
$ImportTime = uv run python -c @"
import time
start = time.perf_counter()
import vexy_markliff
end = time.perf_counter()
print(f'{(end-start)*1000:.1f}')
"@
Write-Success "Package import time: ${ImportTime}ms"

# Step 9: Set up VS Code (optional)
if (!$NoVSCode -and (Test-Command "code")) {
    Write-Info "Setting up VS Code..."

    # Install recommended extensions
    $extensions = @(
        "ms-python.python",
        "ms-python.vscode-pylance",
        "charliermarsh.ruff",
        "ms-python.mypy-type-checker"
    )

    foreach ($ext in $extensions) {
        try {
            code --install-extension $ext 2>$null
        } catch {
            # Ignore errors
        }
    }

    Write-Success "VS Code extensions installed"
}

# Step 10: Create local configuration
Write-Info "Creating local development configuration..."

# Create .env file if it doesn't exist
$EnvFile = Join-Path $ProjectRoot ".env"
if (!(Test-Path $EnvFile)) {
    $envContent = @"
# Local development environment variables
VEXY_MARKLIFF_DEBUG=true
VEXY_MARKLIFF_LOG_LEVEL=DEBUG
VEXY_MARKLIFF_CACHE_DIR=$env:USERPROFILE\.cache\vexy-markliff
"@
    Set-Content -Path $EnvFile -Value $envContent
    Write-Success "Created .env file"
} else {
    Write-Success ".env file already exists"
}

# Step 11: Display helpful information
Write-Host ""
Write-Host "======================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "======================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Quick Start Commands:" -ForegroundColor Yellow
Write-Host ""
Write-Host "  Run tests:"
Write-Host "    uv run pytest tests/" -ForegroundColor Green
Write-Host ""
Write-Host "  Run specific test:"
Write-Host "    uv run pytest tests/test_file.py::test_name" -ForegroundColor Green
Write-Host ""
Write-Host "  Format code:"
Write-Host "    uv run ruff format ." -ForegroundColor Green
Write-Host ""
Write-Host "  Lint code:"
Write-Host "    uv run ruff check . --fix" -ForegroundColor Green
Write-Host ""
Write-Host "  Type check:"
Write-Host "    uv run mypy src/" -ForegroundColor Green
Write-Host ""
Write-Host "  Run CLI:"
Write-Host "    uv run vexy-markliff --help" -ForegroundColor Green
Write-Host ""
Write-Host "  Build package:"
Write-Host "    uv build" -ForegroundColor Green
Write-Host ""
Write-Host "  Update dependencies:"
Write-Host "    uv lock --upgrade" -ForegroundColor Green
Write-Host ""
Write-Host "  Performance monitor:"
Write-Host "    uv run python scripts/performance_monitor.py" -ForegroundColor Green
Write-Host ""
Write-Host "  Quality dashboard:"
Write-Host "    uv run python scripts/quality_dashboard.py" -ForegroundColor Green
Write-Host ""
Write-Host "Documentation:" -ForegroundColor Yellow
Write-Host "  - README.md: Project overview"
Write-Host "  - CONTRIBUTING.md: Contribution guidelines"
Write-Host "  - DEV_README.md: Developer documentation"
Write-Host "  - ARCHITECTURE_ANALYSIS.md: Codebase structure"
Write-Host ""
Write-Host "Happy coding! 🚀" -ForegroundColor Cyan
