"""
Coordinate transformation utilities for zoom and pan functionality.
"""
from PyQt6.QtCore import QPointF, QRectF
from typing import Tuple


class CoordinateTransform:
    """Handles coordinate transformations for zoom and pan operations."""
    
    def __init__(self):
        self.zoom_factor = 1.0
        self.pan_offset = QPointF(0, 0)
        self.min_zoom = 0.1
        self.max_zoom = 5.0
    
    def set_zoom(self, zoom: float) -> None:
        """Set zoom factor within allowed bounds."""
        self.zoom_factor = max(self.min_zoom, min(self.max_zoom, zoom))
    
    def get_zoom(self) -> float:
        """Get current zoom factor."""
        return self.zoom_factor
    
    def set_pan(self, offset: QPointF) -> None:
        """Set pan offset."""
        self.pan_offset = offset
    
    def get_pan(self) -> QPointF:
        """Get current pan offset."""
        return self.pan_offset
    
    def reset(self) -> None:
        """Reset zoom and pan to defaults."""
        self.zoom_factor = 1.0
        self.pan_offset = QPointF(0, 0)
    
    def widget_to_canvas(self, widget_point: QPointF) -> QPointF:
        """Transform widget coordinates to canvas coordinates."""
        # Reverse the transformation: subtract pan offset and divide by zoom
        canvas_x = (widget_point.x() - self.pan_offset.x()) / self.zoom_factor
        canvas_y = (widget_point.y() - self.pan_offset.y()) / self.zoom_factor
        return QPointF(canvas_x, canvas_y)
    
    def canvas_to_widget(self, canvas_point: QPointF) -> QPointF:
        """Transform canvas coordinates to widget coordinates."""
        # Apply transformation: multiply by zoom and add pan offset
        widget_x = canvas_point.x() * self.zoom_factor + self.pan_offset.x()
        widget_y = canvas_point.y() * self.zoom_factor + self.pan_offset.y()
        return QPointF(widget_x, widget_y)
    
    def transform_rect(self, canvas_rect: QRectF) -> QRectF:
        """Transform a canvas rectangle to widget coordinates."""
        top_left = self.canvas_to_widget(canvas_rect.topLeft())
        size = QPointF(
            canvas_rect.width() * self.zoom_factor,
            canvas_rect.height() * self.zoom_factor
        )
        return QRectF(top_left, top_left + size)
    
    def inverse_transform_rect(self, widget_rect: QRectF) -> QRectF:
        """Transform a widget rectangle to canvas coordinates."""
        top_left = self.widget_to_canvas(widget_rect.topLeft())
        size = QPointF(
            widget_rect.width() / self.zoom_factor,
            widget_rect.height() / self.zoom_factor
        )
        return QRectF(top_left, top_left + size)


def zoom_at_point(transform: CoordinateTransform, zoom_point: QPointF, zoom_delta: float) -> None:
    """Zoom at a specific point, keeping that point stationary."""
    old_zoom = transform.get_zoom()
    new_zoom = old_zoom * zoom_delta
    
    # Clamp zoom to bounds
    new_zoom = max(transform.min_zoom, min(transform.max_zoom, new_zoom))
    actual_delta = new_zoom / old_zoom
    
    if abs(actual_delta - 1.0) < 0.001:  # No significant change
        return
    
    # Calculate new pan offset to keep zoom point stationary
    old_pan = transform.get_pan()
    new_pan_x = zoom_point.x() - (zoom_point.x() - old_pan.x()) * actual_delta
    new_pan_y = zoom_point.y() - (zoom_point.y() - old_pan.y()) * actual_delta
    
    transform.set_zoom(new_zoom)
    transform.set_pan(QPointF(new_pan_x, new_pan_y))


def calculate_fit_zoom(canvas_size: Tuple[int, int], widget_size: Tuple[int, int]) -> float:
    """Calculate zoom factor to fit canvas in widget."""
    canvas_w, canvas_h = canvas_size
    widget_w, widget_h = widget_size
    
    # Add some padding
    padding = 20
    available_w = widget_w - 2 * padding
    available_h = widget_h - 2 * padding
    
    zoom_w = available_w / canvas_w
    zoom_h = available_h / canvas_h
    
    # Use the smaller zoom to ensure everything fits
    return min(zoom_w, zoom_h, 1.0)  # Don't zoom in beyond 100%
