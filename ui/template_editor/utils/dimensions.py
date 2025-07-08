"""
Content type dimensions and aspect ratios for ReelTune templates.
"""

CONTENT_DIMENSIONS = {
    "reel": {
        "width": 1080,
        "height": 1920,
        "name": "Instagram Reel (9:16)",
        "aspect_ratio": 9/16,
        "has_timeline": True
    },
    "story": {
        "width": 1080, 
        "height": 1920,
        "name": "Instagram Story (9:16)",
        "aspect_ratio": 9/16,
        "has_timeline": True
    },
    "post": {
        "width": 1080,
        "height": 1080, 
        "name": "Instagram Post (1:1)",
        "aspect_ratio": 1.0,
        "has_timeline": False
    },
    "tutorial": {
        "width": 1920,
        "height": 1080,
        "name": "YouTube Tutorial (16:9)",
        "aspect_ratio": 16/9,
        "has_timeline": True
    }
}

def get_content_dimensions(content_type: str) -> dict:
    """Get dimensions for a content type."""
    return CONTENT_DIMENSIONS.get(content_type.lower(), CONTENT_DIMENSIONS["reel"])

def get_canvas_size(content_type: str, scale_factor: float = 1.0) -> tuple[int, int]:
    """Get scaled canvas size for content type."""
    dims = get_content_dimensions(content_type)
    # Scale to fit in UI while maintaining aspect ratio
    base_height = 400
    aspect = dims["aspect_ratio"]
    
    if aspect < 1.0:  # Portrait (9:16)
        height = int(base_height * scale_factor)
        width = int(height * aspect)
    else:  # Landscape or square
        width = int(base_height * aspect * scale_factor)
        height = int(base_height * scale_factor)
    
    return width, height

def is_portrait(content_type: str) -> bool:
    """Check if content type is portrait orientation."""
    dims = get_content_dimensions(content_type)
    return dims["aspect_ratio"] < 1.0

def is_landscape(content_type: str) -> bool:
    """Check if content type is landscape orientation."""
    dims = get_content_dimensions(content_type)
    return dims["aspect_ratio"] > 1.0

def is_square(content_type: str) -> bool:
    """Check if content type is square."""
    dims = get_content_dimensions(content_type)
    return abs(dims["aspect_ratio"] - 1.0) < 0.01
