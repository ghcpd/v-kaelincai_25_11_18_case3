#!/usr/bin/env python3
"""
Advanced UI/UX Enhancement Module
Implements sophisticated enhancement algorithms with quality metrics.
"""

import numpy as np
from PIL import Image, ImageEnhance, ImageFilter
import cv2
from typing import Dict, List
from pathlib import Path


class AdvancedUIUXEnhancer:
    """Advanced image enhancement with multiple algorithms."""
    
    def __init__(self):
        self.applied_enhancements = []
    
    def process_image(self, input_path: str, output_path: str) -> Dict:
        """
        Process image with advanced enhancements.
        
        Returns:
            Dictionary with success status and enhancement details
        """
        self.applied_enhancements = []
        
        try:
            # Load image
            img = Image.open(input_path)
            original_mode = img.mode
            
            # Convert to RGB for processing
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Apply enhancement pipeline
            img = self._adaptive_exposure_correction(img)
            img = self._advanced_color_harmonization(img)
            img = self._intelligent_noise_reduction(img)
            img = self._selective_sharpening(img)
            img = self._contrast_optimization(img)
            img = self._saturation_enhancement(img)
            img = self._white_balance_correction(img)
            
            # Convert back if needed
            if original_mode == 'RGBA':
                img = img.convert('RGBA')
            
            # Save enhanced image
            img.save(output_path, "PNG", optimize=True)
            
            return {
                "success": True,
                "enhancements": self.applied_enhancements.copy(),
                "output_path": output_path
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "enhancements": []
            }
    
    def _adaptive_exposure_correction(self, img: Image.Image) -> Image.Image:
        """Adaptive exposure correction based on image statistics."""
        img_array = np.array(img)
        
        # Calculate brightness
        brightness = np.mean(img_array)
        
        # Adaptive correction
        if brightness < 100:  # Too dark
            factor = 1.2
            self.applied_enhancements.append("brightness_boost")
        elif brightness > 200:  # Too bright
            factor = 0.9
            self.applied_enhancements.append("brightness_reduction")
        else:
            factor = 1.05
            self.applied_enhancements.append("exposure_normalization")
        
        enhancer = ImageEnhance.Brightness(img)
        return enhancer.enhance(factor)
    
    def _advanced_color_harmonization(self, img: Image.Image) -> Image.Image:
        """Advanced color harmonization using LAB color space."""
        img_array = np.array(img)
        
        # Convert to LAB
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Normalize a and b channels for color harmony
        a_mean = np.mean(a)
        b_mean = np.mean(b)
        
        # Slight adjustment towards neutral
        a = np.clip(a + (128 - a_mean) * 0.1, 0, 255).astype(np.uint8)
        b = np.clip(b + (128 - b_mean) * 0.1, 0, 255).astype(np.uint8)
        
        # Merge and convert back
        lab = cv2.merge([l, a, b])
        img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        img = Image.fromarray(img_array)
        self.applied_enhancements.append("color_harmonization")
        return img
    
    def _intelligent_noise_reduction(self, img: Image.Image) -> Image.Image:
        """Intelligent noise reduction preserving edges."""
        img_array = np.array(img)
        
        # Use non-local means denoising for better quality
        # Fallback to bilateral filter if NL-means is too slow
        if img_array.shape[0] * img_array.shape[1] < 1000000:  # Small images
            denoised = cv2.fastNlMeansDenoisingColored(
                img_array, None, 10, 10, 7, 21
            )
        else:
            denoised = cv2.bilateralFilter(img_array, 5, 50, 50)
        
        img = Image.fromarray(denoised)
        self.applied_enhancements.append("noise_reduction")
        return img
    
    def _selective_sharpening(self, img: Image.Image) -> Image.Image:
        """Selective sharpening focusing on important areas."""
        # Use unsharp mask for better control
        img_array = np.array(img)
        
        # Create blurred version
        blurred = cv2.GaussianBlur(img_array, (0, 0), 2.0)
        
        # Unsharp mask
        sharpened = cv2.addWeighted(img_array, 1.5, blurred, -0.5, 0)
        sharpened = np.clip(sharpened, 0, 255).astype(np.uint8)
        
        img = Image.fromarray(sharpened)
        self.applied_enhancements.append("selective_sharpening")
        return img
    
    def _contrast_optimization(self, img: Image.Image) -> Image.Image:
        """Optimize contrast using CLAHE."""
        img_array = np.array(img)
        
        # Convert to LAB
        lab = cv2.cvtColor(img_array, cv2.COLOR_RGB2LAB)
        l, a, b = cv2.split(lab)
        
        # Apply CLAHE to L channel
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
        l = clahe.apply(l)
        
        # Merge and convert back
        lab = cv2.merge([l, a, b])
        img_array = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
        
        img = Image.fromarray(img_array)
        self.applied_enhancements.append("contrast_optimization")
        return img
    
    def _saturation_enhancement(self, img: Image.Image) -> Image.Image:
        """Enhance saturation for modern look."""
        enhancer = ImageEnhance.Color(img)
        img = enhancer.enhance(1.15)  # Moderate saturation boost
        
        self.applied_enhancements.append("saturation_enhancement")
        return img
    
    def _white_balance_correction(self, img: Image.Image) -> Image.Image:
        """Correct white balance for natural colors."""
        img_array = np.array(img)
        
        # Calculate color temperature
        r_mean = np.mean(img_array[:, :, 0])
        g_mean = np.mean(img_array[:, :, 1])
        b_mean = np.mean(img_array[:, :, 2])
        
        # Normalize to gray world assumption
        gray_value = (r_mean + g_mean + b_mean) / 3
        
        if gray_value > 0:
            img_array[:, :, 0] = np.clip(
                img_array[:, :, 0] * (gray_value / max(r_mean, 1)), 0, 255
            )
            img_array[:, :, 1] = np.clip(
                img_array[:, :, 1] * (gray_value / max(g_mean, 1)), 0, 255
            )
            img_array[:, :, 2] = np.clip(
                img_array[:, :, 2] * (gray_value / max(b_mean, 1)), 0, 255
            )
        
        img = Image.fromarray(img_array.astype('uint8'))
        self.applied_enhancements.append("white_balance_correction")
        return img

