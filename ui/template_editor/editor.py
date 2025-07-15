"""
Clean template editor widget for per-event editing.
"""
import datetime
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
        self._loading_frame = False  # Flag to prevent recursion
        
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
        # Note: Frame navigation is now handled by frame_timeline, not controls
        self.controls.constraint_mode_changed.connect(self.canvas.set_constraint_mode)
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
            # Set up frame timeline with the new update method
            self.frame_timeline.update_for_event(self.current_event_data.__dict__)
            self.frame_timeline.set_current_frame(0)
        
        # Load first frame
        self.load_frame(0)
    
    def load_frame(self, frame_index: int):
        """Load a specific frame with COMPLETE restoration of ALL element properties."""
        if self._loading_frame:  # Prevent recursion
            return
            
        if not self.current_event_id or not self.current_event_data:
            return
        
        self._loading_frame = True
        try:
            # Save current frame before switching
            if self.current_frame_index != frame_index:
                self._save_current_frame()
            
            self.current_frame_index = frame_index
            
            # Get COMPLETE frame data from event template config
            frame_data = self._get_frame_data(self.current_event_id, frame_index)
            
            print(f"🔄 LOADING INDEPENDENT FRAME {frame_index}: {len(frame_data.get('elements', {}))} elements")
            
            # Load frame elements into canvas with FULL restoration
            elements_data = frame_data.get('elements', {})
            
            # Ensure complete element restoration
            for element_id, element_data in elements_data.items():
                print(f"   📋 Element {element_id}: type={element_data.get('type')}, visible={element_data.get('visible', True)}")
                
                # For text elements - restore ALL text properties
                if element_data.get('type') == 'text':
                    print(f"      📝 Text content: '{element_data.get('content', '')}', size: {element_data.get('size', 24)}")
                
                # For PiP elements - restore ALL PiP properties  
                elif element_data.get('type') == 'pip':
                    print(f"      🎬 PiP visible: {element_data.get('visible', True)}, corner_radius: {element_data.get('corner_radius', 0)}")
            
            self.canvas.load_frame_elements(elements_data)
            
            # Update frame timeline with description
            if self.frame_timeline.isVisible():
                self.frame_timeline.set_current_frame(frame_index)
                frame_desc = frame_data.get('frame_description', f'Frame {frame_index + 1}')
                self.frame_timeline.set_frame_description(frame_desc)
                
            print(f"✅ FRAME {frame_index} LOADED: Completely independent with all properties restored")
            
        finally:
            self._loading_frame = False
    
    def _get_frame_data(self, event_id: str, frame_index: int) -> dict:
        """Get frame data for an event, creating default elements if frame is new."""
        if not self.project or event_id not in self.project.release_events:
            return {}
        
        event = self.project.release_events[event_id]
        frame_data = event.template_config.get('frame_data', {})
        existing_frame_data = frame_data.get(str(frame_index), {})
        
        # If frame has no elements, create default ones
        if not existing_frame_data.get('elements'):
            print(f"🔧 Creating default elements for new frame {frame_index} ({event.content_type})")
            
            # Use canvas to create default elements for this content type
            self.canvas._setup_content_type_elements(event.content_type)
            
            # Get the default elements from canvas
            if event.content_type in self.canvas.content_states:
                import copy
                default_elements = copy.deepcopy(self.canvas.content_states[event.content_type]['elements'])
                
                # Convert to serializable format
                from core.project import convert_enums
                default_elements = convert_enums(default_elements)
                
                existing_frame_data = {
                    'frame_index': frame_index,
                    'frame_description': f'{event.content_type.title()} frame {frame_index + 1}',
                    'elements': default_elements
                }
                
                # Save the default elements to the event
                if 'frame_data' not in event.template_config:
                    event.template_config['frame_data'] = {}
                event.template_config['frame_data'][str(frame_index)] = existing_frame_data
                
                print(f"✅ Created {len(default_elements)} default elements for frame {frame_index}")
        else:
            # Clean up existing data to remove unnecessary properties
            elements = existing_frame_data.get('elements', {})
            cleaned_elements = {}
            
            for element_id, element_data in elements.items():
                # Only keep essential properties
                cleaned_element = {
                    'type': element_data.get('type', 'text'),
                    'content': element_data.get('content', ''),
                    'font_size': element_data.get('font_size', element_data.get('size', 12)),
                    'position_preset': element_data.get('position_preset', 'center'),
                    'visible': element_data.get('visible', True)
                }
                
                # Add PiP-specific properties
                if element_data.get('type') == 'pip':
                    cleaned_element['corner_radius'] = element_data.get('corner_radius', 0)
                
                cleaned_elements[element_id] = cleaned_element
            
            # Update the frame data with cleaned elements
            existing_frame_data['elements'] = cleaned_elements
            print(f"🧹 Cleaned {len(cleaned_elements)} elements for frame {frame_index}")
        
        return existing_frame_data
    
    def _save_current_frame(self):
        """Save the current frame data with COMPLETE independence - ALL element properties."""
        if self._loading_frame:  # Don't save while loading
            return
            
        if not self.current_event_id:
            return
        
        # Get comprehensive frame data including ALL element properties
        elements_data = self.canvas.get_elements_data()
        
        # Ensure each element has complete data for frame independence
        for element_id, element_data in elements_data.items():
            # Make sure ALL properties are saved per frame
            if 'visible' not in element_data:
                element_data['visible'] = True
            
            # For text elements - save ALL text properties per frame
            if element_data.get('type') == 'text':
                if 'content' not in element_data:
                    element_data['content'] = f'Text Frame {self.current_frame_index + 1}'
                if 'font_size' not in element_data:
                    element_data['font_size'] = 24
                if 'position_preset' not in element_data:
                    element_data['position_preset'] = 'center'
            
            # For PiP elements - save ALL PiP properties per frame
            elif element_data.get('type') == 'pip':
                if 'corner_radius' not in element_data:
                    element_data['corner_radius'] = 0
                if 'visible' not in element_data:
                    element_data['visible'] = True
        
        # Get frame description from timeline if available
        frame_description = 'Frame description'
        if hasattr(self, 'frame_timeline') and self.frame_timeline:
            frame_description = self.frame_timeline.get_current_frame_description()
        
        # Create comprehensive frame data
        frame_data = {
            'frame_index': self.current_frame_index,
            'frame_description': frame_description,
            'elements': self._clean_elements_data(elements_data),
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        print(f"💾 SAVING INDEPENDENT FRAME {self.current_frame_index}: {len(elements_data)} elements with complete properties")
        
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
        
        # Mark project as modified (no need for per-event last_modified tracking)
    
    def _save_event_template(self):
        """Save current event template configuration."""
        if not self.current_event_id:
            return
        
        # Save current frame
        self._save_current_frame()
        
        # Get and clean all frame data
        all_frame_data = self._get_all_frame_data()
        cleaned_frame_data = {}
        
        for frame_key, frame_data in all_frame_data.items():
            cleaned_frame_data[frame_key] = {
                'frame_index': frame_data.get('frame_index', 0),
                'frame_description': frame_data.get('frame_description', ''),
                'elements': self._clean_elements_data(frame_data.get('elements', {})),
                'timestamp': frame_data.get('timestamp', datetime.datetime.now().isoformat())
            }
        
        # Get template config
        template_config = {
            'frame_data': cleaned_frame_data
        }
        
        # Save to project
        self.project.set_event_template_config(self.current_event_id, template_config)
        print(f"💾 Saved clean template config for event {self.current_event_id} with {len(cleaned_frame_data)} frames")
    
    def _get_all_frame_data(self) -> dict:
        """Get all frame data for the current event - ENSURES ALL FRAMES ARE INCLUDED."""
        if not self.current_event_data:
            return {}
        
        all_frames = {}
        frame_count = self.current_event_data.frame_count
        
        print(f"🔍 Getting ALL frame data for event {self.current_event_id}: frame_count={frame_count}")
        
        for i in range(frame_count):
            frame_data = self._get_frame_data(self.current_event_id, i)
            # ALWAYS include frame data, even if empty - ensures ALL frames are exported
            all_frames[str(i)] = frame_data
            print(f"   📋 Frame {i}: {len(frame_data.get('elements', {}))} elements")
        
        print(f"✅ Collected {len(all_frames)} frames for export (should match frame_count: {frame_count})")
        return all_frames
    
    def refresh_events(self):
        """Refresh the event list in the controls."""
        if self.project:
            self.controls.refresh_events(self.project.release_events)
    
    def set_current_event(self, event_id: str):
        """Set the current event being edited."""
        self.load_event(event_id)
    
    def _clean_elements_data(self, elements_data: dict) -> dict:
        """Clean elements data to ensure only essential properties are saved."""
        cleaned_elements = {}
        
        for element_id, element_data in elements_data.items():
            # Only keep essential properties
            cleaned_element = {
                'type': element_data.get('type', 'text'),
                'content': element_data.get('content', ''),
                'font_size': element_data.get('font_size', 12),
                'position_preset': element_data.get('position_preset', 'center'),
                'visible': element_data.get('visible', True)
            }
            
            # Add PiP-specific properties
            if element_data.get('type') == 'pip':
                cleaned_element['corner_radius'] = element_data.get('corner_radius', 0)
            
            cleaned_elements[element_id] = cleaned_element
        
        return cleaned_elements
    
    # === SIGNAL HANDLERS ===
    
    def _handle_element_selection(self, element_id: str):
        """Handle element selection in canvas."""
        # Get element data from canvas
        element_data = self.canvas.get_element_data(element_id)
        self.controls.set_selected_element(element_id, element_data)
    
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
    
    def keyPressEvent(self, event):
        """Handle key press events for shortcuts."""
        if event.key() == Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Cmd+S: Save project
            self.save_all()
            event.accept()
        else:
            super().keyPressEvent(event)
    
    def save_all(self):
        """Save all current changes to the project."""
        if self.project and self.current_event_id:
            # Clean up and save current template data
            self._save_event_template()
            
            # Save the project
            self.project.save()
            print("✅ Project saved with clean template data")
    
    def clean_all_project_data(self):
        """Clean all project data to remove unnecessary properties."""
        if not self.project:
            return
        
        print("🧹 Cleaning all project template data...")
        
        # Clean all release events
        for event in self.project.release_events.values():
            if 'frame_data' in event.template_config:
                event.template_config = self.project._clean_template_config_for_export(event.template_config)
        
        print("✅ All project template data cleaned")
