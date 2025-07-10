#!/usr/bin/env python3
"""
ReelTune - Professional AI-Ready Content Creation Tool

A professional content planning and asset management tool designed for social media
content creation with AI integration capabilities.

Author: Assistant
License: MIT
Version: 1.0.0
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from core.logging_config import log_info, log_error, log_warning, log_debug
from ui.startup_dialog import StartupDialog
from ui.mainwindow import MainWindow
from ui.style_utils import get_app_stylesheet


class ReelTuneApp(QApplication):
    """Main application class for ReelTune"""

    def __init__(self, argv):
        super().__init__(argv)

        # Application metadata
        self.setApplicationName("ReelTune")
        self.setApplicationVersion("1.2.0")
        self.setOrganizationName("Artists in DSP")
        self.setOrganizationDomain("artistsindsp.com")

        # High DPI support is enabled by default in PyQt6
        # No need to set attributes manually

        # Set application icon (if available)
        # self.setWindowIcon(QIcon(":/icons/app_icon.png"))

        # Apply dark theme
        self.setStyleSheet(get_app_stylesheet())

        self.main_window = None
        self.startup_dialog = None

    def start(self):
        """Start the application with startup dialog"""
        self.startup_dialog = StartupDialog()

        # Show startup dialog and get result
        if self.startup_dialog.exec():
            # Dialog was accepted - get project data
            project_data = self.startup_dialog.get_project_data()
            if project_data:
                self.open_main_window_with_project_data(project_data)
                return True
            else:
                return False
        else:
            # Dialog was cancelled
            return False

    def open_main_window_with_project_data(self, project_data):
        """Open main window with project data from startup dialog"""
        try:
            # Close startup dialog
            if self.startup_dialog:
                self.startup_dialog.close()
                self.startup_dialog = None

            # Create and show main window
            self.main_window = MainWindow()

            # Load the project data
            self.main_window.load_project_data(project_data)

            # Show the window
            self.main_window.show()

        except Exception as e:
            log_error(f"Error opening main window: {e}")
            sys.exit(1)


def main():
    """Main entry point"""
    try:
        # Create application instance
        app = ReelTuneApp(sys.argv)

        # Start the application
        if app.start():
            # Run the event loop
            sys.exit(app.exec())
        else:
            # User cancelled startup
            sys.exit(0)

    except Exception as e:
        import traceback
        log_error(f"Fatal error: {e}")
        log_error(f"Full traceback: {traceback.format_exc()}")
        sys.exit(1)


if __name__ == "__main__":
    main()