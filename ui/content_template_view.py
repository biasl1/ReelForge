"""
Content Template View for ReelTune Main Window
Visual WYSIWYG template editor like mini After Effects
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame, 
    QComboBox, QPushButton, QGridLayout, QGroupBox,
    QRadioButton, QButtonGroup, QScrollArea, QSplitter,
    QListWidget, QListWidgetItem, QSlider, QSpinBox,
    QCheckBox, QColorDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QPointF, QRectF
from PyQt6.QtGui import QFont, QPainter, QColor, QPen, QBrush, QPixmap

from typing import Dict, Any, Optional


# Standard social media dimensions
CONTENT_DIMENSIONS = {
    "reel": {"width": 1080, "height": 1920, "name": "Instagram Reel (9:16)", "has_timeline": True},
    "story": {"width": 1080, "height": 1920, "name": "Instagram Story (9:16)", "has_timeline": True}, 
    "post": {"width": 1080, "height": 1080, "name": "Instagram Post (1:1)", "has_timeline": False},
    "tutorial": {"width": 1920, "height": 1080, "name": "YouTube (16:9)", "has_timeline": True}
}

class LayerItem:
    """Represents a visual layer in the composition"""
    def __init__(self, name: str, layer_type: str, rect: QRectF = None, asset_id: str = None):
        self.name = name
        self.layer_type = layer_type  # background, main_media, subtitle, intro, outro
        self.rect = rect or QRectF(0, 0, 100, 100)
        self.asset_id = asset_id
        self.visible = True
        self.locked = False
        self.color = QColor(255, 255, 255, 128)
        
class VisualCanvas(QWidget):
    """Visual canvas for template editing - like mini After Effects"""
    
    layer_selected = pyqtSignal(str)  # layer_type
    layer_moved = pyqtSignal(str, QRectF)  # layer_type, new_rect
    
    def __init__(self):
        super().__init__()
        self.content_type = "reel"
        self.layers = {}
        self.selected_layer = None
        self.dragging = False
        self.drag_start = QPointF()
        self.canvas_scale = 0.3  # Scale factor for display
        
        self.setMinimumSize(400, 600)
        self.setStyleSheet("background-color: #2b2b2b; border: 1px solid #555;")
        self._setup_default_layers()
        
    def _setup_default_layers(self):
        """Setup default layers for current content type"""
        dims = CONTENT_DIMENSIONS[self.content_type]
        canvas_width = dims["width"] * self.canvas_scale
        canvas_height = dims["height"] * self.canvas_scale
        
        # Background layer (full size)
        self.layers["background"] = LayerItem(
            "Background", "background", 
            QRectF(0, 0, canvas_width, canvas_height),
            None
        )
        self.layers["background"].color = QColor(50, 50, 50, 255)
        
        # Main media layer (80% of canvas, centered)
        main_width = canvas_width * 0.8
        main_height = canvas_height * 0.6
        main_x = (canvas_width - main_width) / 2
        main_y = (canvas_height - main_height) / 2
        
        self.layers["main_media"] = LayerItem(
            "Main Media", "main_media",
            QRectF(main_x, main_y, main_width, main_height),
            None
        )
        self.layers["main_media"].color = QColor(100, 150, 200, 180)
        
        # Subtitle layer (bottom 20%)
        subtitle_height = canvas_height * 0.15
        subtitle_y = canvas_height - subtitle_height - 20
        
        self.layers["subtitle"] = LayerItem(
            "Subtitles", "subtitle",
            QRectF(20, subtitle_y, canvas_width - 40, subtitle_height),
            None
        )
        self.layers["subtitle"].color = QColor(255, 255, 100, 150)
        
        # Timeline layers (only for video content)
        if dims["has_timeline"]:
            # Intro layer (first 2 seconds)
            intro_height = canvas_height * 0.2
            self.layers["intro"] = LayerItem(
                "Intro", "intro",
                QRectF(10, 10, canvas_width - 20, intro_height),
                None
            )
            self.layers["intro"].color = QColor(100, 255, 100, 120)
            
            # Outro layer (last 3 seconds) 
            outro_height = canvas_height * 0.2
            outro_y = canvas_height - outro_height - subtitle_height - 30
            self.layers["outro"] = LayerItem(
                "Outro", "outro", 
                QRectF(10, outro_y, canvas_width - 20, outro_height),
                None
            )
            self.layers["outro"].color = QColor(255, 100, 100, 120)
    
    def set_content_type(self, content_type: str):
        """Change content type and rebuild layers"""
        self.content_type = content_type
        self.layers.clear()
        self._setup_default_layers()
        self.update()
        
    def paintEvent(self, event):
        """Paint the visual canvas"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw canvas background
        dims = CONTENT_DIMENSIONS[self.content_type]
        canvas_width = dims["width"] * self.canvas_scale
        canvas_height = dims["height"] * self.canvas_scale
        
        # Center the canvas in the widget
        widget_rect = self.rect()
        canvas_x = (widget_rect.width() - canvas_width) / 2
        canvas_y = (widget_rect.height() - canvas_height) / 2
        
        canvas_rect = QRectF(canvas_x, canvas_y, canvas_width, canvas_height)
        
        # Draw canvas border
        painter.setPen(QPen(QColor(100, 100, 100), 2))
        painter.setBrush(QBrush(QColor(30, 30, 30)))
        painter.drawRect(canvas_rect)
        
        # Draw dimension label
        painter.setPen(QColor(200, 200, 200))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(canvas_rect.topLeft() + QPointF(5, -5), dims["name"])
        
        # Draw layers
        for layer_type, layer in self.layers.items():
            if not layer.visible:
                continue
                
            # Offset layer rect by canvas position
            layer_rect = QRectF(
                layer.rect.x() + canvas_x,
                layer.rect.y() + canvas_y, 
                layer.rect.width(),
                layer.rect.height()
            )
            
            # Draw layer
            painter.setBrush(QBrush(layer.color))
            
            # Highlight selected layer
            if layer_type == self.selected_layer:
                painter.setPen(QPen(QColor(255, 255, 0), 3))
            else:
                painter.setPen(QPen(QColor(150, 150, 150), 1))
                
            painter.drawRect(layer_rect)
            
            # Draw layer label
            painter.setPen(QColor(255, 255, 255))
            painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
            text_rect = QRectF(layer_rect.x() + 5, layer_rect.y() + 5, 
                             layer_rect.width() - 10, 20)
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft, layer.name)
            
            # Draw asset info if assigned
            if layer.asset_id:
                painter.setPen(QColor(200, 255, 200))
                painter.setFont(QFont("Arial", 8))
                asset_text = f"Asset: {layer.asset_id[:8]}..."
                asset_rect = QRectF(layer_rect.x() + 5, layer_rect.y() + 25,
                                  layer_rect.width() - 10, 15)
                painter.drawText(asset_rect, Qt.AlignmentFlag.AlignLeft, asset_text)
    
    def mousePressEvent(self, event):
        """Handle mouse press for layer selection and dragging"""
        if event.button() == Qt.MouseButton.LeftButton:
            # Find clicked layer
            clicked_layer = self._get_layer_at_position(event.position())
            if clicked_layer:
                self.selected_layer = clicked_layer
                self.dragging = True
                self.drag_start = event.position()
                self.layer_selected.emit(clicked_layer)
                self.update()
                
    def mouseMoveEvent(self, event):
        """Handle mouse move for dragging layers"""
        if self.dragging and self.selected_layer:
            delta = event.position() - self.drag_start
            layer = self.layers[self.selected_layer]
            
            # Update layer position
            new_rect = QRectF(
                layer.rect.x() + delta.x(),
                layer.rect.y() + delta.y(),
                layer.rect.width(),
                layer.rect.height()
            )
            
            layer.rect = new_rect
            self.drag_start = event.position()
            self.layer_moved.emit(self.selected_layer, new_rect)
            self.update()
            
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        self.dragging = False
        
    def _get_layer_at_position(self, pos: QPointF) -> Optional[str]:
        """Find which layer is at the given position"""
        dims = CONTENT_DIMENSIONS[self.content_type]
        canvas_width = dims["width"] * self.canvas_scale
        canvas_height = dims["height"] * self.canvas_scale
        
        # Calculate canvas offset
        widget_rect = self.rect()
        canvas_x = (widget_rect.width() - canvas_width) / 2
        canvas_y = (widget_rect.height() - canvas_height) / 2
        
        # Check layers in reverse order (top to bottom)
        for layer_type in reversed(list(self.layers.keys())):
            layer = self.layers[layer_type]
            if not layer.visible:
                continue
                
            layer_rect = QRectF(
                layer.rect.x() + canvas_x,
                layer.rect.y() + canvas_y,
                layer.rect.width(), 
                layer.rect.height()
            )
            
            if layer_rect.contains(pos):
                return layer_type
                
        return None
    """Main content template view with timeline-like layout"""
    
    template_changed = pyqtSignal(str, str, str)  # content_type, parameter, mode
    
    def __init__(self):
        super().__init__()
        self.current_content_type = "reel"
        self.current_project = None
        self.parameter_widgets = {}  # Store references to parameter UI elements
        self.templates = {
            "reel": {"title": "Reel", "duration": "15-30s", "color": "#E91E63"},
            "story": {"title": "Story", "duration": "5-15s", "color": "#9C27B0"}, 
            "post": {"title": "Post", "duration": "30-60s", "color": "#2196F3"},
            "tutorial": {"title": "Tutorial", "duration": "60-120s", "color": "#FF9800"}
        }
        self.setup_ui()
        
    def setup_ui(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Header
        header = QLabel("Content Templates")
        header.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Content type selector
        type_selector = self.create_type_selector()
        layout.addWidget(type_selector)
        
        # Main template editor
        self.template_editor = self.create_template_editor()
        layout.addWidget(self.template_editor)
        
        self.setLayout(layout)
        self.update_template_view()
        
    def create_type_selector(self) -> QWidget:
        """Create content type selector buttons"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setMaximumHeight(80)
        
        layout = QHBoxLayout()
        
        # Title
        title = QLabel("Content Type:")
        title.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout.addWidget(title)
        
        layout.addStretch()
        
        # Type buttons
        self.type_buttons = QButtonGroup()
        for i, (type_key, type_data) in enumerate(self.templates.items()):
            btn = QPushButton(f"{type_data['title']}\n{type_data['duration']}")
            btn.setCheckable(True)
            btn.setMinimumSize(100, 50)
            btn.setStyleSheet(f"""
                QPushButton {{
                    border: 2px solid {type_data['color']};
                    border-radius: 8px;
                    background-color: white;
                    font-weight: bold;
                }}
                QPushButton:checked {{
                    background-color: {type_data['color']};
                    color: white;
                }}
                QPushButton:hover {{
                    background-color: {type_data['color']}40;
                }}
            """)
            btn.clicked.connect(lambda checked, key=type_key: self.select_content_type(key))
            self.type_buttons.addButton(btn, i)
            layout.addWidget(btn)
            
            if type_key == self.current_content_type:
                btn.setChecked(True)
        
        layout.addStretch()
        frame.setLayout(layout)
        return frame
        
    def create_template_editor(self) -> QWidget:
        """Create the main template editor area"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Template sections
        self.subtitle_section = self.create_parameter_section("Subtitle Settings", [
            {"name": "Font Size", "key": "font_size", "default": "24px"},
            {"name": "Font Family", "key": "font_family", "default": "Arial"},
            {"name": "Text Color", "key": "text_color", "default": "White"},
            {"name": "Position", "key": "position", "default": "Bottom"}
        ])
        layout.addWidget(self.subtitle_section)
        
        self.timing_section = self.create_parameter_section("Timing Settings", [
            {"name": "Duration", "key": "duration", "default": "30s"},
            {"name": "Intro Length", "key": "intro", "default": "2s"},
            {"name": "Outro Length", "key": "outro", "default": "3s"},
            {"name": "Sections Count", "key": "sections", "default": "4"}
        ])
        layout.addWidget(self.timing_section)
        
        self.style_section = self.create_parameter_section("Style Settings", [
            {"name": "Background", "key": "background", "default": "Transparent"},
            {"name": "Animation", "key": "animation", "default": "Fade In"},
            {"name": "Overlay", "key": "overlay", "default": "None"},
            {"name": "Branding", "key": "branding", "default": "Logo"}
        ])
        layout.addWidget(self.style_section)
        
        layout.addStretch()
        widget.setLayout(layout)
        scroll.setWidget(widget)
        return scroll
        
    def create_parameter_section(self, title: str, parameters: list) -> QGroupBox:
        """Create a parameter section with Universal/Fixed options"""
        group = QGroupBox(title)
        group.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        layout = QGridLayout()
        layout.setSpacing(15)
        
        # Header row
        layout.addWidget(QLabel("Parameter"), 0, 0)
        layout.addWidget(QLabel("Value"), 0, 1)
        layout.addWidget(QLabel("Universal"), 0, 2)
        layout.addWidget(QLabel("Fixed"), 0, 3)
        
        # Parameters
        for i, param in enumerate(parameters, 1):
            # Parameter name
            name_label = QLabel(param["name"])
            layout.addWidget(name_label, i, 0)
            
            # Current value
            value_label = QLabel(param["default"])
            value_label.setStyleSheet("border: 1px solid #ccc; padding: 4px; background: white;")
            layout.addWidget(value_label, i, 1)
            
            # Universal/Fixed radio buttons
            universal_radio = QRadioButton()
            fixed_radio = QRadioButton()
            fixed_radio.setChecked(True)  # Default to Fixed
            
            # Store widget references for later updates
            self.parameter_widgets[param["key"]] = (universal_radio, fixed_radio)
            
            # Group the radio buttons
            button_group = QButtonGroup()
            button_group.addButton(universal_radio, 0)
            button_group.addButton(fixed_radio, 1)
            
            # Connect signals
            universal_radio.toggled.connect(
                lambda checked, key=param["key"]: self.on_mode_changed(key, "universal" if checked else "fixed")
            )
            
            layout.addWidget(universal_radio, i, 2)
            layout.addWidget(fixed_radio, i, 3)
        
        group.setLayout(layout)
        return group
        
    def select_content_type(self, content_type: str):
        """Switch to different content type"""
        self.current_content_type = content_type
        self.update_template_view()
        
        # Load template data for this content type
        if self.current_project and hasattr(self.current_project, 'content_generation_manager'):
            self.load_templates_from_project()
        
        # Load template data for new content type
        if self.current_project:
            self.load_templates_from_project()
        
    def update_template_view(self):
        """Update the view for current content type"""
        # Update styling based on current type
        type_data = self.templates[self.current_content_type]
        color = type_data["color"]
        
        # Update section headers with type-specific colors
        for section in [self.subtitle_section, self.timing_section, self.style_section]:
            section.setStyleSheet(f"""
                QGroupBox {{
                    font-weight: bold;
                    border: 2px solid {color};
                    border-radius: 8px;
                    margin: 10px 0;
                    padding-top: 10px;
                }}
                QGroupBox::title {{
                    subcontrol-origin: margin;
                    left: 10px;
                    padding: 0 5px 0 5px;
                    color: {color};
                }}
            """)
    
    def on_mode_changed(self, parameter_key: str, mode: str):
        """Handle parameter mode change"""
        self.template_changed.emit(self.current_content_type, parameter_key, mode)
        print(f"Template changed: {self.current_content_type}.{parameter_key} -> {mode}")

    def set_project(self, project):
        """Set the current project and update UI with project template data"""
        self.current_project = project
        if project and hasattr(project, 'content_generation_manager'):
            self.load_templates_from_project()
        
    def load_templates_from_project(self):
        """Load template settings from the current project"""
        if not self.current_project or not hasattr(self.current_project, 'content_generation_manager'):
            return
            
        manager = self.current_project.content_generation_manager
        template = manager.get_content_template(self.current_content_type)
        
        # Update UI based on template settings
        self._update_parameter_modes(template)
        
    def _update_parameter_modes(self, template):
        """Update UI radio buttons based on template parameter modes"""
        # Update subtitle parameters
        subtitle_mapping = {
            'font_size': 'font_size',
            'font_family': 'font_family', 
            'text_color': 'color',
            'position': 'position'
        }
        
        for ui_key, template_key in subtitle_mapping.items():
            if hasattr(template.subtitle, template_key):
                param = getattr(template.subtitle, template_key)
                self._set_parameter_mode(ui_key, param.mode.value)
        
        # Update timing parameters  
        timing_mapping = {
            'duration': 'duration',
            'intro': 'intro_duration',
            'outro': 'outro_duration',
            'sections': 'segment_count'
        }
        
        for ui_key, template_key in timing_mapping.items():
            if hasattr(template.timing, template_key):
                param = getattr(template.timing, template_key)
                self._set_parameter_mode(ui_key, param.mode.value)
                
        # Update overlay parameters
        overlay_mapping = {
            'background': 'background_style',
            'animation': 'animation_style',
            'overlay': 'overlay_elements',
            'branding': 'branding_elements'
        }
        
        for ui_key, template_key in overlay_mapping.items():
            if hasattr(template.overlay, template_key):
                param = getattr(template.overlay, template_key)
                self._set_parameter_mode(ui_key, param.mode.value)
    
    def _set_parameter_mode(self, parameter_key: str, mode: str):
        """Set the radio button state for a parameter"""
        if parameter_key in self.parameter_widgets:
            universal_radio, fixed_radio = self.parameter_widgets[parameter_key]
            if mode == "free":
                universal_radio.setChecked(True)
            else:
                fixed_radio.setChecked(True)
