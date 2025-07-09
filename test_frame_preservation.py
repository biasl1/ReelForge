#!/usr/bin/env python3

"""
Test frame count preservation when switching content types
"""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_frame_count_preservation():
    """Test the exact issue: remove frames, switch content types, come back"""
    app = QApplication([])
    
    # Create editor
    editor = TemplateEditor()
    
    print("\n🧪 Testing frame count preservation issue...")
    
    # Start with story
    editor.set_content_type('story')
    initial_story_frames = len(editor.frame_timeline.frame_buttons)
    print(f"📋 Story starts with {initial_story_frames} frames")
    
    # Remove frames until only 1 left
    while len(editor.frame_timeline.frame_buttons) > 1:
        print(f"   Removing frame, current count: {len(editor.frame_timeline.frame_buttons)}")
        editor.frame_timeline._remove_frame()
    
    story_frames_after_removal = len(editor.frame_timeline.frame_buttons)
    print(f"✂️ Story after removal: {story_frames_after_removal} frames")
    
    # Switch to reel
    print(f"🔄 Switching to reel...")
    editor.set_content_type('reel')
    reel_frames = len(editor.frame_timeline.frame_buttons)
    print(f"📋 Reel has {reel_frames} frames")
    
    # Switch back to story
    print(f"🔄 Switching back to story...")
    editor.set_content_type('story')
    story_frames_after_return = len(editor.frame_timeline.frame_buttons)
    print(f"📋 Story after returning: {story_frames_after_return} frames")
    
    # Check if the issue happened
    if story_frames_after_return != story_frames_after_removal:
        print(f"❌ BUG CONFIRMED! Story should have {story_frames_after_removal} frames but has {story_frames_after_return}")
        print(f"   This is exactly the issue you described!")
    else:
        print(f"✅ Frame count preserved correctly")
    
    print("\n🏁 Test complete")

if __name__ == "__main__":
    test_frame_count_preservation()
