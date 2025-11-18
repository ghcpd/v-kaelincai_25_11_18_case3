#!/usr/bin/env python3
"""
Image Generator Module
Generates synthetic UI screenshots, app interfaces, and photos for testing.
"""

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import numpy as np
from typing import Optional


class ImageGenerator:
    """Generates test images for UI/UX optimization."""
    
    def __init__(self):
        self.ui_colors = [
            (52, 152, 219),   # Blue
            (46, 204, 113),   # Green
            (241, 196, 15),   # Yellow
            (231, 76, 60),    # Red
            (155, 89, 182),   # Purple
        ]
        
    def generate_image(
        self,
        image_type: str = "mixed",
        output_path: Optional[Path] = None,
        width: int = 800,
        height: int = 600
    ) -> Path:
        """
        Generate a test image.
        
        Args:
            image_type: "ui", "photo", or "mixed"
            output_path: Path to save the image
            width: Image width
            height: Image height
        """
        if image_type == "ui":
            img = self._generate_ui_screenshot(width, height)
        elif image_type == "photo":
            img = self._generate_photo(width, height)
        else:  # mixed
            img = self._generate_mixed_image(width, height)
        
        # Add some imperfections (noise, compression artifacts, etc.)
        img = self._add_imperfections(img)
        
        if output_path:
            img.save(output_path, "PNG")
            return Path(output_path)
        else:
            return img
    
    def _generate_ui_screenshot(self, width: int, height: int) -> Image.Image:
        """Generate a synthetic UI screenshot with layout issues."""
        img = Image.new('RGB', (width, height), color=(240, 240, 240))
        draw = ImageDraw.Draw(img)
        
        # Inconsistent header
        header_color = random.choice(self.ui_colors)
        draw.rectangle([0, 0, width, 80], fill=header_color)
        
        # Cluttered text
        try:
            font_large = ImageFont.truetype("arial.ttf", 24)
            font_medium = ImageFont.truetype("arial.ttf", 16)
            font_small = ImageFont.truetype("arial.ttf", 12)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Inconsistent spacing
        y_positions = [20, 50, 100, 130, 160, 200, 230, 280, 320]
        for i, y in enumerate(y_positions):
            if y < height - 20:
                text_color = random.choice([(0, 0, 0), (50, 50, 50), (100, 100, 100)])
                draw.text((20 + random.randint(-5, 5), y), 
                         f"UI Element {i+1}", fill=text_color, font=font_medium)
        
        # Random buttons with inconsistent styling
        for i in range(3):
            x = 50 + i * 200 + random.randint(-10, 10)
            y = 400 + random.randint(-5, 5)
            w = 150 + random.randint(-20, 20)
            h = 40 + random.randint(-5, 5)
            btn_color = random.choice(self.ui_colors)
            draw.rectangle([x, y, x+w, y+h], fill=btn_color, outline=(0, 0, 0), width=2)
            draw.text((x+20, y+10), f"Button {i+1}", fill=(255, 255, 255), font=font_small)
        
        return img
    
    def _generate_photo(self, width: int, height: int) -> Image.Image:
        """Generate a synthetic photo with noise and exposure issues."""
        # Create base image with gradient
        img = Image.new('RGB', (width, height))
        pixels = np.array(img)
        
        # Create gradient background
        for y in range(height):
            for x in range(width):
                r = int(100 + (y / height) * 100 + random.randint(-20, 20))
                g = int(120 + (x / width) * 80 + random.randint(-20, 20))
                b = int(140 + random.randint(-30, 30))
                pixels[y, x] = [max(0, min(255, r)), max(0, min(255, g)), max(0, min(255, b))]
        
        img = Image.fromarray(pixels.astype('uint8'))
        
        # Add some shapes to simulate objects
        draw = ImageDraw.Draw(img)
        for i in range(5):
            x = random.randint(50, width - 100)
            y = random.randint(50, height - 100)
            size = random.randint(30, 80)
            color = (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))
            draw.ellipse([x, y, x+size, y+size], fill=color)
        
        return img
    
    def _generate_mixed_image(self, width: int, height: int) -> Image.Image:
        """Generate a mixed image combining UI and photo elements."""
        # Start with photo-like background
        img = self._generate_photo(width, height)
        draw = ImageDraw.Draw(img)
        
        # Add UI overlay elements - create overlay same size as base image
        overlay_color = random.choice(self.ui_colors)
        overlay_alpha = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay_alpha)
        overlay_draw.rectangle([0, 0, width, 150], fill=overlay_color + (180,))
        img = Image.alpha_composite(img.convert('RGBA'), overlay_alpha).convert('RGB')
        draw = ImageDraw.Draw(img)
        
        # Add text overlay
        try:
            font = ImageFont.truetype("arial.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        draw.text((20, 20), "Mixed Content", fill=(255, 255, 255), font=font)
        
        return img
    
    def _add_imperfections(self, img: Image.Image) -> Image.Image:
        """Add imperfections like noise, compression artifacts, etc."""
        # Add slight noise
        pixels = np.array(img)
        noise = np.random.randint(-10, 10, pixels.shape, dtype=np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
        
        # Slight blur to simulate compression
        if random.random() > 0.5:
            img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
        
        return img

