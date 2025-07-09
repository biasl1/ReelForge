#!/usr/bin/env python3
"""
Debug script to test the frame initialization and switching issue.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor.frame_timeline import FrameTimeline
from ui.template_editor.canvas import TemplateCanvas
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

def test_frame_issue():
    """Test the frame initialization and content type switching."""
    app = QApplication(sys.argv)
    
    # Create timeline and canvas
    timeline = FrameTimeline()
    canvas = TemplateCanvas()
    
    # Connect timeline to canvas
    timeline.set_canvas(canvas)
    
    print("=== INITIAL STATE ===")
    print(f"Timeline frames: {len(timeline.frames)}")
    print(f"Current frame: {timeline.current_frame}")
    
    # Test setting content type to reel (should have only 1 frame)
    print("\n=== SETTING CONTENT TYPE TO REEL ===")
    timeline.set_content_type_frames('reel')
    
    print(f"Timeline frames after setting reel: {len(timeline.frames)}")
    print(f"Current frame: {timeline.current_frame}")
    
    # Test frame switching - this should NOT go to frame 1 for reel
    print("\n=== TESTING FRAME SWITCHING ===")
    if len(timeline.frames) > 1:
        print("ERROR: Reel should only have 1 frame, but timeline has multiple frames!")
        print(f"Frame buttons: {len(timeline.frame_buttons)}")
    
    # Test accessing non-existent frame
    print("\n=== TESTING CANVAS STATES ===")
    canvas.set_content_type('reel')
    
    print(f"Canvas content type: {canvas.content_type}")
    print(f"Canvas current frame: {canvas.current_frame}")
    
    # Test getting frame data for frame 0 (should exist)
    frame_0_data = canvas.get_current_frame_data()
    print(f"Frame 0 data exists: {frame_0_data is not None}")
    
    # Test getting frame data for frame 1 (should NOT exist for reel)
    canvas.current_frame = 1
    frame_1_data = canvas.get_current_frame_data()
    print(f"Frame 1 data exists: {frame_1_data is not None}")
    print(f"Frame 1 data: {frame_1_data}")
    
    # Test the _load_current_frame_state with invalid frame
    print("\n=== TESTING FRAME LOADING ===")
    canvas.current_frame = 1  # This should not exist for reel
    try:
        canvas._load_current_frame_state()
        print("Frame 1 loaded successfully (this should not happen for reel)")
    except Exception as e:
        print(f"Error loading frame 1: {e}")
    
    app.quit()

if __name__ == "__main__":
    test_frame_issue()
