"""
Frame Timeline Widget for video content types (story, reel, tutorial).
Allows multiple independent frames/windows with separate element configurations.
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QFrame, 
    QScrollArea, QLabel, QSpinBox, QToolButton
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
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_frame = 0
        self.frames = []  # List of frame configurations
        self.frame_buttons = []
        
        self._setup_ui()
        self._initialize_default_frames()
    
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
        
        # Frame count control
        frame_count_label = QLabel("Frames:")
        self.frame_count_spin = QSpinBox()
        self.frame_count_spin.setRange(1, 10)
        self.frame_count_spin.setValue(3)
        self.frame_count_spin.valueChanged.connect(self._on_frame_count_changed)
        
        header_layout.addWidget(frame_count_label)
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
        self.current_frame_label = QLabel("Current: Frame 1")
        self.current_frame_label.setStyleSheet("font-weight: bold; color: #0078d4;")
        layout.addWidget(self.current_frame_label)
    
    def _initialize_default_frames(self):
        """Initialize with 3 default frames."""
        for i in range(3):
            frame_config = {
                'elements': {},  # Will be populated when switching to this frame
                'duration': 1.0,  # Duration in seconds
                'transition': 'none'
            }
            self.frames.append(frame_config)
            self._create_frame_button(i)
        
        # Select first frame
        if self.frame_buttons:
            self.frame_buttons[0].setChecked(True)
            self._update_current_frame_label()
    
    def _create_frame_button(self, frame_index: int):
        """Create a new frame button."""
        frame_btn = FrameButton(frame_index)
        frame_btn.clicked.connect(lambda checked, idx=frame_index: self._on_frame_selected(idx))
        
        self.frame_buttons.append(frame_btn)
        self.frame_layout.addWidget(frame_btn)
        
        # Update the remove button state
        self.remove_frame_btn.setEnabled(len(self.frame_buttons) > 1)
    
    def _on_frame_selected(self, frame_index: int):
        """Handle frame selection."""
        if frame_index == self.current_frame:
            return
            
        # Uncheck all other buttons
        for i, btn in enumerate(self.frame_buttons):
            btn.setChecked(i == frame_index)
        
        self.current_frame = frame_index
        self._update_current_frame_label()
        self.frame_changed.emit(frame_index)
    
    def _update_current_frame_label(self):
        """Update the current frame label."""
        self.current_frame_label.setText(f"Current: Frame {self.current_frame + 1}")
    
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
        """Add a new frame."""
        if len(self.frames) >= 10:  # Max limit
            return
            
        frame_index = len(self.frames)
        frame_config = {
            'elements': {},
            'duration': 1.0,
            'transition': 'none'
        }
        
        self.frames.append(frame_config)
        self._create_frame_button(frame_index)
        
        # Update spinner
        self.frame_count_spin.setValue(len(self.frames))
        
        self.frames_modified.emit()
    
    def _remove_frame(self):
        """Remove the last frame."""
        if len(self.frames) <= 1:  # Keep at least one frame
            return
            
        self._remove_frame_at_index(len(self.frames) - 1)
    
    def _remove_frame_at_index(self, index: int):
        """Remove frame at specific index."""
        if len(self.frames) <= 1 or index < 0 or index >= len(self.frames):
            return
        
        # Remove from data
        self.frames.pop(index)
        
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
        
        # Update selection
        if self.frame_buttons:
            for btn in self.frame_buttons:
                btn.setChecked(False)
            self.frame_buttons[self.current_frame].setChecked(True)
        
        # Update UI
        self.frame_count_spin.setValue(len(self.frames))
        self._update_current_frame_label()
        self.remove_frame_btn.setEnabled(len(self.frame_buttons) > 1)
        
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
        return content_type in ['story', 'reel', 'tutorial']
    
    def set_content_type_frames(self, content_type: str):
        """Set the number of frames based on content type."""
        # Define frame counts per content type - MUST match canvas.py
        frame_counts = {
            'reel': 1,      # Reels are usually single frame
            'story': 5,     # Stories can have multiple frames  
            'tutorial': 8,  # Tutorials have many steps
            'post': 1,      # Posts are static
            'teaser': 1     # Teasers are static
        }
        
        target_frame_count = frame_counts.get(content_type, 3)
        current_frame_count = len(self.frames)
        
        if target_frame_count == current_frame_count:
            return  # Already correct
        
        # Clear existing frames and buttons
        self.frames.clear()
        for button in self.frame_buttons:
            button.setParent(None)
            button.deleteLater()
        self.frame_buttons.clear()
        
        # Create new frames for this content type
        for i in range(target_frame_count):
            frame_config = {
                'elements': {},
                'duration': 1.0,
                'transition': 'none'
            }
            self.frames.append(frame_config)
            self._create_frame_button(i)
        
        # Update UI - no need to call _update_frame_display since buttons are already created
        
        # Reset to first frame
        self.current_frame = 0
        if self.frame_buttons:
            self.frame_buttons[0].setChecked(True)
            self._update_current_frame_label()
        
        # Update frame count spinner
        self.frame_count_spin.setValue(target_frame_count)
        
        print(f"🎬 Timeline updated for {content_type}: {target_frame_count} frames")
