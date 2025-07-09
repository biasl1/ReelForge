#!/usr/bin/env python3
"""
Test frame description persistence with the new sync fix.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_with_saved_data():
    """Test description persistence with saved project data."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    
    # Simulate loading saved settings (this would normally be called by main app)
    print("🔄 Simulating project loading...")
    
    # Set to story and check frame count  
    editor.set_content_type('story')
    frame_count = editor.frame_timeline.get_frame_count()
    print(f"📊 Story has {frame_count} frames after loading")
    
    # Go to last frame if there are more than 3
    if frame_count > 3:
        last_frame = frame_count - 1
        editor.frame_timeline.set_current_frame(last_frame)
        
        # Check description
        if last_frame < len(editor.frame_timeline.frames):
            current_desc = editor.frame_timeline.frames[last_frame].get('frame_description', 'NOT FOUND')
            print(f"📝 Frame {last_frame} description: '{current_desc}'")
            
            # Test the sync method directly
            print("🔄 Testing sync method...")
            editor.frame_timeline.sync_descriptions_with_canvas()
            
            # Check description after sync
            current_desc_after = editor.frame_timeline.frames[last_frame].get('frame_description', 'NOT FOUND')
            print(f"📝 Frame {last_frame} description after sync: '{current_desc_after}'")
        else:
            print(f"❌ Frame {last_frame} not found in timeline frames")
    else:
        print("ℹ️  Using default 3 frames (no saved data loaded)")

if __name__ == "__main__":
    test_with_saved_data()
