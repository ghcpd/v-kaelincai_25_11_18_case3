#!/usr/bin/env python3
"""
Comparison Builder Module
Creates enhanced comparison images with annotations.
"""

from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
from typing import Optional


class ComparisonBuilder:
    """Builds comparison images with enhanced features."""
    
    def __init__(self):
        self.padding = 30
        self.label_height = 50
        self.font_size = 18
        self.border_width = 2
    
    def build_comparison(
        self,
        original_path: str,
        optimized_path: str,
        output_path: str
    ) -> Image.Image:
        """
        Build an enhanced comparison image.
        
        Args:
            original_path: Path to original image
            optimized_path: Path to optimized image
            output_path: Path to save comparison
            
        Returns:
            Comparison PIL Image
        """
        # Load images
        original = Image.open(original_path)
        optimized = Image.open(optimized_path)
        
        # Resize to same height
        target_height = max(original.height, optimized.height)
        if original.height != target_height:
            original = self._resize_proportional(original, target_height)
        if optimized.height != target_height:
            optimized = self._resize_proportional(optimized, target_height)
        
        # Calculate canvas size
        image_width = max(original.width, optimized.width)
        total_width = image_width * 2 + self.padding * 3
        total_height = target_height + self.label_height + self.padding * 2
        
        # Create canvas
        comparison = Image.new('RGB', (total_width, total_height), color=(245, 245, 245))
        draw = ImageDraw.Draw(comparison)
        
        # Calculate positions
        orig_x = self.padding
        opt_x = orig_x + image_width + self.padding
        y_offset = self.padding + self.label_height
        
        # Center images if different widths
        orig_y_offset = (image_width - original.width) // 2
        opt_y_offset = (image_width - optimized.width) // 2
        
        # Paste images
        comparison.paste(original, (orig_x + orig_y_offset, y_offset))
        comparison.paste(optimized, (opt_x + opt_y_offset, y_offset))
        
        # Add labels with background
        try:
            font = ImageFont.truetype("arial.ttf", self.font_size)
            font_bold = ImageFont.truetype("arial.ttf", self.font_size)
        except:
            font = ImageFont.load_default()
            font_bold = ImageFont.load_default()
        
        label_y = self.padding // 2
        
        # Original label
        label_bg_color = (220, 220, 220)
        label_text_color = (80, 80, 80)
        draw.rectangle(
            [orig_x, label_y, orig_x + image_width, label_y + self.label_height - 10],
            fill=label_bg_color
        )
        draw.text(
            (orig_x + image_width // 2 - 40, label_y + 10),
            "Original",
            fill=label_text_color,
            font=font
        )
        
        # Optimized label
        label_bg_color_opt = (200, 230, 200)
        label_text_color_opt = (30, 120, 30)
        draw.rectangle(
            [opt_x, label_y, opt_x + image_width, label_y + self.label_height - 10],
            fill=label_bg_color_opt
        )
        draw.text(
            (opt_x + image_width // 2 - 50, label_y + 10),
            "Optimized",
            fill=label_text_color_opt,
            font=font
        )
        
        # Add divider line
        divider_x = orig_x + image_width + self.padding // 2
        draw.line(
            [(divider_x, y_offset - 5), (divider_x, y_offset + target_height + 5)],
            fill=(180, 180, 180),
            width=self.border_width
        )
        
        # Add border around comparison
        draw.rectangle(
            [0, 0, total_width - 1, total_height - 1],
            outline=(150, 150, 150),
            width=self.border_width
        )
        
        # Save
        comparison.save(output_path, "PNG", optimize=True)
        return comparison
    
    def _resize_proportional(self, img: Image.Image, target_height: int) -> Image.Image:
        """Resize image proportionally to target height."""
        ratio = target_height / img.height
        new_width = int(img.width * ratio)
        return img.resize((new_width, target_height), Image.Resampling.LANCZOS)

