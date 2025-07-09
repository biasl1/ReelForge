#!/usr/bin/env python3

"""
Test the full template editor integration with timeline
"""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_editor_integration():
    """Test full editor integration"""
    app = QApplication([])
    
    # Create editor (this creates timeline and canvas)
    editor = TemplateEditor()
    
    print("\n🧪 Testing template editor integration...")
    
    # Test content type switching through editor
    content_types = ['reel', 'story', 'tutorial']
    
    for content_type in content_types:
        print(f"\n📋 Testing {content_type} through editor:")
        
        # Switch content type through editor
        editor.set_content_type(content_type)
        
        # Check editor state
        print(f"   Editor content_type: {editor.get_content_type()}")
        
        # Check timeline state
        print(f"   Timeline content_type: {editor.frame_timeline.content_type}")
        print(f"   Timeline frame count: {len(editor.frame_timeline.frame_buttons)}")
        
        # Check canvas state  
        canvas_frame_count = editor.canvas.get_content_type_frame_count()
        print(f"   Canvas frame count: {canvas_frame_count}")
        
        # Verify all components are in sync
        editor_correct = editor.get_content_type() == content_type
        timeline_correct = editor.frame_timeline.content_type == content_type
        frame_count_consistent = len(editor.frame_timeline.frame_buttons) == canvas_frame_count
        
        if editor_correct and timeline_correct and frame_count_consistent:
            print(f"   ✅ All components synchronized correctly")
        else:
            print(f"   ❌ Synchronization issue:")
            if not editor_correct:
                print(f"       Editor content_type wrong: {editor.get_content_type()}")
            if not timeline_correct:
                print(f"       Timeline content_type wrong: {editor.frame_timeline.content_type}")
            if not frame_count_consistent:
                print(f"       Frame count mismatch: Timeline={len(editor.frame_timeline.frame_buttons)}, Canvas={canvas_frame_count}")
    
    print(f"\n🎯 Testing frame switching:")
    
    # Test frame switching in tutorial (the problematic case)
    editor.set_content_type('tutorial')
    timeline = editor.frame_timeline
    
    print(f"   Tutorial has {len(timeline.frame_buttons)} frames")
    
    # Try switching frames
    for frame in range(min(3, len(timeline.frame_buttons))):
        print(f"   Switching to frame {frame}...")
        try:
            timeline.set_current_frame(frame)
            print(f"     ✅ Successfully switched to frame {frame}")
            print(f"     Current frame: {timeline.current_frame}")
        except Exception as e:
            print(f"     ❌ Error switching to frame {frame}: {e}")
    
    print("\n🏁 Editor integration test complete")

if __name__ == "__main__":
    test_editor_integration()
