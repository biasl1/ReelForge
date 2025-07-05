#!/usr/bin/env python3
"""
Demo for the simplified AI-focused Template Editor
Shows the streamlined interface focused on AI content generation
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.ai_template_editor import AITemplateEditor
from core.project import ReelForgeProject


class AITemplateDemo(QMainWindow):
    """Demo window for the AI-focused template editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🤖 ReelTune AI Template Editor - Simplified")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Demo info
        info_layout = QHBoxLayout()
        
        self.load_reel_btn = QPushButton("📱 Load Reel Template")
        self.load_story_btn = QPushButton("📖 Load Story Template")  
        self.load_post_btn = QPushButton("📸 Load Post Template")
        self.reset_btn = QPushButton("🔄 Reset to Defaults")
        
        info_layout.addWidget(self.load_reel_btn)
        info_layout.addWidget(self.load_story_btn)
        info_layout.addWidget(self.load_post_btn)
        info_layout.addWidget(self.reset_btn)
        info_layout.addStretch()
        
        layout.addLayout(info_layout)
        
        # Create the AI template editor
        self.template_editor = AITemplateEditor()
        layout.addWidget(self.template_editor)
        
        # Create a demo project
        self.demo_project = ReelForgeProject("AI Demo Project")
        self.demo_project.ai_templates = {}
        self.template_editor.set_project(self.demo_project)
        
        # Connect demo buttons
        self.load_reel_btn.clicked.connect(lambda: self._load_demo_template("reel"))
        self.load_story_btn.clicked.connect(lambda: self._load_demo_template("story"))
        self.load_post_btn.clicked.connect(lambda: self._load_demo_template("post"))
        self.reset_btn.clicked.connect(self._reset_to_defaults)
        
        # Auto-load reel template
        QTimer.singleShot(500, lambda: self._load_demo_template("reel"))
        
    def _load_demo_template(self, content_type: str):
        """Load a demo template configuration"""
        print(f"\n🤖 Loading {content_type} AI template...")
        
        # Set content type in editor
        index = ["reel", "story", "post", "tutorial"].index(content_type)
        self.template_editor.content_type_selector.setCurrentIndex(index)
        
        # Apply content-specific settings
        if content_type == "reel":
            # Reel: All zones enabled, mostly AI-controlled
            self.template_editor.bg_enabled.setChecked(True)
            self.template_editor.bg_ai_controlled.setChecked(True)
            self.template_editor.media_enabled.setChecked(True)
            self.template_editor.media_ai_controlled.setChecked(True)
            self.template_editor.subtitle_enabled.setChecked(True)
            self.template_editor.subtitle_ai_controlled.setChecked(True)
            self.template_editor.font_size_fixed.setChecked(False)
            
        elif content_type == "story":
            # Story: Background AI-controlled, fixed subtitle
            self.template_editor.bg_enabled.setChecked(True)
            self.template_editor.bg_ai_controlled.setChecked(True)
            self.template_editor.media_enabled.setChecked(True)
            self.template_editor.media_ai_controlled.setChecked(False)  # Fixed positioning
            self.template_editor.subtitle_enabled.setChecked(True)
            self.template_editor.subtitle_ai_controlled.setChecked(False)
            self.template_editor.font_size_fixed.setChecked(True)
            self.template_editor.font_size_value.setValue(28)
            
        elif content_type == "post":
            # Post: More controlled layout
            self.template_editor.bg_enabled.setChecked(True)
            self.template_editor.bg_ai_controlled.setChecked(False)  # Fixed background
            self.template_editor.media_enabled.setChecked(True)
            self.template_editor.media_ai_controlled.setChecked(False)  # Fixed media
            self.template_editor.subtitle_enabled.setChecked(True)
            self.template_editor.subtitle_ai_controlled.setChecked(True)
            self.template_editor.font_size_fixed.setChecked(True)
            self.template_editor.font_size_value.setValue(32)
            
        # Update preview
        self.template_editor._update_template_preview()
        print(f"✅ Loaded {content_type} template configuration")
        
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        self.template_editor.bg_enabled.setChecked(True)
        self.template_editor.bg_ai_controlled.setChecked(True)
        self.template_editor.media_enabled.setChecked(True)
        self.template_editor.media_ai_controlled.setChecked(True)
        self.template_editor.subtitle_enabled.setChecked(True)
        self.template_editor.subtitle_ai_controlled.setChecked(True)
        self.template_editor.font_size_fixed.setChecked(False)
        self.template_editor.font_size_value.setValue(24)
        
        # Clear timeline
        self.template_editor.timeline.clear_intro()
        self.template_editor.timeline.clear_outro()
        
        self.template_editor._update_template_preview()
        print("🔄 Reset to default settings")


def main():
    """Run the AI template editor demo"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show demo window
    demo = AITemplateDemo()
    demo.show()
    
    print("🤖 ReelTune AI Template Editor - Simplified")
    print("=" * 55)
    print("🎯 Key Features:")
    print("✅ Focus on essential AI template settings only")
    print("✅ Background, Media Window, Subtitle zones")
    print("✅ AI control vs Fixed settings toggle")
    print("✅ Simple intro/outro timeline")
    print("✅ Drag & drop assets for intro/outro")
    print("✅ Template zone preview")
    print("✅ AI prompt generation")
    print("✅ Clean, focused interface")
    print("\n💡 Instructions:")
    print("• Use content type buttons to see different templates")
    print("• Toggle AI vs Fixed control for each zone")
    print("• Drag assets to intro/outro timeline sections")
    print("• Save template or export AI configuration")
    print("• Generate AI prompts for content creation")
    print("\n🎬 This editor integrates with ReelTune's AI pipeline!")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
