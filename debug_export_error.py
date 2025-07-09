#!/usr/bin/env python3
"""
Debug script to reproduce the 'list' object has no attribute 'get' error
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from core.project import ReelForgeProject
from ui.template_editor.editor import TemplateEditor
import traceback

def main():
    print("=== Debug Export Error Script ===")
    app = QApplication(sys.argv)
    
    try:
        # Create a new project
        project = ReelForgeProject()
        project.metadata.name = "Debug Export Test"
        
        # Add some test events to trigger template export
        from core.project import ReleaseEvent
        from datetime import datetime
        
        event = ReleaseEvent(
            id="test_event_1",
            date=datetime.now().date().isoformat(),  # Convert to string
            content_type="reel",
            title="Test Reel",
            description="Test prompt for debugging",
            platforms=["instagram"]
        )
        project.add_release_event(event)
        
        # Create template editor
        template_editor = TemplateEditor()
        template_editor.set_content_type("reel")
        
        # Add some elements to create frames data
        from PyQt6.QtCore import QRect
        from PyQt6.QtGui import QColor
        
        # Directly add elements to the canvas to trigger the export issue
        template_editor.canvas.elements['title'] = {
            'type': 'text',
            'rect': QRect(50, 100, 300, 80),
            'content': "Test Title",
            'color': QColor(255, 255, 255),
            'size': 24,
            'style': 'normal',
            'enabled': True
        }
        
        # Try to export - this should trigger the error
        print("Attempting to export AI generation data...")
        
        # First let's see what the template editor exports
        export_data = template_editor.export_template_data()
        print("Template editor export data structure:")
        print(f"Type: {type(export_data)}")
        
        if isinstance(export_data, dict):
            for key, value in export_data.items():
                print(f"  {key}: {type(value)}")
                if isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        print(f"    {sub_key}: {type(sub_value)}")
                        if sub_key == 'frames' and hasattr(sub_value, 'items'):
                            for frame_key, frame_value in sub_value.items():
                                print(f"      {frame_key}: {type(frame_value)}")
                                if hasattr(frame_value, 'items'):
                                    for frame_sub_key, frame_sub_value in frame_value.items():
                                        print(f"        {frame_sub_key}: {type(frame_sub_value)}")
        
        # Now try the actual export that's failing
        result = project.export_ai_data_to_json("debug_export.json", template_editor)
        print(f"Export result: {result}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()
        
        # Try to analyze what caused the error
        import re
        error_str = str(e)
        if "'list' object has no attribute 'get'" in error_str:
            print("\n=== FOUND THE LIST/GET ERROR ===")
            print("This error occurs when a list is passed where a dict is expected")
            print("Looking for where .get() is called on something that should be a dict but is a list")

if __name__ == "__main__":
    main()
