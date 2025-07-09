#!/usr/bin/env python3
"""
Quick test to understand the frame description persistence issue.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_description_persistence():
    """Test frame description persistence."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    
    # Set to story and go to frame 5 (should be the last frame)
    editor.set_content_type('story')
    
    # Check current frame count
    frame_count = editor.frame_timeline.get_frame_count()
    print(f"📊 Story has {frame_count} frames")
    
    # Go to last frame
    last_frame = frame_count - 1
    editor.frame_timeline.set_current_frame(last_frame)
    
    # Get current description
    if last_frame < len(editor.frame_timeline.frames):
        current_desc = editor.frame_timeline.frames[last_frame].get('frame_description', 'NOT FOUND')
        print(f"📝 Frame {last_frame} description: '{current_desc}'")
    else:
        print(f"❌ Frame {last_frame} not found in timeline frames")
    
    # Check canvas description
    canvas_desc = editor.canvas.get_current_frame_data()
    if canvas_desc:
        canvas_frame_desc = canvas_desc.get('frame_description', 'NOT FOUND')
        print(f"📝 Canvas frame description: '{canvas_frame_desc}'")
    else:
        print(f"❌ No canvas frame data found")

if __name__ == "__main__":
    test_description_persistence()
