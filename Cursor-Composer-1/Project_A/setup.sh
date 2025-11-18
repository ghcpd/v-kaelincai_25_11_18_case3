#!/bin/bash
# Setup script for Project A - UI/UX Image Optimization Pipeline

set -e

echo "=========================================="
echo "Setting up Project A Environment"
echo "=========================================="

# Check Python version
echo "Checking Python version..."
python3 --version || python --version

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv venv || python -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || source venv/Scripts/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing requirements..."
pip install -r requirements.txt

# Create output directories
echo "Creating output directories..."
mkdir -p output/images_original
mkdir -p output/images_optimized
mkdir -p output/images_comparison
mkdir -p output/results

echo "=========================================="
echo "Setup complete!"
echo "=========================================="
echo "To activate the environment, run:"
echo "  source venv/bin/activate  (Linux/Mac)"
echo "  venv\\Scripts\\activate  (Windows)"
echo ""
echo "To run the pipeline:"
echo "  python main.py --num-images 5"
echo ""
echo "To run tests:"
echo "  python -m pytest tests/ -v"
echo "  or"
echo "  ./run_tests.sh"
echo "=========================================="

