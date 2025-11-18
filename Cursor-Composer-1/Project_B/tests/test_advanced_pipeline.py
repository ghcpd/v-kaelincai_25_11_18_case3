#!/usr/bin/env python3
"""
Comprehensive test suite for Advanced UI/UX Image Optimization Pipeline (Project B).
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

from main import AdvancedImagePipeline
from image_collector import ImageCollector
from advanced_enhancer import AdvancedUIUXEnhancer
from comparison_builder import ComparisonBuilder
from folder_manager import FolderManager
from metrics_calculator import MetricsCalculator


class TestImageCollector(unittest.TestCase):
    """Test advanced image collection functionality."""
    
    def setUp(self):
        self.collector = ImageCollector()
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_generate_ui_images(self):
        """Test UI image generation with different patterns."""
        patterns = ["dashboard", "landing_page", "form", "card_layout", "navigation"]
        
        for pattern_type in ["ui", "photo", "mixed"]:
            output_path = Path(self.temp_dir) / f"test_{pattern_type}.png"
            result = self.collector.generate_image(
                image_type=pattern_type,
                output_path=output_path
            )
            self.assertTrue(result.exists())
            img = Image.open(result)
            self.assertIsNotNone(img)
    
    def test_imperfections_application(self):
        """Test that imperfections are applied when requested."""
        output_path = Path(self.temp_dir) / "test_imperfect.png"
        self.collector.generate_image(
            image_type="ui",
            output_path=output_path,
            add_imperfections=True
        )
        
        # Verify image exists and can be opened
        self.assertTrue(output_path.exists())
        img = Image.open(output_path)
        self.assertIsNotNone(img)


class TestAdvancedEnhancer(unittest.TestCase):
    """Test advanced enhancement functionality."""
    
    def setUp(self):
        self.enhancer = AdvancedUIUXEnhancer()
        self.temp_dir = tempfile.mkdtemp()
        self.collector = ImageCollector()
        
        # Create test image
        self.test_image_path = Path(self.temp_dir) / "test_input.png"
        self.output_path = Path(self.temp_dir) / "test_output.png"
        self.collector.generate_image(
            image_type="ui",
            output_path=self.test_image_path
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_process_image(self):
        """Test image processing."""
        result = self.enhancer.process_image(
            str(self.test_image_path),
            str(self.output_path)
        )
        
        self.assertTrue(result["success"])
        self.assertIn("enhancements", result)
        self.assertGreater(len(result["enhancements"]), 0)
        self.assertTrue(self.output_path.exists())
    
    def test_enhancement_preserves_size(self):
        """Test that enhancement preserves image dimensions."""
        original = Image.open(self.test_image_path)
        original_size = original.size
        
        self.enhancer.process_image(
            str(self.test_image_path),
            str(self.output_path)
        )
        
        enhanced = Image.open(self.output_path)
        self.assertEqual(enhanced.size, original_size)


class TestComparisonBuilder(unittest.TestCase):
    """Test comparison image building."""
    
    def setUp(self):
        self.builder = ComparisonBuilder()
        self.temp_dir = tempfile.mkdtemp()
        self.collector = ImageCollector()
        self.enhancer = AdvancedUIUXEnhancer()
        
        # Create test images
        self.original_path = Path(self.temp_dir) / "original.png"
        self.optimized_path = Path(self.temp_dir) / "optimized.png"
        self.comparison_path = Path(self.temp_dir) / "comparison.png"
        
        self.collector.generate_image(
            image_type="ui",
            output_path=self.original_path
        )
        
        self.enhancer.process_image(
            str(self.original_path),
            str(self.optimized_path)
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_build_comparison(self):
        """Test comparison image creation."""
        comparison = self.builder.build_comparison(
            str(self.original_path),
            str(self.optimized_path),
            str(self.comparison_path)
        )
        
        self.assertIsNotNone(comparison)
        self.assertTrue(self.comparison_path.exists())
        
        # Verify comparison is wider than individual images
        original = Image.open(self.original_path)
        comparison_img = Image.open(self.comparison_path)
        self.assertGreater(comparison_img.width, original.width)


class TestFolderManager(unittest.TestCase):
    """Test folder management."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.folder_manager = FolderManager(self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_directory_creation(self):
        """Test that all directories are created."""
        self.assertTrue(self.folder_manager.original_dir.exists())
        self.assertTrue(self.folder_manager.optimized_dir.exists())
        self.assertTrue(self.folder_manager.comparison_dir.exists())
        self.assertTrue(self.folder_manager.results_dir.exists())
    
    def test_verify_structure(self):
        """Test structure verification."""
        missing = self.folder_manager.verify_structure()
        self.assertEqual(len(missing), 0)


class TestMetricsCalculator(unittest.TestCase):
    """Test metrics calculation."""
    
    def setUp(self):
        self.calculator = MetricsCalculator()
        self.temp_dir = tempfile.mkdtemp()
        self.collector = ImageCollector()
        self.enhancer = AdvancedUIUXEnhancer()
        
        # Create test images
        self.original_path = Path(self.temp_dir) / "original.png"
        self.optimized_path = Path(self.temp_dir) / "optimized.png"
        
        self.collector.generate_image(
            image_type="ui",
            output_path=self.original_path
        )
        
        self.enhancer.process_image(
            str(self.original_path),
            str(self.optimized_path)
        )
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_calculate_improvement(self):
        """Test metrics calculation."""
        metrics = self.calculator.calculate_improvement(
            str(self.original_path),
            str(self.optimized_path)
        )
        
        self.assertIn("brightness_improvement", metrics)
        self.assertIn("contrast_improvement", metrics)
        self.assertIn("sharpness_improvement", metrics)
        self.assertIn("saturation_improvement", metrics)
        self.assertIn("noise_reduction", metrics)


class TestAdvancedPipelineIntegration(unittest.TestCase):
    """Integration tests for the complete advanced pipeline."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = AdvancedImagePipeline(output_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_pipeline_initialization(self):
        """Test pipeline initialization."""
        self.assertIsNotNone(self.pipeline.folder_manager)
        self.assertIsNotNone(self.pipeline.collector)
        self.assertIsNotNone(self.pipeline.enhancer)
        self.assertIsNotNone(self.pipeline.comparison_builder)
        self.assertIsNotNone(self.pipeline.metrics)
    
    def test_collect_images(self):
        """Test image collection."""
        image_paths = self.pipeline.collect_images(count=3)
        self.assertEqual(len(image_paths), 3)
        
        for path in image_paths:
            self.assertTrue(path.exists())
    
    def test_complete_pipeline(self):
        """Test complete pipeline execution."""
        report = self.pipeline.run_pipeline(
            num_images=3,
            generate_images=True
        )
        
        # Verify report structure
        self.assertIn("summary", report)
        self.assertIn("average_metrics", report)
        
        # Verify outputs
        optimized_files = list(self.pipeline.folder_manager.optimized_dir.glob("*.png"))
        self.assertGreater(len(optimized_files), 0)
        
        comparison_files = list(self.pipeline.folder_manager.comparison_dir.glob("*.png"))
        self.assertGreater(len(comparison_files), 0)
        
        # Check metadata file
        metadata_path = self.pipeline.folder_manager.results_dir / "metadata.json"
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            self.assertIn("summary", metadata)
            self.assertIn("images", metadata)


class TestEdgeCasesAdvanced(unittest.TestCase):
    """Test edge cases for advanced pipeline."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = AdvancedImagePipeline(output_dir=self.temp_dir)
        self.enhancer = AdvancedUIUXEnhancer()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_very_small_image(self):
        """Test processing very small images."""
        collector = ImageCollector()
        small_image = Path(self.temp_dir) / "small.png"
        output_image = Path(self.temp_dir) / "small_out.png"
        
        collector.generate_image(
            image_type="ui",
            output_path=small_image,
            width=32,
            height=32
        )
        
        result = self.enhancer.process_image(str(small_image), str(output_image))
        self.assertTrue(result["success"])
    
    def test_very_large_image(self):
        """Test processing large images."""
        collector = ImageCollector()
        large_image = Path(self.temp_dir) / "large.png"
        output_image = Path(self.temp_dir) / "large_out.png"
        
        collector.generate_image(
            image_type="ui",
            output_path=large_image,
            width=3000,
            height=2000
        )
        
        result = self.enhancer.process_image(str(large_image), str(output_image))
        # May take longer but should complete
        self.assertIsNotNone(result)
    
    def test_nonexistent_image(self):
        """Test handling of non-existent image."""
        fake_path = Path(self.temp_dir) / "nonexistent.png"
        
        result = self.pipeline.process_single_image(fake_path, "001")
        self.assertIn("error", result)


class TestOutputStructureAdvanced(unittest.TestCase):
    """Test output structure for advanced pipeline."""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.pipeline = AdvancedImagePipeline(output_dir=self.temp_dir)
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_metadata_structure(self):
        """Test metadata JSON structure."""
        self.pipeline.collect_images(count=2)
        report = self.pipeline.run_pipeline(num_images=2, generate_images=False)
        
        metadata_path = self.pipeline.folder_manager.results_dir / "metadata.json"
        self.assertTrue(metadata_path.exists())
        
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
            
            # Check structure
            self.assertIn("summary", metadata)
            self.assertIn("images", metadata)
            self.assertIn("average_metrics", metadata)
            
            # Check summary
            summary = metadata["summary"]
            self.assertIn("total_images", summary)
            self.assertIn("success_rate", summary)
            
            # Check image entries
            if len(metadata["images"]) > 0:
                image_entry = metadata["images"][0]
                self.assertIn("id", image_entry)
                self.assertIn("enhancements", image_entry)
                if "metrics" in image_entry:
                    self.assertIsInstance(image_entry["metrics"], dict)


if __name__ == '__main__':
    unittest.main()

