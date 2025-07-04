"""
UX Improvements for ReelTune
Practical enhancements for better content creation workflow
"""

from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QLabel, QPushButton, QFrame,
    QToolButton, QMenu, QStyle, QSizePolicy, QApplication,
    QVBoxLayout, QStatusBar
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QPixmap, QPainter, QColor, QFont, QKeySequence, QAction, QShortcut
from core.logging_config import log_info, log_debug


class AutoSaveIndicator(QWidget):
    """Visual indicator for auto-save status"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_saving = False
        self.has_unsaved_changes = False
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # Status icon
        self.status_icon = QLabel()
        self.status_icon.setFixedSize(16, 16)
        layout.addWidget(self.status_icon)

        # Status text
        self.status_text = QLabel("Saved")
        self.status_text.setStyleSheet("color: #4CAF50; font-size: 11px;")
        layout.addWidget(self.status_text)

        self.update_status()

    def update_status(self):
        """Update the save status display"""
        if self.is_saving:
            self.status_text.setText("Saving...")
            self.status_text.setStyleSheet("color: #FF9800; font-size: 11px;")
            self._create_icon("#FF9800")  # Orange
        elif self.has_unsaved_changes:
            self.status_text.setText("Unsaved changes")
            self.status_text.setStyleSheet("color: #F44336; font-size: 11px;")
            self._create_icon("#F44336")  # Red
        else:
            self.status_text.setText("Saved")
            self.status_text.setStyleSheet("color: #4CAF50; font-size: 11px;")
            self._create_icon("#4CAF50")  # Green

    def _create_icon(self, color):
        """Create a colored circle icon"""
        pixmap = QPixmap(16, 16)
        pixmap.fill(Qt.GlobalColor.transparent)

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QColor(color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(3, 3, 10, 10)
        painter.end()

        self.status_icon.setPixmap(pixmap)

    def set_saving(self):
        """Indicate saving in progress"""
        self.is_saving = True
        self.has_unsaved_changes = False
        self.update_status()

    def set_saved(self):
        """Indicate save completed"""
        self.is_saving = False
        self.has_unsaved_changes = False
        self.update_status()

    def set_unsaved_changes(self):
        """Indicate unsaved changes"""
        self.is_saving = False
        self.has_unsaved_changes = True
        self.update_status()


class QuickActionToolbar(QWidget):
    """Quick action toolbar for common tasks"""

    # Signals for quick actions
    action_triggered = pyqtSignal(str)  # action_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Quick event creation buttons
        quick_label = QLabel("Quick Create:")
        quick_label.setStyleSheet("color: #999; font-size: 11px; font-weight: bold;")
        layout.addWidget(quick_label)

        # Content type quick buttons
        content_types = [
            ("📸", "post", "Instagram Post"),
            ("🎬", "reel", "Instagram Reel"),
            ("📱", "story", "Story"),
            ("🎵", "teaser", "Audio Teaser"),
            ("🎓", "tutorial", "Tutorial")
        ]

        for emoji, content_type, tooltip in content_types:
            btn = QPushButton(f"{emoji}")
            btn.setToolTip(f"Create {tooltip}")
            btn.setFixedSize(32, 28)
            btn.setStyleSheet("""
                QPushButton {
                    border: 1px solid #444;
                    border-radius: 4px;
                    background: #2B2B2B;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background: #3B3B3B;
                    border-color: #555;
                }
                QPushButton:pressed {
                    background: #1B1B1B;
                }
            """)
            btn.clicked.connect(lambda checked, ct=content_type: self.action_triggered.emit(f"create_{ct}"))
            layout.addWidget(btn)

        layout.addWidget(self._create_separator())

        # Duplicate button
        duplicate_btn = QPushButton("📋")
        duplicate_btn.setToolTip("Duplicate Selected Event")
        duplicate_btn.setFixedSize(32, 28)
        duplicate_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #444;
                border-radius: 4px;
                background: #2B2B2B;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #3B3B3B;
                border-color: #555;
            }
        """)
        duplicate_btn.clicked.connect(lambda: self.action_triggered.emit("duplicate_event"))
        layout.addWidget(duplicate_btn)

        layout.addWidget(self._create_separator())

        # View toggle button
        view_btn = QPushButton("📅")
        view_btn.setToolTip("Toggle Week/Month View")
        view_btn.setFixedSize(32, 28)
        view_btn.setStyleSheet("""
            QPushButton {
                border: 1px solid #444;
                border-radius: 4px;
                background: #2B2B2B;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #3B3B3B;
                border-color: #555;
            }
        """)
        view_btn.clicked.connect(lambda: self.action_triggered.emit("toggle_view"))
        layout.addWidget(view_btn)

        # Spacer
        layout.addStretch()

    def _create_separator(self):
        """Create a vertical separator line"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #444;")
        return separator


class ContentTypeTemplates:
    """Pre-defined templates for different content types"""

    TEMPLATES = {
        "post": {
            "title": "New Product Showcase",
            "description": "Show off the key features and benefits of [PLUGIN_NAME]. Focus on the unique sound and professional quality.",
            "duration_seconds": 0,  # Static post
            "platforms": ["instagram"],
            "hashtags": ["#plugin", "#music", "#producer", "#sound"]
        },
        "reel": {
            "title": "[PLUGIN_NAME] in Action",
            "description": "Quick demo showing [PLUGIN_NAME] transforming audio. Before/after comparison with engaging visuals.",
            "duration_seconds": 30,
            "platforms": ["instagram", "tiktok"],
            "hashtags": ["#reel", "#musicproducer", "#plugin", "#beforeafter"]
        },
        "story": {
            "title": "Behind the Scenes",
            "description": "Story series about the development process of [PLUGIN_NAME]. Show the team, inspiration, and creative process.",
            "duration_seconds": 15,
            "platforms": ["instagram"],
            "hashtags": ["#story", "#behindthescenes", "#musictech"]
        },
        "teaser": {
            "title": "[PLUGIN_NAME] Teaser",
            "description": "Short audio teaser showcasing the signature sound of [PLUGIN_NAME]. Pure audio focus with minimal visuals.",
            "duration_seconds": 20,
            "platforms": ["instagram", "tiktok", "youtube"],
            "hashtags": ["#teaser", "#audio", "#plugin", "#sound"]
        },
        "tutorial": {
            "title": "How to Use [PLUGIN_NAME]",
            "description": "Step-by-step tutorial showing how to get the best results with [PLUGIN_NAME]. Include tips and tricks.",
            "duration_seconds": 60,
            "platforms": ["youtube", "instagram"],
            "hashtags": ["#tutorial", "#howto", "#musicproduction", "#tips"]
        }
    }

    @classmethod
    def get_template(cls, content_type: str, plugin_name: str = None) -> dict:
        """Get template with plugin name substitution"""
        template = cls.TEMPLATES.get(content_type, {}).copy()

        if plugin_name and template:
            # Replace [PLUGIN_NAME] placeholder
            template["title"] = template["title"].replace("[PLUGIN_NAME]", plugin_name)
            template["description"] = template["description"].replace("[PLUGIN_NAME]", plugin_name)

        return template


class ProjectProgressIndicator(QWidget):
    """Shows project completion progress"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.total_events = 0
        self.completed_events = 0
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 2, 5, 2)

        # Progress label
        self.progress_label = QLabel("Project Progress:")
        self.progress_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(self.progress_label)

        # Progress bar (text-based for simplicity)
        self.progress_text = QLabel("0/0 events")
        self.progress_text.setStyleSheet("color: #FFF; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.progress_text)

        # Completion percentage
        self.percentage_label = QLabel("0%")
        self.percentage_label.setStyleSheet("color: #4CAF50; font-size: 11px; font-weight: bold;")
        layout.addWidget(self.percentage_label)

    def update_progress(self, total: int, completed: int):
        """Update progress display"""
        self.total_events = total
        self.completed_events = completed

        self.progress_text.setText(f"{completed}/{total} events")

        if total > 0:
            percentage = int((completed / total) * 100)
            self.percentage_label.setText(f"{percentage}%")

            # Color coding for progress
            if percentage < 30:
                color = "#F44336"  # Red
            elif percentage < 70:
                color = "#FF9800"  # Orange
            else:
                color = "#4CAF50"  # Green

            self.percentage_label.setStyleSheet(f"color: {color}; font-size: 11px; font-weight: bold;")
        else:
            self.percentage_label.setText("0%")
            self.percentage_label.setStyleSheet("color: #999; font-size: 11px; font-weight: bold;")


class KeyboardShortcutManager(QWidget):
    """Manages keyboard shortcuts for the application"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.shortcuts = {}
        self.parent_window = parent

    def add_shortcut(self, key_sequence: str, callback, description: str = ""):
        """Add a keyboard shortcut"""
        shortcut = QShortcut(QKeySequence(key_sequence), self.parent_window)
        shortcut.activated.connect(callback)

        self.shortcuts[key_sequence] = {
            'shortcut': shortcut,
            'callback': callback,
            'description': description
        }

        log_debug(f"Added keyboard shortcut: {key_sequence} - {description}")

    def remove_shortcut(self, key_sequence: str):
        """Remove a keyboard shortcut"""
        if key_sequence in self.shortcuts:
            shortcut_info = self.shortcuts[key_sequence]
            shortcut_info['shortcut'].deleteLater()
            del self.shortcuts[key_sequence]
            log_debug(f"Removed keyboard shortcut: {key_sequence}")

    def get_shortcuts_help(self) -> str:
        """Get help text for all shortcuts"""
        help_text = "Keyboard Shortcuts:\n\n"
        for key, info in self.shortcuts.items():
            help_text += f"{key}: {info['description']}\n"
        return help_text


class RecentAssetsWidget(QWidget):
    """Widget showing recently imported assets for quick access"""

    asset_selected = pyqtSignal(str)  # asset_id

    def __init__(self, parent=None):
        super().__init__(parent)
        self.recent_assets = []
        self.max_recent = 5
        self.setup_ui()

    def setup_ui(self):
        from PyQt6.QtWidgets import QVBoxLayout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)

        # Title
        title = QLabel("Recent Assets")
        title.setStyleSheet("color: #999; font-size: 11px; font-weight: bold; margin-bottom: 5px;")
        layout.addWidget(title)

        # Assets container
        self.assets_container = QWidget()
        self.assets_layout = QVBoxLayout(self.assets_container)
        self.assets_layout.setContentsMargins(0, 0, 0, 0)
        self.assets_layout.setSpacing(2)
        layout.addWidget(self.assets_container)

        # Initially show "No recent assets"
        self.update_display()

    def add_recent_asset(self, asset_id: str, asset_name: str, asset_type: str):
        """Add an asset to recent list"""
        # Remove if already exists
        self.recent_assets = [asset for asset in self.recent_assets if asset['id'] != asset_id]

        # Add to front
        self.recent_assets.insert(0, {
            'id': asset_id,
            'name': asset_name,
            'type': asset_type
        })

        # Limit size
        self.recent_assets = self.recent_assets[:self.max_recent]

        self.update_display()

    def update_display(self):
        """Update the display of recent assets"""
        # Clear existing widgets
        for i in reversed(range(self.assets_layout.count())):
            child = self.assets_layout.itemAt(i).widget()
            if child:
                child.deleteLater()

        if not self.recent_assets:
            # Show placeholder
            placeholder = QLabel("No recent assets")
            placeholder.setStyleSheet("color: #666; font-size: 10px; font-style: italic; padding: 10px;")
            placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.assets_layout.addWidget(placeholder)
        else:
            # Show recent assets
            for asset in self.recent_assets:
                asset_btn = self._create_asset_button(asset)
                self.assets_layout.addWidget(asset_btn)

    def _create_asset_button(self, asset: dict) -> QPushButton:
        """Create button for recent asset"""
        # Truncate long names
        display_name = asset['name']
        if len(display_name) > 20:
            display_name = display_name[:17] + "..."

        # Get emoji for asset type
        type_emoji = {
            'image': '🖼️',
            'video': '🎬',
            'audio': '🎵',
            'text': '📄'
        }.get(asset['type'], '📎')

        btn = QPushButton(f"{type_emoji} {display_name}")
        btn.setToolTip(f"{asset['name']} ({asset['type']})")
        btn.setStyleSheet("""
            QPushButton {
                text-align: left;
                padding: 4px 8px;
                border: 1px solid #444;
                border-radius: 3px;
                background: #2B2B2B;
                color: #FFF;
                font-size: 10px;
            }
            QPushButton:hover {
                background: #3B3B3B;
                border-color: #555;
            }
            QPushButton:pressed {
                background: #1B1B1B;
            }
        """)

        btn.clicked.connect(lambda: self.asset_selected.emit(asset['id']))
        return btn


class SmartStatusBar(QStatusBar):
    """Enhanced status bar with project info and progress"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        # Create a widget to hold our custom layout
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(10, 2, 10, 2)
        layout.setSpacing(15)

        # Project info section
        self.project_label = QLabel("No project loaded")
        self.project_label.setStyleSheet("color: #FFF; font-size: 11px;")
        layout.addWidget(self.project_label)

        # Separator
        sep1 = self._create_separator()
        layout.addWidget(sep1)

        # Asset count
        self.asset_count_label = QLabel("Assets: 0")
        self.asset_count_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(self.asset_count_label)

        # Separator
        sep2 = self._create_separator()
        layout.addWidget(sep2)

        # Events count
        self.events_count_label = QLabel("Events: 0")
        self.events_count_label.setStyleSheet("color: #999; font-size: 11px;")
        layout.addWidget(self.events_count_label)

        # Spacer
        layout.addStretch()

        # Status message area
        self.status_message = QLabel("Ready")
        self.status_message.setStyleSheet("color: #4CAF50; font-size: 11px;")
        layout.addWidget(self.status_message)

        # Add the widget to the status bar
        self.addWidget(widget, 1)

        # Message timer
        self.message_timer = QTimer()
        self.message_timer.timeout.connect(self._clear_message)

    def _create_separator(self):
        """Create a vertical separator"""
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.VLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet("color: #444;")
        separator.setFixedHeight(16)
        return separator

    def update_project_info(self, project_name: str, asset_count: int, event_count: int):
        """Update project information display"""
        self.project_label.setText(f"Project: {project_name}")
        self.asset_count_label.setText(f"Assets: {asset_count}")
        self.events_count_label.setText(f"Events: {event_count}")

    def show_message(self, message: str, duration: int = 2000):
        """Show a temporary status message"""
        self.status_message.setText(message)
        self.status_message.setStyleSheet("color: #4CAF50; font-size: 11px;")

        if duration > 0:
            self.message_timer.start(duration)

        # Also show in status bar
        self.showMessage(message, duration)

    def show_error(self, message: str, duration: int = 3000):
        """Show an error message"""
        self.status_message.setText(message)
        self.status_message.setStyleSheet("color: #F44336; font-size: 11px;")

        if duration > 0:
            self.message_timer.start(duration)

        # Also show in status bar
        self.showMessage(message, duration)

    def show_warning(self, message: str, duration: int = 2500):
        """Show a warning message"""
        self.status_message.setText(message)
        self.status_message.setStyleSheet("color: #FF9800; font-size: 11px;")

        if duration > 0:
            self.message_timer.start(duration)

        # Also show in status bar
        self.showMessage(message, duration)

    def _clear_message(self):
        """Clear the status message"""
        self.message_timer.stop()
        self.status_message.setText("Ready")
        self.status_message.setStyleSheet("color: #4CAF50; font-size: 11px;")
        self.clearMessage()

    def addPermanentWidget(self, widget):
        """Add a permanent widget to the status bar"""
        super().addPermanentWidget(widget)
