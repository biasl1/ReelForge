#!/usr/bin/env python3
"""
Demo script for the Visual Template Editor
Shows off all the features of the WYSIWYG template editor
"""

import sys
import json
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor

# Add the project root to path
sys.path.insert(0, str(Path(__file__).parent))

from ui.template_editor import SimpleTemplateEditor as VisualTemplateEditor
from ui.template_editor.compat import LayerItem
from core.content_generation import ContentGenerationManager
from core.project import ReelForgeProject


class TemplateEditorDemo(QMainWindow):
    """Demo window showcasing the Visual Template Editor"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎬 ReelTune Visual Template Editor Demo")
        self.setGeometry(100, 100, 1400, 900)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Demo controls
        controls_layout = QHBoxLayout()
        
        self.demo_reel_btn = QPushButton("📱 Demo Reel Template")
        self.demo_story_btn = QPushButton("📖 Demo Story Template")  
        self.demo_post_btn = QPushButton("📸 Demo Post Template")
        self.demo_tutorial_btn = QPushButton("🎓 Demo Tutorial Template")
        self.save_demo_btn = QPushButton("💾 Save Demo Template")
        self.export_config_btn = QPushButton("📋 Export Config")
        self.generate_prompt_btn = QPushButton("🤖 Generate AI Prompt")
        
        controls_layout.addWidget(self.demo_reel_btn)
        controls_layout.addWidget(self.demo_story_btn)
        controls_layout.addWidget(self.demo_post_btn)
        controls_layout.addWidget(self.demo_tutorial_btn)
        controls_layout.addWidget(self.save_demo_btn)
        controls_layout.addWidget(self.export_config_btn)
        controls_layout.addWidget(self.generate_prompt_btn)
        
        layout.addLayout(controls_layout)
        
        # Create the visual template editor
        self.template_editor = VisualTemplateEditor()
        layout.addWidget(self.template_editor)
        
        # Create a demo project
        self.demo_project = ReelForgeProject("Demo Project")
        self.demo_project.content_generation_manager = ContentGenerationManager()
        self.template_editor.set_project(self.demo_project)
        
        # Connect demo buttons
        self.demo_reel_btn.clicked.connect(lambda: self._load_demo_template("reel"))
        self.demo_story_btn.clicked.connect(lambda: self._load_demo_template("story"))
        self.demo_post_btn.clicked.connect(lambda: self._load_demo_template("post"))
        self.demo_tutorial_btn.clicked.connect(lambda: self._load_demo_template("tutorial"))
        self.save_demo_btn.clicked.connect(self._save_demo_template)
        self.export_config_btn.clicked.connect(self._export_config)
        self.generate_prompt_btn.clicked.connect(self._generate_ai_prompt)
        
        # Auto-load reel template
        QTimer.singleShot(500, lambda: self._load_demo_template("reel"))
        
    def _load_demo_template(self, content_type: str):
        """Load a demo template for the specified content type"""
        print(f"\n🎬 Loading {content_type} demo template...")
        
        # Set content type
        index = ["reel", "story", "post", "tutorial"].index(content_type)
        self.template_editor.content_type_selector.setCurrentIndex(index)
        
        # Clear existing layers
        self.template_editor.canvas.clear_layers()
        
        if content_type == "reel":
            self._create_reel_demo()
        elif content_type == "story":
            self._create_story_demo()
        elif content_type == "post":
            self._create_post_demo()
        elif content_type == "tutorial":
            self._create_tutorial_demo()
            
        self.template_editor._refresh_layer_tree()
        print(f"✅ Loaded {content_type} template with {len(self.template_editor.canvas.layers)} layers")
        
    def _create_reel_demo(self):
        """Create a demo reel template"""
        # Background gradient
        bg_layer = LayerItem("Gradient Background", "background")
        bg_layer.rect.setRect(0, 0, 405, 720)
        bg_layer.color = QColor(20, 25, 40)
        self.template_editor.canvas.add_layer(bg_layer)
        
        # Main video area
        video_layer = LayerItem("Main Video", "media")
        video_layer.rect.setRect(25, 80, 355, 500)
        self.template_editor.canvas.add_layer(video_layer)
        
        # Title overlay
        title_layer = LayerItem("Title", "text")
        title_layer.rect.setRect(40, 20, 325, 50)
        title_layer.text = "🔥 EPIC REEL TITLE"
        title_layer.font_size = 32
        title_layer.text_color = QColor(255, 255, 255)
        self.template_editor.canvas.add_layer(title_layer)
        
        # Subtitle track
        subtitle_layer = LayerItem("Subtitles", "text")
        subtitle_layer.rect.setRect(40, 600, 325, 80)
        subtitle_layer.text = "Dynamic subtitle text appears here"
        subtitle_layer.font_size = 24
        subtitle_layer.text_color = QColor(255, 255, 0)
        self.template_editor.canvas.add_layer(subtitle_layer)
        
        # CTA button
        cta_layer = LayerItem("CTA Button", "overlay")
        cta_layer.rect.setRect(280, 680, 100, 30)
        cta_layer.color = QColor(255, 59, 48, 200)
        self.template_editor.canvas.add_layer(cta_layer)
        
    def _create_story_demo(self):
        """Create a demo story template"""
        # Background
        bg_layer = LayerItem("Story Background", "background")
        bg_layer.rect.setRect(0, 0, 405, 720)
        bg_layer.color = QColor(255, 45, 85)
        self.template_editor.canvas.add_layer(bg_layer)
        
        # Main content
        content_layer = LayerItem("Story Content", "media")
        content_layer.rect.setRect(40, 120, 325, 400)
        self.template_editor.canvas.add_layer(content_layer)
        
        # Story title
        title_layer = LayerItem("Story Title", "text")
        title_layer.rect.setRect(40, 40, 325, 60)
        title_layer.text = "📖 Story Moment"
        title_layer.font_size = 28
        title_layer.text_color = QColor(255, 255, 255)
        self.template_editor.canvas.add_layer(title_layer)
        
        # Quick text overlay
        text_layer = LayerItem("Quick Text", "text")
        text_layer.rect.setRect(40, 550, 325, 100)
        text_layer.text = "Swipe up for more!"
        text_layer.font_size = 20
        text_layer.text_color = QColor(255, 255, 255)
        self.template_editor.canvas.add_layer(text_layer)
        
    def _create_post_demo(self):
        """Create a demo post template"""
        # Clean background
        bg_layer = LayerItem("Post Background", "background")
        bg_layer.rect.setRect(0, 0, 600, 600)
        bg_layer.color = QColor(248, 248, 248)
        self.template_editor.canvas.add_layer(bg_layer)
        
        # Main image area
        image_layer = LayerItem("Main Image", "media")
        image_layer.rect.setRect(50, 50, 500, 350)
        self.template_editor.canvas.add_layer(image_layer)
        
        # Post title
        title_layer = LayerItem("Post Title", "text")
        title_layer.rect.setRect(50, 420, 500, 60)
        title_layer.text = "✨ Amazing Post Title"
        title_layer.font_size = 36
        title_layer.text_color = QColor(50, 50, 50)
        self.template_editor.canvas.add_layer(title_layer)
        
        # Description
        desc_layer = LayerItem("Description", "text")
        desc_layer.rect.setRect(50, 500, 500, 80)
        desc_layer.text = "Engaging description that tells the story..."
        desc_layer.font_size = 18
        desc_layer.text_color = QColor(100, 100, 100)
        self.template_editor.canvas.add_layer(desc_layer)
        
        # Brand logo
        logo_layer = LayerItem("Brand Logo", "overlay")
        logo_layer.rect.setRect(500, 20, 80, 80)
        logo_layer.color = QColor(0, 122, 255, 150)
        self.template_editor.canvas.add_layer(logo_layer)
        
    def _create_tutorial_demo(self):
        """Create a demo tutorial template"""
        # Tutorial background
        bg_layer = LayerItem("Tutorial Background", "background")
        bg_layer.rect.setRect(0, 0, 405, 720)
        bg_layer.color = QColor(30, 30, 30)
        self.template_editor.canvas.add_layer(bg_layer)
        
        # Step indicator
        step_layer = LayerItem("Step Indicator", "overlay")
        step_layer.rect.setRect(20, 20, 60, 30)
        step_layer.color = QColor(52, 199, 89, 200)
        self.template_editor.canvas.add_layer(step_layer)
        
        # Tutorial content
        content_layer = LayerItem("Tutorial Video", "media")
        content_layer.rect.setRect(30, 70, 345, 400)
        self.template_editor.canvas.add_layer(content_layer)
        
        # Tutorial title
        title_layer = LayerItem("Tutorial Title", "text")
        title_layer.rect.setRect(30, 480, 345, 50)
        title_layer.text = "🎓 How to: Step by Step"
        title_layer.font_size = 24
        title_layer.text_color = QColor(255, 255, 255)
        self.template_editor.canvas.add_layer(title_layer)
        
        # Instructions
        inst_layer = LayerItem("Instructions", "text")
        inst_layer.rect.setRect(30, 540, 345, 120)
        inst_layer.text = "Follow these simple steps to master this technique..."
        inst_layer.font_size = 16
        inst_layer.text_color = QColor(200, 200, 200)
        self.template_editor.canvas.add_layer(inst_layer)
        
        # Progress bar
        progress_layer = LayerItem("Progress Bar", "overlay")
        progress_layer.rect.setRect(30, 680, 200, 8)
        progress_layer.color = QColor(255, 159, 10, 200)
        self.template_editor.canvas.add_layer(progress_layer)
        
    def _save_demo_template(self):
        """Save the current template"""
        self.template_editor.save_template_to_project()
        print(f"💾 Saved template for {self.template_editor.current_content_type}")
        
    def _export_config(self):
        """Export current template configuration"""
        config = self.template_editor.export_template_config()
        
        # Save to file
        output_file = Path("demo_template_config.json")
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)
            
        print(f"📋 Exported template config to {output_file}")
        print(f"Config keys: {list(config.keys())}")
        
    def _generate_ai_prompt(self):
        """Generate AI prompt for current template"""
        prompt = self.template_editor.generate_ai_prompt()
        
        # Save to file
        output_file = Path("demo_ai_prompt.txt")
        with open(output_file, 'w') as f:
            f.write(prompt)
            
        print(f"🤖 Generated AI prompt:")
        print("-" * 50)
        print(prompt)
        print("-" * 50)
        print(f"Saved to {output_file}")


def main():
    """Run the template editor demo"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Create and show demo window
    demo = TemplateEditorDemo()
    demo.show()
    
    print("🎬 ReelTune Visual Template Editor Demo")
    print("=" * 50)
    print("Features demonstrated:")
    print("✅ WYSIWYG visual editing")
    print("✅ Multiple content types (Reel, Story, Post, Tutorial)")
    print("✅ Layer management with drag & drop")
    print("✅ Property editing (position, size, colors, text)")
    print("✅ Template saving/loading")
    print("✅ Config export for AI generation")
    print("✅ AI prompt generation")
    print("✅ Keyboard shortcuts (Del, G, Ctrl+D, arrows)")
    print("✅ Grid snapping and visual guides")
    print("\n🎯 Try the demo buttons to see different template types!")
    
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
