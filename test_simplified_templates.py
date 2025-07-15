#!/usr/bin/env python3
"""
Test script to verify the simplified template system works correctly.
"""

import json
import sys
import os
sys.path.insert(0, os.path.abspath('.'))

from core.project import Project

def test_template_persistence():
    """Test that template data is saved and loaded correctly."""
    
    # Create a test project
    project = Project()
    project.project_name = "Test Simplified Templates"
    
    # Create test events
    video_event = project.create_event("TEST_VIDEO", "VIDEO", "Test Video Content")
    
    # Create simplified template data
    template_data = {
        "frame_1": {
            "title": {
                "type": "text",
                "content": "My Video Title",
                "font_size": 24,
                "position_preset": "top",
                "visible": True
            },
            "description": {
                "type": "text", 
                "content": "Video description here",
                "font_size": 16,
                "position_preset": "bottom",
                "visible": True
            }
        }
    }
    
    # Set template data
    video_event.template_config = template_data
    
    # Save project
    project.save_project("test_simplified.rforge")
    
    # Load project
    loaded_project = Project()
    loaded_project.load_project("test_simplified.rforge")
    
    # Verify the data
    loaded_event = loaded_project.get_event("TEST_VIDEO")
    loaded_template = loaded_event.template_config
    
    print("Original template data:")
    print(json.dumps(template_data, indent=2))
    
    print("\nLoaded template data:")
    print(json.dumps(loaded_template, indent=2))
    
    # Verify key properties
    frame_1 = loaded_template["frame_1"]
    title = frame_1["title"]
    description = frame_1["description"]
    
    assert title["content"] == "My Video Title"
    assert title["position_preset"] == "top"
    assert title["visible"] is True
    
    assert description["content"] == "Video description here"
    assert description["position_preset"] == "bottom"
    assert description["visible"] is True
    
    print("\n✅ Template persistence test PASSED!")
    
    # Clean up
    os.remove("test_simplified.rforge")

if __name__ == "__main__":
    test_template_persistence()
