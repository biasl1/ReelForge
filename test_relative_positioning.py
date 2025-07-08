#!/usr/bin/env python3
"""
Test script to verify that element positions remain RELATIVE to the content frame.
This tests the critical resize bug fix!
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def test_relative_positioning():
    """Test that elements maintain relative positions when content frame changes."""
    app = QApplication(sys.argv)
    
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Testing RELATIVE positioning during frame resize...")
    
    visual_editor = editor.visual_editor
    canvas = editor.canvas
    
    # Test 1: Set up initial state
    print("\n1. Setting up initial state...")
    editor._on_content_type_changed('reel')
    
    # Get initial frame and element positions
    initial_frame = QRect(canvas.content_frame)
    initial_pip = QRect(visual_editor.pip_rect)
    initial_title = QRect(visual_editor.text_overlays['title']['rect'])
    
    print(f"  Initial frame: ({initial_frame.x()}, {initial_frame.y()}) {initial_frame.width()}x{initial_frame.height()}")
    print(f"  Initial PiP: ({initial_pip.x()}, {initial_pip.y()}) {initial_pip.width()}x{initial_pip.height()}")
    print(f"  Initial title: ({initial_title.x()}, {initial_title.y()}) {initial_title.width()}x{initial_title.height()}")
    
    # Calculate initial RELATIVE positions (as percentages)
    pip_rel_x = (initial_pip.x() - initial_frame.x()) / initial_frame.width()
    pip_rel_y = (initial_pip.y() - initial_frame.y()) / initial_frame.height()
    pip_rel_w = initial_pip.width() / initial_frame.width()
    pip_rel_h = initial_pip.height() / initial_frame.height()
    
    title_rel_x = (initial_title.x() - initial_frame.x()) / initial_frame.width()
    title_rel_y = (initial_title.y() - initial_frame.y()) / initial_frame.height()
    title_rel_w = initial_title.width() / initial_frame.width()
    title_rel_h = initial_title.height() / initial_frame.height()
    
    print(f"  PiP relative position: {pip_rel_x:.3f}, {pip_rel_y:.3f} (size: {pip_rel_w:.3f}, {pip_rel_h:.3f})")
    print(f"  Title relative position: {title_rel_x:.3f}, {title_rel_y:.3f} (size: {title_rel_w:.3f}, {title_rel_h:.3f})")
    
    # Test 2: Manually move elements to custom positions
    print("\n2. Moving elements to custom positions...")
    
    # Move PiP to 25% from left, 30% from top
    custom_pip_x = initial_frame.x() + (0.25 * initial_frame.width())
    custom_pip_y = initial_frame.y() + (0.30 * initial_frame.height())
    visual_editor.pip_rect.moveTo(int(custom_pip_x), int(custom_pip_y))
    
    # Move title to 10% from left, 60% from top
    custom_title_x = initial_frame.x() + (0.10 * initial_frame.width())
    custom_title_y = initial_frame.y() + (0.60 * initial_frame.height())
    visual_editor.text_overlays['title']['rect'].moveTo(int(custom_title_x), int(custom_title_y))
    
    print(f"  Moved PiP to 25%/30% position: ({custom_pip_x:.0f}, {custom_pip_y:.0f})")
    print(f"  Moved title to 10%/60% position: ({custom_title_x:.0f}, {custom_title_y:.0f})")
    
    # Update the canvas elements
    canvas.elements['pip']['rect'] = visual_editor.pip_rect
    canvas.elements['title']['rect'] = visual_editor.text_overlays['title']['rect']
    
    # Test 3: Simulate content frame resize (like what happens during window resize)
    print("\n3. Simulating content frame resize...")
    
    # Store old frame for comparison
    old_frame = QRect(canvas.content_frame)
    
    # Simulate a resize - make frame larger
    new_frame = QRect(initial_frame.x() + 20, initial_frame.y() + 10, 
                     int(initial_frame.width() * 1.5), int(initial_frame.height() * 1.2))
    canvas.content_frame = new_frame
    
    print(f"  Old frame: ({old_frame.x()}, {old_frame.y()}) {old_frame.width()}x{old_frame.height()}")
    print(f"  New frame: ({new_frame.x()}, {new_frame.y()}) {new_frame.width()}x{new_frame.height()}")
    
    # Apply the update
    canvas._update_elements_for_new_frame(old_frame)
    
    # Test 4: Check if relative positions are maintained
    print("\n4. Checking relative positions after resize...")
    
    # Get updated positions
    updated_pip = canvas.elements['pip']['rect']
    updated_title = canvas.elements['title']['rect']
    
    print(f"  Updated PiP: ({updated_pip.x()}, {updated_pip.y()}) {updated_pip.width()}x{updated_pip.height()}")
    print(f"  Updated title: ({updated_title.x()}, {updated_title.y()}) {updated_title.width()}x{updated_title.height()}")
    
    # Calculate NEW relative positions
    new_pip_rel_x = (updated_pip.x() - new_frame.x()) / new_frame.width()
    new_pip_rel_y = (updated_pip.y() - new_frame.y()) / new_frame.height()
    new_pip_rel_w = updated_pip.width() / new_frame.width()
    new_pip_rel_h = updated_pip.height() / new_frame.height()
    
    new_title_rel_x = (updated_title.x() - new_frame.x()) / new_frame.width()
    new_title_rel_y = (updated_title.y() - new_frame.y()) / new_frame.height()
    new_title_rel_w = updated_title.width() / new_frame.width()
    new_title_rel_h = updated_title.height() / new_frame.height()
    
    print(f"  PiP new relative position: {new_pip_rel_x:.3f}, {new_pip_rel_y:.3f} (size: {new_pip_rel_w:.3f}, {new_pip_rel_h:.3f})")
    print(f"  Title new relative position: {new_title_rel_x:.3f}, {new_title_rel_y:.3f} (size: {new_title_rel_w:.3f}, {new_title_rel_h:.3f})")
    
    # Test 5: Verify relative positions are preserved
    print("\n5. Verifying relative position preservation...")
    
    tolerance = 0.01  # 1% tolerance for floating point precision
    
    # Check PiP position
    pip_x_preserved = abs(new_pip_rel_x - 0.25) < tolerance
    pip_y_preserved = abs(new_pip_rel_y - 0.30) < tolerance
    
    # Check title position  
    title_x_preserved = abs(new_title_rel_x - 0.10) < tolerance
    title_y_preserved = abs(new_title_rel_y - 0.60) < tolerance
    
    print(f"  PiP X position preserved (25%): {pip_x_preserved} (actual: {new_pip_rel_x:.3f})")
    print(f"  PiP Y position preserved (30%): {pip_y_preserved} (actual: {new_pip_rel_y:.3f})")
    print(f"  Title X position preserved (10%): {title_x_preserved} (actual: {new_title_rel_x:.3f})")
    print(f"  Title Y position preserved (60%): {title_y_preserved} (actual: {new_title_rel_y:.3f})")
    
    # Assert all positions are preserved
    assert pip_x_preserved, f"PiP X position not preserved! Expected 0.25, got {new_pip_rel_x:.3f}"
    assert pip_y_preserved, f"PiP Y position not preserved! Expected 0.30, got {new_pip_rel_y:.3f}"
    assert title_x_preserved, f"Title X position not preserved! Expected 0.10, got {new_title_rel_x:.3f}"
    assert title_y_preserved, f"Title Y position not preserved! Expected 0.60, got {new_title_rel_y:.3f}"
    
    print("  ✅ ALL RELATIVE POSITIONS PERFECTLY PRESERVED!")
    
    print("\n✅ RELATIVE POSITIONING TEST PASSED!")
    print("🎯 Elements maintain their relative positions when content frame resizes!")
    
    app.quit()
    return True

if __name__ == "__main__":
    try:
        test_relative_positioning()
        print("\n🔥 RELATIVE POSITIONING VERIFICATION PASSED! 🔥")
        print("📐 Elements now maintain proper relative layout during resize!")
    except Exception as e:
        print(f"\n❌ RELATIVE POSITIONING VERIFICATION FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
