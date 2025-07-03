"""
Plugin Information Dashboard
Displays and manages plugin information imported from .adsp files
"""

from pathlib import Path
from typing import Optional
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, 
    QPushButton, QGroupBox, QFormLayout, QScrollArea,
    QFileDialog, QMessageBox, QComboBox, QFrame, QSplitter,
    QListWidget, QListWidgetItem, QTabWidget
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPalette

from core.plugins import PluginInfo, get_supported_content_types, generate_ai_prompts_for_plugin


class PluginInfoWidget(QWidget):
    """Widget to display detailed plugin information"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_plugin: Optional[PluginInfo] = None
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
    """Complete plugin management dashboard"""
    
    plugin_selected = pyqtSignal(str)  # plugin_name
    plugin_imported = pyqtSignal(str)  # plugin_name
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup the dashboard UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title and controls
        header_layout = QHBoxLayout()
        
        title = QLabel("Plugin Information")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Import button
        self.import_btn = QPushButton("Import .adsp")
        self.import_btn.clicked.connect(self._import_adsp_file)
        header_layout.addWidget(self.import_btn)
        
        layout.addLayout(header_layout)
        
        # Splitter for plugin list and details
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Plugin selection panel
        selection_panel = self._create_selection_panel()
        splitter.addWidget(selection_panel)
        
        # Plugin info display
        self.plugin_info_widget = PluginInfoWidget()
        splitter.addWidget(self.plugin_info_widget)
        
        splitter.setSizes([200, 400])
        layout.addWidget(splitter)
        
        # Generate button (placeholder for future AI integration)
        self.generate_btn = QPushButton("🚀 Generate Media (Coming Soon)")
        self.generate_btn.setEnabled(False)
        self.generate_btn.setStyleSheet("""
            QPushButton {
                background-color: #007acc;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:disabled {
                background-color: #464647;
                color: #969696;
            }
        """)
        layout.addWidget(self.generate_btn)
        
    def _create_selection_panel(self) -> QWidget:
        """Create plugin selection panel"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Current plugin label
        current_label = QLabel("Current Plugin:")
        current_label.setStyleSheet("font-weight: bold; color: #cccccc;")
        layout.addWidget(current_label)
        
        self.current_plugin_label = QLabel("None selected")
        self.current_plugin_label.setStyleSheet("color: #007acc; font-style: italic;")
        layout.addWidget(self.current_plugin_label)
        
        # Available plugins
        layout.addWidget(QLabel("Available Plugins:"))
        
        self.plugins_list = QListWidget()
        self.plugins_list.itemClicked.connect(self._on_plugin_selected)
        layout.addWidget(self.plugins_list)
        
        return panel
        
    def set_project(self, project):
        """Set current project"""
        self.current_project = project
        self._refresh_plugins_list()
        
        # Update current plugin display
        if project and project.current_plugin:
            self.current_plugin_label.setText(project.current_plugin)
            plugin_info = project.get_current_plugin_info()
            self.plugin_info_widget.set_plugin(plugin_info)
            self.generate_btn.setEnabled(plugin_info is not None)
        else:
            self.current_plugin_label.setText("None selected")
            self.plugin_info_widget.set_plugin(None)
            self.generate_btn.setEnabled(False)
            
    def _refresh_plugins_list(self):
        """Refresh the plugins list"""
        self.plugins_list.clear()
        
        if not self.current_project:
            return
            
        for plugin in self.current_project.plugin_manager.get_all_plugins():
            item = QListWidgetItem(f"{plugin.name} (v{plugin.version})")
            item.setData(Qt.ItemDataRole.UserRole, plugin.name)
            self.plugins_list.addItem(item)
            
    def _on_plugin_selected(self, item):
        """Handle plugin selection"""
        plugin_name = item.data(Qt.ItemDataRole.UserRole)
        if self.current_project and plugin_name:
            # Set as current plugin
            self.current_project.set_current_plugin(plugin_name)
            self.current_plugin_label.setText(plugin_name)
            
            # Update display
            plugin_info = self.current_project.get_current_plugin_info()
            self.plugin_info_widget.set_plugin(plugin_info)
            self.generate_btn.setEnabled(True)
            
            self.plugin_selected.emit(plugin_name)
            
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
                self._refresh_plugins_list()
                
                # Auto-select the imported plugin
                plugin_name = self.current_project.current_plugin
                if plugin_name:
                    self.current_plugin_label.setText(plugin_name)
                    plugin_info = self.current_project.get_current_plugin_info()
                    self.plugin_info_widget.set_plugin(plugin_info)
                    self.generate_btn.setEnabled(True)
                    
                self.plugin_imported.emit(plugin_name or "")
                
                QMessageBox.information(
                    self,
                    "Import Successful",
                    f"Plugin information imported successfully!\n\n"
                    f"Plugin: {plugin_info.name if plugin_info else 'Unknown'}\n"
                    f"Version: {plugin_info.version if plugin_info else 'Unknown'}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Import Failed",
                    "Failed to import plugin information. Please check the file format."
                )
