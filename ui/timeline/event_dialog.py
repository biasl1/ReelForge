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
    """Dialog for creating/editing release events - AI-focused workflow"""
    
    event_created = pyqtSignal(ReleaseEvent)
    event_updated = pyqtSignal(ReleaseEvent)
    
    def __init__(self, date: datetime, event: Optional[ReleaseEvent] = None, parent=None):
        super().__init__(parent)
        
        self.target_date = date
        self.editing_event = event
        
        self.setup_ui()
        self.setup_connections()
        
        if event:
            self.populate_from_event(event)
            
        self.setWindowTitle("Schedule Content" if not event else "Edit Content")
        self.resize(450, 400)
        
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
        
        # Basic info - simplified for AI workflow
        basic_group = self.create_basic_info_group()
        form_layout.addWidget(basic_group)
        
        # AI prompt - the key input for content generation
        prompt_group = self.create_prompt_group()
        form_layout.addWidget(prompt_group)
        
        # Target platforms
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
        """Create basic information group - simplified for AI"""
        group = QGroupBox("Content Planning")
        layout = QFormLayout(group)
        
        # Content type
        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems([
            "reel", "story", "post", "teaser", "tutorial"
        ])
        layout.addRow("Content Type:", self.content_type_combo)
        
        # Title - simplified, can be AI-generated
        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Enter title or leave blank for AI generation...")
        layout.addRow("Title (optional):", self.title_edit)
        
        return group
        
    def create_prompt_group(self) -> QGroupBox:
        """Create AI prompt group - the main input for content generation"""
        group = QGroupBox("AI Content Prompt")
        layout = QVBoxLayout(group)
        
        # Main prompt explanation
        explanation = QLabel("Describe what you want this content to showcase. The AI will use this prompt along with your plugin info and project assets to generate the content.")
        explanation.setStyleSheet("color: #969696; font-style: italic; font-size: 10px;")
        explanation.setWordWrap(True)
        layout.addWidget(explanation)
        
        # Description/prompt text area
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(100)
        self.description_edit.setPlaceholderText("Example: 'Show the warm saturation effect on a guitar melody, highlighting the vintage tube sound...'")
        layout.addWidget(self.description_edit)
        
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
        """Save the event with simplified AI-focused data"""
        try:
            # Collect form data
            title = self.title_edit.text().strip()
            description = self.description_edit.toPlainText().strip()
            content_type = self.content_type_combo.currentText()
            
            # Use title as description if title is empty (AI will generate title)
            if not title and description:
                title = f"{content_type.title()} - AI Generated"
            elif not title and not description:
                title = f"{content_type.title()} Content"
                
            # If no description, use a default AI prompt
            if not description:
                description = f"Generate {content_type} content showcasing the plugin features."
                        
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
                event.platforms = selected_platforms
                
                self.event_updated.emit(event)
            else:
                # Create new event with AI-focused defaults
                event = ReleaseEvent(
                    id="",  # Will be auto-generated
                    date=self.target_date.date().isoformat(),
                    title=title,
                    description=description,
                    content_type=content_type,
                    status="planned",  # Default status
                    duration_seconds=30,  # Default duration
                    assets=[],  # AI will select assets
                    platforms=selected_platforms,
                    hashtags=[]  # AI will generate hashtags
                )
                
                self.event_created.emit(event)
                
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save event:\n{str(e)}")
            
    def populate_from_event(self, event: ReleaseEvent):
        """Populate dialog with existing event data"""
        self.content_type_combo.setCurrentText(event.content_type)
        self.title_edit.setText(event.title)
        self.description_edit.setPlainText(event.description)
        
        # Set platforms
        for platform, checkbox in self.platform_checkboxes.items():
            checkbox.setChecked(platform in event.platforms)
