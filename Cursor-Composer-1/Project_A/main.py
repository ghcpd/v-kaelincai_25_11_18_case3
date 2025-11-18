#!/usr/bin/env python3
"""
Project A: UI/UX Image Optimization Pipeline
Main entry point for image collection, enhancement, and output generation.
"""

import os
import json
import argparse
from pathlib import Path
from typing import List, Dict
from datetime import datetime

from image_generator import ImageGenerator
from uiux_enhancer import UIUXEnhancer
from comparison_generator import ComparisonGenerator
from utils import ensure_directories, setup_logging, log_info, log_error


class ImageOptimizationPipeline:
    """Main pipeline for UI/UX image optimization."""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.original_dir = self.output_dir / "images_original"
        self.optimized_dir = self.output_dir / "images_optimized"
        self.comparison_dir = self.output_dir / "images_comparison"
        self.results_dir = self.output_dir / "results"
        
        ensure_directories([
            self.original_dir,
            self.optimized_dir,
            self.comparison_dir,
            self.results_dir
        ])
        
        self.generator = ImageGenerator()
        self.enhancer = UIUXEnhancer()
        self.comparison_gen = ComparisonGenerator()
        self.metadata = []
        
    def generate_test_images(self, count: int = 5) -> List[str]:
        """Generate or collect test images."""
        log_info(f"Generating {count} test images...")
        image_paths = []
        
        for i in range(count):
            img_path = self.generator.generate_image(
                image_type="mixed",  # Can be "ui", "photo", "mixed"
                output_path=self.original_dir / f"input_{i+1:03d}.png"
            )
            image_paths.append(str(img_path))
            log_info(f"Generated image {i+1}/{count}: {img_path}")
        
        return image_paths
    
    def process_image(self, original_path: str, image_id: str) -> Dict:
        """Process a single image through the optimization pipeline."""
        try:
            original_path_obj = Path(original_path)
            if not original_path_obj.exists():
                raise FileNotFoundError(f"Image not found: {original_path}")
            
            # Generate output paths
            optimized_path = self.optimized_dir / f"input_{image_id}_optimized.png"
            comparison_path = self.comparison_dir / f"input_{image_id}_compare.png"
            
            # Perform UI/UX enhancement
            log_info(f"Enhancing image {image_id}...")
            enhanced_image = self.enhancer.enhance_image(str(original_path_obj))
            
            # Save optimized image
            enhanced_image.save(str(optimized_path))
            log_info(f"Saved optimized image: {optimized_path}")
            
            # Generate comparison image
            comparison_image = self.comparison_gen.create_comparison(
                str(original_path_obj),
                str(optimized_path)
            )
            comparison_image.save(str(comparison_path))
            log_info(f"Saved comparison image: {comparison_path}")
            
            # Create metadata entry
            metadata_entry = {
                "id": image_id,
                "original": f"images_original/input_{image_id}.png",
                "optimized": f"images_optimized/input_{image_id}_optimized.png",
                "comparison": f"images_comparison/input_{image_id}_compare.png",
                "notes": self.enhancer.get_enhancement_notes(),
                "timestamp": datetime.now().isoformat()
            }
            
            return metadata_entry
            
        except Exception as e:
            log_error(f"Error processing image {image_id}: {str(e)}")
            return {
                "id": image_id,
                "original": f"images_original/input_{image_id}.png",
                "optimized": None,
                "comparison": None,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def run_pipeline(self, num_images: int = 5, generate_images: bool = True):
        """Run the complete optimization pipeline."""
        log_info("=" * 60)
        log_info("Starting UI/UX Image Optimization Pipeline")
        log_info("=" * 60)
        
        # Generate or collect images
        if generate_images:
            image_paths = self.generate_test_images(num_images)
        else:
            # Use existing images in original_dir
            image_paths = list(self.original_dir.glob("*.png"))
            image_paths = [str(p) for p in image_paths]
        
        # Process each image
        processed_count = 0
        failed_count = 0
        
        for i, img_path in enumerate(image_paths, 1):
            image_id = f"{i:03d}"
            log_info(f"\nProcessing image {i}/{len(image_paths)}")
            
            result = self.process_image(img_path, image_id)
            self.metadata.append(result)
            
            if result.get("error"):
                failed_count += 1
            else:
                processed_count += 1
        
        # Save metadata
        metadata_path = self.results_dir / "metadata.json"
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump({
                "summary": {
                    "total_images": len(image_paths),
                    "processed": processed_count,
                    "failed": failed_count,
                    "success_rate": f"{(processed_count/len(image_paths)*100):.2f}%" if image_paths else "0%"
                },
                "images": self.metadata
            }, f, indent=2, ensure_ascii=False)
        
        log_info("\n" + "=" * 60)
        log_info("Pipeline Complete")
        log_info(f"Processed: {processed_count}/{len(image_paths)}")
        log_info(f"Failed: {failed_count}/{len(image_paths)}")
        log_info(f"Metadata saved to: {metadata_path}")
        log_info("=" * 60)
        
        return processed_count, failed_count


def main():
    parser = argparse.ArgumentParser(
        description="UI/UX Image Optimization Pipeline"
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
    
    args = parser.parse_args()
    
    setup_logging(args.output_dir)
    
    pipeline = ImageOptimizationPipeline(output_dir=args.output_dir)
    pipeline.run_pipeline(
        num_images=args.num_images,
        generate_images=not args.no_generate
    )


if __name__ == "__main__":
    main()

