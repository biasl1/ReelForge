#!/usr/bin/env python3
"""
Test that frame count is properly synced between timeline and canvas
and preserved when switching content types.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_frame_count_sync():
    """Test that frame count changes are properly synced between timeline and canvas."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    
    print("🧪 Testing frame count synchronization...")
    
    # Start with story content type  
    print("\n1️⃣ Starting with story content type...")
    editor.set_content_type("story")
    initial_count = editor.frame_timeline.get_frame_count()
    canvas_count = editor.canvas.get_content_type_frame_count("story")
    print(f"   Story initial frames: timeline={initial_count}, canvas={canvas_count}")
    
    # Remove frames in story to have only 1
    print("\n2️⃣ Removing frames in story to have only 1...")
    while editor.frame_timeline.get_frame_count() > 1:
        editor.frame_timeline._remove_frame()
    
    story_count_after_removal = editor.frame_timeline.get_frame_count()
    canvas_count_after_removal = editor.canvas.get_content_type_frame_count("story")
    print(f"   Story after removal: timeline={story_count_after_removal}, canvas={canvas_count_after_removal}")
    
    # Switch to reel
    print("\n3️⃣ Switching to reel...")
    editor.set_content_type("reel")
    reel_count = editor.frame_timeline.get_frame_count()
    reel_canvas_count = editor.canvas.get_content_type_frame_count("reel")
    print(f"   Reel frames: timeline={reel_count}, canvas={reel_canvas_count}")
    
    # Switch back to story - THIS IS THE CRITICAL TEST
    print("\n4️⃣ Switching back to story (CRITICAL TEST)...")
    editor.set_content_type("story")
    story_final_count = editor.frame_timeline.get_frame_count()
    story_final_canvas_count = editor.canvas.get_content_type_frame_count("story")
    print(f"   Story final: timeline={story_final_count}, canvas={story_final_canvas_count}")
    
    # Check results
    print("\n🔍 Results:")
    if story_final_count == 1 and story_final_canvas_count == 1:
        print("✅ SUCCESS: Frame count preserved correctly!")
        print(f"   Story maintained 1 frame after content type switching")
    else:
        print("❌ FAILURE: Frame count not preserved!")
        print(f"   Expected 1 frame, got timeline={story_final_count}, canvas={story_final_canvas_count}")
    
    # Test with more complex scenario
    print("\n5️⃣ Complex test: Add frames to reel, then check preservation...")
    editor.set_content_type("reel")
    
    # Add 2 more frames to reel
    editor.frame_timeline._add_frame()
    editor.frame_timeline._add_frame()
    
    reel_expanded_count = editor.frame_timeline.get_frame_count()
    reel_expanded_canvas = editor.canvas.get_content_type_frame_count("reel")
    print(f"   Reel expanded: timeline={reel_expanded_count}, canvas={reel_expanded_canvas}")
    
    # Switch to tutorial and back to reel
    editor.set_content_type("tutorial")
    tutorial_count = editor.frame_timeline.get_frame_count()
    print(f"   Tutorial frames: {tutorial_count}")
    
    editor.set_content_type("reel")
    reel_preserved_count = editor.frame_timeline.get_frame_count()
    reel_preserved_canvas = editor.canvas.get_content_type_frame_count("reel")
    print(f"   Reel preserved: timeline={reel_preserved_count}, canvas={reel_preserved_canvas}")
    
    # Final check for story
    editor.set_content_type("story")
    story_still_preserved = editor.frame_timeline.get_frame_count()
    story_still_canvas = editor.canvas.get_content_type_frame_count("story")
    print(f"   Story still preserved: timeline={story_still_preserved}, canvas={story_still_canvas}")
    
    print("\n🏁 Final Results:")
    success = (
        story_still_preserved == 1 and story_still_canvas == 1 and
        reel_preserved_count == 5 and reel_preserved_canvas == 5
    )
    
    if success:
        print("🎉 ALL TESTS PASSED! Frame count sync is working correctly!")
    else:
        print("💥 TESTS FAILED! Frame count sync is not working.")
        print(f"   Story: expected 1, got timeline={story_still_preserved}, canvas={story_still_canvas}")
        print(f"   Reel: expected 5, got timeline={reel_preserved_count}, canvas={reel_preserved_canvas}")

if __name__ == "__main__":
    test_frame_count_sync()
