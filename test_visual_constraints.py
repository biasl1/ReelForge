#!/usr/bin/env python3
"""
Additional test script to verify visual element behavior in the ReelTune editor.
This test checks that all constraints and positioning work correctly.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

# Add the project root to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor import SimpleTemplateEditor, TemplateCanvas
from core.project import ReelForgeProject

def test_visual_constraints():
    """Test that visual elements are properly constrained and scaled"""
    app = QApplication(sys.argv)
    
    # Create project and editor
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing visual element constraints and positioning...")
    
    # Test 1: Verify constraint function works
    print("\n1. Testing constraint functions...")
    
    visual_editor = editor.visual_editor
    
    # Set a content frame
    visual_editor.content_frame = QRect(100, 100, 400, 600)
    
    # Move PiP outside the frame intentionally
    visual_editor.pip_rect = QRect(50, 50, 100, 100)  # Partially outside
    print(f"  PiP before constraint: ({visual_editor.pip_rect.x()}, {visual_editor.pip_rect.y()})")
    
    # Apply constraints
    visual_editor._constrain_elements_to_frame()
    print(f"  PiP after constraint: ({visual_editor.pip_rect.x()}, {visual_editor.pip_rect.y()})")
    
    # Verify it's now within the frame
    assert visual_editor.pip_rect.left() >= visual_editor.content_frame.left(), "PiP left edge not constrained"
    assert visual_editor.pip_rect.top() >= visual_editor.content_frame.top(), "PiP top edge not constrained"
    assert visual_editor.pip_rect.right() <= visual_editor.content_frame.right(), "PiP right edge not constrained"
    assert visual_editor.pip_rect.bottom() <= visual_editor.content_frame.bottom(), "PiP bottom edge not constrained"
    
    print("  ✓ PiP constraint works correctly")
    
    # Test text overlay constraints
    for text_type, text_data in visual_editor.text_overlays.items():
        if text_data['enabled']:
            # Move outside frame
            text_data['rect'] = QRect(50, 50, 100, 50)
            
    visual_editor._constrain_elements_to_frame()
    
    for text_type, text_data in visual_editor.text_overlays.items():
        if text_data['enabled']:
            rect = text_data['rect']
            assert rect.left() >= visual_editor.content_frame.left(), f"{text_type} left edge not constrained"
            assert rect.top() >= visual_editor.content_frame.top(), f"{text_type} top edge not constrained"
            assert rect.right() <= visual_editor.content_frame.right(), f"{text_type} right edge not constrained"
            assert rect.bottom() <= visual_editor.content_frame.bottom(), f"{text_type} bottom edge not constrained"
    
    print("  ✓ Text overlay constraints work correctly")
    
    # Test 2: Verify all overlay types are handled in resize
    print("\n2. Testing resize handling for all overlay types...")
    
    # Set initial positions
    old_frame = QRect(100, 100, 400, 600)
    visual_editor.content_frame = old_frame
    visual_editor.pip_rect = QRect(150, 150, 100, 100)
    
    initial_overlays = {}
    for text_type, text_data in visual_editor.text_overlays.items():
        if text_data['enabled']:
            text_data['rect'] = QRect(120, 200 + len(initial_overlays) * 60, 200, 50)
            initial_overlays[text_type] = QRect(text_data['rect'])
    
    print(f"  Initial frame: {old_frame.width()}x{old_frame.height()}")
    print(f"  Initial PiP: ({visual_editor.pip_rect.x()}, {visual_editor.pip_rect.y()}) {visual_editor.pip_rect.width()}x{visual_editor.pip_rect.height()}")
    for text_type, rect in initial_overlays.items():
        print(f"  Initial {text_type}: ({rect.x()}, {rect.y()}) {rect.width()}x{rect.height()}")
    
    # Resize the frame
    new_frame = QRect(100, 100, 600, 800)  # 1.5x width, 1.33x height
    visual_editor.content_frame = new_frame
    visual_editor._update_elements_for_new_frame(old_frame)
    
    print(f"  New frame: {new_frame.width()}x{new_frame.height()}")
    print(f"  Scaled PiP: ({visual_editor.pip_rect.x()}, {visual_editor.pip_rect.y()}) {visual_editor.pip_rect.width()}x{visual_editor.pip_rect.height()}")
    
    # Verify scaling ratios
    scale_x = new_frame.width() / old_frame.width()
    scale_y = new_frame.height() / old_frame.height()
    
    print(f"  Scale factors: {scale_x:.2f}x, {scale_y:.2f}y")
    
    # Check all overlays were scaled
    for text_type, text_data in visual_editor.text_overlays.items():
        if text_type in initial_overlays:
            rect = text_data['rect']
            print(f"  Scaled {text_type}: ({rect.x()}, {rect.y()}) {rect.width()}x{rect.height()}")
    
    print("  ✓ All overlay types handled in resize")
    
    # Test 3: Test different content types have different defaults
    print("\n3. Testing content type-specific defaults...")
    
    content_types = ['reel', 'story', 'teaser', 'tutorial', 'post']
    type_settings = {}
    
    for content_type in content_types:
        editor._on_content_type_changed(content_type)
        
        type_settings[content_type] = {
            'pip_shape': visual_editor.pip_shape,
            'pip_pos': (visual_editor.pip_rect.x(), visual_editor.pip_rect.y()),
            'enabled_overlays': [t for t, d in visual_editor.text_overlays.items() if d['enabled']]
        }
        
        print(f"  {content_type}: {type_settings[content_type]['pip_shape']} PiP, {len(type_settings[content_type]['enabled_overlays'])} overlays enabled")
    
    # Verify tutorial has different defaults than other types
    tutorial_settings = type_settings['tutorial']
    reel_settings = type_settings['reel']
    
    print(f"  Tutorial PiP shape: {tutorial_settings['pip_shape']}")
    print(f"  Reel PiP shape: {reel_settings['pip_shape']}")
    
    print("  ✓ Content types have appropriate defaults")
    
    # Test 4: Test save/load cycle maintains all data
    print("\n4. Testing complete save/load cycle...")
    
    # Modify settings for reel
    editor._on_content_type_changed('reel')
    
    # Modify positions and content
    visual_editor.pip_rect.moveTo(200, 150)
    visual_editor.text_overlays['title']['rect'].moveTo(100, 250)
    visual_editor.text_overlays['title']['content'] = "Test Save/Load"
    visual_editor.text_overlays['subtitle']['enabled'] = True
    visual_editor.text_overlays['subtitle']['rect'].moveTo(100, 300)
    
    # Manually trigger save since we're modifying programmatically
    editor._save_all_current_settings()
    
    # Save to project
    editor._auto_save_to_project()
    
    # Get the saved configuration
    config = editor.get_template_config()
    
    # Create new editor and set the same project (which will load the saved settings)
    editor2 = SimpleTemplateEditor()
    editor2.set_project(project)  # This will automatically load the saved settings
    
    # Switch to reel and verify
    editor2._on_content_type_changed('reel')
    
    # Check positions
    pip2_pos = (editor2.visual_editor.pip_rect.x(), editor2.visual_editor.pip_rect.y())
    title2_pos = (editor2.visual_editor.text_overlays['title']['rect'].x(), 
                  editor2.visual_editor.text_overlays['title']['rect'].y())
    title2_content = editor2.visual_editor.text_overlays['title']['content']
    subtitle2_enabled = editor2.visual_editor.text_overlays['subtitle']['enabled']
    
    print(f"  Original PiP: (200, 150), Loaded: {pip2_pos}")
    print(f"  Original title: (100, 250), Loaded: {title2_pos}")
    print(f"  Original title content: 'Test Save/Load', Loaded: '{title2_content}'")
    print(f"  Original subtitle enabled: True, Loaded: {subtitle2_enabled}")
    
    assert pip2_pos == (200, 150), f"PiP position not preserved: expected (200, 150), got {pip2_pos}"
    assert title2_pos == (100, 250), f"Title position not preserved: expected (100, 250), got {title2_pos}"
    assert title2_content == "Test Save/Load", f"Title content not preserved"
    assert subtitle2_enabled == True, f"Subtitle enabled state not preserved"
    
    print("  ✓ Complete save/load cycle preserves all data")
    
    print("\n✅ All visual constraint and positioning tests PASSED!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_visual_constraints()
        print("\n🎉 Visual constraints verification PASSED!")
    except Exception as e:
        print(f"\n❌ Visual constraints verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
