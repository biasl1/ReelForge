"""
Backward compatibility wrapper for old template editor tests.
This provides the old interface so existing tests don't break.
"""
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor

from .editor import TemplateEditor


class BackwardCompatibleTemplateEditor(TemplateEditor):
    """
    Wrapper that provides backward compatibility with old template editor interface.
    """
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Create a visual_editor attribute that maps to our canvas for compatibility
        self.visual_editor = VisualEditorCompat(self.canvas)
        
        # Add compatibility attributes for old interface
        self.constrain_to_frame = self.controls.constrain_checkbox
        # Create a compatibility structure for content_settings
        self.content_settings = {
            'reel': {'pip_rect': None, 'text_overlays': {}},
            'story': {'pip_rect': None, 'text_overlays': {}},
            'teaser': {'pip_rect': None, 'text_overlays': {}},
            'tutorial': {'pip_rect': None, 'text_overlays': {}},
            'post': {'pip_rect': None, 'text_overlays': {}}
        }
    
    def _on_content_type_changed(self, content_type: str):
        """Old method name for content type change."""
        self.set_content_type(content_type)
        self._load_all_settings_for_current_type()
    
    def _on_constraint_changed(self):
        """Old method name for constraint change."""
        # The new interface automatically updates the canvas constraint mode
        # via the signal/slot connection, so we don't need to do anything here
        pass
    
    def _save_all_current_settings(self):
        """Old method name for saving settings."""
        # Update the compatibility content_settings structure with current canvas state
        current_type = self.canvas.content_type
        if current_type in self.content_settings:
            settings = self.content_settings[current_type]
            
            # Save PiP rect if it exists
            if 'pip' in self.canvas.elements:
                rect = self.canvas.elements['pip']['rect']
                settings['pip_rect'] = (rect.x(), rect.y(), rect.width(), rect.height())
            
            # Save text overlay rects
            settings['text_overlays'] = {}
            for element_id, element in self.canvas.elements.items():
                if element['type'] == 'text':
                    rect = element['rect']
                    settings['text_overlays'][element_id] = {
                        'rect': (rect.x(), rect.y(), rect.width(), rect.height()),
                        'content': element.get('content', ''),
                        'enabled': element.get('enabled', True)
                    }
    
    def _load_all_settings_for_current_type(self):
        """Old method name for loading settings."""
        current_type = self.canvas.content_type
        if current_type in self.content_settings:
            settings = self.content_settings[current_type]
            
            # Load PiP rect if it exists
            if 'pip_rect' in settings and settings['pip_rect']:
                rect_data = settings['pip_rect']
                from PyQt6.QtCore import QRect
                rect = QRect(rect_data[0], rect_data[1], rect_data[2], rect_data[3])
                if 'pip' in self.canvas.elements:
                    self.canvas.elements['pip']['rect'] = rect
            
            # Load text overlay rects
            if 'text_overlays' in settings and settings['text_overlays']:
                for element_id, overlay_data in settings['text_overlays'].items():
                    if element_id in self.canvas.elements:
                        rect_data = overlay_data['rect']
                        from PyQt6.QtCore import QRect
                        rect = QRect(rect_data[0], rect_data[1], rect_data[2], rect_data[3])
                        self.canvas.elements[element_id]['rect'] = rect
                        self.canvas.elements[element_id]['content'] = overlay_data.get('content', '')
                        self.canvas.elements[element_id]['enabled'] = overlay_data.get('enabled', True)
            
            self.canvas.update()
    
    def _update_elements_for_new_frame(self, old_frame: QRect):
        """Update elements for new frame (compatibility)."""
        self.canvas._update_elements_for_new_frame(old_frame)
    
    def _auto_save_to_project(self):
        """Auto-save to project (compatibility)."""
        # In the old system this would save to project automatically
        # For now we just ensure internal state is consistent
        if hasattr(self, 'project') and self.project:
            # Store template settings in project
            config = self.get_template_config()
            if not hasattr(self.project, 'template_settings'):
                self.project.template_settings = {}
            self.project.template_settings.update(config)
    
    def _transform_point_to_canvas(self, screen_point):
        """Transform screen point to canvas coordinates (compatibility)."""
        from PyQt6.QtCore import QPointF
        return self.canvas.transform.widget_to_canvas(QPointF(screen_point))
    
    def _transform_point_to_screen(self, canvas_point):
        """Transform canvas point to screen coordinates (compatibility)."""
        from PyQt6.QtCore import QPointF
        return self.canvas.transform.canvas_to_widget(QPointF(canvas_point))


class VisualEditorCompat:
    """
    Compatibility wrapper for the old visual editor interface.
    Maps old attribute access to new canvas properties.
    """
    
    def __init__(self, canvas):
        self.canvas = canvas
    
    @property
    def pip_rect(self) -> QRect:
        """Get PiP rectangle (compatibility)."""
        if 'pip' in self.canvas.elements:
            return self.canvas.elements['pip']['rect']
        else:
            # Return default if not found
            return QRect(50, 50, 100, 100)
    
    @pip_rect.setter
    def pip_rect(self, value: QRect):
        """Set PiP rectangle (compatibility)."""
        if 'pip' in self.canvas.elements:
            self.canvas.elements['pip']['rect'] = value
            self.canvas.update()
    
    @property
    def text_overlays(self) -> dict:
        """Get text overlays (compatibility)."""
        # Return a special dict that updates the canvas when modified
        return TextOverlayDictCompat(self.canvas)
    
    @text_overlays.setter
    def text_overlays(self, value: dict):
        """Set text overlays (compatibility)."""
        for element_id, element_data in value.items():
            if element_id in self.canvas.elements and self.canvas.elements[element_id]['type'] == 'text':
                element = self.canvas.elements[element_id]
                element['rect'] = element_data.get('rect', element['rect'])
                element['enabled'] = element_data.get('enabled', element.get('enabled', True))
                element['content'] = element_data.get('content', element.get('content', ''))
                element['size'] = element_data.get('size', element.get('size', 24))
                element['color'] = element_data.get('color', element.get('color', QColor(255, 255, 255)))
                element['style'] = element_data.get('style', element.get('style', 'normal'))
        
        self.canvas.update()
    
    @property
    def constrain_to_frame(self) -> bool:
        """Get constraint mode (compatibility)."""
        return self.canvas.constrain_to_frame
    
    @constrain_to_frame.setter
    def constrain_to_frame(self, value: bool):
        """Set constraint mode (compatibility)."""
        self.canvas.set_constraint_mode(value)
    
    def _constrain_elements_to_frame(self):
        """Constrain all elements to content frame (compatibility)."""
        self.canvas._constrain_elements_to_frame()
    
    def _update_elements_for_new_frame(self, old_frame: QRect):
        """Update elements for new frame (compatibility)."""
        self.canvas._update_elements_for_new_frame(old_frame)
    
    @property
    def zoom_factor(self) -> float:
        """Get zoom factor (compatibility)."""
        return self.canvas.get_zoom()
    
    @zoom_factor.setter  
    def zoom_factor(self, value: float):
        """Set zoom factor (compatibility)."""
        self.canvas.set_zoom(value)
    
    @property
    def pan_offset_x(self) -> float:
        """Get pan X offset (compatibility)."""
        return self.canvas.transform.get_pan().x()
    
    @pan_offset_x.setter
    def pan_offset_x(self, value: float):
        """Set pan X offset (compatibility)."""
        current_pan = self.canvas.transform.get_pan()
        from PyQt6.QtCore import QPointF
        self.canvas.transform.set_pan(QPointF(value, current_pan.y()))
    
    @property
    def pan_offset_y(self) -> float:
        """Get pan Y offset (compatibility)."""
        return self.canvas.transform.get_pan().y()
    
    @pan_offset_y.setter
    def pan_offset_y(self, value: float):
        """Set pan Y offset (compatibility)."""
        current_pan = self.canvas.transform.get_pan()
        from PyQt6.QtCore import QPointF
        self.canvas.transform.set_pan(QPointF(current_pan.x(), value))
    
    def _transform_point_to_canvas(self, screen_point):
        """Transform screen point to canvas coordinates (compatibility)."""
        from PyQt6.QtCore import QPointF
        return self.canvas.transform.widget_to_canvas(QPointF(screen_point))
    
    def _transform_point_to_screen(self, canvas_point):
        """Transform canvas point to screen coordinates (compatibility)."""
        from PyQt6.QtCore import QPointF
        return self.canvas.transform.canvas_to_widget(QPointF(canvas_point))
    
    @property
    def content_frame(self) -> QRect:
        """Get content frame (compatibility)."""
        return self.canvas.content_frame
    
    @content_frame.setter
    def content_frame(self, value: QRect):
        """Set content frame (compatibility)."""
        self.canvas.content_frame = value
        self.canvas.update()
    
    @property
    def zoom_factor(self) -> float:
        """Get zoom factor (compatibility)."""
        return self.canvas.get_zoom()
    
    @zoom_factor.setter  
    def zoom_factor(self, value: float):
        """Set zoom factor (compatibility)."""
        self.canvas.set_zoom(value)


class TextOverlayDictCompat(dict):
    """
    Special dictionary that provides compatibility with old text overlay access patterns.
    """
    
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas
        self._update_from_canvas()
    
    def _update_from_canvas(self):
        """Update this dict from canvas elements."""
        self.clear()
        for element_id, element in self.canvas.elements.items():
            if element['type'] == 'text':
                self[element_id] = TextOverlayCompat(self.canvas, element_id, element)
    
    def __getitem__(self, key):
        """Get text overlay, updating from canvas first."""
        self._update_from_canvas()
        return super().__getitem__(key)
    
    def items(self):
        """Get items, updating from canvas first."""
        self._update_from_canvas()
        return super().items()
    
    def keys(self):
        """Get keys, updating from canvas first."""
        self._update_from_canvas()
        return super().keys()
    
    def values(self):
        """Get values, updating from canvas first."""
        self._update_from_canvas()
        return super().values()


class TextOverlayCompat:
    """
    Compatibility wrapper for individual text overlay elements.
    Allows direct attribute access while updating the canvas.
    """
    
    def __init__(self, canvas, element_id: str, element: dict):
        self.canvas = canvas
        self.element_id = element_id
        self._element = element
    
    @property
    def rect(self) -> QRect:
        return self._element['rect']
    
    @rect.setter
    def rect(self, value: QRect):
        self._element['rect'] = value
        self.canvas.update()
    
    def __getitem__(self, key):
        """Dictionary-style access for compatibility."""
        if key == 'rect':
            return self.rect
        return self._element.get(key)
    
    def __setitem__(self, key, value):
        """Dictionary-style assignment for compatibility."""
        if key == 'rect':
            self.rect = value
        else:
            self._element[key] = value
            self.canvas.update()
    
    def get(self, key, default=None):
        """Dictionary-style get for compatibility."""
        if key == 'rect':
            return self.rect
        return self._element.get(key, default)


# For backward compatibility with tests
SimpleTemplateEditor = BackwardCompatibleTemplateEditor
AITemplateEditor = BackwardCompatibleTemplateEditor
