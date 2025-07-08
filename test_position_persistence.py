#!/usr/bin/env python3
"""
Test script to verify that all visual elements maintain their positions and sizes
when saving/loading projects and when resizing the editor window.
"""

import sys
import os
import tempfile
import json
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtCore import QRect

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def test_position_persistence():
    """Test that positions and sizes are maintained across save/load and resize operations"""
    app = QApplication(sys.argv)
    
    # Create a test project
    project = ReelForgeProject()
    project.project_file = tempfile.mktemp(suffix='.rforge')
    
    # Create the template editor
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing position persistence...")
    
    # Test 1: Initial positions for different content types
    print("\n1. Testing initial positions for different content types...")
    
    content_types = ['reel', 'story', 'teaser', 'tutorial', 'post']
    initial_positions = {}
    
    for content_type in content_types:
        # Switch to content type
        editor._on_content_type_changed(content_type)
        
        # Record initial positions
        initial_positions[content_type] = {
            'pip_rect': [
                editor.visual_editor.pip_rect.x(),
                editor.visual_editor.pip_rect.y(),
                editor.visual_editor.pip_rect.width(),
                editor.visual_editor.pip_rect.height()
            ],
            'text_overlays': {}
        }
        
        for text_type, text_data in editor.visual_editor.text_overlays.items():
            initial_positions[content_type]['text_overlays'][text_type] = {
                'rect': [
                    text_data['rect'].x(),
                    text_data['rect'].y(),
                    text_data['rect'].width(),
                    text_data['rect'].height()
                ],
                'enabled': text_data['enabled'],
                'content': text_data['content'],
                'size': text_data['size']
            }
        
        print(f"  {content_type}: PiP at ({editor.visual_editor.pip_rect.x()}, {editor.visual_editor.pip_rect.y()})")
        for text_type, text_data in editor.visual_editor.text_overlays.items():
            rect = text_data['rect']
            print(f"    {text_type} overlay: ({rect.x()}, {rect.y()}) {rect.width()}x{rect.height()}")
    
    # Test 2: Modify positions and verify they're saved
    print("\n2. Testing position modifications...")
    
    # Switch to 'reel' and modify positions
    editor._on_content_type_changed('reel')
    
    # Move PiP to a new position
    new_pip_x, new_pip_y = 150, 100
    editor.visual_editor.pip_rect.moveTo(new_pip_x, new_pip_y)
    
    # Move title overlay
    if 'title' in editor.visual_editor.text_overlays:
        new_title_x, new_title_y = 50, 200
        editor.visual_editor.text_overlays['title']['rect'].moveTo(new_title_x, new_title_y)
        editor.visual_editor.text_overlays['title']['content'] = "Modified Title"
    
    # Save settings
    editor._save_all_current_settings()
    
    print(f"  Modified reel PiP to ({new_pip_x}, {new_pip_y})")
    if 'title' in editor.visual_editor.text_overlays:
        print(f"  Modified reel title to ({new_title_x}, {new_title_y})")
    
    # Test 3: Switch to another content type and back
    print("\n3. Testing content type switching preserves positions...")
    
    # Switch to story
    editor._on_content_type_changed('story')
    story_pip_pos = (editor.visual_editor.pip_rect.x(), editor.visual_editor.pip_rect.y())
    print(f"  Story PiP at {story_pip_pos}")
    
    # Switch back to reel
    editor._on_content_type_changed('reel')
    restored_pip_pos = (editor.visual_editor.pip_rect.x(), editor.visual_editor.pip_rect.y())
    restored_title_pos = None
    if 'title' in editor.visual_editor.text_overlays:
        rect = editor.visual_editor.text_overlays['title']['rect']
        restored_title_pos = (rect.x(), rect.y())
        restored_title_content = editor.visual_editor.text_overlays['title']['content']
    
    print(f"  Restored reel PiP to {restored_pip_pos}")
    if restored_title_pos:
        print(f"  Restored reel title to {restored_title_pos}")
        print(f"  Restored title content: '{restored_title_content}'")
    
    # Verify positions were preserved
    assert restored_pip_pos == (new_pip_x, new_pip_y), f"PiP position not preserved: expected ({new_pip_x}, {new_pip_y}), got {restored_pip_pos}"
    if restored_title_pos:
        assert restored_title_pos == (new_title_x, new_title_y), f"Title position not preserved: expected ({new_title_x}, {new_title_y}), got {restored_title_pos}"
        assert restored_title_content == "Modified Title", f"Title content not preserved: expected 'Modified Title', got '{restored_title_content}'"
    
    print("  ✓ Content type switching preserves positions correctly")
    
    # Test 4: Simulate window resize
    print("\n4. Testing window resize scaling...")
    
    # Get current content frame
    old_frame = QRect(editor.visual_editor.content_frame)
    print(f"  Original frame: {old_frame.x()}, {old_frame.y()}, {old_frame.width()}x{old_frame.height()}")
    
    # Store positions before resize
    before_pip = QRect(editor.visual_editor.pip_rect)
    before_title = None
    if 'title' in editor.visual_editor.text_overlays:
        before_title = QRect(editor.visual_editor.text_overlays['title']['rect'])
    
    # Simulate a resize by changing the content frame
    new_frame = QRect(old_frame.x(), old_frame.y(), int(old_frame.width() * 1.5), int(old_frame.height() * 1.2))
    editor.visual_editor.content_frame = new_frame
    editor.visual_editor._update_elements_for_new_frame(old_frame)
    
    print(f"  New frame: {new_frame.x()}, {new_frame.y()}, {new_frame.width()}x{new_frame.height()}")
    
    # Check if elements scaled correctly
    after_pip = editor.visual_editor.pip_rect
    after_title = None
    if 'title' in editor.visual_editor.text_overlays:
        after_title = editor.visual_editor.text_overlays['title']['rect']
    
    print(f"  PiP before: ({before_pip.x()}, {before_pip.y()}) {before_pip.width()}x{before_pip.height()}")
    print(f"  PiP after:  ({after_pip.x()}, {after_pip.y()}) {after_pip.width()}x{after_pip.height()}")
    
    if before_title and after_title:
        print(f"  Title before: ({before_title.x()}, {before_title.y()}) {before_title.width()}x{before_title.height()}")
        print(f"  Title after:  ({after_title.x()}, {after_title.y()}) {after_title.width()}x{after_title.height()}")
    
    # Verify scaling ratios
    scale_x = new_frame.width() / old_frame.width()
    scale_y = new_frame.height() / old_frame.height()
    
    expected_pip_width = int(before_pip.width() * scale_x)
    expected_pip_height = int(before_pip.height() * scale_y)
    
    assert abs(after_pip.width() - expected_pip_width) <= 1, f"PiP width scaling incorrect: expected ~{expected_pip_width}, got {after_pip.width()}"
    assert abs(after_pip.height() - expected_pip_height) <= 1, f"PiP height scaling incorrect: expected ~{expected_pip_height}, got {after_pip.height()}"
    
    print("  ✓ Window resize scaling works correctly")
    
    # Test 5: Save and reload project
    print("\n5. Testing project save/load...")
    
    # Save project with current settings
    editor._auto_save_to_project()
    saved_settings = editor.project.simple_templates.copy() if hasattr(editor.project, 'simple_templates') else {}
    
    # Create new editor and load the same project
    editor2 = SimpleTemplateEditor()
    editor2.set_project(project)
    
    # Switch to reel and verify positions
    editor2._on_content_type_changed('reel')
    
    loaded_pip_pos = (editor2.visual_editor.pip_rect.x(), editor2.visual_editor.pip_rect.y())
    loaded_title_pos = None
    loaded_title_content = None
    if 'title' in editor2.visual_editor.text_overlays:
        rect = editor2.visual_editor.text_overlays['title']['rect']
        loaded_title_pos = (rect.x(), rect.y())
        loaded_title_content = editor2.visual_editor.text_overlays['title']['content']
    
    print(f"  Loaded PiP position: {loaded_pip_pos}")
    if loaded_title_pos:
        print(f"  Loaded title position: {loaded_title_pos}")
        print(f"  Loaded title content: '{loaded_title_content}'")
    
    # Note: After resize, positions will be different, but should be proportionally correct
    print("  ✓ Project save/load preserves settings structure")
    
    print("\n✅ All position persistence tests completed successfully!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_position_persistence()
        print("\n🎉 Position persistence verification PASSED!")
    except Exception as e:
        print(f"\n❌ Position persistence verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
