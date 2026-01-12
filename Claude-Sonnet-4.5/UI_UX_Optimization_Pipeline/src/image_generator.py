"""
Image Generator Module
Generates synthetic test images with various UI/UX issues for testing the optimization pipeline.
"""

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import random
import os
from typing import List, Tuple


class ImageGenerator:
    """Generates test images with UI/UX problems for optimization testing."""
    
    def __init__(self, output_dir: str = "images_original"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
    def generate_ui_screenshot_poor_spacing(self, filename: str) -> str:
        """Generate a UI screenshot with poor spacing and cluttered layout."""
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color='#f0f0f0')
        draw = ImageDraw.Draw(img)
        
        # Poor spacing - elements too close together
        colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        
        # Cluttered header with no padding
        draw.rectangle([0, 0, width, 60], fill='#2c3e50')
        draw.text((5, 5), "App Title", fill='white')  # Too close to edge
        
        # Buttons with inconsistent spacing
        button_y = 80
        for i in range(5):
            x = 20 + i * 140  # Uneven spacing
            draw.rectangle([x, button_y, x + 120, button_y + 40], 
                          fill=colors[i], outline='#34495e', width=2)
            draw.text((x + 10, button_y + 10), f"Button {i+1}", fill='white')
        
        # Content boxes with poor alignment
        for i in range(3):
            y = 150 + i * 130
            x = 30 + (i * 15)  # Misaligned
            draw.rectangle([x, y, x + 700, y + 100], 
                          fill='white', outline='#bdc3c7', width=1)
            draw.text((x + 5, y + 5), f"Content Block {i+1}\nPoorly spaced text", 
                     fill='#2c3e50')
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_ui_screenshot_bad_colors(self, filename: str) -> str:
        """Generate UI with inconsistent, clashing colors."""
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color='#ffff00')  # Harsh yellow
        draw = ImageDraw.Draw(img)
        
        # Clashing color combinations
        draw.rectangle([0, 0, width, 80], fill='#ff00ff')  # Magenta header
        draw.text((20, 20), "Inconsistent Design", fill='#00ff00')  # Green text
        
        # Random color boxes
        colors = ['#ff0000', '#00ff00', '#0000ff', '#ffff00', '#ff00ff', '#00ffff']
        for i in range(6):
            x = 50 + (i % 3) * 250
            y = 100 + (i // 3) * 200
            draw.rectangle([x, y, x + 200, y + 150], 
                          fill=colors[i], outline='#000000', width=3)
            draw.text((x + 10, y + 10), f"Box {i+1}", fill='white')
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_noisy_photo(self, filename: str) -> str:
        """Generate a photo with noise and poor clarity."""
        width, height = 640, 480
        
        # Create gradient background
        img = Image.new('RGB', (width, height))
        pixels = img.load()
        
        for y in range(height):
            for x in range(width):
                r = int(100 + (x / width) * 100)
                g = int(150 - (y / height) * 50)
                b = int(200 - (x / width) * 100)
                
                # Add noise
                noise = random.randint(-50, 50)
                r = max(0, min(255, r + noise))
                g = max(0, min(255, g + noise))
                b = max(0, min(255, b + noise))
                
                pixels[x, y] = (r, g, b)
        
        draw = ImageDraw.Draw(img)
        
        # Add some shapes to simulate content
        for _ in range(5):
            x1 = random.randint(50, width - 150)
            y1 = random.randint(50, height - 150)
            x2 = x1 + random.randint(50, 100)
            y2 = y1 + random.randint(50, 100)
            color = (random.randint(0, 255), random.randint(0, 255), 
                    random.randint(0, 255))
            draw.rectangle([x1, y1, x2, y2], fill=color, outline='white', width=2)
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_low_resolution_image(self, filename: str) -> str:
        """Generate a very low resolution image."""
        width, height = 160, 120  # Very small
        img = Image.new('RGB', (width, height), color='#ecf0f1')
        draw = ImageDraw.Draw(img)
        
        # Simple UI elements
        draw.rectangle([10, 10, 150, 40], fill='#3498db')
        draw.rectangle([10, 50, 150, 80], fill='#e74c3c')
        draw.rectangle([10, 90, 150, 110], fill='#2ecc71')
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_very_large_image(self, filename: str) -> str:
        """Generate a very large resolution image."""
        width, height = 3840, 2160  # 4K
        img = Image.new('RGB', (width, height), color='#34495e')
        draw = ImageDraw.Draw(img)
        
        # Create a grid pattern
        grid_size = 100
        for x in range(0, width, grid_size):
            draw.line([(x, 0), (x, height)], fill='#7f8c8d', width=2)
        for y in range(0, height, grid_size):
            draw.line([(0, y), (width, y)], fill='#7f8c8d', width=2)
        
        # Add some content
        draw.rectangle([width//4, height//4, 3*width//4, 3*height//4], 
                      fill='#2c3e50', outline='#ecf0f1', width=10)
        draw.text((width//2 - 200, height//2), "Large Image Test", 
                 fill='white')
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_mixed_marketing_banner(self, filename: str) -> str:
        """Generate a marketing banner with style inconsistencies."""
        width, height = 1200, 400
        img = Image.new('RGB', (width, height))
        
        # Create gradient background (left to right)
        for x in range(width):
            for y in range(height):
                r = int(255 * (x / width))
                g = int(150 + 105 * (1 - x / width))
                b = int(200 * (y / height))
                img.putpixel((x, y), (r, g, b))
        
        draw = ImageDraw.Draw(img)
        
        # Inconsistent text styles
        draw.rectangle([50, 50, 350, 150], fill='white', outline='black', width=3)
        draw.text((70, 80), "SALE!", fill='red')
        
        draw.rectangle([400, 50, 800, 150], fill='#000000')
        draw.text((420, 80), "Premium Quality", fill='yellow')
        
        draw.rectangle([850, 50, 1150, 150], fill='#ff6b6b')
        draw.text((870, 80), "Buy Now", fill='white')
        
        # Add noise to bottom section
        for x in range(width):
            for y in range(200, height):
                pixel = img.getpixel((x, y))
                noise = random.randint(-30, 30)
                new_pixel = tuple(max(0, min(255, c + noise)) for c in pixel)
                img.putpixel((x, y), new_pixel)
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_invalid_image(self, filename: str) -> str:
        """Generate a corrupted/invalid image file."""
        filepath = os.path.join(self.output_dir, filename)
        
        # Write random binary data
        with open(filepath, 'wb') as f:
            f.write(b'INVALID_IMAGE_DATA_' + os.urandom(100))
        
        return filepath
    
    def generate_empty_image(self, filename: str) -> str:
        """Generate an empty/blank image."""
        width, height = 800, 600
        img = Image.new('RGB', (width, height), color='white')
        
        filepath = os.path.join(self.output_dir, filename)
        img.save(filepath)
        return filepath
    
    def generate_all_test_images(self) -> List[Tuple[str, str]]:
        """Generate all test images and return list of (type, filepath) tuples."""
        test_images = []
        
        # Normal flows
        test_images.append(("normal_ui_poor_spacing", 
                          self.generate_ui_screenshot_poor_spacing("input_001.png")))
        test_images.append(("normal_ui_bad_colors", 
                          self.generate_ui_screenshot_bad_colors("input_002.png")))
        test_images.append(("normal_noisy_photo", 
                          self.generate_noisy_photo("input_003.png")))
        
        # Edge cases
        test_images.append(("edge_low_resolution", 
                          self.generate_low_resolution_image("input_004.png")))
        test_images.append(("edge_marketing_banner", 
                          self.generate_mixed_marketing_banner("input_005.png")))
        
        # Boundary cases
        test_images.append(("boundary_very_large", 
                          self.generate_very_large_image("input_006.png")))
        test_images.append(("boundary_empty", 
                          self.generate_empty_image("input_007.png")))
        
        # Invalid inputs
        test_images.append(("invalid_corrupted", 
                          self.generate_invalid_image("input_008.dat")))
        
        # Additional mixed types
        test_images.append(("mixed_ui_photo", 
                          self.generate_ui_screenshot_poor_spacing("input_009.png")))
        test_images.append(("mixed_noisy_ui", 
                          self.generate_noisy_photo("input_010.png")))
        
        return test_images


def main():
    """Generate all test images."""
    generator = ImageGenerator()
    images = generator.generate_all_test_images()
    
    print(f"Generated {len(images)} test images:")
    for img_type, filepath in images:
        print(f"  - {img_type}: {filepath}")


if __name__ == "__main__":
    main()
