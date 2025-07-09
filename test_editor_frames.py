#!/usr/bin/env python3
"""
Test that demonstrates frame independence working in the actual template editor
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from ui.template_editor import TemplateEditor

def test_editor_frame_independence():
    """Test frame independence in the actual template editor"""
    app = QApplication([])
    
    editor = TemplateEditor()
    
    print("🎬 TESTING TEMPLATE EDITOR FRAME INDEPENDENCE")
    print("=" * 60)
    
    # Set to video content type
    editor.set_content_type("story")
    
    # Test frame 0
    print("\n📝 Testing Frame 0:")
    editor.frame_timeline._on_frame_selected(0)
    frame0_positions = {}
    for elem_id, elem in editor.canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame0_positions[elem_id] = pos
        print(f"   {elem_id}: {pos}")
    
    # Test frame 1
    print("\n📝 Testing Frame 1:")
    editor.frame_timeline._on_frame_selected(1)
    frame1_positions = {}
    for elem_id, elem in editor.canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame1_positions[elem_id] = pos
        print(f"   {elem_id}: {pos}")
    
    # Test frame 2
    print("\n📝 Testing Frame 2:")
    editor.frame_timeline._on_frame_selected(2)
    frame2_positions = {}
    for elem_id, elem in editor.canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame2_positions[elem_id] = pos
        print(f"   {elem_id}: {pos}")
    
    # Verify independence
    print("\n🔍 VERIFYING INDEPENDENCE:")
    print("=" * 40)
    
    all_independent = True
    for elem_id in frame0_positions:
        if elem_id in frame1_positions and elem_id in frame2_positions:
            pos0 = frame0_positions[elem_id]
            pos1 = frame1_positions[elem_id]
            pos2 = frame2_positions[elem_id]
            
            if pos0 == pos1 == pos2:
                print(f"❌ {elem_id}: ALL FRAMES HAVE SAME POSITION {pos0}")
                all_independent = False
            else:
                print(f"✅ {elem_id}: INDEPENDENT - F0:{pos0}, F1:{pos1}, F2:{pos2}")
    
    if all_independent:
        print(f"\n🎉 SUCCESS! ALL FRAMES ARE INDEPENDENT!")
        print("🎬 Each frame has unique element positions!")
        print("👆 When you click Frame 1, move elements, then click Frame 2, they will be different!")
    else:
        print(f"\n💥 FAILED! Frames are not independent!")
    
    app.quit()
    return all_independent

if __name__ == "__main__":
    success = test_editor_frame_independence()
    if success:
        print("\n✅ FRAME INDEPENDENCE IS WORKING CORRECTLY!")
        print("🎬 You can now click different frames and each will have unique positions!")
    else:
        print("\n❌ Frame independence needs more work")
