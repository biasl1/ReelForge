"""
Main template editor widget that combines canvas and controls.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QColor

from .canvas import TemplateCanvas
from .controls import TemplateControls
from .persistence import TemplatePersistence
from .frame_timeline import FrameTimeline


class TemplateEditor(QWidget):
    """
    Main template editor combining canvas, controls, and frame timeline.
    """
    
    # Signals
    template_changed = pyqtSignal(dict)  # Template configuration changed
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        
        # Initialize persistence
        self.persistence = TemplatePersistence()
        
        # Frame management for video content types
        self.current_content_type = "reel"
        self.frames_data = {}  # Store frame data per content type
        
        self._setup_ui()
        self._connect_signals()
        
        # Load default state
        self._load_default_template()
    
    def _setup_ui(self):
        """Set up the main UI layout."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Main content area (canvas + controls)
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Create canvas
        self.canvas = TemplateCanvas()
        
        # Create controls
        self.controls = TemplateControls()
        
        # Add to main splitter
        main_splitter.addWidget(self.canvas)
        main_splitter.addWidget(self.controls)
        
        # Set splitter proportions (canvas gets most space)
        main_splitter.setSizes([600, 200])
        main_splitter.setStretchFactor(0, 1)  # Canvas stretches
        main_splitter.setStretchFactor(1, 0)  # Controls fixed
        
        layout.addWidget(main_splitter)
        
        # Frame timeline (initially hidden)
        self.frame_timeline = FrameTimeline()
        self.frame_timeline.setVisible(False)  # Hidden for non-video content
        layout.addWidget(self.frame_timeline)
    
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
        
        # Frame timeline signals
        self.frame_timeline.frame_changed.connect(self._handle_frame_change)
        self.frame_timeline.frames_modified.connect(self._handle_frames_modified)
        
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
        # The canvas handles everything now, including frame data
        config = {
            'canvas_config': self.canvas.get_element_config()
        }
        
        # Add frame data for video content types - get from canvas
        if self._is_video_content_type():
            canvas_config = config['canvas_config']
            if 'frames' in canvas_config:
                config['frames_config'] = {
                    'timeline_config': self.frame_timeline.get_all_frames_config(),
                    'frames_data': canvas_config.get('frames', {}),
                    'current_frame': canvas_config.get('current_frame', 0)
                }
        return config
    
    def set_template_config(self, config: dict):
        """Set template configuration."""
        if not config:
            return
        
        # Load canvas configuration
        canvas_config = config.get('canvas_config', {})
        self.canvas.set_element_config(canvas_config)
        
        # Load frame data for video content types
        if self._is_video_content_type() and 'frames_config' in config:
            frames_config = config['frames_config']
            
            # Restore timeline configuration
            if 'timeline_config' in frames_config:
                self.frame_timeline.set_all_frames_config(frames_config['timeline_config'])
            
            # Restore frames data
            if 'frames_data' in frames_config:
                self.frames_data[self.current_content_type] = frames_config['frames_data']
            
            # Restore current frame
            if 'current_frame' in frames_config:
                current_frame = frames_config['current_frame']
                self.frame_timeline.set_current_frame(current_frame)
                self._load_frame_elements(current_frame)
    
    def set_content_type(self, content_type: str):
        """Set the content type."""
        if content_type == self.current_content_type:
            return
        
        # Save current frame if in video mode
        if self._is_video_content_type():
            self._save_current_frame_elements()
        
        self.current_content_type = content_type
        self.canvas.set_content_type(content_type)
        self.controls.set_content_type(content_type)
        
        # Show/hide frame timeline based on content type
        is_video = self._is_video_content_type()
        self.frame_timeline.setVisible(is_video)
        
        if is_video:
            # Set the correct frame count for this content type
            self.frame_timeline.set_content_type_frames(content_type)
            
            # Tell canvas to switch to this content type (it handles its own frame independence)
            current_frame = 0  # Always start with frame 0 for new content type
            current_frame = self.frame_timeline.get_current_frame()
            self._load_frame_elements(current_frame)
        
        self._emit_template_changed()
    
    @property
    def current_content_type(self):
        """Get current content type."""
        return self._current_content_type
    
    @current_content_type.setter
    def current_content_type(self, value):
        """Set current content type."""
        self._current_content_type = value
    
    def get_content_type(self) -> str:
        """Get the current content type."""
        return self.current_content_type
    
    def _is_video_content_type(self) -> bool:
        """Check if current content type is video-based."""
        return self.current_content_type in ['story', 'reel', 'tutorial']
    
    def _handle_content_type_change(self, content_type: str):
        """Handle content type change from controls."""
        self.set_content_type(content_type)
    
    def _handle_frame_change(self, frame_index: int):
        """Handle frame change from timeline."""
        if self._is_video_content_type():
            # Tell the canvas to switch frames - THIS IS CRITICAL FOR INDEPENDENCE!
            self.canvas.set_current_frame(frame_index)
            
            # Save current frame elements before switching
            self._save_current_frame_elements()
            
            # Load new frame elements
            self._load_frame_elements(frame_index)
            
            self._emit_template_changed()
    
    def _handle_frames_modified(self):
        """Handle frames modification from timeline."""
        if self._is_video_content_type():
            # Update frame data structure to match new frame count
            frame_count = self.frame_timeline.get_frame_count()
            current_frames = self.frames_data.get(self.current_content_type, {})
            
            # Remove frames that no longer exist (convert frame keys to int for comparison)
            frames_to_remove = [f for f in current_frames.keys() if int(f) >= frame_count]
            for frame_idx in frames_to_remove:
                del current_frames[frame_idx]
            
            self._update_frame_timeline_display()
            self._emit_template_changed()
    
    def _update_frame_timeline_display(self):
        """Update the frame timeline display."""
        if self._is_video_content_type():
            # Update timeline to reflect current frame structure
            current_frame = self.frame_timeline.get_current_frame()
            frame_count = self.frame_timeline.get_frame_count()
            
            # Ensure current frame is valid
            if current_frame >= frame_count:
                self.frame_timeline.set_current_frame(max(0, frame_count - 1))
    
    def _save_current_frame_elements(self):
        """Save current canvas elements to the current frame."""
        if not self._is_video_content_type():
            return
        
        # The canvas handles its own frame saving
        print(f"💾 Editor asking canvas to save current frame")
    
    def _load_frame_elements(self, frame_index: int):
        """Load elements for the specified frame."""
        if not self._is_video_content_type():
            return
        
        # The canvas already handles frame switching and independence internally
        # We just need to tell it which frame to load
        print(f"📁 Editor loading frame {frame_index} - canvas handles independence")
    
    def _initialize_fresh_frame(self, frame_index: int):
        """Initialize a completely fresh frame with unique element positions."""
        # Create a temporary canvas to get fresh default elements
        from PyQt6.QtCore import QRect
        import random
        
        # Get default elements for this content type
        self.canvas.set_content_type(self.current_content_type)
        fresh_config = self.canvas.get_element_config()
        
        # Randomize positions for each element to make them INDEPENDENT
        if 'elements' in fresh_config:
            for element_id, element_data in fresh_config['elements'].items():
                if 'rect' in element_data:
                    # Generate unique random positions for this frame
                    base_x = 50 + (frame_index * 30) + random.randint(-20, 20)
                    base_y = 50 + (frame_index * 40) + random.randint(-20, 20)
                    
                    original_rect = element_data['rect']
                    new_rect = QRect(
                        base_x,
                        base_y, 
                        original_rect.width(),
                        original_rect.height()
                    )
                    element_data['rect'] = new_rect
        
        # Save this fresh frame data
        if self.current_content_type not in self.frames_data:
            self.frames_data[self.current_content_type] = {}
        
        self.frames_data[self.current_content_type][frame_index] = fresh_config
        
        # Load the fresh frame
        self.canvas.set_element_config(fresh_config)
        
        print(f"🎨 Created INDEPENDENT frame {frame_index} with unique positions!")
    
    def set_project(self, project):
        """Set the current project for the template editor."""
        # This method is called by the main window when a project is loaded
        # The actual template data is loaded through set_template_config method
        pass
    
    def export_template_data(self) -> dict:
        """Export current template data for AI generation."""
        # Save current state first
        if self._is_video_content_type():
            self._save_current_frame_elements()
        
        return self.get_template_config()