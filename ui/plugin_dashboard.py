"""
Plugin Information Dashboard
Displays plugin information for the current project (one plugin per project)
"""

from pathlib import Path
from typing import Optional
from datetime import datetime
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QGroupBox, QFormLayout, QScrollArea,
    QFileDialog, QMessageBox, QFrame, QTabWidget,
    QComboBox, QSplitter, QListWidget, QListWidgetItem
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap

from core.plugins import PluginInfo, get_supported_content_types, generate_ai_prompts_for_plugin


class PluginInfoWidget(QWidget):
    """Widget to display detailed plugin information"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_plugin: Optional[PluginInfo] = None
        self.template_editor = None  # Reference to template editor (if any)
        self._setup_ui()

    def _setup_ui(self):
        """Setup the plugin info display UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)

        # Plugin header
        self.header_frame = self._create_header_section()
        layout.addWidget(self.header_frame)

        # Tabs for different info sections
        self.tab_widget = QTabWidget()
        layout.addWidget(self.tab_widget)

        # Basic Info Tab
        self.basic_tab = self._create_basic_info_tab()
        self.tab_widget.addTab(self.basic_tab, "Basic Info")

        # Marketing Tab
        self.marketing_tab = self._create_marketing_tab()
        self.tab_widget.addTab(self.marketing_tab, "Marketing")

        # Technical Tab
        self.technical_tab = self._create_technical_tab()
        self.tab_widget.addTab(self.technical_tab, "Technical")

        # AI Prompts Tab
        self.ai_prompts_tab = self._create_ai_prompts_tab()
        self.tab_widget.addTab(self.ai_prompts_tab, "AI Prompts")

    def _create_header_section(self) -> QFrame:
        """Create plugin header section"""
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #2d2d30;
                border-radius: 5px;
                padding: 10px;
            }
        """)

        layout = QVBoxLayout(frame)
        layout.setSpacing(5)

        # Plugin name
        self.name_label = QLabel("No Plugin Selected")
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        self.name_label.setFont(font)
        self.name_label.setStyleSheet("color: #007acc;")
        layout.addWidget(self.name_label)

        # Plugin tagline
        self.tagline_label = QLabel("")
        self.tagline_label.setStyleSheet("color: #cccccc; font-style: italic;")
        layout.addWidget(self.tagline_label)

        # Company and version
        info_layout = QHBoxLayout()
        self.company_label = QLabel("")
        self.version_label = QLabel("")
        self.company_label.setStyleSheet("color: #969696;")
        self.version_label.setStyleSheet("color: #969696;")

        info_layout.addWidget(self.company_label)
        info_layout.addStretch()
        info_layout.addWidget(self.version_label)
        layout.addLayout(info_layout)

        return frame

    def _create_basic_info_tab(self) -> QWidget:
        """Create basic info tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QFormLayout(content)

        # Basic fields
        self.title_field = QLabel()
        self.code_field = QLabel()
        self.category_field = QLabel()
        self.use_cases_field = QLabel()
        self.one_word_field = QLabel()
        self.personality_field = QLabel()

        content_layout.addRow("Title:", self.title_field)
        content_layout.addRow("Code:", self.code_field)
        content_layout.addRow("Categories:", self.category_field)
        content_layout.addRow("Use Cases:", self.use_cases_field)
        content_layout.addRow("One Word:", self.one_word_field)
        content_layout.addRow("Personality:", self.personality_field)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        return widget

    def _create_marketing_tab(self) -> QWidget:
        """Create marketing info tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Scroll area
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        content = QWidget()
        content_layout = QVBoxLayout(content)

        # Marketing fields
        self.short_desc_field = QTextEdit()
        self.short_desc_field.setMaximumHeight(80)
        self.short_desc_field.setReadOnly(True)

        self.long_desc_field = QTextEdit()
        self.long_desc_field.setMaximumHeight(120)
        self.long_desc_field.setReadOnly(True)

        self.unique_field = QTextEdit()
        self.unique_field.setMaximumHeight(80)
        self.unique_field.setReadOnly(True)

        self.problem_field = QTextEdit()
        self.problem_field.setMaximumHeight(60)
        self.problem_field.setReadOnly(True)

        self.wow_field = QTextEdit()
        self.wow_field.setMaximumHeight(60)
        self.wow_field.setReadOnly(True)

        content_layout.addWidget(QLabel("Short Description:"))
        content_layout.addWidget(self.short_desc_field)
        content_layout.addWidget(QLabel("Long Description:"))
        content_layout.addWidget(self.long_desc_field)
        content_layout.addWidget(QLabel("Unique Selling Point:"))
        content_layout.addWidget(self.unique_field)
        content_layout.addWidget(QLabel("Problem Solved:"))
        content_layout.addWidget(self.problem_field)
        content_layout.addWidget(QLabel("Wow Factor:"))
        content_layout.addWidget(self.wow_field)

        scroll.setWidget(content)
        layout.addWidget(scroll)

        return widget

    def _create_technical_tab(self) -> QWidget:
        """Create technical info tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Form layout
        form_layout = QFormLayout()

        self.input_type_field = QLabel()
        self.sidechain_field = QLabel()
        self.tech_summary_field = QTextEdit()
        self.tech_summary_field.setMaximumHeight(100)
        self.tech_summary_field.setReadOnly(True)

        form_layout.addRow("Input Type:", self.input_type_field)
        form_layout.addRow("Has Sidechain:", self.sidechain_field)
        form_layout.addRow("Technical Summary:", self.tech_summary_field)

        layout.addLayout(form_layout)
        layout.addStretch()

        return widget

    def _create_ai_prompts_tab(self) -> QWidget:
        """Create AI prompts tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Content type selector
        selector_layout = QHBoxLayout()
        selector_layout.addWidget(QLabel("Content Type:"))

        self.content_type_combo = QComboBox()
        self.content_type_combo.addItems(list(get_supported_content_types().keys()))
        self.content_type_combo.currentTextChanged.connect(self._update_ai_prompts)
        selector_layout.addWidget(self.content_type_combo)
        selector_layout.addStretch()

        layout.addLayout(selector_layout)

        # AI prompts list
        self.prompts_list = QListWidget()
        layout.addWidget(self.prompts_list)

        return widget

    def set_plugin(self, plugin_info: Optional[PluginInfo]):
        """Set the plugin to display"""
        self.current_plugin = plugin_info
        self._update_display()

    def set_template_editor(self, template_editor):
        """Set reference to the template editor for real layout export"""
        self.template_editor = template_editor

    def _update_display(self):
        """Update all display elements"""
        if not self.current_plugin:
            self._clear_display()
            return

        plugin = self.current_plugin

        # Update header
        self.name_label.setText(plugin.name)
        self.tagline_label.setText(plugin.tagline)
        self.company_label.setText(plugin.company)
        self.version_label.setText(f"v{plugin.version}")

        # Update basic info
        self.title_field.setText(plugin.title)
        self.code_field.setText(plugin.code)
        self.category_field.setText(", ".join(plugin.category))
        self.use_cases_field.setText(", ".join(plugin.intended_use))
        self.one_word_field.setText(plugin.one_word)
        self.personality_field.setText(plugin.personality)

        # Update marketing
        self.short_desc_field.setText(plugin.short_description)
        self.long_desc_field.setText(plugin.long_description)
        self.unique_field.setText(plugin.unique)
        self.problem_field.setText(plugin.problem)
        self.wow_field.setText(plugin.wow)

        # Update technical
        self.input_type_field.setText(plugin.input_type)
        self.sidechain_field.setText("Yes" if plugin.has_sidechain else "No")
        self.tech_summary_field.setText(plugin.tech_summary)

        # Update AI prompts
        self._update_ai_prompts()

    def _update_ai_prompts(self):
        """Update AI prompts based on selected content type"""
        if not self.current_plugin:
            return

        content_type = self.content_type_combo.currentText()
        prompts = generate_ai_prompts_for_plugin(self.current_plugin, content_type)

        self.prompts_list.clear()
        for i, prompt in enumerate(prompts, 1):
            item = QListWidgetItem(f"{i}. {prompt}")
            self.prompts_list.addItem(item)

    def _clear_display(self):
        """Clear all display elements"""
        self.name_label.setText("No Plugin Selected")
        self.tagline_label.setText("")
        self.company_label.setText("")
        self.version_label.setText("")

        # Clear all fields
        for field in [self.title_field, self.code_field, self.category_field,
                     self.use_cases_field, self.one_word_field, self.personality_field,
                     self.input_type_field, self.sidechain_field]:
            field.setText("")

        for field in [self.short_desc_field, self.long_desc_field, self.unique_field,
                     self.problem_field, self.wow_field, self.tech_summary_field]:
            field.setText("")

        self.prompts_list.clear()


class PluginDashboard(QWidget):
    """Simplified plugin dashboard - one plugin per project workflow"""

    plugin_imported = pyqtSignal(str)  # plugin_name

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.current_moodboard_path = None
        self._setup_ui()

    def _setup_ui(self):
        """Setup the simplified dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        # Header section
        header_layout = QHBoxLayout()

        title = QLabel("Plugin Information")
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        title.setFont(font)
        title.setStyleSheet("color: #cccccc;")
        header_layout.addWidget(title)

        header_layout.addStretch()

        # Import button
        self.import_btn = QPushButton("Import .adsp File")
        self.import_btn.clicked.connect(self._import_adsp_file)
        self.import_btn.setStyleSheet("""
            QPushButton {
                background-color: #0e639c;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
        """)
        header_layout.addWidget(self.import_btn)

        layout.addLayout(header_layout)

        # Plugin info display (main content)
        self.plugin_info_widget = PluginInfoWidget()
        layout.addWidget(self.plugin_info_widget)

        # Global prompt section
        global_prompt_group = self._create_global_prompt_section()
        layout.addWidget(global_prompt_group)

        # Moodboard section
        moodboard_group = self._create_moodboard_section()
        layout.addWidget(moodboard_group)

        # Generate button (placeholder for future AI integration)
        self.generate_btn = QPushButton("🚀 Generate AI Data JSON")
        self.generate_btn.clicked.connect(self._generate_ai_data_json)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #1177bb;
            }
            QPushButton:disabled {
                background-color: #464647;
                color: #969696;
            }
        """)
        layout.addWidget(self.generate_btn)

    def _create_global_prompt_section(self) -> QGroupBox:
        """Create global AI prompt section"""
        group = QGroupBox("Global AI Prompt")
        layout = QVBoxLayout(group)

        # Explanation
        explanation = QLabel("This prompt will be used for all content generation along with individual event prompts. Describe the overall style, brand voice, and key messaging for your plugin.")
        explanation.setStyleSheet("color: #969696; font-style: italic; font-size: 10px;")
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # Global prompt text area
        self.global_prompt_edit = QTextEdit()
        self.global_prompt_edit.setMaximumHeight(80)
        self.global_prompt_edit.setPlaceholderText("Example: 'Professional, warm tone. Focus on the vintage analog character. Show real-world music production scenarios...'")
        self.global_prompt_edit.textChanged.connect(self._on_global_prompt_changed)
        layout.addWidget(self.global_prompt_edit)

        return group

    def _create_moodboard_section(self) -> QGroupBox:
        """Create moodboard upload section"""
        group = QGroupBox("Moodboard (Optional)")
        layout = QVBoxLayout(group)

        # Explanation
        explanation = QLabel("Upload a reference image to guide the visual style of generated content.")
        explanation.setStyleSheet("color: #969696; font-style: italic; font-size: 10px;")
        explanation.setWordWrap(True)
        layout.addWidget(explanation)

        # Preview area (hidden by default)
        self.moodboard_preview = QLabel()
        self.moodboard_preview.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.moodboard_preview.setMinimumHeight(100)
        self.moodboard_preview.setMaximumHeight(100)
        self.moodboard_preview.setStyleSheet("""
            QLabel {
                border: 1px solid #444;
                border-radius: 6px;
                background-color: #2A2A2A;
            }
        """)
        self.moodboard_preview.hide()  # Hidden by default
        layout.addWidget(self.moodboard_preview)

        # Moodboard controls
        moodboard_layout = QHBoxLayout()

        self.moodboard_label = QLabel("No moodboard uploaded")
        self.moodboard_label.setStyleSheet("color: #969696; font-style: italic;")
        moodboard_layout.addWidget(self.moodboard_label)

        moodboard_layout.addStretch()

        # Upload button
        self.upload_moodboard_btn = QPushButton("Upload Image")
        self.upload_moodboard_btn.clicked.connect(self._upload_moodboard)
        moodboard_layout.addWidget(self.upload_moodboard_btn)

        # Clear button
        self.clear_moodboard_btn = QPushButton("Clear")
        self.clear_moodboard_btn.clicked.connect(self._clear_moodboard)
        self.clear_moodboard_btn.setVisible(False)
        moodboard_layout.addWidget(self.clear_moodboard_btn)

        layout.addLayout(moodboard_layout)

        return group

    def set_project(self, project):
        """Set current project"""
        self.current_project = project

        # Update plugin display
        if project and project.current_plugin:
            plugin_info = project.get_current_plugin_info()
            self.plugin_info_widget.set_plugin(plugin_info)
            self.generate_btn.setEnabled(plugin_info is not None)

            # Load global prompt if available
            if hasattr(project, 'global_prompt'):
                self.global_prompt_edit.setPlainText(project.global_prompt)

            # Load moodboard if available
            if hasattr(project, 'moodboard_path') and project.moodboard_path:
                self.current_moodboard_path = project.moodboard_path
                self._update_moodboard_display()
        else:
            self.plugin_info_widget.set_plugin(None)
            self.generate_btn.setEnabled(False)
            self.global_prompt_edit.clear()
            self._clear_moodboard()

    def set_template_editor(self, template_editor):
        """Set reference to the template editor for real layout export"""
        self.template_editor = template_editor

    def _on_global_prompt_changed(self):
        """Handle global prompt text change"""
        if self.current_project:
            self.current_project.global_prompt = self.global_prompt_edit.toPlainText()
            self.current_project.mark_modified()

    def _upload_moodboard(self):
        """Upload moodboard image"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please create or open a project first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Upload Moodboard Image",
            str(Path.home()),
            "Image Files (*.jpg *.jpeg *.png *.gif *.bmp);;All Files (*)"
        )

        if file_path:
            try:
                # Copy to project directory
                project_dir = self.current_project.project_directory
                if project_dir:
                    moodboard_dir = project_dir / "moodboard"
                    moodboard_dir.mkdir(exist_ok=True)

                    file_ext = Path(file_path).suffix
                    new_path = moodboard_dir / f"moodboard{file_ext}"

                    import shutil
                    shutil.copy2(file_path, new_path)

                    self.current_moodboard_path = str(new_path.relative_to(project_dir))
                    self.current_project.moodboard_path = self.current_moodboard_path
                    self.current_project.mark_modified()

                    self._update_moodboard_display()

            except Exception as e:
                QMessageBox.critical(self, "Upload Failed", f"Failed to upload moodboard: {e}")

    def _clear_moodboard(self):
        """Clear current moodboard"""
        self.current_moodboard_path = None
        if self.current_project:
            self.current_project.moodboard_path = None
            self.current_project.mark_modified()
        self._update_moodboard_display()

    def _update_moodboard_display(self):
        """Update moodboard display"""
        if self.current_moodboard_path:
            filename = Path(self.current_moodboard_path).name
            self.moodboard_label.setText(f"Uploaded: {filename}")
            self.moodboard_label.setStyleSheet("color: #007acc;")
            self.clear_moodboard_btn.setVisible(True)

            # Show preview with image
            self._load_moodboard_preview()
            self.moodboard_preview.show()
        else:
            self.moodboard_label.setText("No moodboard uploaded")
            self.moodboard_label.setStyleSheet("color: #969696; font-style: italic;")
            self.clear_moodboard_btn.setVisible(False)

            # Hide preview
            self.moodboard_preview.hide()

    def _load_moodboard_preview(self):
        """Load and display moodboard preview image"""
        if not self.current_moodboard_path or not self.current_project:
            return

        try:
            # Get full path to moodboard
            project_dir = self.current_project.project_directory
            if project_dir:
                full_path = project_dir / self.current_moodboard_path

                if full_path.exists():
                    # Load and scale the image to fit preview
                    pixmap = QPixmap(str(full_path))
                    if not pixmap.isNull():
                        scaled_pixmap = pixmap.scaled(
                            200, 100,
                            Qt.AspectRatioMode.KeepAspectRatio,
                            Qt.TransformationMode.SmoothTransformation
                        )
                        self.moodboard_preview.setPixmap(scaled_pixmap)
        except Exception as e:
            self.moodboard_preview.setText("Error loading preview")

    def _import_adsp_file(self):
        """Import .adsp file"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please create or open a project first.")
            return

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Plugin (.adsp file)",
            str(Path.home()),
            "Artista Plugin Files (*.adsp);;All Files (*)"
        )

        if file_path:
            success = self.current_project.import_plugin_info(Path(file_path))
            if success:
                # Update display
                plugin_info = self.current_project.get_current_plugin_info()
                self.plugin_info_widget.set_plugin(plugin_info)
                self.generate_btn.setEnabled(True)

                self.plugin_imported.emit(self.current_project.current_plugin or "")

                QMessageBox.information(
                    self,
                    "Import Successful",
                    f"Plugin information imported successfully!\n\n"
                    f"Plugin: {plugin_info.name if plugin_info else 'Unknown'}\n"
                    f"Version: {plugin_info.version if plugin_info else 'Unknown'}\n\n"
                    f"This plugin is now ready for AI content generation."
                )
            else:
                QMessageBox.critical(
                    self,
                    "Import Failed",
                    "Failed to import plugin information. Please check the file format."
                )

    def _generate_ai_data_json(self):
        """Generate AI data JSON file for content generation"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please create or open a project first.")
            return

        # Check if we have minimum requirements
        if not self.current_project.current_plugin:
            QMessageBox.warning(
                self,
                "No Plugin",
                "Please import a plugin (.adsp file) first.\n\nThe AI needs plugin information to generate relevant content."
            )
            return

        if not self.current_project.release_events:
            reply = QMessageBox.question(
                self,
                "No Scheduled Content",
                "No content events are scheduled on the timeline.\n\nDo you want to generate AI data anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.No:
                return

        try:
            # Get complete AI generation data with real template layouts
            template_editor = getattr(self, 'template_editor', None)
            ai_data = self.current_project.get_ai_generation_data(template_editor=template_editor)

            # Choose export location
            current_time = datetime.now()
            default_name = f"{self.current_project.project_name}_ai_data_{current_time.strftime('%Y%m%d_%H%M%S')}.json"

            file_path, _ = QFileDialog.getSaveFileName(
                self,
                "Export AI Generation Data",
                str(Path.home() / default_name),
                "JSON Files (*.json);;All Files (*)"
            )

            if file_path:
                # Export the JSON
                import json
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(ai_data, f, indent=2, ensure_ascii=False)

                # Show success message with details
                plugin_name = ai_data.get("plugin", {}).get("name", "Unknown") if ai_data.get("plugin") else "None"
                events_count = len(ai_data.get("scheduled_content", []))
                assets_count = len(ai_data.get("assets", []))
                sessions_count = len(ai_data.get("xplainpack_sessions", []))

                success_message = (
                    f"AI generation data exported to:\n{file_path}\n\n"
                    f"📊 Data Summary:\n"
                    f"Plugin: {plugin_name}\n"
                    f"Scheduled Content: {events_count} events\n"
                    f"Available Assets: {assets_count} files\n"
                )
                
                if sessions_count > 0:
                    success_message += f"XplainPack Sessions: {sessions_count} sessions\n"
                
                success_message += (
                    f"Global Prompt: {'✓' if ai_data.get('global_prompt') else '✗'}\n"
                    f"Moodboard: {'✓' if ai_data.get('moodboard_path') else '✗'}\n\n"
                )
                
                if sessions_count > 0:
                    success_message += "🎙️ Enhanced with XplainPack synchronized voice and transient data!\n\n"
                
                success_message += "This JSON contains all the information needed for AI content generation!"

                QMessageBox.information(
                    self,
                    "AI Data Exported Successfully!",
                    success_message
                )

                # Offer to open the file
                reply = QMessageBox.question(
                    self,
                    "Open File?",
                    "Would you like to open the exported JSON file to review the data?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                    QMessageBox.StandardButton.No
                )

                if reply == QMessageBox.StandardButton.Yes:
                    import subprocess
                    import sys

                    try:
                        if sys.platform == "darwin":  # macOS
                            subprocess.call(["open", file_path])
                        elif sys.platform == "win32":  # Windows
                            subprocess.call(["start", file_path], shell=True)
                        else:  # Linux
                            subprocess.call(["xdg-open", file_path])
                    except Exception as e:
                        QMessageBox.information(
                            self,
                            "File Location",
                            f"File saved at:\n{file_path}\n\n(Could not auto-open: {e})"
                        )

        except Exception as e:
            QMessageBox.critical(
                self,
                "Export Failed",
                f"Failed to export AI generation data:\n\n{str(e)}\n\nPlease check your project data and try again."
            )
