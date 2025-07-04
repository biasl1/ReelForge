#!/usr/bin/env python3
"""
IMMEDIATE UX IMPROVEMENTS DEMO - WORKING NOW!
Shows the new UX features in ReelTune
"""

import sys
import os
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QMessageBox
from PyQt6.QtCore import QTimer
from ui.ux_improvements import QuickActionToolbar, AutoSaveIndicator, ProjectProgressIndicator, ContentTypeTemplates
from core.logging_config import log_info


class UXDemoWindow(QMainWindow):
    """Demo window showing UX improvements"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 ReelTune UX Improvements DEMO")
        self.setGeometry(100, 100, 800, 600)
        self.setup_ui()

    def setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        # Quick Action Toolbar
        self.quick_toolbar = QuickActionToolbar()
        self.quick_toolbar.quick_event_requested.connect(self.on_quick_event)
        self.quick_toolbar.duplicate_event_requested.connect(self.on_duplicate)
        self.quick_toolbar.toggle_week_view.connect(self.on_toggle_view)
        layout.addWidget(self.quick_toolbar)

        # Status indicators
        status_layout = QHBoxLayout()

        # Auto-save indicator
        self.save_indicator = AutoSaveIndicator()
        status_layout.addWidget(self.save_indicator)

        # Progress indicator
        self.progress_indicator = ProjectProgressIndicator()
        status_layout.addWidget(self.progress_indicator)

        status_layout.addStretch()
        layout.addLayout(status_layout)

        # Demo info
        self.show_demo_info()

        # Auto-demo sequence
        self.start_demo_sequence()

    def on_quick_event(self, content_type):
        """Handle quick event creation"""
        template = ContentTypeTemplates.get_template(content_type, "Demo Plugin")
        log_info(f"✨ Quick event created: {content_type}")
        log_info(f"   Title: {template.get('title', 'N/A')}")
        log_info(f"   Platforms: {template.get('platforms', [])}")

        # Show visual feedback
        self.save_indicator.set_unsaved_changes()
        QTimer.singleShot(1000, self.save_indicator.set_saved)

    def on_duplicate(self):
        """Handle duplicate event"""
        log_info("📋 Duplicate event requested")

    def on_toggle_view(self):
        """Handle view toggle"""
        log_info("📅 Timeline view toggled")

    def start_demo_sequence(self):
        """Start automated demo sequence"""
        # Update progress over time
        QTimer.singleShot(2000, lambda: self.progress_indicator.update_progress(5, 1))
        QTimer.singleShot(4000, lambda: self.progress_indicator.update_progress(5, 3))
        QTimer.singleShot(6000, lambda: self.progress_indicator.update_progress(5, 5))

        # Show save states
        QTimer.singleShot(3000, self.save_indicator.set_saving)
        QTimer.singleShot(3500, self.save_indicator.set_saved)
        QTimer.singleShot(5000, self.save_indicator.set_unsaved_changes)
        QTimer.singleShot(7000, self.save_indicator.set_saved)

    def show_demo_info(self):
        """Show demo information"""
        info = """
🎉 UX IMPROVEMENTS DEMO ACTIVE!

✨ FEATURES TO TRY:
• Click emoji buttons: 📸🎬📱🎵🎓 (Quick event creation)
• Use keyboard shortcuts: Ctrl+1, Ctrl+2, Ctrl+3, Ctrl+4, Ctrl+5
• Watch the auto-save indicator change colors
• See project progress tracking in action

🎯 PRACTICAL IMPROVEMENTS:
• One-click event creation with smart templates
• Visual auto-save status with colored indicators
• Project progress tracking with percentage
• Professional status displays

📋 TRY THESE ACTIONS:
1. Click the 📸 button (Instagram Post)
2. Click the 🎬 button (Instagram Reel)
3. Press Ctrl+3 (Story template)
4. Click 📋 (Duplicate)
5. Click 📅 (Toggle view)

The demo will show automated progress updates!
        """

        msg = QMessageBox(self)
        msg.setWindowTitle("🚀 UX Demo Features")
        msg.setText(info)
        msg.setStyleSheet("""
            QMessageBox {
                background: #2B2B2B;
                color: #FFFFFF;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QMessageBox QPushButton {
                background: #3B3B3B;
                border: 1px solid #555;
                padding: 8px 15px;
                border-radius: 4px;
                color: #FFF;
                font-weight: bold;
            }
            QMessageBox QPushButton:hover {
                background: #4B4B4B;
                border-color: #777;
            }
        """)

        # Show after window is displayed
        QTimer.singleShot(500, msg.exec)


def main():
    """Run the UX improvements demo"""
    print("🚀 STARTING UX IMPROVEMENTS DEMO!")
    print("=" * 50)

    app = QApplication(sys.argv)

    # Apply dark theme
    app.setStyleSheet("""
        QMainWindow {
            background: #1E1E1E;
            color: #FFFFFF;
        }
        QWidget {
            background: #1E1E1E;
            color: #FFFFFF;
        }
    """)

    window = UXDemoWindow()
    window.show()

    print("✅ Demo window opened!")
    print("🎯 Try the quick action buttons and keyboard shortcuts!")
    print("⚡ Watch the status indicators change!")

    # Auto-close after 30 seconds
    QTimer.singleShot(30000, app.quit)

    return app.exec()


if __name__ == "__main__":
    try:
        main()
        print("✨ UX Demo completed successfully!")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        sys.exit(1)
