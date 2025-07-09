#!/usr/bin/env python3
"""
Specific test to reproduce the 'list' object has no attribute 'get' error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from core.project import ReelForgeProject, convert_enums
from ui.template_editor.editor import TemplateEditor
import traceback
import json

def test_conversion_error():
    print("=== Testing Conversion Error ===")
    
    # Create a frame data structure like what the canvas saves
    from PyQt6.QtCore import QRect
    
    frame_data = {
        'elements': {'title': {'type': 'text', 'content': 'test'}},
        'content_frame': QRect(50, 50, 300, 500),  # This is a QRect!
        'constrain_to_frame': False,
        'frame_description': 'Test frame'
    }
    
    print("Original frame data:")
    print(f"  content_frame type: {type(frame_data['content_frame'])}")
    
    # Convert through convert_enums (this is what happens during export)
    converted_frame_data = convert_enums(frame_data)
    
    print("After convert_enums:")
    print(f"  content_frame type: {type(converted_frame_data['content_frame'])}")
    print(f"  content_frame value: {converted_frame_data['content_frame']}")
    
    # Now try to access like the export code does
    try:
        elements = converted_frame_data.get('elements', {})
        print("✓ Successfully accessed elements")
    except Exception as e:
        print(f"✗ Error accessing elements: {e}")
    
    # Let's also test if somehow the ENTIRE frame data becomes a list
    print("\n=== Testing if frame data becomes a list ===")
    
    frames_dict = {
        0: frame_data,
        1: frame_data
    }
    
    converted_frames = convert_enums(frames_dict)
    print(f"Converted frames structure:")
    for key, value in converted_frames.items():
        print(f"  {key}: {type(value)}")
        if hasattr(value, 'get'):
            print(f"    Has 'get' method: ✓")
        else:
            print(f"    Has 'get' method: ✗")
            print(f"    Trying to call .get() on this will fail!")
            try:
                value.get('elements', {})
            except Exception as e:
                print(f"    Error: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    test_conversion_error()
