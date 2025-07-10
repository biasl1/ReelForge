"""
Enhanced Asset Panel with Thumbnails and Previews

Professional asset management interface with visual previews, right-click context menus,
and content categorization for AI-ready content creation.

Features:
- Thumbnail generation for images, videos, and audio files
- Right-click context menus for edit/delete operations
- Content categorization system
- Asset description editing for AI context
- Background thumbnail processing
- Professional visual design

Author: Assistant
License: MIT
"""

import os
import subprocess
import tempfile
from pathlib import Path
from typing import Optional

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QScrollArea, QFrame, QGridLayout, QMessageBox, QFileDialog,
    QApplication, QSizePolicy, QMenu, QDialog, QDialogButtonBox,
    QTextEdit, QFormLayout, QComboBox, QLineEdit
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QThread, pyqtSlot, QMimeData, QRect
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QFont, QIcon, QPen, QAction, QDrag

from core.logging_config import log_info, log_error, log_warning, log_debug


class XplainPackSessionDialog(QDialog):
    """Dialog for viewing/editing XplainPack session metadata"""

    def __init__(self, session_data, parent=None):
        super().__init__(parent)
        self.session_data = session_data
        self.setWindowTitle(f"XplainPack Session: {session_data.get('name', 'Unknown')}")
        self.setModal(True)
        self.resize(500, 400)

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # Header
        header_frame = QFrame()
        header_frame.setStyleSheet("background-color: #2d2d30; border-radius: 5px; padding: 10px;")
        header_layout = QVBoxLayout(header_frame)
        
        title_label = QLabel("XplainPack Session Details")
        title_label.setStyleSheet("color: #cccccc; font-size: 16px; font-weight: bold;")
        header_layout.addWidget(title_label)
        
        layout.addWidget(header_frame)

        # Form layout
        form_layout = QFormLayout()

        # Session ID (read-only)
        self.session_id_label = QLabel()
        self.session_id_label.setStyleSheet("font-weight: bold; color: #007acc;")
        form_layout.addRow("Session ID:", self.session_id_label)

        # Session name
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("Enter session name...")
        form_layout.addRow("Name:", self.name_edit)

        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Describe the content of this XplainPack session...")
        form_layout.addRow("Description:", self.description_edit)

        # File information (read-only)
        self.video_file_label = QLabel()
        self.video_file_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        form_layout.addRow("Video File:", self.video_file_label)

        self.audio_file_label = QLabel()
        self.audio_file_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        form_layout.addRow("Audio File:", self.audio_file_label)

        # Duration info
        self.duration_label = QLabel()
        self.duration_label.setStyleSheet("color: #cccccc; font-size: 11px;")
        form_layout.addRow("Duration:", self.duration_label)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _load_data(self):
        """Load session data into the form"""
        self.session_id_label.setText(self.session_data.get('id', 'N/A'))
        self.name_edit.setText(self.session_data.get('name', ''))
        self.description_edit.setPlainText(self.session_data.get('description', ''))
        
        # File information
        video_file = self.session_data.get('video_file', 'N/A')
        audio_file = self.session_data.get('audio_file', 'N/A')
        self.video_file_label.setText(video_file)
        self.audio_file_label.setText(audio_file)
        
        # Duration
        duration = self.session_data.get('duration', 'Unknown')
        self.duration_label.setText(str(duration))

    def get_updated_data(self):
        """Get the updated session data"""
        updated_data = self.session_data.copy()
        updated_data['name'] = self.name_edit.text().strip()
        updated_data['description'] = self.description_edit.toPlainText().strip()
        return updated_data


class AssetDescriptionDialog(QDialog):
    """Dialog for editing asset description and category"""

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.setWindowTitle(f"Edit Asset: {asset.name}")
        self.setModal(True)
        self.resize(400, 250)

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Form layout
        form_layout = QFormLayout()

        # Asset name (read-only)
        name_label = QLabel(self.asset.name)
        name_label.setStyleSheet("font-weight: bold; color: #007acc;")
        form_layout.addRow("Asset Name:", name_label)

        # Content category
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "General",
            "Intro",
            "Demo",
            "Tutorial",
            "Outro",
            "Background",
            "UI/Interface",
            "Audio Sample"
        ])
        form_layout.addRow("Category:", self.category_combo)

        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Add description to help AI understand this asset's purpose and content...")
        form_layout.addRow("Description:", self.description_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _load_data(self):
        """Load current asset data"""
        # Set category if it exists in description or folder
        current_category = getattr(self.asset, 'folder', '') or 'General'
        index = self.category_combo.findText(current_category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)

        # Set description
        description = getattr(self.asset, 'description', '')
        self.description_edit.setPlainText(description)

    def get_category(self) -> str:
        """Get selected category"""
        return self.category_combo.currentText()

    def get_description(self) -> str:
        """Get description text"""
        return self.description_edit.toPlainText().strip()


class ThumbnailWorker(QThread):
    """Background worker for generating thumbnails"""

    thumbnail_ready = pyqtSignal(str, QPixmap)  # asset_id, thumbnail

    def __init__(self, asset_id: str, file_path: str, file_type: str):
        super().__init__()
        self.asset_id = asset_id
        self.file_path = file_path
        self.file_type = file_type

    def run(self):
        """Generate thumbnail in background"""
        try:
            if self.file_type == "image":
                thumbnail = self.create_image_thumbnail()
            elif self.file_type == "video":
                thumbnail = self.create_video_thumbnail()
            elif self.file_type == "xplainpack":
                thumbnail = self.create_xplainpack_thumbnail()
            else:
                thumbnail = self.create_icon_thumbnail()

            if thumbnail and not thumbnail.isNull():
                self.thumbnail_ready.emit(self.asset_id, thumbnail)
        except Exception as e:
            log_error(f"Error generating thumbnail for {self.asset_id}: {e}")

    def create_xplainpack_thumbnail(self) -> QPixmap:
        """Create thumbnail for XplainPack sessions"""
        thumbnail = QPixmap(150, 150)
        thumbnail.fill(QColor(255, 107, 53))  # Orange background for XplainPacks
        
        painter = QPainter(thumbnail)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw XplainPack icon design
        # Background gradient
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 150, 150)
        gradient.setColorAt(0, QColor(255, 107, 53))  # Orange
        gradient.setColorAt(1, QColor(204, 85, 42))   # Darker orange
        painter.fillRect(thumbnail.rect(), QBrush(gradient))
        
        # Draw microphone icon (for voice/audio)
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setBrush(QBrush(QColor(255, 255, 255)))
        
        # Microphone body
        center_x, center_y = 75, 65
        mic_rect = QRect(center_x - 12, center_y - 20, 24, 30)
        painter.drawRoundedRect(mic_rect, 12, 12)
        
        # Microphone stand
        painter.drawLine(center_x, center_y + 10, center_x, center_y + 30)
        painter.drawLine(center_x - 15, center_y + 30, center_x + 15, center_y + 30)
        
        # Sound waves
        painter.setPen(QPen(QColor(255, 255, 255, 150), 2))
        for i, radius in enumerate([35, 45, 55]):
            painter.drawArc(center_x - radius//2, center_y - radius//2, radius, radius, 45*16, 90*16)
        
        # Video play symbol overlay
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255, 200)))
        
        # Small play triangle
        play_x, play_y = 110, 110
        play_size = 8
        from PyQt6.QtCore import QPoint
        from PyQt6.QtGui import QPolygon
        play_triangle = QPolygon([
            QPoint(play_x - play_size//2, play_y - play_size//2),
            QPoint(play_x - play_size//2, play_y + play_size//2),
            QPoint(play_x + play_size//2, play_y)
        ])
        painter.drawPolygon(play_triangle)
        
        # XplainPack label
        painter.setFont(QFont("Arial", 9, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.drawText(10, 140, "XPLAINPACK")
        
        painter.end()
        return thumbnail

    def create_image_thumbnail(self) -> QPixmap:
        """Create thumbnail for image files"""
        pixmap = QPixmap(self.file_path)
        if pixmap.isNull():
            return self.create_icon_thumbnail("image")

        # Scale to thumbnail size maintaining aspect ratio
        return pixmap.scaled(
            150, 150,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )

    def create_video_thumbnail(self) -> QPixmap:
        """Create thumbnail for video files"""
        try:
            # Try to use Qt's video capabilities first
            from PyQt6.QtMultimedia import QMediaPlayer
            from PyQt6.QtMultimediaWidgets import QVideoWidget

            # For now, create a nice video icon as fallback
            # Future enhancement: implement proper video frame extraction
            return self.create_icon_thumbnail("video")

        except ImportError:
            # Qt Multimedia not available, use icon
            return self.create_icon_thumbnail("video")

    def add_play_overlay(self, thumbnail: QPixmap) -> QPixmap:
        """Add play button overlay to video thumbnail"""
        # Create a copy to draw on
        result = QPixmap(thumbnail)
        painter = QPainter(result)

        # Semi-transparent overlay
        overlay = QBrush(QColor(0, 0, 0, 100))
        painter.fillRect(result.rect(), overlay)

        # Play button
        painter.setPen(QPen(QColor(255, 255, 255), 3))
        painter.setBrush(QBrush(QColor(255, 255, 255, 200)))

        center_x = result.width() // 2
        center_y = result.height() // 2
        size = min(result.width(), result.height()) // 4

        # Draw play triangle
        points = [
            (center_x - size//2, center_y - size//2),
            (center_x - size//2, center_y + size//2),
            (center_x + size//2, center_y)
        ]

        from PyQt6.QtCore import QPoint
        from PyQt6.QtGui import QPolygon

        play_triangle = QPolygon([QPoint(x, y) for x, y in points])
        painter.drawPolygon(play_triangle)

        painter.end()
        return result

    def create_icon_thumbnail(self, file_type: str = "other") -> QPixmap:
        """Create icon-based thumbnail for audio and other files"""
        # Create a 150x150 thumbnail with icon
        thumbnail = QPixmap(150, 150)
        thumbnail.fill(QColor(40, 40, 40))  # Dark background

        painter = QPainter(thumbnail)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Create gradient background
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 0, 150)

        if file_type == "audio":
            gradient.setColorAt(0, QColor(70, 130, 180))  # Steel blue
            gradient.setColorAt(1, QColor(25, 25, 112))   # Midnight blue
            icon_text = "♪"
            label_text = "AUDIO"
            label_color = QColor(173, 216, 230)  # Light blue
        elif file_type == "video":
            gradient.setColorAt(0, QColor(220, 20, 60))   # Crimson
            gradient.setColorAt(1, QColor(139, 0, 0))     # Dark red
            icon_text = "▶"
            label_text = "VIDEO"
            label_color = QColor(255, 182, 193)  # Light pink
        elif file_type == "image":
            gradient.setColorAt(0, QColor(50, 205, 50))   # Lime green
            gradient.setColorAt(1, QColor(0, 100, 0))     # Dark green
            icon_text = "🖼"
            label_text = "IMAGE"
            label_color = QColor(144, 238, 144)  # Light green
        else:
            gradient.setColorAt(0, QColor(105, 105, 105)) # Dim gray
            gradient.setColorAt(1, QColor(47, 79, 79))    # Dark slate gray
            icon_text = "📄"
            label_text = "FILE"
            label_color = QColor(192, 192, 192)  # Silver

        # Fill background with gradient
        painter.fillRect(thumbnail.rect(), QBrush(gradient))

        # Draw main icon circle
        painter.setPen(QPen(QColor(255, 255, 255, 100), 2))
        painter.setBrush(QBrush(QColor(255, 255, 255, 30)))
        painter.drawEllipse(35, 35, 80, 80)

        # Draw icon symbol
        painter.setPen(QPen(QColor(255, 255, 255), 2))
        painter.setFont(QFont("Arial", 28, QFont.Weight.Bold))
        painter.drawText(65, 85, icon_text)

        # Draw type label
        painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        painter.setPen(QPen(label_color, 2))
        text_rect = painter.fontMetrics().boundingRect(label_text)
        x = (150 - text_rect.width()) // 2
        painter.drawText(x, 130, label_text)

        # Add subtle border
        painter.setPen(QPen(QColor(100, 100, 100), 1))
        painter.drawRect(0, 0, 149, 149)

        painter.end()
        return thumbnail


class AssetThumbnailWidget(QFrame):
    """Individual asset widget with thumbnail and info"""

    clicked = pyqtSignal(str)  # asset_id
    double_clicked = pyqtSignal(str)  # asset_id
    edit_requested = pyqtSignal(str)  # asset_id
    delete_requested = pyqtSignal(str)  # asset_id

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.thumbnail_worker = None

        self.setFixedSize(180, 220)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setStyleSheet("""
            AssetThumbnailWidget {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            AssetThumbnailWidget:hover {
                background-color: #4a4a4a;
                border: 1px solid #007acc;
            }
        """)

        self.setup_ui()
        self.generate_thumbnail()

        # Enable context menu
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def setup_ui(self):
        """Setup the widget UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(5)

        # Thumbnail area
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(150, 150)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                background-color: #2d2d2d;
                border: 1px solid #666666;
                border-radius: 4px;
            }
        """)

        # Placeholder while loading
        placeholder = QPixmap(150, 150)
        placeholder.fill(QColor(45, 45, 45))
        painter = QPainter(placeholder)
        painter.setPen(QColor(150, 150, 150))
        painter.setFont(QFont("Arial", 10))
        painter.drawText(placeholder.rect(), Qt.AlignmentFlag.AlignCenter, "Loading...")
        painter.end()
        self.thumbnail_label.setPixmap(placeholder)

        layout.addWidget(self.thumbnail_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Asset info
        self.name_label = QLabel(self.asset.name)
        self.name_label.setWordWrap(True)
        self.name_label.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-size: 11px;
            }
        """)
        self.name_label.setMaximumHeight(30)
        layout.addWidget(self.name_label)

        # Type and size info
        size_text = self.format_file_size(self.asset.file_size or 0)
        category = getattr(self.asset, 'folder', '') or 'General'
        info_text = f"{self.asset.file_type.upper()} • {category} • {size_text}"
        self.info_label = QLabel(info_text)
        self.info_label.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                font-size: 9px;
            }
        """)
        layout.addWidget(self.info_label)

        # Description preview (if exists)
        description = getattr(self.asset, 'description', '')
        if description:
            desc_preview = description[:40] + "..." if len(description) > 40 else description
            self.desc_label = QLabel(desc_preview)
            self.desc_label.setWordWrap(True)
            self.desc_label.setStyleSheet("""
                QLabel {
                    color: #888888;
                    font-size: 8px;
                    font-style: italic;
                }
            """)
            self.desc_label.setMaximumHeight(25)
            layout.addWidget(self.desc_label)

    def format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"

        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024.0:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024.0
        return f"{size_bytes:.1f} TB"

    def generate_thumbnail(self):
        """Generate thumbnail for this asset"""
        if self.thumbnail_worker:
            self.thumbnail_worker.quit()
            self.thumbnail_worker.wait()

        self.thumbnail_worker = ThumbnailWorker(
            self.asset.id,
            self.asset.file_path,
            self.asset.file_type
        )
        self.thumbnail_worker.thumbnail_ready.connect(self.on_thumbnail_ready)
        self.thumbnail_worker.start()

    @pyqtSlot(str, QPixmap)
    def on_thumbnail_ready(self, asset_id: str, thumbnail: QPixmap):
        """Handle thumbnail ready"""
        if asset_id == self.asset.id:
            self.thumbnail_label.setPixmap(thumbnail)

    def mousePressEvent(self, event):
        """Handle mouse press with drag initiation"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.asset.id)
            self.drag_start_position = event.position()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        """Handle mouse move for drag operations"""
        if not (event.buttons() & Qt.MouseButton.LeftButton):
            return

        if not hasattr(self, 'drag_start_position'):
            return

        # Check if we've moved far enough to start a drag
        if ((event.position() - self.drag_start_position).manhattanLength() <
            QApplication.startDragDistance()):
            return

        # Start drag operation
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setText(self.asset.id)  # Pass asset ID
        drag.setMimeData(mime_data)

        # Create drag pixmap (thumbnail of the asset)
        pixmap = self.thumbnail_label.pixmap()
        if pixmap:
            # Scale down for drag
            scaled_pixmap = pixmap.scaled(64, 64, Qt.AspectRatioMode.KeepAspectRatio,
                                        Qt.TransformationMode.SmoothTransformation)
            drag.setPixmap(scaled_pixmap)
            drag.setHotSpot(scaled_pixmap.rect().center())

        # Execute drag
        drop_action = drag.exec(Qt.DropAction.CopyAction)

    def mouseDoubleClickEvent(self, event):
        """Handle double click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.asset.id)
        super().mouseDoubleClickEvent(event)

    def show_context_menu(self, position):
        """Show context menu for asset actions"""
        context_menu = QMenu(self)

        # Edit action
        edit_action = QAction("Edit Description && Category", self)
        edit_action.triggered.connect(lambda: self.edit_requested.emit(self.asset.id))
        context_menu.addAction(edit_action)

        context_menu.addSeparator()

        # Delete action
        delete_action = QAction("Delete Asset", self)
        delete_action.triggered.connect(lambda: self.delete_requested.emit(self.asset.id))
        context_menu.addAction(delete_action)

        # Show menu at cursor position
        context_menu.exec(self.mapToGlobal(position))


class EnhancedAssetPanel(QWidget):
    """Enhanced asset panel with thumbnails and previews"""

    asset_selected = pyqtSignal(str)  # asset_id
    asset_imported = pyqtSignal(str)  # asset_id
    asset_double_clicked = pyqtSignal(str)  # asset_id
    assets_changed = pyqtSignal()  # When assets are modified/deleted

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.asset_widgets = {}
        self.current_category_filter = "All"

        self.setup_ui()

    def setup_ui(self):
        """Setup the enhanced asset panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Header
        header_layout = QHBoxLayout()

        title = QLabel("Project Assets")
        title.setStyleSheet("""
            QLabel {
                color: #ffffff;
                font-weight: bold;
                font-size: 16px;
                padding: 5px;
            }
        """)
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Import button
        import_btn = QPushButton("Import")
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QPushButton:pressed {
                background-color: #004578;
            }
        """)
        import_btn.clicked.connect(self.import_assets)
        header_layout.addWidget(import_btn)

        layout.addLayout(header_layout)

        # Category filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Category:"))

        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All", "General", "Intro", "Demo", "Tutorial",
            "Outro", "Background", "UI/Interface", "Audio Sample"
        ])
        self.category_filter.currentTextChanged.connect(self._on_category_filter_changed)
        filter_layout.addWidget(self.category_filter)

        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Scroll area for assets
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setStyleSheet("""
            QScrollArea {
                background-color: #2d2d2d;
                border: 1px solid #555555;
                border-radius: 4px;
            }
        """)

        # Container for asset thumbnails
        self.assets_container = QWidget()
        self.assets_layout = QGridLayout(self.assets_container)
        self.assets_layout.setSpacing(10)
        self.assets_layout.setContentsMargins(10, 10, 10, 10)

        scroll.setWidget(self.assets_container)
        layout.addWidget(scroll)

        # Enable drag and drop
        self.setAcceptDrops(True)

    def set_project(self, project):
        """Set current project"""
        self.current_project = project
        self.refresh_assets()

    def refresh_assets(self):
        """Refresh asset display with categorization"""
        # Clear existing widgets
        for widget in self.asset_widgets.values():
            widget.setParent(None)
        self.asset_widgets.clear()

        # Clear the layout
        while self.assets_layout.count():
            child = self.assets_layout.takeAt(0)
            if child.widget():
                child.widget().setParent(None)

        if not self.current_project:
            return

        # Get filtered assets
        all_assets = self.current_project.get_all_assets()
        if self.current_category_filter == "All":
            assets = all_assets
        else:
            assets = [a for a in all_assets
                     if getattr(a, 'folder', 'General') == self.current_category_filter]

        # Group assets by type
        asset_groups = {
            'xplainpack': [],
            'image': [],
            'video': [],
            'audio': [],
            'other': []
        }

        for asset in assets:
            asset_groups[asset.file_type].append(asset)
            
        # Add XplainPack sessions as special assets
        if self.current_project:
            xplainpack_sessions = self.current_project.get_all_xplainpack_sessions()
            for session in xplainpack_sessions:
                # Create a pseudo-asset for XplainPack display
                class XplainPackAsset:
                    def __init__(self, session_data):
                        self.id = f"xplainpack_{session_data.get('id', 'unknown')}"
                        self.name = session_data.get('name', 'Unknown Session')
                        self.file_type = 'xplainpack'
                        self.description = session_data.get('description', '')
                        self.session_data = session_data
                        self.file_size = 0  # XplainPack sessions don't have a single file size
                        self.folder = 'XplainPack Sessions'  # Add folder for consistency
                        self.file_path = session_data.get('folder_path', '')  # Add file_path
                        
                asset_groups['xplainpack'].append(XplainPackAsset(session))

        # Create category sections
        row = 0
        category_styles = {
            'xplainpack': {'color': '#FF6B35', 'name': 'XplainPack Sessions'},
            'image': {'color': '#4CAF50', 'name': 'Images'},
            'video': {'color': '#f44336', 'name': 'Videos'},
            'audio': {'color': '#2196F3', 'name': 'Audio'},
            'other': {'color': '#9E9E9E', 'name': 'Other'}
        }

        for category, assets_in_category in asset_groups.items():
            if not assets_in_category:
                continue

            style = category_styles[category]

            # Category header
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 10, 0, 5)

            header_label = QLabel(f"{style['name']} ({len(assets_in_category)})")
            header_label.setStyleSheet(f"""
                QLabel {{
                    color: {style['color']};
                    font-weight: bold;
                    font-size: 14px;
                    padding: 5px 0px;
                }}
            """)
            header_layout.addWidget(header_label)
            header_layout.addStretch()

            self.assets_layout.addWidget(header_widget, row, 0, 1, 2)
            row += 1

            # Assets in this category
            col = 0
            for asset in assets_in_category:
                if col >= 2:  # Two columns max
                    col = 0
                    row += 1

                asset_widget = AssetThumbnailWidget(asset)
                asset_widget.clicked.connect(self.asset_selected.emit)
                asset_widget.double_clicked.connect(self._handle_asset_double_click)
                asset_widget.edit_requested.connect(self._edit_asset)
                asset_widget.delete_requested.connect(self._delete_asset)

                self.assets_layout.addWidget(asset_widget, row, col)
                self.asset_widgets[asset.id] = asset_widget

                col += 1

            # Move to next row for next category
            if col > 0:
                row += 1

        # Add stretch to push everything to top
        self.assets_layout.setRowStretch(row + 1, 1)

    def _handle_asset_double_click(self, asset_id: str):
        """Handle double-click on an asset"""
        if not self.current_project:
            return
        
        # Check if this is a XplainPack session
        if asset_id.startswith("xplainpack_"):
            session_id = asset_id.replace("xplainpack_", "")
            session_data = self.current_project.get_xplainpack_session(session_id)
            
            if session_data:
                # Open XplainPack session editor
                dialog = XplainPackSessionDialog(session_data, self)
                if dialog.exec() == QDialog.DialogCode.Accepted:
                    # Update session data
                    updated_data = dialog.get_updated_data()
                    # Update in project (we need to implement this method)
                    self.current_project.update_xplainpack_session(session_id, updated_data)
                    # Refresh display
                    self.refresh_assets()
        else:
            # Regular asset double-click - emit signal for other handlers
            self.asset_double_clicked.emit(asset_id)

    def import_assets(self):
        """Import assets dialog with XplainPack support"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please create or open a project first.")
            return

        # Create dialog with options for regular assets vs XplainPacks
        from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel
        
        dialog = QDialog(self)
        dialog.setWindowTitle("Import Assets")
        dialog.setModal(True)
        dialog.resize(400, 200)
        
        layout = QVBoxLayout(dialog)
        
        # Title
        title = QLabel("Choose Import Type:")
        title.setStyleSheet("font-size: 14px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Regular assets button
        assets_btn = QPushButton("Import Media Files")
        assets_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078d4;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #106ebe;
            }
        """)
        assets_btn.clicked.connect(lambda: self._import_regular_assets(dialog))
        layout.addWidget(assets_btn)
        
        # XplainPack button
        xplainpack_btn = QPushButton("Import XplainPack Session")
        xplainpack_btn.setStyleSheet("""
            QPushButton {
                background-color: #107c10;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 4px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0e6e0e;
            }
        """)
        xplainpack_btn.clicked.connect(lambda: self._import_xplainpack(dialog))
        layout.addWidget(xplainpack_btn)
        
        # Info text
        info_text = QLabel("💡 XplainPacks are specialized folders containing synchronized video + audio for AI content generation")
        info_text.setStyleSheet("color: #969696; font-size: 10px; margin: 10px; text-align: center;")
        info_text.setWordWrap(True)
        layout.addWidget(info_text)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(dialog.reject)
        layout.addWidget(cancel_btn)
        
        dialog.exec()

    def _import_regular_assets(self, dialog):
        """Import regular media assets"""
        dialog.accept()
        
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Assets",
            str(Path.home()),
            "Media Files (*.mp4 *.mov *.avi *.mkv *.mp3 *.wav *.aac *.jpg *.jpeg *.png *.gif);;All Files (*)"
        )

        for file_path in file_paths:
            self.import_single_asset(Path(file_path))

    def _import_xplainpack(self, dialog):
        """Import XplainPack session"""
        dialog.accept()
        
        pack_path = QFileDialog.getExistingDirectory(
            self,
            "Select XplainPack Folder",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly
        )
        
        if pack_path:
            self.import_xplainpack_session(Path(pack_path))

    def import_xplainpack_session(self, pack_path: Path):
        """Import an XplainPack session"""
        if not self.current_project:
            return
            
        try:
            session_id = self.current_project.import_xplainpack(pack_path)
            if session_id:
                log_info(f"Imported XplainPack session: {pack_path.name} (ID: {session_id})")
                
                # Show success message with session details
                session_data = self.current_project.get_xplainpack_session(session_id)
                if session_data:
                    QMessageBox.information(
                        self,
                        "XplainPack Imported Successfully!",
                        f"Session: {session_data.get('name', 'Unknown')}\n"
                        f"ID: {session_id}\n"
                        f"Description: {session_data.get('description', 'No description')}\n"
                        f"Files: Video, Audio, Metadata\n\n"
                        f"This session can now be linked to content events for synchronized AI generation."
                    )
                
                # Refresh display - XplainPacks will appear as special asset type
                self.refresh_assets()
                
            else:
                QMessageBox.warning(
                    self,
                    "Import Failed",
                    f"Failed to import XplainPack from:\n{pack_path}\n\n"
                    f"Please ensure the folder contains:\n"
                    f"• A video file (.mov preferred)\n"
                    f"• An audio file (.mp3/.wav)\n"
                    f"• Optional: metadata.json with transcript/transients"
                )
                
        except Exception as e:
            log_error(f"Error importing XplainPack {pack_path}: {e}")
            QMessageBox.critical(
                self,
                "Import Error", 
                f"Error importing XplainPack:\n{str(e)}"
            )

    def import_single_asset(self, file_path: Path):
        """Import a single asset"""
        if not self.current_project:
            return

        try:
            # Import asset to project
            asset_id = self.current_project.import_asset(str(file_path))
            if asset_id:
                log_info(f"Imported asset: {file_path.name} (ID: {asset_id})")
                # Refresh the display
                self.refresh_assets()
                # Emit signal
                self.asset_imported.emit(asset_id)
            else:
                log_warning(f"Failed to import: {file_path.name}")
        except Exception as e:
            log_error(f"Error importing {file_path}: {e}")

    def dragEnterEvent(self, event):
        """Handle drag enter"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        """Handle drop event with XplainPack support"""
        if not self.current_project:
            return

        for url in event.mimeData().urls():
            file_path = Path(url.toLocalFile())
            
            if file_path.is_file():
                # Regular file import
                self.import_single_asset(file_path)
            elif file_path.is_dir():
                # Check if it might be an XplainPack
                from core.assets import AssetManager
                asset_manager = AssetManager(self.current_project.project_directory)
                pack_info = asset_manager._validate_xplainpack(file_path)
                
                if pack_info.is_valid:
                    # Import as XplainPack
                    self.import_xplainpack_session(file_path)
                else:
                    # Scan directory for media files
                    media_files = []
                    for ext in ['.mp4', '.mov', '.avi', '.mp3', '.wav', '.jpg', '.png']:
                        media_files.extend(file_path.glob(f'*{ext}'))
                        media_files.extend(file_path.glob(f'*{ext.upper()}'))
                    
                    if media_files:
                        for media_file in media_files:
                            self.import_single_asset(media_file)
                    else:
                        log_warning(f"No supported media files found in: {file_path}")

    def _on_category_filter_changed(self, category):
        """Handle category filter change"""
        self.current_category_filter = category
        self.refresh_assets()

    def _edit_asset(self, asset_id: str):
        """Edit asset description and category"""
        if not self.current_project or asset_id not in self.current_project.assets:
            return

        asset = self.current_project.assets[asset_id]
        dialog = AssetDescriptionDialog(asset, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update asset
            new_category = dialog.get_category()
            new_description = dialog.get_description()

            self.current_project.update_asset_folder(asset_id, new_category)
            self.current_project.update_asset_description(asset_id, new_description)

            # Refresh display
            self.refresh_assets()
            self.assets_changed.emit()

    def _delete_asset(self, asset_id: str):
        """Delete asset after confirmation"""
        if not self.current_project:
            return

        # Check if this is an XplainPack session
        if asset_id.startswith("xplainpack_"):
            xplainpack_session_id = asset_id.replace("xplainpack_", "")
            self._delete_xplainpack_session(xplainpack_session_id)
            return

        # Regular asset deletion
        if asset_id not in self.current_project.assets:
            return

        asset = self.current_project.assets[asset_id]

        reply = QMessageBox.question(
            self,
            "Delete Asset",
            f"Are you sure you want to delete '{asset.name}'?\n\nThis will remove the asset from all events and delete the file.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.current_project.delete_asset(asset_id):
                self.refresh_assets()
                self.assets_changed.emit()
                QMessageBox.information(self, "Deleted", f"Asset '{asset.name}' has been deleted.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete asset.")

    def _delete_xplainpack_session(self, session_id: str):
        """Delete XplainPack session after confirmation"""
        if not self.current_project or not self.current_project.xplainpack_manager:
            return

        session = self.current_project.xplainpack_manager.get_session(session_id)
        if not session:
            return

        reply = QMessageBox.question(
            self,
            "Delete XplainPack Session",
            f"Are you sure you want to delete XplainPack session '{session.name}'?\n\nThis will remove the session from the project but will not delete the original files.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.current_project.remove_xplainpack_session(session_id):
                self.refresh_assets()
                self.assets_changed.emit()
                QMessageBox.information(self, "Deleted", f"XplainPack session '{session.name}' has been removed from the project.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete XplainPack session.")


class AssetDescriptionDialog(QDialog):
    """Dialog for editing asset description and category"""

    def __init__(self, asset, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.setWindowTitle(f"Edit Asset: {asset.name}")
        self.setModal(True)
        self.resize(400, 250)

        self._setup_ui()
        self._load_data()

    def _setup_ui(self):
        layout = QVBoxLayout(self)

        # Form layout
        form_layout = QFormLayout()

        # Asset name (read-only)
        name_label = QLabel(self.asset.name)
        name_label.setStyleSheet("font-weight: bold; color: #007acc;")
        form_layout.addRow("Asset Name:", name_label)

        # Content category
        self.category_combo = QComboBox()
        self.category_combo.addItems([
            "General",
            "Intro",
            "Demo",
            "Tutorial",
            "Outro",
            "Background",
            "UI/Interface",
            "Audio Sample"
        ])
        form_layout.addRow("Category:", self.category_combo)

        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Add description to help AI understand this asset's purpose and content...")
        form_layout.addRow("Description:", self.description_edit)

        layout.addLayout(form_layout)

        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _load_data(self):
        """Load current asset data"""
        # Set category if it exists in description or folder
        current_category = getattr(self.asset, 'folder', '') or 'General'
        index = self.category_combo.findText(current_category)
        if index >= 0:
            self.category_combo.setCurrentIndex(index)

        # Set description
        description = getattr(self.asset, 'description', '')
        self.description_edit.setPlainText(description)

    def get_category(self) -> str:
        """Get selected category"""
        return self.category_combo.currentText()

    def get_description(self) -> str:
        """Get description text"""
        return self.description_edit.toPlainText().strip()
