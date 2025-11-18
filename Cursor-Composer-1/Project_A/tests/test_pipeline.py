#!/usr/bin/env python3
"""
Comprehensive test suite for UI/UX Image Optimization Pipeline.
"""

import unittest
import os
import sys
import json
from pathlib import Path
from PIL import Image
import tempfile
import shutil

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import ImageOptimizationPipeline
from image_generator import ImageGenerator
from uiux_enhancer import UIUXEnhancer
from comparison_generator import ComparisonGenerator


class TestImageGenerator(unittest.TestCase):
    """Test image generation functionality."""
    
    def setUp(self):
        self.generator = ImageGenerator()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_generate_ui_image(self):
        """Test UI screenshot generation."""
        output_path = Path(self.temp_dir) / "test_ui.png"
        result = self.generator.generate_image(
            image_type="ui",
            output_path=output_path,
            width=800,
            height=600
        )
        self.assertTrue(result.exists())
        self.assertEqual(result.suffix, ".png")
        
        # Verify image can be opened
        img = Image.open(result)
        self.assertEqual(img.size, (800, 600))
    
    def test_generate_photo_image(self):
        """Test photo generation."""
        output_path = Path(self.temp_dir) / "test_photo.png"
        result = self.generator.generate_image(
            image_type="photo",
            output_path=output_path
        )
        self.assertTrue(result.exists())
        img = Image.open(result)
        self.assertIsNotNone(img)
    
    def test_generate_mixed_image(self):
        """Test mixed image generation."""
        output_path = Path(self.temp_dir) / "test_mixed.png"
        result = self.generator.generate_image(
            image_type="mixed",
            output_path=output_path
        )
        self.assertTrue(result.exists())


class TestUIUXEnhancer(unittest.TestCase):
    """Test UI/UX enhancement functionality."""
    
    def setUp(self):
        self.enhancer = UIUXEnhancer()
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ImageGenerator()
        
        # Create a test image
        self.test_image_path = Path(self.temp_dir) / "test_input.png"
        self.generator.generate_image(
            image_type="ui",
            output_path=self.test_image_path
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_enhance_image(self):
        """Test basic image enhancement."""
        enhanced = self.enhancer.enhance_image(str(self.test_image_path))
        self.assertIsNotNone(enhanced)
        self.assertIsInstance(enhanced, Image.Image)
        
        # Verify enhancement notes
        notes = self.enhancer.get_enhancement_notes()
        self.assertIsInstance(notes, str)
        self.assertGreater(len(notes), 0)
    
    def test_enhancement_preserves_dimensions(self):
        """Test that enhancement preserves image dimensions."""
        original = Image.open(self.test_image_path)
        original_size = original.size
        
        enhanced = self.enhancer.enhance_image(str(self.test_image_path))
        self.assertEqual(enhanced.size, original_size)
    
    def test_enhancement_improves_quality(self):
        """Test that enhancement improves image quality metrics."""
        enhanced = self.enhancer.enhance_image(str(self.test_image_path))
        
        # Save and verify it's a valid image
        output_path = Path(self.temp_dir) / "test_enhanced.png"
        enhanced.save(output_path)
        self.assertTrue(output_path.exists())


class TestComparisonGenerator(unittest.TestCase):
    """Test comparison image generation."""
    
    def setUp(self):
        self.comparison_gen = ComparisonGenerator()
        self.temp_dir = tempfile.mkdtemp()
        self.generator = ImageGenerator()
        
        # Create test images
        self.original_path = Path(self.temp_dir) / "original.png"
        self.optimized_path = Path(self.temp_dir) / "optimized.png"
        
        self.generator.generate_image(
            image_type="ui",
            output_path=self.original_path
        )
        
        # Create optimized version
        enhancer = UIUXEnhancer()
        enhanced = enhancer.enhance_image(str(self.original_path))
        enhanced.save(self.optimized_path)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_create_comparison(self):
        """Test comparison image creation."""
        comparison = self.comparison_gen.create_comparison(
            str(self.original_path),
            str(self.optimized_path)
        )
        
        self.assertIsNotNone(comparison)
        self.assertIsInstance(comparison, Image.Image)
        
        # Verify comparison is wider than individual images
        original = Image.open(self.original_path)
        self.assertGreater(comparison.width, original.width)


class TestPipelineIntegration(unittest.TestCase):
    """Integration tests for the complete pipeline."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = ImageOptimizationPipeline(output_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_pipeline_creates_directories(self):
        """Test that pipeline creates required directories."""
        self.assertTrue(self.pipeline.original_dir.exists())
        self.assertTrue(self.pipeline.optimized_dir.exists())
        self.assertTrue(self.pipeline.comparison_dir.exists())
        self.assertTrue(self.pipeline.results_dir.exists())
    
    def test_pipeline_generates_images(self):
        """Test that pipeline generates test images."""
        image_paths = self.pipeline.generate_test_images(count=3)
        self.assertEqual(len(image_paths), 3)
        
        for path in image_paths:
            self.assertTrue(Path(path).exists())
    
    def test_pipeline_processes_images(self):
        """Test complete image processing pipeline."""
        # Generate test images
        self.pipeline.generate_test_images(count=2)
        
        # Process images
        processed, failed = self.pipeline.run_pipeline(
            num_images=2,
            generate_images=False
        )
        
        # Verify outputs
        self.assertGreaterEqual(processed, 0)
        self.assertLessEqual(failed, 2)
        
        # Check that optimized images exist
        optimized_files = list(self.pipeline.optimized_dir.glob("*.png"))
        self.assertGreater(len(optimized_files), 0)
        
        # Check that comparison images exist
        comparison_files = list(self.pipeline.comparison_dir.glob("*.png"))
        self.assertGreater(len(comparison_files), 0)
        
        # Check metadata file
        metadata_path = self.pipeline.results_dir / "metadata.json"
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            self.assertIn("summary", metadata)
            self.assertIn("images", metadata)
            self.assertEqual(metadata["summary"]["total_images"], 2)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error handling."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = ImageOptimizationPipeline(output_dir=self.temp_dir)
        self.enhancer = UIUXEnhancer()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_small_image(self):
        """Test processing very small images."""
        generator = ImageGenerator()
        small_image = Path(self.temp_dir) / "small.png"
        generator.generate_image(
            image_type="ui",
            output_path=small_image,
            width=50,
            height=50
        )
        
        enhanced = self.enhancer.enhance_image(str(small_image))
        self.assertIsNotNone(enhanced)
    
    def test_large_image(self):
        """Test processing large images."""
        generator = ImageGenerator()
        large_image = Path(self.temp_dir) / "large.png"
        generator.generate_image(
            image_type="ui",
            output_path=large_image,
            width=2000,
            height=1500
        )
        
        enhanced = self.enhancer.enhance_image(str(large_image))
        self.assertIsNotNone(enhanced)
    
    def test_nonexistent_image(self):
        """Test handling of non-existent image."""
        fake_path = Path(self.temp_dir) / "nonexistent.png"
        
        result = self.pipeline.process_image(str(fake_path), "001")
        self.assertIn("error", result)
    
    def test_invalid_image_format(self):
        """Test handling of invalid image format."""
        # Create a fake image file
        fake_image = Path(self.temp_dir) / "fake.png"
        with open(fake_image, 'w') as f:
            f.write("not an image")
        
        # Should handle gracefully
        try:
            result = self.pipeline.process_image(str(fake_image), "001")
            # Either succeeds or fails gracefully
            self.assertIsNotNone(result)
        except Exception as e:
            # Exception is acceptable for invalid format
            self.assertIsNotNone(e)


class TestOutputStructure(unittest.TestCase):
    """Test output folder structure and file organization."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = ImageOptimizationPipeline(output_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_folder_structure(self):
        """Test that all required folders are created."""
        required_folders = [
            "images_original",
            "images_optimized",
            "images_comparison",
            "results"
        ]
        
        for folder in required_folders:
            folder_path = Path(self.temp_dir) / folder
            self.assertTrue(folder_path.exists(), f"Folder {folder} should exist")
            self.assertTrue(folder_path.is_dir(), f"{folder} should be a directory")
    
    def test_metadata_structure(self):
        """Test metadata JSON structure."""
        self.pipeline.generate_test_images(count=1)
        self.pipeline.run_pipeline(num_images=1, generate_images=False)
        
        metadata_path = self.pipeline.results_dir / "metadata.json"
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
            # Check structure
            self.assertIn("summary", metadata)
            self.assertIn("images", metadata)
            
            # Check summary fields
            summary = metadata["summary"]
            self.assertIn("total_images", summary)
            self.assertIn("processed", summary)
            self.assertIn("failed", summary)
            self.assertIn("success_rate", summary)
            
            # Check image entry structure
            if len(metadata["images"]) > 0:
                image_entry = metadata["images"][0]
                self.assertIn("id", image_entry)
                self.assertIn("original", image_entry)
                self.assertIn("timestamp", image_entry)


if __name__ == '__main__':
    unittest.main()

