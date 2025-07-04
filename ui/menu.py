"""
Menu bar setup for ReelForge main window
"""

from PyQt6.QtWidgets import QMenuBar, QMenu, QFileDialog, QMessageBox
from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QAction, QKeySequence
from pathlib import Path

from core.project import ReelForgeProject


class MenuManager(QObject):
    """Manages the application menu bar"""

    # Signals
    new_project_requested = pyqtSignal()
    open_project_requested = pyqtSignal(str)  # file_path
    save_project_requested = pyqtSignal()
    save_as_project_requested = pyqtSignal()
    exit_requested = pyqtSignal()
    about_requested = pyqtSignal()

    def __init__(self, menu_bar: QMenuBar, parent=None):
        super().__init__(parent)
        self.menu_bar = menu_bar
        self.current_project = None

        self._create_menus()
        self._update_menu_states()

    def _create_menus(self):
        """Create all menus"""
        self._create_file_menu()
        self._create_edit_menu()
        self._create_view_menu()
        self._create_help_menu()

    def _create_file_menu(self):
        """Create File menu"""
        file_menu = self.menu_bar.addMenu("File")

        # New Project
        self.new_action = QAction("New Project...", self)
        self.new_action.setShortcut(QKeySequence.StandardKey.New)
        self.new_action.setStatusTip("Create a new project")
        self.new_action.triggered.connect(self.new_project_requested)
        file_menu.addAction(self.new_action)

        file_menu.addSeparator()

        # Open Project
        self.open_action = QAction("Open Project...", self)
        self.open_action.setShortcut(QKeySequence.StandardKey.Open)
        self.open_action.setStatusTip("Open an existing project")
        self.open_action.triggered.connect(self._open_project)
        file_menu.addAction(self.open_action)

        # Recent Projects submenu
        self.recent_menu = file_menu.addMenu("Open Recent")
        self._update_recent_menu()

        file_menu.addSeparator()

        # Save Project
        self.save_action = QAction("Save Project", self)
        self.save_action.setShortcut(QKeySequence.StandardKey.Save)
        self.save_action.setStatusTip("Save the current project")
        self.save_action.triggered.connect(self.save_project_requested)
        file_menu.addAction(self.save_action)

        # Save As
        self.save_as_action = QAction("Save Project As...", self)
        self.save_as_action.setShortcut(QKeySequence.StandardKey.SaveAs)
        self.save_as_action.setStatusTip("Save the project with a new name")
        self.save_as_action.triggered.connect(self.save_as_project_requested)
        file_menu.addAction(self.save_as_action)

        file_menu.addSeparator()

        # Exit
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.setStatusTip("Exit ReelForge")
        exit_action.triggered.connect(self.exit_requested)
        file_menu.addAction(exit_action)

    def _create_edit_menu(self):
        """Create Edit menu"""
        edit_menu = self.menu_bar.addMenu("Edit")

        # Undo
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.setStatusTip("Undo the last action")
        undo_action.setEnabled(False)  # TODO: Implement undo/redo
        edit_menu.addAction(undo_action)

        # Redo
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.setStatusTip("Redo the last undone action")
        redo_action.setEnabled(False)  # TODO: Implement undo/redo
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        # Cut, Copy, Paste
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.setEnabled(False)  # TODO: Implement clipboard
        edit_menu.addAction(cut_action)

        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.setEnabled(False)  # TODO: Implement clipboard
        edit_menu.addAction(copy_action)

        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.setEnabled(False)  # TODO: Implement clipboard
        edit_menu.addAction(paste_action)

    def _create_view_menu(self):
        """Create View menu"""
        view_menu = self.menu_bar.addMenu("View")

        # Toggle panels
        assets_action = QAction("Assets Panel", self)
        assets_action.setCheckable(True)
        assets_action.setChecked(True)
        assets_action.setStatusTip("Toggle assets panel visibility")
        view_menu.addAction(assets_action)

        properties_action = QAction("Properties Panel", self)
        properties_action.setCheckable(True)
        properties_action.setChecked(True)
        properties_action.setStatusTip("Toggle properties panel visibility")
        view_menu.addAction(properties_action)

        view_menu.addSeparator()

        # Zoom
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.setEnabled(False)  # TODO: Implement zoom
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.setEnabled(False)  # TODO: Implement zoom
        view_menu.addAction(zoom_out_action)

        zoom_fit_action = QAction("Zoom to Fit", self)
        zoom_fit_action.setShortcut("Ctrl+0")
        zoom_fit_action.setEnabled(False)  # TODO: Implement zoom
        view_menu.addAction(zoom_fit_action)

    def _create_help_menu(self):
        """Create Help menu"""
        help_menu = self.menu_bar.addMenu("Help")

        # About
        about_action = QAction("About ReelForge", self)
        about_action.setStatusTip("About ReelForge")
        about_action.triggered.connect(self.about_requested)
        help_menu.addAction(about_action)

        # Documentation (placeholder)
        docs_action = QAction("Documentation", self)
        docs_action.setStatusTip("Open documentation")
        docs_action.setEnabled(False)  # TODO: Add documentation
        help_menu.addAction(docs_action)

    def _open_project(self):
        """Open project file dialog"""
        file_path, _ = QFileDialog.getOpenFileName(
            self.menu_bar,
            "Open ReelForge Project",
            str(Path.home()),
            "ReelForge Projects (*.rforge);;All Files (*)"
        )

        if file_path:
            self.open_project_requested.emit(file_path)

    def _update_recent_menu(self):
        """Update recent projects menu"""
        self.recent_menu.clear()

        # TODO: Get recent projects from project manager
        # For now, add placeholder
        no_recent_action = QAction("No recent projects", self)
        no_recent_action.setEnabled(False)
        self.recent_menu.addAction(no_recent_action)

    def set_current_project(self, project: ReelForgeProject):
        """Set the current project"""
        self.current_project = project
        self._update_menu_states()

    def _update_menu_states(self):
        """Update menu item enabled states based on current project"""
        has_project = self.current_project is not None

        # File menu states
        self.save_action.setEnabled(has_project)
        self.save_as_action.setEnabled(has_project)

    def update_recent_projects(self, recent_projects):
        """Update recent projects menu with new list"""
        self.recent_menu.clear()

        if not recent_projects:
            no_recent_action = QAction("No recent projects", self)
            no_recent_action.setEnabled(False)
            self.recent_menu.addAction(no_recent_action)
            return

        for project_path in recent_projects[:10]:  # Show max 10 recent
            path = Path(project_path)
            action = QAction(path.stem, self)
            action.setStatusTip(str(path))
            action.triggered.connect(lambda checked, p=project_path: self.open_project_requested.emit(p))
            self.recent_menu.addAction(action)
