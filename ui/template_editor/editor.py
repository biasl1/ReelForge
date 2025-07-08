"""
Main template editor widget that combines canvas and controls.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QColor

from .canvas import TemplateCanvas
from .controls import TemplateControls
from .persistence import TemplatePersistence


class TemplateEditor(QWidget):
    """
    Main template editor combining canvas and controls.
    """
    
    # Signals
    template_changed = pyqtSignal(dict)  # Template configuration changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        
        # Initialize persistence
        self.persistence = TemplatePersistence()
        
        self._setup_ui()
        self._connect_signals()
        
        # Load default state
        self._load_default_template()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create splitter for resizable panels
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create canvas
        self.canvas = TemplateCanvas()
        
        # Create controls
        self.controls = TemplateControls()
        
        # Add to splitter
        splitter.addWidget(self.canvas)
        splitter.addWidget(self.controls)
        
        # Set splitter proportions (canvas gets most space)
        splitter.setSizes([600, 200])
        splitter.setStretchFactor(0, 1)  # Canvas stretches
        splitter.setStretchFactor(1, 0)  # Controls fixed
        
        layout.addWidget(splitter)
    
    def _connect_signals(self):
        """Connect signals between components."""
        # Controls -> Canvas
        self.controls.content_type_changed.connect(self._handle_content_type_change)
        self.controls.constraint_mode_changed.connect(self.canvas.set_constraint_mode)
        self.controls.reset_positions_requested.connect(self.canvas.reset_positions)
        self.controls.element_property_changed.connect(self._handle_element_property_change)
        
        # Canvas -> Controls
        self.canvas.element_selected.connect(self._handle_element_selection)
        self.canvas.element_moved.connect(self._handle_element_moved)
        self.canvas.element_resized.connect(self._handle_element_resized)
        self.canvas.canvas_clicked.connect(self._handle_canvas_clicked)
        
        # Internal updates
        self.canvas.element_moved.connect(self._emit_template_changed)
        self.canvas.element_resized.connect(self._emit_template_changed)
        self.controls.content_type_changed.connect(self._emit_template_changed)
        self.controls.constraint_mode_changed.connect(self._emit_template_changed)
    
    def _load_default_template(self):
        """Load default template configuration."""
        # Set initial content type
        self.canvas.set_content_type("reel")
        self.controls.set_content_type("reel")
        
        # Set initial constraint mode
        self.canvas.set_constraint_mode(False)  # Free placement by default
        self.controls.set_constraint_mode(False)
    
    def _handle_element_selection(self, element_id: str):
        """Handle element selection from canvas."""
        if element_id in self.canvas.elements:
            element_data = self.canvas.elements[element_id]
            self.controls.set_selected_element(element_id, element_data)
        else:
            self.controls.clear_selection()
    
    def _handle_canvas_clicked(self, position):
        """Handle canvas click (deselect elements)."""
        self.controls.clear_selection()
    
    def _handle_element_moved(self, element_id: str, new_rect: QRect):
        """Handle element move from canvas."""
        # Update controls if this element is selected
        if self.controls.current_element == element_id:
            element_data = self.canvas.elements[element_id]
            self.controls.set_selected_element(element_id, element_data)
    
    def _handle_element_resized(self, element_id: str, new_rect: QRect):
        """Handle element resize from canvas."""
        # Update controls if this element is selected
        if self.controls.current_element == element_id:
            element_data = self.canvas.elements[element_id]
            self.controls.set_selected_element(element_id, element_data)
    
    def _handle_element_property_change(self, element_id: str, property_name: str, value):
        """Handle property change from controls."""
        if element_id not in self.canvas.elements:
            return
        
        element = self.canvas.elements[element_id]
        
        # Handle special rect properties
        if property_name.startswith('rect_'):
            rect_prop = property_name.replace('rect_', '')
            rect = element['rect']
            
            if rect_prop == 'x':
                rect.moveLeft(value)
            elif rect_prop == 'y':
                rect.moveTop(value)
            elif rect_prop == 'width':
                rect.setWidth(value)
            elif rect_prop == 'height':
                rect.setHeight(value)
        else:
            # Direct property update
            element[property_name] = value
        
        self.canvas.update()
        self._emit_template_changed()
    
    def _emit_template_changed(self):
        """Emit template changed signal with current configuration."""
        config = self.get_template_config()
        self.template_changed.emit(config)
    
    # Public API
    def get_template_config(self) -> dict:
        """Get current template configuration."""
        return {
            'canvas_config': self.canvas.get_element_config()
        }
    
    def set_template_config(self, config: dict):
        """Set template configuration."""
        if 'canvas_config' in config:
            canvas_config = config['canvas_config']
            
            # Update canvas
            self.canvas.set_element_config(canvas_config)
            
            # Update controls
            content_type = canvas_config.get('content_type', 'reel')
            constrain = canvas_config.get('constrain_to_frame', False)
            
            self.controls.set_content_type(content_type)
            self.controls.set_constraint_mode(constrain)
    
    def save_template(self, filepath: str):
        """Save template to file."""
        config = self.get_template_config()
        self.persistence.save_template(config, filepath)
    
    def load_template(self, filepath: str):
        """Load template from file."""
        config = self.persistence.load_template(filepath)
        if config:
            self.set_template_config(config)
            return True
        return False
    
    def export_template_data(self) -> dict:
        """Export template data for use in content generation."""
        canvas_config = self.canvas.get_element_config()
        
        # Convert to format expected by content generation
        export_data = {
            'content_type': canvas_config.get('content_type', 'reel'),
            'settings': {
                'constrain_to_frame': canvas_config.get('constrain_to_frame', False)
            },
            'elements': {}
        }
        
        # Convert elements to export format
        for element_id, element in canvas_config.get('elements', {}).items():
            if not element.get('enabled', True):
                continue
            
            element_data = {
                'type': element['type'],
                'rect': {
                    'x': element['rect'].x(),
                    'y': element['rect'].y(),
                    'width': element['rect'].width(),
                    'height': element['rect'].height()
                }
            }
            
            # Add type-specific properties
            if element['type'] == 'text':
                # Handle color conversion properly
                color = element.get('color', QColor(255, 255, 255))
                if isinstance(color, QColor):
                    color_str = color.name()
                else:
                    color_str = str(color)
                
                element_data.update({
                    'content': element.get('content', ''),
                    'size': element.get('size', 24),
                    'color': color_str,
                    'style': element.get('style', 'normal')
                })
            elif element['type'] == 'pip':
                element_data.update({
                    'shape': element.get('shape', 'square'),
                    'corner_radius': element.get('corner_radius', 10),
                    'color': element.get('color', QColor(100, 150, 200, 128)).name(),
                    'border_color': element.get('border_color', QColor(255, 255, 255)).name()
                })
            
            export_data['elements'][element_id] = element_data
        
        return export_data
    
    # Backward compatibility methods
    def set_project(self, project):
        """Set project (backward compatibility)."""
        # Store project reference if needed for asset loading
        self.project = project
        
        # Load template settings from project if they exist
        if hasattr(project, 'template_settings'):
            template_settings = getattr(project, 'template_settings', {})
            if template_settings:
                self.set_template_config(template_settings)
    
    def get_template_settings(self) -> dict:
        """Get template settings in old format (backward compatibility)."""
        config = self.get_template_config()
        canvas_config = config.get('canvas_config', {})
        
        # Convert to old format
        settings = {
            'content_type': canvas_config.get('content_type', 'reel'),
            'constrain_to_frame': canvas_config.get('constrain_to_frame', False),
            'elements': {}
        }
        
        # Convert elements to old format
        elements = canvas_config.get('elements', {})
        for element_id, element in elements.items():
            if element['type'] == 'text':
                settings['elements'][element_id] = {
                    'enabled': element.get('enabled', True),
                    'rect': [
                        element['rect'].x(), element['rect'].y(),
                        element['rect'].width(), element['rect'].height()
                    ],
                    'content': element.get('content', ''),
                    'size': element.get('size', 24),
                    'color': element.get('color', QColor(255, 255, 255)).getRgb()[:3],
                    'style': element.get('style', 'normal')
                }
            elif element['type'] == 'pip':
                settings['elements'][element_id] = {
                    'enabled': element.get('enabled', True),
                    'rect': [
                        element['rect'].x(), element['rect'].y(),
                        element['rect'].width(), element['rect'].height()
                    ],
                    'shape': element.get('shape', 'square')
                }
        
        return settings
    
    def load_template_settings(self, settings: dict):
        """Load template settings from old format (backward compatibility)."""
        # Convert old format to new format
        canvas_config = {
            'content_type': settings.get('content_type', 'reel'),
            'constrain_to_frame': settings.get('constrain_to_frame', False),
            'elements': {}
        }
        
        # Convert elements from old format
        old_elements = settings.get('elements', {})
        for element_id, element_data in old_elements.items():
            if 'content' in element_data:  # Text element
                rect_data = element_data.get('rect', [50, 50, 200, 50])
                color_data = element_data.get('color', [255, 255, 255])
                
                canvas_config['elements'][element_id] = {
                    'type': 'text',
                    'enabled': element_data.get('enabled', True),
                    'rect': QRect(rect_data[0], rect_data[1], rect_data[2], rect_data[3]),
                    'content': element_data.get('content', ''),
                    'size': element_data.get('size', 24),
                    'color': QColor(color_data[0], color_data[1], color_data[2]),
                    'style': element_data.get('style', 'normal')
                }
            elif 'shape' in element_data:  # PiP element
                rect_data = element_data.get('rect', [50, 50, 100, 100])
                
                canvas_config['elements'][element_id] = {
                    'type': 'pip',
                    'enabled': element_data.get('enabled', True),
                    'rect': QRect(rect_data[0], rect_data[1], rect_data[2], rect_data[3]),
                    'shape': element_data.get('shape', 'square'),
                    'color': QColor(100, 150, 200, 128),
                    'border_color': QColor(255, 255, 255),
                    'border_width': 2
                }
        
        # Set the configuration
        config = {'canvas_config': canvas_config}
        self.set_template_config(config)
    
    def _handle_content_type_change(self, content_type: str):
        """Handle content type change and sync constraint mode."""
        # First, update the canvas (which will save old state and load new state)
        self.canvas.set_content_type(content_type)
        
        # Then update the controls to match the new content type's constraint mode
        if content_type in self.canvas.content_states:
            constraint_mode = self.canvas.content_states[content_type]['constrain_to_frame']
            self.controls.set_constraint_mode(constraint_mode)
    
    # Convenience methods for backward compatibility
    def set_content_type(self, content_type: str):
        """Set content type (convenience method)."""
        self.canvas.set_content_type(content_type)
        self.controls.set_content_type(content_type)
    
    def get_content_type(self) -> str:
        """Get current content type."""
        return self.canvas.content_type
