#!/usr/bin/env python3
"""
Folder Management Module
Handles directory structure creation and management.
"""

from pathlib import Path
from typing import List


class FolderManager:
    """Manages output folder structure."""
    
    def __init__(self, base_output_dir: str = "output"):
        self.base_dir = Path(base_output_dir)
        self.original_dir = self.base_dir / "images_original"
        self.optimized_dir = self.base_dir / "images_optimized"
        self.comparison_dir = self.base_dir / "images_comparison"
        self.results_dir = self.base_dir / "results"
        
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure all required directories exist."""
        directories = [
            self.original_dir,
            self.optimized_dir,
            self.comparison_dir,
            self.results_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_structure(self) -> dict:
        """Get folder structure information."""
        return {
            "base": str(self.base_dir),
            "original": str(self.original_dir),
            "optimized": str(self.optimized_dir),
            "comparison": str(self.comparison_dir),
            "results": str(self.results_dir)
        }
    
    def verify_structure(self) -> List[str]:
        """Verify folder structure and return any missing directories."""
        missing = []
        
        if not self.original_dir.exists():
            missing.append(str(self.original_dir))
        if not self.optimized_dir.exists():
            missing.append(str(self.optimized_dir))
        if not self.comparison_dir.exists():
            missing.append(str(self.comparison_dir))
        if not self.results_dir.exists():
            missing.append(str(self.results_dir))
        
        return missing

