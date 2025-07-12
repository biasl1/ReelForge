"""
Clean template editor widget for per-event editing.
"""
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QSplitter
from PyQt6.QtCore import Qt, pyqtSignal

from .canvas import TemplateCanvas
from .controls import TemplateControls
from .persistence import TemplatePersistence
from .frame_timeline import FrameTimeline


class TemplateEditor(QWidget):
    """
    Template editor for individual calendar events and their frames.
    """
    
    # Signals
    template_changed = pyqtSignal(str, dict)  # event_id, template_configuration
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(800, 600)
        
        # Initialize persistence
        self.persistence = TemplatePersistence()
        
        # Event-based management
        self.current_event_id = None
        self.current_event_data = None
        self.current_frame_index = 0
        self.project = None  # Reference to the project
        
        self._setup_ui()
        self._connect_signals()
    
    def set_project(self, project):
        """Set the project reference and load events."""
        self.project = project
        self._load_events()
    
    def _load_events(self):
        """Load calendar events into the editor."""
        if not self.project:
            return
        
        events = list(self.project.release_events.values())
        self.controls.set_events(events)
    
    def _setup_ui(self):
        """Set up the UI layout."""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        
        # Create splitter for controls and canvas
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Controls panel
        self.controls = TemplateControls()
        self.controls.setMinimumWidth(300)
        self.controls.setMaximumWidth(400)
        splitter.addWidget(self.controls)
        
        # Canvas
        self.canvas = TemplateCanvas()
        splitter.addWidget(self.canvas)
        
        # Set splitter proportions
        splitter.setSizes([300, 500])
        layout.addWidget(splitter)
        
        # Frame timeline (initially hidden)
        self.frame_timeline = FrameTimeline()
        self.frame_timeline.setVisible(False)
        
        # Connect frame timeline to canvas
        self.frame_timeline.set_canvas(self.canvas)
        
        layout.addWidget(self.frame_timeline)
    
    def _connect_signals(self):
        """Connect signals between components."""
        # Controls -> Editor
        self.controls.event_changed.connect(self.load_event)
        self.controls.frame_changed.connect(self.load_frame)
        self.controls.constraint_mode_changed.connect(self.canvas.set_constraint_mode)
        self.controls.reset_positions_requested.connect(self.canvas.reset_positions)
        self.controls.element_property_changed.connect(self._handle_element_property_change)
        
        # Canvas -> Controls
        self.canvas.element_selected.connect(self._handle_element_selection)
        self.canvas.element_moved.connect(self._handle_element_moved)
        self.canvas.element_resized.connect(self._handle_element_resized)
        self.canvas.canvas_clicked.connect(self._handle_canvas_clicked)
        
        # Frame timeline signals
        self.frame_timeline.frame_changed.connect(self.load_frame)
        self.frame_timeline.frames_modified.connect(self._handle_frames_modified)
        self.frame_timeline.frame_description_changed.connect(self._handle_frame_description_change)
        
        # Internal updates
        self.canvas.element_moved.connect(self._save_current_frame)
        self.canvas.element_resized.connect(self._save_current_frame)
    
    def load_event(self, event_id: str):
        """Load a calendar event for editing."""
        if not self.project or event_id not in self.project.release_events:
            return
        
        # Save current event if we have one
        if self.current_event_id:
            self._save_event_template()
        
        # Load new event
        self.current_event_id = event_id
        self.current_event_data = self.project.release_events[event_id]
        self.current_frame_index = 0
        
        # Update UI
        self.controls.set_current_event(event_id, self.current_event_data.__dict__)
        
        # Show/hide frame timeline based on content type
        is_video = self.current_event_data.content_type == 'video'
        self.frame_timeline.setVisible(is_video)
        
        if is_video:
            # Set up frame timeline
            frame_count = self.current_event_data.frame_count
            self.frame_timeline.set_frame_count(frame_count)
            self.frame_timeline.set_current_frame(0)
        
        # Load first frame
        self.load_frame(0)
    
    def load_frame(self, frame_index: int):
        """Load a specific frame for the current event."""
        if not self.current_event_id or not self.current_event_data:
            return
        
        # Save current frame before switching
        if self.current_frame_index != frame_index:
            self._save_current_frame()
        
        self.current_frame_index = frame_index
        
        # Get frame data from event template config
        frame_data = self._get_frame_data(self.current_event_id, frame_index)
        
        # Load frame elements into canvas
        self.canvas.load_frame_elements(frame_data.get('elements', {}))
        
        # Update frame timeline
        if self.frame_timeline.isVisible():
            self.frame_timeline.set_current_frame(frame_index)
    
    def _get_frame_data(self, event_id: str, frame_index: int) -> dict:
        """Get frame data for an event."""
        if not self.project or event_id not in self.project.release_events:
            return {}
        
        event = self.project.release_events[event_id]
        frame_data = event.template_config.get('frame_data', {})
        return frame_data.get(str(frame_index), {})
    
    def _save_current_frame(self):
        """Save the current frame data."""
        if not self.current_event_id:
            return
        
        frame_data = {
            'elements': self.canvas.get_elements_data(),
            'frame_description': self.canvas.get_frame_description()
        }
        
        # Save to event template config
        self._set_frame_data(self.current_event_id, self.current_frame_index, frame_data)
    
    def _set_frame_data(self, event_id: str, frame_index: int, frame_data: dict):
        """Set frame data for an event."""
        if not self.project or event_id not in self.project.release_events:
            return
        
        event = self.project.release_events[event_id]
        if 'frame_data' not in event.template_config:
            event.template_config['frame_data'] = {}
        
        event.template_config['frame_data'][str(frame_index)] = frame_data
        
        # Mark as modified
        import datetime
        event.last_modified = datetime.datetime.now()
    
    def _save_event_template(self):
        """Save current event template configuration."""
        if not self.current_event_id:
            return
        
        # Save current frame
        self._save_current_frame()
        
        # Get template config
        template_config = {
            'frame_data': self._get_all_frame_data(),
            'last_modified': self.current_event_data.last_modified
        }
        
        # Save to project
        self.project.set_event_template_config(self.current_event_id, template_config)
    
    def _get_all_frame_data(self) -> dict:
        """Get all frame data for the current event."""
        if not self.current_event_data:
            return {}
        
        all_frames = {}
        frame_count = self.current_event_data.frame_count
        
        for i in range(frame_count):
            frame_data = self._get_frame_data(self.current_event_id, i)
            if frame_data:
                all_frames[str(i)] = frame_data
        
        return all_frames
    
    def refresh_events(self):
        """Refresh the event list in the controls."""
        if self.project:
            self.controls.refresh_events(self.project.release_events)
    
    def set_current_event(self, event_id: str):
        """Set the current event being edited."""
        self.load_event(event_id)
    
    # === SIGNAL HANDLERS ===
    
    def _handle_element_selection(self, element_id: str):
        """Handle element selection in canvas."""
        self.controls.set_selected_element(element_id)
    
    def _handle_element_moved(self, element_id: str, new_rect):
        """Handle element moved in canvas."""
        self.controls.update_element_position(element_id, new_rect)
    
    def _handle_element_resized(self, element_id: str, new_rect):
        """Handle element resized in canvas."""
        self.controls.update_element_size(element_id, new_rect)
    
    def _handle_canvas_clicked(self):
        """Handle canvas clicked (deselect elements)."""
        self.controls.clear_selection()
    
    def _handle_element_property_change(self, element_id: str, property_name: str, value):
        """Handle element property change from controls."""
        self.canvas.update_element_property(element_id, property_name, value)
    
    def _handle_frames_modified(self):
        """Handle frames modification from timeline."""
        # Update project with new frame count
        if self.current_event_id:
            frame_count = self.frame_timeline.get_frame_count()
            self.project.set_event_frame_count(self.current_event_id, frame_count)
    
    def _handle_frame_description_change(self, frame_index: int, description: str):
        """Handle frame description change from timeline."""
        # Update frame data with new description
        if self.current_event_id:
            frame_data = self._get_frame_data(self.current_event_id, frame_index)
            frame_data['frame_description'] = description
            self._set_frame_data(self.current_event_id, frame_index, frame_data)
    
    # === COMPATIBILITY METHODS ===
    
    def get_template_config(self) -> dict:
        """Get current template configuration."""
        if not self.current_event_id:
            return {}
        
        return {
            'canvas_config': {
                'elements': self.canvas.get_elements_data(),
                'frames': {}
            }
        }
    
    def get_content_type(self):
        """Get current content type."""
        if self.current_event_data:
            return self.current_event_data.content_type
        return 'video'  # Default
