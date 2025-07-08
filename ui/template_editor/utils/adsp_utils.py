"""
Utility functions for handling .adsp plugin files and extracting dimensions.
"""
import json
import os
from typing import Optional, Tuple


def load_adsp_file(file_path: str) -> Optional[dict]:
    """
    Load and parse an .adsp plugin file.
    
    Args:
        file_path: Path to the .adsp file
        
    Returns:
        Dictionary containing plugin data, or None if failed
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading .adsp file: {e}")
        return None


def get_plugin_aspect_ratio(file_path: str) -> Optional[float]:
    """
    Extract aspect ratio from .adsp plugin file.
    
    Args:
        file_path: Path to the .adsp file
        
    Returns:
        Aspect ratio (width/height) or None if failed
    """
    plugin_data = load_adsp_file(file_path)
    if not plugin_data:
        return None
    
    plugin_size = plugin_data.get('pluginSize')
    if not plugin_size or len(plugin_size) != 2:
        return None
    
    width, height = plugin_size
    if height == 0:
        return None
    
    return width / height


def get_plugin_dimensions(file_path: str) -> Optional[Tuple[int, int]]:
    """
    Extract dimensions from .adsp plugin file.
    
    Args:
        file_path: Path to the .adsp file
        
    Returns:
        Tuple of (width, height) or None if failed
    """
    plugin_data = load_adsp_file(file_path)
    if not plugin_data:
        return None
    
    plugin_size = plugin_data.get('pluginSize')
    if not plugin_size or len(plugin_size) != 2:
        return None
    
    return tuple(plugin_size)


def get_plugin_info(file_path: str) -> Optional[dict]:
    """
    Extract key plugin information from .adsp file.
    
    Args:
        file_path: Path to the .adsp file
        
    Returns:
        Dictionary with plugin info or None if failed
    """
    plugin_data = load_adsp_file(file_path)
    if not plugin_data:
        return None
    
    info = {}
    
    # Basic info
    info['name'] = plugin_data.get('pluginName', 'Unknown Plugin')
    info['title'] = plugin_data.get('pluginTitle', info['name'])
    info['version'] = plugin_data.get('pluginVersion', '1.0.0')
    
    # Dimensions and aspect ratio
    plugin_size = plugin_data.get('pluginSize')
    if plugin_size and len(plugin_size) == 2:
        width, height = plugin_size
        info['width'] = width
        info['height'] = height
        info['aspect_ratio'] = width / height if height > 0 else 1.0
        info['dimensions_text'] = f"{width}×{height}px"
    else:
        info['width'] = 700
        info['height'] = 400
        info['aspect_ratio'] = 1.75
        info['dimensions_text'] = "700×400px"
    
    return info


def find_adsp_files_in_directory(directory: str) -> list:
    """
    Find all .adsp files in a directory.
    
    Args:
        directory: Directory to search
        
    Returns:
        List of .adsp file paths
    """
    adsp_files = []
    
    if not os.path.exists(directory):
        return adsp_files
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith('.adsp'):
                adsp_files.append(os.path.join(root, file))
    
    return adsp_files


def get_default_plugin_aspect_ratios() -> dict:
    """
    Get common plugin aspect ratios as fallbacks.
    
    Returns:
        Dictionary of common plugin aspect ratios
    """
    return {
        'standard': 1.75,      # 700x400 (common)
        'wide': 2.0,           # 800x400 
        'square': 1.0,         # 400x400
        'tall': 0.8,           # 400x500
        'compact': 1.5,        # 600x400
        'euclyd': 700/400      # From the example file
    }
