"""
Template editor utilities package.
"""

from .dimensions import (
    CONTENT_DIMENSIONS,
    get_content_dimensions,
    get_canvas_size,
    is_portrait,
    is_landscape,
    is_square
)

from .coordinates import (
    CoordinateTransform,
    zoom_at_point,
    calculate_fit_zoom
)

from .constraints import (
    apply_constraints,
    constrain_to_frame_bounds,
    constrain_resize,
    is_point_in_resize_handle,
    snap_to_grid
)

__all__ = [
    # Dimensions
    'CONTENT_DIMENSIONS',
    'get_content_dimensions',
    'get_canvas_size',
    'is_portrait',
    'is_landscape',
    'is_square',
    
    # Coordinates
    'CoordinateTransform',
    'zoom_at_point',
    'calculate_fit_zoom',
    
    # Constraints
    'apply_constraints',
    'constrain_to_frame_bounds',
    'constrain_resize',
    'is_point_in_resize_handle',
    'snap_to_grid'
]
