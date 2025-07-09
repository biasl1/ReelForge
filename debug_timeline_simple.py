#!/usr/bin/env python3
"""
Simple debug test to track timeline content type data.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def debug_timeline_data():
    """Debug timeline content type data to see what's happening."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    timeline = editor.frame_timeline
    
    print("🔍 Initial state:")
    print(f"  Content type: {timeline.content_type}")
    print(f"  Content type data: {timeline.content_type_data}")
    print(f"  Current frames: {len(timeline.frames)}")
    
    # Switch to story
    print("\n📖 Switching to story...")
    timeline.set_content_type("story")
    print(f"  Content type: {timeline.content_type}")
    print(f"  Story data: {timeline.content_type_data.get('story', 'NOT FOUND')}")
    print(f"  Current frames: {len(timeline.frames)}")
    
    # Remove frames
    print("\n➖ Removing frames in story...")
    timeline._remove_frame()  # 3 -> 2
    print(f"  After 1st removal: {len(timeline.frames)} frames")
    print(f"  Story data: {timeline.content_type_data.get('story', 'NOT FOUND')}")
    
    timeline._remove_frame()  # 2 -> 1
    print(f"  After 2nd removal: {len(timeline.frames)} frames")
    print(f"  Story data: {timeline.content_type_data.get('story', 'NOT FOUND')}")
    
    # Switch to reel
    print("\n🎬 Switching to reel...")
    timeline.set_content_type("reel")
    print(f"  Content type: {timeline.content_type}")
    print(f"  Reel data: {timeline.content_type_data.get('reel', 'NOT FOUND')}")
    print(f"  Current frames: {len(timeline.frames)}")
    
    # Switch back to story
    print("\n📖 Switching back to story...")
    timeline.set_content_type("story")
    print(f"  Content type: {timeline.content_type}")
    print(f"  Story data: {timeline.content_type_data.get('story', 'NOT FOUND')}")
    print(f"  Current frames: {len(timeline.frames)}")
    
    # Check if story frame count is preserved
    if len(timeline.frames) == 1:
        print("✅ SUCCESS: Story frame count preserved!")
    else:
        print(f"❌ FAILURE: Story frame count not preserved! Expected 1, got {len(timeline.frames)}")
        
        # Debug the internal data
        print("\n🔍 Debugging internal data:")
        print(f"  timeline.frames: {timeline.frames}")
        if 'story' in timeline.content_type_data:
            story_data = timeline.content_type_data['story']
            print(f"  story content_type_data: {story_data}")
            print(f"  story frames count: {len(story_data.get('frames', []))}")

if __name__ == "__main__":
    debug_timeline_data()
