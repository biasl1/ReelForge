#!/usr/bin/env python3
"""
🚀 SUPER SMART AI TEMPLATE EDITOR DEMO
========================================

This demo showcases the fully refined AI Template Editor - a "super smart, nice program"
that demonstrates perfect integration, unified save/export functionality, and intelligent
user interaction patterns.

Features Demonstrated:
- Beautiful, professional UI with modern styling
- Smart template validation with comprehensive feedback
- Unified save & export functionality
- Intelligent AI prompt generation
- Real-time preview with drag-and-drop timeline
- Smart user override patterns (user actions always override AI)
- Contextual help and feedback systems
- Professional error handling and messaging

Run this demo to see the ReelTune AI Template Editor in action!
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QHBoxLayout, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Import our super smart AI Template Editor
from ui.ai_template_editor import AITemplateEditor

class MockProject:
    """Mock project class for demo purposes"""
    def __init__(self):
        self.ai_templates = {}
        self.name = "Demo ReelTune Project"
        self.assets = [
            {"id": "intro_logo", "name": "Company Logo Animation", "type": "video"},
            {"id": "outro_cta", "name": "Call to Action Overlay", "type": "image"},
            {"id": "bg_music", "name": "Background Music", "type": "audio"},
            {"id": "brand_watermark", "name": "Brand Watermark", "type": "image"}
        ]

class SuperSmartDemoWindow(QMainWindow):
    """Demo window showcasing the Super Smart AI Template Editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🚀 ReelTune Super Smart AI Template Editor - Demo")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create mock project
        self.project = MockProject()
        
        self._setup_ui()
        self._apply_professional_styling()
        
    def _setup_ui(self):
        """Setup the demo UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Demo header
        self._create_demo_header(main_layout)
        
        # Main AI Template Editor
        self.template_editor = AITemplateEditor()
        self.template_editor.set_project(self.project)
        main_layout.addWidget(self.template_editor)
        
        # Demo footer with instructions
        self._create_demo_footer(main_layout)
        
    def _create_demo_header(self, layout):
        """Create demo header with title and description"""
        header_frame = QWidget()
        header_frame.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #0078d4, stop:1 #52c759);
                border-radius: 12px;
                padding: 20px;
            }
        """)
        header_layout = QVBoxLayout(header_frame)
        
        title = QLabel("🚀 ReelTune Super Smart AI Template Editor")
        title.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 24px;
                font-weight: bold;
                background: transparent;
            }
        """)
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(title)
        
        subtitle = QLabel("Professional • Intelligent • Beautiful - The future of AI-driven content creation")
        subtitle.setStyleSheet("""
            QLabel {
                color: rgba(255, 255, 255, 0.9);
                font-size: 14px;
                font-style: italic;
                background: transparent;
            }
        """)
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
        
    def _create_demo_footer(self, layout):
        """Create demo footer with instructions"""
        footer_frame = QWidget()
        footer_frame.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border: 1px solid rgba(255, 255, 255, 0.1);
                border-radius: 8px;
                padding: 15px;
            }
        """)
        footer_layout = QHBoxLayout(footer_frame)
        
        instructions = QLabel("""
        💡 Try These Features:
        • Change content types and watch timeline adapt
        • Toggle zones to see real-time validation
        • Use font size override to see smart user control
        • Save & Export to see unified functionality
        • Generate AI prompts for intelligent content creation
        • Preview AI instructions for detailed configuration
        """)
        instructions.setStyleSheet("""
            QLabel {
                color: #ccc;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        instructions.setWordWrap(True)
        footer_layout.addWidget(instructions)
        
        features = QLabel("""
        ✨ Smart Features Active:
        • Real-time template validation
        • Intelligent status messages
        • Context-aware AI prompt generation
        • Professional error handling
        • User actions override AI (smart design)
        • Modern, beautiful UI with gradients
        """)
        features.setStyleSheet("""
            QLabel {
                color: #ccc;
                font-size: 12px;
                line-height: 1.4;
            }
        """)
        features.setWordWrap(True)
        footer_layout.addWidget(features)
        
        layout.addWidget(footer_frame)
        
    def _apply_professional_styling(self):
        """Apply professional dark theme styling"""
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #1a1a1a);
                color: #ffffff;
            }
        """)

def main():
    """Main demo function"""
    # Create QApplication
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ReelTune Super Smart AI Template Editor")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Artists in DSP")
    
    # Set professional font
    font = QFont("SF Pro Display", 10)
    app.setFont(font)
    
    # Create and show demo window
    demo_window = SuperSmartDemoWindow()
    demo_window.show()
    
    print("🚀 Super Smart AI Template Editor Demo Started!")
    print("=" * 60)
    print("Features to explore:")
    print("• Beautiful, professional UI with modern styling")
    print("• Smart template validation with real-time feedback") 
    print("• Unified save & export functionality")
    print("• Intelligent AI prompt generation")
    print("• Context-aware status messages")
    print("• User actions always override AI (smart design)")
    print("• Professional error handling and messaging")
    print("=" * 60)
    print("Enjoy exploring the future of AI-driven content creation! 🎨")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
