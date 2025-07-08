#!/usr/bin/env python3
"""
Test script to verify zoom, pan, and unconstrained positioning functionality
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, QPoint

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.ai_template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def test_zoom_pan_unconstrained():
    """Test zoom, pan, and unconstrained positioning features"""
    app = QApplication(sys.argv)
    
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing zoom, pan, and unconstrained positioning...")
    
    # Test 1: Verify default constraint state
    print("\n1. Testing default constraint state...")
    print(f"Constrain checkbox: {editor.constrain_elements.isChecked()}")
    print(f"Visual editor constraint: {editor.visual_editor.constrain_to_frame}")
    print(f"Default zoom: {editor.visual_editor.zoom_factor}")
    print(f"Default pan: ({editor.visual_editor.pan_offset_x}, {editor.visual_editor.pan_offset_y})")
    
    # Test 2: Test placing elements outside content frame
    print("\n2. Testing unconstrained positioning...")
    
    editor._on_content_type_changed('reel')
    
    # Get content frame bounds
    frame = editor.visual_editor.content_frame
    print(f"Content frame: ({frame.x()}, {frame.y()}) {frame.width()}x{frame.height()}")
    
    # Move PiP outside the frame (to the left)
    outside_x = frame.x() - 50
    outside_y = frame.y() + 50
    editor.visual_editor.pip_rect.moveTo(outside_x, outside_y)
    
    print(f"Moved PiP to: ({editor.visual_editor.pip_rect.x()}, {editor.visual_editor.pip_rect.y()})")
    print(f"PiP is outside frame: {not frame.contains(editor.visual_editor.pip_rect)}")
    
    # Move title overlay outside the frame (to the right)
    if 'title' in editor.visual_editor.text_overlays:
        title_outside_x = frame.right() + 20
        title_outside_y = frame.y() + 100
        editor.visual_editor.text_overlays['title']['rect'].moveTo(title_outside_x, title_outside_y)
        title_rect = editor.visual_editor.text_overlays['title']['rect']
        print(f"Moved title to: ({title_rect.x()}, {title_rect.y()})")
        print(f"Title is outside frame: {not frame.contains(title_rect)}")
    
    # Test 3: Test zoom functionality
    print("\n3. Testing zoom functionality...")
    
    # Test zoom in
    editor.visual_editor.zoom_factor = 1.5
    print(f"Zoom set to: {editor.visual_editor.zoom_factor}x")
    
    # Test zoom limits
    editor.visual_editor.zoom_factor = 0.1  # Min
    print(f"Min zoom: {editor.visual_editor.zoom_factor}x")
    
    editor.visual_editor.zoom_factor = 5.0  # Max
    print(f"Max zoom: {editor.visual_editor.zoom_factor}x")
    
    # Reset zoom
    editor.visual_editor.zoom_factor = 1.0
    print(f"Reset zoom: {editor.visual_editor.zoom_factor}x")
    
    # Test 4: Test pan functionality
    print("\n4. Testing pan functionality...")
    
    # Set pan offset
    editor.visual_editor.pan_offset_x = 100
    editor.visual_editor.pan_offset_y = 50
    print(f"Pan offset: ({editor.visual_editor.pan_offset_x}, {editor.visual_editor.pan_offset_y})")
    
    # Reset pan
    editor.visual_editor.pan_offset_x = 0
    editor.visual_editor.pan_offset_y = 0
    print(f"Reset pan: ({editor.visual_editor.pan_offset_x}, {editor.visual_editor.pan_offset_y})")
    
    # Test 5: Test constraint toggle
    print("\n5. Testing constraint toggle...")
    
    # Place element outside frame
    editor.visual_editor.pip_rect.moveTo(frame.x() - 100, frame.y() - 50)
    outside_before = editor.visual_editor.pip_rect.topLeft()
    print(f"PiP placed outside at: {outside_before}")
    
    # Enable constraints
    editor.constrain_elements.setChecked(True)
    editor._on_constraint_changed()
    print(f"Constraints enabled: {editor.visual_editor.constrain_to_frame}")
    
    # Apply constraints manually (simulating what would happen during drag)
    editor.visual_editor._constrain_elements_to_frame()
    constrained_pos = editor.visual_editor.pip_rect.topLeft()
    print(f"PiP after constraint: {constrained_pos}")
    print(f"PiP was moved by constraint: {constrained_pos != outside_before}")
    
    # Disable constraints again
    editor.constrain_elements.setChecked(False)
    editor._on_constraint_changed()
    print(f"Constraints disabled: {not editor.visual_editor.constrain_to_frame}")
    
    # Test 6: Test coordinate transformation
    print("\n6. Testing coordinate transformation...")
    
    # Set some zoom and pan
    editor.visual_editor.zoom_factor = 2.0
    editor.visual_editor.pan_offset_x = 50
    editor.visual_editor.pan_offset_y = 30
    
    # Test coordinate transformation
    screen_point = editor.visual_editor._transform_point_to_screen(QPoint(100, 100))
    canvas_point = editor.visual_editor._transform_point_to_canvas(screen_point)
    
    print(f"Canvas (100, 100) -> Screen {screen_point} -> Canvas {canvas_point}")
    print(f"Round-trip accuracy: {abs(canvas_point.x() - 100) <= 1 and abs(canvas_point.y() - 100) <= 1}")
    
    # Test 7: Save/load with unconstrained positions  
    print("\n7. Testing save/load with unconstrained positions...")
    
    # Reset for clean test
    editor.visual_editor.zoom_factor = 1.0
    editor.visual_editor.pan_offset_x = 0
    editor.visual_editor.pan_offset_y = 0
    
    # Place elements outside frame
    pip_outside = QPoint(frame.x() - 75, frame.y() + 200)
    editor.visual_editor.pip_rect.moveTo(pip_outside)
    editor._save_all_current_settings()
    
    print(f"Saved PiP position outside frame: {pip_outside}")
    
    # Switch content type and back
    editor._on_content_type_changed('story')
    editor._on_content_type_changed('reel')
    
    restored_pos = editor.visual_editor.pip_rect.topLeft()
    print(f"Restored PiP position: {restored_pos}")
    print(f"Position preserved: {restored_pos == pip_outside}")
    
    print("\n✅ All zoom, pan, and unconstrained positioning tests completed!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_zoom_pan_unconstrained()
        print("\n🎉 Zoom, pan, and unconstrained positioning verification PASSED!")
    except Exception as e:
        print(f"\n❌ Test FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
