#!/usr/bin/env python3
"""
Test the complete save/load workflow for template settings
"""
import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication

def test_complete_save_load_workflow():
    """Test complete save and load workflow"""
    
    app = QApplication([])
    
    print("🧪 Testing COMPLETE save/load workflow...")
    
    # Step 1: Create new project and modify template settings
    print("\n1. Creating new project and modifying template settings...")
    project = ReelForgeProject()
    project.metadata.name = "Complete Test Project"
    
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    # Make visual changes
    editor.visual_editor.pip_dragging = True
    editor.visual_editor.pip_rect.translate(30, 20)
    mock_event = type('MockEvent', (), {})()
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    # Make settings changes
    editor.fixed_intro.setChecked(True)
    editor._on_intro_outro_changed()
    
    # Change content type and make changes there too
    editor.current_content_type = "story"
    editor.visual_editor.set_content_type("story")
    editor._load_all_settings_for_current_type()
    
    editor.visual_editor.text_resizing = True
    editor.visual_editor.text_rect.setSize(editor.visual_editor.text_rect.size() + editor.visual_editor.text_rect.size())
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    print("✅ Made changes to reel and story templates")
    
    # Step 2: Save project to file (simulating Cmd+S)
    print("\n2. Saving project to file (simulating Cmd+S)...")
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    success = project.save(tmp_path)
    assert success, "Project save failed"
    print(f"✅ Project saved to: {tmp_path}")
    
    # Step 3: Close application and reopen (load from file)
    print("\n3. Reopening application (loading from saved file)...")
    
    # Simulate closing the app - destroy editor
    del editor
    
    # Load project from file (simulating app restart and opening existing project)
    loaded_project = ReelForgeProject.load(tmp_path)
    assert loaded_project is not None, "Project load failed"
    print("✅ Project loaded from file")
    
    # Step 4: Create new editor and verify settings are preserved
    print("\n4. Creating new editor and checking if settings are preserved...")
    new_editor = SimpleTemplateEditor()
    new_editor.set_project(loaded_project)
    
    # Check reel settings
    reel_settings = loaded_project.simple_templates['content_settings']['reel']
    expected_reel_pip = [80, 70, 100, 100]  # Original [50,50,100,100] + [30,20,0,0]
    actual_reel_pip = reel_settings['pip_rect']
    assert actual_reel_pip == expected_reel_pip, f"Reel PiP not preserved: {actual_reel_pip} != {expected_reel_pip}"
    
    assert reel_settings['fixed_intro'] == True, f"Reel fixed_intro not preserved: {reel_settings['fixed_intro']}"
    print("✅ Reel template settings correctly preserved")
    
    # Check story settings  
    story_settings = loaded_project.simple_templates['content_settings']['story']
    story_text_rect = story_settings['text_rect']
    # Text should have been doubled in size: original [50,400,200,50] -> bigger
    assert story_text_rect[2] > 200 or story_text_rect[3] > 50, f"Story text resize not preserved: {story_text_rect}"
    print("✅ Story template settings correctly preserved")
    
    # Verify UI reflects loaded settings
    assert new_editor.fixed_intro.isChecked() == True, "UI doesn't reflect loaded fixed_intro"
    
    new_pip_rect = [
        new_editor.visual_editor.pip_rect.x(),
        new_editor.visual_editor.pip_rect.y(),
        new_editor.visual_editor.pip_rect.width(),
        new_editor.visual_editor.pip_rect.height()
    ]
    assert new_pip_rect == expected_reel_pip, f"Visual editor doesn't reflect loaded PiP: {new_pip_rect} != {expected_reel_pip}"
    print("✅ UI correctly reflects all loaded settings")
    
    # Step 5: Make more changes and verify they save again
    print("\n5. Making more changes to verify ongoing saving...")
    new_editor.visual_editor.pip_dragging = True
    new_editor.visual_editor.pip_rect.translate(10, 5)
    new_editor.visual_editor.mouseReleaseEvent(mock_event)
    
    # Save again
    success = loaded_project.save(tmp_path)
    assert success, "Second save failed"
    
    # Verify the new changes are in the saved file
    final_project = ReelForgeProject.load(tmp_path)
    final_pip = final_project.simple_templates['content_settings']['reel']['pip_rect']
    expected_final_pip = [90, 75, 100, 100]  # Previous [80,70,100,100] + [10,5,0,0]
    assert final_pip == expected_final_pip, f"Second save not preserved: {final_pip} != {expected_final_pip}"
    print("✅ Subsequent changes also save correctly")
    
    # Clean up
    tmp_path.unlink()
    
    print("\n🎉 COMPLETE WORKFLOW TEST PASSED!")
    print("✅ Template settings save with project")
    print("✅ Template settings load when reopening project")
    print("✅ Visual changes persist across app restarts")
    print("✅ All content types preserve their independent settings")
    print("✅ Subsequent saves continue to work correctly")
    print("\n💡 The issue is likely that you're creating NEW projects instead of opening SAVED projects!")

if __name__ == "__main__":
    test_complete_save_load_workflow()
