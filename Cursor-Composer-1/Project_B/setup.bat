@echo off
REM Setup script for Project B - Advanced UI/UX Image Optimization Pipeline (Windows)

echo ==========================================
echo Setting up Project B Environment
echo ==========================================

REM Check Python version
echo Checking Python version...
python --version
if errorlevel 1 (
    echo Python not found! Please install Python 3.8 or higher.
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment!
    exit /b 1
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
if errorlevel 1 (
    echo Failed to install requirements!
    exit /b 1
)

REM Create output directories
echo Creating output directories...
if not exist "output\images_original" mkdir output\images_original
if not exist "output\images_optimized" mkdir output\images_optimized
if not exist "output\images_comparison" mkdir output\images_comparison
if not exist "output\results" mkdir output\results

echo ==========================================
echo Setup complete!
echo ==========================================
echo To activate the environment, run:
echo   venv\Scripts\activate
echo.
echo To run the pipeline:
echo   python main.py --num-images 5
echo.
echo To run tests:
echo   python -m pytest tests\ -v
echo   or
echo   run_tests.bat
echo ==========================================

