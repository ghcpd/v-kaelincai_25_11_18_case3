# Quick Start Guide

## Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)

## Installation & Testing (One Command)

### Linux/Mac

**Project A:**
```bash
cd Project_A
chmod +x setup.sh run_tests.sh
./setup.sh && ./run_tests.sh
```

**Project B:**
```bash
cd Project_B
chmod +x setup.sh run_tests.sh
./setup.sh && ./run_tests.sh
```

### Windows

**Project A:**
```cmd
cd Project_A
setup.bat
run_tests.bat
```

**Project B:**
```cmd
cd Project_B
setup.bat
run_tests.bat
```

## Manual Setup

### Step 1: Create Virtual Environment

```bash
python -m venv venv
```

### Step 2: Activate Virtual Environment

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Windows:**
```cmd
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run Pipeline

```bash
python main.py --num-images 5
```

### Step 5: Run Tests

```bash
python -m pytest tests/ -v
```

## Expected Output

After running the pipeline, you should see:

```
output/
├── images_original/      # 5 generated images
├── images_optimized/     # 5 enhanced images
├── images_comparison/    # 5 comparison images
└── results/
    ├── metadata.json      # Processing metadata
    └── pipeline.log       # Execution log
```

## Verification Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed successfully
- [ ] Pipeline runs without errors
- [ ] All three output folders created
- [ ] Images generated in `images_original/`
- [ ] Enhanced images in `images_optimized/`
- [ ] Comparison images in `images_comparison/`
- [ ] `metadata.json` file created
- [ ] All tests pass

## Troubleshooting

### Import Errors
```bash
pip install --upgrade -r requirements.txt
```

### Permission Errors (Linux/Mac)
```bash
chmod +x setup.sh run_tests.sh
```

### OpenCV Issues
```bash
pip install opencv-python-headless
```

### Python Not Found
- Ensure Python 3.8+ is installed
- Check PATH environment variable
- Use `python3` instead of `python` if needed

## Next Steps

1. Review the README.md in each project for detailed documentation
2. Explore the test files to understand test scenarios
3. Modify enhancement parameters in the enhancer modules
4. Add custom image types or enhancement algorithms

## Project Differences

- **Project A**: Simpler, faster, good for basic use cases
- **Project B**: Advanced algorithms, quality metrics, better for detailed analysis

Choose based on your needs!

