#!/usr/bin/env python3
"""
Test script to verify that content types maintain INDEPENDENT settings.
This was the critical bug that needed fixing!
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def test_content_type_independence():
    """Test that each content type maintains independent settings - CRITICAL!"""
    app = QApplication(sys.argv)
    
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing content type INDEPENDENCE...")
    
    visual_editor = editor.visual_editor
    
    # Test 1: Set up different settings for REEL
    print("\n1. Setting up REEL with specific settings...")
    editor._on_content_type_changed('reel')
    
    # Modify reel settings
    reel_pip_pos = (100, 150)
    reel_title_pos = (75, 250)
    reel_constraint = True
    
    visual_editor.pip_rect.moveTo(*reel_pip_pos)
    visual_editor.text_overlays['title']['rect'].moveTo(*reel_title_pos)
    visual_editor.text_overlays['title']['content'] = "REEL TITLE"
    editor.constrain_to_frame.setChecked(reel_constraint)
    editor._on_constraint_changed()
    
    print(f"  REEL PiP position: {reel_pip_pos}")
    print(f"  REEL title position: {reel_title_pos}")
    print(f"  REEL constraint: {reel_constraint}")
    print(f"  REEL title content: 'REEL TITLE'")
    
    # Save reel settings
    editor._save_all_current_settings()
    
    # Test 2: Switch to STORY and set different settings
    print("\n2. Switching to STORY and setting different settings...")
    editor._on_content_type_changed('story')
    
    # Story should start with defaults, not reel settings
    story_pip_initial = (visual_editor.pip_rect.x(), visual_editor.pip_rect.y())
    story_title_initial = (visual_editor.text_overlays['title']['rect'].x(), 
                          visual_editor.text_overlays['title']['rect'].y())
    story_constraint_initial = visual_editor.constrain_to_frame
    story_title_content_initial = visual_editor.text_overlays['title']['content']
    
    print(f"  STORY initial PiP: {story_pip_initial}")
    print(f"  STORY initial title: {story_title_initial}")
    print(f"  STORY initial constraint: {story_constraint_initial}")
    print(f"  STORY initial title content: '{story_title_content_initial}'")
    
    # Verify story starts fresh (not inheriting reel settings)
    assert story_pip_initial != reel_pip_pos, f"STORY should not inherit REEL PiP position! Got {story_pip_initial}, expected different from {reel_pip_pos}"
    assert story_title_initial != reel_title_pos, f"STORY should not inherit REEL title position! Got {story_title_initial}, expected different from {reel_title_pos}"
    assert story_constraint_initial != reel_constraint, f"STORY should not inherit REEL constraint! Got {story_constraint_initial}, expected different from {reel_constraint}"
    assert story_title_content_initial != "REEL TITLE", f"STORY should not inherit REEL title content! Got '{story_title_content_initial}'"
    
    print("  ✓ STORY starts with independent settings (not inheriting from REEL)")
    
    # Now modify story settings
    story_pip_pos = (200, 300)
    story_title_pos = (150, 400)
    story_constraint = False
    
    visual_editor.pip_rect.moveTo(*story_pip_pos)
    visual_editor.text_overlays['title']['rect'].moveTo(*story_title_pos)
    visual_editor.text_overlays['title']['content'] = "STORY TITLE"
    editor.constrain_to_frame.setChecked(story_constraint)
    editor._on_constraint_changed()
    
    print(f"  Modified STORY PiP: {story_pip_pos}")
    print(f"  Modified STORY title: {story_title_pos}")
    print(f"  Modified STORY constraint: {story_constraint}")
    print(f"  Modified STORY title content: 'STORY TITLE'")
    
    # Save story settings
    editor._save_all_current_settings()
    
    # Test 3: Switch back to REEL - should restore REEL settings, not STORY
    print("\n3. Switching back to REEL - should restore original REEL settings...")
    editor._on_content_type_changed('reel')
    
    restored_reel_pip = (visual_editor.pip_rect.x(), visual_editor.pip_rect.y())
    restored_reel_title = (visual_editor.text_overlays['title']['rect'].x(),
                          visual_editor.text_overlays['title']['rect'].y())
    restored_reel_constraint = visual_editor.constrain_to_frame
    restored_reel_title_content = visual_editor.text_overlays['title']['content']
    
    print(f"  Restored REEL PiP: {restored_reel_pip}")
    print(f"  Restored REEL title: {restored_reel_title}")
    print(f"  Restored REEL constraint: {restored_reel_constraint}")
    print(f"  Restored REEL title content: '{restored_reel_title_content}'")
    
    # Verify reel settings were preserved
    assert restored_reel_pip == reel_pip_pos, f"REEL PiP should be preserved! Expected {reel_pip_pos}, got {restored_reel_pip}"
    assert restored_reel_title == reel_title_pos, f"REEL title should be preserved! Expected {reel_title_pos}, got {restored_reel_title}"
    assert restored_reel_constraint == reel_constraint, f"REEL constraint should be preserved! Expected {reel_constraint}, got {restored_reel_constraint}"
    assert restored_reel_title_content == "REEL TITLE", f"REEL title content should be preserved! Expected 'REEL TITLE', got '{restored_reel_title_content}'"
    
    print("  ✓ REEL settings perfectly preserved!")
    
    # Test 4: Switch to POST (new content type) - should get defaults
    print("\n4. Switching to POST (new content type) - should get fresh defaults...")
    editor._on_content_type_changed('post')
    
    post_pip = (visual_editor.pip_rect.x(), visual_editor.pip_rect.y())
    post_title = (visual_editor.text_overlays['title']['rect'].x(),
                 visual_editor.text_overlays['title']['rect'].y())
    post_constraint = visual_editor.constrain_to_frame
    post_title_content = visual_editor.text_overlays['title']['content']
    
    print(f"  POST PiP: {post_pip}")
    print(f"  POST title: {post_title}")
    print(f"  POST constraint: {post_constraint}")
    print(f"  POST title content: '{post_title_content}'")
    
    # Verify post doesn't inherit from reel or story
    assert post_pip != reel_pip_pos and post_pip != story_pip_pos, f"POST should not inherit PiP from REEL or STORY!"
    assert post_title != reel_title_pos and post_title != story_title_pos, f"POST should not inherit title from REEL or STORY!"
    assert post_title_content not in ["REEL TITLE", "STORY TITLE"], f"POST should not inherit title content!"
    
    print("  ✓ POST gets independent default settings")
    
    # Test 5: Final verification - switch back to STORY
    print("\n5. Final verification - switch back to STORY...")
    editor._on_content_type_changed('story')
    
    final_story_pip = (visual_editor.pip_rect.x(), visual_editor.pip_rect.y())
    final_story_title = (visual_editor.text_overlays['title']['rect'].x(),
                        visual_editor.text_overlays['title']['rect'].y())
    final_story_constraint = visual_editor.constrain_to_frame
    final_story_title_content = visual_editor.text_overlays['title']['content']
    
    print(f"  Final STORY PiP: {final_story_pip}")
    print(f"  Final STORY title: {final_story_title}")
    print(f"  Final STORY constraint: {final_story_constraint}")
    print(f"  Final STORY title content: '{final_story_title_content}'")
    
    # Verify story settings were preserved
    assert final_story_pip == story_pip_pos, f"STORY PiP should be preserved! Expected {story_pip_pos}, got {final_story_pip}"
    assert final_story_title == story_title_pos, f"STORY title should be preserved! Expected {story_title_pos}, got {final_story_title}"
    assert final_story_constraint == story_constraint, f"STORY constraint should be preserved! Expected {story_constraint}, got {final_story_constraint}"
    assert final_story_title_content == "STORY TITLE", f"STORY title content should be preserved! Expected 'STORY TITLE', got '{final_story_title_content}'"
    
    print("  ✓ STORY settings perfectly preserved!")
    
    print("\n✅ ALL CONTENT TYPE INDEPENDENCE TESTS PASSED!")
    print("🎉 Each content type maintains completely independent settings!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_content_type_independence()
        print("\n🔥 CONTENT TYPE INDEPENDENCE VERIFICATION PASSED! 🔥")
        print("📋 REEL, STORY, POST, etc. all maintain separate settings!")
    except Exception as e:
        print(f"\n❌ CONTENT TYPE INDEPENDENCE VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
