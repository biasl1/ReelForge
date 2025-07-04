#!/usr/bin/env python3
"""
Moodboard Enhancement Demo
Shows the new moodboard preview and background functionality
"""

import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QTimer
from core.logging_config import log_info

def demo_moodboard_features():
    """Demo the enhanced moodboard functionality"""
    log_info("Starting Moodboard Enhancement Demo...")

    app = QApplication(sys.argv)

    # Import and create main window
    from ui.mainwindow import MainWindow
    window = MainWindow()
    window.show()

    # Show information about the new moodboard features
    def show_feature_info():
        QMessageBox.information(
            window,
            "🎨 Enhanced Moodboard Features",
            "NEW MOODBOARD ENHANCEMENTS:\n\n"
            "📸 PREVIEW: Uploaded moodboard images now show a preview\n"
            "🎨 BACKGROUND: Moodboard becomes a darker background theme for the 'Plugin Information' tab\n"
            "✨ VISUAL STYLE: Creates an immersive, branded experience\n\n"
            "HOW TO USE:\n"
            "1. Create or open a project\n"
            "2. Go to Plugin Dashboard (right panel)\n"
            "3. Scroll to 'Moodboard (Optional)' section\n"
            "4. Click 'Upload Image' to select your moodboard\n"
            "5. Watch the 'Plugin Information' tab transform!\n\n"
            "The moodboard will be saved with your project and automatically loaded when reopened."
        )

    # Show info after window loads
    QTimer.singleShot(1000, show_feature_info)

    log_info("🎨 Moodboard Enhancement Demo is ready!")
    log_info("Try uploading a moodboard image to see the new features in action!")

    return app.exec()

if __name__ == "__main__":
    sys.exit(demo_moodboard_features())
