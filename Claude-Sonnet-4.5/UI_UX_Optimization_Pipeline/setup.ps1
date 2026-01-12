# Setup script for UI/UX Image Optimization Pipeline (Windows PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "UI/UX Image Optimization Pipeline Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python version
Write-Host "Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
Write-Host "Python version: $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Upgrade pip
Write-Host ""
Write-Host "Upgrading pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip

# Install dependencies
Write-Host ""
Write-Host "Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

# Create necessary directories
Write-Host ""
Write-Host "Creating project directories..." -ForegroundColor Yellow
New-Item -ItemType Directory -Force -Path images_original | Out-Null
New-Item -ItemType Directory -Force -Path images_optimized | Out-Null
New-Item -ItemType Directory -Force -Path images_comparison | Out-Null
New-Item -ItemType Directory -Force -Path results | Out-Null

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup completed successfully!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "To activate the environment, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
Write-Host ""
Write-Host "To run the pipeline, execute:" -ForegroundColor Yellow
Write-Host "  .\run_tests.ps1" -ForegroundColor White
Write-Host ""
