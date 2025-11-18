#!/usr/bin/env python3
"""
Metrics Calculator Module
Calculates quality improvement metrics for before/after comparison.
"""

import numpy as np
from PIL import Image
import cv2
from typing import Dict


class MetricsCalculator:
    """Calculates image quality metrics."""
    
    def calculate_improvement(self, original_path: str, optimized_path: str) -> Dict:
        """
        Calculate improvement metrics between original and optimized images.
        
        Returns:
            Dictionary with various quality metrics
        """
        original = np.array(Image.open(original_path).convert('RGB'))
        optimized = np.array(Image.open(optimized_path).convert('RGB'))
        
        metrics = {}
        
        # Brightness improvement
        orig_brightness = np.mean(original)
        opt_brightness = np.mean(optimized)
        metrics["brightness_improvement"] = opt_brightness - orig_brightness
        
        # Contrast improvement (standard deviation)
        orig_contrast = np.std(original)
        opt_contrast = np.std(optimized)
        metrics["contrast_improvement"] = opt_contrast - orig_contrast
        
        # Sharpness improvement (Laplacian variance)
        orig_gray = cv2.cvtColor(original, cv2.COLOR_RGB2GRAY)
        opt_gray = cv2.cvtColor(optimized, cv2.COLOR_RGB2GRAY)
        
        orig_sharpness = cv2.Laplacian(orig_gray, cv2.CV_64F).var()
        opt_sharpness = cv2.Laplacian(opt_gray, cv2.CV_64F).var()
        metrics["sharpness_improvement"] = opt_sharpness - orig_sharpness
        
        # Color variance (saturation indicator)
        orig_hsv = cv2.cvtColor(original, cv2.COLOR_RGB2HSV)
        opt_hsv = cv2.cvtColor(optimized, cv2.COLOR_RGB2HSV)
        
        orig_saturation = np.mean(orig_hsv[:, :, 1])
        opt_saturation = np.mean(opt_hsv[:, :, 1])
        metrics["saturation_improvement"] = opt_saturation - orig_saturation
        
        # Noise level (lower is better)
        orig_noise = self._estimate_noise(orig_gray)
        opt_noise = self._estimate_noise(opt_gray)
        metrics["noise_reduction"] = orig_noise - opt_noise
        
        return metrics
    
    def _estimate_noise(self, gray_image: np.ndarray) -> float:
        """Estimate noise level in grayscale image."""
        # Use median absolute deviation as noise estimator
        median = np.median(gray_image)
        mad = np.median(np.abs(gray_image - median))
        return float(mad)

