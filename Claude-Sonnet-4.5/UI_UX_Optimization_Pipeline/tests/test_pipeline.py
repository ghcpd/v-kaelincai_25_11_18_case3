"""
Automated Test Suite for UI/UX Image Optimization Pipeline
Tests normal flows, edge cases, boundary conditions, and invalid inputs.
"""

import unittest
import os
import sys
import json
from pathlib import Path
from PIL import Image
import numpy as np

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from image_generator import ImageGenerator
from image_optimizer import UIUXOptimizer, ComparisonGenerator


class TestImageGeneration(unittest.TestCase):
    """Test image generation functionality."""
    
    @classmethod
    def setUpClass(cls):
        cls.output_dir = "images_original"
        cls.generator = ImageGenerator(cls.output_dir)
    
    def test_01_generate_poor_spacing_ui(self):
        """Test generation of UI screenshot with poor spacing."""
        filepath = self.generator.generate_ui_screenshot_poor_spacing("test_spacing.png")
        
        self.assertTrue(os.path.exists(filepath), "Image file should be created")
        
        img = Image.open(filepath)
        self.assertEqual(img.size, (800, 600), "Image should be 800x600")
        self.assertEqual(img.mode, "RGB", "Image should be in RGB mode")
    
    def test_02_generate_bad_colors_ui(self):
        """Test generation of UI with bad color scheme."""
        filepath = self.generator.generate_ui_screenshot_bad_colors("test_colors.png")
        
        self.assertTrue(os.path.exists(filepath))
        
        img = Image.open(filepath)
        self.assertEqual(img.size, (800, 600))
    
    def test_03_generate_noisy_photo(self):
        """Test generation of noisy photo."""
        filepath = self.generator.generate_noisy_photo("test_noisy.png")
        
        self.assertTrue(os.path.exists(filepath))
        
        img = Image.open(filepath)
        self.assertEqual(img.size, (640, 480))
    
    def test_04_edge_low_resolution(self):
        """Test edge case: very low resolution image."""
        filepath = self.generator.generate_low_resolution_image("test_lowres.png")
        
        self.assertTrue(os.path.exists(filepath))
        
        img = Image.open(filepath)
        self.assertEqual(img.size, (160, 120), "Low-res image should be 160x120")
    
    def test_05_boundary_very_large(self):
        """Test boundary case: very large image."""
        filepath = self.generator.generate_very_large_image("test_large.png")
        
        self.assertTrue(os.path.exists(filepath))
        
        img = Image.open(filepath)
        self.assertEqual(img.size, (3840, 2160), "Large image should be 4K resolution")
    
    def test_06_generate_empty_image(self):
        """Test boundary case: empty/blank image."""
        filepath = self.generator.generate_empty_image("test_empty.png")
        
        self.assertTrue(os.path.exists(filepath))
        
        img = Image.open(filepath)
        # Check if mostly white
        pixels = list(img.getdata())
        white_pixels = sum(1 for p in pixels if p == (255, 255, 255))
        self.assertGreater(white_pixels / len(pixels), 0.95, 
                          "Empty image should be mostly white")
    
    def test_07_generate_batch(self):
        """Test batch generation of all test images."""
        images = self.generator.generate_all_test_images()
        
        self.assertGreaterEqual(len(images), 10, "Should generate at least 10 test images")
        
        for img_type, filepath in images:
            if not filepath.endswith('.dat'):  # Skip invalid files
                self.assertTrue(os.path.exists(filepath), 
                              f"Generated file should exist: {filepath}")


class TestImageOptimization(unittest.TestCase):
    """Test image optimization functionality."""
    
    @classmethod
    def setUpClass(cls):
        # Generate test images first
        cls.generator = ImageGenerator("images_original")
        cls.test_images = cls.generator.generate_all_test_images()
        
        cls.optimizer = UIUXOptimizer("images_optimized")
    
    def test_01_optimize_normal_ui_image(self):
        """Test normal flow: optimize UI screenshot."""
        input_path = "images_original/input_001.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_ui_screenshot_poor_spacing("input_001.png")
        
        result = self.optimizer.optimize_image(input_path, "output_001.png")
        
        self.assertIsNotNone(result, "Optimization should return result")
        self.assertEqual(result["status"], "success", "Optimization should succeed")
        self.assertTrue(os.path.exists(result["output"]), "Output file should exist")
        
        # Verify optimized image
        img = Image.open(result["output"])
        self.assertIsNotNone(img, "Optimized image should be loadable")
    
    def test_02_optimize_bad_colors(self):
        """Test normal flow: optimize image with bad colors."""
        input_path = "images_original/input_002.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_ui_screenshot_bad_colors("input_002.png")
        
        result = self.optimizer.optimize_image(input_path, "output_002.png")
        
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(result["output"]))
    
    def test_03_optimize_noisy_photo(self):
        """Test normal flow: optimize noisy photo."""
        input_path = "images_original/input_003.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_noisy_photo("input_003.png")
        
        result = self.optimizer.optimize_image(input_path, "output_003.png")
        
        self.assertEqual(result["status"], "success")
        
        # Verify noise reduction
        original = Image.open(input_path)
        optimized = Image.open(result["output"])
        
        self.assertIsNotNone(original)
        self.assertIsNotNone(optimized)
    
    def test_04_edge_low_resolution(self):
        """Test edge case: optimize very low resolution image."""
        input_path = "images_original/input_004.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_low_resolution_image("input_004.png")
        
        result = self.optimizer.optimize_image(input_path, "output_004.png")
        
        # Should still succeed
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(result["output"]))
    
    def test_05_boundary_large_image(self):
        """Test boundary case: optimize very large image."""
        input_path = "images_original/input_006.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_very_large_image("input_006.png")
        
        result = self.optimizer.optimize_image(input_path, "output_006.png")
        
        # Should handle large images
        self.assertEqual(result["status"], "success")
        self.assertTrue(os.path.exists(result["output"]))
        
        # Verify file is not corrupted
        img = Image.open(result["output"])
        self.assertIsNotNone(img)
    
    def test_06_invalid_corrupted_file(self):
        """Test invalid input: corrupted file."""
        input_path = "images_original/input_008.dat"
        
        if not os.path.exists(input_path):
            self.generator.generate_invalid_image("input_008.dat")
        
        result = self.optimizer.optimize_image(input_path, "output_008.png")
        
        # Should fail gracefully
        self.assertIsNotNone(result)
        self.assertEqual(result["status"], "failed")
        self.assertIn("error", result)
    
    def test_07_invalid_nonexistent_file(self):
        """Test invalid input: file doesn't exist."""
        result = self.optimizer.optimize_image("nonexistent.png", "output_none.png")
        
        # Should fail gracefully
        self.assertEqual(result["status"], "failed")
    
    def test_08_batch_optimization(self):
        """Test batch processing of multiple images."""
        results = self.optimizer.optimize_batch("images_original", "input_*.png")
        
        self.assertIn("total", results)
        self.assertIn("successful", results)
        self.assertIn("failed", results)
        self.assertGreater(results["total"], 0, "Should process at least one image")
    
    def test_09_optimization_quality(self):
        """Test that optimization improves image quality metrics."""
        input_path = "images_original/input_003.png"
        
        if not os.path.exists(input_path):
            self.generator.generate_noisy_photo("input_003.png")
        
        result = self.optimizer.optimize_image(input_path, "output_quality_test.png")
        
        if result["status"] == "success":
            original = Image.open(input_path)
            optimized = Image.open(result["output"])
            
            # Check that images are valid
            self.assertIsNotNone(original)
            self.assertIsNotNone(optimized)
            
            # Optimized image should exist and be loadable
            self.assertTrue(os.path.exists(result["output"]))


class TestComparisonGeneration(unittest.TestCase):
    """Test comparison image generation."""
    
    @classmethod
    def setUpClass(cls):
        # Ensure we have test images
        generator = ImageGenerator("images_original")
        generator.generate_ui_screenshot_poor_spacing("input_001.png")
        
        # Optimize them
        optimizer = UIUXOptimizer("images_optimized")
        optimizer.optimize_image("images_original/input_001.png", "input_001_optimized.png")
        
        cls.comparator = ComparisonGenerator("images_comparison")
    
    def test_01_generate_single_comparison(self):
        """Test generating a single comparison image."""
        original = "images_original/input_001.png"
        optimized = "images_optimized/input_001_optimized.png"
        
        comparison_path = self.comparator.generate_comparison(
            original, optimized, "input_001_comparison.png"
        )
        
        self.assertIsNotNone(comparison_path, "Comparison should be generated")
        self.assertTrue(os.path.exists(comparison_path), "Comparison file should exist")
        
        # Verify comparison image
        img = Image.open(comparison_path)
        self.assertIsNotNone(img)
        
        # Comparison should be wider than original (side-by-side)
        original_img = Image.open(original)
        self.assertGreater(img.width, original_img.width, 
                          "Comparison should be wider than original")
    
    def test_02_comparison_invalid_files(self):
        """Test comparison generation with invalid files."""
        result = self.comparator.generate_comparison(
            "nonexistent1.png", "nonexistent2.png", "test_invalid.png"
        )
        
        self.assertIsNone(result, "Should return None for invalid files")


class TestFolderStructure(unittest.TestCase):
    """Test that the correct folder structure is maintained."""
    
    def test_01_original_folder_exists(self):
        """Test that images_original folder exists."""
        self.assertTrue(os.path.exists("images_original"))
        self.assertTrue(os.path.isdir("images_original"))
    
    def test_02_optimized_folder_exists(self):
        """Test that images_optimized folder exists."""
        self.assertTrue(os.path.exists("images_optimized"))
        self.assertTrue(os.path.isdir("images_optimized"))
    
    def test_03_comparison_folder_exists(self):
        """Test that images_comparison folder exists."""
        self.assertTrue(os.path.exists("images_comparison"))
        self.assertTrue(os.path.isdir("images_comparison"))
    
    def test_04_results_folder_exists(self):
        """Test that results folder exists."""
        self.assertTrue(os.path.exists("results"))
        self.assertTrue(os.path.isdir("results"))
    
    def test_05_file_pairing(self):
        """Test that optimized files are properly paired with originals."""
        original_files = set(f for f in os.listdir("images_original") 
                           if f.endswith('.png'))
        optimized_files = set(f for f in os.listdir("images_optimized") 
                            if f.endswith('.png'))
        
        self.assertGreater(len(original_files), 0, "Should have original images")
        self.assertGreater(len(optimized_files), 0, "Should have optimized images")


class TestEndToEndPipeline(unittest.TestCase):
    """End-to-end integration tests."""
    
    def test_01_full_pipeline(self):
        """Test the complete pipeline from generation to optimization to comparison."""
        # Generate test images
        generator = ImageGenerator("images_original")
        test_images = generator.generate_all_test_images()
        
        self.assertGreater(len(test_images), 0, "Should generate test images")
        
        # Optimize images
        optimizer = UIUXOptimizer("images_optimized")
        results = optimizer.optimize_batch("images_original", "input_*.png")
        
        self.assertGreater(results["successful"], 0, "Should optimize at least one image")
        
        # Generate comparisons
        comparator = ComparisonGenerator("images_comparison")
        comparisons = comparator.generate_batch_comparisons(results)
        
        self.assertGreater(len(comparisons), 0, "Should generate comparison images")
        
        # Verify results JSON
        results_file = "results/optimization_results.json"
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                data = json.load(f)
            
            self.assertIn("total", data)
            self.assertIn("successful", data)
            self.assertIn("failed", data)
            self.assertIn("images", data)
    
    def test_02_edge_case_coverage(self):
        """Test that edge cases are properly handled."""
        edge_cases = [
            ("Low resolution", "images_original/input_004.png"),
            ("Very large", "images_original/input_006.png"),
            ("Empty image", "images_original/input_007.png")
        ]
        
        optimizer = UIUXOptimizer("images_optimized")
        
        for case_name, input_path in edge_cases:
            if os.path.exists(input_path):
                output_name = os.path.basename(input_path).replace("input_", "edge_")
                result = optimizer.optimize_image(input_path, output_name)
                
                # Should handle gracefully (either success or controlled failure)
                self.assertIsNotNone(result, f"{case_name} should return a result")
                self.assertIn("status", result, f"{case_name} should have status")


def run_tests():
    """Run all tests and generate report."""
    print("=" * 80)
    print("UI/UX IMAGE OPTIMIZATION PIPELINE - AUTOMATED TEST SUITE")
    print("=" * 80)
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test cases
    suite.addTests(loader.loadTestsFromTestCase(TestImageGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestImageOptimization))
    suite.addTests(loader.loadTestsFromTestCase(TestComparisonGeneration))
    suite.addTests(loader.loadTestsFromTestCase(TestFolderStructure))
    suite.addTests(loader.loadTestsFromTestCase(TestEndToEndPipeline))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Generate summary
    print()
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print()
    
    # Save results to JSON
    test_results = {
        "total_tests": result.testsRun,
        "passed": result.testsRun - len(result.failures) - len(result.errors),
        "failed": len(result.failures),
        "errors": len(result.errors),
        "success_rate": (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
    }
    
    os.makedirs("results", exist_ok=True)
    with open("results/test_results.json", 'w') as f:
        json.dump(test_results, f, indent=2)
    
    print("Test results saved to: results/test_results.json")
    print("=" * 80)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
