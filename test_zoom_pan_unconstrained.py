#!/usr/bin/env python3
"""
Test script to verify zoom, pan, and unconstrained placement functionality.
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, QPoint
from PyQt6.QtGui import QWheelEvent

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def test_zoom_pan_unconstrained():
    """Test zoom, pan, and unconstrained placement features"""
    app = QApplication(sys.argv)
    
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing zoom, pan, and unconstrained placement...")
    
    visual_editor = editor.visual_editor
    
    # Test 1: Initial zoom and pan state
    print("\n1. Testing initial zoom/pan state...")
    print(f"  Initial zoom factor: {visual_editor.zoom_factor}")
    print(f"  Initial pan offset: ({visual_editor.pan_offset_x}, {visual_editor.pan_offset_y})")
    print(f"  Initial constraint mode: {visual_editor.constrain_to_frame}")
    
    assert visual_editor.zoom_factor == 1.0, "Initial zoom should be 1.0"
    assert visual_editor.pan_offset_x == 0, "Initial pan X should be 0"
    assert visual_editor.pan_offset_y == 0, "Initial pan Y should be 0"
    assert visual_editor.constrain_to_frame == False, "Initial constraint should be disabled"
    
    print("  ✓ Initial state correct")
    
    # Test 2: Coordinate transformation
    print("\n2. Testing coordinate transformation...")
    
    # Test with default zoom/pan
    screen_point = QPoint(100, 100)
    canvas_point = visual_editor._transform_point_to_canvas(screen_point)
    back_to_screen = visual_editor._transform_point_to_screen(canvas_point)
    
    print(f"  Screen point: {screen_point.x()}, {screen_point.y()}")
    print(f"  Canvas point: {canvas_point.x()}, {canvas_point.y()}")
    print(f"  Back to screen: {back_to_screen.x()}, {back_to_screen.y()}")
    
    assert abs(screen_point.x() - back_to_screen.x()) <= 1, "X coordinate transformation round-trip failed"
    assert abs(screen_point.y() - back_to_screen.y()) <= 1, "Y coordinate transformation round-trip failed"
    
    # Test with zoom
    visual_editor.zoom_factor = 2.0
    canvas_point = visual_editor._transform_point_to_canvas(screen_point)
    print(f"  With 2x zoom - Canvas point: {canvas_point.x()}, {canvas_point.y()}")
    
    # Test with pan
    visual_editor.pan_offset_x = 50
    visual_editor.pan_offset_y = 30
    canvas_point = visual_editor._transform_point_to_canvas(screen_point)
    print(f"  With pan offset - Canvas point: {canvas_point.x()}, {canvas_point.y()}")
    
    # Reset for next tests
    visual_editor.zoom_factor = 1.0
    visual_editor.pan_offset_x = 0
    visual_editor.pan_offset_y = 0
    
    print("  ✓ Coordinate transformation works")
    
    # Test 3: Unconstrained placement
    print("\n3. Testing unconstrained placement...")
    
    # Switch to reel type
    editor._on_content_type_changed('reel')
    
    # Get content frame bounds
    frame = visual_editor.content_frame
    print(f"  Content frame: ({frame.x()}, {frame.y()}) {frame.width()}x{frame.height()}")
    
    # Place PiP outside the content frame
    outside_x = frame.right() + 50
    outside_y = frame.bottom() + 50
    visual_editor.pip_rect.moveTo(outside_x, outside_y)
    
    print(f"  Moved PiP to: ({outside_x}, {outside_y}) - outside content frame")
    
    # Apply constraints (should do nothing since constrain_to_frame is False)
    visual_editor._constrain_elements_to_frame()
    
    pip_after_constraint = visual_editor.pip_rect
    print(f"  PiP after constraint call: ({pip_after_constraint.x()}, {pip_after_constraint.y()})")
    
    # Should still be outside the frame
    assert pip_after_constraint.x() == outside_x, "PiP X should remain outside frame when unconstrained"
    assert pip_after_constraint.y() == outside_y, "PiP Y should remain outside frame when unconstrained"
    
    print("  ✓ Unconstrained placement works")
    
    # Test 4: Test constraint toggle
    print("\n4. Testing constraint toggle...")
    
    # Enable constraints via UI
    editor.constrain_to_frame.setChecked(True)
    editor._on_constraint_changed()
    
    print(f"  Constraint mode after toggle: {visual_editor.constrain_to_frame}")
    assert visual_editor.constrain_to_frame == True, "Constraint should be enabled after toggle"
    
    # Now apply constraints - should move PiP back inside
    visual_editor._constrain_elements_to_frame()
    
    pip_after_enable = visual_editor.pip_rect
    print(f"  PiP after enabling constraints: ({pip_after_enable.x()}, {pip_after_enable.y()})")
    
    # Should now be inside the frame
    assert pip_after_enable.right() <= frame.right(), "PiP should be constrained to frame after enabling"
    assert pip_after_enable.bottom() <= frame.bottom(), "PiP should be constrained to frame after enabling"
    
    print("  ✓ Constraint toggle works")
    
    # Test 5: Test text overlay outside bounds
    print("\n5. Testing text overlay outside bounds...")
    
    # Disable constraints again
    editor.constrain_to_frame.setChecked(False)
    editor._on_constraint_changed()
    
    # Move title overlay outside frame
    title_outside_x = frame.left() - 100
    title_outside_y = frame.top() - 50
    visual_editor.text_overlays['title']['rect'].moveTo(title_outside_x, title_outside_y)
    
    print(f"  Moved title overlay to: ({title_outside_x}, {title_outside_y}) - outside content frame")
    
    # Apply constraints (should do nothing)
    visual_editor._constrain_elements_to_frame()
    
    title_after = visual_editor.text_overlays['title']['rect']
    print(f"  Title after constraint call: ({title_after.x()}, {title_after.y()})")
    
    assert title_after.x() == title_outside_x, "Title X should remain outside frame when unconstrained"
    assert title_after.y() == title_outside_y, "Title Y should remain outside frame when unconstrained"
    
    print("  ✓ Text overlay unconstrained placement works")
    
    # Test 6: Save/load with outside positions
    print("\n6. Testing save/load with outside positions...")
    
    # Save current settings with elements outside frame
    editor._save_all_current_settings()
    
    # Get saved settings
    saved_settings = editor.content_settings['reel']
    saved_pip_rect = saved_settings['pip_rect']
    saved_title_rect = saved_settings['text_overlays']['title']['rect']
    
    print(f"  Saved PiP rect: {saved_pip_rect}")
    print(f"  Saved title rect: {saved_title_rect}")
    
    # Create new editor and load settings
    editor2 = SimpleTemplateEditor()
    editor2.set_project(project)
    editor2.content_settings = editor.content_settings.copy()
    editor2._on_content_type_changed('reel')
    
    # Check loaded positions
    loaded_pip = editor2.visual_editor.pip_rect
    loaded_title = editor2.visual_editor.text_overlays['title']['rect']
    
    print(f"  Loaded PiP rect: ({loaded_pip.x()}, {loaded_pip.y()}) {loaded_pip.width()}x{loaded_pip.height()}")
    print(f"  Loaded title rect: ({loaded_title.x()}, {loaded_title.y()}) {loaded_title.width()}x{loaded_title.height()}")
    
    assert loaded_pip.x() == saved_pip_rect[0], "PiP X position should be preserved when loading"
    assert loaded_pip.y() == saved_pip_rect[1], "PiP Y position should be preserved when loading"
    assert loaded_title.x() == saved_title_rect[0], "Title X position should be preserved when loading"
    assert loaded_title.y() == saved_title_rect[1], "Title Y position should be preserved when loading"
    
    print("  ✓ Save/load preserves outside positions")
    
    print("\n✅ All zoom, pan, and unconstrained placement tests PASSED!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_zoom_pan_unconstrained()
        print("\n🎉 Zoom, pan, and unconstrained placement verification PASSED!")
    except Exception as e:
        print(f"\n❌ Zoom, pan, and unconstrained placement verification FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
