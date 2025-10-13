<#
.SYNOPSIS
  PowerShell equivalent of Makefile tasks for Windows users.

.DESCRIPTION
  Usage examples:
    ./make.ps1 help
    ./make.ps1 setup
    ./make.ps1 clean
    ./make.ps1 docs
    ./make.ps1 tests
#>

param(
    [Parameter(Position=0)]
    [ValidateSet("help", "setup", "clean", "docs", "tests")]
    [string]$Target = "help"
)

# --- Configuration ---
$VENV = ".venv"
$PYTHON = "python"
$SPHINXBUILD = "sphinx-build"
$SOURCEDIR = "docs"
$BUILDDIR = "docs/_build"
$HTMLDIR = Join-Path $BUILDDIR "html"
$INDEXFILE = Join-Path $HTMLDIR "index.html"

# --- Helper Functions ---

function Create-Venv {
    if (-Not (Test-Path $VENV)) {
        Write-Host "Creating virtual environment in $VENV..."
        & $PYTHON -m venv $VENV
    } else {
        Write-Host "Virtual environment already exists."
    }

    $pip = Join-Path $VENV "Scripts\pip.exe"
    Write-Host "Upgrading pip..."
    & $pip install --upgrade pip

    if (Test-Path "requirements.txt") {
        Write-Host "Installing dependencies..."
        & $pip install -r requirements.txt
    } else {
        Write-Warning "requirements.txt not found. Skipping dependency installation."
    }
}

function Build-Docs {
    $sphinx = Join-Path $VENV "Scripts\sphinx-build.exe"
    if (-Not (Test-Path $sphinx)) {
        Write-Error "Sphinx not found in virtual environment. Please run './make.ps1 setup' first."
        exit 1
    }

    Write-Host "Building documentation..."
    & $sphinx -b html $SOURCEDIR $HTMLDIR
}

function Open-Docs {
    if (Test-Path $INDEXFILE) {
        Write-Host "Opening documentation..."
        Start-Process $INDEXFILE
    } else {
        Write-Warning "Documentation not found. Run './make.ps1 setup' first."
    }
}

function Clean {
    Write-Host "Removing virtual environment and build directory..."
    if (Test-Path $VENV) { Remove-Item -Recurse -Force $VENV }
    if (Test-Path $BUILDDIR) { Remove-Item -Recurse -Force $BUILDDIR }
    Write-Host "Cleanup complete."
}

function Run-Tests {
    Write-Host "Running Python tests..." -ForegroundColor Cyan

    $pythonExe = Join-Path $VENV "Scripts\python.exe"

    if (-Not (Test-Path $pythonExe)) {
        Write-Error "Python executable not found in virtual environment. Please run './make.ps1 setup' first."
        exit 1
    }

    & $pythonExe -m pytest -v
}

function Show-Help {
    Write-Host "Available commands:" -ForegroundColor Cyan
    Write-Host "  ./make.ps1 setup   - Create venv, install deps, build docs"
    Write-Host "  ./make.ps1 docs    - Open docs"
    Write-Host "  ./make.ps1 tests   - Run Python tests"
    Write-Host "  ./make.ps1 clean   - Remove venv and docs"
    Write-Host "  ./make.ps1 help    - Show this help message"
}

# --- Main dispatcher ---
switch ($Target) {
    "help"  { Show-Help }
    "setup" {
        Create-Venv
        Build-Docs
        Write-Host "`nSetup complete!" -ForegroundColor Green
        Write-Host "######################################"
        Write-Host "# To activate your virtual env:      #"
        Write-Host "#   .\$VENV\Scripts\Activate.ps1     #"
        Write-Host "######################################"
    }
    "clean" { Clean }
    "docs"  { Open-Docs }
    "tests" { Run-Tests }
}
