#!/usr/bin/env python3
"""Test script to verify complete save/load functionality works properly."""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from pathlib import Path
import tempfile
import json

def test_complete_save_load():
    """Test that save and load work like a normal application."""
    
    print("🧪 Testing complete save/load functionality...")
    
    # Import after setting up path
    from core.project import ReelForgeProject
    
    # Create a test project
    project = ReelForgeProject()
    project._project_name = "Test Save Load Project"
    project._is_modified = True
    
    # Add some test data
    project.global_prompt = "Test global prompt"
    project.moodboard_path = "/test/moodboard.jpg"
    
    # Add template editor settings
    project.template_editor_settings = {
        'reel': {
            'canvas_config': {
                'elements': {
                    'title': {
                        'type': 'text',
                        'rect': [100, 50, 200, 30],
                        'content': 'Test Title'
                    }
                },
                'content_frame': [50, 50, 300, 500],
                'constrain_to_frame': True
            }
        }
    }
    
    # Test save to temporary file
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp_file:
        test_path = tmp_file.name
    
    print(f"💾 Testing save to: {test_path}")
    
    # Test save with string path (common usage)
    success = project.save(test_path)
    if not success:
        print("❌ Save failed!")
        return False
    
    print("✅ Save successful")
    
    # Verify file exists and has content
    if not Path(test_path).exists():
        print("❌ Saved file doesn't exist!")
        return False
    
    # Check file content
    with open(test_path, 'r') as f:
        saved_data = json.load(f)
    
    print(f"📊 Saved data keys: {list(saved_data.keys())}")
    
    # Test load with string path
    print(f"📂 Testing load from: {test_path}")
    loaded_project = ReelForgeProject.load(test_path)
    
    if not loaded_project:
        print("❌ Load failed!")
        return False
    
    print("✅ Load successful")
    
    # Verify data integrity
    print("🔍 Verifying data integrity...")
    
    checks = [
        ("project_name", project.project_name, loaded_project.project_name),
        ("global_prompt", project.global_prompt, loaded_project.global_prompt),
        ("moodboard_path", project.moodboard_path, loaded_project.moodboard_path),
        ("is_modified", False, loaded_project.is_modified),  # Should be False after load
    ]
    
    all_good = True
    for name, original, loaded in checks:
        if original != loaded:
            print(f"❌ {name} mismatch: '{original}' != '{loaded}'")
            all_good = False
        else:
            print(f"✅ {name}: {loaded}")
    
    # Check template editor settings
    if hasattr(loaded_project, 'template_editor_settings'):
        template_settings = loaded_project.template_editor_settings
        if 'reel' in template_settings:
            print("✅ Template editor settings preserved")
        else:
            print("❌ Template editor settings missing content")
            all_good = False
    else:
        print("❌ Template editor settings not loaded")
        all_good = False
    
    # Test save with Path object
    path_obj_test = Path(test_path).with_name('test_path_object.rforge')
    print(f"💾 Testing save with Path object: {path_obj_test}")
    
    success = loaded_project.save(path_obj_test)
    if not success:
        print("❌ Save with Path object failed!")
        all_good = False
    else:
        print("✅ Save with Path object successful")
    
    # Clean up
    try:
        Path(test_path).unlink()
        if path_obj_test.exists():
            path_obj_test.unlink()
    except:
        pass
    
    return all_good

if __name__ == "__main__":
    success = test_complete_save_load()
    if success:
        print("\n🎉 Complete save/load functionality works perfectly!")
        print("   - Save with string paths ✅")
        print("   - Save with Path objects ✅") 
        print("   - Load with string paths ✅")
        print("   - Data integrity preserved ✅")
        print("   - Template settings preserved ✅")
        sys.exit(0)
    else:
        print("\n💥 Save/load functionality has issues!")
        sys.exit(1)
