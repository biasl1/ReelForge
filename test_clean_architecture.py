#!/usr/bin/env python3
"""
Test the new modular template editor architecture.
"""
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import Qt

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from ui.template_editor import SimpleTemplateEditor


class TestWindow(QMainWindow):
    """Test window for the new template editor."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("ReelTune Template Editor - Clean Architecture Test")
        self.setGeometry(100, 100, 1200, 800)
        
        # Central widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Test buttons
        button_layout = QHBoxLayout()
        
        reel_btn = QPushButton("Reel (9:16)")
        reel_btn.clicked.connect(lambda: self.editor.set_content_type("reel"))
        button_layout.addWidget(reel_btn)
        
        tutorial_btn = QPushButton("Tutorial (16:9)")
        tutorial_btn.clicked.connect(lambda: self.editor.set_content_type("tutorial"))
        button_layout.addWidget(tutorial_btn)
        
        post_btn = QPushButton("Post (1:1)")
        post_btn.clicked.connect(lambda: self.editor.set_content_type("post"))
        button_layout.addWidget(post_btn)
        
        save_btn = QPushButton("Save Template")
        save_btn.clicked.connect(self.save_template)
        button_layout.addWidget(save_btn)
        
        load_btn = QPushButton("Load Template")
        load_btn.clicked.connect(self.load_template)
        button_layout.addWidget(load_btn)
        
        button_layout.addStretch()
        layout.addLayout(button_layout)
        
        # Template editor
        self.editor = SimpleTemplateEditor()
        self.editor.template_changed.connect(self.on_template_changed)
        layout.addWidget(self.editor)
    
    def on_template_changed(self, config):
        """Handle template changes."""
        print(f"Template changed: {config['canvas_config']['content_type']}")
        print(f"Constrain mode: {config['canvas_config']['constrain_to_frame']}")
        print(f"Zoom: {config['view_state']['zoom']:.2f}")
    
    def save_template(self):
        """Save current template."""
        try:
            self.editor.save_template("test_template.json")
            print("✅ Template saved successfully!")
        except Exception as e:
            print(f"❌ Error saving template: {e}")
    
    def load_template(self):
        """Load saved template."""
        try:
            if self.editor.load_template("test_template.json"):
                print("✅ Template loaded successfully!")
            else:
                print("❌ Failed to load template")
        except Exception as e:
            print(f"❌ Error loading template: {e}")


def main():
    """Main function."""
    app = QApplication(sys.argv)
    
    # Test the modular architecture
    print("🧪 Testing New Modular Template Editor Architecture")
    print("=" * 60)
    
    try:
        # Test imports
        from ui.template_editor import SimpleTemplateEditor, TemplateCanvas, TemplateControls
        from ui.template_editor.utils import CONTENT_DIMENSIONS, CoordinateTransform
        print("✅ All imports successful")
        
        # Test content dimensions
        print(f"✅ Content dimensions loaded: {len(CONTENT_DIMENSIONS)} types")
        
        # Test coordinate transform
        transform = CoordinateTransform()
        transform.set_zoom(2.0)
        print(f"✅ Coordinate transform working: zoom = {transform.get_zoom()}")
        
        # Create test window
        window = TestWindow()
        window.show()
        
        print("✅ Template editor created successfully")
        print("\n🎉 SUCCESS: New modular architecture is working!")
        print("\nTest Instructions:")
        print("1. Try different content types (Reel, Tutorial, Post)")
        print("2. Toggle 'Constrain elements to content frame' checkbox")
        print("3. Zoom in/out with mouse wheel + Ctrl")
        print("4. Pan with right-click and drag")
        print("5. Drag elements around (they can go outside frame when unconstrained)")
        print("6. Select elements and edit properties in the right panel")
        print("7. Save and load templates")
        
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
