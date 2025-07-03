"""
Utility functions for ReelForge application
"""

import os
import sys
from pathlib import Path
from typing import Optional, Any


def get_app_data_directory() -> Path:
    """Get application data directory"""
    if sys.platform == "win32":
        app_data = os.environ.get("APPDATA", "")
        return Path(app_data) / "ReelForge"
    elif sys.platform == "darwin":  # macOS
        home = Path.home()
        return home / "Library" / "Application Support" / "ReelForge"
    else:  # Linux and others
        home = Path.home()
        return home / ".config" / "ReelForge"


def ensure_directory(directory: Path) -> bool:
    """Ensure directory exists, create if needed"""
    try:
        directory.mkdir(parents=True, exist_ok=True)
        return True
    except Exception:
        return False


def safe_filename(filename: str) -> str:
    """Convert string to safe filename"""
    import re
    # Remove or replace unsafe characters
    safe_name = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Remove leading/trailing whitespace and dots
    safe_name = safe_name.strip('. ')
    # Ensure not empty
    if not safe_name:
        safe_name = "untitled"
    return safe_name


def get_unique_filename(directory: Path, base_name: str, extension: str = "") -> Path:
    """Get unique filename in directory"""
    if not extension.startswith('.') and extension:
        extension = '.' + extension
        
    target_path = directory / f"{base_name}{extension}"
    
    counter = 1
    while target_path.exists():
        target_path = directory / f"{base_name}_{counter}{extension}"
        counter += 1
        
    return target_path


def format_duration(seconds: Optional[float]) -> str:
    """Format duration in seconds to readable string"""
    if seconds is None:
        return "Unknown"
        
    try:
        total_seconds = int(seconds)
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60
        
        if hours > 0:
            return f"{hours:02d}:{minutes:02d}:{secs:02d}"
        else:
            return f"{minutes:02d}:{secs:02d}"
    except Exception:
        return "Unknown"


def validate_project_name(name: str) -> tuple[bool, str]:
    """Validate project name"""
    if not name or not name.strip():
        return False, "Project name cannot be empty"
        
    name = name.strip()
    
    if len(name) > 100:
        return False, "Project name must be less than 100 characters"
        
    # Check for invalid characters
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        if char in name:
            return False, f"Project name cannot contain: {invalid_chars}"
            
    return True, ""


class SingletonMeta(type):
    """Singleton metaclass"""
    _instances = {}
    
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
