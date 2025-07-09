#!/usr/bin/env python3
"""
Test the save functionality for frame independence
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor import TemplateEditor
from core.project import ReelForgeProject
from pathlib import Path

def test_save_functionality():
    """Test that saving works with frame independence"""
    app = QApplication([])
    
    # Create a project and template editor
    project = ReelForgeProject()
    project._project_name = "Test Frame Save"
    project._project_file_path = Path("/tmp/test_frame_save.rforge")
    
    editor = TemplateEditor()
    editor.set_content_type("story")  # Video content type
    
    print("🧪 Testing Save Functionality with Frame Independence")
    print("=" * 60)
    
    # Switch to different frames to create frame data
    print("Creating frame data...")
    
    # Frame 0 - modify elements
    editor.frame_timeline._on_frame_selected(0)
    print(f"Frame 0 elements: {list(editor.canvas.elements.keys())}")
    
    # Frame 1 - will create different elements
    editor.frame_timeline._on_frame_selected(1)
    print(f"Frame 1 elements: {list(editor.canvas.elements.keys())}")
    
    # Frame 2 - will create different elements
    editor.frame_timeline._on_frame_selected(2)
    print(f"Frame 2 elements: {list(editor.canvas.elements.keys())}")
    
    # Now try to save
    print("\n💾 Testing Save...")
    try:
        project.save_template_editor_settings(editor)
        print("✅ Save successful!")
        
        # Check what was saved
        template_settings = getattr(project, 'template_editor_settings', {})
        if 'story' in template_settings:
            story_config = template_settings['story']
            print(f"📊 Saved story config keys: {list(story_config.keys())}")
            
            if 'frames_config' in story_config:
                frames_config = story_config['frames_config']
                print(f"🎬 Frames config keys: {list(frames_config.keys())}")
                
                if 'frames_data' in frames_config:
                    frames_data = frames_config['frames_data']
                    print(f"📁 Frame data keys: {list(frames_data.keys())}")
                    
                    for frame_idx, frame_data in frames_data.items():
                        if 'elements' in frame_data:
                            elements = frame_data['elements']
                            print(f"   Frame {frame_idx}: {len(elements)} elements")
            
        return True
        
    except Exception as e:
        print(f"❌ Save failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        app.quit()

if __name__ == "__main__":
    success = test_save_functionality()
    if success:
        print("\n🎉 SAVE FUNCTIONALITY WORKS!")
    else:
        print("\n💥 Save functionality needs fixing")
