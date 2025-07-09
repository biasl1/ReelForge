#!/usr/bin/env python3
"""
Debug script to trace the frame initialization issue.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.template_editor.canvas import TemplateCanvas
from PyQt6.QtWidgets import QApplication

def debug_canvas_initialization():
    """Debug the canvas initialization."""
    app = QApplication(sys.argv)
    
    canvas = TemplateCanvas()
    
    print("=== CANVAS INITIALIZATION ===")
    print(f"Canvas content type: {canvas.content_type}")
    print(f"Canvas current frame: {canvas.current_frame}")
    print(f"Content states: {list(canvas.content_states.keys())}")
    
    # Check reel state
    reel_state = canvas.content_states.get('reel', {})
    print(f"Reel state: {reel_state}")
    
    if 'frames' in reel_state:
        frames = reel_state['frames']
        print(f"Reel frames: {frames}")
        print(f"Frame 0 exists: {0 in frames}")
        if 0 in frames:
            print(f"Frame 0 data: {frames[0]}")
    
    # Test get_current_frame_data
    print("\n=== TESTING get_current_frame_data ===")
    canvas.content_type = 'reel'
    canvas.current_frame = 0
    
    frame_data = canvas.get_current_frame_data()
    print(f"Frame data for frame 0: {frame_data}")
    print(f"Frame data is None: {frame_data is None}")
    
    if frame_data:
        print(f"Frame 0 elements: {frame_data.get('elements', {})}")
    
    app.quit()

if __name__ == "__main__":
    debug_canvas_initialization()
