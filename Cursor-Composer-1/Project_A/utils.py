#!/usr/bin/env python3
"""
Utility functions for the image optimization pipeline.
"""

import os
import logging
from pathlib import Path
from typing import List


def ensure_directories(directories: List[Path]):
    """Ensure all specified directories exist."""
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


def setup_logging(output_dir: str):
    """Setup logging configuration."""
    log_dir = Path(output_dir) / "results"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    log_file = log_dir / "pipeline.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )


def log_info(message: str):
    """Log an info message."""
    logging.info(message)


def log_error(message: str):
    """Log an error message."""
    logging.error(message)


def log_warning(message: str):
    """Log a warning message."""
    logging.warning(message)

