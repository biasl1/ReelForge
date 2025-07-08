#!/usr/bin/env python3
"""
Simple test to verify the template settings save/load correctly
"""
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication

def test_template_persistence():
    """Test that template settings persist when saving and loading project"""
    
    app = QApplication([])
    
    print("🧪 Testing template persistence...")
    
    # Create project and modify settings
    project = ReelForgeProject()
    project.metadata.name = "Persistence Test"
    
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    # Make some changes
    editor.visual_editor.pip_dragging = True
    editor.visual_editor.pip_rect.translate(25, 15)
    mock_event = type('MockEvent', (), {})()
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    print(f"Modified PiP position to: {project.simple_templates['content_settings']['reel']['pip_rect']}")
    
    # Save to file
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    success = project.save(tmp_path)
    assert success, "Save failed"
    print(f"✅ Saved project to: {tmp_path}")
    
    # Load from file
    loaded_project = ReelForgeProject.load(tmp_path)
    assert loaded_project is not None, "Load failed"
    
    # Check settings are preserved
    loaded_pip = loaded_project.simple_templates['content_settings']['reel']['pip_rect']
    expected_pip = [75, 65, 100, 100]  # [50,50,100,100] + [25,15,0,0]
    
    assert loaded_pip == expected_pip, f"Settings not preserved: {loaded_pip} != {expected_pip}"
    print(f"✅ Settings preserved in file: {loaded_pip}")
    
    # Create new editor with loaded project
    new_editor = SimpleTemplateEditor()
    new_editor.set_project(loaded_project)
    
    # Verify visual editor reflects loaded settings
    visual_pip = [
        new_editor.visual_editor.pip_rect.x(),
        new_editor.visual_editor.pip_rect.y(),
        new_editor.visual_editor.pip_rect.width(),
        new_editor.visual_editor.pip_rect.height()
    ]
    
    assert visual_pip == expected_pip, f"Visual editor doesn't reflect loaded settings: {visual_pip} != {expected_pip}"
    print(f"✅ Visual editor correctly shows loaded settings: {visual_pip}")
    
    # Clean up
    tmp_path.unlink()
    
    print("\n🎉 TEMPLATE PERSISTENCE WORKS PERFECTLY!")
    print("\n📋 HOW TO USE CORRECTLY:")
    print("1. Open ReelTune")
    print("2. Create a project (or open existing)")
    print("3. Make template changes (drag, resize, settings)")
    print("4. Save project with Cmd+S")
    print("5. When reopening ReelTune, select 'Open Existing Project'")
    print("6. Choose your saved .rforge file")
    print("7. All template settings will be exactly as you left them!")
    print("\n⚠️  If you always click 'Create New Project', settings will reset!")

if __name__ == "__main__":
    test_template_persistence()
