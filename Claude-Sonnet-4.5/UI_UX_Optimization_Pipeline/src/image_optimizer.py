"""
UI/UX Image Optimizer Module
Performs visual enhancement on images focusing on layout, colors, clarity, and style consistency.
"""

import os
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import cv2
from typing import Optional, Dict, Tuple, List
import json


class UIUXOptimizer:
    """Optimizes images for better UI/UX appearance."""
    
    def __init__(self, output_dir: str = "images_optimized"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def optimize_image(self, input_path: str, output_filename: str) -> Optional[Dict]:
        """
        Optimize a single image for better UI/UX.
        
        Args:
            input_path: Path to the input image
            output_filename: Filename for the optimized output
            
        Returns:
            Dictionary with optimization metadata, or None if failed
        """
        try:
            # Load image
            img = Image.open(input_path)
            original_size = img.size
            original_format = img.format
            
            # Convert to RGB if necessary
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply optimization pipeline
            img = self._enhance_clarity(img)
            img = self._harmonize_colors(img)
            img = self._improve_layout(img)
            img = self._apply_style_consistency(img)
            img = self._denoise(img)
            
            # Save optimized image
            output_path = os.path.join(self.output_dir, output_filename)
            img.save(output_path, quality=95)
            
            metadata = {
                "input": input_path,
                "output": output_path,
                "original_size": original_size,
                "optimized_size": img.size,
                "original_format": original_format,
                "status": "success",
                "notes": self._generate_notes(original_size, img.size)
            }
            
            return metadata
            
        except Exception as e:
            return {
                "input": input_path,
                "output": None,
                "status": "failed",
                "error": str(e)
            }
    
    def _enhance_clarity(self, img: Image.Image) -> Image.Image:
        """Enhance image clarity and sharpness."""
        # Sharpen the image
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.3)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.1)
        
        return img
    
    def _harmonize_colors(self, img: Image.Image) -> Image.Image:
        """Harmonize colors for better visual consistency."""
        # Convert to numpy array for processing
        img_array = np.array(img)
        
        # Apply subtle color balance
        img_array = self._auto_white_balance(img_array)
        
        # Reduce color saturation if too harsh
        img = Image.fromarray(img_array)
        enhancer = ImageEnhance.Color(img)
        
        # Calculate average saturation
        hsv = img.convert('HSV')
        h, s, v = hsv.split()
        s_array = np.array(s)
        avg_saturation = np.mean(s_array)
        
        # If too saturated, reduce it
        if avg_saturation > 180:
            img = enhancer.enhance(0.7)
        elif avg_saturation < 50:
            img = enhancer.enhance(1.2)
        
        return img
    
    def _auto_white_balance(self, img_array: np.ndarray) -> np.ndarray:
        """Apply automatic white balance."""
        result = img_array.copy().astype(np.float32)
        
        for i in range(3):  # RGB channels
            channel = result[:, :, i]
            # Simple gray world assumption
            avg = np.mean(channel)
            if avg > 0:
                result[:, :, i] = np.clip(channel * (128 / avg), 0, 255)
        
        return result.astype(np.uint8)
    
    def _improve_layout(self, img: Image.Image) -> Image.Image:
        """Improve layout by adding consistent padding/margins."""
        width, height = img.size
        
        # Add padding for better spacing (5% on each side)
        padding_percent = 0.05
        padding_x = int(width * padding_percent)
        padding_y = int(height * padding_percent)
        
        # Create new image with padding
        new_width = width + 2 * padding_x
        new_height = height + 2 * padding_y
        
        # Use a neutral background color
        bg_color = self._get_dominant_background_color(img)
        new_img = Image.new('RGB', (new_width, new_height), bg_color)
        
        # Paste original image with padding
        new_img.paste(img, (padding_x, padding_y))
        
        return new_img
    
    def _get_dominant_background_color(self, img: Image.Image) -> Tuple[int, int, int]:
        """Get the dominant background color (from edges)."""
        # Sample edges
        width, height = img.size
        edge_pixels = []
        
        # Top and bottom edges
        for x in range(0, width, 10):
            edge_pixels.append(img.getpixel((x, 0)))
            edge_pixels.append(img.getpixel((x, height - 1)))
        
        # Left and right edges
        for y in range(0, height, 10):
            edge_pixels.append(img.getpixel((0, y)))
            edge_pixels.append(img.getpixel((width - 1, y)))
        
        # Calculate average
        avg_r = int(np.mean([p[0] for p in edge_pixels]))
        avg_g = int(np.mean([p[1] for p in edge_pixels]))
        avg_b = int(np.mean([p[2] for p in edge_pixels]))
        
        # Lighten the color slightly for better appearance
        avg_r = min(255, int(avg_r * 1.1))
        avg_g = min(255, int(avg_g * 1.1))
        avg_b = min(255, int(avg_b * 1.1))
        
        return (avg_r, avg_g, avg_b)
    
    def _apply_style_consistency(self, img: Image.Image) -> Image.Image:
        """Apply consistent styling (soft shadows, rounded aesthetics)."""
        # Apply subtle blur to harsh edges
        img = img.filter(ImageFilter.SMOOTH_MORE)
        
        # Apply subtle brightness adjustment
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.05)
        
        return img
    
    def _denoise(self, img: Image.Image) -> Image.Image:
        """Remove noise from the image."""
        # Convert to numpy array
        img_array = np.array(img)
        
        # Apply bilateral filter (preserves edges while denoising)
        denoised = cv2.bilateralFilter(img_array, 9, 75, 75)
        
        return Image.fromarray(denoised)
    
    def _generate_notes(self, original_size: Tuple[int, int], 
                       optimized_size: Tuple[int, int]) -> str:
        """Generate notes about the optimization."""
        notes = []
        
        notes.append("Enhanced clarity and sharpness")
        notes.append("Harmonized color palette")
        notes.append("Improved layout spacing")
        notes.append("Applied style consistency")
        notes.append("Reduced image noise")
        
        if optimized_size != original_size:
            notes.append(f"Adjusted dimensions from {original_size} to {optimized_size}")
        
        return "; ".join(notes)
    
    def optimize_batch(self, input_dir: str, file_pattern: str = "*.png") -> Dict:
        """
        Optimize all images in a directory.
        
        Args:
            input_dir: Directory containing input images
            file_pattern: Pattern to match files (default: *.png)
            
        Returns:
            Dictionary with batch processing results
        """
        import glob
        
        pattern = os.path.join(input_dir, file_pattern)
        input_files = glob.glob(pattern)
        
        results = {
            "total": len(input_files),
            "successful": 0,
            "failed": 0,
            "images": []
        }
        
        for input_path in input_files:
            filename = os.path.basename(input_path)
            base_name = os.path.splitext(filename)[0]
            output_filename = f"{base_name}_optimized.png"
            
            metadata = self.optimize_image(input_path, output_filename)
            
            if metadata and metadata["status"] == "success":
                results["successful"] += 1
            else:
                results["failed"] += 1
            
            results["images"].append(metadata)
        
        return results


class ComparisonGenerator:
    """Generates before/after comparison images."""
    
    def __init__(self, output_dir: str = "images_comparison"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def generate_comparison(self, original_path: str, optimized_path: str, 
                          output_filename: str) -> Optional[str]:
        """
        Generate a side-by-side comparison image.
        
        Args:
            original_path: Path to original image
            optimized_path: Path to optimized image
            output_filename: Filename for comparison output
            
        Returns:
            Path to comparison image, or None if failed
        """
        try:
            # Load images
            img_original = Image.open(original_path)
            img_optimized = Image.open(optimized_path)
            
            # Convert to RGB
            if img_original.mode != 'RGB':
                img_original = img_original.convert('RGB')
            if img_optimized.mode != 'RGB':
                img_optimized = img_optimized.convert('RGB')
            
            # Resize to same height for comparison
            max_height = max(img_original.height, img_optimized.height)
            
            if img_original.height != max_height:
                ratio = max_height / img_original.height
                new_width = int(img_original.width * ratio)
                img_original = img_original.resize((new_width, max_height), 
                                                   Image.Resampling.LANCZOS)
            
            if img_optimized.height != max_height:
                ratio = max_height / img_optimized.height
                new_width = int(img_optimized.width * ratio)
                img_optimized = img_optimized.resize((new_width, max_height), 
                                                     Image.Resampling.LANCZOS)
            
            # Create comparison image
            gap = 20
            label_height = 40
            total_width = img_original.width + gap + img_optimized.width
            total_height = max_height + label_height
            
            comparison = Image.new('RGB', (total_width, total_height), 'white')
            
            # Paste images
            comparison.paste(img_original, (0, label_height))
            comparison.paste(img_optimized, (img_original.width + gap, label_height))
            
            # Add labels
            from PIL import ImageDraw
            draw = ImageDraw.Draw(comparison)
            
            # Draw labels
            draw.rectangle([0, 0, img_original.width, label_height], 
                          fill='#3498db')
            draw.rectangle([img_original.width + gap, 0, total_width, label_height], 
                          fill='#2ecc71')
            
            draw.text((10, 10), "ORIGINAL", fill='white')
            draw.text((img_original.width + gap + 10, 10), "OPTIMIZED", fill='white')
            
            # Save comparison
            output_path = os.path.join(self.output_dir, output_filename)
            comparison.save(output_path, quality=95)
            
            return output_path
            
        except Exception as e:
            print(f"Failed to generate comparison: {e}")
            return None
    
    def generate_batch_comparisons(self, results: Dict) -> List[str]:
        """Generate comparisons for all successful optimizations."""
        comparison_paths = []
        
        for img_data in results["images"]:
            if img_data["status"] == "success":
                original = img_data["input"]
                optimized = img_data["output"]
                
                base_name = os.path.splitext(os.path.basename(original))[0]
                comparison_filename = f"{base_name}_comparison.png"
                
                comparison_path = self.generate_comparison(
                    original, optimized, comparison_filename
                )
                
                if comparison_path:
                    comparison_paths.append(comparison_path)
                    img_data["comparison"] = comparison_path
        
        return comparison_paths


def main():
    """Main optimization pipeline."""
    print("Starting UI/UX Image Optimization Pipeline...")
    
    # Initialize optimizer
    optimizer = UIUXOptimizer("images_optimized")
    
    # Optimize all images
    print("\nOptimizing images...")
    results = optimizer.optimize_batch("images_original", "*.png")
    
    print(f"\nOptimization Results:")
    print(f"  Total: {results['total']}")
    print(f"  Successful: {results['successful']}")
    print(f"  Failed: {results['failed']}")
    
    # Generate comparisons
    print("\nGenerating comparison images...")
    comparator = ComparisonGenerator("images_comparison")
    comparisons = comparator.generate_batch_comparisons(results)
    print(f"  Generated {len(comparisons)} comparison images")
    
    # Save results to JSON
    output_json = "results/optimization_results.json"
    os.makedirs("results", exist_ok=True)
    
    with open(output_json, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_json}")
    print("Pipeline completed successfully!")


if __name__ == "__main__":
    main()
