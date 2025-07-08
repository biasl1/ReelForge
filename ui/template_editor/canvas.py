"""
Interactive canvas for template editing with drag and element manipulation.
"""
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QSize, QPointF, QPoint
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QBrush, QWheelEvent, QMouseEvent

from .utils import (
    get_content_dimensions, 
    get_canvas_size
)


class TemplateCanvas(QWidget):
    """
    Interactive canvas for template editing with element manipulation.
    No zoom/pan - clean, centered layout with reset functionality.
    """
    
    # Signals
    element_moved = pyqtSignal(str, QRect)  # element_type, new_rect
    element_resized = pyqtSignal(str, QRect)  # element_type, new_rect
    element_selected = pyqtSignal(str)  # element_type
    canvas_clicked = pyqtSignal(QPointF)  # click position
    reset_positions_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 600)
        self.setMouseTracking(True)
        self.content_type = "reel"
        self.content_frame = QRect(50, 50, 300, 500)
        self._need_frame_check = False
        
        # Content-specific state storage - CRITICAL for independence!
        self.content_states = {}  # Store elements, frame, etc. per content type
        self._initialize_content_states()
        
        # Constraint settings
        self.constrain_to_frame = False
        self.snap_to_grid = False
        self.grid_size = 10
        
        # Elements and selection
        self.elements = {}
        self.selected_element = None
        self.dragging_element = None
        self.resizing_element = None
        self.resize_handle = None
        self.drag_start_pos = None
        self.original_rect = None
        
        # Initialize default elements for current content type
        self._setup_content_type_elements(self.content_type)
        
        # Connect reset positions
        if hasattr(self, 'reset_positions_requested'):
            self.reset_positions_requested.connect(self.reset_positions)
    
    def _initialize_content_states(self):
        """Initialize separate states for each content type - CRITICAL for independence!"""
        content_types = ['reel', 'story', 'post', 'teaser', 'tutorial']
        for content_type in content_types:
            self.content_states[content_type] = {
                'elements': {},
                'content_frame': QRect(50, 50, 300, 500),
                'constrain_to_frame': False
                # REMOVE 'zoom', 'pan'
            }
    
    def _setup_default_elements(self):
        """Setup default elements for the current content type."""
        defaults = {
            'reel': {
                'pip': {
                    'type': 'pip',
                    'enabled': True,
                    'rect': QRect(50, 50, 100, 100),
                    'use_plugin_aspect_ratio': False,  # Toggle for using .adsp aspect ratio
                    'plugin_aspect_ratio': 1.75,      # Default plugin aspect ratio (700x400)  
                    'plugin_file_path': '',           # Path to .adsp file
                    'corner_radius': 8,               # Corner roundness (0-50)
                    'shape': 'rectangle',             # 'square' or 'rectangle'
                    'color': QColor(100, 150, 200, 128),
                    'border_color': QColor(255, 255, 255),
                    'border_width': 2
                },
                'title': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 80, 200, 60),
                    'content': "Main Title",
                    'size': 36,
                    'color': QColor(255, 255, 255),
                    'style': 'bold'
                },
                'subtitle': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 450, 200, 40),
                    'content': "Subtitle text here",
                    'size': 18,
                    'color': QColor(200, 200, 200),
                    'style': 'normal'
                }
            },
            'story': {
                'title': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 50, 300, 80),
                    'content': "Story Title",
                    'size': 32,
                    'color': QColor(255, 255, 255),
                    'style': 'bold'
                },
                'body': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 150, 300, 300),
                    'content': "Once upon a time...",
                    'size': 18,
                    'color': QColor(255, 255, 255),
                    'style': 'normal'
                }
            },
            'post': {
                'image': {
                    'type': 'pip',
                    'enabled': True,
                    'rect': QRect(50, 50, 300, 200),
                    'use_plugin_aspect_ratio': False,  # Toggle for using .adsp aspect ratio
                    'plugin_aspect_ratio': 1.75,      # Default plugin aspect ratio (700x400)
                    'plugin_file_path': '',           # Path to .adsp file  
                    'corner_radius': 12,              # Corner roundness (0-50)
                    'shape': 'rectangle',
                    'color': QColor(100, 150, 200, 128),
                    'border_color': QColor(255, 255, 255),
                    'border_width': 2
                },
                'caption': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 260, 300, 60),
                    'content': "Caption for the post image.",
                    'size': 18,
                    'color': QColor(255, 255, 255),
                    'style': 'normal'
                }
            },
            'teaser': {
                'title': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 50, 250, 70),
                    'content': "Teaser Title",
                    'size': 28,
                    'color': QColor(255, 255, 255),
                    'style': 'bold'
                },
                'preview': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 130, 250, 50),
                    'content': "Exciting preview of the content...",
                    'size': 16,
                    'color': QColor(200, 200, 200),
                    'style': 'normal'
                }
            },
            'tutorial': {
                'title': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 50, 300, 80),
                    'content': "Tutorial Title",
                    'size': 32,
                    'color': QColor(255, 255, 255),
                    'style': 'bold'
                },
                'steps': {
                    'type': 'text',
                    'enabled': True,
                    'rect': QRect(50, 150, 300, 300),
                    'content': "1. Step one...\n2. Step two...\n3. Step three...",
                    'size': 18,
                    'color': QColor(255, 255, 255),
                    'style': 'normal'
                }
            }
        }
        
        # Clear existing elements
        self.elements = {}
        
        # Setup new defaults
        if self.content_type in defaults:
            for element_id, element in defaults[self.content_type].items():
                self.elements[element_id] = element
    
    def set_content_type(self, content_type: str):
        """Set the content type and switch to its independent state."""
        new_content_type = content_type.lower()
        
        # If switching to a different content type, save current state first
        if new_content_type != self.content_type:
            self._save_current_state()
        
        # Switch to new content type
        self.content_type = new_content_type
        
        # Load the state for the new content type
        self._load_content_state()
        
        self._need_frame_check = True
        self.update()
    
    def _save_current_state(self):
        """Save current canvas state for the current content type."""
        if self.content_type in self.content_states:
            state = self.content_states[self.content_type]
            
            # Deep copy elements to avoid reference issues
            import copy
            state['elements'] = copy.deepcopy(self.elements)
            state['content_frame'] = QRect(self.content_frame)
            state['constrain_to_frame'] = self.constrain_to_frame
            # REMOVE zoom/pan
    
    def _load_content_state(self):
        """Load state for the current content type."""
        if self.content_type not in self.content_states:
            # Initialize if not exists
            self.content_states[self.content_type] = {
                'elements': {},
                'content_frame': QRect(50, 50, 300, 500),
                'constrain_to_frame': False
            }
        
        state = self.content_states[self.content_type]
        
        # If elements are empty, set up defaults for this content type
        if not state['elements']:
            self._setup_content_type_elements(self.content_type)
            state = self.content_states[self.content_type]  # Refresh state
        
        # Restore elements (deep copy to avoid reference issues)
        import copy
        self.elements = copy.deepcopy(state['elements'])
        
        # Restore frame and settings
        self.content_frame = QRect(state['content_frame'])
        self.constrain_to_frame = state['constrain_to_frame']
        # REMOVE zoom/pan
    
    def _setup_content_type_elements(self, content_type: str):
        """Set up default elements for a specific content type."""
        from .utils.dimensions import get_content_dimensions
        
        # Get dimensions for this content type
        dims = get_content_dimensions(content_type)
        
        # Set up default content frame (based on content type aspect ratio)
        if dims['aspect_ratio'] == 1.0:  # Square (post)
            frame_rect = QRect(50, 50, 400, 400)
        elif dims['aspect_ratio'] > 1.0:  # Landscape (tutorial, teaser)
            frame_rect = QRect(50, 50, 500, 300)
        else:  # Portrait (reel, story)
            frame_rect = QRect(50, 50, 300, 500)
        
        elements = {}
        
        # Add PiP element (standardized position)
        elements['pip'] = {
            'type': 'pip',
            'rect': QRect(50, 50, 100, 100),
            'enabled': True,
            'use_plugin_aspect_ratio': False,  # Toggle for using .adsp aspect ratio
            'plugin_aspect_ratio': 1.75,      # Default plugin aspect ratio (700x400)
            'plugin_file_path': '',           # Path to .adsp file
            'corner_radius': 0,               # Corner roundness (0-50)
            'shape': 'rectangle',             # 'square' or 'rectangle'
            'color': QColor(100, 150, 200, 128),
            'border_color': QColor(255, 255, 255),
            'border_width': 2
        }
        
        # Add text overlays (content-type specific)
        if content_type in ['reel', 'story']:
            # Portrait layout
            elements['title'] = {
                'type': 'text',
                'rect': QRect(50, 80, 200, 60),
                'content': f'{content_type.title()} Title',
                'size': 24,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
            elements['subtitle'] = {
                'type': 'text', 
                'rect': QRect(50, 450, 200, 40),
                'content': 'Subtitle',
                'size': 18,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
        elif content_type == 'post':
            # Square layout
            elements['title'] = {
                'type': 'text',
                'rect': QRect(50, 50, 300, 60),
                'content': 'Post Title',
                'size': 24,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
            elements['subtitle'] = {
                'type': 'text',
                'rect': QRect(50, 350, 300, 40),
                'content': 'Post Subtitle',
                'size': 18,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
        else:  # tutorial, teaser - landscape
            elements['title'] = {
                'type': 'text',
                'rect': QRect(50, 50, 400, 60),
                'content': f'{content_type.title()} Title',
                'size': 24,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
            elements['subtitle'] = {
                'type': 'text',
                'rect': QRect(50, 250, 400, 40),
                'content': f'{content_type.title()} Subtitle',
                'size': 18,
                'color': QColor(255, 255, 255),
                'style': 'normal',
                'enabled': True
            }
        
        # Save to content state
        self.content_states[content_type]['elements'] = elements
        self.content_states[content_type]['content_frame'] = frame_rect
    
    def set_constraint_mode(self, constrain: bool):
        """Enable/disable constraining elements to content frame."""
        self.constrain_to_frame = constrain
        if constrain:
            self._constrain_elements_to_frame()
        self.update()
    
    def get_element_config(self) -> dict:
        """Get current element configuration."""
        return {
            'content_type': self.content_type,
            'constrain_to_frame': self.constrain_to_frame,
            'elements': {k: dict(v) for k, v in self.elements.items()}
        }
    
    def set_element_config(self, config: dict):
        """Set element configuration."""
        if 'content_type' in config:
            self.content_type = config['content_type']
        if 'constrain_to_frame' in config:
            self.constrain_to_frame = config['constrain_to_frame']
        if 'elements' in config:
            self.elements.update(config['elements'])
        self._need_frame_check = True
        self.update()
    
    def paintEvent(self, event):
        """Paint the canvas."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width, height = self.width(), self.height()
        
        # Always center content frame and elements
        frame = self.content_frame
        dx = (width - frame.width()) // 2 - frame.x()
        dy = (height - frame.height()) // 2 - frame.y()
        for element in self.elements.values():
            rect = element['rect']
            element['rect'] = QRect(rect.x() + dx, rect.y() + dy, rect.width(), rect.height())
        self.content_frame.moveTo((width - frame.width()) // 2, (height - frame.height()) // 2)
        
        # Background
        painter.fillRect(0, 0, width, height, QColor(30, 30, 30))
        
        # Draw content frame
        self._draw_content_frame(painter, width, height)
        
        # Draw grid if enabled
        if self.snap_to_grid:
            self._draw_grid(painter)
        
        # Draw elements
        self._draw_elements(painter)
        
        # Draw UI overlays (not transformed)
        self._draw_ui_overlays(painter, width, height)
    
    def _draw_content_frame(self, painter, canvas_width, canvas_height):
        """Draw the content frame with proper aspect ratio."""
        dims = get_content_dimensions(self.content_type)
        aspect_ratio = dims["aspect_ratio"]
        
        # Calculate frame size
        padding = 60
        available_width = canvas_width - 2 * padding
        available_height = canvas_height - 2 * padding - 50
        
        if aspect_ratio > 1.0:  # Landscape
            frame_width = min(available_width * 0.9, available_height * aspect_ratio)
            frame_height = frame_width / aspect_ratio
        elif aspect_ratio == 1.0:  # Square
            frame_size = min(available_width * 0.7, available_height * 0.7)
            frame_width = frame_height = frame_size
        else:  # Portrait
            frame_height = min(available_height, available_width / aspect_ratio)
            frame_width = frame_height * aspect_ratio
        
        # Center the frame
        frame_x = (canvas_width - frame_width) / 2
        frame_y = (canvas_height - frame_height) / 2 + 25
        
        old_frame = self.content_frame
        self.content_frame = QRect(int(frame_x), int(frame_y), int(frame_width), int(frame_height))
        
        # Update elements if frame changed (size or position)
        if (self._need_frame_check or 
            (old_frame and (old_frame.size() != self.content_frame.size() or 
                           old_frame.topLeft() != self.content_frame.topLeft()))):
            self._update_elements_for_new_frame(old_frame)
            self._need_frame_check = False
        
        # Draw frame
        painter.setPen(QPen(QColor(150, 150, 150), 3))
        painter.setBrush(QBrush(QColor(45, 45, 45)))
        painter.drawRect(self.content_frame)
        
        # Draw corner guides
        self._draw_corner_guides(painter)
        
        # Draw frame info
        painter.setPen(QColor(200, 200, 200))
        font = QFont("Arial", 11, QFont.Weight.Bold)
        painter.setFont(font)
        ratio_text = f"{dims['name']} • {int(frame_width)}×{int(frame_height)}px"
        painter.drawText(self.content_frame.left(), self.content_frame.bottom() + 20, ratio_text)
    
    def _draw_corner_guides(self, painter):
        """Draw corner guides for the content frame."""
        corner_size = 15
        painter.setPen(QPen(QColor(200, 200, 0), 2))
        
        # Top-left
        painter.drawLine(
            self.content_frame.left(), self.content_frame.top() + corner_size,
            self.content_frame.left(), self.content_frame.top()
        )
        painter.drawLine(
            self.content_frame.left(), self.content_frame.top(),
            self.content_frame.left() + corner_size, self.content_frame.top()
        )
        
        # Top-right
        painter.drawLine(
            self.content_frame.right() - corner_size, self.content_frame.top(),
            self.content_frame.right(), self.content_frame.top()
        )
        painter.drawLine(
            self.content_frame.right(), self.content_frame.top(),
            self.content_frame.right(), self.content_frame.top() + corner_size
        )
        
        # Bottom-left
        painter.drawLine(
            self.content_frame.left(), self.content_frame.bottom() - corner_size,
            self.content_frame.left(), self.content_frame.bottom()
        )
        painter.drawLine(
            self.content_frame.left(), self.content_frame.bottom(),
            self.content_frame.left() + corner_size, self.content_frame.bottom()
        )
        
        # Bottom-right
        painter.drawLine(
            self.content_frame.right() - corner_size, self.content_frame.bottom(),
            self.content_frame.right(), self.content_frame.bottom()
        )
        painter.drawLine(
            self.content_frame.right(), self.content_frame.bottom(),
            self.content_frame.right(), self.content_frame.bottom() - corner_size
        )
    
    def _draw_grid(self, painter):
        """Draw snap grid."""
        if self.grid_size <= 0:
            return
        
        painter.setPen(QPen(QColor(60, 60, 60), 1))
        
        # Vertical lines
        x = self.content_frame.left()
        while x <= self.content_frame.right():
            painter.drawLine(x, self.content_frame.top(), x, self.content_frame.bottom())
            x += self.grid_size
        
        # Horizontal lines
        y = self.content_frame.top()
        while y <= self.content_frame.bottom():
            painter.drawLine(self.content_frame.left(), y, self.content_frame.right(), y)
            y += self.grid_size
    
    def _draw_elements(self, painter):
        """Draw all template elements."""
        for element_id, element in self.elements.items():
            # Draw all elements, but show disabled ones differently
            if element['type'] == 'pip':
                self._draw_pip_element(painter, element_id, element)
            elif element['type'] == 'text':
                self._draw_text_element(painter, element_id, element)
    
    def _draw_pip_element(self, painter, element_id, element):
        """Draw picture-in-picture element with optional rounded corners and plugin aspect ratio."""
        rect = element['rect']
        corner_radius = element.get('corner_radius', 0)
        enabled = element.get('enabled', True)
        
        # Apply opacity for disabled elements
        if not enabled:
            painter.setOpacity(0.3)
        
        # Use plugin highlight color if available, otherwise default colors
        default_color = QColor(100, 150, 200, 128)
        border_color = QColor(255, 255, 255)
        
        # Background with optional rounded corners
        painter.setBrush(QBrush(default_color))
        painter.setPen(QPen(border_color, element.get('border_width', 2)))
        
        if corner_radius > 0:
            # Draw rounded rectangle
            painter.drawRoundedRect(rect, corner_radius, corner_radius)
        else:
            # Draw regular rectangle
            painter.drawRect(rect)
        
        # PiP label and plugin info
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 10, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Show if using plugin aspect ratio
        if element.get('use_plugin_aspect_ratio', False):
            aspect_ratio = element.get('plugin_aspect_ratio', 1.75)
            plugin_text = f"Plugin\n{aspect_ratio:.2f}:1"
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, plugin_text)
        else:
            painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, "PiP")
        
        # Show disabled indicator
        if not enabled:
            painter.setPen(QColor(255, 100, 100))
            painter.drawText(rect.adjusted(5, 5, -5, -5), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight, "OFF")
        
        # Reset opacity
        painter.setOpacity(1.0)
        
        # Selection handles
        if element_id == self.selected_element:
            self._draw_selection_handles(painter, rect)
    
    def _draw_text_element(self, painter, element_id, element):
        """Draw text overlay element."""
        rect = element['rect']
        enabled = element.get('enabled', True)
        
        # Apply opacity for disabled elements
        if not enabled:
            painter.setOpacity(0.3)
        
        # Background
        painter.setBrush(QBrush(QColor(0, 0, 0, 100)))
        painter.setPen(QPen(QColor(255, 255, 255, 100), 1))
        painter.drawRect(rect)
        
        # Text
        color = element.get('color', QColor(255, 255, 255))
        size = element.get('size', 24)
        style = element.get('style', 'normal')
        content = element.get('content', 'Text')
        
        painter.setPen(color)
        font = QFont("Arial", size)
        if style == 'bold':
            font.setWeight(QFont.Weight.Bold)
        painter.setFont(font)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, content)
        
        # Show disabled indicator
        if not enabled:
            painter.setPen(QColor(255, 100, 100))
            painter.drawText(rect.adjusted(5, 5, -5, -5), Qt.AlignmentFlag.AlignBottom | Qt.AlignmentFlag.AlignRight, "OFF")
        
        # Reset opacity
        painter.setOpacity(1.0)
        
        # Selection handles
        if element_id == self.selected_element:
            self._draw_selection_handles(painter, rect)
    
    def _draw_selection_handles(self, painter, rect):
        """Draw selection handles around an element."""
        handle_size = 8
        painter.setBrush(QBrush(QColor(0, 120, 255)))
        painter.setPen(QPen(QColor(255, 255, 255), 1))
        
        handles = [
            QRect(rect.left() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            QRect(rect.right() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            QRect(rect.left() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size),
            QRect(rect.right() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size)
        ]
        
        for handle in handles:
            painter.drawRect(handle)
    
    def _draw_ui_overlays(self, painter, width, height):
        """Draw UI overlays that aren't affected by zoom/pan."""
        # Title
        painter.setPen(QColor(255, 255, 255))
        font = QFont("Arial", 16, QFont.Weight.Bold)
        painter.setFont(font)
        title = f"{self.content_type.title()} Template"
        painter.drawText(20, 35, title)
        
        # Constraint indicator
        if self.constrain_to_frame:
            painter.setPen(QColor(255, 200, 0))
            painter.drawText(20, height - 20, "⚠ Elements constrained to frame")
        else:
            painter.setPen(QColor(100, 255, 100))
            painter.drawText(20, height - 20, "✓ Free placement mode")
    
    def _update_elements_for_new_frame(self, old_frame):
        """Update element positions when content frame changes - MAINTAIN RELATIVE POSITIONS!"""
        if old_frame.isNull() or old_frame.width() == 0 or old_frame.height() == 0:
            return
        
        # Calculate scaling factors
        scale_x = self.content_frame.width() / old_frame.width()
        scale_y = self.content_frame.height() / old_frame.height()
        
        # Update all elements maintaining RELATIVE positions within the frame
        for element in self.elements.values():
            old_rect = element['rect']
            
            # Calculate RELATIVE position within old frame (as percentages)
            rel_x_percent = (old_rect.x() - old_frame.x()) / old_frame.width()
            rel_y_percent = (old_rect.y() - old_frame.y()) / old_frame.height()
            rel_width_percent = old_rect.width() / old_frame.width()
            rel_height_percent = old_rect.height() / old_frame.height()
            
            # Apply relative position to new frame
            new_x = self.content_frame.x() + (rel_x_percent * self.content_frame.width())
            new_y = self.content_frame.y() + (rel_y_percent * self.content_frame.height())
            new_width = rel_width_percent * self.content_frame.width()
            new_height = rel_height_percent * self.content_frame.height()
            
            # Update element rect
            element['rect'] = QRect(int(new_x), int(new_y), int(new_width), int(new_height))
        
        # Save the updated positions to content state
        self._save_current_state()
    
    def _position_elements_relative_to_frame(self):
        """Position elements relative to content frame."""
        frame = self.content_frame
        
        # Position PiP
        if 'pip' in self.elements:
            pip_size = min(100, frame.width() // 4, frame.height() // 4)
            self.elements['pip']['rect'] = QRect(
                frame.x() + 20, frame.y() + 20, pip_size, pip_size
            )
        
        # Position text elements
        positions = {
            'title': (20, 60, min(250, frame.width() - 40), 50),
            'subtitle': (20, frame.height() - 90, min(200, frame.width() - 40), 40)
        }
        
        for element_id, element in self.elements.items():
            if element['type'] == 'text' and element_id in positions:
                x, y, w, h = positions[element_id]
                element['rect'] = QRect(frame.x() + x, frame.y() + y, w, h)
    
    def _constrain_elements_to_frame(self):
        """Constrain elements to content frame if enabled."""
        if not self.constrain_to_frame:
            return
        
        for element in self.elements.values():
            if not element.get('enabled', True):
                continue
            
            rect = element['rect']
            
            # Keep element within frame bounds
            if rect.right() > self.content_frame.right():
                rect.moveRight(self.content_frame.right())
            if rect.bottom() > self.content_frame.bottom():
                rect.moveBottom(self.content_frame.bottom())
            if rect.left() < self.content_frame.left():
                rect.moveLeft(self.content_frame.left())
            if rect.top() < self.content_frame.top():
                rect.moveTop(self.content_frame.top())
    
    def resizeEvent(self, event):
        """Handle widget resize to update element positions."""
        super().resizeEvent(event)
        # When the widget is resized, we need to check if the content frame changes
        # and update element positions accordingly
        self._need_frame_check = True
        self.update()
    
    # Mouse event handling
    def wheelEvent(self, event: QWheelEvent):
        """Handle mouse wheel for zooming."""
        # Remove mouse wheel zoom logic
        super().wheelEvent(event)
    
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press events."""
        if event.button() == Qt.MouseButton.LeftButton:
            # Get mouse position
            canvas_point = QPoint(int(event.position().x()), int(event.position().y()))
            
            # Check for element selection/interaction
            selected = self._find_element_at_point(canvas_point)
            
            if selected:
                element_id, interaction_type = selected
                self.selected_element = element_id
                
                if interaction_type == "resize":
                    self.resizing_element = element_id
                    self.resize_handle = self._get_resize_handle(canvas_point, self.elements[element_id]['rect'])
                elif interaction_type == "move":
                    self.dragging_element = element_id
                    self.last_mouse_pos = canvas_point
                
                self.element_selected.emit(element_id)
            else:
                self.selected_element = None
                self.canvas_clicked.emit(QPointF(event.position().x(), event.position().y()))
            
            self.update()
    
    def mouseMoveEvent(self, event: QMouseEvent):
        """Handle mouse move events."""
        if self.dragging_element:
            # Move element
            canvas_point = QPoint(int(event.position().x()), int(event.position().y()))
            
            if self.last_mouse_pos:
                delta = canvas_point - self.last_mouse_pos
                element = self.elements[self.dragging_element]
                old_rect = element['rect']
                new_rect = QRect(old_rect.x() + delta.x(), old_rect.y() + delta.y(),
                               old_rect.width(), old_rect.height())
                
                # Apply constraints if enabled
                if self.constrain_to_frame:
                    if new_rect.left() < self.content_frame.left():
                        new_rect.moveLeft(self.content_frame.left())
                    if new_rect.top() < self.content_frame.top():
                        new_rect.moveTop(self.content_frame.top())
                    if new_rect.right() > self.content_frame.right():
                        new_rect.moveRight(self.content_frame.right())
                    if new_rect.bottom() > self.content_frame.bottom():
                        new_rect.moveBottom(self.content_frame.bottom())
                
                element['rect'] = new_rect
                self.element_moved.emit(self.dragging_element, new_rect)
            
            self.last_mouse_pos = canvas_point
            self.update()
        
        elif self.resizing_element:
            # Resize element
            canvas_point = QPoint(int(event.position().x()), int(event.position().y()))
            
            element = self.elements[self.resizing_element]
            old_rect = element['rect']
            new_rect = self._calculate_resize(old_rect, canvas_point, self.resize_handle)
            
            # Apply constraints if enabled
            if self.constrain_to_frame:
                if new_rect.left() < self.content_frame.left():
                    new_rect.moveLeft(self.content_frame.left())
                if new_rect.top() < self.content_frame.top():
                    new_rect.moveTop(self.content_frame.top())
                if new_rect.right() > self.content_frame.right():
                    new_rect.moveRight(self.content_frame.right())
                if new_rect.bottom() > self.content_frame.bottom():
                    new_rect.moveBottom(self.content_frame.bottom())
            
            # Ensure minimum size
            if new_rect.width() < 20:
                new_rect.setWidth(20)
            if new_rect.height() < 20:
                new_rect.setHeight(20)
            
            element['rect'] = new_rect
            self.element_resized.emit(self.resizing_element, new_rect)
            self.update()
    
    def mouseReleaseEvent(self, event: QMouseEvent):
        """Handle mouse release events."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.dragging_element = None
            self.resizing_element = None
            self.resize_handle = ""
            self.last_mouse_pos = None
    
    def _find_element_at_point(self, point: QPoint) -> tuple[str, str] | None:
        """Find element at point and determine interaction type."""
        # Check resize handles first (if an element is selected)
        if self.selected_element and self.selected_element in self.elements:
            element = self.elements[self.selected_element]
            if self._point_in_resize_handle(point, element['rect']):
                return self.selected_element, "resize"
        
        # Check for elements (in reverse order for top-to-bottom selection)
        # NOTE: Allow selection of disabled elements so users can re-enable them!
        for element_id, element in reversed(list(self.elements.items())):
            if element['rect'].contains(point):
                return element_id, "move"
        
        return None
    
    def _point_in_resize_handle(self, point: QPoint, rect: QRect) -> bool:
        """Check if point is in any resize handle."""
        handle_size = 8
        handles = [
            QRect(rect.left() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            QRect(rect.right() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            QRect(rect.left() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size),
            QRect(rect.right() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size)
        ]
        return any(handle.contains(point) for handle in handles)
    
    def _get_resize_handle(self, point: QPoint, rect: QRect) -> str:
        """Get which resize handle is being dragged."""
        handle_size = 8
        handles = {
            "top-left": QRect(rect.left() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            "top-right": QRect(rect.right() - handle_size//2, rect.top() - handle_size//2, handle_size, handle_size),
            "bottom-left": QRect(rect.left() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size),
            "bottom-right": QRect(rect.right() - handle_size//2, rect.bottom() - handle_size//2, handle_size, handle_size)
        }
        
        for handle_name, handle_rect in handles.items():
            if handle_rect.contains(point):
                return handle_name
        return "bottom-right"  # Default
    
    def _calculate_resize(self, old_rect: QRect, mouse_pos: QPoint, handle: str) -> QRect:
        """Calculate new rectangle size based on handle being dragged."""
        new_rect = QRect(old_rect)
        
        if handle == "top-left":
            new_rect.setTopLeft(mouse_pos)
        elif handle == "top-right":
            new_rect.setTopRight(mouse_pos)
        elif handle == "bottom-left":
            new_rect.setBottomLeft(mouse_pos)
        elif handle == "bottom-right":
            new_rect.setBottomRight(mouse_pos)
        
        # Check if this is a PiP element with plugin aspect ratio enabled
        if self.resizing_element and self.resizing_element in self.elements:
            element = self.elements[self.resizing_element]
            if (element.get('type') == 'pip' and 
                element.get('use_plugin_aspect_ratio', False)):
                
                # Maintain plugin aspect ratio during resize
                aspect_ratio = element.get('plugin_aspect_ratio', 1.75)
                new_rect = self._maintain_aspect_ratio(new_rect, aspect_ratio, handle)
        
        return new_rect
    
    def _maintain_aspect_ratio(self, rect: QRect, aspect_ratio: float, handle: str) -> QRect:
        """Maintain aspect ratio during resize."""
        # Calculate new dimensions based on the handle being dragged
        if handle in ["bottom-right", "top-left"]:
            # Use width to determine height
            new_height = int(rect.width() / aspect_ratio)
            if handle == "bottom-right":
                rect.setHeight(new_height)
            else:  # top-left
                rect.setTop(rect.bottom() - new_height)
        elif handle in ["top-right", "bottom-left"]:
            # Use width to determine height
            new_height = int(rect.width() / aspect_ratio)
            if handle == "top-right":
                rect.setTop(rect.bottom() - new_height)
            else:  # bottom-left
                rect.setHeight(new_height)
        
        return rect
    
    # Public API methods
    def load_plugin_aspect_ratio(self, element_id: str, adsp_file_path: str):
        """Load aspect ratio from .adsp plugin file and apply to PiP element."""
        if element_id not in self.elements:
            return False
        
        element = self.elements[element_id]
        if element.get('type') != 'pip':
            return False
        
        # Import the adsp utils
        from .utils.adsp_utils import get_plugin_info
        
        plugin_info = get_plugin_info(adsp_file_path)
        if not plugin_info:
            return False
        
        # Update element properties
        element['plugin_file_path'] = adsp_file_path
        element['plugin_aspect_ratio'] = plugin_info['aspect_ratio']
        element['use_plugin_aspect_ratio'] = True
        
        # Apply the aspect ratio to current rect if enabled
        if element.get('use_plugin_aspect_ratio', False):
            self._apply_plugin_aspect_ratio(element_id)
        
        self.update()
        return True
    
    def _apply_plugin_aspect_ratio(self, element_id: str):
        """Apply plugin aspect ratio to element's current rectangle."""
        if element_id not in self.elements:
            return
        
        element = self.elements[element_id]
        aspect_ratio = element.get('plugin_aspect_ratio', 1.75)
        current_rect = element['rect']
        
        # Maintain center point and adjust size to match aspect ratio
        center_x = current_rect.center().x()
        center_y = current_rect.center().y()
        
        # Use current width and calculate new height
        width = current_rect.width()
        height = int(width / aspect_ratio)
        
        # Create new rect centered on the same point
        new_rect = QRect(
            center_x - width // 2,
            center_y - height // 2,
            width,
            height
        )
        
        element['rect'] = new_rect
    
    def set_pip_corner_radius(self, element_id: str, radius: int):
        """Set corner radius for PiP element."""
        if element_id in self.elements and self.elements[element_id].get('type') == 'pip':
            self.elements[element_id]['corner_radius'] = max(0, min(50, radius))
            self.update()
    
    def toggle_plugin_aspect_ratio(self, element_id: str, enabled: bool):
        """Toggle plugin aspect ratio for PiP element."""
        if element_id in self.elements and self.elements[element_id].get('type') == 'pip':
            self.elements[element_id]['use_plugin_aspect_ratio'] = enabled
            if enabled:
                self._apply_plugin_aspect_ratio(element_id)
            self.update()
    
    def get_pip_properties(self, element_id: str) -> dict:
        """Get PiP element properties for UI controls."""
        if element_id not in self.elements:
            return {}
        
        element = self.elements[element_id]
        if element.get('type') != 'pip':
            return {}
        
        return {
            'use_plugin_aspect_ratio': element.get('use_plugin_aspect_ratio', False),
            'plugin_aspect_ratio': element.get('plugin_aspect_ratio', 1.75),
            'plugin_file_path': element.get('plugin_file_path', ''),
            'corner_radius': element.get('corner_radius', 0),
            'shape': element.get('shape', 'rectangle'),
            'color': element.get('color', QColor(100, 150, 200, 128)),
            'border_color': element.get('border_color', QColor(255, 255, 255)),
            'border_width': element.get('border_width', 2)
        }
    
    def reset_positions(self):
        """Reset all elements to their default positions for the current content type."""
        # Clear current elements
        self.elements = {}
        
        # Re-setup default elements for current content type
        self._setup_content_type_elements(self.content_type)
        
        # Load the fresh defaults
        if self.content_type in self.content_states:
            import copy
            self.elements = copy.deepcopy(self.content_states[self.content_type]['elements'])
        
        # Clear selection
        self.selected_element = None
        
        # Update display
        self.update()
        print(f"Reset element positions for {self.content_type}")
