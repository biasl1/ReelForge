"""
Main window for ReelTune application
Professional content creation interface
"""

from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

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
from core.content_generation import ContentGenerationManager, ConfigMode
from ui.menu import MenuManager
from ui.startup_dialog import StartupDialog
from ui.timeline.canvas import TimelineCanvas
from ui.timeline.controls import TimelineControls
from ui.timeline.event_dialog import EventDialog
from ui.plugin_dashboard import PluginDashboard
from ui.enhanced_asset_panel import EnhancedAssetPanel
from ui.template_editor import TemplateEditor


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
        self.setWindowTitle("ReelTune")
        self.resize(1400, 900)  # Increased size for plugin dashboard

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

        # Left panel - Enhanced Assets with Thumbnails
        self.asset_panel = EnhancedAssetPanel()
        self.asset_panel.setMinimumWidth(300)
        self.asset_panel.setMaximumWidth(450)
        main_splitter.addWidget(self.asset_panel)

        # Center panel - Timeline/Canvas (placeholder)
        self.center_panel = self._create_center_panel()
        main_splitter.addWidget(self.center_panel)

        # Right panel - Plugin Dashboard
        self.plugin_dashboard = PluginDashboard()
        self.plugin_dashboard.setMinimumWidth(350)
        self.plugin_dashboard.setMaximumWidth(500)
        main_splitter.addWidget(self.plugin_dashboard)
        
        # Pass template editor reference to plugin dashboard
        self.plugin_dashboard.set_template_editor(self.content_template_view)

        # Set splitter proportions
        main_splitter.setSizes([300, 600, 400])

        # Setup menu bar
        self.menu_manager = MenuManager(self.menuBar(), self)

    def _create_center_panel(self) -> QWidget:
        """Create center panel with timeline canvas and content template view"""
        panel = QFrame()
        panel.setFrameStyle(QFrame.Shape.StyledPanel)

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # View toggle controls
        toggle_frame = QFrame()
        toggle_frame.setMaximumHeight(50)
        toggle_layout = QHBoxLayout(toggle_frame)
        
        # View toggle buttons
        self.calendar_btn = QPushButton("📅 Calendar View")
        self.templates_btn = QPushButton("🎬 Content Templates")
        
        self.calendar_btn.setCheckable(True)
        self.templates_btn.setCheckable(True)
        self.calendar_btn.setChecked(True)  # Default to calendar
        
        # Style the buttons
        button_style = """
            QPushButton {
                padding: 8px 16px;
                border-radius: 4px;
                border: 2px solid #0078d4;
                background-color: white;
                font-weight: bold;
                font-size: 12px;
            }
            QPushButton:checked {
                background-color: #0078d4;
                color: white;
            }
            QPushButton:hover {
                background-color: #106ebe;
                color: white;
            }
        """
        self.calendar_btn.setStyleSheet(button_style)
        self.templates_btn.setStyleSheet(button_style)
        
        # Connect toggle buttons
        self.calendar_btn.clicked.connect(self._show_calendar_view)
        self.templates_btn.clicked.connect(self._show_template_view)
        
        toggle_layout.addWidget(QLabel("View:"))
        toggle_layout.addWidget(self.calendar_btn)
        toggle_layout.addWidget(self.templates_btn)
        toggle_layout.addStretch()
        
        layout.addWidget(toggle_frame)

        # Stacked widget to hold both views
        from PyQt6.QtWidgets import QStackedWidget
        self.stacked_widget = QStackedWidget()
        
        # Calendar view (original timeline)
        calendar_widget = QWidget()
        calendar_layout = QVBoxLayout(calendar_widget)
        calendar_layout.setContentsMargins(0, 0, 0, 0)
        calendar_layout.setSpacing(0)
        
        # Timeline controls
        self.timeline_controls = TimelineControls()
        calendar_layout.addWidget(self.timeline_controls)

        # Timeline canvas
        self.timeline_canvas = TimelineCanvas()
        calendar_layout.addWidget(self.timeline_canvas)
        
        # Content template view
        self.content_template_view = TemplateEditor()
        
        # Add both views to stacked widget
        self.stacked_widget.addWidget(calendar_widget)  # Index 0
        self.stacked_widget.addWidget(self.content_template_view)  # Index 1
        
        layout.addWidget(self.stacked_widget)

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
        self.asset_panel.assets_changed.connect(self._on_assets_changed)

        # Plugin dashboard connections
        self.plugin_dashboard.plugin_imported.connect(self._on_plugin_imported)

        # Timeline connections
        self.timeline_canvas.day_selected.connect(self._on_day_selected)
        self.timeline_canvas.day_double_clicked.connect(self._on_day_double_clicked)
        self.timeline_canvas.edit_event_requested.connect(self._on_edit_event_requested)
        self.timeline_canvas.delete_event_requested.connect(self._on_delete_event_requested)
        # Duration is now fixed to 4 weeks - no longer need duration_changed signal
        self.timeline_controls.start_date_changed.connect(self._on_timeline_start_date_changed)
        self.timeline_controls.previous_period.connect(self._on_timeline_previous)
        self.timeline_controls.next_period.connect(self._on_timeline_next)
        self.timeline_controls.today_clicked.connect(self._on_timeline_today)
        
        # Content template connections
        self.content_template_view.template_changed.connect(self._on_template_changed)

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
            "ReelTune Projects (*.rforge)"
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
            self.plugin_dashboard.set_project(self.current_project)

            # Initialize timeline if needed
            if not self.current_project.timeline_plan:
                self.current_project.initialize_timeline()

            # Initialize content generation manager if needed
            if not hasattr(self.current_project, 'content_generation_manager'):
                self.current_project.content_generation_manager = ContentGenerationManager()

            # Update content template view with project data
            self.content_template_view.set_project(self.current_project)

            # Update timeline
            self._update_timeline_display()

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
            title = f"ReelTune - {self.current_project.project_name}"
            if self.current_project.is_modified:
                title += " *"
            self.setWindowTitle(title)
        else:
            self.setWindowTitle("ReelTune")

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
                # Show asset details in status bar
                self.status_bar.showMessage(f"Selected: {asset.name} ({asset.file_type})", 3000)

    def _on_assets_changed(self):
        """Handle asset changes (add, delete, modify)"""
        self._update_status_bar()
        # Refresh timeline display in case events reference deleted assets
        self._update_timeline_display()

    def _on_plugin_imported(self, plugin_name: str):
        """Handle plugin import"""
        self._update_status_bar()
        self.status_bar.showMessage(f"Plugin '{plugin_name}' imported and ready for AI content generation", 3000)

    def _show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About ReelTune",
            "ReelTune v1.0.0\n\n"
            "Professional AI-Ready Content Creation Tool\n"
            "Plan, organize, and manage social media content\n"
            "with AI integration capabilities.\n\n"
            "Built with PyQt6\n\n"
            "© 2025 Artists in DSP"
        )

    # Timeline interaction methods
    def _on_day_selected(self, date):
        """Handle day selection in timeline"""
        # Could show events for this day in properties panel
        pass

    def _on_day_double_clicked(self, date):
        """Handle day double-click to create new event"""
        if not self.current_project:
            return

        # Create new event dialog (simplified for AI workflow)
        dialog = EventDialog(date, parent=self)
        dialog.event_created.connect(self._on_event_created)

        if dialog.exec() == EventDialog.DialogCode.Accepted:
            pass  # Handled by signals

    def _on_edit_event_requested(self, event):
        """Handle event edit request"""
        if not self.current_project:
            return

        # Parse date from event
        from datetime import datetime
        event_date = datetime.fromisoformat(event.date)

        # Open edit dialog
        dialog = EventDialog(event_date, event=event, parent=self)
        dialog.event_updated.connect(self._on_event_updated)

        if dialog.exec() == EventDialog.DialogCode.Accepted:
            pass  # Handled by signals

    def _on_delete_event_requested(self, event):
        """Handle event deletion request"""
        if not self.current_project:
            return

        reply = QMessageBox.question(
            self,
            "Delete Event",
            f"Are you sure you want to delete the event '{event.title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            if self.current_project.remove_release_event(event.id):
                self._update_timeline_display()
                self.status_bar.showMessage(f"Event '{event.title}' deleted", 2000)
            else:
                QMessageBox.warning(
                    self,
                    "Delete Failed",
                    "Failed to delete the event. Please try again."
                )

    # Duration is now fixed to 4 weeks - method no longer needed
    # def _on_timeline_duration_changed(self, weeks):
    #     """Handle timeline duration change - REMOVED: Duration is now fixed to 4 weeks"""
    #     pass

    def _on_timeline_start_date_changed(self, date):
        """Handle timeline start date change"""
        if self.current_project and self.current_project.timeline_plan:
            self.current_project.timeline_plan.start_date = date.date().isoformat()
            self.timeline_canvas.set_start_date(date)
            self.current_project.mark_modified()
            # Restore events after timeline rebuild
            self._delayed_event_update()

    def _on_timeline_previous(self):
        """Handle previous period navigation"""
        if self.current_project and self.current_project.timeline_plan:
            current_date = datetime.fromisoformat(self.current_project.timeline_plan.start_date)
            weeks = self.current_project.timeline_plan.duration_weeks
            new_date = current_date - timedelta(weeks=weeks)

            self.current_project.timeline_plan.start_date = new_date.date().isoformat()
            self.timeline_canvas.set_start_date(new_date)
            self.timeline_controls.set_start_date(new_date)
            self.current_project.mark_modified()
            # Restore events after timeline rebuild
            self._delayed_event_update()

    def _on_timeline_next(self):
        """Handle next period navigation"""
        if self.current_project and self.current_project.timeline_plan:
            current_date = datetime.fromisoformat(self.current_project.timeline_plan.start_date)
            weeks = self.current_project.timeline_plan.duration_weeks
            new_date = current_date + timedelta(weeks=weeks)

            self.current_project.timeline_plan.start_date = new_date.date().isoformat()
            self.timeline_canvas.set_start_date(new_date)
            self.timeline_controls.set_start_date(new_date)
            self.current_project.mark_modified()
            # Restore events after timeline rebuild
            self._delayed_event_update()

    def _on_timeline_today(self):
        """Handle today navigation"""
        if self.current_project and self.current_project.timeline_plan:
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())

            self.current_project.timeline_plan.start_date = monday.date().isoformat()
            self.timeline_canvas.set_start_date(monday)
            self.timeline_controls.set_start_date(monday)
            self.current_project.mark_modified()
            # Restore events after timeline rebuild
            self._delayed_event_update()

    def _on_event_created(self, event):
        """Handle new event creation"""
        if self.current_project:
            if self.current_project.add_release_event(event):
                self._update_timeline_display()
                self.status_bar.showMessage(f"Event '{event.title}' created", 2000)
            else:
                QMessageBox.warning(
                    self,
                    "Event Creation Failed",
                    "Failed to create the event. Please try again."
                )

    def _on_event_updated(self, event):
        """Handle event update"""
        if self.current_project:
            # Use the proper update method that handles date changes correctly
            if self.current_project.update_release_event(event):
                self._update_timeline_display()
                self.status_bar.showMessage(f"Event '{event.title}' updated", 2000)
            else:
                QMessageBox.warning(
                    self,
                    "Event Update Failed",
                    "Failed to update the event. Please try again."
                )

    def _update_timeline_display(self):
        """Update timeline canvas with current project events"""
        if not self.current_project or not self.current_project.timeline_plan:
            return

        # Temporarily disconnect signals to avoid loops
        self.timeline_controls.start_date_changed.disconnect()

        try:
            # Update timeline controls FIRST (this rebuilds the timeline canvas)
            timeline_plan = self.current_project.timeline_plan
            from datetime import datetime
            start_date = datetime.fromisoformat(timeline_plan.start_date)
            # Duration is now fixed to 4 weeks - no need to set duration
            self.timeline_controls.set_start_date(start_date)

            # Update canvas directly and ensure it's rebuilt - duration is always 4 weeks
            self.timeline_canvas.set_duration(4)
            self.timeline_canvas.set_start_date(start_date)

        finally:
            # Reconnect signals
            self.timeline_controls.start_date_changed.connect(self._on_timeline_start_date_changed)

        # Delay event update to ensure rebuild is complete
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(0, self._delayed_event_update)

    def _delayed_event_update(self):
        """Update events after timeline rebuild is complete"""
        if not self.current_project or not self.current_project.timeline_plan:
            return

        # Group events by date and update canvas
        events_by_date = {}
        for date_str, event_ids in self.current_project.timeline_plan.events.items():
            events = [
                self.current_project.release_events[event_id]
                for event_id in event_ids
                if event_id in self.current_project.release_events
            ]
            if events:
                events_by_date[date_str] = events

        # Update timeline canvas with events (after it's been rebuilt)
        self.timeline_canvas.update_events(events_by_date)

    def _show_calendar_view(self):
        """Switch to calendar view"""
        self.calendar_btn.setChecked(True)
        self.templates_btn.setChecked(False)
        self.stacked_widget.setCurrentIndex(0)
        
    def _show_template_view(self):
        """Switch to content template view"""
        self.calendar_btn.setChecked(False)
        self.templates_btn.setChecked(True)
        self.stacked_widget.setCurrentIndex(1)
        
    def _on_template_changed(self):
        """Handle template parameter changes"""
        print(f"Template changed signal received.")
        if self.current_project:
            self.current_project.mark_modified()
            self._update_status_bar()
