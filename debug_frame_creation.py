#!/usr/bin/env python3
"""
Debug script to trace frame creation step by step
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from ui.template_editor.canvas import TemplateCanvas

def debug_frame_creation():
    """Debug frame creation step by step"""
    app = QApplication([])
    
    canvas = TemplateCanvas()
    canvas.set_content_type("story")  # Video content type
    
    print("🔍 DEBUGGING FRAME CREATION")
    print("=" * 50)
    
    # Check initial state
    print(f"Initial current_frame: {canvas.current_frame}")
    print(f"Initial elements: {list(canvas.elements.keys())}")
    
    # Set to frame 0 and check elements
    print("\n📝 Setting to frame 0...")
    canvas.set_current_frame(0)
    frame0_positions = {}
    for elem_id, elem in canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame0_positions[elem_id] = pos
        print(f"   Frame 0 - {elem_id}: {pos}")
    
    # Set to frame 1 and check elements
    print("\n📝 Setting to frame 1...")
    canvas.set_current_frame(1)
    frame1_positions = {}
    for elem_id, elem in canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame1_positions[elem_id] = pos
        print(f"   Frame 1 - {elem_id}: {pos}")
    
    # Set to frame 2 and check elements
    print("\n📝 Setting to frame 2...")
    canvas.set_current_frame(2)
    frame2_positions = {}
    for elem_id, elem in canvas.elements.items():
        pos = (elem['rect'].x(), elem['rect'].y())
        frame2_positions[elem_id] = pos
        print(f"   Frame 2 - {elem_id}: {pos}")
    
    # Check for duplicates
    print("\n🔍 CHECKING FOR INDEPENDENCE:")
    print("=" * 50)
    
    all_different = True
    for elem_id in frame0_positions:
        if elem_id in frame1_positions and elem_id in frame2_positions:
            pos0 = frame0_positions[elem_id]
            pos1 = frame1_positions[elem_id]
            pos2 = frame2_positions[elem_id]
            
            if pos0 == pos1 == pos2:
                print(f"❌ {elem_id}: ALL SAME {pos0}")
                all_different = False
            elif pos0 == pos1:
                print(f"⚠️  {elem_id}: Frame 0&1 same {pos0}, Frame 2 different {pos2}")
                all_different = False
            elif pos0 == pos2:
                print(f"⚠️  {elem_id}: Frame 0&2 same {pos0}, Frame 1 different {pos1}")
                all_different = False
            elif pos1 == pos2:
                print(f"⚠️  {elem_id}: Frame 1&2 same {pos1}, Frame 0 different {pos0}")
                all_different = False
            else:
                print(f"✅ {elem_id}: All different - Frame 0:{pos0}, Frame 1:{pos1}, Frame 2:{pos2}")
    
    if all_different:
        print("\n🎉 SUCCESS: All frames have INDEPENDENT positions!")
    else:
        print("\n💥 FAILURE: Frames are not independent!")
    
    app.quit()
    return all_different

if __name__ == "__main__":
    debug_frame_creation()
