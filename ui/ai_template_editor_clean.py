"""
Clean AI Template Editor for ReelTune - Essential functionality only
"""
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel,
    QComboBox, QGroupBox, QPushButton, QSplitter, QCheckBox, 
    QSpinBox, QScrollArea, QApplication, QDialog, QTextEdit, QMessageBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QPainter, QPen, QFont
from datetime import datetime
import json


class SimpleTemplateCanvas(QWidget):
    """Preview canvas for template layout"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(300, 400)
        self.setMaximumSize(500, 600)
        self.content_type = "reel"
        self.config = {}
        self.subtitle_position = "Bottom"
        self.font_size = 24
        self.is_fixed = False

    def set_content_type(self, content_type: str):
        self.content_type = content_type.lower()
        self.update()

    def update_template_config(self, config):
        self.config = config
        self.update()

    def update_subtitle_preview(self, position, font_size, is_fixed):
        self.subtitle_position = position
        self.font_size = font_size
        self.is_fixed = is_fixed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        width, height = self.width(), self.height()
        
        # Background
        painter.fillRect(0, 0, width, height, QColor(26, 26, 26))
        
        # Draw zones based on content type
        if self.content_type in ["reel", "story", "tutorial"]:
            self._draw_video_zones(painter, width, height)
        else:
            self._draw_post_zones(painter, width, height)

    def _draw_video_zones(self, painter, width, height):
        # Background zone
        if self.config.get('background_enabled', True):
            painter.setPen(QPen(QColor(0, 120, 212), 2))
            painter.drawRect(10, 10, width-20, height//3)
            painter.drawText(20, 30, "Background Zone")
        
        # Media zone
        if self.config.get('media_window_enabled', True):
            painter.setPen(QPen(QColor(255, 149, 0), 2))
            painter.drawRect(10, height//3 + 20, width-20, height//3)
            painter.drawText(20, height//3 + 40, "Media Window")
        
        # Subtitle zone
        if self.config.get('subtitle_enabled', True):
            painter.setPen(QPen(QColor(82, 199, 89), 2))
            y_pos = height//3 * 2 + 30
            painter.drawRect(10, y_pos, width-20, height//3 - 40)
            
            # Show subtitle preview
            font = QFont("Arial", max(8, self.font_size // 3))
            painter.setFont(font)
            color = QColor(255, 149, 0) if self.is_fixed else QColor(255, 255, 255)
            painter.setPen(color)
            
            text = f"Sample Text ({self.subtitle_position}, {self.font_size}px)"
            if self.subtitle_position == "Top":
                painter.drawText(20, y_pos + 20, text)
            elif self.subtitle_position == "Center":
                painter.drawText(20, y_pos + height//6, text)
            else:  # Bottom
                painter.drawText(20, y_pos + height//3 - 30, text)

    def _draw_post_zones(self, painter, width, height):
        # Simplified post layout
        painter.setPen(QPen(QColor(0, 120, 212), 2))
        painter.drawRect(10, 10, width-20, height-20)
        painter.drawText(20, 30, f"{self.content_type.title()} Template")


class TimelineSection(QWidget):
    """Simple timeline widget"""
    asset_dropped = pyqtSignal(str, str)
    asset_removed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.intro_asset = None
        self.outro_asset = None
        self.intro_duration = 3
        self.outro_duration = 3
        
        layout = QHBoxLayout(self)
        layout.addWidget(QLabel("🎬 Timeline: Drag assets here"))

    def set_intro_duration(self, duration):
        self.intro_duration = duration

    def set_outro_duration(self, duration):
        self.outro_duration = duration

    def has_intro(self):
        return self.intro_asset is not None

    def has_outro(self):
        return self.outro_asset is not None


class AITemplateEditor(QWidget):
    """Clean AI Template Editor"""
    template_changed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.project = None
        self.current_content_type = "reel"
        self._setup_ui()
        self._setup_connections()

    def _setup_ui(self):
        """Setup clean UI"""
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Left panel - Preview
        left_panel = QFrame()
        left_panel.setStyleSheet("QFrame { background: #2d2d2d; border-radius: 8px; }")
        left_layout = QVBoxLayout(left_panel)
        
        # Content type selector
        self.content_type_selector = QComboBox()
        self.content_type_selector.addItems(["Reel", "Story", "Post", "Tutorial"])
        left_layout.addWidget(self.content_type_selector)
        
        # Canvas
        self.canvas = SimpleTemplateCanvas()
        left_layout.addWidget(self.canvas)
        
        # Timeline (for video content only)
        self.timeline_group = QGroupBox("Timeline")
        timeline_layout = QVBoxLayout(self.timeline_group)
        
        # AI choices
        ai_layout = QHBoxLayout()
        self.intro_ai_chooses = QCheckBox("AI chooses intro")
        self.outro_ai_chooses = QCheckBox("AI chooses outro")
        ai_layout.addWidget(self.intro_ai_chooses)
        ai_layout.addWidget(self.outro_ai_chooses)
        timeline_layout.addLayout(ai_layout)
        
        self.timeline = TimelineSection()
        timeline_layout.addWidget(self.timeline)
        
        # Duration controls
        duration_layout = QHBoxLayout()
        duration_layout.addWidget(QLabel("Intro:"))
        self.intro_duration = QSpinBox()
        self.intro_duration.setRange(1, 10)
        self.intro_duration.setValue(3)
        self.intro_duration.setSuffix("s")
        duration_layout.addWidget(self.intro_duration)
        
        duration_layout.addWidget(QLabel("Outro:"))
        self.outro_duration = QSpinBox()
        self.outro_duration.setRange(1, 10)
        self.outro_duration.setValue(3)
        self.outro_duration.setSuffix("s")
        duration_layout.addWidget(self.outro_duration)
        timeline_layout.addLayout(duration_layout)
        
        left_layout.addWidget(self.timeline_group)
        
        # Right panel - Settings
        right_panel = QFrame()
        right_panel.setStyleSheet("QFrame { background: #2d2d2d; border-radius: 8px; }")
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        settings_widget = QWidget()
        self.settings_layout = QVBoxLayout(settings_widget)
        
        self._create_settings()
        
        scroll_area.setWidget(settings_widget)
        right_layout = QVBoxLayout(right_panel)
        right_layout.addWidget(scroll_area)
        
        # Add panels to main layout
        main_layout.addWidget(left_panel, 1)
        main_layout.addWidget(right_panel, 1)

    def _create_settings(self):
        """Create settings sections"""
        
        # Template Zones
        zones_group = QGroupBox("Template Zones")
        zones_layout = QVBoxLayout(zones_group)
        
        self.bg_enabled = QCheckBox("Background Zone")
        self.bg_enabled.setChecked(True)
        zones_layout.addWidget(self.bg_enabled)
        
        self.media_enabled = QCheckBox("Media Window")
        self.media_enabled.setChecked(True)
        zones_layout.addWidget(self.media_enabled)
        
        self.subtitle_enabled = QCheckBox("Text/Subtitles")
        self.subtitle_enabled.setChecked(True)
        zones_layout.addWidget(self.subtitle_enabled)
        
        self.settings_layout.addWidget(zones_group)
        
        # Fixed Variables
        fixed_group = QGroupBox("Fixed Variables")
        fixed_layout = QVBoxLayout(fixed_group)
        
        # Subtitle position
        pos_layout = QHBoxLayout()
        self.subtitle_position_fixed = QCheckBox("Fix position:")
        self.subtitle_position_combo = QComboBox()
        self.subtitle_position_combo.addItems(["Top", "Center", "Bottom"])
        self.subtitle_position_combo.setCurrentText("Bottom")
        self.subtitle_position_combo.setEnabled(False)
        pos_layout.addWidget(self.subtitle_position_fixed)
        pos_layout.addWidget(self.subtitle_position_combo)
        fixed_layout.addLayout(pos_layout)
        
        # Font size
        font_layout = QHBoxLayout()
        self.font_size_fixed = QCheckBox("Fix font size:")
        self.font_size_value = QSpinBox()
        self.font_size_value.setRange(12, 72)
        self.font_size_value.setValue(24)
        self.font_size_value.setSuffix("px")
        self.font_size_value.setEnabled(False)
        font_layout.addWidget(self.font_size_fixed)
        font_layout.addWidget(self.font_size_value)
        fixed_layout.addLayout(font_layout)
        
        self.settings_layout.addWidget(fixed_group)
        
        # Actions
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)
        
        self.save_btn = QPushButton("💾 Save & Export")
        self.save_btn.clicked.connect(self._save_and_export)
        actions_layout.addWidget(self.save_btn)
        
        self.prompt_btn = QPushButton("🤖 Generate AI Prompt")
        self.prompt_btn.clicked.connect(self._generate_prompt)
        actions_layout.addWidget(self.prompt_btn)
        
        self.settings_layout.addWidget(actions_group)
        self.settings_layout.addStretch()

    def _setup_connections(self):
        """Setup signal connections"""
        self.content_type_selector.currentTextChanged.connect(self._on_content_type_changed)
        
        # Zone toggles
        self.bg_enabled.toggled.connect(self._update_preview)
        self.media_enabled.toggled.connect(self._update_preview)
        self.subtitle_enabled.toggled.connect(self._update_preview)
        
        # Fixed variables
        self.subtitle_position_fixed.toggled.connect(self.subtitle_position_combo.setEnabled)
        self.subtitle_position_fixed.toggled.connect(self._update_preview)
        self.subtitle_position_combo.currentTextChanged.connect(self._update_preview)
        
        self.font_size_fixed.toggled.connect(self.font_size_value.setEnabled)
        self.font_size_fixed.toggled.connect(self._update_preview)
        self.font_size_value.valueChanged.connect(self._update_preview)
        
        # AI choices
        self.intro_ai_chooses.toggled.connect(lambda checked: self.intro_duration.setEnabled(not checked))
        self.outro_ai_chooses.toggled.connect(lambda checked: self.outro_duration.setEnabled(not checked))
        
        # Initialize
        self._update_preview()

    def _on_content_type_changed(self, content_type: str):
        """Handle content type change"""
        self.current_content_type = content_type.lower()
        self.canvas.set_content_type(content_type)
        
        # Show timeline only for video content
        is_video = self.current_content_type in ["reel", "story", "tutorial"]
        self.timeline_group.setVisible(is_video)
        
        self.template_changed.emit()

    def _update_preview(self):
        """Update preview canvas"""
        config = {
            'background_enabled': self.bg_enabled.isChecked(),
            'media_window_enabled': self.media_enabled.isChecked(),
            'subtitle_enabled': self.subtitle_enabled.isChecked()
        }
        self.canvas.update_template_config(config)
        
        # Update subtitle preview
        position = self.subtitle_position_combo.currentText()
        font_size = self.font_size_value.value()
        is_fixed = self.subtitle_position_fixed.isChecked() or self.font_size_fixed.isChecked()
        self.canvas.update_subtitle_preview(position, font_size, is_fixed)

    def _save_and_export(self):
        """Save template and export config"""
        if not self.project:
            QMessageBox.warning(self, "No Project", "Please open a project first.")
            return
            
        # Save to project
        config = self._get_config()
        if not hasattr(self.project, 'ai_templates'):
            self.project.ai_templates = {}
        self.project.ai_templates[self.current_content_type] = config
        
        # Export to file
        from pathlib import Path
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = Path(f"ai_template_{self.current_content_type}_{timestamp}.json")
        
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        QMessageBox.information(self, "Success", f"Template saved and exported to {output_file.name}")

    def _generate_prompt(self):
        """Generate AI prompt"""
        config = self._get_config()
        
        prompt_parts = [
            f"Create a {self.current_content_type} with these settings:",
            ""
        ]
        
        # Zones
        if config['zones']['background']['enabled']:
            prompt_parts.append("🎨 Background: AI controlled")
        if config['zones']['media_window']['enabled']:
            prompt_parts.append("📹 Media: AI positioned")
        if config['zones']['subtitle']['enabled']:
            prompt_parts.append("📝 Text: AI generated")
            if config['fixed_variables']['subtitle_position_fixed']:
                prompt_parts.append(f"   - Position: {config['fixed_variables']['subtitle_position_value']}")
            if config['fixed_variables']['font_size_fixed']:
                prompt_parts.append(f"   - Font size: {config['fixed_variables']['font_size_value']}px")
        
        prompt = "\n".join(prompt_parts)
        
        # Show in dialog
        dialog = QDialog(self)
        dialog.setWindowTitle("AI Prompt")
        dialog.resize(400, 300)
        
        layout = QVBoxLayout(dialog)
        text_edit = QTextEdit()
        text_edit.setPlainText(prompt)
        layout.addWidget(text_edit)
        
        close_btn = QPushButton("Close")
        close_btn.clicked.connect(dialog.accept)
        layout.addWidget(close_btn)
        
        dialog.exec()

    def _get_config(self):
        """Get current configuration"""
        return {
            'content_type': self.current_content_type,
            'zones': {
                'background': {'enabled': self.bg_enabled.isChecked()},
                'media_window': {'enabled': self.media_enabled.isChecked()},
                'subtitle': {'enabled': self.subtitle_enabled.isChecked()}
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
                'intro_duration': self.intro_duration.value(),
                'outro_duration': self.outro_duration.value()
            }
        }

    def set_project(self, project):
        """Set project"""
        self.project = project
