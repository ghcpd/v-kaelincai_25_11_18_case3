#!/usr/bin/env python3
"""
Advanced Image Collector Module
Generates diverse test images with configurable imperfections.
"""

import random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import numpy as np
from typing import Optional, List


class ImageCollector:
    """Advanced image collection and generation."""
    
    def __init__(self):
        self.modern_colors = {
            "primary": (59, 130, 246),      # Blue
            "secondary": (16, 185, 129),    # Green
            "accent": (245, 158, 11),       # Amber
            "danger": (239, 68, 68),        # Red
            "purple": (139, 92, 246),       # Purple
        }
        
        self.ui_patterns = [
            "dashboard",
            "landing_page",
            "form",
            "card_layout",
            "navigation"
        ]
    
    def generate_image(
        self,
        image_type: str = "mixed",
        output_path: Optional[Path] = None,
        width: int = 800,
        height: int = 600,
        add_imperfections: bool = True
    ) -> Path:
        """Generate a test image with optional imperfections."""
        if image_type == "ui":
            img = self._generate_advanced_ui(width, height)
        elif image_type == "photo":
            img = self._generate_realistic_photo(width, height)
        else:  # mixed
            img = self._generate_hybrid_image(width, height)
        
        if add_imperfections:
            img = self._apply_imperfections(img)
        
        if output_path:
            img.save(output_path, "PNG", optimize=True)
            return Path(output_path)
        else:
            return img
    
    def _generate_advanced_ui(self, width: int, height: int) -> Image.Image:
        """Generate advanced UI with modern design patterns."""
        pattern = random.choice(self.ui_patterns)
        
        if pattern == "dashboard":
            return self._create_dashboard_ui(width, height)
        elif pattern == "landing_page":
            return self._create_landing_page(width, height)
        elif pattern == "form":
            return self._create_form_ui(width, height)
        elif pattern == "card_layout":
            return self._create_card_layout(width, height)
        else:  # navigation
            return self._create_navigation_ui(width, height)
    
    def _create_dashboard_ui(self, width: int, height: int) -> Image.Image:
        """Create a dashboard-style UI."""
        img = Image.new('RGB', (width, height), color=(248, 250, 252))
        draw = ImageDraw.Draw(img)
        
        # Header with gradient effect - adjust for small images
        header_height = min(60, height // 2)
        header_color = random.choice(list(self.modern_colors.values()))
        for y in range(header_height):
            alpha = int(255 * (1 - y / max(header_height, 1)))
            color = tuple(int(min(255, c + (255 - c) * (1 - alpha/255))) for c in header_color)
            draw.rectangle([0, y, width, y+1], fill=color)
        
        # Sidebar - only draw if there's space
        if height > header_height and width > 100:
            sidebar_color = (30, 41, 59)
            sidebar_width = min(200, width // 3)
            draw.rectangle([0, header_height, sidebar_width, height], fill=sidebar_color)
        
        # Content area with cards - only draw if there's space
        if width > 300 and height > 200:
            card_y = header_height + 20
            for i in range(3):
                card_x = sidebar_width + 20 + (i % 2) * 280 if height > header_height and width > 200 else 20 + (i % 2) * 280
                card_y = header_height + 20 + (i // 2) * 180
            
            # Card with shadow effect
            card_color = (255, 255, 255)
            draw.rectangle([card_x, card_y, card_x+250, card_y+150], fill=card_color)
            draw.rectangle([card_x, card_y, card_x+250, card_y+150], outline=(226, 232, 240), width=1)
            
            # Card content
            try:
                font = ImageFont.truetype("arial.ttf", 14)
            except:
                font = ImageFont.load_default()
            
            draw.text((card_x+10, card_y+10), f"Card {i+1}", fill=(30, 41, 59), font=font)
        
        return img
    
    def _create_landing_page(self, width: int, height: int) -> Image.Image:
        """Create a landing page UI."""
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Hero section
        hero_color = random.choice(list(self.modern_colors.values()))
        draw.rectangle([0, 0, width, height//2], fill=hero_color)
        
        # Overlay text
        try:
            font_large = ImageFont.truetype("arial.ttf", 32)
            font_medium = ImageFont.truetype("arial.ttf", 16)
        except:
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
        
        draw.text((width//4, height//4), "Welcome", fill=(255, 255, 255), font=font_large)
        draw.text((width//4, height//4 + 50), "Landing Page Content", fill=(255, 255, 255), font=font_medium)
        
        # Features section
        feature_y = height//2 + 40
        for i in range(3):
            x = 50 + i * (width - 100) // 3
            draw.rectangle([x, feature_y, x+200, feature_y+100], outline=(200, 200, 200), width=2)
            draw.text((x+10, feature_y+10), f"Feature {i+1}", fill=(50, 50, 50), font=font_medium)
        
        return img
    
    def _create_form_ui(self, width: int, height: int) -> Image.Image:
        """Create a form UI."""
        img = Image.new('RGB', (width, height), color=(249, 250, 251))
        draw = ImageDraw.Draw(img)
        
        # Form container
        form_x = width//4
        form_y = 50
        form_w = width//2
        form_h = height - 100
        
        draw.rectangle([form_x, form_y, form_x+form_w, form_y+form_h], fill=(255, 255, 255))
        
        # Form fields
        try:
            font = ImageFont.truetype("arial.ttf", 12)
        except:
            font = ImageFont.load_default()
        
        field_y = form_y + 30
        for i in range(5):
            field_height = 35
            # Label
            draw.text((form_x+20, field_y), f"Field {i+1}:", fill=(75, 85, 99), font=font)
            # Input box
            draw.rectangle(
                [form_x+20, field_y+20, form_x+form_w-20, field_y+20+field_height],
                fill=(255, 255, 255),
                outline=(209, 213, 219),
                width=1
            )
            field_y += field_height + 30
        
        # Submit button
        btn_color = random.choice(list(self.modern_colors.values()))
        btn_y = form_y + form_h - 60
        draw.rectangle(
            [form_x+form_w-120, btn_y, form_x+form_w-20, btn_y+40],
            fill=btn_color
        )
        draw.text((form_x+form_w-100, btn_y+10), "Submit", fill=(255, 255, 255), font=font)
        
        return img
    
    def _create_card_layout(self, width: int, height: int) -> Image.Image:
        """Create a card-based layout."""
        img = Image.new('RGB', (width, height), color=(243, 244, 246))
        draw = ImageDraw.Draw(img)
        
        # Grid of cards - adjust for small images
        cols = min(3, max(1, width // 50))
        rows = min(2, max(1, height // 50))
        
        padding = min(20, width // 4, height // 4)
        spacing = min(10, width // 8, height // 8)
        
        if width > padding * 2 and height > padding * 2:
            card_w = max(10, (width - padding * 2 - spacing * (cols - 1)) // cols)
            card_h = max(10, (height - padding * 2 - spacing * (rows - 1)) // rows)
            
            for row in range(rows):
                for col in range(cols):
                    x = padding + col * (card_w + spacing)
                    y = padding + row * (card_h + spacing)
                    
                    # Ensure coordinates are valid
                    if x + card_w <= width and y + card_h <= height and card_w > 0 and card_h > 0:
                        card_color = (255, 255, 255)
                        draw.rectangle([x, y, x+card_w, y+card_h], fill=card_color)
                        draw.rectangle([x, y, x+card_w, y+card_h], outline=(229, 231, 235), width=1)
                        
                        # Card content
                        try:
                            font = ImageFont.truetype("arial.ttf", 16)
                        except:
                            font = ImageFont.load_default()
                        
                        draw.text((x+2, y+2), f"C{row*cols+col+1}", fill=(31, 41, 55), font=font)
        
        return img
    
    def _create_navigation_ui(self, width: int, height: int) -> Image.Image:
        """Create a navigation-focused UI."""
        img = Image.new('RGB', (width, height), color=(255, 255, 255))
        draw = ImageDraw.Draw(img)
        
        # Top navigation bar - adjust height for small images
        nav_height = min(60, height // 2)
        nav_color = (17, 24, 39)
        draw.rectangle([0, 0, width, nav_height], fill=nav_color)
        
        # Navigation items
        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()
        
        nav_items = ["Home", "About", "Services", "Contact"]
        item_width = width // len(nav_items)
        for i, item in enumerate(nav_items):
            x = i * item_width + item_width // 2
            draw.text((x-30, nav_height // 3), item, fill=(255, 255, 255), font=font)
        
        # Content area - only draw if there's space
        if height > nav_height:
            content_color = (249, 250, 251)
            draw.rectangle([0, nav_height, width, height], fill=content_color)
        
        return img
    
    def _generate_realistic_photo(self, width: int, height: int) -> Image.Image:
        """Generate a realistic photo-like image."""
        # Create base with natural gradients
        img = Image.new('RGB', (width, height))
        pixels = np.array(img, dtype=np.float32)
        
        # Sky gradient
        for y in range(height // 2):
            for x in range(width):
                blue = 135 + (y / (height//2)) * 50 + np.random.normal(0, 5)
                pixels[y, x] = [min(255, max(0, blue-20)), min(255, max(0, blue)), min(255, max(0, blue+30))]
        
        # Ground/foreground
        for y in range(height // 2, height):
            for x in range(width):
                green = 100 + np.random.normal(0, 15)
                brown = 80 + np.random.normal(0, 10)
                pixels[y, x] = [min(255, max(0, brown)), min(255, max(0, green)), min(255, max(0, brown-20))]
        
        img = Image.fromarray(pixels.astype('uint8'))
        
        # Add some objects
        draw = ImageDraw.Draw(img)
        for i in range(3):
            x = random.randint(50, width - 100)
            y = random.randint(height // 2, height - 100)
            size = random.randint(40, 100)
            color = (random.randint(50, 150), random.randint(100, 200), random.randint(50, 150))
            draw.ellipse([x, y, x+size, y+size], fill=color)
        
        return img
    
    def _generate_hybrid_image(self, width: int, height: int) -> Image.Image:
        """Generate a hybrid UI/photo image."""
        # Start with photo background
        img = self._generate_realistic_photo(width, height)
        
        # Add UI overlay - create overlay same size as base image
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.rectangle([0, 0, width, 200], fill=(0, 0, 0, 180))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        draw = ImageDraw.Draw(img)
        try:
            font = ImageFont.truetype("arial.ttf", 24)
        except:
            font = ImageFont.load_default()
        
        draw.text((30, 30), "Hybrid Content", fill=(255, 255, 255), font=font)
        
        return img
    
    def _apply_imperfections(self, img: Image.Image) -> Image.Image:
        """Apply various imperfections to simulate real-world issues."""
        # Add noise
        pixels = np.array(img)
        noise_strength = random.randint(5, 15)
        noise = np.random.randint(-noise_strength, noise_strength, pixels.shape, dtype=np.int16)
        pixels = np.clip(pixels.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        img = Image.fromarray(pixels)
        
        # Random blur
        if random.random() > 0.6:
            img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.3, 1.0)))
        
        # Slight color shift
        if random.random() > 0.5:
            enhancer = ImageEnhance.Color(img)
            img = enhancer.enhance(random.uniform(0.9, 1.1))
        
        # Exposure issues
        if random.random() > 0.7:
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(random.uniform(0.85, 1.15))
        
        return img

