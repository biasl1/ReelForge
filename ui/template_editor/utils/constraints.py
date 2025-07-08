"""
Element constraint logic for template editor.
"""
from PyQt6.QtCore import QRectF, QRect, QSizeF
from typing import Tuple, Union


def apply_constraints(
    element_rect: Union[QRect, QRectF],
    content_frame: Union[QRect, QRectF],
    constrain_to_frame: bool,
    maintain_aspect_ratio: bool = False,
    min_size: Tuple[int, int] = (20, 20)
) -> QRect:
    """
    Apply positioning and sizing constraints to an element.
    
    Args:
        element_rect: The desired element rectangle
        content_frame: The content frame boundaries
        constrain_to_frame: Whether to constrain element to frame
        maintain_aspect_ratio: Whether to maintain aspect ratio during resize
        min_size: Minimum allowed size (width, height)
    
    Returns:
        Constrained rectangle as QRect
    """
    # Convert to QRect for consistency
    if isinstance(element_rect, QRectF):
        result_rect = QRect(
            int(element_rect.x()), int(element_rect.y()),
            int(element_rect.width()), int(element_rect.height())
        )
    else:
        result_rect = QRect(element_rect)
    
    if isinstance(content_frame, QRectF):
        frame_rect = QRect(
            int(content_frame.x()), int(content_frame.y()),
            int(content_frame.width()), int(content_frame.height())
        )
    else:
        frame_rect = QRect(content_frame)
    
    # Apply minimum size constraints
    min_w, min_h = min_size
    if result_rect.width() < min_w:
        result_rect.setWidth(min_w)
    if result_rect.height() < min_h:
        result_rect.setHeight(min_h)
    
    # Apply frame constraints if enabled
    if constrain_to_frame:
        result_rect = constrain_to_frame_bounds(result_rect, frame_rect)
    
    return result_rect


def constrain_to_frame_bounds(element_rect: QRect, content_frame: QRect) -> QRect:
    """
    Constrain element rectangle to stay within content frame bounds.
    """
    result_rect = QRect(element_rect)
    
    # Constrain size to not exceed frame
    max_width = content_frame.width()
    max_height = content_frame.height()
    
    if result_rect.width() > max_width:
        result_rect.setWidth(max_width)
    if result_rect.height() > max_height:
        result_rect.setHeight(max_height)
    
    # Constrain position to keep element inside frame
    if result_rect.left() < content_frame.left():
        result_rect.moveLeft(content_frame.left())
    if result_rect.top() < content_frame.top():
        result_rect.moveTop(content_frame.top())
    if result_rect.right() > content_frame.right():
        result_rect.moveRight(content_frame.right())
    if result_rect.bottom() > content_frame.bottom():
        result_rect.moveBottom(content_frame.bottom())
    
    return result_rect


def constrain_resize(
    original_rect: QRect,
    new_rect: QRect,
    content_frame: QRect,
    constrain_to_frame: bool,
    maintain_aspect_ratio: bool = False,
    corner: str = "bottom-right"
) -> QRect:
    """
    Constrain resize operation based on settings.
    
    Args:
        original_rect: Original element rectangle
        new_rect: Desired new rectangle
        content_frame: Content frame bounds
        constrain_to_frame: Whether to constrain to frame
        maintain_aspect_ratio: Whether to maintain aspect ratio
        corner: Which corner is being dragged
    
    Returns:
        Constrained rectangle
    """
    result_rect = QRect(new_rect)
    
    # Maintain aspect ratio if requested
    if maintain_aspect_ratio and original_rect.width() > 0 and original_rect.height() > 0:
        original_aspect = original_rect.width() / original_rect.height()
        
        if corner in ["bottom-right", "top-left"]:
            # Use width to determine height
            new_height = result_rect.width() / original_aspect
            if corner == "bottom-right":
                result_rect.setHeight(int(new_height))
            else:  # top-left
                old_bottom = result_rect.bottom()
                result_rect.setHeight(int(new_height))
                result_rect.moveBottom(old_bottom)
        else:
            # Use height to determine width
            new_width = result_rect.height() * original_aspect
            if corner in ["bottom-left", "top-right"]:
                result_rect.setWidth(int(new_width))
    
    # Apply other constraints
    return apply_constraints(result_rect, content_frame, constrain_to_frame)


def is_point_in_resize_handle(point: QRect, element_rect: QRect, handle_size: int = 8) -> str:
    """
    Check if point is in a resize handle and return handle type.
    
    Returns:
        Handle type: "top-left", "top-right", "bottom-left", "bottom-right", or ""
    """
    handles = {
        "top-left": QRect(
            element_rect.left() - handle_size//2,
            element_rect.top() - handle_size//2,
            handle_size, handle_size
        ),
        "top-right": QRect(
            element_rect.right() - handle_size//2,
            element_rect.top() - handle_size//2,
            handle_size, handle_size
        ),
        "bottom-left": QRect(
            element_rect.left() - handle_size//2,
            element_rect.bottom() - handle_size//2,
            handle_size, handle_size
        ),
        "bottom-right": QRect(
            element_rect.right() - handle_size//2,
            element_rect.bottom() - handle_size//2,
            handle_size, handle_size
        )
    }
    
    for handle_type, handle_rect in handles.items():
        if handle_rect.contains(point):
            return handle_type
    
    return ""


def snap_to_grid(rect: QRect, grid_size: int = 10) -> QRect:
    """Snap rectangle position to grid."""
    if grid_size <= 0:
        return rect
    
    snapped_rect = QRect(rect)
    
    # Snap position
    snapped_x = round(rect.x() / grid_size) * grid_size
    snapped_y = round(rect.y() / grid_size) * grid_size
    snapped_rect.moveTo(snapped_x, snapped_y)
    
    return snapped_rect
