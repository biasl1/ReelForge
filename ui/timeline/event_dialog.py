"""
Event Scheduling Dialog
Dialog for creating and editing release events with VIDEO/PICTURE content types
"""

from datetime import datetime
from typing import List, Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel,
    QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QListWidget, QListWidgetItem, QGroupBox, QCheckBox,
    QDateTimeEdit, QMessageBox, QFrame, QScrollArea, QWidget,
    QTabWidget, QSlider
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont

from core.project import ReleaseEvent


class EventDialog(QDialog):
    """Dialog for creating/editing VIDEO/PICTURE events with per-event template config"""

    event_created = pyqtSignal(ReleaseEvent)
    event_updated = pyqtSignal(ReleaseEvent)

    def __init__(self, date: datetime, event: Optional[ReleaseEvent] = None, project=None, parent=None):
        super().__init__(parent)
        self.target_date = date
        self.editing_event = event
        self.project = project
        self.setup_ui()
        self.setup_connections()
        if event:
            self.populate_from_event(event)
        else:
            self.validate_form()
        self.setWindowTitle("Schedule Content" if not event else "Edit Content")
        self.resize(520, 600)

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        header = self.create_header()
        layout.addWidget(header)
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        form_widget = QWidget()
        scroll.setWidget(form_widget)
        form_layout = QVBoxLayout(form_widget)
        form_layout.setSpacing(10)

        # Basic info
        basic_group = self.create_basic_info_group()
        form_layout.addWidget(basic_group)

        # Description/prompt
        desc_group = self.create_description_group()
        form_layout.addWidget(desc_group)

        # Per-event template config
        template_group = self.create_template_group()
        form_layout.addWidget(template_group)

        form_layout.addStretch()
        layout.addWidget(scroll)

        # Buttons
        buttons = self.create_buttons()
        layout.addWidget(buttons)

    def create_header(self) -> QWidget:
        header = QFrame()
        header.setStyleSheet("background-color: #2d2d30; border-radius: 5px; padding: 10px;")
        layout = QVBoxLayout(header)
        title = QLabel("Schedule Content Event")
        title.setStyleSheet("color: #cccccc; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        date_label = QLabel(f"Date: {self.target_date.strftime('%A, %B %d, %Y')}")
        date_label.setStyleSheet("color: #969696; font-size: 12px;")
        layout.addWidget(date_label)
        return header

    def create_basic_info_group(self) -> QGroupBox:
        group = QGroupBox("Event Info")
        layout = QFormLayout(group)

        # Content type: VIDEO or PICTURE
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems(["VIDEO", "PICTURE"])
        layout.addRow("Type:", self.content_type_combo)

        # Title
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter event title...")
        layout.addRow("Title:", self.title_edit)

        return group

    def create_description_group(self) -> QGroupBox:
        group = QGroupBox("Description / Prompt")
        layout = QVBoxLayout(group)

        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Describe this event or leave blank for AI generation...")
        layout.addWidget(self.description_edit)

        return group

    def create_template_group(self) -> QGroupBox:
        group = QGroupBox("📋 Template Configuration")
        layout = QVBoxLayout(group)

        # Clear info about where templates are actually configured
        info_widget = QWidget()
        info_layout = QVBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel("🎨 Template Editor Settings")
        title_label.setStyleSheet("font-weight: bold; color: #2196F3; margin-bottom: 5px;")
        info_layout.addWidget(title_label)
        
        info_text = QLabel(
            "• Frame count: Set in Template Editor only\n"
            "• Element positions: Configured per frame in Template Editor\n" 
            "• Text/PiP properties: Managed per frame independently"
        )
        info_text.setStyleSheet("color: #666; font-size: 11px; margin-left: 15px;")
        info_layout.addWidget(info_text)
        
        layout.addWidget(info_widget)
        
        # Simplified template import/export area (for advanced users)
        advanced_label = QLabel("🔧 Advanced: Import/Export Template JSON")
        advanced_label.setStyleSheet("font-weight: bold; color: #FF9800; margin-top: 10px; margin-bottom: 5px;")
        layout.addWidget(advanced_label)
        
        self.template_edit = QTextEdit()
        self.template_edit.setPlaceholderText("Advanced users: Paste template JSON here to import existing configurations...")
        self.template_edit.setMaximumHeight(60)
        self.template_edit.setStyleSheet("font-family: monospace; font-size: 10px; color: #666;")
        layout.addWidget(self.template_edit)

        return group

    def create_buttons(self) -> QWidget:
        button_widget = QFrame()
        layout = QHBoxLayout(button_widget)

        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)

        layout.addStretch()

        self.save_btn = QPushButton("Create Event" if not self.editing_event else "Update Event")
        self.save_btn.setDefault(True)
        self.save_btn.clicked.connect(self.save_event)
        layout.addWidget(self.save_btn)

        return button_widget

    def setup_connections(self):
        self.title_edit.textChanged.connect(self.validate_form)
        self.content_type_combo.currentTextChanged.connect(self.on_content_type_changed)
        # ✅ FRAME COUNT REMOVED - no more connections needed!

    def on_content_type_changed(self):
        # ✅ FRAME COUNT REMOVED - content type change only validates form now
        self.validate_form()

    def validate_form(self):
        title = self.title_edit.text().strip()
        content_type = self.content_type_combo.currentText()
        is_valid = bool(title and content_type)
        self.save_btn.setEnabled(is_valid)

    def populate_from_event(self, event: ReleaseEvent):
        self.title_edit.setText(event.title)
        self.description_edit.setPlainText(event.description)

        # Set type
        idx = self.content_type_combo.findText(event.content_type.upper())
        if idx >= 0:
            self.content_type_combo.setCurrentIndex(idx)

        # ✅ FRAME COUNT REMOVED - no longer set in calendar dialog!
        # (Frame count is only set in the Template Editor now)

        # Template config
        if hasattr(event, 'template_config') and event.template_config:
            import json
            try:
                self.template_edit.setPlainText(json.dumps(event.template_config, indent=2))
            except Exception:
                self.template_edit.setPlainText(str(event.template_config))

        self.on_content_type_changed()

    def save_event(self):
        try:
            import json
            title = self.title_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            content_type = self.content_type_combo.currentText().lower()
            
            # 🔥 FRAME COUNT NO LONGER SET HERE - Only in Template Editor!
            # Use default frame counts: 1 for pictures, 3 for videos (can be changed in template editor)
            frame_count = 1 if content_type == "picture" else 3

            # Parse template config
            template_config = {}
            txt = self.template_edit.toPlainText().strip()
            if txt:
                try:
                    template_config = json.loads(txt)
                except Exception:
                    template_config = {"raw": txt}

            # Create or update event
            if self.editing_event:
                event = self.editing_event
                event.title = title
                event.description = description
                event.content_type = content_type
                event.frame_count = frame_count
                event.template_config = template_config
                self.event_updated.emit(event)
            else:
                from core.project import ReleaseEvent
                import uuid
                event = ReleaseEvent(
                    id=str(uuid.uuid4()),
                    date=self.target_date.date().isoformat(),
                    title=title,
                    description=description,
                    content_type=content_type,
                    status="planned",
                    duration_seconds=30 if content_type == "video" else 5,
                    assets=[],
                    platforms=[],
                    hashtags=[],
                    session_id=None,
                    frame_count=frame_count,
                    template_config=template_config
                )
                self.event_created.emit(event)

            self.accept()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save event:\n{str(e)}")
