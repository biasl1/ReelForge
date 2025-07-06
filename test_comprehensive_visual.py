#!/usr/bin/env python3
"""
Comprehensive test for visual element saving
"""
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.ai_template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint, QSize
from PyQt6.QtGui import QMouseEvent

def test_all_visual_operations():
    """Test all visual drag/resize operations save correctly"""
    
    app = QApplication([])
    
    # Create project and editor
    project = ReelForgeProject()
    project.metadata.name = "Visual Test Project"
    
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("🧪 Testing all visual operations...")
    
    # Test 1: PiP move
    print("\n1. Testing PiP move...")
    editor.visual_editor.pip_dragging = True
    editor.visual_editor.pip_rect.translate(25, 15)
    mock_event = type('MockEvent', (), {})()
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    saved_pip = project.simple_templates['content_settings']['reel']['pip_rect']
    expected_pip = [75, 65, 100, 100]  # Original [50,50,100,100] + [25,15,0,0]
    assert saved_pip == expected_pip, f"PiP move failed: {saved_pip} != {expected_pip}"
    print("✅ PiP move saved correctly")
    
    # Test 2: PiP resize
    print("\n2. Testing PiP resize...")
    editor.visual_editor.pip_resizing = True
    editor.visual_editor.pip_rect.setSize(QSize(150, 120))
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    saved_pip = project.simple_templates['content_settings']['reel']['pip_rect']
    expected_pip = [75, 65, 150, 120]
    assert saved_pip == expected_pip, f"PiP resize failed: {saved_pip} != {expected_pip}"
    print("✅ PiP resize saved correctly")
    
    # Test 3: Text move
    print("\n3. Testing text move...")
    editor.visual_editor.text_dragging = True
    editor.visual_editor.text_rect.translate(30, -20)
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    saved_text = project.simple_templates['content_settings']['reel']['text_rect']
    expected_text = [80, 380, 200, 50]  # Original [50,400,200,50] + [30,-20,0,0]
    assert saved_text == expected_text, f"Text move failed: {saved_text} != {expected_text}"
    print("✅ Text move saved correctly")
    
    # Test 4: Text resize
    print("\n4. Testing text resize...")
    editor.visual_editor.text_resizing = True
    editor.visual_editor.text_rect.setSize(QSize(300, 80))
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    saved_text = project.simple_templates['content_settings']['reel']['text_rect']
    expected_text = [80, 380, 300, 80]
    assert saved_text == expected_text, f"Text resize failed: {saved_text} != {expected_text}"
    print("✅ Text resize saved correctly")
    
    # Test 5: Save and reload from file
    print("\n5. Testing save/reload persistence...")
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    success = project.save(tmp_path)
    assert success, "Project save failed"
    
    loaded_project = ReelForgeProject.load(tmp_path)
    assert loaded_project is not None, "Project load failed"
    
    # Check all saved values persist
    loaded_pip = loaded_project.simple_templates['content_settings']['reel']['pip_rect']
    loaded_text = loaded_project.simple_templates['content_settings']['reel']['text_rect']
    
    assert loaded_pip == expected_pip, f"PiP persistence failed: {loaded_pip} != {expected_pip}"
    assert loaded_text == expected_text, f"Text persistence failed: {loaded_text} != {expected_text}"
    
    print("✅ All visual changes persist in saved project file")
    
    # Test 6: New editor loads correctly
    print("\n6. Testing new editor loads saved visual state...")
    new_editor = SimpleTemplateEditor()
    new_editor.set_project(loaded_project)
    
    new_pip_rect = [
        new_editor.visual_editor.pip_rect.x(),
        new_editor.visual_editor.pip_rect.y(),
        new_editor.visual_editor.pip_rect.width(),
        new_editor.visual_editor.pip_rect.height()
    ]
    
    new_text_rect = [
        new_editor.visual_editor.text_rect.x(),
        new_editor.visual_editor.text_rect.y(),
        new_editor.visual_editor.text_rect.width(),
        new_editor.visual_editor.text_rect.height()
    ]
    
    assert new_pip_rect == expected_pip, f"New editor PiP load failed: {new_pip_rect} != {expected_pip}"
    assert new_text_rect == expected_text, f"New editor text load failed: {new_text_rect} != {expected_text}"
    
    print("✅ New editor correctly loads all visual positions and sizes")
    
    # Clean up
    tmp_path.unlink()
    
    print("\n🎉 ALL VISUAL OPERATIONS WORK PERFECTLY!")
    print("✅ Drag PiP → Auto-saves to project")
    print("✅ Resize PiP → Auto-saves to project") 
    print("✅ Drag text → Auto-saves to project")
    print("✅ Resize text → Auto-saves to project")
    print("✅ Cmd+S saves everything to .rforge file")
    print("✅ Reopening project restores all visual positions/sizes")

if __name__ == "__main__":
    test_all_visual_operations()
