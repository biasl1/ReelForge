"""
Enhanced Asset Management Panel
Professional asset management with descriptions, folders, and deletion
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, 
    QScrollArea, QFrame, QGridLayout, QMessageBox, QFileDialog,
    QApplication, QSizePolicy, QLineEdit, QTextEdit, QComboBox,
    QMenu, QDialog, QDialogButtonBox, QFormLayout, QTreeWidget,
    QTreeWidgetItem, QSplitter, QGroupBox
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize, QThread, pyqtSlot
from PyQt6.QtGui import QPixmap, QPainter, QBrush, QColor, QFont, QIcon, QPen, QAction
from pathlib import Path
from typing import Optional, List
import subprocess
from core.logging_config import log_info, log_error, log_warning, log_debug
from core.project import AssetReference
import tempfile
import os


class AssetDescriptionDialog(QDialog):
    """Dialog for editing asset description and folder"""
    
    def __init__(self, asset: AssetReference, available_folders: List[str], parent=None):
        super().__init__(parent)
        self.asset = asset
        self.available_folders = available_folders
        self.setWindowTitle(f"Edit Asset: {asset.name}")
        self.setModal(True)
        self.resize(400, 300)
        
        self._setup_ui()
        self._load_data()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        
        # Form layout
        form_layout = QFormLayout()
        
        # Asset name (read-only)
        name_label = QLabel(self.asset.name)
        name_label.setStyleSheet("font-weight: bold; color: #007acc;")
        form_layout.addRow("Asset Name:", name_label)
        
        # File type (read-only)
        type_label = QLabel(self.asset.file_type.upper())
        form_layout.addRow("Type:", type_label)
        
        # Folder selection
        self.folder_combo = QComboBox()
        self.folder_combo.setEditable(True)
        self.folder_combo.addItem("")  # No folder option
        self.folder_combo.addItems(self.available_folders)
        form_layout.addRow("Folder:", self.folder_combo)
        
        # Description
        self.description_edit = QTextEdit()
        self.description_edit.setMaximumHeight(120)
        self.description_edit.setPlaceholderText("Add description to help AI understand this asset...")
        form_layout.addRow("Description:", self.description_edit)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def _load_data(self):
        """Load current asset data"""
        self.folder_combo.setCurrentText(self.asset.folder)
        self.description_edit.setPlainText(self.asset.description)
        
    def get_folder(self) -> str:
        """Get selected folder"""
        return self.folder_combo.currentText().strip()
        
    def get_description(self) -> str:
        """Get description text"""
        return self.description_edit.toPlainText().strip()


class AssetCard(QFrame):
    """Individual asset card with thumbnail, info, and controls"""
    
    edit_requested = pyqtSignal(str)  # asset_id
    delete_requested = pyqtSignal(str)  # asset_id
    clicked = pyqtSignal(str)  # asset_id
    
    def __init__(self, asset: AssetReference, parent=None):
        super().__init__(parent)
        self.asset = asset
        self.setFixedSize(200, 280)
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.setStyleSheet("""
            AssetCard {
                background-color: #3c3c3c;
                border: 1px solid #555555;
                border-radius: 8px;
            }
            AssetCard:hover {
                background-color: #4a4a4a;
                border: 1px solid #007acc;
            }
        """)
        
        self._setup_ui()
        self._load_thumbnail()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)
        
        # Thumbnail area
        self.thumbnail_label = QLabel()
        self.thumbnail_label.setFixedSize(180, 120)
        self.thumbnail_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 1px solid #666;
                border-radius: 4px;
                background-color: #2a2a2a;
            }
        """)
        layout.addWidget(self.thumbnail_label)
        
        # Asset name
        name_label = QLabel(self.asset.name)
        name_label.setWordWrap(True)
        name_label.setStyleSheet("font-weight: bold; color: #cccccc;")
        name_label.setMaximumHeight(40)
        layout.addWidget(name_label)
        
        # Asset info
        info_text = f"{self.asset.file_type.upper()}"
        if self.asset.folder:
            info_text += f" • {self.asset.folder}"
        info_label = QLabel(info_text)
        info_label.setStyleSheet("color: #999999; font-size: 10px;")
        layout.addWidget(info_label)
        
        # Description preview
        if self.asset.description:
            desc_preview = self.asset.description[:50] + "..." if len(self.asset.description) > 50 else self.asset.description
            desc_label = QLabel(desc_preview)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet("color: #bbbbbb; font-size: 9px; font-style: italic;")
            desc_label.setMaximumHeight(30)
            layout.addWidget(desc_label)
        
        # Control buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(4)
        
        edit_btn = QPushButton("Edit")
        edit_btn.setFixedHeight(24)
        edit_btn.clicked.connect(lambda: self.edit_requested.emit(self.asset.id))
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete")
        delete_btn.setFixedHeight(24)
        delete_btn.setStyleSheet("QPushButton { background-color: #cc4444; }")
        delete_btn.clicked.connect(lambda: self.delete_requested.emit(self.asset.id))
        button_layout.addWidget(delete_btn)
        
        layout.addLayout(button_layout)
        
    def _load_thumbnail(self):
        """Load or generate thumbnail"""
        # Simple placeholder for now - can be enhanced later
        self.thumbnail_label.setText(f"{self.asset.file_type.upper()}\nFile")
        self.thumbnail_label.setStyleSheet("""
            QLabel {
                border: 1px solid #666;
                border-radius: 4px;
                background-color: #2a2a2a;
                color: #999;
                font-size: 12px;
            }
        """)
        
    def mousePressEvent(self, event):
        """Handle mouse click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.asset.id)
        super().mousePressEvent(event)


class AssetManagementPanel(QWidget):
    """Enhanced asset management panel with folders and descriptions"""
    
    asset_selected = pyqtSignal(str)  # asset_id
    assets_changed = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_project = None
        self.current_folder_filter = ""  # Empty = show all
        
        self._setup_ui()
        
    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(10)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("Asset Management")
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #cccccc;")
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add asset button
        add_btn = QPushButton("Add Assets")
        add_btn.clicked.connect(self._add_assets)
        header_layout.addWidget(add_btn)
        
        # Create folder button
        folder_btn = QPushButton("New Folder")
        folder_btn.clicked.connect(self._create_folder)
        header_layout.addWidget(folder_btn)
        
        layout.addLayout(header_layout)
        
        # Folder filter
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Show:"))
        
        self.folder_filter = QComboBox()
        self.folder_filter.currentTextChanged.connect(self._on_folder_filter_changed)
        filter_layout.addWidget(self.folder_filter)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Asset grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.asset_container = QWidget()
        self.asset_grid = QGridLayout(self.asset_container)
        self.asset_grid.setSpacing(10)
        
        scroll_area.setWidget(self.asset_container)
        layout.addWidget(scroll_area)
        
    def set_project(self, project):
        """Set current project"""
        self.current_project = project
        self._refresh_folder_filter()
        self._refresh_assets()
        
    def _refresh_folder_filter(self):
        """Refresh folder filter dropdown"""
        self.folder_filter.blockSignals(True)
        self.folder_filter.clear()
        
        self.folder_filter.addItem("All Assets", "")
        self.folder_filter.addItem("No Folder", "none")
        
        if self.current_project:
            folders = self.current_project.get_asset_folders()
            for folder in folders:
                self.folder_filter.addItem(folder, folder)
                
        self.folder_filter.blockSignals(False)
        
    def _on_folder_filter_changed(self, text):
        """Handle folder filter change"""
        current_data = self.folder_filter.currentData()
        if current_data is not None:
            self.current_folder_filter = current_data
            self._refresh_assets()
        
    def _refresh_assets(self):
        """Refresh asset display"""
        # Clear existing assets
        while self.asset_grid.count():
            child = self.asset_grid.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        if not self.current_project:
            return
            
        # Get filtered assets
        if self.current_folder_filter == "":
            assets = self.current_project.get_all_assets()
        elif self.current_folder_filter == "none":
            assets = self.current_project.get_assets_without_folder()
        else:
            assets = self.current_project.get_assets_in_folder(self.current_folder_filter)
            
        # Create asset cards
        cols = 3  # Number of columns
        for i, asset in enumerate(assets):
            row = i // cols
            col = i % cols
            
            card = AssetCard(asset)
            card.edit_requested.connect(self._edit_asset)
            card.delete_requested.connect(self._delete_asset)
            card.clicked.connect(lambda asset_id: self.asset_selected.emit(asset_id))
            
            self.asset_grid.addWidget(card, row, col)
            
    def _add_assets(self):
        """Add new assets"""
        if not self.current_project:
            QMessageBox.warning(self, "No Project", "Please open a project first.")
            return
            
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Select Asset Files",
            str(Path.home()),
            "All Supported (*.mp4 *.mov *.avi *.mp3 *.wav *.jpg *.png);;All Files (*)"
        )
        
        if files:
            # TODO: Implement asset import logic
            QMessageBox.information(self, "Import", f"Would import {len(files)} files")
            
    def _create_folder(self):
        """Create new folder"""
        from PyQt6.QtWidgets import QInputDialog
        
        folder_name, ok = QInputDialog.getText(
            self,
            "New Folder",
            "Enter folder name:",
            QLineEdit.EchoMode.Normal
        )
        
        if ok and folder_name.strip():
            # Folder will be created when assets are moved to it
            QMessageBox.information(self, "Folder", f"Folder '{folder_name}' will be created when assets are added to it.")
            
    def _edit_asset(self, asset_id: str):
        """Edit asset description and folder"""
        if not self.current_project or asset_id not in self.current_project.assets:
            return
            
        asset = self.current_project.assets[asset_id]
        available_folders = self.current_project.get_asset_folders()
        
        dialog = AssetDescriptionDialog(asset, available_folders, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update asset
            new_folder = dialog.get_folder()
            new_description = dialog.get_description()
            
            self.current_project.update_asset_folder(asset_id, new_folder)
            self.current_project.update_asset_description(asset_id, new_description)
            
            # Refresh display
            self._refresh_folder_filter()
            self._refresh_assets()
            self.assets_changed.emit()
            
    def _delete_asset(self, asset_id: str):
        """Delete asset"""
        if not self.current_project or asset_id not in self.current_project.assets:
            return
            
        asset = self.current_project.assets[asset_id]
        
        reply = QMessageBox.question(
            self,
            "Delete Asset",
            f"Are you sure you want to delete '{asset.name}'?\n\nThis will remove the asset from all events and delete the file.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.current_project.delete_asset(asset_id):
                self._refresh_folder_filter()
                self._refresh_assets()
                self.assets_changed.emit()
                QMessageBox.information(self, "Deleted", f"Asset '{asset.name}' has been deleted.")
            else:
                QMessageBox.critical(self, "Error", "Failed to delete asset.")


# For backward compatibility, create an alias
EnhancedAssetPanel = AssetManagementPanel
