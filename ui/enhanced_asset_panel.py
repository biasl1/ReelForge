"""
Enhanced Asset Panel with thumbnails and previews
Professional-looking asset management with visual previews
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGridLayout, QMessageBox, QFileDialog,
    QApplication, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QThread, pyqtSlot
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QFont, QIcon, QPen
from pathlib import Path
from typing import Optional
import subprocess
from core.logging_config import log_info, log_error, log_warning, log_debug
import tempfile
import os


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
            else:
                thumbnail = self.create_icon_thumbnail()
                
            if thumbnail and not thumbnail.isNull():
                self.thumbnail_ready.emit(self.asset_id, thumbnail)
        except Exception as e:
            log_error(f"Error generating thumbnail for {self.asset_id}: {e}")
            
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
        info_text = f"{self.asset.file_type.upper()} • {size_text}"
        self.info_label = QLabel(info_text)
        self.info_label.setStyleSheet("""
            QLabel {
                color: #b0b0b0;
                font-size: 9px;
            }
        """)
        layout.addWidget(self.info_label)
        
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
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.asset.id)
        super().mousePressEvent(event)
        
    def mouseDoubleClickEvent(self, event):
        """Handle double click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.asset.id)
        super().mouseDoubleClickEvent(event)


class EnhancedAssetPanel(QWidget):
    """Enhanced asset panel with thumbnails and previews"""
    
    asset_selected = pyqtSignal(str)  # asset_id
    asset_imported = pyqtSignal(str)  # asset_id
    asset_double_clicked = pyqtSignal(str)  # asset_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.asset_widgets = {}
        
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
            
        # Group assets by type
        assets = self.current_project.get_all_assets()
        asset_groups = {
            'image': [],
            'video': [],
            'audio': [],
            'other': []
        }
        
        for asset in assets:
            asset_groups[asset.file_type].append(asset)
        
        # Create category sections
        row = 0
        category_styles = {
            'image': {'color': '#4CAF50', 'icon': '🖼️', 'name': 'Images'},
            'video': {'color': '#f44336', 'icon': '🎬', 'name': 'Videos'},
            'audio': {'color': '#2196F3', 'icon': '🎵', 'name': 'Audio'},
            'other': {'color': '#9E9E9E', 'icon': '📄', 'name': 'Other'}
        }
        
        for category, assets_in_category in asset_groups.items():
            if not assets_in_category:
                continue
                
            style = category_styles[category]
            
            # Category header
            header_widget = QWidget()
            header_layout = QHBoxLayout(header_widget)
            header_layout.setContentsMargins(0, 10, 0, 5)
            
            header_label = QLabel(f"{style['icon']} {style['name']} ({len(assets_in_category)})")
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
                asset_widget.double_clicked.connect(self.asset_double_clicked.emit)
                
                self.assets_layout.addWidget(asset_widget, row, col)
                self.asset_widgets[asset.id] = asset_widget
                
                col += 1
                
            # Move to next row for next category
            if col > 0:
                row += 1
        
        # Add stretch to push everything to top
        self.assets_layout.setRowStretch(row + 1, 1)
        
    def import_assets(self):
        """Import assets dialog"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please create or open a project first.")
            return
            
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Assets",
            str(Path.home()),
            "Media Files (*.mp4 *.mov *.avi *.mkv *.mp3 *.wav *.aac *.jpg *.jpeg *.png *.gif);;All Files (*)"
        )
        
        for file_path in file_paths:
            self.import_single_asset(Path(file_path))
            
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
        """Handle drop event"""
        if not self.current_project:
            return
            
        for url in event.mimeData().urls():
            file_path = Path(url.toLocalFile())
            if file_path.is_file():
                self.import_single_asset(file_path)
