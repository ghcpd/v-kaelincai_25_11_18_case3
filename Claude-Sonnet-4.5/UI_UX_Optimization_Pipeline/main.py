"""
Main Pipeline Runner
Orchestrates the complete UI/UX image optimization workflow.
"""

import os
import sys
import json
from datetime import datetime

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.image_generator import ImageGenerator
from src.image_optimizer import UIUXOptimizer, ComparisonGenerator


def print_header(title):
    """Print a formatted header."""
    print("\n" + "=" * 80)
    print(title.center(80))
    print("=" * 80 + "\n")


def print_section(title):
    """Print a section divider."""
    print("\n" + "-" * 80)
    print(title)
    print("-" * 80)


def run_pipeline():
    """Execute the complete optimization pipeline."""
    start_time = datetime.now()
    
    print_header("UI/UX IMAGE OPTIMIZATION PIPELINE")
    print(f"Start Time: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ensure directories exist
    for directory in ["images_original", "images_optimized", "images_comparison", "results"]:
        os.makedirs(directory, exist_ok=True)
    
    # Step 1: Generate Test Images
    print_section("STEP 1: Generating Test Images")
    generator = ImageGenerator("images_original")
    test_images = generator.generate_all_test_images()
    
    print(f"✓ Generated {len(test_images)} test images")
    print("\nTest Image Types:")
    for img_type, filepath in test_images:
        filename = os.path.basename(filepath)
        print(f"  - {filename:30s} : {img_type}")
    
    # Step 2: Optimize Images
    print_section("STEP 2: Optimizing Images")
    optimizer = UIUXOptimizer("images_optimized")
    results = optimizer.optimize_batch("images_original", "input_*.png")
    
    print(f"\nOptimization Results:")
    print(f"  Total Images: {results['total']}")
    print(f"  Successful:   {results['successful']} ({results['successful']/results['total']*100:.1f}%)")
    print(f"  Failed:       {results['failed']}")
    
    if results['failed'] > 0:
        print("\nFailed Images:")
        for img_data in results['images']:
            if img_data['status'] == 'failed':
                print(f"  - {img_data['input']}: {img_data.get('error', 'Unknown error')}")
    
    # Step 3: Generate Comparisons
    print_section("STEP 3: Generating Comparison Images")
    comparator = ComparisonGenerator("images_comparison")
    comparisons = comparator.generate_batch_comparisons(results)
    
    print(f"✓ Generated {len(comparisons)} comparison images")
    
    # Step 4: Save Results
    print_section("STEP 4: Saving Results")
    
    # Save optimization results
    results_file = "results/optimization_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Optimization results saved to: {results_file}")
    
    # Generate detailed report
    report_file = "results/detailed_report.txt"
    with open(report_file, 'w') as f:
        f.write("=" * 80 + "\n")
        f.write("UI/UX IMAGE OPTIMIZATION PIPELINE - DETAILED REPORT\n")
        f.write("=" * 80 + "\n\n")
        f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("SUMMARY\n")
        f.write("-" * 80 + "\n")
        f.write(f"Total Images Processed: {results['total']}\n")
        f.write(f"Successful Optimizations: {results['successful']}\n")
        f.write(f"Failed Optimizations: {results['failed']}\n")
        f.write(f"Success Rate: {results['successful']/results['total']*100:.2f}%\n")
        f.write(f"Comparison Images Generated: {len(comparisons)}\n\n")
        
        f.write("OPTIMIZATION DETAILS\n")
        f.write("-" * 80 + "\n")
        for i, img_data in enumerate(results['images'], 1):
            f.write(f"\n{i}. {os.path.basename(img_data['input'])}\n")
            f.write(f"   Status: {img_data['status']}\n")
            if img_data['status'] == 'success':
                f.write(f"   Original Size: {img_data['original_size']}\n")
                f.write(f"   Optimized Size: {img_data['optimized_size']}\n")
                f.write(f"   Output: {os.path.basename(img_data['output'])}\n")
                if 'comparison' in img_data:
                    f.write(f"   Comparison: {os.path.basename(img_data['comparison'])}\n")
                f.write(f"   Notes: {img_data['notes']}\n")
            else:
                f.write(f"   Error: {img_data.get('error', 'Unknown')}\n")
        
        f.write("\n" + "=" * 80 + "\n")
    
    print(f"✓ Detailed report saved to: {report_file}")
    
    # Generate summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    
    print_section("PIPELINE SUMMARY")
    print(f"Status: {'✓ SUCCESS' if results['failed'] == 0 else '⚠ COMPLETED WITH ERRORS'}")
    print(f"Duration: {duration:.2f} seconds")
    print(f"")
    print(f"Output Locations:")
    print(f"  - Original Images:    images_original/")
    print(f"  - Optimized Images:   images_optimized/")
    print(f"  - Comparison Images:  images_comparison/")
    print(f"  - Results:            results/")
    print(f"")
    print(f"Next Steps:")
    print(f"  1. Review comparison images: images_comparison/")
    print(f"  2. Check detailed report: results/detailed_report.txt")
    print(f"  3. Run automated tests: python tests/test_pipeline.py")
    
    print_header("PIPELINE COMPLETED")
    
    return results['failed'] == 0


if __name__ == "__main__":
    try:
        success = run_pipeline()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ Pipeline failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
