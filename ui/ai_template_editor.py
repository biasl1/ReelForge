"""
Beautiful AI-Focused Template Editor for ReelTune
Professional, intuitive interface focusing only on essential AI-driven template settings.
Smart design: user actions automatically override AI, no redundant toggles.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QGroupBox, QFormLayout, QPushButton,
    QSplitter, QCheckBox, QSlider, QSpinBox, QScrollArea,
    QListWidget, QListWidgetItem, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QSizeF, QMimeData, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QDrag, QLinearGradient


class SimpleTemplateCanvas(QWidget):
    """Beautiful preview canvas showing template layout zones with professional styling"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.content_type = "reel"
        self.canvas_size = QSizeF(405, 720)  # 9:16 default
        self.template_config = {
            'background_enabled': True,
            'media_window_enabled': True,
            'subtitle_enabled': True
        }
        
        self.setMinimumSize(int(self.canvas_size.width()), int(self.canvas_size.height()))
        
        # Professional styling with gradient background
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #1a1a1a);
                border: 2px solid #0078d4;
                border-radius: 8px;
            }
        """)
        
        # Add subtle drop shadow
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 60))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)
        
    def set_content_type(self, content_type: str):
        """Set canvas dimensions based on content type"""
        if content_type.lower() in ["reel", "story", "tutorial"]:
            self.canvas_size = QSizeF(405, 720)  # 9:16
        elif content_type.lower() == "post":
            self.canvas_size = QSizeF(600, 600)  # 1:1
            
        self.setFixedSize(int(self.canvas_size.width()), int(self.canvas_size.height()))
        self.content_type = content_type.lower()
        self.update()
        
    def update_template_config(self, config):
        """Update template configuration"""
        self.template_config.update(config)
        self.update()
        
    def paintEvent(self, event):
        """Paint the template zones preview with modern styling"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Modern gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(45, 45, 45))
        gradient.setColorAt(1, QColor(26, 26, 26))
        painter.fillRect(self.rect(), gradient)
        
        width = self.canvas_size.width()
        height = self.canvas_size.height()
        
        # Draw template zones based on content type
        if self.content_type in ["reel", "story", "tutorial"]:
            self._draw_video_template_zones(painter, width, height)
        else:  # post
            self._draw_post_template_zones(painter, width, height)
            
    def _draw_video_template_zones(self, painter, width, height):
        """Draw zones for video content with modern UI design"""
        font = QFont("SF Pro Display", 11, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Background zone (always full canvas)
        if self.template_config.get('background_enabled', True):
            painter.setPen(QPen(QColor(120, 120, 120), 2, Qt.PenStyle.DashLine))
            painter.drawRoundedRect(8, 8, int(width-16), int(height-16), 6, 6)
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(20, 35, "🎨 Background Zone")
            painter.setPen(QPen(QColor(160, 160, 160)))
            painter.drawText(20, 55, "AI will choose/generate")
        
        # Media window zone (main content area) with modern accent
        if self.template_config.get('media_window_enabled', True):
            media_rect = QRectF(25, 80, width-50, height*0.6)
            
            # Gradient fill for media zone
            media_gradient = QLinearGradient(media_rect.topLeft(), media_rect.bottomLeft())
            media_gradient.setColorAt(0, QColor(0, 120, 255, 40))
            media_gradient.setColorAt(1, QColor(0, 150, 255, 20))
            painter.fillRect(media_rect, media_gradient)
            
            painter.setPen(QPen(QColor(0, 150, 255), 3))
            painter.drawRoundedRect(media_rect, 8, 8)
            painter.setPen(QPen(QColor(120, 200, 255)))
            painter.drawText(35, 110, "📹 Main Media Window")
            painter.setPen(QPen(QColor(180, 220, 255)))
            painter.drawText(35, 130, "Primary content area")
        
        # Subtitle zone (bottom area) with warm accent
        if self.template_config.get('subtitle_enabled', True):
            subtitle_rect = QRectF(25, height*0.75, width-50, height*0.2)
            
            # Gradient fill for subtitle zone
            subtitle_gradient = QLinearGradient(subtitle_rect.topLeft(), subtitle_rect.bottomLeft())
            subtitle_gradient.setColorAt(0, QColor(255, 200, 0, 40))
            subtitle_gradient.setColorAt(1, QColor(255, 180, 0, 20))
            painter.fillRect(subtitle_rect, subtitle_gradient)
            
            painter.setPen(QPen(QColor(255, 200, 0), 2))
            painter.drawRoundedRect(subtitle_rect, 6, 6)
            painter.setPen(QPen(QColor(255, 220, 100)))
            painter.drawText(35, int(height*0.75 + 25), "📝 Subtitle Zone")
            painter.setPen(QPen(QColor(255, 230, 150)))
            painter.drawText(35, int(height*0.75 + 45), "AI-generated text")
            
    def _draw_post_template_zones(self, painter, width, height):
        """Draw zones for post content with modern styling"""
        font = QFont("SF Pro Display", 11, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Background zone
        if self.template_config.get('background_enabled', True):
            painter.setPen(QPen(QColor(120, 120, 120), 2, Qt.PenStyle.DashLine))
            painter.drawRoundedRect(8, 8, int(width-16), int(height-16), 6, 6)
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(20, 35, "🎨 Background Zone")
        
        # Media window (center area)
        if self.template_config.get('media_window_enabled', True):
            media_rect = QRectF(40, 100, width-80, height*0.6)
            
            media_gradient = QLinearGradient(media_rect.topLeft(), media_rect.bottomLeft())
            media_gradient.setColorAt(0, QColor(0, 120, 255, 40))
            media_gradient.setColorAt(1, QColor(0, 150, 255, 20))
            painter.fillRect(media_rect, media_gradient)
            
            painter.setPen(QPen(QColor(0, 150, 255), 3))
            painter.drawRoundedRect(media_rect, 8, 8)
            painter.setPen(QPen(QColor(120, 200, 255)))
            painter.drawText(50, 130, "📸 Main Media Window")
        
        # Text overlay zone (bottom)
        if self.template_config.get('subtitle_enabled', True):
            text_rect = QRectF(40, height*0.75, width-80, height*0.2)
            
            text_gradient = QLinearGradient(text_rect.topLeft(), text_rect.bottomLeft())
            text_gradient.setColorAt(0, QColor(255, 200, 0, 40))
            text_gradient.setColorAt(1, QColor(255, 180, 0, 20))
            painter.fillRect(text_rect, text_gradient)
            
            painter.setPen(QPen(QColor(255, 200, 0), 2))
            painter.drawRoundedRect(text_rect, 6, 6)
            painter.setPen(QPen(QColor(255, 220, 100)))
            painter.drawText(50, int(height*0.75 + 25), "📝 Text Overlay Zone")


class TimelineSection(QWidget):
    """Professional timeline for optional intro/outro asset placement with drag-and-drop"""
    
    asset_dropped = pyqtSignal(str, str)  # section, asset_id
    asset_removed = pyqtSignal(str)  # section
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.intro_asset = None
        self.outro_asset = None
        self.intro_duration = 3.0  # seconds
        self.outro_duration = 3.0  # seconds
        
        self.setFixedHeight(100)
        self.setAcceptDrops(True)
        
        # Modern styling with gradients
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a3a, stop:1 #2a2a2a);
                border: 2px solid #555;
                border-radius: 8px;
            }
        """)
        
        # Add shadow effect
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 40))
        shadow.setOffset(0, 1)
        self.setGraphicsEffect(shadow)
        
    def paintEvent(self, event):
        """Paint the timeline sections with modern UI"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width = self.width()
        height = self.height()
        
        # Modern font
        font = QFont("SF Pro Display", 10, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Calculate section widths
        intro_width = 100
        outro_width = 100
        main_width = width - intro_width - outro_width - 30
        margin = 15
        
        # Intro section with modern styling
        intro_rect = QRectF(margin, 20, intro_width, height-40)
        if self.intro_asset:
            # Active intro with green gradient
            intro_gradient = QLinearGradient(intro_rect.topLeft(), intro_rect.bottomLeft())
            intro_gradient.setColorAt(0, QColor(82, 199, 137, 200))
            intro_gradient.setColorAt(1, QColor(52, 199, 89, 180))
            painter.fillRect(intro_rect, intro_gradient)
            painter.setPen(QPen(QColor(52, 199, 89), 3))
        else:
            # Empty intro slot with dashed border
            painter.fillRect(intro_rect, QColor(60, 60, 60, 80))
            painter.setPen(QPen(QColor(120, 120, 120), 2, Qt.PenStyle.DashLine))
        painter.drawRoundedRect(intro_rect, 6, 6)
        
        # Intro text
        painter.setPen(QPen(QColor(255, 255, 255)))
        text = f"🎬 Intro\n{self.intro_duration}s" if not self.intro_asset else f"🎬 Intro\n{self.intro_duration}s\n✓ Asset Set"
        painter.drawText(intro_rect, Qt.AlignmentFlag.AlignCenter, text)
        
        # Main section (AI-generated content) with blue gradient
        main_rect = QRectF(intro_width + margin*2, 20, main_width, height-40)
        main_gradient = QLinearGradient(main_rect.topLeft(), main_rect.bottomLeft())
        main_gradient.setColorAt(0, QColor(0, 140, 255, 120))
        main_gradient.setColorAt(1, QColor(0, 120, 255, 100))
        painter.fillRect(main_rect, main_gradient)
        painter.setPen(QPen(QColor(0, 140, 255), 2))
        painter.drawRoundedRect(main_rect, 6, 6)
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(main_rect, Qt.AlignmentFlag.AlignCenter, "🤖 AI-Generated Content\n(Duration varies based on content)")
        
        # Outro section with modern styling
        outro_rect = QRectF(width - outro_width - margin, 20, outro_width, height-40)
        if self.outro_asset:
            # Active outro with red gradient
            outro_gradient = QLinearGradient(outro_rect.topLeft(), outro_rect.bottomLeft())
            outro_gradient.setColorAt(0, QColor(255, 89, 68, 200))
            outro_gradient.setColorAt(1, QColor(255, 59, 48, 180))
            painter.fillRect(outro_rect, outro_gradient)
            painter.setPen(QPen(QColor(255, 59, 48), 3))
        else:
            # Empty outro slot with dashed border
            painter.fillRect(outro_rect, QColor(60, 60, 60, 80))
            painter.setPen(QPen(QColor(120, 120, 120), 2, Qt.PenStyle.DashLine))
        painter.drawRoundedRect(outro_rect, 6, 6)
        
        # Outro text
        painter.setPen(QPen(QColor(255, 255, 255)))
        text = f"🎬 Outro\n{self.outro_duration}s" if not self.outro_asset else f"🎬 Outro\n{self.outro_duration}s\n✓ Asset Set"
        painter.drawText(outro_rect, Qt.AlignmentFlag.AlignCenter, text)
        
    def dragEnterEvent(self, event):
        """Accept asset drops"""
        if event.mimeData().hasText():
            event.acceptProposedAction()
            
    def dragMoveEvent(self, event):
        """Highlight drop zones during drag"""
        event.acceptProposedAction()
        
    def dropEvent(self, event):
        """Handle asset drop with smart positioning"""
        asset_id = event.mimeData().text()
        pos = event.position()
        
        # Determine which section was dropped on based on position
        width = self.width()
        intro_end = 115  # intro_width + margin
        outro_start = width - 115  # width - outro_width - margin
        
        section = None
        if pos.x() < intro_end:
            section = "intro"
            self.intro_asset = asset_id
        elif pos.x() > outro_start:
            section = "outro"
            self.outro_asset = asset_id
        else:
            # Dropped on main section - show helpful message
            return
            
        if section:
            self.asset_dropped.emit(section, asset_id)
            self.update()
            event.acceptProposedAction()
        
    def mousePressEvent(self, event):
        """Handle right-click to remove assets"""
        if event.button() == Qt.MouseButton.RightButton:
            pos = event.position()
            width = self.width()
            intro_end = 115
            outro_start = width - 115
            
            if pos.x() < intro_end and self.intro_asset:
                self.intro_asset = None
                self.asset_removed.emit("intro")
                self.update()
            elif pos.x() > outro_start and self.outro_asset:
                self.outro_asset = None
                self.asset_removed.emit("outro")
                self.update()
        
    def set_intro_duration(self, duration):
        """Set intro duration"""
        self.intro_duration = duration
        self.update()
        
    def set_outro_duration(self, duration):
        """Set outro duration"""
        self.outro_duration = duration
        self.update()
        
    def clear_intro(self):
        """Clear intro asset"""
        self.intro_asset = None
        self.asset_removed.emit("intro")
        self.update()
        
    def clear_outro(self):
        """Clear outro asset"""
        self.outro_asset = None
        self.asset_removed.emit("outro")
        self.update()
        
    def has_intro(self):
        """Check if intro asset is set"""
        return self.intro_asset is not None
        
    def has_outro(self):
        """Check if outro asset is set"""
        return self.outro_asset is not None


class AITemplateEditor(QWidget):
    """
    Beautiful AI-focused template editor - Smart, not hard.
    User actions automatically override AI settings, no redundant toggles.
    """
    template_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.current_content_type = "reel"
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Set up the beautiful, professional UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(main_splitter)

        # --- Left Panel: Template Preview ---
        left_panel = QFrame()
        left_panel.setMaximumWidth(500)
        left_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #252525);
                border-radius: 12px;
                border: 1px solid #444;
            }
        """)
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)
        
        # Header with content type selector
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        title_label = QLabel("✨ AI Template Designer")
        title_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        header_layout.addWidget(title_label)
        
        self.content_type_selector = QComboBox()
        self.content_type_selector.addItems(["Reel", "Story", "Post", "Tutorial"])
        self.content_type_selector.setStyleSheet("""
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #0078d4;
                border-radius: 8px;
                font-weight: bold;
                font-size: 14px;
                min-width: 120px;
                background: #333;
                color: #fff;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #0078d4;
            }
        """)
        header_layout.addWidget(self.content_type_selector)
        left_layout.addWidget(header_frame)

        # Template Preview Canvas
        canvas_wrapper = QFrame()
        canvas_wrapper.setStyleSheet("""
            QFrame {
                background: #1a1a1a;
                border: 1px solid #555;
                border-radius: 8px;
                padding: 15px;
            }
        """)
        canvas_layout = QVBoxLayout(canvas_wrapper)
        canvas_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        preview_label = QLabel("📱 Live Preview")
        preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_label.setStyleSheet("""
            QLabel {
                color: #ccc;
                font-weight: bold;
                font-size: 14px;
                padding: 10px;
            }
        """)
        canvas_layout.addWidget(preview_label)
        
        self.canvas = SimpleTemplateCanvas()
        canvas_layout.addWidget(self.canvas)
        left_layout.addWidget(canvas_wrapper)
        
        # Timeline Section (only for video content)
        self.timeline_group = QGroupBox()
        self.timeline_group.setStyleSheet("""
            QGroupBox {
                font-weight: bold;
                font-size: 14px;
                border: 2px solid #555;
                border-radius: 8px;
                margin: 5px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #3a3a3a, stop:1 #2d2d2d);
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: #fff;
            }
        """)
        self._setup_timeline_section()
        left_layout.addWidget(self.timeline_group)
        
        main_splitter.addWidget(left_panel)

        # --- Right Panel: Smart AI Settings ---
        right_panel = QFrame()
        right_panel.setMinimumWidth(380)
        right_panel.setStyleSheet("""
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #252525);
                border-radius: 12px;
                border: 1px solid #444;
            }
        """)
        
        # Scrollable settings area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                background: #333;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #555;
                border-radius: 6px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background: #666;
            }
        """)
        
        settings_widget = QWidget()
        settings_widget.setStyleSheet("background: transparent;")
        self.settings_layout = QVBoxLayout(settings_widget)
        self.settings_layout.setContentsMargins(20, 20, 20, 20)
        self.settings_layout.setSpacing(20)
        
        self._create_smart_settings()
        
        scroll_area.setWidget(settings_widget)
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(0, 0, 0, 0)
        right_layout.addWidget(scroll_area)
        
        main_splitter.addWidget(right_panel)
        main_splitter.setSizes([500, 380])

    def _setup_timeline_section(self):
        """Setup the timeline section for intro/outro"""
        self.timeline_group.setTitle("🎬 Timeline - Optional Intro/Outro")
        timeline_layout = QVBoxLayout(self.timeline_group)
        timeline_layout.setContentsMargins(15, 25, 15, 15)
        
        # Smart tip
        tip_label = QLabel("💡 Simply drag assets from your Asset Panel to add intro/outro")
        tip_label.setStyleSheet("""
            QLabel {
                color: #aaa;
                font-style: italic;
                font-size: 12px;
                padding: 8px;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 4px;
            }
        """)
        tip_label.setWordWrap(True)
        timeline_layout.addWidget(tip_label)
        
        self.timeline = TimelineSection()
        timeline_layout.addWidget(self.timeline)
        
        # Duration controls in a nice layout
        duration_frame = QFrame()
        duration_layout = QHBoxLayout(duration_frame)
        
        # Intro duration
        intro_label = QLabel("Intro:")
        intro_label.setStyleSheet("color: #52c759; font-weight: bold;")
        duration_layout.addWidget(intro_label)
        
        self.intro_duration = QSpinBox()
        self.intro_duration.setRange(1, 10)
        self.intro_duration.setValue(3)
        self.intro_duration.setSuffix("s")
        self.intro_duration.setStyleSheet("""
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #555;
                border-radius: 4px;
                background: #333;
                color: #fff;
                font-weight: bold;
            }
        """)
        duration_layout.addWidget(self.intro_duration)
        
        duration_layout.addStretch()
        
        # Outro duration
        outro_label = QLabel("Outro:")
        outro_label.setStyleSheet("color: #ff3b30; font-weight: bold;")
        duration_layout.addWidget(outro_label)
        
        self.outro_duration = QSpinBox()
        self.outro_duration.setRange(1, 10)
        self.outro_duration.setValue(3)
        self.outro_duration.setSuffix("s")
        self.outro_duration.setStyleSheet(self.intro_duration.styleSheet())
        duration_layout.addWidget(self.outro_duration)
        
        timeline_layout.addWidget(duration_frame)

    def _create_smart_settings(self):
        """Create smart AI settings - no redundant toggles"""
        
        # Header
        header_label = QLabel("🎨 Smart Template Settings")
        header_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 0;
            }
        """)
        self.settings_layout.addWidget(header_label)
        
        # Template zones - simple enable/disable
        zones_group = QGroupBox("Template Zones")
        zones_group.setStyleSheet(self._get_group_style("#0078d4"))
        zones_layout = QVBoxLayout(zones_group)
        zones_layout.setSpacing(15)
        
        # Background zone
        bg_frame = self._create_zone_frame("🎨", "Background", 
                                         "AI will choose appropriate backgrounds unless overridden")
        self.bg_enabled = QCheckBox("Enable Background Zone")
        self.bg_enabled.setChecked(True)
        self.bg_enabled.setStyleSheet(self._get_checkbox_style())
        bg_frame.layout().addWidget(self.bg_enabled)
        zones_layout.addWidget(bg_frame)
        
        # Media window zone
        media_frame = self._create_zone_frame("📹", "Media Window", 
                                            "AI will optimally position and scale your content")
        self.media_enabled = QCheckBox("Enable Media Window")
        self.media_enabled.setChecked(True)
        self.media_enabled.setStyleSheet(self._get_checkbox_style())
        media_frame.layout().addWidget(self.media_enabled)
        zones_layout.addWidget(media_frame)
        
        # Subtitle zone
        subtitle_frame = self._create_zone_frame("📝", "Text & Subtitles", 
                                               "AI will generate and style text appropriately")
        self.subtitle_enabled = QCheckBox("Enable Text Zone")
        self.subtitle_enabled.setChecked(True)
        self.subtitle_enabled.setStyleSheet(self._get_checkbox_style())
        subtitle_frame.layout().addWidget(self.subtitle_enabled)
        
        # Optional font size override
        font_override_frame = QFrame()
        font_layout = QHBoxLayout(font_override_frame)
        font_layout.setContentsMargins(0, 10, 0, 0)
        
        self.font_size_override = QCheckBox("Override font size:")
        self.font_size_override.setStyleSheet(self._get_checkbox_style("#ff9500"))
        font_layout.addWidget(self.font_size_override)
        
        self.font_size_value = QSpinBox()
        self.font_size_value.setRange(12, 72)
        self.font_size_value.setValue(24)
        self.font_size_value.setSuffix("px")
        self.font_size_value.setEnabled(False)
        self.font_size_value.setStyleSheet("""
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #555;
                border-radius: 4px;
                background: #333;
                color: #fff;
                min-width: 80px;
            }
            QSpinBox:disabled {
                background: #222;
                color: #666;
            }
        """)
        font_layout.addWidget(self.font_size_value)
        font_layout.addStretch()
        
        subtitle_frame.layout().addWidget(font_override_frame)
        zones_layout.addWidget(subtitle_frame)
        
        self.settings_layout.addWidget(zones_group)
        
        # AI Generation Controls
        self._create_generation_controls()
        
        self.settings_layout.addStretch()

    def _create_zone_frame(self, icon, title, description):
        """Create a styled frame for template zones"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(10, 10, 10, 10)
        
        title_label = QLabel(f"{icon} {title}")
        title_label.setStyleSheet("""
            QLabel {
                color: #fff;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        layout.addWidget(title_label)
        
        desc_label = QLabel(description)
        desc_label.setStyleSheet("""
            QLabel {
                color: #bbb;
                font-size: 11px;
                margin-bottom: 8px;
            }
        """)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        return frame

    def _create_generation_controls(self):
        """Create AI generation and export controls"""
        gen_group = QGroupBox("🤖 AI Generation Ready")
        gen_group.setStyleSheet(self._get_group_style("#52c759"))
        gen_layout = QVBoxLayout(gen_group)
        gen_layout.setSpacing(15)
        
        # Status info
        status_label = QLabel("✓ Template configured! Your AI assistant is ready to create amazing content.")
        status_label.setStyleSheet("""
            QLabel {
                color: #52c759;
                font-weight: bold;
                font-size: 12px;
                padding: 10px;
                background: rgba(82, 199, 89, 0.1);
                border-radius: 6px;
                border: 1px solid rgba(82, 199, 89, 0.3);
            }
        """)
        status_label.setWordWrap(True)
        gen_layout.addWidget(status_label)
        
        # Action buttons
        self.save_template_btn = self._create_action_button(
            "💾 Save Template", "#52c759", "#5ed467")
        gen_layout.addWidget(self.save_template_btn)
        
        self.export_config_btn = self._create_action_button(
            "📋 Export AI Config", "#0078d4", "#1984e0")
        gen_layout.addWidget(self.export_config_btn)
        
        self.generate_prompt_btn = self._create_action_button(
            "🚀 Generate AI Prompt", "#ff9500", "#ffad33")
        gen_layout.addWidget(self.generate_prompt_btn)
        
        self.settings_layout.addWidget(gen_group)

    def _create_action_button(self, text, color, hover_color):
        """Create a styled action button"""
        button = QPushButton(text)
        button.setStyleSheet(f"""
            QPushButton {{
                background: {color};
                color: white;
                font-weight: bold;
                font-size: 13px;
                padding: 12px 20px;
                border: none;
                border-radius: 8px;
            }}
            QPushButton:hover {{
                background: {hover_color};
            }}
            QPushButton:pressed {{
                background: {color};
                transform: translateY(1px);
            }}
        """)
        return button

    def _get_group_style(self, accent_color):
        """Get consistent group box styling"""
        return f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 14px;
                border: 2px solid {accent_color};
                border-radius: 10px;
                margin: 5px;
                padding-top: 20px;
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 rgba{self._hex_to_rgba(accent_color, 0.1)}, 
                    stop:1 rgba{self._hex_to_rgba(accent_color, 0.05)});
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top center;
                padding: 0 10px;
                color: {accent_color};
            }}
        """

    def _get_checkbox_style(self, color="#0078d4"):
        """Get consistent checkbox styling"""
        return f"""
            QCheckBox {{
                font-weight: bold;
                color: #fff;
                spacing: 8px;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 3px;
                border: 2px solid #555;
                background: #333;
            }}
            QCheckBox::indicator:checked {{
                background: {color};
                border-color: {color};
            }}
            QCheckBox::indicator:checked:after {{
                content: "✓";
                color: white;
                font-weight: bold;
            }}
        """

    def _hex_to_rgba(self, hex_color, alpha):
        """Convert hex color to rgba tuple for gradients"""
        hex_color = hex_color.lstrip('#')
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return f"({r}, {g}, {b}, {alpha})"

    def _setup_connections(self):
        """Connect signals and slots for smart behavior"""
        # Content type changes
        self.content_type_selector.currentTextChanged.connect(self._on_content_type_changed)
        
        # Template zone toggles - simple enable/disable
        self.bg_enabled.toggled.connect(self._update_template_preview)
        self.media_enabled.toggled.connect(self._update_template_preview)
        self.subtitle_enabled.toggled.connect(self._update_template_preview)
        
        # Smart font size override - when checked, enables custom size
        self.font_size_override.toggled.connect(self.font_size_value.setEnabled)
        self.font_size_override.toggled.connect(self.template_changed.emit)
        self.font_size_value.valueChanged.connect(self.template_changed.emit)
        
        # Timeline controls
        self.intro_duration.valueChanged.connect(self.timeline.set_intro_duration)
        self.outro_duration.valueChanged.connect(self.timeline.set_outro_duration)
        
        # Timeline asset management
        self.timeline.asset_dropped.connect(self._on_asset_dropped_timeline)
        self.timeline.asset_removed.connect(self._on_asset_removed_timeline)
        
        # Action buttons
        self.save_template_btn.clicked.connect(self._save_template)
        self.export_config_btn.clicked.connect(self._export_config)
        self.generate_prompt_btn.clicked.connect(self._generate_ai_prompt)
        
        # All zone changes trigger template update
        for widget in [self.bg_enabled, self.media_enabled, self.subtitle_enabled]:
            widget.toggled.connect(self.template_changed.emit)

    def _on_content_type_changed(self, content_type: str):
        """Handle content type change - smart timeline visibility"""
        self.current_content_type = content_type.lower()
        self.canvas.set_content_type(content_type)
        
        # Smart visibility: timeline only for video content
        is_video = self.current_content_type in ["reel", "story", "tutorial"]
        self.timeline_group.setVisible(is_video)
        
        self.template_changed.emit()
        
    def _update_template_preview(self):
        """Update the template preview canvas"""
        config = {
            'background_enabled': self.bg_enabled.isChecked(),
            'media_window_enabled': self.media_enabled.isChecked(),
            'subtitle_enabled': self.subtitle_enabled.isChecked()
        }
        self.canvas.update_template_config(config)
        
    def _on_asset_dropped_timeline(self, section, asset_id):
        """Handle asset dropped on timeline - smart feedback"""
        print(f"✓ {asset_id} added to {section} section")
        # Show visual feedback
        if section == "intro":
            self.timeline.set_intro_duration(self.intro_duration.value())
        else:
            self.timeline.set_outro_duration(self.outro_duration.value())
        self.template_changed.emit()
        
    def _on_asset_removed_timeline(self, section):
        """Handle asset removed from timeline"""
        print(f"✗ {section} asset removed")
        self.template_changed.emit()
        
    def set_project(self, project):
        """Set the current project"""
        self.project = project
        self._load_template_from_project()
        
    def _save_template(self):
        """Save current template to project with smart defaults"""
        if not self.project:
            print("No project loaded")
            return
            
        template_config = self._get_current_template_config()
        
        if not hasattr(self.project, 'ai_templates'):
            self.project.ai_templates = {}
            
        self.project.ai_templates[self.current_content_type] = template_config
        print(f"✅ Template saved for {self.current_content_type}")
        
    def _export_config(self):
        """Export template configuration for AI"""
        config = self._get_current_template_config()
        
        ai_config = {
            'content_type': self.current_content_type,
            'template_zones': config,
            'ai_instructions': self._generate_ai_instructions(),
            'assets': {
                'intro_asset': self.timeline.intro_asset if hasattr(self.timeline, 'intro_asset') else None,
                'outro_asset': self.timeline.outro_asset if hasattr(self.timeline, 'outro_asset') else None
            },
            'smart_overrides': {
                'font_size_override': self.font_size_override.isChecked(),
                'custom_font_size': self.font_size_value.value() if self.font_size_override.isChecked() else None
            }
        }
        
        import json
        from pathlib import Path
        output_file = Path(f"ai_template_{self.current_content_type}.json")
        with open(output_file, 'w') as f:
            json.dump(ai_config, f, indent=2)
            
        print(f"📋 AI config exported to {output_file}")
        
    def _generate_ai_prompt(self):
        """Generate smart AI prompt based on template settings"""
        prompt_parts = [f"Create a stunning {self.current_content_type} using this template configuration:"]
        
        config = self._get_current_template_config()
        
        # Add zone instructions with smart logic
        if config['zones']['background']['enabled']:
            prompt_parts.append("🎨 Background: AI has full creative control over background design and aesthetics")
                
        if config['zones']['media_window']['enabled']:
            prompt_parts.append("📹 Media: AI should optimally position and scale media for maximum visual impact")
                
        if config['zones']['subtitle']['enabled']:
            if self.font_size_override.isChecked():
                prompt_parts.append(f"📝 Text: Use {self.font_size_value.value()}px font size, AI controls positioning and styling")
            else:
                prompt_parts.append("📝 Text: AI has full control over text sizing, positioning, and styling")
                
        # Add smart timeline instructions
        if hasattr(self.timeline, 'intro_asset') and self.timeline.intro_asset:
            prompt_parts.append(f"🎬 Intro: Use asset '{self.timeline.intro_asset}' for {self.intro_duration.value()}s opening")
        if hasattr(self.timeline, 'outro_asset') and self.timeline.outro_asset:
            prompt_parts.append(f"🎬 Outro: Use asset '{self.timeline.outro_asset}' for {self.outro_duration.value()}s closing")
            
        prompt_parts.append("\n🚀 Create engaging, professional content that captures attention and delivers value!")
            
        prompt = "\n• ".join(prompt_parts)
        
        # Save prompt
        from pathlib import Path
        output_file = Path(f"ai_prompt_{self.current_content_type}.txt")
        with open(output_file, 'w') as f:
            f.write(prompt)
            
        print("🤖 Smart AI Prompt Generated:")
        print("=" * 50)
        print(prompt)
        print("=" * 50)
        print(f"💾 Saved to {output_file}")
        
    def _get_current_template_config(self):
        """Get current template configuration with smart defaults"""
        return {
            'content_type': self.current_content_type,
            'zones': {
                'background': {
                    'enabled': self.bg_enabled.isChecked()
                },
                'media_window': {
                    'enabled': self.media_enabled.isChecked()
                },
                'subtitle': {
                    'enabled': self.subtitle_enabled.isChecked()
                }
            },
            'smart_overrides': {
                'font_size_override': self.font_size_override.isChecked(),
                'font_size_value': self.font_size_value.value() if self.font_size_override.isChecked() else None
            },
            'timeline': {
                'intro_asset': getattr(self.timeline, 'intro_asset', None),
                'intro_duration': self.intro_duration.value(),
                'outro_asset': getattr(self.timeline, 'outro_asset', None),
                'outro_duration': self.outro_duration.value(),
                'has_intro': self.timeline.has_intro() if hasattr(self.timeline, 'has_intro') else False,
                'has_outro': self.timeline.has_outro() if hasattr(self.timeline, 'has_outro') else False
            }
        }
        
    def _generate_ai_instructions(self):
        """Generate smart AI instructions"""
        instructions = []
        
        instructions.append("Smart Template Configuration for AI Content Generation")
        instructions.append(f"Content Type: {self.current_content_type.title()}")
        instructions.append("")
        
        config = self._get_current_template_config()
        
        instructions.append("Template Zones:")
        if config['zones']['background']['enabled']:
            instructions.append("• Background: AI has full creative control - choose/generate appropriate backgrounds")
                
        if config['zones']['media_window']['enabled']:
            instructions.append("• Media Window: AI should optimally position and scale media content for impact")
                
        if config['zones']['subtitle']['enabled']:
            instructions.append("• Text/Subtitles: AI controls text generation and styling")
            if config['smart_overrides']['font_size_override']:
                instructions.append(f"  - Font size override: {config['smart_overrides']['font_size_value']}px")
            else:
                instructions.append("  - Font size: AI choice")
                
        if config['timeline']['has_intro'] or config['timeline']['has_outro']:
            instructions.append("")
            instructions.append("Timeline Assets:")
            if config['timeline']['has_intro']:
                instructions.append(f"• Intro: {config['timeline']['intro_duration']}s using asset '{config['timeline']['intro_asset']}'")
            if config['timeline']['has_outro']:
                instructions.append(f"• Outro: {config['timeline']['outro_duration']}s using asset '{config['timeline']['outro_asset']}'")
                
        instructions.append("")
        instructions.append("Smart Logic: User-specified settings override AI defaults. AI has creative freedom elsewhere.")
                
        return "\n".join(instructions)
        
    def _load_template_from_project(self):
        """Load existing template from project"""
        if not self.project or not hasattr(self.project, 'ai_templates'):
            return
            
        if self.current_content_type in self.project.ai_templates:
            config = self.project.ai_templates[self.current_content_type]
            self._apply_template_config(config)
            
    def _apply_template_config(self, config):
        """Apply loaded template configuration with smart defaults"""
        zones = config.get('zones', {})
        
        # Apply zone settings
        if 'background' in zones:
            self.bg_enabled.setChecked(zones['background'].get('enabled', True))
            
        if 'media_window' in zones:
            self.media_enabled.setChecked(zones['media_window'].get('enabled', True))
            
        if 'subtitle' in zones:
            self.subtitle_enabled.setChecked(zones['subtitle'].get('enabled', True))
            
        # Apply smart overrides
        overrides = config.get('smart_overrides', {})
        self.font_size_override.setChecked(overrides.get('font_size_override', False))
        if overrides.get('font_size_value'):
            self.font_size_value.setValue(overrides['font_size_value'])
        
        # Apply timeline settings
        timeline_config = config.get('timeline', {})
        if timeline_config.get('intro_asset') and hasattr(self.timeline, 'intro_asset'):
            self.timeline.intro_asset = timeline_config['intro_asset']
        if timeline_config.get('outro_asset') and hasattr(self.timeline, 'outro_asset'):
            self.timeline.outro_asset = timeline_config['outro_asset']
        self.intro_duration.setValue(timeline_config.get('intro_duration', 3))
        self.outro_duration.setValue(timeline_config.get('outro_duration', 3))
        
        self._update_template_preview()
