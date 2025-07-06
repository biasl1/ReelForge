"""
Simple Visual Template Editor for ReelTune
Per-content-type settings with visual drag & drop editing
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QGroupBox, QPushButton, QCheckBox, 
    QSpinBox, QSlider, QMessageBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QBrush
from datetime import datetime
from pathlib import Path
import json


class VisualTemplateEditor(QWidget):
    """Visual template editor with drag & drop elements"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 600)
        self.content_type = "reel"
        
        # Content frame for aspect ratio guidance
        self.content_frame = QRect(50, 50, 300, 500)  # Default, will be recalculated
        self._need_frame_check = False
        
        # Picture-in-picture settings
        self.pip_enabled = True
        self.pip_shape = "square"  # "square" or "rectangle"
        self.pip_rect = QRect(50, 50, 100, 100)  # x, y, width, height
        self.pip_dragging = False
        self.pip_resizing = False
        
        # Text overlay settings
        self.text_enabled = True
        self.text_rect = QRect(50, 400, 200, 50)
        self.text_content = "Sample Text"
        self.text_size = 24
        self.text_dragging = False
        self.text_resizing = False
        
        # Mouse tracking
        self.last_mouse_pos = None
        self.setMouseTracking(True)

    def set_content_type(self, content_type: str):
        self.content_type = content_type.lower()
        self._ensure_elements_in_frame()
        self.update()

    def _ensure_elements_in_frame(self):
        """Ensure PiP and text elements are within the content frame"""
        # This will be called after content_frame is recalculated in paintEvent
        # We'll add a flag to trigger this after the next paint
        self._need_frame_check = True

    def set_pip_shape(self, shape: str):
        """Set picture-in-picture shape: 'square' or 'rectangle'"""
        self.pip_shape = shape
        if shape == "square":
            # Make it square
            size = min(self.pip_rect.width(), self.pip_rect.height())
            self.pip_rect.setSize(QSize(size, size))
        else:
            # Make it rectangle (16:9 aspect ratio)
            if self.pip_rect.width() < self.pip_rect.height():
                width = self.pip_rect.height() * 16 // 9
                self.pip_rect.setWidth(width)
        self.update()

    def set_text_size(self, size: int):
        self.text_size = size
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width, height = self.width(), self.height()
        
        # Background
        painter.fillRect(0, 0, width, height, QColor(30, 30, 30))
        
        # Draw content type layout with proper aspect ratio
        self._draw_content_frame(painter, width, height)
        
        # Title
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(20, 35, f"{self.content_type.title()} Template")
        
        # Picture-in-picture area
        if self.pip_enabled:
            self._draw_pip(painter)
        
        # Text overlay area
        if self.text_enabled:
            self._draw_text_overlay(painter)
    def _draw_content_frame(self, painter, canvas_width, canvas_height):
        """Draw content frame with proper aspect ratio for content type"""
        # Define aspect ratios for different content types
        aspect_ratios = {
            'reel': (9, 16),     # Vertical: 9:16 (Instagram Reels, TikTok)
            'story': (9, 16),    # Vertical: 9:16 (Instagram Stories)
            'teaser': (9, 16),   # Vertical: 9:16 (Short form content)
            'tutorial': (16, 9), # Horizontal: 16:9 (YouTube, longer content)
            'post': (1, 1)       # Square: 1:1 (Instagram Posts, LinkedIn)
        }
        
        # Get aspect ratio for current content type
        aspect_w, aspect_h = aspect_ratios.get(self.content_type, (9, 16))
        
        # Calculate frame size to fit in canvas with padding
        padding = 60  # Space around the frame
        available_width = canvas_width - 2 * padding
        available_height = canvas_height - 2 * padding - 50  # Extra space for title
        
        # Calculate frame dimensions maintaining aspect ratio
        if aspect_w > aspect_h:  # Landscape (tutorial)
            # For tutorials, make them much larger - use almost all available space
            frame_width = min(available_width * 0.95, available_height * aspect_w / aspect_h)
            frame_height = frame_width * aspect_h / aspect_w
            # If still too small, prioritize width to show 1920x1080 proportions better
            if frame_width < available_width * 0.8:
                frame_width = available_width * 0.9
                frame_height = frame_width * aspect_h / aspect_w
        elif aspect_w == aspect_h:  # Square (post)
            # For square posts, use a good size
            frame_size = min(available_width * 0.7, available_height * 0.7)
            frame_width = frame_height = frame_size
        else:  # Portrait (reel, story, teaser)
            frame_height = min(available_height, available_width * aspect_h / aspect_w)
            frame_width = frame_height * aspect_w / aspect_h
        
        # Center the frame
        frame_x = (canvas_width - frame_width) / 2
        frame_y = (canvas_height - frame_height) / 2 + 25  # Offset for title
        
        old_frame = self.content_frame
        self.content_frame = QRect(int(frame_x), int(frame_y), int(frame_width), int(frame_height))
        
        # Update PiP and text positions to be relative to the new frame
        self._update_elements_for_new_frame(old_frame)
        
        # Draw the content frame with thicker border for better visibility
        painter.setPen(QPen(QColor(150, 150, 150), 3))  # Thicker border
        painter.setBrush(QBrush(QColor(45, 45, 45)))  # Slightly lighter background
        painter.drawRect(self.content_frame)
        
        # Draw corner guides to show it's a bounded area
        corner_size = 15
        painter.setPen(QPen(QColor(200, 200, 0), 2))  # Yellow corners
        # Top-left corner
        painter.drawLine(self.content_frame.left(), self.content_frame.top() + corner_size, 
                        self.content_frame.left(), self.content_frame.top())
        painter.drawLine(self.content_frame.left(), self.content_frame.top(), 
                        self.content_frame.left() + corner_size, self.content_frame.top())
        # Top-right corner
        painter.drawLine(self.content_frame.right() - corner_size, self.content_frame.top(), 
                        self.content_frame.right(), self.content_frame.top())
        painter.drawLine(self.content_frame.right(), self.content_frame.top(), 
                        self.content_frame.right(), self.content_frame.top() + corner_size)
        # Bottom-left corner
        painter.drawLine(self.content_frame.left(), self.content_frame.bottom() - corner_size, 
                        self.content_frame.left(), self.content_frame.bottom())
        painter.drawLine(self.content_frame.left(), self.content_frame.bottom(), 
                        self.content_frame.left() + corner_size, self.content_frame.bottom())
        # Bottom-right corner
        painter.drawLine(self.content_frame.right() - corner_size, self.content_frame.bottom(), 
                        self.content_frame.right(), self.content_frame.bottom())
        painter.drawLine(self.content_frame.right(), self.content_frame.bottom(), 
                        self.content_frame.right(), self.content_frame.bottom() - corner_size)
        
        # Draw aspect ratio indicator with better formatting
        painter.setPen(QColor(200, 200, 200))
        font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(font)
        # Show actual resolution equivalents for better understanding
        if self.content_type == 'tutorial':
            ratio_text = f"Tutorial 16:9 • {int(frame_width)}×{int(frame_height)}px (≈1920×1080)"
        elif self.content_type == 'post':
            ratio_text = f"Post 1:1 • {int(frame_width)}×{int(frame_height)}px (Square)"
        else:
            ratio_text = f"Standard {aspect_w}:{aspect_h} • {int(frame_width)}×{int(frame_height)}px"
        painter.drawText(self.content_frame.left(), self.content_frame.bottom() + 20, ratio_text)
        
        # Ensure elements stay within frame after content type change
        if hasattr(self, '_need_frame_check') and self._need_frame_check:
            self._constrain_elements_to_frame()
            self._need_frame_check = False

    def _constrain_elements_to_frame(self):
        """Constrain PiP and text elements to stay within content frame"""
        # Constrain PiP
        if self.pip_rect.right() > self.content_frame.right():
            self.pip_rect.moveRight(self.content_frame.right())
        if self.pip_rect.bottom() > self.content_frame.bottom():
            self.pip_rect.moveBottom(self.content_frame.bottom())
        if self.pip_rect.left() < self.content_frame.left():
            self.pip_rect.moveLeft(self.content_frame.left())
        if self.pip_rect.top() < self.content_frame.top():
            self.pip_rect.moveTop(self.content_frame.top())
            
        # Constrain text
        if self.text_rect.right() > self.content_frame.right():
            self.text_rect.moveRight(self.content_frame.right())
        if self.text_rect.bottom() > self.content_frame.bottom():
            self.text_rect.moveBottom(self.content_frame.bottom())
        if self.text_rect.left() < self.content_frame.left():
            self.text_rect.moveLeft(self.content_frame.left())
        if self.text_rect.top() < self.content_frame.top():
            self.text_rect.moveTop(self.content_frame.top())
    def _update_elements_for_new_frame(self, old_frame):
        """Update element positions when content frame changes"""
        if old_frame.isNull() or old_frame.width() == 0 or old_frame.height() == 0:
            # First time initialization - position elements relative to new frame
            self._position_elements_relative_to_frame()
            return
        
        # Calculate scaling factors between old and new frames
        scale_x = self.content_frame.width() / old_frame.width()
        scale_y = self.content_frame.height() / old_frame.height()
        
        # Calculate offset between old and new frame positions
        offset_x = self.content_frame.x() - old_frame.x()
        offset_y = self.content_frame.y() - old_frame.y()
        
        # Update PiP position and size relative to the new frame
        old_pip_rel_x = self.pip_rect.x() - old_frame.x()
        old_pip_rel_y = self.pip_rect.y() - old_frame.y()
        
        new_pip_x = self.content_frame.x() + (old_pip_rel_x * scale_x)
        new_pip_y = self.content_frame.y() + (old_pip_rel_y * scale_y)
        new_pip_width = self.pip_rect.width() * scale_x
        new_pip_height = self.pip_rect.height() * scale_y
        
        self.pip_rect = QRect(int(new_pip_x), int(new_pip_y), int(new_pip_width), int(new_pip_height))
        
        # Update text position and size relative to the new frame
        old_text_rel_x = self.text_rect.x() - old_frame.x()
        old_text_rel_y = self.text_rect.y() - old_frame.y()
        
        new_text_x = self.content_frame.x() + (old_text_rel_x * scale_x)
        new_text_y = self.content_frame.y() + (old_text_rel_y * scale_y)
        new_text_width = self.text_rect.width() * scale_x
        new_text_height = self.text_rect.height() * scale_y
        
        self.text_rect = QRect(int(new_text_x), int(new_text_y), int(new_text_width), int(new_text_height))
        
        # Ensure elements stay within the new frame bounds
        self._constrain_elements_to_frame()

    def _position_elements_relative_to_frame(self):
        """Position elements relative to the content frame for the first time"""
        # Position PiP in top-left area of content frame
        pip_x = self.content_frame.x() + 20
        pip_y = self.content_frame.y() + 20
        pip_size = min(100, self.content_frame.width() // 4, self.content_frame.height() // 4)
        
        if self.pip_shape == "rectangle":
            pip_width = min(120, self.content_frame.width() // 3)
            pip_height = min(80, pip_width * 9 // 16)  # 16:9 aspect ratio
        else:
            pip_width = pip_height = pip_size
        
        self.pip_rect = QRect(pip_x, pip_y, pip_width, pip_height)
        
        # Position text overlay in bottom area of content frame
        text_width = min(200, self.content_frame.width() - 40)
        text_height = min(50, self.content_frame.height() // 8)
        text_x = self.content_frame.x() + 20
        text_y = self.content_frame.bottom() - text_height - 20
        
        self.text_rect = QRect(text_x, text_y, text_width, text_height)
        
        # Ensure elements are within bounds
        self._constrain_elements_to_frame()

    def _draw_pip(self, painter):
        """Draw picture-in-picture area"""
        # Main area
        painter.setPen(QPen(QColor(0, 120, 212), 2))
        painter.setBrush(QBrush(QColor(0, 120, 212, 30)))
        painter.drawRect(self.pip_rect)
        
        # Corner resize handle
        handle_size = 10
        handle_rect = QRect(
            self.pip_rect.right() - handle_size,
            self.pip_rect.bottom() - handle_size,
            handle_size, handle_size
        )
        painter.setPen(QPen(QColor(0, 120, 212), 2))
        painter.setBrush(QBrush(QColor(0, 120, 212)))
        painter.drawRect(handle_rect)
        
        # Label
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10)
        painter.setFont(font)
        text_y = self.pip_rect.top() - 5
        painter.drawText(self.pip_rect.left(), text_y, f"PiP ({self.pip_shape})")

    def _draw_text_overlay(self, painter):
        """Draw text overlay area"""
        # Text background
        painter.setPen(QPen(QColor(82, 199, 89), 2))
        painter.setBrush(QBrush(QColor(82, 199, 89, 30)))
        painter.drawRect(self.text_rect)
        
        # Sample text
        font = QFont("Arial", max(8, self.text_size // 2))
        painter.setFont(font)
        painter.setPen(QColor(255, 255, 255))
        painter.drawText(self.text_rect, Qt.AlignmentFlag.AlignCenter, self.text_content)
        
        # Corner resize handle
        handle_size = 10
        handle_rect = QRect(
            self.text_rect.right() - handle_size,
            self.text_rect.bottom() - handle_size,
            handle_size, handle_size
        )
        painter.setPen(QPen(QColor(82, 199, 89), 2))
        painter.setBrush(QBrush(QColor(82, 199, 89)))
        painter.drawRect(handle_rect)
        
        # Label
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10)
        painter.setFont(font)
        text_y = self.text_rect.top() - 5
        painter.drawText(self.text_rect.left(), text_y, f"Text ({self.text_size}px)")

    def mousePressEvent(self, event):
        pos = event.position().toPoint()
        
        # Check PiP resize handle
        if self.pip_enabled:
            handle_rect = QRect(
                self.pip_rect.right() - 10,
                self.pip_rect.bottom() - 10,
                10, 10
            )
            if handle_rect.contains(pos):
                self.pip_resizing = True
                self.last_mouse_pos = pos
                return
        
        # Check text resize handle
        if self.text_enabled:
            handle_rect = QRect(
                self.text_rect.right() - 10,
                self.text_rect.bottom() - 10,
                10, 10
            )
            if handle_rect.contains(pos):
                self.text_resizing = True
                self.last_mouse_pos = pos
                return
        
        # Check PiP dragging
        if self.pip_enabled and self.pip_rect.contains(pos):
            self.pip_dragging = True
            self.last_mouse_pos = pos
            return
        
        # Check text dragging
        if self.text_enabled and self.text_rect.contains(pos):
            self.text_dragging = True
            self.last_mouse_pos = pos
            return

    def mouseMoveEvent(self, event):
        if not self.last_mouse_pos:
            return
            
        pos = event.position().toPoint()
        delta = pos - self.last_mouse_pos
        
        if self.pip_resizing:
            # Resize PiP
            new_width = max(50, self.pip_rect.width() + delta.x())
            new_height = max(50, self.pip_rect.height() + delta.y())
            
            if self.pip_shape == "square":
                # Keep it square
                size = max(new_width, new_height)
                new_width = new_height = size
            
            # Constrain to content frame
            max_width = self.content_frame.right() - self.pip_rect.left()
            max_height = self.content_frame.bottom() - self.pip_rect.top()
            new_width = min(new_width, max_width)
            new_height = min(new_height, max_height)
            
            self.pip_rect.setSize(QSize(new_width, new_height))
            
        elif self.text_resizing:
            # Resize text area
            new_width = max(100, self.text_rect.width() + delta.x())
            new_height = max(30, self.text_rect.height() + delta.y())
            
            # Constrain to content frame
            max_width = self.content_frame.right() - self.text_rect.left()
            max_height = self.content_frame.bottom() - self.text_rect.top()
            new_width = min(new_width, max_width)
            new_height = min(new_height, max_height)
            
            self.text_rect.setSize(QSize(new_width, new_height))
            
        elif self.pip_dragging:
            # Move PiP
            new_rect = self.pip_rect.translated(delta)
            
            # Constrain to content frame
            if new_rect.left() < self.content_frame.left():
                new_rect.moveLeft(self.content_frame.left())
            if new_rect.top() < self.content_frame.top():
                new_rect.moveTop(self.content_frame.top())
            if new_rect.right() > self.content_frame.right():
                new_rect.moveRight(self.content_frame.right())
            if new_rect.bottom() > self.content_frame.bottom():
                new_rect.moveBottom(self.content_frame.bottom())
            
            self.pip_rect = new_rect
            
        elif self.text_dragging:
            # Move text
            new_rect = self.text_rect.translated(delta)
            
            # Constrain to content frame
            if new_rect.left() < self.content_frame.left():
                new_rect.moveLeft(self.content_frame.left())
            if new_rect.top() < self.content_frame.top():
                new_rect.moveTop(self.content_frame.top())
            if new_rect.right() > self.content_frame.right():
                new_rect.moveRight(self.content_frame.right())
            if new_rect.bottom() > self.content_frame.bottom():
                new_rect.moveBottom(self.content_frame.bottom())
            
            self.text_rect = new_rect
        
        self.last_mouse_pos = pos
        self.update()

    def mouseReleaseEvent(self, event):
        # Check if we were dragging/resizing and need to save changes
        was_modifying = (self.pip_dragging or self.pip_resizing or 
                        self.text_dragging or self.text_resizing)
        
        self.pip_dragging = False
        self.pip_resizing = False
        self.text_dragging = False
        self.text_resizing = False
        self.last_mouse_pos = None
        
        # Emit signal to save changes if we were modifying
        if was_modifying:
            # Use direct reference if available, otherwise try parent
            template_editor = getattr(self, 'template_editor', None) or self.parent()
            
            if template_editor and hasattr(template_editor, '_save_all_current_settings'):
                template_editor._save_all_current_settings()
                # Also auto-save to project
                if hasattr(template_editor, '_auto_save_to_project'):
                    template_editor._auto_save_to_project()


class SimpleTemplateEditor(QWidget):
    """Simple template editor with per-content-type settings"""
    template_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.loading_project = False  # Flag to prevent auto-save during project loading
        
        # Per-content-type settings - EVERYTHING independent per type
        self.content_settings = {
            'reel': {
                'fixed_intro': False, 
                'fixed_outro': False,
                'intro_asset': None,  # Asset path or None for AI decision
                'outro_asset': None,  # Asset path or None for AI decision
                'intro_length': 0.0,  # Length in seconds, 0.0 for AI decision
                'outro_length': 0.0,  # Length in seconds, 0.0 for AI decision
                'pip_enabled': True,
                'pip_shape': 'square',
                'pip_rect': [80, 80, 100, 100],  # x, y, width, height - top area for vertical
                'text_enabled': True,
                'text_size': 24,
                'text_rect': [80, 450, 180, 50]  # Bottom area for vertical
            },
            'story': {
                'fixed_intro': False, 
                'fixed_outro': False,
                'intro_asset': None,
                'outro_asset': None,
                'intro_length': 0.0,
                'outro_length': 0.0,
                'pip_enabled': True,
                'pip_shape': 'square',
                'pip_rect': [80, 80, 100, 100],  # Top area for vertical
                'text_enabled': True,
                'text_size': 24,
                'text_rect': [80, 450, 180, 50]  # Bottom area for vertical
            },
            'teaser': {
                'fixed_intro': False, 
                'fixed_outro': False,
                'intro_asset': None,
                'outro_asset': None,
                'intro_length': 0.0,
                'outro_length': 0.0,
                'pip_enabled': True,
                'pip_shape': 'square',
                'pip_rect': [80, 80, 100, 100],  # Top area for vertical
                'text_enabled': True,
                'text_size': 24,
                'text_rect': [80, 450, 180, 50]  # Bottom area for vertical
            },
            'tutorial': {
                'fixed_intro': False, 
                'fixed_outro': False,
                'intro_asset': None,
                'outro_asset': None,
                'intro_length': 0.0,
                'outro_length': 0.0,
                'pip_enabled': True,
                'pip_shape': 'rectangle',  # Rectangle better for horizontal layout
                'pip_rect': [50, 50, 120, 80],  # Wider for horizontal content
                'text_enabled': True,
                'text_size': 24,
                'text_rect': [50, 200, 250, 50]  # More space for horizontal
            },
            'post': {
                'fixed_intro': False, 
                'fixed_outro': False,
                'intro_asset': None,
                'outro_asset': None,
                'intro_length': 0.0,
                'outro_length': 0.0,
                'pip_enabled': True,
                'pip_shape': 'square',  # Square fits well in square content
                'pip_rect': [60, 60, 100, 100],  # Center-ish for square content
                'text_enabled': True,
                'text_size': 24,
                'text_rect': [60, 300, 200, 50]  # Bottom area for square
            }
        }
        
        self.current_content_type = "reel"
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Setup simple UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel - Visual editor
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { background: #2d2d2d; border-radius: 8px; }")
        left_layout = QVBoxLayout(left_panel)
        
        # Content type selector
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Content Type:"))
        self.content_type_selector = QComboBox()
        self.content_type_selector.addItems(["Reel", "Story", "Teaser", "Tutorial", "Post"])
        type_layout.addWidget(self.content_type_selector)
        type_layout.addStretch()
        left_layout.addLayout(type_layout)
        
        # Visual editor
        self.visual_editor = VisualTemplateEditor(self)
        self.visual_editor.template_editor = self  # Direct reference for callbacks
        left_layout.addWidget(self.visual_editor)
        
        # Right panel - Settings
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { background: #2d2d2d; border-radius: 8px; }")
        right_panel.setMaximumWidth(300)
        right_layout = QVBoxLayout(right_panel)
        
        self._create_settings(right_layout)
        
        # Add panels
        main_layout.addWidget(left_panel, 2)
        main_layout.addWidget(right_panel, 1)

    def _create_settings(self, layout):
        """Create settings panel"""
        
        # Intro/Outro Settings
        intro_outro_group = QGroupBox("Intro/Outro Settings")
        intro_outro_layout = QVBoxLayout(intro_outro_group)
        
        self.fixed_intro = QCheckBox("Fixed Intro (choose specific asset)")
        self.fixed_outro = QCheckBox("Fixed Outro (choose specific asset)")
        
        intro_outro_layout.addWidget(self.fixed_intro)
        intro_outro_layout.addWidget(self.fixed_outro)
        
        # Intro asset selection
        intro_asset_layout = QHBoxLayout()
        intro_asset_layout.addWidget(QLabel("Intro Asset:"))
        self.intro_asset_combo = QComboBox()
        self.intro_asset_combo.addItem("AI decides", None)
        intro_asset_layout.addWidget(self.intro_asset_combo)
        intro_outro_layout.addLayout(intro_asset_layout)
        
        # Intro length
        intro_length_layout = QHBoxLayout()
        intro_length_layout.addWidget(QLabel("Intro Length:"))
        self.intro_length_spin = QDoubleSpinBox()
        self.intro_length_spin.setRange(0.0, 30.0)
        self.intro_length_spin.setSuffix(" sec")
        self.intro_length_spin.setSpecialValueText("AI decides")
        self.intro_length_spin.setValue(0.0)
        intro_length_layout.addWidget(self.intro_length_spin)
        intro_outro_layout.addLayout(intro_length_layout)
        
        # Outro asset selection
        outro_asset_layout = QHBoxLayout()
        outro_asset_layout.addWidget(QLabel("Outro Asset:"))
        self.outro_asset_combo = QComboBox()
        self.outro_asset_combo.addItem("AI decides", None)
        outro_asset_layout.addWidget(self.outro_asset_combo)
        intro_outro_layout.addLayout(outro_asset_layout)
        
        # Outro length
        outro_length_layout = QHBoxLayout()
        outro_length_layout.addWidget(QLabel("Outro Length:"))
        self.outro_length_spin = QDoubleSpinBox()
        self.outro_length_spin.setRange(0.0, 30.0)
        self.outro_length_spin.setSuffix(" sec")
        self.outro_length_spin.setSpecialValueText("AI decides")
        self.outro_length_spin.setValue(0.0)
        outro_length_layout.addWidget(self.outro_length_spin)
        intro_outro_layout.addLayout(outro_length_layout)
        
        help_label = QLabel("Unchecked = AI will manage based on project assets\nLength 0.0 = AI decides duration")
        help_label.setStyleSheet("color: #888; font-size: 11px;")
        help_label.setWordWrap(True)
        intro_outro_layout.addWidget(help_label)
        
        layout.addWidget(intro_outro_group)
        
        # Picture-in-Picture Settings
        pip_group = QGroupBox("Picture-in-Picture")
        pip_layout = QVBoxLayout(pip_group)
        
        self.pip_enabled = QCheckBox("Enable Picture-in-Picture")
        self.pip_enabled.setChecked(True)
        pip_layout.addWidget(self.pip_enabled)
        
        # Shape selection
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(QLabel("Shape:"))
        self.pip_square = QCheckBox("Square")
        self.pip_rectangle = QCheckBox("Rectangle")
        self.pip_square.setChecked(True)
        shape_layout.addWidget(self.pip_square)
        shape_layout.addWidget(self.pip_rectangle)
        pip_layout.addLayout(shape_layout)
        
        pip_help = QLabel("Drag to move, drag corner to resize")
        pip_help.setStyleSheet("color: #888; font-size: 11px;")
        pip_layout.addWidget(pip_help)
        
        layout.addWidget(pip_group)
        
        # Text Overlay Settings
        text_group = QGroupBox("Text Overlay")
        text_layout = QVBoxLayout(text_group)
        
        self.text_enabled = QCheckBox("Enable Text Overlay")
        self.text_enabled.setChecked(True)
        text_layout.addWidget(self.text_enabled)
        
        # Text size
        size_layout = QHBoxLayout()
        size_layout.addWidget(QLabel("Size:"))
        self.text_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.text_size_slider.setRange(12, 72)
        self.text_size_slider.setValue(24)
        self.text_size_label = QLabel("24px")
        size_layout.addWidget(self.text_size_slider)
        size_layout.addWidget(self.text_size_label)
        text_layout.addLayout(size_layout)
        
        text_help = QLabel("Drag to move, drag corner to resize")
        text_help.setStyleSheet("color: #888; font-size: 11px;")
        text_layout.addWidget(text_help)
        
        layout.addWidget(text_group)
        
        # Actions - removed useless Save Template button since everything auto-saves
        layout.addStretch()

    def _setup_connections(self):
        """Setup connections"""
        self.content_type_selector.currentTextChanged.connect(self._on_content_type_changed)
        
        # Intro/outro settings
        self.fixed_intro.toggled.connect(self._on_intro_outro_changed)
        self.fixed_outro.toggled.connect(self._on_intro_outro_changed)
        self.intro_asset_combo.currentIndexChanged.connect(self._on_intro_outro_changed)
        self.outro_asset_combo.currentIndexChanged.connect(self._on_intro_outro_changed)
        self.intro_length_spin.valueChanged.connect(self._on_intro_outro_changed)
        self.outro_length_spin.valueChanged.connect(self._on_intro_outro_changed)
        
        # PiP settings
        self.pip_enabled.toggled.connect(self._on_pip_settings_changed)
        self.pip_square.toggled.connect(self._on_pip_shape_changed)
        self.pip_rectangle.toggled.connect(self._on_pip_shape_changed)
        
        # Text settings
        self.text_enabled.toggled.connect(self._on_text_settings_changed)
        self.text_size_slider.valueChanged.connect(self._on_text_size_changed)
        
        # Initialize with first content type
        self._load_all_settings_for_current_type()
        
        # Populate asset combos initially
        self._populate_asset_combos()

    def _on_content_type_changed(self, content_type: str):
        """Handle content type change - SAVE CURRENT, LOAD NEW"""
        # Save ALL current settings (intro/outro + visual elements)
        self._save_all_current_settings()
        
        # Switch to new type
        self.current_content_type = content_type.lower()
        self.visual_editor.set_content_type(content_type)
        
        # Load ALL settings for new type
        self._load_all_settings_for_current_type()
        
        # Auto-save to project immediately
        self._auto_save_to_project()
        
        self.template_changed.emit()

    def _save_all_current_settings(self):
        """Save ALL current settings including visual elements"""
        self.content_settings[self.current_content_type] = {
            'fixed_intro': self.fixed_intro.isChecked(),
            'fixed_outro': self.fixed_outro.isChecked(),
            'intro_asset': self.intro_asset_combo.currentData(),
            'outro_asset': self.outro_asset_combo.currentData(),
            'intro_length': self.intro_length_spin.value(),
            'outro_length': self.outro_length_spin.value(),
            'pip_enabled': self.visual_editor.pip_enabled,
            'pip_shape': self.visual_editor.pip_shape,
            'pip_rect': [
                self.visual_editor.pip_rect.x(),
                self.visual_editor.pip_rect.y(),
                self.visual_editor.pip_rect.width(),
                self.visual_editor.pip_rect.height()
            ],
            'text_enabled': self.visual_editor.text_enabled,
            'text_size': self.visual_editor.text_size,
            'text_rect': [
                self.visual_editor.text_rect.x(),
                self.visual_editor.text_rect.y(),
                self.visual_editor.text_rect.width(),
                self.visual_editor.text_rect.height()
            ]
        }

    def _load_all_settings_for_current_type(self):
        """Load ALL settings for current content type"""
        # Ensure the content type exists in settings (for backward compatibility)
        if self.current_content_type not in self.content_settings:
            print(f"Content type '{self.current_content_type}' not found in settings. Creating default settings.")
            self._create_default_settings_for_type(self.current_content_type)
        
        settings = self.content_settings[self.current_content_type]
        
        # Update UI checkboxes
        self.fixed_intro.setChecked(settings['fixed_intro'])
        self.fixed_outro.setChecked(settings['fixed_outro'])
        
        # Update asset selections (find by data value)
        self._set_combo_by_data(self.intro_asset_combo, settings.get('intro_asset'))
        self._set_combo_by_data(self.outro_asset_combo, settings.get('outro_asset'))
        
        # Update length settings
        self.intro_length_spin.setValue(settings.get('intro_length', 0.0))
        self.outro_length_spin.setValue(settings.get('outro_length', 0.0))
        
        # Update PiP settings
        self.pip_enabled.setChecked(settings['pip_enabled'])
        if settings['pip_shape'] == 'square':
            self.pip_square.setChecked(True)
            self.pip_rectangle.setChecked(False)
        else:
            self.pip_square.setChecked(False)
            self.pip_rectangle.setChecked(True)
        
        # Update text settings
        self.text_enabled.setChecked(settings['text_enabled'])
        self.text_size_slider.setValue(settings['text_size'])
        self.text_size_label.setText(f"{settings['text_size']}px")
        
        # Update visual editor
        self.visual_editor.pip_enabled = settings['pip_enabled']
        self.visual_editor.pip_shape = settings['pip_shape']
        self.visual_editor.pip_rect = QRect(*settings['pip_rect'])
        self.visual_editor.text_enabled = settings['text_enabled']
        self.visual_editor.text_size = settings['text_size']
        self.visual_editor.text_rect = QRect(*settings['text_rect'])
        self.visual_editor.update()

    def _set_combo_by_data(self, combo, data_value):
        """Set combo box selection by data value"""
        for i in range(combo.count()):
            if combo.itemData(i) == data_value:
                combo.setCurrentIndex(i)
                return
        # If not found, set to first item (AI decides)
        combo.setCurrentIndex(0)

    def _save_current_settings(self):
        """Save current UI settings to content_settings - LEGACY METHOD"""
        self._save_all_current_settings()

    def _update_ui_from_settings(self):
        """Update UI from content_settings - LEGACY METHOD"""
        self._load_all_settings_for_current_type()

    def _on_intro_outro_changed(self):
        """Handle intro/outro checkbox changes"""
        self._save_all_current_settings()
        # Auto-save to project immediately
        self._auto_save_to_project()
        self.template_changed.emit()

    def _on_pip_settings_changed(self):
        """Handle PiP settings changes"""
        self.visual_editor.pip_enabled = self.pip_enabled.isChecked()
        self.visual_editor.update()
        self._save_all_current_settings()
        # Auto-save to project immediately
        self._auto_save_to_project()

    def _on_pip_shape_changed(self):
        """Handle PiP shape changes"""
        if self.pip_square.isChecked():
            self.pip_rectangle.setChecked(False)
            self.visual_editor.set_pip_shape("square")
        elif self.pip_rectangle.isChecked():
            self.pip_square.setChecked(False)
            self.visual_editor.set_pip_shape("rectangle")
        self._save_all_current_settings()
        # Auto-save to project immediately
        self._auto_save_to_project()

    def _on_text_settings_changed(self):
        """Handle text settings changes"""
        self.visual_editor.text_enabled = self.text_enabled.isChecked()
        self.visual_editor.update()
        self._save_all_current_settings()
        # Auto-save to project immediately
        self._auto_save_to_project()

    def _on_text_size_changed(self, size):
        """Handle text size changes"""
        self.text_size_label.setText(f"{size}px")
        self.visual_editor.set_text_size(size)
        self._save_all_current_settings()
        # Auto-save to project immediately
        self._auto_save_to_project()

    def _auto_save_to_project(self):
        """Automatically save template settings to project"""
        if self.project and not self.loading_project:
            config = self.get_template_config()
            self.project.simple_templates = config
            print("Auto-saved template settings to project")

    def _create_default_settings_for_type(self, content_type):
        """Create default settings for a content type that doesn't exist in saved settings"""
        # Get current content frame to calculate relative positions
        frame = self.visual_editor.content_frame if hasattr(self, 'visual_editor') else QRect(50, 50, 300, 500)
        
        # Calculate relative positions based on content frame
        pip_x = frame.x() + 20
        pip_y = frame.y() + 20
        text_x = frame.x() + 20
        text_y = frame.bottom() - 70  # 50px height + 20px margin
        
        # Default settings template with relative positioning
        default_settings = {
            'fixed_intro': False, 
            'fixed_outro': False,
            'intro_asset': None,
            'outro_asset': None,
            'intro_length': 0.0,
            'outro_length': 0.0,
            'pip_enabled': True,
            'pip_shape': 'square',
            'pip_rect': [pip_x, pip_y, 100, 100],
            'text_enabled': True,
            'text_size': 24,
            'text_rect': [text_x, text_y, 180, 50]
        }
        
        # Customize based on content type
        if content_type == 'tutorial':
            default_settings['pip_shape'] = 'rectangle'
            default_settings['pip_rect'] = [pip_x, pip_y, 120, 80]
            # For horizontal content, place text in middle area
            default_settings['text_rect'] = [pip_x, frame.y() + frame.height()//2, 250, 50]
        elif content_type == 'post':
            # For square content, center the text more
            default_settings['text_rect'] = [text_x, frame.y() + frame.height()//2 + 50, 200, 50]
        
        # Add to content_settings
        self.content_settings[content_type] = default_settings
        print(f"Created default settings for content type: {content_type}")


    def set_project(self, project):
        """Set project and populate asset combos"""
        self.project = project
        
        # Temporarily disable auto-save during project loading
        self.loading_project = True
        
        # First populate the asset combos with new project assets
        self._populate_asset_combos()
        
        # Then load any saved template settings from the project
        if self.project and hasattr(self.project, 'simple_templates'):
            try:
                self.load_template_config(self.project.simple_templates)
                print("Loaded template settings from project")
            except Exception as e:
                print(f"Could not load template settings from project: {e}")
        else:
            # Refresh the UI to show the current settings with new assets
            self._load_all_settings_for_current_type()
        
        # Re-enable auto-save
        self.loading_project = False

    def _populate_asset_combos(self):
        """Populate intro/outro asset combo boxes with project assets"""
        # Clear existing items except "AI decides"
        self.intro_asset_combo.clear()
        self.outro_asset_combo.clear()
        
        # Always add "AI decides" as first option
        self.intro_asset_combo.addItem("AI decides", None)
        self.outro_asset_combo.addItem("AI decides", None)
        
        # Add project assets if available
        if self.project:
            try:
                # Try different ways to get assets from the project
                assets = []
                
                # Method 1: Check if project has assets dictionary
                if hasattr(self.project, 'assets') and self.project.assets:
                    for asset_path, asset_info in self.project.assets.items():
                        if isinstance(asset_info, dict):
                            asset_name = asset_info.get('name', asset_path.split('/')[-1])
                            assets.append((asset_name, asset_path))
                        else:
                            # If asset_info is just a string/path
                            asset_name = str(asset_info).split('/')[-1]
                            assets.append((asset_name, str(asset_info)))
                
                # Method 2: Check if project has get_assets method
                elif hasattr(self.project, 'get_assets'):
                    project_assets = self.project.get_assets()
                    for asset in project_assets:
                        if hasattr(asset, 'name') and hasattr(asset, 'path'):
                            assets.append((asset.name, asset.path))
                        else:
                            asset_name = str(asset).split('/')[-1]
                            assets.append((asset_name, str(asset)))
                
                # Method 3: Check if project has files list
                elif hasattr(self.project, 'files'):
                    for file_path in self.project.files:
                        if any(file_path.lower().endswith(ext) for ext in ['.mp4', '.mov', '.avi', '.mkv', '.webm']):
                            asset_name = file_path.split('/')[-1]
                            assets.append((asset_name, file_path))
                
                # Add assets to combos
                for asset_name, asset_path in assets:
                    self.intro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)
                    self.outro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)
                
                print(f"Added {len(assets)} assets to combos")
                
            except Exception as e:
                print(f"Error loading project assets: {e}")
                # Add some placeholder assets for testing
                placeholder_assets = [
                    ("intro_brand.mp4", "/path/to/intro_brand.mp4"),
                    ("intro_music.mp4", "/path/to/intro_music.mp4"), 
                    ("outro_subscribe.mp4", "/path/to/outro_subscribe.mp4"),
                    ("outro_logo.mp4", "/path/to/outro_logo.mp4")
                ]
                for asset_name, asset_path in placeholder_assets:
                    self.intro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)
                    self.outro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)
        else:
            # No project loaded, add placeholder assets for testing
            placeholder_assets = [
                ("intro_brand.mp4", "/path/to/intro_brand.mp4"),
                ("intro_music.mp4", "/path/to/intro_music.mp4"), 
                ("outro_subscribe.mp4", "/path/to/outro_subscribe.mp4"),
                ("outro_logo.mp4", "/path/to/outro_logo.mp4")
            ]
            for asset_name, asset_path in placeholder_assets:
                self.intro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)
                self.outro_asset_combo.addItem(f"🎬 {asset_name}", asset_path)

    def get_template_config(self):
        """Get current template configuration for all content types"""
        return {
            'content_settings': self.content_settings,
            'current_content_type': self.current_content_type
        }

    def load_template_config(self, config):
        """Load template configuration"""
        print(f"Loading template config: {config.keys() if config else 'None'}")
        
        if 'content_settings' in config:
            self.content_settings = config['content_settings']
            print(f"Loaded settings for content types: {list(self.content_settings.keys())}")
        
        if 'current_content_type' in config:
            self.current_content_type = config['current_content_type']
            # Update UI to reflect loaded content type
            for i in range(self.content_type_selector.count()):
                if self.content_type_selector.itemText(i).lower() == self.current_content_type:
                    self.content_type_selector.setCurrentIndex(i)
                    break
            print(f"Set current content type to: {self.current_content_type}")
        
        # Reload current settings
        self._load_all_settings_for_current_type()
        print("Template configuration loaded successfully")


# For backward compatibility, alias the main class
AITemplateEditor = SimpleTemplateEditor
