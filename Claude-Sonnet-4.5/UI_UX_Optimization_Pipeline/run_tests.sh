#!/bin/bash
# Automated test execution script for UI/UX Image Optimization Pipeline

echo "=========================================="
echo "UI/UX Image Optimization Pipeline"
echo "Automated Test Execution"
echo "=========================================="
echo ""

# Ensure we're in the project directory
cd "$(dirname "$0")"

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Warning: Virtual environment not found. Run setup.sh first."
    echo "Continuing with system Python..."
fi

# Clean previous results
echo ""
echo "Cleaning previous results..."
rm -rf images_original/*.png
rm -rf images_optimized/*.png
rm -rf images_comparison/*.png
rm -rf results/*.json

# Step 1: Generate test images
echo ""
echo "=========================================="
echo "Step 1: Generating Test Images"
echo "=========================================="
python3 src/image_generator.py

# Check if generation succeeded
if [ $? -eq 0 ]; then
    echo "✓ Test images generated successfully"
else
    echo "✗ Failed to generate test images"
    exit 1
fi

# Step 2: Run optimization pipeline
echo ""
echo "=========================================="
echo "Step 2: Running Optimization Pipeline"
echo "=========================================="
python3 src/image_optimizer.py

# Check if optimization succeeded
if [ $? -eq 0 ]; then
    echo "✓ Optimization completed successfully"
else
    echo "✗ Failed to optimize images"
    exit 1
fi

# Step 3: Run automated tests
echo ""
echo "=========================================="
echo "Step 3: Running Automated Tests"
echo "=========================================="
python3 tests/test_pipeline.py

# Check if tests passed
if [ $? -eq 0 ]; then
    echo "✓ All tests passed"
    test_status="SUCCESS"
else
    echo "✗ Some tests failed"
    test_status="FAILED"
fi

# Step 4: Generate summary report
echo ""
echo "=========================================="
echo "Step 4: Generating Summary Report"
echo "=========================================="

# Count files
original_count=$(ls -1 images_original/*.png 2>/dev/null | wc -l)
optimized_count=$(ls -1 images_optimized/*.png 2>/dev/null | wc -l)
comparison_count=$(ls -1 images_comparison/*.png 2>/dev/null | wc -l)

# Create summary report
cat > results/summary_report.txt << EOF
========================================
UI/UX IMAGE OPTIMIZATION PIPELINE
EXECUTION SUMMARY REPORT
========================================
Date: $(date)
Status: $test_status

IMAGE STATISTICS
----------------
Original Images: $original_count
Optimized Images: $optimized_count
Comparison Images: $comparison_count

FILE LOCATIONS
--------------
Original Images: images_original/
Optimized Images: images_optimized/
Comparison Images: images_comparison/
Test Results: results/test_results.json
Optimization Results: results/optimization_results.json

NEXT STEPS
----------
1. Review comparison images in images_comparison/
2. Check detailed results in results/optimization_results.json
3. Review test results in results/test_results.json

========================================
EOF

cat results/summary_report.txt

echo ""
echo "=========================================="
echo "Execution Complete!"
echo "=========================================="
echo ""
echo "Results saved to: results/"
echo "Summary report: results/summary_report.txt"
echo ""

# Exit with appropriate code
if [ "$test_status" = "SUCCESS" ]; then
    exit 0
else
    exit 1
fi
