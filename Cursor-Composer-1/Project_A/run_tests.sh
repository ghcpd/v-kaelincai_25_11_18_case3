#!/bin/bash
# Automated test runner for Project A

set -e

echo "=========================================="
echo "Running UI/UX Image Optimization Tests"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
else
    echo -e "${YELLOW}Warning: Virtual environment not found. Running setup...${NC}"
    bash setup.sh
    source venv/bin/activate 2>/dev/null || source venv/Scripts/activate 2>/dev/null
fi

# Create results directory
mkdir -p output/results

# Run unit tests
echo ""
echo "=========================================="
echo "Running Unit Tests"
echo "=========================================="
python -m pytest tests/test_pipeline.py -v --tb=short || {
    echo -e "${RED}Unit tests failed!${NC}"
    exit 1
}

# Run pipeline with test images
echo ""
echo "=========================================="
echo "Running Pipeline Integration Test"
echo "=========================================="
python main.py --num-images 5 --output-dir output/test_run || {
    echo -e "${RED}Pipeline test failed!${NC}"
    exit 1
}

# Verify output structure
echo ""
echo "=========================================="
echo "Verifying Output Structure"
echo "=========================================="

check_dir() {
    if [ -d "$1" ]; then
        file_count=$(find "$1" -type f | wc -l)
        echo -e "${GREEN}✓${NC} $1 exists ($file_count files)"
        return 0
    else
        echo -e "${RED}✗${NC} $1 missing"
        return 1
    fi
}

errors=0
check_dir "output/test_run/images_original" || errors=$((errors+1))
check_dir "output/test_run/images_optimized" || errors=$((errors+1))
check_dir "output/test_run/images_comparison" || errors=$((errors+1))
check_dir "output/test_run/results" || errors=$((errors+1))

# Check metadata file
if [ -f "output/test_run/results/metadata.json" ]; then
    echo -e "${GREEN}✓${NC} metadata.json exists"
    
    # Count processed images
    processed=$(python -c "import json; data=json.load(open('output/test_run/results/metadata.json')); print(data['summary']['processed'])" 2>/dev/null || echo "0")
    total=$(python -c "import json; data=json.load(open('output/test_run/results/metadata.json')); print(data['summary']['total_images'])" 2>/dev/null || echo "0")
    
    echo "  Processed: $processed/$total images"
else
    echo -e "${RED}✗${NC} metadata.json missing"
    errors=$((errors+1))
fi

# Generate test summary
echo ""
echo "=========================================="
echo "Test Summary"
echo "=========================================="

if [ $errors -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    echo ""
    echo "Output files are in: output/test_run/"
    echo "Results metadata: output/test_run/results/metadata.json"
    exit 0
else
    echo -e "${RED}Tests completed with $errors error(s)${NC}"
    exit 1
fi

