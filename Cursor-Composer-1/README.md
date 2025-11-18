# UI/UX Image Optimization Pipeline - Evaluation Project

This repository contains two complete implementations for evaluating AI models' ability to perform UI/UX-oriented visual optimization on real-world images.

## Project Structure

```
.
├── Project_A/          # Basic implementation with core features
├── Project_B/          # Advanced implementation with enhanced algorithms
└── README.md           # This file
```

## Overview

Both projects implement a complete pipeline that:

1. **Automatically collects or generates** a batch of images (screenshots, photos, mixed assets)
2. **Performs UI/UX visual enhancement** on each image
3. **Outputs original and optimized versions** into separate folders
4. **Generates comparison images** showing before/after results
5. **Includes automated testing** and a fully reproducible environment

## Quick Start

### Project A (Basic Implementation)

```bash
cd Project_A
chmod +x setup.sh run_tests.sh
./setup.sh
./run_tests.sh
```

### Project B (Advanced Implementation)

```bash
cd Project_B
chmod +x setup.sh run_tests.sh
./setup.sh
./run_tests.sh
```

## Project Comparison

| Feature | Project A | Project B |
|---------|-----------|-----------|
| **Image Generation** | Basic UI/Photo/Mixed | Advanced (5 UI patterns) |
| **Enhancement Algorithms** | Standard (bilateral filter, CLAHE) | Advanced (NL-means, unsharp mask) |
| **Quality Metrics** | Enhancement notes | Quantitative metrics |
| **Output Reports** | JSON metadata | JSON + Text summary |
| **Error Handling** | Basic | Advanced with detailed errors |
| **Code Organization** | Monolithic modules | Modular with separate managers |

## Key Features

### Image Generation
- **UI Screenshots**: Synthetic app interfaces with realistic layout issues
- **Photos**: Generated images with noise and exposure problems
- **Mixed Content**: Combination of UI and photo elements
- **Imperfections**: Noise, blur, color shifts, exposure issues

### UI/UX Enhancements
- **Exposure Correction**: Automatic brightness and contrast adjustment
- **Color Harmonization**: Unified color palette across images
- **Noise Reduction**: Advanced denoising while preserving details
- **Clarity Enhancement**: Sharpness and detail improvement
- **Contrast Normalization**: Adaptive histogram equalization
- **Modern Styling**: Contemporary UI aesthetic improvements

### Output Structure
Both projects create the same folder structure:
```
output/
├── images_original/      # Original input images
├── images_optimized/     # Enhanced output images
├── images_comparison/    # Side-by-side comparisons
└── results/
    ├── metadata.json     # Processing metadata
    └── pipeline.log      # Execution logs
```

## Test Scenarios

### Normal Flow
- Valid image input → successful optimization → output files created
- Multiple images processed in batch
- Metadata JSON generated with correct structure

### Edge Cases
- **Low-resolution images**: Processed with appropriate scaling
- **Noisy screenshots**: Enhanced with noise reduction
- **Very large images**: Handled efficiently
- **Very small images**: Preserved and enhanced
- **Broken files**: Graceful error handling

### Boundary Cases
- Empty input directory
- Single image processing
- Large batch processing (10+ images)

## Requirements

Both projects require:
- Python 3.8+
- Pillow >= 10.0.0
- opencv-python >= 4.8.0
- numpy >= 1.24.0
- pytest >= 7.4.0 (for testing)

## Evaluation Criteria

The implementations are evaluated on:

1. **Correctness**: Proper image processing and enhancement
2. **Efficiency**: Optimized processing algorithms
3. **Edge Case Handling**: Graceful handling of malformed inputs
4. **Test Coverage**: Comprehensive automated tests
5. **Reproducibility**: Complete environment setup
6. **Documentation**: Clear usage and explanation

## Quantitative Metrics

Both pipelines track:
- **Number of processed images**: Total successfully enhanced
- **Pass/fail ratio**: Success rate percentage
- **Edge-case coverage**: Tests for various image types and sizes
- **Structural consistency**: Verification of output folder structure

## Usage Examples

### Project A

```bash
# Generate and process 5 images
python main.py

# Process 10 images
python main.py --num-images 10

# Use existing images
python main.py --no-generate
```

### Project B

```bash
# Generate and process 5 images
python main.py

# Process specific image types
python main.py --num-images 10 --image-types ui photo

# Custom output directory
python main.py --output-dir my_results
```

## Testing

### Run All Tests

**Project A:**
```bash
cd Project_A
./run_tests.sh
```

**Project B:**
```bash
cd Project_B
./run_tests.sh
```

### Manual Testing

```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Run unit tests
python -m pytest tests/ -v

# Run pipeline
python main.py --num-images 5
```

## Expected Output

For each processed image, both projects output:

1. **Original image**: `images_original/input_001.png`
2. **Optimized image**: `images_optimized/input_001_optimized.png`
3. **Comparison image**: `images_comparison/input_001_compare.png`
4. **JSON metadata entry** describing the image mapping

### Metadata Format (Project A)

```json
{
  "id": "001",
  "original": "images_original/input_001.png",
  "optimized": "images_optimized/input_001_optimized.png",
  "comparison": "images_comparison/input_001_compare.png",
  "notes": "Improved exposure and contrast; Harmonized color palette; ...",
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

### Metadata Format (Project B)

```json
{
  "id": "001",
  "original": "images_original/input_001.png",
  "optimized": "images_optimized/input_001_optimized.png",
  "comparison": "images_comparison/input_001_compare.png",
  "enhancements": ["brightness_boost", "color_harmonization", ...],
  "metrics": {
    "brightness_improvement": 15.2,
    "contrast_improvement": 9.8,
    "sharpness_improvement": 52.3
  },
  "timestamp": "2024-01-15T10:30:45.123456"
}
```

## Limitations

1. **Aesthetic Optimization Only**: The pipelines improve visual appearance but do not change semantic content
2. **No Semantic Understanding**: Cannot understand UI context or content meaning
3. **Generated vs Real Images**: Synthetic images may differ from real-world screenshots
4. **Style Consistency**: While harmonization is applied, perfect consistency across diverse sources may not be achievable

## Potential Pitfalls

1. **Over-stylization**: Aggressive enhancement may make images look artificial
2. **Semantic Drift**: Enhancement should preserve original content meaning
3. **Folder Structure**: Ensure proper directory creation and permissions
4. **Inconsistent Style**: Mixed image sources may result in varying optimization quality

## Troubleshooting

### Common Issues

**Import Errors:**
```bash
pip install --upgrade -r requirements.txt
```

**Permission Errors (Linux/Mac):**
```bash
chmod +x setup.sh run_tests.sh
```

**OpenCV Installation Issues:**
```bash
pip install opencv-python-headless
```

**Font Issues:**
- Both projects fall back to default fonts if system fonts are unavailable
- This is handled gracefully

## Documentation

- **Project A**: See `Project_A/README.md`
- **Project B**: See `Project_B/README.md`
- **Test Documentation**: See test files in `tests/` directories

## License

This project is provided as-is for evaluation purposes.

## Contact

For issues or questions, please refer to the individual project README files or test documentation.

