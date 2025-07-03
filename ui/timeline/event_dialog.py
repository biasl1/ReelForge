"""
Event Scheduling Dialog
Dialog for creating and editing release events
"""

from datetime import datetime
from typing import List, Optional
from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QLabel, 
    QPushButton, QLineEdit, QTextEdit, QComboBox, QSpinBox,
    QListWidget, QListWidgetItem, QGroupBox, QCheckBox,
    QDateTimeEdit, QMessageBox, QFrame, QScrollArea, QWidget
)
from PyQt6.QtCore import Qt, QDateTime, pyqtSignal
from PyQt6.QtGui import QFont

from core.project import ReleaseEvent


class EventDialog(QDialog):
    """Dialog for creating/editing release events"""
    
    event_created = pyqtSignal(ReleaseEvent)
    event_updated = pyqtSignal(ReleaseEvent)
    
    def __init__(self, date: datetime, event: Optional[ReleaseEvent] = None, 
                 available_assets: List[tuple] = None, parent=None):
        super().__init__(parent)
        
        self.target_date = date
        self.editing_event = event
        self.available_assets = available_assets or []  # [(asset_id, asset_name), ...]
        
        self.setup_ui()
        self.setup_connections()
        
        if event:
            self.populate_from_event(event)
            
        self.setWindowTitle("Schedule Content" if not event else "Edit Content")
        self.resize(500, 600)
        
    def setup_ui(self):
        """Setup dialog UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        
        # Header
        header = self.create_header()
        layout.addWidget(header)
        
        # Scroll area for form
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
        
        # Content details
        content_group = self.create_content_group()
        form_layout.addWidget(content_group)
        
        # Asset selection
        assets_group = self.create_assets_group()
        form_layout.addWidget(assets_group)
        
        # Platform selection
        platforms_group = self.create_platforms_group()
        form_layout.addWidget(platforms_group)
        
        form_layout.addStretch()
        layout.addWidget(scroll)
        
        # Buttons
        buttons = self.create_buttons()
        layout.addWidget(buttons)
        
    def create_header(self) -> QWidget:
        """Create dialog header"""
        header = QFrame()
        header.setStyleSheet("background-color: #2d2d30; border-radius: 5px; padding: 10px;")
        
        layout = QVBoxLayout(header)
        
        title = QLabel("Schedule Content Release")
        title.setStyleSheet("color: #cccccc; font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        date_label = QLabel(f"Date: {self.target_date.strftime('%A, %B %d, %Y')}")
        date_label.setStyleSheet("color: #969696; font-size: 12px;")
        layout.addWidget(date_label)
        
        return header
        
    def create_basic_info_group(self) -> QGroupBox:
        """Create basic information group"""
        group = QGroupBox("Basic Information")
        layout = QFormLayout(group)
        
        # Content type
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems([
            "reel", "story", "post", "teaser", "tutorial"
        ])
        layout.addRow("Content Type:", self.content_type_combo)
        
        # Title
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter content title...")
        layout.addRow("Title:", self.title_edit)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Brief description of the content...")
        layout.addRow("Description:", self.description_edit)
        
        # Duration
        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(5, 300)  # 5 seconds to 5 minutes
        self.duration_spin.setValue(30)
        self.duration_spin.setSuffix(" seconds")
        layout.addRow("Duration:", self.duration_spin)
        
        return group
        
    def create_content_group(self) -> QGroupBox:
        """Create content details group"""
        group = QGroupBox("Content Details")
        layout = QFormLayout(group)
        
        # Status
        self.status_combo = QComboBox()
        self.status_combo.addItems(["planned", "ready", "published"])
        layout.addRow("Status:", self.status_combo)
        
        # Hashtags
        self.hashtags_edit = QLineEdit()
        self.hashtags_edit.setPlaceholderText("#plugin #music #production (separate with spaces)")
        layout.addRow("Hashtags:", self.hashtags_edit)
        
        return group
        
    def create_assets_group(self) -> QGroupBox:
        """Create asset selection group"""
        group = QGroupBox("Assets")
        layout = QVBoxLayout(group)
        
        if not self.available_assets:
            no_assets_label = QLabel("No assets available in project")
            no_assets_label.setStyleSheet("color: #969696; font-style: italic;")
            layout.addWidget(no_assets_label)
        else:
            # Asset list with checkboxes
            self.assets_list = QListWidget()
            self.assets_list.setMaximumHeight(120)
            
            for asset_id, asset_name in self.available_assets:
                item = QListWidgetItem(asset_name)
                item.setData(Qt.ItemDataRole.UserRole, asset_id)
                item.setFlags(item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
                item.setCheckState(Qt.CheckState.Unchecked)
                self.assets_list.addItem(item)
                
            layout.addWidget(QLabel("Select assets to include:"))
            layout.addWidget(self.assets_list)
            
        return group
        
    def create_platforms_group(self) -> QGroupBox:
        """Create platform selection group"""
        group = QGroupBox("Target Platforms")
        layout = QVBoxLayout(group)
        
        # Platform checkboxes
        platforms_layout = QHBoxLayout()
        
        self.platform_checkboxes = {}
        platforms = ["instagram", "tiktok", "youtube", "twitter", "facebook"]
        
        for platform in platforms:
            checkbox = QCheckBox(platform.title())
            self.platform_checkboxes[platform] = checkbox
            platforms_layout.addWidget(checkbox)
            
        layout.addLayout(platforms_layout)
        
        return group
        
    def create_buttons(self) -> QWidget:
        """Create dialog buttons"""
        button_widget = QFrame()
        layout = QHBoxLayout(button_widget)
        
        # Cancel button
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        layout.addWidget(cancel_btn)
        
        layout.addStretch()
        
        # Save button
        self.save_btn = QPushButton("Create Event" if not self.editing_event else "Update Event")
        self.save_btn.setDefault(True)
        self.save_btn.clicked.connect(self.save_event)
        layout.addWidget(self.save_btn)
        
        return button_widget
        
    def setup_connections(self):
        """Setup signal connections"""
        self.title_edit.textChanged.connect(self.validate_form)
        self.content_type_combo.currentTextChanged.connect(self.validate_form)
        
    def validate_form(self):
        """Validate form and enable/disable save button"""
        title = self.title_edit.text().strip()
        content_type = self.content_type_combo.currentText()
        
        is_valid = bool(title and content_type)
        self.save_btn.setEnabled(is_valid)
        
    def populate_from_event(self, event: ReleaseEvent):
        """Populate form from existing event"""
        self.title_edit.setText(event.title)
        self.description_edit.setPlainText(event.description)
        
        # Set content type
        index = self.content_type_combo.findText(event.content_type)
        if index >= 0:
            self.content_type_combo.setCurrentIndex(index)
            
        # Set status
        status_index = self.status_combo.findText(event.status)
        if status_index >= 0:
            self.status_combo.setCurrentIndex(status_index)
            
        # Set duration
        self.duration_spin.setValue(event.duration_seconds)
        
        # Set hashtags
        if event.hashtags:
            self.hashtags_edit.setText(" ".join(event.hashtags))
            
        # Set selected assets
        if hasattr(self, 'assets_list'):
            for i in range(self.assets_list.count()):
                item = self.assets_list.item(i)
                asset_id = item.data(Qt.ItemDataRole.UserRole)
                if asset_id in event.assets:
                    item.setCheckState(Qt.CheckState.Checked)
                    
        # Set platforms
        for platform, checkbox in self.platform_checkboxes.items():
            checkbox.setChecked(platform in event.platforms)
            
    def save_event(self):
        """Save the event"""
        try:
            # Collect form data
            title = self.title_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            content_type = self.content_type_combo.currentText()
            status = self.status_combo.currentText()
            duration = self.duration_spin.value()
            
            # Get hashtags
            hashtags_text = self.hashtags_edit.text().strip()
            hashtags = [tag.strip() for tag in hashtags_text.split() if tag.strip().startswith('#')]
            
            # Get selected assets
            selected_assets = []
            if hasattr(self, 'assets_list'):
                for i in range(self.assets_list.count()):
                    item = self.assets_list.item(i)
                    if item.checkState() == Qt.CheckState.Checked:
                        asset_id = item.data(Qt.ItemDataRole.UserRole)
                        selected_assets.append(asset_id)
                        
            # Get selected platforms
            selected_platforms = []
            for platform, checkbox in self.platform_checkboxes.items():
                if checkbox.isChecked():
                    selected_platforms.append(platform)
                    
            # Create or update event
            if self.editing_event:
                # Update existing event
                event = self.editing_event
                event.title = title
                event.description = description
                event.content_type = content_type
                event.status = status
                event.duration_seconds = duration
                event.assets = selected_assets
                event.platforms = selected_platforms
                event.hashtags = hashtags
                
                self.event_updated.emit(event)
            else:
                # Create new event
                event = ReleaseEvent(
                    id="",  # Will be auto-generated
                    date=self.target_date.date().isoformat(),
                    title=title,
                    description=description,
                    content_type=content_type,
                    status=status,
                    duration_seconds=duration,
                    assets=selected_assets,
                    platforms=selected_platforms,
                    hashtags=hashtags
                )
                
                self.event_created.emit(event)
                
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save event:\n{str(e)}")
            
    def get_selected_assets(self) -> List[str]:
        """Get list of selected asset IDs"""
        selected = []
        if hasattr(self, 'assets_list'):
            for i in range(self.assets_list.count()):
                item = self.assets_list.item(i)
                if item.checkState() == Qt.CheckState.Checked:
                    asset_id = item.data(Qt.ItemDataRole.UserRole)
                    selected.append(asset_id)
        return selected
