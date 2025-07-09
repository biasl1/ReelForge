#!/usr/bin/env python3
"""
Test script to verify frame independence - each frame has unique element positions.
"""
import sys
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

def test_frame_independence():
    """Test that each frame has independent element positions."""
    app = QApplication([])
    
    from ui.template_editor import TemplateEditor
    
    # Create template editor
    editor = TemplateEditor()
    editor.show()
    
    print("🎬 Testing Frame Independence...")
    
    # Set to story (video content type)
    editor.set_content_type("story")
    
    # Test frames 0, 1, 2
    frame_positions = {}
    
    for frame_idx in range(3):
        print(f"\n📝 Testing Frame {frame_idx}:")
        
        # Switch to frame
        editor.frame_timeline._on_frame_selected(frame_idx)
        editor._load_frame_elements(frame_idx)
        
        # Get element positions
        config = editor.canvas.get_element_config()
        frame_positions[frame_idx] = {}
        
        if 'elements' in config:
            for element_id, element_data in config['elements'].items():
                if 'rect' in element_data:
                    rect = element_data['rect']
                    frame_positions[frame_idx][element_id] = (rect.x(), rect.y())
                    print(f"   {element_id}: position ({rect.x()}, {rect.y()})")
    
    # Verify independence
    print("\n🔍 Verifying Frame Independence:")
    independent = True
    
    for element_id in ['title', 'subtitle', 'pip']:
        positions = []
        for frame_idx in range(3):
            if element_id in frame_positions[frame_idx]:
                pos = frame_positions[frame_idx][element_id]
                positions.append(pos)
        
        # Check if all positions are different
        unique_positions = set(positions)
        if len(unique_positions) == len(positions):
            print(f"✅ {element_id}: INDEPENDENT positions {positions}")
        else:
            print(f"❌ {element_id}: DUPLICATE positions {positions}")
            independent = False
    
    if independent:
        print("\n🎉 SUCCESS: All frames have INDEPENDENT element positions!")
    else:
        print("\n💥 FAIL: Frames are not independent!")
    
    app.quit()
    return independent

if __name__ == "__main__":
    success = test_frame_independence()
    sys.exit(0 if success else 1)
