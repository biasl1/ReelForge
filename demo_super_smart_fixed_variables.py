#!/usr/bin/env python3
"""
Demo of the Super Smart AI Template Editor with Fixed Variables and AI Choices
Now includes:
- Fixed Variables that apply to ALL content types (reels, posts, stories, tutorials)
- AI Choice options for intro/outro (let AI decide)
- Fully scrollable window for complete usability
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt

# Import the updated template editor
from ui.template_editor import TemplateEditor as AITemplateEditor

class DemoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 Super Smart AI Template Editor - Fixed Variables & AI Choices Demo")
        self.setGeometry(100, 100, 1200, 800)
        
        # Set dark theme
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a1a1a;
                color: #ffffff;
            }
        """)
        
        # Create the template editor
        self.template_editor = AITemplateEditor()
        
        # Set up the central widget
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.template_editor)
        
        self.setCentralWidget(central_widget)
        
        print("🎯 SUPER SMART AI TEMPLATE EDITOR DEMO")
        print("=" * 60)
        print("✨ NEW FEATURES:")
        print("📌 Fixed Variables:")
        print("   • Set subtitle position once → applies to ALL content types")
        print("   • Set font size once → applies to reels, posts, stories, tutorials")
        print("   • AI respects these settings EVERYWHERE")
        print("")
        print("🤖 AI Choice System:")
        print("   • Let AI decide whether to include intro/outro")
        print("   • AI has complete creative freedom for these elements")
        print("")
        print("📜 Fully Scrollable Window:")
        print("   • Entire template editor is now scrollable")
        print("   • No more cutting off of controls")
        print("   • Perfect usability for all screen sizes")
        print("")
        print("🎨 INSTRUCTIONS:")
        print("1. Try the Fixed Variables section (orange)")
        print("2. Set subtitle position and watch it apply to ALL content types")
        print("3. Try the AI Choice checkboxes for intro/outro")
        print("4. Scroll up and down to see everything works perfectly")
        print("5. Save & Export to see the comprehensive configuration")
        print("=" * 60)

def main():
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    
    app = QApplication(sys.argv)
    
    # Set the application style for better cross-platform appearance
    app.setStyle('Fusion')
    
    # Create and show the demo window
    demo_window = DemoWindow()
    demo_window.show()
    
    print("🚀 Demo running! Test the new super smart features.")
    print("💡 The template editor now has:")
    print("   • Fixed variables for ALL content types")
    print("   • AI choice system for intro/outro")
    print("   • Perfect scrollable interface")
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
