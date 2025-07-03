"""
Startup dialog for ReelForge application
Handles new project creation and opening existing projects
"""

import os
from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QFrame, QListWidget, QListWidgetItem, QFileDialog,
    QLineEdit, QTextEdit, QComboBox, QGroupBox, QFormLayout,
    QMessageBox, QWidget, QSizePolicy
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap, QIcon

from core.project import ProjectManager, ReelForgeProject
from core.utils import validate_project_name, safe_filename


class StartupDialog(QDialog):
    """Startup dialog for creating/opening projects"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ReelForge - Welcome")
        self.setModal(True)
        self.resize(800, 600)
        
        # Initialize project manager
        self.project_manager = ProjectManager()
        self.selected_project_path = None
        self.project_data = None
        
        self._setup_ui()
        self._load_recent_projects()
        
    def _setup_ui(self):
        """Setup the user interface"""
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Left panel - Recent projects
        self._create_left_panel(layout)
        
        # Right panel - New project
        self._create_right_panel(layout)
        
    def _create_left_panel(self, parent_layout):
        """Create left panel with recent projects"""
        left_frame = QFrame()
        left_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        left_frame.setFixedWidth(350)
        
        layout = QVBoxLayout(left_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Recent Projects")
        title.setFont(QFont("", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Recent projects list
        self.recent_list = QListWidget()
        self.recent_list.itemClicked.connect(self._on_recent_project_selected)
        self.recent_list.itemDoubleClicked.connect(self._on_recent_project_opened)
        layout.addWidget(self.recent_list)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.open_button = QPushButton("Open Selected")
        self.open_button.setEnabled(False)
        self.open_button.clicked.connect(self._open_selected_project)
        button_layout.addWidget(self.open_button)
        
        browse_button = QPushButton("Browse...")
        browse_button.clicked.connect(self._browse_for_project)
        button_layout.addWidget(browse_button)
        
        layout.addLayout(button_layout)
        
        parent_layout.addWidget(left_frame)
        
    def _create_right_panel(self, parent_layout):
        """Create right panel with new project options"""
        right_frame = QFrame()
        right_frame.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(right_frame)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Create New Project")
        title.setFont(QFont("", 16, QFont.Weight.Bold))
        layout.addWidget(title)
        
        # Project details form
        self._create_project_form(layout)
        
        # Project templates
        self._create_templates_section(layout)
        
        # Buttons
        self._create_action_buttons(layout)
        
        parent_layout.addWidget(right_frame)
        
    def _create_project_form(self, parent_layout):
        """Create project details form"""
        form_group = QGroupBox("Project Details")
        form_layout = QFormLayout(form_group)
        
        # Project name
        self.project_name_edit = QLineEdit()
        self.project_name_edit.setPlaceholderText("Enter project name...")
        self.project_name_edit.textChanged.connect(self._validate_form)
        form_layout.addRow("Name:", self.project_name_edit)
        
        # Project description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(80)
        self.description_edit.setPlaceholderText("Optional description...")
        form_layout.addRow("Description:", self.description_edit)
        
        # Location
        location_layout = QHBoxLayout()
        self.location_edit = QLineEdit()
        self.location_edit.setText(str(Path.home() / "Documents" / "ReelForge Projects"))
        location_layout.addWidget(self.location_edit)
        
        location_button = QPushButton("Browse")
        location_button.clicked.connect(self._browse_location)
        location_layout.addWidget(location_button)
        
        form_layout.addRow("Location:", location_layout)
        
        parent_layout.addWidget(form_group)
        
    def _create_templates_section(self, parent_layout):
        """Create project templates section"""
        templates_group = QGroupBox("Project Template")
        templates_layout = QVBoxLayout(templates_group)
        
        self.template_combo = QComboBox()
        templates = self.project_manager.get_project_templates()
        
        for name, template in templates.items():
            self.template_combo.addItem(
                f"{name} ({template['format']}, {template['fps']}fps)",
                template
            )
            
        templates_layout.addWidget(self.template_combo)
        
        # Template description
        self.template_description = QLabel()
        self.template_description.setWordWrap(True)
        self.template_description.setStyleSheet("color: #969696; font-style: italic;")
        templates_layout.addWidget(self.template_description)
        
        self.template_combo.currentTextChanged.connect(self._update_template_description)
        self._update_template_description()  # Initial update
        
        parent_layout.addWidget(templates_group)
        
    def _create_action_buttons(self, parent_layout):
        """Create action buttons"""
        parent_layout.addStretch()
        
        button_layout = QHBoxLayout()
        
        # Cancel button
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)
        
        button_layout.addStretch()
        
        # Create button
        self.create_button = QPushButton("Create Project")
        self.create_button.setDefault(True)
        self.create_button.setEnabled(False)
        self.create_button.clicked.connect(self._create_project)
        button_layout.addWidget(self.create_button)
        
        parent_layout.addLayout(button_layout)
        
    def _load_recent_projects(self):
        """Load recent projects into the list"""
        self.recent_list.clear()
        recent_projects = self.project_manager.get_recent_projects()
        
        if not recent_projects:
            item = QListWidgetItem("No recent projects")
            item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.recent_list.addItem(item)
            return
            
        for project_path in recent_projects:
            path = Path(project_path)
            item = QListWidgetItem(path.stem)
            item.setData(Qt.ItemDataRole.UserRole, str(path))
            item.setToolTip(str(path))
            self.recent_list.addItem(item)
            
    def _on_recent_project_selected(self, item):
        """Handle recent project selection"""
        if item.data(Qt.ItemDataRole.UserRole):
            self.selected_project_path = item.data(Qt.ItemDataRole.UserRole)
            self.open_button.setEnabled(True)
        else:
            self.selected_project_path = None
            self.open_button.setEnabled(False)
            
    def _on_recent_project_opened(self, item):
        """Handle recent project double-click"""
        if item.data(Qt.ItemDataRole.UserRole):
            self.selected_project_path = item.data(Qt.ItemDataRole.UserRole)
            self._open_selected_project()
            
    def _open_selected_project(self):
        """Open the selected recent project"""
        if not self.selected_project_path:
            return
            
        project_path = Path(self.selected_project_path)
        if not project_path.exists():
            QMessageBox.warning(
                self, 
                "Project Not Found",
                f"The project file could not be found:\\n{project_path}"
            )
            return
            
        project = ReelForgeProject.load(project_path)
        if project:
            self.project_data = {"type": "existing", "project": project}
            self.project_manager.add_recent_project(str(project_path))
            self.accept()
        else:
            QMessageBox.critical(
                self,
                "Error Loading Project", 
                f"Failed to load project from:\\n{project_path}"
            )
            
    def _browse_for_project(self):
        """Browse for existing project file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open ReelForge Project",
            str(Path.home()),
            "ReelForge Projects (*.rforge);;All Files (*)"
        )
        
        if file_path:
            project_path = Path(file_path)
            project = ReelForgeProject.load(project_path)
            
            if project:
                self.project_data = {"type": "existing", "project": project}
                self.project_manager.add_recent_project(str(project_path))
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error Loading Project",
                    f"Failed to load project from:\\n{project_path}"
                )
                
    def _browse_location(self):
        """Browse for project location"""
        directory = QFileDialog.getExistingDirectory(
            self,
            "Select Project Location",
            self.location_edit.text()
        )
        
        if directory:
            self.location_edit.setText(directory)
            
    def _validate_form(self):
        """Validate the project form"""
        name = self.project_name_edit.text().strip()
        is_valid, _ = validate_project_name(name)
        self.create_button.setEnabled(is_valid)
        
    def _update_template_description(self):
        """Update template description"""
        current_data = self.template_combo.currentData()
        if current_data:
            self.template_description.setText(current_data.get("description", ""))
            
    def _create_project(self):
        """Create new project"""
        # Validate input
        name = self.project_name_edit.text().strip()
        is_valid, error_msg = validate_project_name(name)
        
        if not is_valid:
            QMessageBox.warning(self, "Invalid Project Name", error_msg)
            return
            
        # Get form data
        description = self.description_edit.toPlainText().strip()
        location = Path(self.location_edit.text().strip())
        template_data = self.template_combo.currentData()
        
        # Validate location
        if not location.exists():
            try:
                location.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(
                    self,
                    "Invalid Location",
                    f"Cannot create directory:\\n{location}\\n\\nError: {e}"
                )
                return
                
        # Create project
        try:
            project = ReelForgeProject()
            safe_name = safe_filename(name)
            
            success = project.create_new(
                name=name,
                location=location,
                description=description,
                format_preset=template_data.get("format", "1920x1080")
            )
            
            if success:
                self.project_data = {"type": "new", "project": project}
                self.project_manager.add_recent_project(str(project.project_file_path))
                self.accept()
            else:
                QMessageBox.critical(
                    self,
                    "Error Creating Project",
                    "Failed to create the project. Please check the location and try again."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Creating Project",
                f"An error occurred while creating the project:\\n{e}"
            )
            
    def get_project_data(self) -> Optional[Dict[str, Any]]:
        """Get project data from dialog"""
        return self.project_data
