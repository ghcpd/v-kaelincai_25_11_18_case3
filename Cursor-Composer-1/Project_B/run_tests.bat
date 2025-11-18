@echo off
REM Automated test runner for Project B (Windows)

echo ==========================================
echo Running Advanced UI/UX Image Optimization Tests
echo ==========================================

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found. Running setup...
    call setup.bat
    call venv\Scripts\activate.bat
)

REM Create results directory
if not exist "output\results" mkdir output\results

REM Run unit tests
echo.
echo ==========================================
echo Running Unit Tests
echo ==========================================
python -m pytest tests\test_advanced_pipeline.py -v --tb=short
if errorlevel 1 (
    echo Unit tests failed!
    exit /b 1
)

REM Run pipeline with test images
echo.
echo ==========================================
echo Running Pipeline Integration Test
echo ==========================================
python main.py --num-images 5 --output-dir output\test_run
if errorlevel 1 (
    echo Pipeline test failed!
    exit /b 1
)

REM Verify output structure
echo.
echo ==========================================
echo Verifying Output Structure
echo ==========================================

if exist "output\test_run\images_original" (
    echo [OK] images_original exists
) else (
    echo [FAIL] images_original missing
    exit /b 1
)

if exist "output\test_run\images_optimized" (
    echo [OK] images_optimized exists
) else (
    echo [FAIL] images_optimized missing
    exit /b 1
)

if exist "output\test_run\images_comparison" (
    echo [OK] images_comparison exists
) else (
    echo [FAIL] images_comparison missing
    exit /b 1
)

if exist "output\test_run\results" (
    echo [OK] results exists
) else (
    echo [FAIL] results missing
    exit /b 1
)

if exist "output\test_run\results\metadata.json" (
    echo [OK] metadata.json exists
) else (
    echo [FAIL] metadata.json missing
    exit /b 1
)

if exist "output\test_run\results\summary.txt" (
    echo [OK] summary.txt exists
) else (
    echo [WARN] summary.txt missing
)

echo.
echo ==========================================
echo Test Summary
echo ==========================================
echo All tests passed!
echo.
echo Output files are in: output\test_run\
echo Results metadata: output\test_run\results\metadata.json
echo Summary report: output\test_run\results\summary.txt

