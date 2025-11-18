# Automated test execution script for UI/UX Image Optimization Pipeline (PowerShell)

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "UI/UX Image Optimization Pipeline" -ForegroundColor Cyan
Write-Host "Automated Test Execution" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Ensure we're in the project directory
Set-Location $PSScriptRoot

# Activate virtual environment if it exists
if (Test-Path "venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    & .\venv\Scripts\Activate.ps1
} else {
    Write-Host "Warning: Virtual environment not found. Run setup.ps1 first." -ForegroundColor Red
    Write-Host "Continuing with system Python..." -ForegroundColor Yellow
}

# Clean previous results
Write-Host ""
Write-Host "Cleaning previous results..." -ForegroundColor Yellow
Remove-Item -Path "images_original\*.png" -ErrorAction SilentlyContinue
Remove-Item -Path "images_optimized\*.png" -ErrorAction SilentlyContinue
Remove-Item -Path "images_comparison\*.png" -ErrorAction SilentlyContinue
Remove-Item -Path "results\*.json" -ErrorAction SilentlyContinue

# Step 1: Generate test images
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 1: Generating Test Images" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
python src\image_generator.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Test images generated successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to generate test images" -ForegroundColor Red
    exit 1
}

# Step 2: Run optimization pipeline
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 2: Running Optimization Pipeline" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
python src\image_optimizer.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Optimization completed successfully" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to optimize images" -ForegroundColor Red
    exit 1
}

# Step 3: Run automated tests
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 3: Running Automated Tests" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
python tests\test_pipeline.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ All tests passed" -ForegroundColor Green
    $testStatus = "SUCCESS"
} else {
    Write-Host "✗ Some tests failed" -ForegroundColor Red
    $testStatus = "FAILED"
}

# Step 4: Generate summary report
Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Step 4: Generating Summary Report" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan

# Count files
$originalCount = (Get-ChildItem -Path "images_original\*.png" -ErrorAction SilentlyContinue).Count
$optimizedCount = (Get-ChildItem -Path "images_optimized\*.png" -ErrorAction SilentlyContinue).Count
$comparisonCount = (Get-ChildItem -Path "images_comparison\*.png" -ErrorAction SilentlyContinue).Count

# Create summary report
$reportContent = @"
==========================================
UI/UX IMAGE OPTIMIZATION PIPELINE
EXECUTION SUMMARY REPORT
==========================================
Date: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Status: $testStatus

IMAGE STATISTICS
----------------
Original Images: $originalCount
Optimized Images: $optimizedCount
Comparison Images: $comparisonCount

FILE LOCATIONS
--------------
Original Images: images_original\
Optimized Images: images_optimized\
Comparison Images: images_comparison\
Test Results: results\test_results.json
Optimization Results: results\optimization_results.json

NEXT STEPS
----------
1. Review comparison images in images_comparison\
2. Check detailed results in results\optimization_results.json
3. Review test results in results\test_results.json

==========================================
"@

$reportContent | Out-File -FilePath "results\summary_report.txt" -Encoding UTF8
Write-Host $reportContent

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Execution Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Results saved to: results\" -ForegroundColor Yellow
Write-Host "Summary report: results\summary_report.txt" -ForegroundColor Yellow
Write-Host ""

# Exit with appropriate code
if ($testStatus -eq "SUCCESS") {
    exit 0
} else {
    exit 1
}
