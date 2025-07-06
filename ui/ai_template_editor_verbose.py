"""
Beautiful AI-Focused Template Editor for ReelTune
Professional, intuitive interface focusing only on essential AI-driven template settings.
Smart design: user actions automatically override AI, no redundant toggles.
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QGroupBox, QPushButton, QSplitter, QCheckBox, 
    QSpinBox, QScrollArea, QGraphicsDropShadowEffect,
    QApplication, QDialog, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QSizeF
from PyQt6.QtGui import QColor, QPainter, QPen, QFont, QLinearGradient
from datetime import datetime
import json


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
        """Draw zones for video content with live subtitle preview"""
        font = QFont("Arial", 11, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Background zone (always full canvas)
        if self.template_config.get('background_enabled', True):
            painter.setPen(QPen(QColor(120, 120, 120), 2, Qt.PenStyle.DashLine))
            painter.drawRoundedRect(8, 8, int(width-16), int(height-16), 6, 6)
            painter.setPen(QPen(QColor(200, 200, 200)))
            painter.drawText(20, 35, "🎨 Background Zone")
            painter.setPen(QPen(QColor(160, 160, 160)))
            painter.drawText(20, 55, "AI will choose/generate")
        
        # Media window zone (main content area)
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
        
        # Live Subtitle Preview Zone with EXACT positioning and font size
        if self.template_config.get('subtitle_enabled', True):
            self._draw_live_subtitle_preview(painter, width, height)
            
    def _draw_live_subtitle_preview(self, painter, width, height):
        """Draw LIVE subtitle preview with EXACT positioning and font size"""
        # Get current subtitle settings
        subtitle_pos = getattr(self, 'current_subtitle_position', 'Bottom')
        font_size = getattr(self, 'current_font_size', 24)
        is_fixed = getattr(self, 'current_subtitle_fixed', False)
        
        # Calculate subtitle zone based on EXACT position
        if subtitle_pos == 'Top':
            subtitle_rect = QRectF(25, 90, width-50, height*0.18)
            subtitle_y = 130
        elif subtitle_pos == 'Center':
            subtitle_rect = QRectF(25, height*0.4, width-50, height*0.2)
            subtitle_y = height*0.5
        else:  # Bottom
            subtitle_rect = QRectF(25, height*0.72, width-50, height*0.23)
            subtitle_y = height*0.82
        
        # Draw subtitle zone background with enhanced styling
        subtitle_gradient = QLinearGradient(subtitle_rect.topLeft(), subtitle_rect.bottomLeft())
        if is_fixed:
            # Special styling for fixed variables
            subtitle_gradient.setColorAt(0, QColor(255, 149, 0, 80))
            subtitle_gradient.setColorAt(1, QColor(255, 149, 0, 40))
            border_color = QColor(255, 149, 0)
            border_width = 4
        else:
            subtitle_gradient.setColorAt(0, QColor(120, 120, 120, 60))
            subtitle_gradient.setColorAt(1, QColor(120, 120, 120, 30))
            border_color = QColor(120, 120, 120)
            border_width = 2
            
        painter.fillRect(subtitle_rect, subtitle_gradient)
        painter.setPen(QPen(border_color, border_width))
        painter.drawRoundedRect(subtitle_rect, 6, 6)
        
        # Calculate preview font size (scale appropriately for preview)
        preview_font_size = max(8, int(font_size * 0.4))  # Scale down but keep readable
        subtitle_font = QFont("Arial", preview_font_size, QFont.Weight.Bold)
        painter.setFont(subtitle_font)
        
        # Live sample subtitle text with real measurements
        if is_fixed:
            sample_text = f"LIVE PREVIEW: {subtitle_pos.upper()}"
            size_text = f"Font: {font_size}px (Fixed for ALL content)"
        else:
            sample_text = "Sample Subtitle Text Here"
            size_text = f"Font: {font_size}px (AI Controlled)"
        
        # Draw text with shadow for better visibility
        shadow_offset = 2
        painter.setPen(QPen(QColor(0, 0, 0, 200)))
        shadow_rect = subtitle_rect.adjusted(shadow_offset, shadow_offset, shadow_offset, shadow_offset)
        painter.drawText(shadow_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, sample_text)
        
        # Draw main text
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.drawText(subtitle_rect, Qt.AlignmentFlag.AlignCenter | Qt.AlignmentFlag.AlignVCenter, sample_text)
        
        # Draw detailed position and size indicator
        info_font = QFont("Arial", 9, QFont.Weight.Medium)
        painter.setFont(info_font)
        
        if is_fixed:
            painter.setPen(QPen(QColor(255, 149, 0)))
            info_text = f"📌 FIXED: {subtitle_pos} Position | {font_size}px Font"
        else:
            painter.setPen(QPen(QColor(150, 150, 150)))
            info_text = f"📝 AI Controlled: {subtitle_pos} | {font_size}px"
            
        painter.drawText(int(subtitle_rect.x() + 10), int(subtitle_rect.y() - 12), info_text)
        
        # Draw size information below
        size_font = QFont("Arial", 8)
        painter.setFont(size_font)
        painter.setPen(QPen(QColor(180, 180, 180)))
        painter.drawText(int(subtitle_rect.x() + 10), int(subtitle_rect.bottom() + 15), size_text)
        
    def update_subtitle_preview(self, position, font_size, is_fixed):
        """Update the live subtitle preview with EXACT current settings"""
        self.current_subtitle_position = position
        self.current_font_size = font_size
        self.current_subtitle_fixed = is_fixed
        self.update()  # Immediate repaint for live preview
            
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
        """Set up the beautiful, professional UI with proper resizing"""
        # Main layout
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(15)
        
        # Create splitter for resizable panels - PROPERLY CONFIGURED
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        main_splitter.setHandleWidth(8)  # Make handle easier to grab
        main_splitter.setChildrenCollapsible(False)  # Prevent collapsing panels
        main_splitter.setStyleSheet("""
            QSplitter::handle {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #666, stop:0.5 #888, stop:1 #666);
                width: 8px;
                border-radius: 4px;
                margin: 2px 0;
            }
            QSplitter::handle:hover {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:0.5 #1984e0, stop:1 #0078d4);
            }
            QSplitter::handle:pressed {
                background: #52c759;
            }
        """)
        main_layout.addWidget(main_splitter)

        # --- Left Panel: Template Preview ---
        left_panel = QFrame()
        left_panel.setMinimumWidth(420)  # Slightly wider minimum
        left_panel.setMaximumWidth(800)  # Prevent too wide
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

        # --- Right Panel: Smart AI Settings - PROPERLY RESIZABLE ---
        right_panel = QFrame()
        right_panel.setMinimumWidth(350)  # Smaller minimum for better resizing
        right_panel.setMaximumWidth(600)  # Reasonable maximum
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
        
        # Set proper resizing behavior and initial sizes
        main_splitter.setStretchFactor(0, 1)  # Left panel can grow
        main_splitter.setStretchFactor(1, 1)  # Right panel can grow  
        main_splitter.setSizes([520, 400])  # Initial sizes in pixels

    def _setup_timeline_section(self):
        """Setup the timeline section for intro/outro with AI choice options"""
        self.timeline_group.setTitle("🎬 Timeline - Smart Intro/Outro Control")
        timeline_layout = QVBoxLayout(self.timeline_group)
        timeline_layout.setContentsMargins(15, 25, 15, 15)
        
        # Smart tip
        tip_label = QLabel("💡 Drag assets for custom intro/outro, or let AI decide what works best")
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
        
        # AI Choice Controls
        ai_choice_frame = QFrame()
        ai_choice_frame.setStyleSheet("""
            QFrame {
                background: rgba(82, 199, 89, 0.1);
                border: 1px solid rgba(82, 199, 89, 0.3);
                border-radius: 8px;
                padding: 10px;
                margin: 5px 0;
            }
        """)
        ai_choice_layout = QHBoxLayout(ai_choice_frame)
        
        ai_choice_label = QLabel("🤖 AI Decision Mode:")
        ai_choice_label.setStyleSheet("color: #52c759; font-weight: bold;")
        ai_choice_layout.addWidget(ai_choice_label)
        
        self.intro_ai_chooses = QCheckBox("Let AI choose intro")
        self.intro_ai_chooses.setStyleSheet(self._get_checkbox_style("#52c759"))
        ai_choice_layout.addWidget(self.intro_ai_chooses)
        
        ai_choice_layout.addStretch()
        
        self.outro_ai_chooses = QCheckBox("Let AI choose outro")
        self.outro_ai_chooses.setStyleSheet(self._get_checkbox_style("#52c759"))
        ai_choice_layout.addWidget(self.outro_ai_chooses)
        
        timeline_layout.addWidget(ai_choice_frame)
        
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
        
        # Fixed Variables System
        self._create_fixed_variables_section()
        
        # Template zones with override options
        zones_group = QGroupBox("Template Zones with Override Options")
        zones_group.setStyleSheet(self._get_group_style("#0078d4"))
        zones_layout = QVBoxLayout(zones_group)
        zones_layout.setSpacing(15)
        
        # Background zone with drag & drop override
        bg_frame = self._create_zone_frame_with_override("🎨", "Background", 
                                         "AI will choose backgrounds, or drag your own")
        self.bg_enabled = QCheckBox("Enable Background Zone")
        self.bg_enabled.setChecked(True)
        self.bg_enabled.setStyleSheet(self._get_checkbox_style())
        bg_frame.layout().addWidget(self.bg_enabled)
        
        # Background override toggle
        self.bg_override = QCheckBox("Override with custom background")
        self.bg_override.setStyleSheet(self._get_checkbox_style("#ff9500"))
        bg_frame.layout().addWidget(self.bg_override)
        
        # Background drop zone
        self.bg_drop_zone = self._create_drop_zone("Drag background asset here")
        self.bg_drop_zone.setVisible(False)
        bg_frame.layout().addWidget(self.bg_drop_zone)
        
        zones_layout.addWidget(bg_frame)
        
        # Media window zone with drag & drop override
        media_frame = self._create_zone_frame_with_override("📹", "Media Window", 
                                            "AI will position content, or drag your specific media")
        self.media_enabled = QCheckBox("Enable Media Window")
        self.media_enabled.setChecked(True)
        self.media_enabled.setStyleSheet(self._get_checkbox_style())
        media_frame.layout().addWidget(self.media_enabled)
        
        # Media override toggle
        self.media_override = QCheckBox("Override with specific media")
        self.media_override.setStyleSheet(self._get_checkbox_style("#ff9500"))
        media_frame.layout().addWidget(self.media_override)
        
        # Media drop zone
        self.media_drop_zone = self._create_drop_zone("Drag media asset here")
        self.media_drop_zone.setVisible(False)
        media_frame.layout().addWidget(self.media_drop_zone)
        
        zones_layout.addWidget(media_frame)
        
        # Subtitle zone (no override needed - handled by fixed variables)
        subtitle_frame = self._create_zone_frame("📝", "Text & Subtitles", 
                                               "AI will generate and style text appropriately")
        self.subtitle_enabled = QCheckBox("Enable Text Zone")
        self.subtitle_enabled.setChecked(True)
        self.subtitle_enabled.setStyleSheet(self._get_checkbox_style())
        subtitle_frame.layout().addWidget(self.subtitle_enabled)
        
        zones_layout.addWidget(subtitle_frame)
        
        self.settings_layout.addWidget(zones_group)
        
        # AI Generation Controls
        self._create_generation_controls()
        
        self.settings_layout.addStretch()

    def _create_fixed_variables_section(self):
        """Create fixed variables system - properties that override AI for CURRENT content type"""
        fixed_vars_group = QGroupBox("📌 Fixed Variables for Current Content Type")
        fixed_vars_group.setStyleSheet(self._get_group_style("#ff9500"))
        fixed_vars_layout = QVBoxLayout(fixed_vars_group)
        fixed_vars_layout.setSpacing(15)
        
        # Explanation
        explanation = QLabel("Set properties for this specific content type - overrides AI defaults for this type only")
        explanation.setStyleSheet("""
            QLabel {
                color: #ff9500;
                font-style: italic;
                font-size: 12px;
                padding: 8px;
                background: rgba(255, 149, 0, 0.1);
                border-radius: 4px;
                border: 1px solid rgba(255, 149, 0, 0.3);
            }
        """)
        explanation.setWordWrap(True)
        fixed_vars_layout.addWidget(explanation)
        
        # Subtitle Position Fixed Variable
        subtitle_pos_frame = QFrame()
        subtitle_pos_frame.setStyleSheet("""
            QFrame {
                background: rgba(255, 149, 0, 0.05);
                border-radius: 8px;
                padding: 10px;
            }
        """)
        subtitle_pos_layout = QVBoxLayout(subtitle_pos_frame)
        
        # Subtitle position controls
        subtitle_pos_header = QLabel("📝 Subtitle Position Override")
        subtitle_pos_header.setStyleSheet("color: #fff; font-weight: bold; font-size: 14px;")
        subtitle_pos_layout.addWidget(subtitle_pos_header)
        
        subtitle_controls_frame = QFrame()
        subtitle_controls_layout = QHBoxLayout(subtitle_controls_frame)
        subtitle_controls_layout.setContentsMargins(0, 5, 0, 0)
        
        self.subtitle_position_fixed = QCheckBox("Fix subtitle position:")
        self.subtitle_position_fixed.setStyleSheet(self._get_checkbox_style("#ff9500"))
        subtitle_controls_layout.addWidget(self.subtitle_position_fixed)
        
        self.subtitle_position_combo = QComboBox()
        self.subtitle_position_combo.addItems(["Top", "Center", "Bottom"])
        self.subtitle_position_combo.setCurrentText("Bottom")
        self.subtitle_position_combo.setEnabled(False)
        self.subtitle_position_combo.setStyleSheet("""
            QComboBox {
                padding: 6px 10px;
                border: 1px solid #ff9500;
                border-radius: 6px;
                background: #333;
                color: #fff;
                min-width: 80px;
            }
            QComboBox:disabled {
                background: #222;
                color: #666;
                border-color: #666;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 4px solid #ff9500;
            }
        """)
        subtitle_controls_layout.addWidget(self.subtitle_position_combo)
        subtitle_controls_layout.addStretch()
        
        subtitle_pos_layout.addWidget(subtitle_controls_frame)
        
        # Font size fixed variable
        font_size_controls_frame = QFrame()
        font_size_controls_layout = QHBoxLayout(font_size_controls_frame)
        font_size_controls_layout.setContentsMargins(0, 5, 0, 0)
        
        self.font_size_fixed = QCheckBox("Fix font size:")
        self.font_size_fixed.setStyleSheet(self._get_checkbox_style("#ff9500"))
        font_size_controls_layout.addWidget(self.font_size_fixed)
        
        self.font_size_value = QSpinBox()
        self.font_size_value.setRange(12, 72)
        self.font_size_value.setValue(24)
        self.font_size_value.setSuffix("px")
        self.font_size_value.setEnabled(False)
        self.font_size_value.setStyleSheet("""
            QSpinBox {
                padding: 4px 8px;
                border: 1px solid #ff9500;
                border-radius: 4px;
                background: #333;
                color: #fff;
                min-width: 80px;
            }
            QSpinBox:disabled {
                background: #222;
                color: #666;
                border-color: #666;
            }
        """)
        font_size_controls_layout.addWidget(self.font_size_value)
        font_size_controls_layout.addStretch()
        
        subtitle_pos_layout.addWidget(font_size_controls_frame)
        fixed_vars_layout.addWidget(subtitle_pos_frame)
        
        self.settings_layout.addWidget(fixed_vars_group)

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

    def _create_zone_frame_with_override(self, icon, title, description):
        """Create a styled frame for template zones with override capability"""
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
        
    def _create_drop_zone(self, placeholder_text):
        """Create a drag & drop zone for assets"""
        drop_zone = QLabel(placeholder_text)
        drop_zone.setAcceptDrops(True)
        drop_zone.setStyleSheet("""
            QLabel {
                background: rgba(255, 149, 0, 0.1);
                border: 2px dashed #ff9500;
                border-radius: 8px;
                padding: 20px;
                text-align: center;
                color: #ff9500;
                font-weight: bold;
                min-height: 60px;
            }
            QLabel:hover {
                background: rgba(255, 149, 0, 0.2);
                border-color: #ffad33;
            }
        """)
        drop_zone.setAlignment(Qt.AlignmentFlag.AlignCenter)
        return drop_zone

    def _create_generation_controls(self):
        """Create unified AI generation and export controls"""
        gen_group = QGroupBox("🚀 AI Generation Hub")
        gen_group.setStyleSheet(self._get_group_style("#52c759"))
        gen_layout = QVBoxLayout(gen_group)
        gen_layout.setSpacing(15)
        
        # Smart status with dynamic updates
        self.status_label = QLabel()
        self._update_status_message()
        self.status_label.setStyleSheet("""
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
        self.status_label.setWordWrap(True)
        gen_layout.addWidget(self.status_label)
        
        # Unified save/export button with smart behavior
        self.unified_save_btn = self._create_action_button(
            "💾 Save & Export Template", "#52c759", "#5ed467")
        self.unified_save_btn.clicked.connect(self._unified_save_and_export)
        gen_layout.addWidget(self.unified_save_btn)
        
        # Smart AI prompt generation
        self.smart_prompt_btn = self._create_action_button(
            "🤖 Generate Smart AI Prompt", "#0078d4", "#1984e0")
        self.smart_prompt_btn.clicked.connect(self._generate_smart_ai_prompt)
        gen_layout.addWidget(self.smart_prompt_btn)
        
        # Quick preview generation
        self.preview_btn = self._create_action_button(
            "�️ Preview AI Instructions", "#ff9500", "#ffad33")
        self.preview_btn.clicked.connect(self._preview_ai_instructions)
        gen_layout.addWidget(self.preview_btn)
        
        # Template validation indicator
        self.validation_frame = QFrame()
        self.validation_frame.setStyleSheet("""
            QFrame {
                background: rgba(0, 120, 255, 0.1);
                border: 1px solid rgba(0, 120, 255, 0.3);
                border-radius: 6px;
                padding: 8px;
            }
        """)
        validation_layout = QHBoxLayout(self.validation_frame)
        validation_layout.setContentsMargins(8, 8, 8, 8)
        
        self.validation_icon = QLabel("✓")
        self.validation_icon.setStyleSheet("color: #52c759; font-weight: bold; font-size: 14px;")
        validation_layout.addWidget(self.validation_icon)
        
        self.validation_text = QLabel("Template ready for AI generation")
        self.validation_text.setStyleSheet("color: #0078d4; font-weight: bold; font-size: 11px;")
        validation_layout.addWidget(self.validation_text)
        validation_layout.addStretch()
        
        gen_layout.addWidget(self.validation_frame)
        
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
        
        # Fixed Variables System - apply to CURRENT content type with IMMEDIATE live preview
        self.subtitle_position_fixed.toggled.connect(self.subtitle_position_combo.setEnabled)
        self.subtitle_position_fixed.toggled.connect(self._on_fixed_variable_changed)
        self.subtitle_position_fixed.toggled.connect(self._update_live_preview)  # Immediate preview
        
        self.subtitle_position_combo.currentTextChanged.connect(self._on_fixed_variable_changed)
        self.subtitle_position_combo.currentTextChanged.connect(self._update_live_preview)  # Immediate preview
        
        self.font_size_fixed.toggled.connect(self.font_size_value.setEnabled)
        self.font_size_fixed.toggled.connect(self._on_fixed_variable_changed)
        self.font_size_fixed.toggled.connect(self._update_live_preview)  # Immediate preview
        
        self.font_size_value.valueChanged.connect(self._on_fixed_variable_changed)
        self.font_size_value.valueChanged.connect(self._update_live_preview)  # Immediate preview
        
        # Override system connections
        self.bg_override.toggled.connect(self.bg_drop_zone.setVisible)
        self.media_override.toggled.connect(self.media_drop_zone.setVisible)
        
        # AI Choice Controls for intro/outro - BLOCK DURATION CONTROLS
        self.intro_ai_chooses.toggled.connect(self._on_ai_choice_changed)
        self.intro_ai_chooses.toggled.connect(lambda checked: self.intro_duration.setEnabled(not checked))
        
        self.outro_ai_chooses.toggled.connect(self._on_ai_choice_changed)
        self.outro_ai_chooses.toggled.connect(lambda checked: self.outro_duration.setEnabled(not checked))
        
        # Timeline controls
        self.intro_duration.valueChanged.connect(self.timeline.set_intro_duration)
        self.outro_duration.valueChanged.connect(self.timeline.set_outro_duration)
        
        # Timeline asset management
        self.timeline.asset_dropped.connect(self._on_asset_dropped_timeline)
        self.timeline.asset_removed.connect(self._on_asset_removed_timeline)
        
        # All zone changes trigger template update and validation
        for widget in [self.bg_enabled, self.media_enabled, self.subtitle_enabled]:
            widget.toggled.connect(self._update_template_preview)
            widget.toggled.connect(self._validate_template)
            widget.toggled.connect(self.template_changed.emit)
            
        # Initialize live preview immediately
        self._update_live_preview()
        self._validate_template()

    def _on_fixed_variable_changed(self):
        """Handle fixed variable changes - these apply to CURRENT content type only"""
        self._update_live_preview()
        self._update_status_message()
        self._validate_template()
        self.template_changed.emit()
        print(f"✓ Fixed variable updated for {self.current_content_type} content type")
        
    def _update_live_preview(self):
        """Update the live subtitle preview with current settings IMMEDIATELY"""
        position = self.subtitle_position_combo.currentText()
        font_size = self.font_size_value.value()
        is_fixed = self.subtitle_position_fixed.isChecked() or self.font_size_fixed.isChecked()
        
        # Update canvas immediately
        self.canvas.update_subtitle_preview(position, font_size, is_fixed)
        
        # Debug output for user feedback
        print(f"🎨 Live Preview Updated: {position} position, {font_size}px font, Fixed: {is_fixed}")
        
    def _on_ai_choice_changed(self):
        """Handle AI choice toggle for intro/outro - BLOCK DURATION CONTROLS"""
        # When AI chooses is enabled, disable manual asset dropping AND duration controls
        if self.intro_ai_chooses.isChecked():
            # Clear any existing intro asset
            if hasattr(self.timeline, 'intro_asset') and self.timeline.intro_asset:
                self.timeline.clear_intro()
            # Block duration control
            self.intro_duration.setEnabled(False)
        else:
            # Re-enable duration control
            self.intro_duration.setEnabled(True)
        
        if self.outro_ai_chooses.isChecked():
            # Clear any existing outro asset
            if hasattr(self.timeline, 'outro_asset') and self.timeline.outro_asset:
                self.timeline.clear_outro()
            # Block duration control
            self.outro_duration.setEnabled(False)
        else:
            # Re-enable duration control
            self.outro_duration.setEnabled(True)
        
        self._update_status_message()
        self._validate_template()
        self.template_changed.emit()
        print(f"✓ AI choice updated - intro: {self.intro_ai_chooses.isChecked()}, outro: {self.outro_ai_chooses.isChecked()}")

    def _on_content_type_changed(self, content_type: str):
        """Handle content type change - load per-content-type settings"""
        self.current_content_type = content_type.lower()
        self.canvas.set_content_type(content_type)
        
        # Smart visibility: timeline only for video content
        is_video = self.current_content_type in ["reel", "story", "tutorial"]
        self.timeline_group.setVisible(is_video)
        
        # Load per-content-type settings
        self._load_template_from_project()
        
        self.template_changed.emit()
        print(f"📋 Switched to {self.current_content_type} - loading specific settings")
        
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
        
    def _save_template_internal(self):
        """Internal save method for unified functionality"""
        if not self.project:
            return False
            
        template_config = self._get_current_template_config()
        
        if not hasattr(self.project, 'ai_templates'):
            self.project.ai_templates = {}
            
        self.project.ai_templates[self.current_content_type] = template_config
        print(f"✅ Template saved for {self.current_content_type}")
        return True
        
    def _export_config_internal(self):
        """Internal export method for unified functionality"""
        try:
            config = self._get_current_template_config()
            
            ai_config = {
                'content_type': self.current_content_type,
                'template_zones': config['zones'],
                'fixed_variables': config['fixed_variables'],
                'ai_choices': config['ai_choices'],
                'timeline': config['timeline'],
                'ai_instructions': self._generate_smart_ai_instructions(),
                'assets': {
                    'intro_asset': self.timeline.intro_asset if hasattr(self.timeline, 'intro_asset') and not self.intro_ai_chooses.isChecked() else None,
                    'outro_asset': self.timeline.outro_asset if hasattr(self.timeline, 'outro_asset') and not self.outro_ai_chooses.isChecked() else None
                },
                'export_timestamp': datetime.now().isoformat(),
                'template_version': '3.0'
            }
            
            from pathlib import Path
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = Path(f"super_smart_ai_template_{self.current_content_type}_{timestamp}.json")
            
            import json
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(ai_config, f, indent=2, ensure_ascii=False)
                
            print(f"📋 Super Smart AI config exported to {output_file}")
            return True
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False
    
    def _generate_smart_ai_instructions(self):
        """Generate comprehensive AI instructions with smart context"""
        instructions = []
        config = self._get_current_template_config()
        
        # Header with metadata
        instructions.append("🤖 SMART TEMPLATE CONFIGURATION FOR AI CONTENT GENERATION")
        instructions.append("=" * 60)
        instructions.append(f"Content Type: {self.current_content_type.title()}")
        instructions.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        instructions.append(f"Template Version: 3.0 (Super Smart AI Editor)")
        instructions.append("")
        
        # Fixed Variables System (applies to CURRENT content type)
        fixed_vars = []
        if config['fixed_variables']['subtitle_position_fixed']:
            fixed_vars.append(f"Subtitle Position: {config['fixed_variables']['subtitle_position_value']}")
        if config['fixed_variables']['font_size_fixed']:
            fixed_vars.append(f"Font Size: {config['fixed_variables']['font_size_value']}px")
            
        if fixed_vars:
            instructions.append(f"📌 FIXED VARIABLES FOR {self.current_content_type.upper()} CONTENT:")
            for var in fixed_vars:
                instructions.append(f"   → {var} - MUST be used for this content type")
            instructions.append(f"   → These settings override AI defaults for {self.current_content_type} content")
            instructions.append("")
        
        # Zone configuration with override detection
        enabled_zones = []
        instructions.append("📋 TEMPLATE ZONES CONFIGURATION:")
        
        if config['zones']['background']['enabled']:
            enabled_zones.append("Background")
            instructions.append("🎨 Background Zone: ENABLED")
            if hasattr(self, 'bg_override') and self.bg_override.isChecked():
                instructions.append("   → OVERRIDE: User-specified background asset will be used")
            else:
                instructions.append("   → AI has full creative control over background design")
            instructions.append("   → Choose or generate backgrounds that enhance content theme")
            
        if config['zones']['media_window']['enabled']:
            enabled_zones.append("Media Window")
            instructions.append("📹 Media Window Zone: ENABLED")
            if hasattr(self, 'media_override') and self.media_override.isChecked():
                instructions.append("   → OVERRIDE: User-specified media asset will be used")
            else:
                instructions.append("   → AI should intelligently position and scale media content")
            instructions.append("   → Optimize for maximum visual impact and engagement")
            
        if config['zones']['subtitle']['enabled']:
            enabled_zones.append("Text/Subtitles")
            instructions.append("📝 Text/Subtitle Zone: ENABLED")
            instructions.append("   → AI controls text generation and styling")
            if config['fixed_variables']['subtitle_position_fixed']:
                instructions.append(f"   → FIXED POSITION: {config['fixed_variables']['subtitle_position_value']} (for {self.current_content_type} content)")
            if config['fixed_variables']['font_size_fixed']:
                instructions.append(f"   → FIXED FONT SIZE: {config['fixed_variables']['font_size_value']}px (for {self.current_content_type} content)")
            if not config['fixed_variables']['subtitle_position_fixed'] and not config['fixed_variables']['font_size_fixed']:
                instructions.append("   → AI has complete control over positioning and typography")
            instructions.append("   → Optimize for readability and visual hierarchy")
        
        instructions.append("")
        
        # AI Choice System for Timeline
        ai_choices = []
        if config['ai_choices']['intro_ai_chooses']:
            ai_choices.append("Intro")
        if config['ai_choices']['outro_ai_chooses']:
            ai_choices.append("Outro")
            
        if ai_choices:
            instructions.append("🤖 AI DECISION ZONES:")
            for choice in ai_choices:
                instructions.append(f"   → {choice}: AI should decide whether to include and what content to use")
            instructions.append("   → AI has full creative freedom for these elements")
            instructions.append("")
        
        # Timeline assets with smart integration
        if config['timeline']['has_intro'] or config['timeline']['has_outro']:
            instructions.append("🎬 TIMELINE ASSET INTEGRATION:")
            
            if config['timeline']['has_intro']:
                instructions.append(f"📥 Intro Sequence: {config['timeline']['intro_duration']}s")
                instructions.append(f"   → Asset: '{config['timeline']['intro_asset']}'")
                instructions.append("   → Create smooth transition from intro to main content")
                instructions.append("   → Ensure engaging opening that captures attention")
                
            if config['timeline']['has_outro']:
                instructions.append(f"📤 Outro Sequence: {config['timeline']['outro_duration']}s")
                instructions.append(f"   → Asset: '{config['timeline']['outro_asset']}'")
                instructions.append("   → Create memorable conclusion with clear call-to-action")
                instructions.append("   → Smooth transition from main content to outro")
                
            instructions.append("")
        
        # Content type specific optimization
        instructions.append("🎯 CONTENT TYPE OPTIMIZATION:")
        
        type_optimizations = {
            'reel': [
                "→ Focus on immediate hook within first 3 seconds",
                "→ Use quick cuts and dynamic transitions",
                "→ Optimize for mobile viewing and vertical format",
                "→ Include trending elements and shareable moments"
            ],
            'story': [
                "→ Emphasize personal connection and authenticity",
                "→ Use intimate framing and natural transitions",
                "→ Create narrative flow that keeps viewers engaged",
                "→ Optimize for full-screen mobile experience"
            ],
            'post': [
                "→ Create thumb-stopping visual impact",
                "→ Ensure instant message comprehension",
                "→ Use bold visuals and clear hierarchy",
                "→ Optimize for feed-based consumption"
            ],
            'tutorial': [
                "→ Prioritize clarity and step-by-step progression",
                "→ Use clean, structured layout with clear sections",
                "→ Ensure educational value and easy following",
                "→ Include visual cues and progress indicators"
            ]
        }
        
        for optimization in type_optimizations.get(self.current_content_type, []):
            instructions.append(f"   {optimization}")
        
        instructions.append("")
        
        # Smart AI directives
        instructions.append("🚀 SUPER SMART AI DIRECTIVES:")
        instructions.append(f"   → FIXED VARIABLES override AI defaults for {self.current_content_type} content type")
        instructions.append("   → OVERRIDE ASSETS take precedence over AI-generated content")
        instructions.append("   → AI chooses elements have complete creative freedom")
        instructions.append("   → User-specified settings take precedence over AI defaults")
        instructions.append("   → AI has creative freedom in non-specified areas")
        instructions.append("   → Optimize for platform-specific best practices")
        instructions.append("   → Ensure professional quality and brand consistency")
        instructions.append("   → Maximize viewer engagement and content value")
        instructions.append("   → Apply current design trends while maintaining timeless appeal")
        
        instructions.append("")
        instructions.append("✨ FINAL NOTE: This is a super smart template configuration where:")
        instructions.append(f"   • Fixed variables apply to {self.current_content_type} content type specifically")
        instructions.append("   • Override assets replace AI-generated content in those zones")
        instructions.append("   • AI choice elements are completely AI-controlled")
        instructions.append("   • User choices take precedence over AI defaults")
        instructions.append("   Create content that exceeds expectations!")
        
        return "\n".join(instructions)
        instructions.append("   → User-specified settings ALWAYS override AI defaults")
        instructions.append("   → AI has creative freedom in non-specified areas")
        instructions.append("   → Optimize for platform-specific best practices")
        instructions.append("   → Ensure professional quality and brand consistency")
        instructions.append("   → Maximize viewer engagement and content value")
        instructions.append("   → Apply current design trends while maintaining timeless appeal")
        
        instructions.append("")
        instructions.append("✨ FINAL NOTE: This is a smart template configuration where user choices")
        instructions.append("   take precedence over AI defaults. Create content that exceeds expectations!")
        
        return "\n".join(instructions)
        
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
            'fixed_variables': {
                'subtitle_position_fixed': self.subtitle_position_fixed.isChecked(),
                'subtitle_position_value': self.subtitle_position_combo.currentText() if self.subtitle_position_fixed.isChecked() else None,
                'font_size_fixed': self.font_size_fixed.isChecked(),
                'font_size_value': self.font_size_value.value() if self.font_size_fixed.isChecked() else None
            },
            'ai_choices': {
                'intro_ai_chooses': self.intro_ai_chooses.isChecked(),
                'outro_ai_chooses': self.outro_ai_chooses.isChecked()
            },
            'timeline': {
                'intro_asset': getattr(self.timeline, 'intro_asset', None) if not self.intro_ai_chooses.isChecked() else None,
                'intro_duration': self.intro_duration.value(),
                'outro_asset': getattr(self.timeline, 'outro_asset', None) if not self.outro_ai_chooses.isChecked() else None,
                'outro_duration': self.outro_duration.value(),
                'has_intro': self.timeline.has_intro() if hasattr(self.timeline, 'has_intro') and not self.intro_ai_chooses.isChecked() else False,
                'has_outro': self.timeline.has_outro() if hasattr(self.timeline, 'has_outro') and not self.outro_ai_chooses.isChecked() else False
            }
        }
        
        
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
            
        # Apply fixed variables
        fixed_vars = config.get('fixed_variables', {})
        self.subtitle_position_fixed.setChecked(fixed_vars.get('subtitle_position_fixed', False))
        if fixed_vars.get('subtitle_position_value'):
            self.subtitle_position_combo.setCurrentText(fixed_vars['subtitle_position_value'])
        self.font_size_fixed.setChecked(fixed_vars.get('font_size_fixed', False))
        if fixed_vars.get('font_size_value'):
            self.font_size_value.setValue(fixed_vars['font_size_value'])
            
        # Apply AI choices
        ai_choices = config.get('ai_choices', {})
        self.intro_ai_chooses.setChecked(ai_choices.get('intro_ai_chooses', False))
        self.outro_ai_chooses.setChecked(ai_choices.get('outro_ai_chooses', False))
        
        # Apply timeline settings
        timeline_config = config.get('timeline', {})
        if timeline_config.get('intro_asset') and hasattr(self.timeline, 'intro_asset'):
            self.timeline.intro_asset = timeline_config['intro_asset']
        if timeline_config.get('outro_asset') and hasattr(self.timeline, 'outro_asset'):
            self.timeline.outro_asset = timeline_config['outro_asset']
        self.intro_duration.setValue(timeline_config.get('intro_duration', 3))
        self.outro_duration.setValue(timeline_config.get('outro_duration', 3))
        
        self._update_template_preview()
    
    def _update_status_message(self):
        """Update the smart status message based on current configuration"""
        config = self._get_current_template_config()
        
        # Count enabled zones
        enabled_zones = sum([
            config['zones']['background']['enabled'],
            config['zones']['media_window']['enabled'],
            config['zones']['subtitle']['enabled']
        ])
        
        # Check for all types of overrides
        fixed_vars_count = sum([
            config['fixed_variables']['subtitle_position_fixed'],
            config['fixed_variables']['font_size_fixed']
        ])
        
        ai_choices_count = sum([
            config['ai_choices']['intro_ai_chooses'],
            config['ai_choices']['outro_ai_chooses']
        ])
        
        has_timeline_assets = config['timeline']['has_intro'] or config['timeline']['has_outro']
        
        # Generate comprehensive status message
        status_parts = []
        
        if enabled_zones == 0:
            message = "⚠️ No zones enabled. Enable at least one zone for AI generation."
            color = "#ff9500"
        else:
            # Basic zones status
            status_parts.append(f"✨ {enabled_zones} zone{'s' if enabled_zones > 1 else ''} active")
            
            # Fixed variables status
            if fixed_vars_count > 0:
                status_parts.append(f"📌 {fixed_vars_count} fixed variable{'s' if fixed_vars_count > 1 else ''} (apply to ALL content types)")
            
            # AI choices status
            if ai_choices_count > 0:
                status_parts.append(f"🤖 {ai_choices_count} AI decision{'s' if ai_choices_count > 1 else ''} enabled")
            
            # Timeline assets status
            if has_timeline_assets:
                status_parts.append("🎬 Custom timeline assets")
            
            if fixed_vars_count > 0 or ai_choices_count > 0 or has_timeline_assets:
                message = f"🎯 Perfect! {' • '.join(status_parts)}. Smart template ready!"
                color = "#52c759"
            else:
                message = f"👍 {status_parts[0]}. AI has full creative control for {self.current_content_type}s."
                color = "#0078d4"
            
        if hasattr(self, 'status_label'):
            self.status_label.setText(message)
            # Update color based on status
            if color == "#ff9500":
                bg_color = "rgba(255, 149, 0, 0.1)"
                border_color = "rgba(255, 149, 0, 0.3)"
            elif color == "#52c759":
                bg_color = "rgba(82, 199, 89, 0.1)"
                border_color = "rgba(82, 199, 89, 0.3)"
            else:
                bg_color = "rgba(0, 120, 255, 0.1)"
                border_color = "rgba(0, 120, 255, 0.3)"
                
            self.status_label.setStyleSheet(f"""
                QLabel {{
                    color: {color};
                    font-weight: bold;
                    font-size: 12px;
                    padding: 10px;
                    background: {bg_color};
                    border-radius: 6px;
                    border: 1px solid {border_color};
                }}
            """)
    
    def _validate_template(self):
        """Super smart template validation with comprehensive feedback"""
        config = self._get_current_template_config()
        
        # Count enabled zones and timeline elements
        enabled_zones = sum([
            config['zones']['background']['enabled'],
            config['zones']['media_window']['enabled'],
            config['zones']['subtitle']['enabled']
        ])
        
        timeline_elements = 0
        if config['timeline']['has_intro']:
            timeline_elements += 1
        if config['timeline']['has_outro']:
            timeline_elements += 1
            
        fixed_variables = sum([
            config['fixed_variables']['subtitle_position_fixed'],
            config['fixed_variables']['font_size_fixed']
        ])
        
        is_valid = enabled_zones > 0
        
        # Update validation UI with smart feedback
        if hasattr(self, 'validation_icon') and hasattr(self, 'validation_text'):
            if is_valid:
                self.validation_icon.setText("✓")
                self.validation_icon.setStyleSheet("color: #52c759; font-weight: bold; font-size: 14px;")
                
                # Smart status message
                status_parts = [f"{enabled_zones} zone{'s' if enabled_zones != 1 else ''}"]
                if timeline_elements > 0:
                    status_parts.append(f"{timeline_elements} timeline element{'s' if timeline_elements > 1 else ''}")
                if fixed_variables > 0:
                    status_parts.append(f"{fixed_variables} fixed variable{'s' if fixed_variables > 1 else ''}")
                    
                self.validation_text.setText(f"✨ Template ready - {', '.join(status_parts)} configured")
                self.validation_text.setStyleSheet("color: #52c759; font-weight: bold; font-size: 11px;")
                
                # Enable action buttons when valid
                if hasattr(self, 'unified_save_btn'):
                    self.unified_save_btn.setEnabled(True)
                if hasattr(self, 'smart_prompt_btn'):
                    self.smart_prompt_btn.setEnabled(True)
                if hasattr(self, 'preview_btn'):
                    self.preview_btn.setEnabled(True)
                    
            else:
                self.validation_icon.setText("⚠️")
                self.validation_icon.setStyleSheet("color: #ff9500; font-weight: bold; font-size: 14px;")
                self.validation_text.setText("Enable at least one template zone to continue")
                self.validation_text.setStyleSheet("color: #ff9500; font-weight: bold; font-size: 11px;")
                
                # Disable action buttons when invalid
                if hasattr(self, 'unified_save_btn'):
                    self.unified_save_btn.setEnabled(False)
                if hasattr(self, 'smart_prompt_btn'):
                    self.smart_prompt_btn.setEnabled(False)
                if hasattr(self, 'preview_btn'):
                    self.preview_btn.setEnabled(False)
        
        self._update_status_message()
        return is_valid
    
    def _unified_save_and_export(self):
        """Super smart unified save and export with comprehensive feedback"""
        try:
            # Validate first with smart feedback
            if not self._validate_template():
                self._show_smart_message("⚠️ Template Incomplete", 
                                       "Please enable at least one template zone before saving.", 
                                       "warning")
                return
            
            config = self._get_current_template_config()
            
            # Count configured elements for smart feedback
            zones_count = sum([config['zones'][z]['enabled'] for z in config['zones']])
            timeline_count = sum([config['timeline']['has_intro'], config['timeline']['has_outro']])
            fixed_vars_count = sum([config['fixed_variables']['subtitle_position_fixed'], config['fixed_variables']['font_size_fixed']])
            ai_choices_count = sum([config['ai_choices']['intro_ai_chooses'], config['ai_choices']['outro_ai_chooses']])
            
            # Save to project (internal)
            success_save = self._save_template_internal()
            
            # Export AI configuration (external)
            success_export = self._export_config_internal()
            
            # Generate comprehensive feedback
            if success_save and success_export:
                # Create detailed success message
                message_parts = []
                message_parts.append(f"✅ Template saved & AI config exported!")
                message_parts.append(f"📋 Configuration: {zones_count} zone{'s' if zones_count != 1 else ''}")
                
                if timeline_count > 0:
                    intro_text = "intro" if config['timeline']['has_intro'] else ""
                    outro_text = "outro" if config['timeline']['has_outro'] else ""
                    timeline_text = " + ".join(filter(None, [intro_text, outro_text]))
                    message_parts.append(f"🎬 Timeline: {timeline_text} configured")
                    
                if fixed_vars_count > 0:
                    message_parts.append(f"📌 Fixed variables: {fixed_vars_count} applied (ALL content types)")
                    
                if ai_choices_count > 0:
                    message_parts.append(f"🤖 AI decisions: {ai_choices_count} enabled")
                    
                message_parts.append(f"🎯 Ready for {self.current_content_type} AI generation")
                
                # Show enhanced success dialog
                self._show_enhanced_success_dialog("\n".join(message_parts), config)
                
            elif success_save and not success_export:
                self._show_smart_message("⚠️ Partial Success", 
                                       "Template saved to project, but AI config export failed.", 
                                       "warning")
            elif not success_save and success_export:
                self._show_smart_message("⚠️ Partial Success", 
                                       "AI config exported, but project save failed.", 
                                       "warning")
            else:
                self._show_smart_message("❌ Save Error", 
                                       "Failed to save template and export configuration.", 
                                       "error")
                
        except Exception as e:
            self._show_smart_message("❌ Unexpected Error", 
                                   f"An error occurred during save/export: {str(e)}", 
                                   "error")
    
    def _generate_smart_ai_prompt(self):
        """Generate an intelligent, context-aware AI prompt"""
        if not self._validate_template():
            self._show_smart_message("⚠️ Template Incomplete", 
                                   "Please configure template zones before generating AI prompt.", 
                                   "warning")
            return
            
        config = self._get_current_template_config()
        
        # Smart prompt generation with context awareness
        prompt_parts = []
        
        # Dynamic opening based on content type and configuration
        content_adjectives = {
            'reel': 'engaging, viral',
            'story': 'intimate, compelling', 
            'post': 'eye-catching, shareable',
            'tutorial': 'clear, educational'
        }
        
        prompt_parts.append(f"Create a {content_adjectives.get(self.current_content_type, 'stunning')} {self.current_content_type} with these intelligent template settings:")
        
        # Zone-specific instructions with smart context
        active_zones = []
        if config['zones']['background']['enabled']:
            active_zones.append("🎨 Background")
            prompt_parts.append("🎨 Background Design: AI has full creative control - select or generate backgrounds that complement the content theme and enhance visual appeal")
                
        if config['zones']['media_window']['enabled']:
            active_zones.append("📹 Media")
            prompt_parts.append("📹 Media Positioning: AI should intelligently position and scale media content for maximum visual impact and optimal viewing experience")
                
        if config['zones']['subtitle']['enabled']:
            active_zones.append("📝 Text")
            if config['fixed_variables']['font_size_fixed']:
                prompt_parts.append(f"📝 Text & Typography: Use FIXED {config['fixed_variables']['font_size_value']}px font size (applies to ALL content types), AI controls positioning, styling, and text generation for maximum readability")
            else:
                prompt_parts.append("📝 Text & Typography: AI has complete control over font sizing, positioning, styling, and text generation - optimize for readability and visual hierarchy")
        
        # Smart timeline integration
        timeline_elements = []
        if config['timeline']['has_intro']:
            timeline_elements.append(f"🎬 Intro ({config['timeline']['intro_duration']}s)")
            prompt_parts.append(f"🎬 Opening Sequence: Integrate asset '{config['timeline']['intro_asset']}' as a {config['timeline']['intro_duration']}-second intro - create smooth transitions and engaging opening")
            
        if config['timeline']['has_outro']:
            timeline_elements.append(f"🎬 Outro ({config['timeline']['outro_duration']}s)")
            prompt_parts.append(f"🎬 Closing Sequence: Use asset '{config['timeline']['outro_asset']}' for a {config['timeline']['outro_duration']}-second outro - ensure memorable conclusion with clear call-to-action")
        
        # Content type specific guidelines
        type_guidelines = {
            'reel': 'Focus on hook, retention, and shareability. Use trending elements and quick cuts.',
            'story': 'Emphasize personal connection and authentic storytelling. Use intimate framing.',
            'post': 'Optimize for thumb-stopping power and instant comprehension. Bold visuals.',
            'tutorial': 'Prioritize clarity, step-by-step flow, and educational value. Clean, structured layout.'
        }
        
        prompt_parts.append(f"🎯 {self.current_content_type.title()} Strategy: {type_guidelines.get(self.current_content_type, 'Create engaging, professional content')}")
        
        # Smart optimization instructions
        prompt_parts.append("🚀 AI Optimization Goals:")
        prompt_parts.append("• Maximize visual impact and viewer engagement")
        prompt_parts.append("• Ensure professional quality and brand consistency") 
        prompt_parts.append("• Optimize for platform-specific best practices")
        prompt_parts.append("• Create content that captures attention and delivers value")
        
        # Compile final prompt
        prompt_header = f"🤖 SMART AI PROMPT for {self.current_content_type.upper()}"
        prompt_metadata = f"Template: {', '.join(active_zones)} | Timeline: {', '.join(timeline_elements) if timeline_elements else 'AI-controlled duration'}"
        prompt_body = "\n\n• ".join(prompt_parts)
        
        full_prompt = f"{prompt_header}\n{'-' * len(prompt_header)}\n{prompt_metadata}\n\n• {prompt_body}"
        
        # Save prompt with timestamp
        from pathlib import Path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(f"smart_ai_prompt_{self.current_content_type}_{timestamp}.txt")
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(full_prompt)
                
            # Show success with details
            zones_count = len(active_zones);
            timeline_count = len(timeline_elements);
            
            success_msg = f"🤖 Smart AI prompt generated!\n"
            success_msg += f"• {zones_count} template zone{'s' if zones_count != 1 else ''} configured\n"
            if timeline_count > 0:
                success_msg += f"• {timeline_count} timeline element{'s' if timeline_count > 1 else ''} integrated\n"
            success_msg += f"• Optimized for {self.current_content_type} content\n"
            success_msg += f"• Saved to: {output_file.name}"
            
            self._show_smart_message("🚀 AI Prompt Ready!", success_msg, "success")
            
            print("🤖 SMART AI PROMPT GENERATED")
            print("=" * 60)
            print(full_prompt)
            print("=" * 60)
            print(f"💾 Saved to: {output_file}")
            
        except Exception as e:
            self._show_smart_message("❌ Export Error", f"Failed to save prompt: {str(e)}", "error")
    
    def _preview_ai_instructions(self):
        """Show a preview of AI instructions in a user-friendly format"""
        if not self._validate_template():
            self._show_smart_message("⚠️ Template Incomplete", 
                                   "Please configure template zones before previewing instructions.", 
                                   "warning")
            return
            
        instructions = self._generate_smart_ai_instructions()
        
        # Create preview dialog
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🤖 AI Instructions Preview")
        dialog.setModal(True)
        dialog.resize(600, 500)
        
        layout = QVBoxLayout(dialog)
        
        # Header
        header = QLabel("Preview of instructions that will be sent to AI:")
        header.setStyleSheet("font-weight: bold; font-size: 14px; color: #0078d4; padding: 10px;")
        layout.addWidget(header)
        
        # Instructions text
        text_edit = QTextEdit()
        text_edit.setPlainText(instructions)
        text_edit.setStyleSheet("""
            QTextEdit {
                background: #2d2d2d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
                font-size: 12px;
            }
        """)
        text_edit.setReadOnly(True)
        layout.addWidget(text_edit)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        copy_btn = QPushButton("📋 Copy to Clipboard")
        copy_btn.setStyleSheet(self._get_button_style("#0078d4"))
        copy_btn.clicked.connect(lambda: QApplication.clipboard().setText(instructions))
        button_layout.addWidget(copy_btn)
        
        close_btn = QPushButton("✓ Close")
        close_btn.setStyleSheet(self._get_button_style("#52c759"))
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec()
    
    def _show_smart_message(self, title, message, type="info"):
        """Show smart contextual messages to user"""
        from PyQt6.QtWidgets import QMessageBox
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if type == "success":
            msg_box.setIcon(QMessageBox.Icon.Information)
        elif type == "warning":
            msg_box.setIcon(QMessageBox.Icon.Warning)
        elif type == "error":
            msg_box.setIcon(QMessageBox.Icon.Critical)
        else:
            msg_box.setIcon(QMessageBox.Icon.Information)
            
        msg_box.exec()
    
    def _get_button_style(self, color):
        """Get consistent button styling"""
        return f"""
            QPushButton {{
                background: {color};
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border: none;
                border-radius: 6px;
            }}
            QPushButton:hover {{
                background: {self._lighten_color(color)};
            }}
        """
    
    def _lighten_color(self, hex_color):
        """Lighten a hex color for hover effects"""
        color_map = {
            "#0078d4": "#1984e0",
            "#52c759": "#5ed467",
            "#ff9500": "#ffad33",
            "#ff3b30": "#ff5a50"
        }
        return color_map.get(hex_color, hex_color)
    
    def set_project(self, project):
        """Set the current project"""
        self.project = project
        self._load_template_from_project()
        self._validate_template()  # Validate on project load
    
    def _show_enhanced_success_dialog(self, message, config):
        """Show enhanced success dialog with additional options"""
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QTextEdit
        
        dialog = QDialog(self)
        dialog.setWindowTitle("🚀 Template Successfully Configured!")
        dialog.setModal(True)
        dialog.resize(500, 400)
        
        layout = QVBoxLayout(dialog)
        
        # Success message
        success_label = QLabel(message)
        success_label.setStyleSheet("""
            QLabel {
                color: #52c759;
                font-weight: bold;
                font-size: 14px;
                padding: 15px;
                background: rgba(82, 199, 89, 0.1);
                border: 1px solid #52c759;
                border-radius: 8px;
            }
        """)
        success_label.setWordWrap(True)
        layout.addWidget(success_label)
        
        # Quick summary
        summary_label = QLabel("📋 Configuration Summary:")
        summary_label.setStyleSheet("font-weight: bold; font-size: 13px; color: #0078d4; margin-top: 10px;")
        layout.addWidget(summary_label)
        
        # Configuration details
        details = []
        if config['zones']['background']['enabled']:
            details.append("🎨 Background: AI controlled")
        if config['zones']['media_window']['enabled']:
            details.append("📹 Media Window: AI positioned")
        if config['zones']['subtitle']['enabled']:
            details.append("📝 Subtitles: AI generated")
        if config['timeline']['has_intro']:
            details.append(f"🎬 Intro: {config['timeline']['intro_duration']}s with {config['timeline']['intro_asset']}")
        if config['timeline']['has_outro']:
            details.append(f"🎬 Outro: {config['timeline']['outro_duration']}s with {config['timeline']['outro_asset']}")
        if config['fixed_variables']['subtitle_position_fixed']:
            details.append(f"📌 Subtitle Position: {config['fixed_variables']['subtitle_position_value']} (ALL content types)")
        if config['fixed_variables']['font_size_fixed']:
            details.append(f"📌 Font Size: {config['fixed_variables']['font_size_value']}px (ALL content types)")
        if config['ai_choices']['intro_ai_chooses']:
            details.append("🤖 Intro: AI will decide")
        if config['ai_choices']['outro_ai_chooses']:
            details.append("🤖 Outro: AI will decide")
            
        details_text = QTextEdit()
        details_text.setPlainText("\n".join(details))
        details_text.setStyleSheet("""
            QTextEdit {
                background: #2d2d2d;
                color: #fff;
                border: 1px solid #555;
                border-radius: 6px;
                padding: 10px;
                font-family: monospace;
                font-size: 11px;
            }
        """)
        details_text.setReadOnly(True)
        details_text.setMaximumHeight(120)
        layout.addWidget(details_text)
        
        # Action buttons
        button_layout = QHBoxLayout()
        
        # Generate AI Prompt button
        prompt_btn = QPushButton("🤖 Generate AI Prompt")
        prompt_btn.setStyleSheet(self._get_button_style("#0078d4"))
        prompt_btn.clicked.connect(lambda: (dialog.accept(), self._generate_smart_ai_prompt()))
        button_layout.addWidget(prompt_btn)
        
        # Preview Instructions button  
        preview_btn = QPushButton("👁️ Preview Instructions")
        preview_btn.setStyleSheet(self._get_button_style("#ff9500"))
        preview_btn.clicked.connect(lambda: self._preview_ai_instructions())
        button_layout.addWidget(preview_btn)
        
        # Close button
        close_btn = QPushButton("✓ Done")
        close_btn.setStyleSheet(self._get_button_style("#52c759"))
        close_btn.clicked.connect(dialog.accept)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
        
        dialog.exec()
