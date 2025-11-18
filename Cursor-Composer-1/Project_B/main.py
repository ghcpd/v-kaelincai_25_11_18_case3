#!/usr/bin/env python3
"""
Project B: Advanced UI/UX Image Optimization Pipeline
Alternative implementation with enhanced features and different algorithms.
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime
import logging

from image_collector import ImageCollector
from advanced_enhancer import AdvancedUIUXEnhancer
from comparison_builder import ComparisonBuilder
from folder_manager import FolderManager
from metrics_calculator import MetricsCalculator


class AdvancedImagePipeline:
    """Advanced pipeline with enhanced UI/UX optimization capabilities."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.folder_manager = FolderManager(output_dir)
        self.collector = ImageCollector()
        self.enhancer = AdvancedUIUXEnhancer()
        self.comparison_builder = ComparisonBuilder()
        self.metrics = MetricsCalculator()
        
        # Setup logging
        self._setup_logging()
        
        self.metadata = []
        self.stats = {
            "total": 0,
            "processed": 0,
            "failed": 0,
            "errors": []
        }
    
    def _setup_logging(self):
        """Setup logging configuration."""
        log_dir = self.folder_manager.results_dir
        log_file = log_dir / "pipeline.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def collect_images(self, count: int = 5, image_types: List[str] = None) -> List[Path]:
        """Collect or generate test images."""
        if image_types is None:
            image_types = ["ui", "photo", "mixed"]
        
        self.logger.info(f"Collecting {count} images of types: {image_types}")
        image_paths = []
        
        for i in range(count):
            img_type = image_types[i % len(image_types)]
            img_path = self.collector.generate_image(
                image_type=img_type,
                output_path=self.folder_manager.original_dir / f"input_{i+1:03d}.png",
                add_imperfections=True
            )
            image_paths.append(img_path)
            self.logger.info(f"Generated image {i+1}/{count}: {img_path.name} ({img_type})")
        
        return image_paths
    
    def process_single_image(self, image_path: Path, image_id: str) -> Dict:
        """Process a single image through the enhancement pipeline."""
        try:
            if not image_path.exists():
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            self.logger.info(f"Processing image {image_id}: {image_path.name}")
            
            # Generate output paths
            optimized_path = self.folder_manager.optimized_dir / f"input_{image_id}_optimized.png"
            comparison_path = self.folder_manager.comparison_dir / f"input_{image_id}_compare.png"
            
            # Perform advanced enhancement
            enhancement_result = self.enhancer.process_image(
                str(image_path),
                str(optimized_path)
            )
            
            if not enhancement_result["success"]:
                raise Exception(enhancement_result.get("error", "Enhancement failed"))
            
            # Generate comparison
            comparison_result = self.comparison_builder.build_comparison(
                str(image_path),
                str(optimized_path),
                str(comparison_path)
            )
            
            # Calculate quality metrics
            metrics = self.metrics.calculate_improvement(
                str(image_path),
                str(optimized_path)
            )
            
            # Create metadata entry
            metadata_entry = {
                "id": image_id,
                "original": f"images_original/input_{image_id}.png",
                "optimized": f"images_optimized/input_{image_id}_optimized.png",
                "comparison": f"images_comparison/input_{image_id}_compare.png",
                "enhancements": enhancement_result["enhancements"],
                "metrics": metrics,
                "timestamp": datetime.now().isoformat()
            }
            
            self.stats["processed"] += 1
            return metadata_entry
            
        except Exception as e:
            error_msg = str(e)
            self.logger.error(f"Error processing image {image_id}: {error_msg}")
            self.stats["failed"] += 1
            self.stats["errors"].append({
                "image_id": image_id,
                "error": error_msg
            })
            
            return {
                "id": image_id,
                "original": f"images_original/input_{image_id}.png",
                "optimized": None,
                "comparison": None,
                "error": error_msg,
                "timestamp": datetime.now().isoformat()
            }
    
    def run_pipeline(
        self,
        num_images: int = 5,
        generate_images: bool = True,
        image_types: Optional[List[str]] = None
    ) -> Dict:
        """Run the complete optimization pipeline."""
        self.logger.info("=" * 70)
        self.logger.info("Starting Advanced UI/UX Image Optimization Pipeline")
        self.logger.info("=" * 70)
        
        # Collect or use existing images
        if generate_images:
            image_paths = self.collect_images(num_images, image_types)
        else:
            image_paths = list(self.folder_manager.original_dir.glob("*.png"))
            if not image_paths:
                raise ValueError("No images found in images_original directory")
        
        self.stats["total"] = len(image_paths)
        
        # Process each image
        for i, img_path in enumerate(image_paths, 1):
            image_id = f"{i:03d}"
            self.logger.info(f"\n--- Processing image {i}/{len(image_paths)} ---")
            
            result = self.process_single_image(img_path, image_id)
            self.metadata.append(result)
        
        # Generate final report
        report = self._generate_report()
        
        # Save metadata and report
        self._save_results(report)
        
        self.logger.info("\n" + "=" * 70)
        self.logger.info("Pipeline Complete")
        self.logger.info(f"Total: {self.stats['total']}")
        self.logger.info(f"Processed: {self.stats['processed']}")
        self.logger.info(f"Failed: {self.stats['failed']}")
        self.logger.info(f"Success Rate: {report['summary']['success_rate']}")
        self.logger.info("=" * 70)
        
        return report
    
    def _generate_report(self) -> Dict:
        """Generate comprehensive processing report."""
        success_rate = (
            (self.stats["processed"] / self.stats["total"] * 100)
            if self.stats["total"] > 0 else 0
        )
        
        # Calculate average metrics
        successful_images = [m for m in self.metadata if "metrics" in m]
        avg_metrics = {}
        if successful_images:
            avg_metrics = {
                "avg_brightness_improvement": sum(
                    m["metrics"].get("brightness_improvement", 0)
                    for m in successful_images
                ) / len(successful_images),
                "avg_contrast_improvement": sum(
                    m["metrics"].get("contrast_improvement", 0)
                    for m in successful_images
                ) / len(successful_images),
                "avg_sharpness_improvement": sum(
                    m["metrics"].get("sharpness_improvement", 0)
                    for m in successful_images
                ) / len(successful_images),
            }
        
        return {
            "summary": {
                "total_images": self.stats["total"],
                "processed": self.stats["processed"],
                "failed": self.stats["failed"],
                "success_rate": f"{success_rate:.2f}%"
            },
            "average_metrics": avg_metrics,
            "errors": self.stats["errors"]
        }
    
    def _save_results(self, report: Dict):
        """Save metadata and report to files."""
        # Save full metadata
        metadata_path = self.folder_manager.results_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                **report,
                "images": self.metadata
            }, f, indent=2, ensure_ascii=False)
        
        # Save summary report
        summary_path = self.folder_manager.results_dir / "summary.txt"
        with open(summary_path, 'w', encoding='utf-8') as f:
            f.write("UI/UX Image Optimization Pipeline - Summary Report\n")
            f.write("=" * 70 + "\n\n")
            f.write(f"Total Images: {report['summary']['total_images']}\n")
            f.write(f"Successfully Processed: {report['summary']['processed']}\n")
            f.write(f"Failed: {report['summary']['failed']}\n")
            f.write(f"Success Rate: {report['summary']['success_rate']}\n\n")
            
            if report.get("average_metrics"):
                f.write("Average Improvements:\n")
                for metric, value in report["average_metrics"].items():
                    f.write(f"  {metric}: {value:.2f}\n")
            
            if report.get("errors"):
                f.write(f"\nErrors ({len(report['errors'])}):\n")
                for error in report["errors"]:
                    f.write(f"  Image {error['image_id']}: {error['error']}\n")
        
        self.logger.info(f"Results saved to: {metadata_path}")
        self.logger.info(f"Summary saved to: {summary_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Advanced UI/UX Image Optimization Pipeline"
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=5,
        help="Number of images to generate/process (default: 5)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="output",
        help="Output directory (default: output)"
    )
    parser.add_argument(
        "--no-generate",
        action="store_true",
        help="Use existing images instead of generating new ones"
    )
    parser.add_argument(
        "--image-types",
        nargs="+",
        choices=["ui", "photo", "mixed"],
        help="Types of images to generate (default: all types)"
    )
    
    args = parser.parse_args()
    
    pipeline = AdvancedImagePipeline(output_dir=args.output_dir)
    
    try:
        report = pipeline.run_pipeline(
            num_images=args.num_images,
            generate_images=not args.no_generate,
            image_types=args.image_types
        )
        
        print(f"\n[SUCCESS] Pipeline completed successfully!")
        print(f"  Success Rate: {report['summary']['success_rate']}")
        
    except Exception as e:
        logging.error(f"Pipeline failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()

