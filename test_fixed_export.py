#!/usr/bin/env python3
"""
Test script to verify that our defensive programming fixes prevent the
'list' object has no attribute 'get' error when exporting AI data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor
from core.project import ReelForgeProject, convert_enums
import traceback
import json

def create_test_data():
    """Create test data that would normally cause the error"""
    # Create frame data where rect is a QRect object
    normal_frame = {
        'elements': {'title': {'type': 'text', 'content': 'Normal Title'}},
        'content_frame': QRect(50, 50, 300, 500),
        'constrain_to_frame': False,
        'frame_description': 'Normal frame'
    }
    
    # Create frame data where elements is a list instead of dict
    bad_elements_frame = {
        'elements': [
            ('title', {'type': 'text', 'content': 'Bad Elements'}),
            ('subtitle', {'type': 'text', 'content': 'This should fail'})
        ],
        'content_frame': QRect(50, 50, 300, 500),
        'constrain_to_frame': False,
        'frame_description': 'Bad elements frame'
    }
    
    # Create frame data that is itself a list
    list_frame = [50, 50, 300, 500]
    
    # Create frames structure
    frames = {
        0: normal_frame,
        1: bad_elements_frame,
        2: list_frame
    }
    
    return frames

def test_export():
    print("=== Testing Fixed Export Logic ===")
    app = QApplication(sys.argv)
    
    try:
        # Create a project
        project = ReelForgeProject()
        project.metadata.name = "Fixed Export Test"
        
        # Add a test event
        from core.project import ReleaseEvent
        from datetime import datetime
        
        event = ReleaseEvent(
            id="test_event_1",
            date=datetime.now().date().isoformat(),
            content_type="reel",
            title="Test Reel",
            description="Test prompt for debugging",
            platforms=["instagram"]
        )
        project.add_release_event(event)
        
        # Create mock template editor
        class MockTemplateEditor:
            def __init__(self):
                self.content_type = "reel"
            
            def get_content_type(self):
                return self.content_type
            
            def set_content_type(self, content_type):
                self.content_type = content_type
            
            def export_template_data(self):
                # Return data that would normally cause the error
                frames = create_test_data()
                
                return {
                    'canvas_config': {
                        'elements': {'title': {'type': 'text', 'content': 'Global Title'}},
                        'frames': frames,
                        'settings': {'aspect_ratio': '9:16'}
                    }
                }
        
        template_editor = MockTemplateEditor()
        
        # Test the export
        print("Attempting to export AI generation data with problematic frames...")
        result = project.export_ai_data_to_json("test_fixed_export.json", template_editor)
        
        if result:
            print("✓ Export completed successfully!")
            print("Our defensive programming fixes are working")
            
            # Check that the file was created
            if os.path.exists("test_fixed_export.json"):
                print("✓ Export file was created")
                
                # Load and verify the JSON
                with open("test_fixed_export.json", "r") as f:
                    data = json.load(f)
                
                if "content_generation" in data and "templates" in data["content_generation"]:
                    templates = data["content_generation"]["templates"]
                    print(f"✓ Templates exported: {list(templates.keys())}")
                    
                    # Check reel template
                    if "reel" in templates:
                        reel = templates["reel"]
                        if "is_video_content" in reel and reel["is_video_content"] and "frames" in reel:
                            frames = reel["frames"]
                            print(f"✓ Frames exported: {len(frames)}")
                            
                            # Check frame structure
                            for frame_id, frame in frames.items():
                                print(f"  - {frame_id}: {frame.get('name')}")
            else:
                print("✗ Export file was not created")
        else:
            print("✗ Export failed")
            print("Our defensive programming fixes are not complete")
    
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    test_export()
