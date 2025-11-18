#!/usr/bin/env python3
"""
UI/UX Enhancement Module
Performs visual optimization: layout improvement, color harmonization, style consistency.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from typing import Tuple, List
import cv2


class UIUXEnhancer:
    """Enhances images for better UI/UX."""
    
    def __init__(self):
        self.enhancement_notes = []
        
    def enhance_image(self, image_path: str) -> Image.Image:
        """
        Apply UI/UX enhancements to an image.
        
        Args:
            image_path: Path to the input image
            
        Returns:
            Enhanced PIL Image
        """
        self.enhancement_notes = []
        
        # Load image
        img = Image.open(image_path)
        original_mode = img.mode
        
        # Convert to RGB if needed
        if img.mode != 'RGB':
            img = img.convert('RGB')
        
        # Apply enhancements
        img = self._improve_exposure(img)
        img = self._harmonize_colors(img)
        img = self._reduce_noise(img)
        img = self._enhance_clarity(img)
        img = self._normalize_contrast(img)
        img = self._apply_modern_styling(img)
        
        # Convert back to original mode if needed
        if original_mode != 'RGB' and original_mode in ['RGBA', 'LA', 'P']:
            # Preserve alpha channel if present
            if original_mode == 'RGBA':
                img = img.convert('RGBA')
        
        return img
    
    def _improve_exposure(self, img: Image.Image) -> Image.Image:
        """Improve image exposure and brightness."""
        enhancer = ImageEnhance.Brightness(img)
        img = enhancer.enhance(1.1)  # Slight brightness increase
        
        enhancer = ImageEnhance.Contrast(img)
        img = enhancer.enhance(1.15)  # Moderate contrast increase
        
        self.enhancement_notes.append("Improved exposure and contrast")
        return img
    
    def _harmonize_colors(self, img: Image.Image) -> Image.Image:
        """Harmonize color palette for consistency."""
        # Convert to numpy array
        pixels = np.array(img)
        
        # Calculate color statistics
        mean_r = np.mean(pixels[:, :, 0])
        mean_g = np.mean(pixels[:, :, 1])
        mean_b = np.mean(pixels[:, :, 2])
        
        # Normalize colors towards a balanced palette
        target_mean = (mean_r + mean_g + mean_b) / 3
        
        # Adjust each channel slightly towards balance
        pixels[:, :, 0] = np.clip(pixels[:, :, 0] * (target_mean / max(mean_r, 1)), 0, 255)
        pixels[:, :, 1] = np.clip(pixels[:, :, 1] * (target_mean / max(mean_g, 1)), 0, 255)
        pixels[:, :, 2] = np.clip(pixels[:, :, 2] * (target_mean / max(mean_b, 1)), 0, 255)
        
        img = Image.fromarray(pixels.astype('uint8'))
        self.enhancement_notes.append("Harmonized color palette")
        return img
    
    def _reduce_noise(self, img: Image.Image) -> Image.Image:
        """Reduce noise while preserving details."""
        # Use bilateral filter via OpenCV for better noise reduction
        img_array = np.array(img)
        img_array = cv2.bilateralFilter(img_array, 5, 50, 50)
        img = Image.fromarray(img_array)
        
        self.enhancement_notes.append("Reduced noise")
        return img
    
    def _enhance_clarity(self, img: Image.Image) -> Image.Image:
        """Enhance image clarity and sharpness."""
        enhancer = ImageEnhance.Sharpness(img)
        img = enhancer.enhance(1.2)  # Moderate sharpness increase
        
        self.enhancement_notes.append("Enhanced clarity")
        return img
    
    def _normalize_contrast(self, img: Image.Image) -> Image.Image:
        """Normalize contrast for better readability."""
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization) via OpenCV
        img_array = np.array(img)
        
        # Convert to LAB color space
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge channels and convert back
        lab = cv2.merge([l, a, b])
        img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        img = Image.fromarray(img_array)
        self.enhancement_notes.append("Normalized contrast")
        return img
    
    def _apply_modern_styling(self, img: Image.Image) -> Image.Image:
        """Apply modern UI styling elements."""
        # Slight saturation boost for modern look
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.1)
        
        self.enhancement_notes.append("Applied modern styling")
        return img
    
    def get_enhancement_notes(self) -> str:
        """Get description of applied enhancements."""
        return "; ".join(self.enhancement_notes) if self.enhancement_notes else "No enhancements applied"

