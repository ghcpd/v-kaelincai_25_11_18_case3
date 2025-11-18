#!/usr/bin/env python3
"""
Comparison Image Generator
Creates side-by-side before/after comparison images.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional


class ComparisonGenerator:
    """Generates before/after comparison images."""
    
    def __init__(self):
        self.label_font_size = 20
        self.padding = 20
        self.label_height = 40
        
    def create_comparison(
        self,
        original_path: str,
        optimized_path: str,
        output_path: Optional[str] = None
    ) -> Image.Image:
        """
        Create a side-by-side comparison image.
        
        Args:
            original_path: Path to original image
            optimized_path: Path to optimized image
            output_path: Optional path to save comparison
            
        Returns:
            Comparison PIL Image
        """
        # Load images
        original = Image.open(original_path)
        optimized = Image.open(optimized_path)
        
        # Resize to same height if needed
        target_height = max(original.height, optimized.height)
        if original.height != target_height:
            original = self._resize_proportional(original, target_height)
        if optimized.height != target_height:
            optimized = self._resize_proportional(optimized, target_height)
        
        # Create comparison canvas
        total_width = original.width + optimized.width + self.padding * 3
        total_height = target_height + self.label_height + self.padding * 2
        
        comparison = Image.new('RGB', (total_width, total_height), color=(255, 255, 255))
        
        # Paste images
        x_offset = self.padding
        y_offset = self.padding + self.label_height
        comparison.paste(original, (x_offset, y_offset))
        comparison.paste(optimized, (x_offset + original.width + self.padding, y_offset))
        
        # Add labels
        draw = ImageDraw.Draw(comparison)
        try:
            font = ImageFont.truetype("arial.ttf", self.label_font_size)
        except:
            font = ImageFont.load_default()
        
        # Original label
        label_y = self.padding // 2
        draw.text(
            (x_offset, label_y),
            "Original",
            fill=(100, 100, 100),
            font=font
        )
        
        # Optimized label
        draw.text(
            (x_offset + original.width + self.padding, label_y),
            "Optimized",
            fill=(50, 150, 50),
            font=font
        )
        
        # Add divider line
        divider_x = x_offset + original.width + self.padding // 2
        draw.line(
            [(divider_x, y_offset), (divider_x, y_offset + target_height)],
            fill=(200, 200, 200),
            width=2
        )
        
        if output_path:
            comparison.save(output_path)
        
        return comparison
    
    def _resize_proportional(self, img: Image.Image, target_height: int) -> Image.Image:
        """Resize image proportionally to target height."""
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        return img.resize((new_width, target_height), Image.Resampling.LANCZOS)

