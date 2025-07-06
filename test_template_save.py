#!/usr/bin/env python3
"""
Test script to verify template settings are saved and loaded with project
"""
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.ai_template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication

def test_template_save_load():
    """Test that template settings are saved and loaded with project"""
    
    app = QApplication([])
    
    # Create a new project
    project = ReelForgeProject()
    project.metadata.name = "Test Template Project"
    
    # Create template editor and set project
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("✅ Created project and template editor")
    
    # Modify some template settings
    editor.current_content_type = "reel"
    editor.content_settings["reel"]["fixed_intro"] = True
    editor.content_settings["reel"]["pip_shape"] = "rectangle"
    editor.content_settings["reel"]["text_size"] = 36
    
    # Save settings to project (simulates auto-save)
    config = editor.get_template_config()
    project.simple_templates = config
    
    print("✅ Modified template settings and saved to project")
    
    # Save project to file
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    success = project.save(tmp_path)
    assert success, "Project save failed"
    
    print("✅ Saved project to file")
    
    # Load project from file
    loaded_project = ReelForgeProject.load(tmp_path)
    assert loaded_project is not None, "Project load failed"
    
    print("✅ Loaded project from file")
    
    # Verify template settings were preserved
    assert hasattr(loaded_project, 'simple_templates'), "simple_templates not found"
    assert 'content_settings' in loaded_project.simple_templates, "content_settings not found"
    
    reel_settings = loaded_project.simple_templates['content_settings']['reel']
    assert reel_settings['fixed_intro'] == True, "fixed_intro not preserved"
    assert reel_settings['pip_shape'] == "rectangle", "pip_shape not preserved"
    assert reel_settings['text_size'] == 36, "text_size not preserved"
    
    print("✅ All template settings correctly preserved in project save/load")
    
    # Test with new editor instance
    new_editor = SimpleTemplateEditor()
    new_editor.set_project(loaded_project)
    
    # Verify settings are loaded correctly in new editor
    assert new_editor.content_settings["reel"]["fixed_intro"] == True
    assert new_editor.content_settings["reel"]["pip_shape"] == "rectangle"
    assert new_editor.content_settings["reel"]["text_size"] == 36
    
    print("✅ Template settings correctly loaded into new editor instance")
    
    # Clean up
    tmp_path.unlink()
    
    print("\n🎉 ALL TESTS PASSED!")
    print("Template settings are now automatically saved with project (Cmd+S)")
    print("No Save Template button needed - everything auto-saves!")

if __name__ == "__main__":
    test_template_save_load()
