"""
Main window for ReelForge application
Professional content creation interface
"""

from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QSplitter, QStatusBar, QLabel, QFrame, QTreeWidget,
    QTreeWidgetItem, QListWidget, QListWidgetItem, QMessageBox,
    QFileDialog, QApplication, QTextEdit, QPushButton,
    QGroupBox, QFormLayout, QLineEdit
)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QAction, QDragEnterEvent, QDropEvent

from core.project import ReelForgeProject, ProjectManager, AssetReference
from core.assets import AssetManager, FileInfo
from ui.menu import MenuManager
from ui.startup_dialog import StartupDialog


class AssetPanel(QWidget):
    """Asset management panel"""
    
    asset_selected = pyqtSignal(str)  # asset_id
    asset_imported = pyqtSignal(str)  # asset_id
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.asset_manager = AssetManager()
        
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup asset panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Project Assets")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)
        
        # Asset tree
        self.asset_tree = QTreeWidget()
        self.asset_tree.setHeaderLabels(["Name", "Type", "Size"])
        self.asset_tree.setRootIsDecorated(True)
        self.asset_tree.itemClicked.connect(self._on_asset_selected)
        layout.addWidget(self.asset_tree)
        
        # Import button
        import_button = QPushButton("Import Assets...")
        import_button.clicked.connect(self._import_assets)
        layout.addWidget(import_button)
        
        # Enable drag and drop
        self.setAcceptDrops(True)
        
    def set_project(self, project: ReelForgeProject):
        """Set current project"""
        self.current_project = project
        if project and project.project_directory:
            self.asset_manager.set_project_directory(project.project_directory)
        self._refresh_assets()
        
    def _refresh_assets(self):
        """Refresh asset tree"""
        self.asset_tree.clear()
        
        if not self.current_project:
            return
            
        # Group assets by type
        video_item = QTreeWidgetItem(["Video", "", ""])
        audio_item = QTreeWidgetItem(["Audio", "", ""])
        image_item = QTreeWidgetItem(["Images", "", ""])
        other_item = QTreeWidgetItem(["Other", "", ""])
        
        self.asset_tree.addTopLevelItem(video_item)
        self.asset_tree.addTopLevelItem(audio_item)
        self.asset_tree.addTopLevelItem(image_item)
        self.asset_tree.addTopLevelItem(other_item)
        
        # Add assets to appropriate categories
        for asset in self.current_project.get_all_assets():
            size_str = self.asset_manager.format_file_size(asset.file_size or 0)
            item = QTreeWidgetItem([asset.name, asset.file_type, size_str])
            item.setData(0, Qt.ItemDataRole.UserRole, asset.id)
            
            if asset.file_type == "video":
                video_item.addChild(item)
            elif asset.file_type == "audio":
                audio_item.addChild(item)
            elif asset.file_type == "image":
                image_item.addChild(item)
            else:
                other_item.addChild(item)
                
        # Expand all categories
        self.asset_tree.expandAll()
        
    def _on_asset_selected(self, item, column):
        """Handle asset selection"""
        asset_id = item.data(0, Qt.ItemDataRole.UserRole)
        if asset_id:
            self.asset_selected.emit(asset_id)
            
    def _import_assets(self):
        """Import assets dialog"""
        if not self.current_project:
            return
            
        file_paths, _ = QFileDialog.getOpenFileNames(
            self,
            "Import Assets",
            str(Path.home()),
            "Media Files (*.mp4 *.mov *.avi *.mp3 *.wav *.jpg *.png);;All Files (*)"
        )
        
        for file_path in file_paths:
            self._import_single_asset(Path(file_path))
            
    def _import_single_asset(self, file_path: Path):
        """Import a single asset"""
        try:
            # Validate file
            file_info = self.asset_manager.validate_file(file_path)
            if not file_info.is_supported:
                QMessageBox.warning(
                    self, 
                    "Unsupported Format",
                    f"The file format '{file_info.extension}' is not supported."
                )
                return
                
            # Copy to project directory
            copied_path = self.asset_manager.copy_asset_to_project(file_path)
            if not copied_path:
                QMessageBox.critical(
                    self,
                    "Import Failed", 
                    f"Failed to import asset: {file_path.name}"
                )
                return
                
            # Create asset reference
            asset_id = self.asset_manager.generate_asset_id(copied_path)
            relative_path = self.asset_manager.get_relative_path(copied_path)
            
            asset = AssetReference(
                id=asset_id,
                name=copied_path.name,
                file_path=relative_path,
                file_type=file_info.file_type,
                file_size=file_info.size
            )
            
            # Add to project
            if self.current_project.add_asset(asset):
                self._refresh_assets()
                self.asset_imported.emit(asset_id)
            else:
                QMessageBox.warning(
                    self,
                    "Asset Exists",
                    f"An asset with this name already exists in the project."
                )
                
        except Exception as e:
            QMessageBox.critical(
                self,
                "Import Error",
                f"Error importing asset: {e}"
            )
            
    def dragEnterEvent(self, event: QDragEnterEvent):
        """Handle drag enter event"""
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            
    def dropEvent(self, event: QDropEvent):
        """Handle drop event"""
        if not self.current_project:
            return
            
        for url in event.mimeData().urls():
            file_path = Path(url.toLocalFile())
            if file_path.is_file():
                self._import_single_asset(file_path)


class PropertiesPanel(QWidget):
    """Properties panel for selected items"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_asset = None
        self._setup_ui()
        
    def _setup_ui(self):
        """Setup properties panel UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("Properties")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(title)
        
        # Properties form
        self.properties_group = QGroupBox("Asset Properties")
        self.properties_layout = QFormLayout(self.properties_group)
        layout.addWidget(self.properties_group)
        
        # Initially empty
        self._show_empty_state()
        
        layout.addStretch()
        
    def _show_empty_state(self):
        """Show empty state when no asset selected"""
        self._clear_properties()
        label = QLabel("No asset selected")
        label.setStyleSheet("color: #969696; font-style: italic;")
        self.properties_layout.addRow(label)
        
    def _clear_properties(self):
        """Clear all property widgets"""
        while self.properties_layout.count():
            child = self.properties_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
    def show_asset_properties(self, asset: AssetReference):
        """Show properties for an asset"""
        self.current_asset = asset
        self._clear_properties()
        
        # Basic properties
        self.properties_layout.addRow("Name:", QLabel(asset.name))
        self.properties_layout.addRow("Type:", QLabel(asset.file_type.title()))
        
        if asset.file_size:
            size_str = AssetManager.format_file_size(asset.file_size)
            self.properties_layout.addRow("Size:", QLabel(size_str))
            
        self.properties_layout.addRow("Path:", QLabel(asset.file_path))
        
        # TODO: Add type-specific properties (dimensions, duration, etc.)


class MainWindow(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        
        # Initialize managers
        self.project_manager = ProjectManager()
        self.current_project: Optional[ReelForgeProject] = None
        
        self._setup_ui()
        self._setup_status_bar()
        self._setup_connections()
        
        # Window settings
        self.setWindowTitle("ReelForge")
        self.resize(1200, 800)
        
    def _setup_ui(self):
        """Setup main window UI"""
        # Central widget with splitter layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Main splitter
        main_splitter = QSplitter(Qt.Orientation.Horizontal)
        layout.addWidget(main_splitter)
        
        # Left panel - Assets
        self.asset_panel = AssetPanel()
        self.asset_panel.setMinimumWidth(250)
        self.asset_panel.setMaximumWidth(400)
        main_splitter.addWidget(self.asset_panel)
        
        # Center panel - Timeline/Canvas (placeholder)
        self.center_panel = self._create_center_panel()
        main_splitter.addWidget(self.center_panel)
        
        # Right panel - Properties
        self.properties_panel = PropertiesPanel()
        self.properties_panel.setMinimumWidth(200)
        self.properties_panel.setMaximumWidth(300)
        main_splitter.addWidget(self.properties_panel)
        
        # Set splitter proportions
        main_splitter.setSizes([300, 600, 250])
        
        # Setup menu bar
        self.menu_manager = MenuManager(self.menuBar(), self)
        
    def _create_center_panel(self) -> QWidget:
        """Create center panel placeholder"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)
        
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Welcome message
        welcome_label = QLabel("Welcome to ReelForge")
        welcome_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #cccccc;")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(welcome_label)
        
        subtitle = QLabel("Create a new project or open an existing one to get started")
        subtitle.setStyleSheet("font-size: 14px; color: #969696;")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitle)
        
        layout.addStretch()
        
        # TODO: Replace with timeline/canvas when implemented
        placeholder = QLabel("Timeline and Canvas will be implemented here")
        placeholder.setStyleSheet("color: #656565; font-style: italic;")
        placeholder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(placeholder)
        
        layout.addStretch()
        
        return panel
        
    def _setup_status_bar(self):
        """Setup status bar"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        
        # Project status label
        self.project_status_label = QLabel("No project loaded")
        self.status_bar.addWidget(self.project_status_label)
        
        # Add permanent widgets on the right
        self.status_bar.addPermanentWidget(QLabel("Ready"))
        
    def _setup_connections(self):
        """Setup signal connections"""
        # Menu connections
        self.menu_manager.new_project_requested.connect(self._new_project)
        self.menu_manager.open_project_requested.connect(self._open_project)
        self.menu_manager.save_project_requested.connect(self._save_project)
        self.menu_manager.save_as_project_requested.connect(self._save_project_as)
        self.menu_manager.exit_requested.connect(self.close)
        self.menu_manager.about_requested.connect(self._show_about)
        
        # Asset panel connections
        self.asset_panel.asset_selected.connect(self._on_asset_selected)
        self.asset_panel.asset_imported.connect(self._on_asset_imported)
        
    def load_project_data(self, project_data: Dict[str, Any]):
        """Load project from startup dialog data"""
        if project_data["type"] == "existing":
            self.current_project = project_data["project"]
        elif project_data["type"] == "new":
            self.current_project = project_data["project"]
            
        self._update_ui_for_project()
        
    def _new_project(self):
        """Create new project"""
        dialog = StartupDialog(self)
        if dialog.exec() == StartupDialog.DialogCode.Accepted:
            project_data = dialog.get_project_data()
            if project_data:
                self.load_project_data(project_data)
                
    def _open_project(self, file_path: str):
        """Open existing project"""
        project = ReelForgeProject.load(Path(file_path))
        if project:
            self.current_project = project
            self.project_manager.add_recent_project(file_path)
            self._update_ui_for_project()
        else:
            QMessageBox.critical(
                self,
                "Error Loading Project",
                f"Failed to load project from: {file_path}"
            )
            
    def _save_project(self):
        """Save current project"""
        if not self.current_project:
            return
            
        if self.current_project.save():
            self.status_bar.showMessage("Project saved", 2000)
        else:
            QMessageBox.critical(
                self,
                "Save Error",
                "Failed to save the project"
            )
            
    def _save_project_as(self):
        """Save project with new name"""
        if not self.current_project:
            return
            
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Project As",
            str(Path.home() / f"{self.current_project.project_name}.rforge"),
            "ReelForge Projects (*.rforge)"
        )
        
        if file_path:
            if self.current_project.save(Path(file_path)):
                self.project_manager.add_recent_project(file_path)
                self._update_window_title()
                self.status_bar.showMessage("Project saved", 2000)
            else:
                QMessageBox.critical(
                    self,
                    "Save Error", 
                    "Failed to save the project"
                )
                
    def _update_ui_for_project(self):
        """Update UI when project changes"""
        if self.current_project:
            # Update panels
            self.asset_panel.set_project(self.current_project)
            
            # Update menu
            self.menu_manager.set_current_project(self.current_project)
            self.menu_manager.update_recent_projects(
                self.project_manager.get_recent_projects()
            )
            
            # Update status and title
            self._update_window_title()
            self._update_status_bar()
            
    def _update_window_title(self):
        """Update window title"""
        if self.current_project:
            title = f"ReelForge - {self.current_project.project_name}"
            if self.current_project.is_modified:
                title += " *"
            self.setWindowTitle(title)
        else:
            self.setWindowTitle("ReelForge")
            
    def _update_status_bar(self):
        """Update status bar"""
        if self.current_project:
            asset_count = len(self.current_project.get_all_assets())
            self.project_status_label.setText(
                f"Project: {self.current_project.project_name} | Assets: {asset_count}"
            )
        else:
            self.project_status_label.setText("No project loaded")
            
    def _on_asset_selected(self, asset_id: str):
        """Handle asset selection"""
        if self.current_project:
            asset = self.current_project.get_asset(asset_id)
            if asset:
                self.properties_panel.show_asset_properties(asset)
                
    def _on_asset_imported(self, asset_id: str):
        """Handle asset import"""
        self._update_status_bar()
        
    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ReelForge",
            "ReelForge v1.0.0\\n\\n"
            "Professional Content Creation Tool\\n"
            "Built with PyQt6\\n\\n"
            "© 2025 Artists in DSP"
        )
        
    def closeEvent(self, event):
        """Handle window close event"""
        if self.current_project and self.current_project.is_modified:
            reply = QMessageBox.question(
                self,
                "Unsaved Changes",
                "The project has unsaved changes. Do you want to save before closing?",
                QMessageBox.StandardButton.Save | 
                QMessageBox.StandardButton.Discard | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Save:
                if not self._save_project():
                    event.ignore()
                    return
            elif reply == QMessageBox.StandardButton.Cancel:
                event.ignore()
                return
                
        event.accept()
