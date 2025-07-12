"""
Frame Timeline Widget for video content types (story, reel, tutorial).
Allows multiple independent frames/windows with separate element configurations.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, 
    QScrollArea, QLabel, QSpinBox, QToolButton, QLineEdit
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush
import copy


class FrameButton(QPushButton):
    """Individual frame button in the timeline."""
    
    def __init__(self, frame_index: int, parent=None):
        super().__init__(parent)
        self.frame_index = frame_index
        self.setCheckable(True)
        self.setFixedSize(80, 60)
        self.setText(f"Frame {frame_index + 1}")
        
        # Style the frame button
        self.setStyleSheet("""
            QPushButton {
                border: 2px solid #666;
                border-radius: 4px;
                background-color: #f0f0f0;
                font-size: 10px;
                font-weight: bold;
            }
            QPushButton:checked {
                border: 3px solid #0078d4;
                background-color: #e3f2fd;
                color: #0078d4;
            }
            QPushButton:hover {
                background-color: #e0e0e0;
            }
            QPushButton:checked:hover {
                background-color: #bbdefb;
            }
        """)


class FrameTimeline(QWidget):
    """
    Timeline widget with multiple frames for video content types.
    Each frame can have independent element configurations.
    """
    
    # Signals
    frame_changed = pyqtSignal(int)  # frame_index
    frames_modified = pyqtSignal()   # frames structure changed
    frame_description_changed = pyqtSignal(int, str)  # frame_index, description
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_frame = 0
        self.frames = []  # List of frame configurations
        self.frame_buttons = []
        
        # Per-event frame management (no longer per-content-type)
        self.current_event_id = None
        self.frame_count = 1
        self.content_type = 'video'  # Default content type
        self.content_type_data = {}  # Not used anymore
        
        self._setup_ui()
        self._initialize_content_type_frames()
    
    def _setup_ui(self):
        """Setup the timeline UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Header with controls
        header_layout = QHBoxLayout()
        
        # Timeline label
        timeline_label = QLabel("Video Frames:")
        timeline_label.setStyleSheet("font-weight: bold; color: #333;")
        header_layout.addWidget(timeline_label)
        
        # 🎯 FRAME COUNT CONTROL - THE ONLY PLACE TO SET FRAME COUNTS!
        frame_info_label = QLabel("🎬 Frame Count (ONLY set here!):")
        frame_info_label.setStyleSheet("font-weight: bold; color: #2196F3;")
        frame_info_label.setToolTip("Frame count is ONLY set in the Template Editor, not in the calendar!")
        
        self.frame_count_spin = QSpinBox()
        self.frame_count_spin.setRange(1, 10)
        self.frame_count_spin.setValue(1)  # Default to 1 frame
        self.frame_count_spin.valueChanged.connect(self._on_frame_count_changed)
        self.frame_count_spin.setToolTip("Change the number of frames for this video event")
        
        header_layout.addWidget(frame_info_label)
        header_layout.addWidget(self.frame_count_spin)
        
        # Add/Remove buttons
        self.add_frame_btn = QToolButton()
        self.add_frame_btn.setText("+")
        self.add_frame_btn.setToolTip("Add Frame")
        self.add_frame_btn.clicked.connect(self._add_frame)
        
        self.remove_frame_btn = QToolButton()
        self.remove_frame_btn.setText("-")
        self.remove_frame_btn.setToolTip("Remove Frame")
        self.remove_frame_btn.clicked.connect(self._remove_frame)
        
        header_layout.addWidget(self.add_frame_btn)
        header_layout.addWidget(self.remove_frame_btn)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Scrollable frame area
        scroll_area = QScrollArea()
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setMaximumHeight(80)
        scroll_area.setWidgetResizable(True)
        
        # Frame container
        self.frame_container = QWidget()
        self.frame_layout = QHBoxLayout(self.frame_container)
        self.frame_layout.setContentsMargins(5, 5, 5, 5)
        self.frame_layout.setSpacing(10)
        
        scroll_area.setWidget(self.frame_container)
        layout.addWidget(scroll_area)
        
        # Current frame info
        frame_info_layout = QHBoxLayout()
        
        self.current_frame_label = QLabel("Current: Frame 1")
        self.current_frame_label.setStyleSheet("font-weight: bold; color: #0078d4;")
        frame_info_layout.addWidget(self.current_frame_label)
        
        # Add frame description editor
        frame_desc_label = QLabel("Description:")
        frame_desc_label.setStyleSheet("font-weight: bold;")
        frame_info_layout.addWidget(frame_desc_label)
        
        self.frame_description_edit = QLineEdit()
        self.frame_description_edit.setPlaceholderText("Enter frame description...")
        self.frame_description_edit.setMinimumWidth(300)
        self.frame_description_edit.editingFinished.connect(self._on_description_changed)
        frame_info_layout.addWidget(self.frame_description_edit)
        
        frame_info_layout.addStretch()
        layout.addLayout(frame_info_layout)
    
    def _initialize_content_type_frames(self):
        """Initialize frames - no longer needed in per-event system."""
        pass
    
    def _load_content_type_frames(self):
        """Load frames for the current content type - COMPLETE ISOLATION."""
        # Save current description if we're switching
        if hasattr(self, 'frame_description_edit') and self.frames:
            current_desc = self.frame_description_edit.text()
            if self.current_frame < len(self.frames):
                self.frames[self.current_frame]['frame_description'] = current_desc
        
        # Clear existing UI
        for btn in self.frame_buttons:
            self.frame_layout.removeWidget(btn)
            btn.deleteLater()
        self.frame_buttons.clear()
        
        # Load frames for current content type
        content_data = self.content_type_data[self.content_type]
        self.frames = content_data['frames'].copy()
        self.current_frame = content_data['current_frame']
        
        # Create buttons for current content type's frames
        for i in range(len(self.frames)):
            self._create_frame_button(i)
        
        # Update UI to show current content type's data
        if self.frame_buttons and 0 <= self.current_frame < len(self.frame_buttons):
            self.frame_buttons[self.current_frame].setChecked(True)
        
        self.frame_count_spin.setValue(len(self.frames))
        self._update_current_frame_label()
    
    def set_content_type(self, content_type: str):
        """Switch to a different content type - COMPLETE DATA ISOLATION."""
        if content_type == self.content_type:
            return  # Already on this content type
        
        # Save current content type's data
        self._save_current_content_type_data()
        
        # Switch to new content type
        self.content_type = content_type
        
        # Initialize if needed
        if content_type not in self.content_type_data:
            self.content_type_data[content_type] = {'frames': [], 'current_frame': 0}
        
        if not self.content_type_data[content_type]['frames']:
            # Create default frames for this content type
            frames = []
            for i in range(3):
                frame_config = {
                    'elements': {},
                    'duration': 1.0,
                    'transition': 'none',
                    'frame_description': f'{content_type.title()} frame {i+1} description'
                }
                frames.append(frame_config)
            
            self.content_type_data[content_type]['frames'] = frames
            self.content_type_data[content_type]['current_frame'] = 0
        
        # Load new content type's frames
        self._load_content_type_frames()
    
    def _save_current_content_type_data(self):
        """Save current content type's data before switching."""
        if hasattr(self, 'frame_description_edit') and self.frames:
            # Save current description
            current_desc = self.frame_description_edit.text()
            if self.current_frame < len(self.frames):
                self.frames[self.current_frame]['frame_description'] = current_desc
        
        # Save to content type data
        self.content_type_data[self.content_type]['frames'] = self.frames.copy()
        self.content_type_data[self.content_type]['current_frame'] = self.current_frame
    
    def _create_frame_button(self, frame_index: int):
        """Create a new frame button."""
        frame_btn = FrameButton(frame_index)
        frame_btn.clicked.connect(lambda checked, idx=frame_index: self._on_frame_selected(idx))
        
        self.frame_buttons.append(frame_btn)
        self.frame_layout.addWidget(frame_btn)
        
        # Update the remove button state
        self.remove_frame_btn.setEnabled(len(self.frame_buttons) > 1)
    
    def _on_frame_selected(self, frame_index: int):
        """Handle frame selection - ONLY WORKS WITH CURRENT CONTENT TYPE DATA."""
        if frame_index == self.current_frame:
            return
        
        # Save current frame's description to LOCAL timeline data
        current_description = self.frame_description_edit.text()
        if self.current_frame < len(self.frames):
            self.frames[self.current_frame]['frame_description'] = current_description
            
        # Uncheck all other buttons
        for i, btn in enumerate(self.frame_buttons):
            btn.setChecked(i == frame_index)
        
        # Switch to new frame
        self.current_frame = frame_index
        
        # Update UI with new frame's data
        self._update_current_frame_label()
        
        # Emit signal to editor
        self.frame_changed.emit(frame_index)
    
    def _update_current_frame_label(self):
        """Update the current frame label and description field."""
        self.current_frame_label.setText(f"Current: Frame {self.current_frame + 1}")
        
        # Load description from current content type's frame data
        if self.current_frame < len(self.frames):
            description = self.frames[self.current_frame].get('frame_description', f'{self.content_type.title()} frame {self.current_frame+1} description')
            
            # Update UI field without triggering events
            self.frame_description_edit.blockSignals(True)
            self.frame_description_edit.setText(description)
            self.frame_description_edit.blockSignals(False)
    
    def _on_description_changed(self):
        """Handle frame description changes - SAVE TO CURRENT CONTENT TYPE ONLY."""
        description = self.frame_description_edit.text()
        
        # Save to current frame in current content type
        if self.current_frame < len(self.frames):
            self.frames[self.current_frame]['frame_description'] = description
            
            # Emit signal to editor
            self.frame_description_changed.emit(self.current_frame, description)
            
    def set_canvas(self, canvas):
        """Connect to canvas - NO SYNC, TIMELINE IS INDEPENDENT."""
        self.canvas = canvas
        # Timeline manages its own descriptions per content type
        # NO automatic sync with canvas
    
    def get_current_frame_description(self) -> str:
        """Get the description of the current frame."""
        if hasattr(self, 'frame_description_edit'):
            return self.frame_description_edit.text()
        elif self.current_frame < len(self.frames):
            return self.frames[self.current_frame].get('frame_description', f'Frame {self.current_frame + 1}')
        return f'Frame {self.current_frame + 1}'
    
    def set_frame_description(self, description: str):
        """Set the description for the current frame."""
        if hasattr(self, 'frame_description_edit'):
            self.frame_description_edit.blockSignals(True)
            self.frame_description_edit.setText(description)
            self.frame_description_edit.blockSignals(False)
        
        # Also update the frames data
        if self.current_frame < len(self.frames):
            self.frames[self.current_frame]['frame_description'] = description
    
    def get_frame_count(self) -> int:
        """Get the total number of frames."""
        return len(self.frames)
    
    def _sync_canvas_frame_count(self):
        """Sync the canvas frame count with timeline frame count - CRITICAL FOR PRESERVATION."""
        if hasattr(self, 'canvas') and self.canvas:
            current_frame_count = len(self.frames)
            print(f"🔄 Timeline syncing canvas frame count to {current_frame_count} for {self.content_type}")
            self.canvas.set_content_type_frame_count(self.content_type, current_frame_count)

    def _on_frame_count_changed(self, count: int):
        """Handle frame count change from spinner."""
        current_count = len(self.frames)
        
        if count > current_count:
            # Add frames
            for i in range(current_count, count):
                self._add_frame()
        elif count < current_count:
            # Remove frames
            for i in range(current_count - 1, count - 1, -1):
                self._remove_frame_at_index(i)
    
    def _add_frame(self):
        """Add a new frame to CURRENT CONTENT TYPE ONLY."""
        if len(self.frames) >= 10:  # Max limit
            return
            
        frame_index = len(self.frames)
        frame_config = {
            'elements': {},
            'duration': 1.0,
            'transition': 'none',
            'frame_description': f'{self.content_type.title()} frame {frame_index+1} description'
        }
        
        # Add to current content type
        self.frames.append(frame_config)
        self.content_type_data[self.content_type]['frames'].append(frame_config)
        
        self._create_frame_button(frame_index)
        
        # Update spinner
        self.frame_count_spin.setValue(len(self.frames))
        
        # CRITICAL: Sync canvas frame count to match timeline
        print(f"🔄 _add_frame: Syncing canvas after adding frame {frame_index+1}")
        self._sync_canvas_frame_count()
        
        self.frames_modified.emit()
    
    def _remove_frame(self):
        """Remove the last frame."""
        if len(self.frames) <= 1:  # Keep at least one frame
            return
            
        self._remove_frame_at_index(len(self.frames) - 1)
    
    def _remove_frame_at_index(self, index: int):
        """Remove frame at specific index from CURRENT CONTENT TYPE."""
        if len(self.frames) <= 1 or index < 0 or index >= len(self.frames):
            return
        
        # Remove from local frames list
        self.frames.pop(index)
        
        # Remove from current content type data - with bounds checking
        content_type_frames = self.content_type_data[self.content_type]['frames']
        if index < len(content_type_frames):
            content_type_frames.pop(index)
        else:
            print(f"⚠️ Warning: Frame {index} not found in content_type_data, skipping content_type_data removal")
        
        # Remove button
        if index < len(self.frame_buttons):
            btn = self.frame_buttons.pop(index)
            self.frame_layout.removeWidget(btn)
            btn.deleteLater()
        
        # Update button indices and labels
        for i, btn in enumerate(self.frame_buttons):
            btn.frame_index = i
            btn.setText(f"Frame {i + 1}")
            btn.clicked.disconnect()
            btn.clicked.connect(lambda checked, idx=i: self._on_frame_selected(idx))
        
        # Adjust current frame if needed
        if self.current_frame >= len(self.frames):
            self.current_frame = len(self.frames) - 1
            self.content_type_data[self.content_type]['current_frame'] = self.current_frame
        
        # Update selection - make sure current_frame is valid for frame_buttons too
        if self.frame_buttons:
            for btn in self.frame_buttons:
                btn.setChecked(False)
            # Double-check bounds for frame_buttons
            if 0 <= self.current_frame < len(self.frame_buttons):
                self.frame_buttons[self.current_frame].setChecked(True)
        
        # Update UI
        self.frame_count_spin.setValue(len(self.frames))
        self._update_current_frame_label()
        self.remove_frame_btn.setEnabled(len(self.frame_buttons) > 1)
        
        # CRITICAL: Notify canvas that frame count has changed
        self._sync_canvas_frame_count()
        
        self.frames_modified.emit()
        self.frame_changed.emit(self.current_frame)
    
    def set_current_frame(self, frame_index: int):
        """Set the current frame and update UI."""
        if frame_index < 0 or frame_index >= len(self.frames):
            return  # Invalid frame index
        
        # Update current frame
        self.current_frame = frame_index
        
        # Update button states
        for i, button in enumerate(self.frame_buttons):
            button.setChecked(i == frame_index)
        
        # Update label
        self._update_current_frame_label()
        
        # Emit signal to notify of frame change
        self.frame_changed.emit(frame_index)
    
    def get_current_frame(self) -> int:
        """Get current frame index."""
        return self.current_frame
    
    def get_frame_count(self) -> int:
        """Get total frame count."""
        return len(self.frames)
    
    def get_frame_config(self, frame_index: int) -> dict:
        """Get configuration for specific frame."""
        if 0 <= frame_index < len(self.frames):
            return self.frames[frame_index].copy()
        return {}
    
    def set_frame_config(self, frame_index: int, config: dict):
        """Set configuration for specific frame."""
        if 0 <= frame_index < len(self.frames):
            self.frames[frame_index] = config.copy()
    
    def get_all_frames_config(self) -> list:
        """Get configuration for all frames."""
        return [frame.copy() for frame in self.frames]
    
    def set_all_frames_config(self, frames_config: list):
        """Set configuration for all frames while preserving canvas descriptions."""
        # CRITICAL: Get current descriptions from canvas before overriding
        canvas_descriptions = {}
        if hasattr(self, "canvas") and self.canvas:
            for i in range(len(self.frames)):
                canvas_frame_data = self.canvas.get_current_frame_data() if i == self.current_frame else None
                if not canvas_frame_data and self.canvas.is_video_content_type():
                    # Get description for this specific frame from canvas
                    canvas_state = self.canvas.content_states.get(self.content_type, {})
                    canvas_frames = canvas_state.get("frames", {})
                    if i in canvas_frames:
                        canvas_descriptions[i] = canvas_frames[i].get("frame_description", "")
        
        """Set configuration for all frames."""
        # Clear existing frames
        for btn in self.frame_buttons:
            self.frame_layout.removeWidget(btn)
            btn.deleteLater()
        
        self.frame_buttons.clear()
        self.frames.clear()
        
        # Add new frames
        for i, frame_config in enumerate(frames_config):
            self.frames.append(frame_config.copy())
            self._create_frame_button(i)
        
        # Ensure at least one frame
        if not self.frames:
            self._initialize_default_frames()
        
        # Update UI
        self.current_frame = 0
        if self.frame_buttons:
            self.frame_buttons[0].setChecked(True)
        
        self.frame_count_spin.setValue(len(self.frames))
        self._update_current_frame_label()
    
    def is_video_content_type(self, content_type: str) -> bool:
        """Check if content type supports frames."""
        return content_type == 'video'
    
    def set_content_type_frames(self, content_type: str):
        """Set the number of frames based on content type - RESPECT USER CHOICE."""
        # DO NOT force predefined frame counts - keep whatever the user has set
        # The timeline already has the correct number of frames that the user wants
        pass

    def sync_descriptions_with_canvas(self):
        """Sync timeline frame descriptions with canvas - FIXES LOADING ISSUES."""
        if not hasattr(self, 'canvas') or not self.canvas:
            return
            
        if not self.canvas.is_video_content_type(self.content_type):
            return
            
        print(f"🔄 Syncing timeline descriptions with canvas for {self.content_type}")
        
        # Get canvas frame descriptions
        canvas_state = self.canvas.content_states.get(self.content_type, {})
        canvas_frames = canvas_state.get('frames', {})
        
        # Update timeline frames with canvas descriptions
        for i, timeline_frame in enumerate(self.frames):
            if i in canvas_frames:
                canvas_desc = canvas_frames[i].get('frame_description', '')
                if canvas_desc:
                    timeline_frame['frame_description'] = canvas_desc
                    # Also update content type data
                    if (self.content_type in self.content_type_data and 
                        'frames' in self.content_type_data[self.content_type] and
                        i < len(self.content_type_data[self.content_type]['frames'])):
                        self.content_type_data[self.content_type]['frames'][i]['frame_description'] = canvas_desc
                    
                    print(f"✅ Synced frame {i} description: '{canvas_desc}'")
        
        # Update UI if we're on the current frame
        self._update_description_display()
        
        print(f"🔄 Timeline-canvas sync complete for {self.content_type}")

    def _update_description_display(self):
        """Update the description edit field with current frame's description."""
        if (hasattr(self, 'frame_description_edit') and 
            self.current_frame < len(self.frames)):
            current_desc = self.frames[self.current_frame].get('frame_description', '')
            self.frame_description_edit.blockSignals(True)
            self.frame_description_edit.setText(current_desc)
            self.frame_description_edit.blockSignals(False)
    
    def set_frame_count(self, frame_count):
        """Set the total number of frames for current content type"""
        # Update internal frames list
        current_count = len(self.frames)
        
        if frame_count > current_count:
            # Add new frames
            for i in range(current_count, frame_count):
                self.frames.append({
                    'frame_description': f'{self.content_type.title()} frame {i + 1}'
                })
        elif frame_count < current_count:
            # Remove extra frames
            self.frames = self.frames[:frame_count]
            
            # Adjust current frame if needed
            if self.current_frame >= frame_count:
                self.current_frame = max(0, frame_count - 1)
        
        # Update content type data
        if self.content_type not in self.content_type_data:
            self.content_type_data[self.content_type] = {}
        
        self.content_type_data[self.content_type]['frames'] = list(range(frame_count))
        self.content_type_data[self.content_type]['current_frame'] = self.current_frame
        
        # Update UI
        self._update_frame_ui()
        
        print(f"📏 Timeline set frame count to {frame_count} for {self.content_type}")
    
    def _update_frame_ui(self):
        """Update the frame UI display - rebuild frame buttons to match frame count"""
        # Clear existing frame buttons
        for btn in self.frame_buttons:
            btn.setParent(None)
            btn.deleteLater()
        self.frame_buttons.clear()
        
        # Create new frame buttons for current frame count
        for i in range(len(self.frames)):
            self._create_frame_button(i)
        
        # Update current frame selection
        if self.frame_buttons and 0 <= self.current_frame < len(self.frame_buttons):
            self.frame_buttons[self.current_frame].setChecked(True)
        
        print(f"🔄 Updated frame UI for {self.content_type}: {len(self.frames)} frames, {len(self.frame_buttons)} buttons")
    
    def update_for_event(self, event_data):
        """Update the frame timeline for a specific event."""
        frame_count = event_data.get('frame_count', 1)
        content_type = event_data.get('content_type', 'video')
        
        print(f"🔄 Timeline updating for {content_type} event with {frame_count} frames")
        
        # Update content type
        self.content_type = content_type
        
        # Update the spinbox without triggering signals
        self.frame_count_spin.blockSignals(True)
        self.frame_count_spin.setValue(frame_count)
        self.frame_count_spin.blockSignals(False)
        
        # Update frame count
        self.set_frame_count(frame_count)
        
        print(f"📏 Timeline set frame count to {frame_count} for {content_type}")

