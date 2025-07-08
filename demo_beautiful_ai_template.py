#!/usr/bin/env python3
"""
Demo: Beautiful AI Template Editor
Showcases the new professional, intuitive AI-focused template editor.

Features demonstrated:
- Beautiful, modern UI with gradients and shadows
- Smart design: user actions override AI, no redundant toggles
- Professional drag-and-drop from asset panel to timeline
- Truly optional intro/outro sections
- Live template preview with modern styling
- Smart AI prompt generation

Run this demo to see the improved template editor in action.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget, QSplitter
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from ui.template_editor import TemplateEditor
from ui.enhanced_asset_panel import EnhancedAssetPanel
from core.project import ReelForgeProject, AssetReference, ProjectMetadata


class BeautifulAITemplateDemo(QMainWindow):
    """Demo window showcasing the beautiful AI template editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("✨ Beautiful AI Template Editor - ReelTune")
        self.setGeometry(100, 100, 1400, 900)
        
        # Set modern font
        font = QFont("SF Pro Display", 10)
        self.setFont(font)
        
        # Dark modern theme
        self.setStyleSheet("""
            QMainWindow {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #2d2d2d, stop:1 #1a1a1a);
                color: #ffffff;
            }
        """)
        
        self.setup_ui()
        self.setup_demo_data()

    def setup_ui(self):
        """Setup the demo UI"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QHBoxLayout(central_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Create main splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Asset panel on the left
        self.asset_panel = EnhancedAssetPanel()
        self.asset_panel.setMaximumWidth(350)
        splitter.addWidget(self.asset_panel)
        
        # AI Template Editor on the right
        self.template_editor = TemplateEditor()
        splitter.addWidget(self.template_editor)
        
        # Set splitter proportions
        splitter.setSizes([350, 1050])
        
        layout.addWidget(splitter)

    def setup_demo_data(self):
        """Setup demo project with sample assets"""
        # Create demo project
        metadata = ProjectMetadata(
            name="Beautiful AI Template Demo",
            description="Demo project showcasing the beautiful AI template editor"
        )
        self.project = ReelForgeProject(metadata)
        
        # Add sample assets
        sample_assets = [
            ("intro_logo.mp4", "video", "Brand intro animation", "Branding"),
            ("outro_cta.mp4", "video", "Call to action outro", "Branding"),
            ("bg_music.mp3", "audio", "Background music track", "Music"),
            ("title_card.png", "image", "Title card design", "Graphics"),
            ("transition.mp4", "video", "Smooth transition effect", "Transitions"),
            ("logo.png", "image", "Company logo", "Branding"),
        ]
        
        for name, file_type, description, category in sample_assets:
            asset = AssetReference(
                id=f"demo_{name.replace('.', '_')}",
                name=name,
                file_path=str(Path(f"demo_assets/{name}")),
                file_type=file_type,
                description=description,
                folder=category
            )
            self.project.assets[asset.id] = asset
        
        # Set project in components
        self.asset_panel.set_project(self.project)
        self.template_editor.set_project(self.project)
        
        print("🎨 Beautiful AI Template Editor Demo")
        print("=" * 50)
        print("Features to explore:")
        print("• 📱 Live template preview with modern styling")
        print("• 🎬 Drag assets from left panel to timeline intro/outro slots")
        print("• ⚙️  Smart settings - no redundant toggles")
        print("• 🤖 AI prompt generation")
        print("• 💾 Template saving and export")
        print("• 🎯 Content type switching (Reel/Story/Post/Tutorial)")
        print("=" * 50)
        print("\n💡 Try this:")
        print("1. Select different content types from the dropdown")
        print("2. Drag 'intro_logo.mp4' to the intro section of the timeline")
        print("3. Drag 'outro_cta.mp4' to the outro section")
        print("4. Toggle template zones on/off")
        print("5. Override font size and see the smart behavior")
        print("6. Generate an AI prompt to see the intelligent output")
        print("\n🚀 The editor is 'smart not hard' - user actions override AI!")


def main():
    """Run the beautiful AI template editor demo"""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("ReelTune AI Template Editor")
    app.setApplicationVersion("2.0")
    app.setOrganizationName("Artists in DSP")
    
    # Create and show demo
    demo = BeautifulAITemplateDemo()
    demo.show()
    
    return app.exec()


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
