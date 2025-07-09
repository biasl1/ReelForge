#!/usr/bin/env python3
"""
Test script to verify that each content type has independent frame counts.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.frame_timeline import FrameTimeline
from ui.template_editor.canvas import TemplateCanvas


def test_content_type_frame_counts():
    """Test that each content type gets the correct frame count."""
    app = QApplication(sys.argv)
    
    # Test FrameTimeline
    print("🎬 Testing FrameTimeline content type frame counts...")
    timeline = FrameTimeline()
    
    # Expected frame counts per content type
    expected_counts = {
        'reel': 1,
        'story': 5, 
        'tutorial': 8,
        'post': 1,
        'teaser': 1
    }
    
    for content_type, expected_count in expected_counts.items():
        print(f"\n📌 Testing {content_type}:")
        timeline.set_content_type_frames(content_type)
        actual_count = timeline.get_frame_count()
        
        print(f"   Expected: {expected_count}, Got: {actual_count}")
        
        if actual_count == expected_count:
            print(f"   ✅ {content_type} has correct frame count: {actual_count}")
        else:
            print(f"   ❌ {content_type} has wrong frame count: expected {expected_count}, got {actual_count}")
    
    # Test TemplateCanvas
    print("\n🎨 Testing TemplateCanvas content type frame counts...")
    canvas = TemplateCanvas()
    
    for content_type, expected_count in expected_counts.items():
        print(f"\n📌 Testing {content_type}:")
        actual_count = canvas.get_content_type_frame_count(content_type)
        
        print(f"   Expected: {expected_count}, Got: {actual_count}")
        
        if actual_count == expected_count:
            print(f"   ✅ {content_type} has correct frame count: {actual_count}")
        else:
            print(f"   ❌ {content_type} has wrong frame count: expected {expected_count}, got {actual_count}")
    
    # Test content type switching on canvas
    print("\n🔄 Testing content type switching on canvas...")
    for content_type in expected_counts.keys():
        print(f"\n📌 Switching canvas to {content_type}:")
        canvas.set_content_type(content_type)
        
        if canvas.is_video_content_type(content_type):
            state = canvas.content_states.get(content_type, {})
            frame_count = state.get('frame_count', 0)
            frames = state.get('frames', {})
            
            print(f"   Frame count in state: {frame_count}")
            print(f"   Actual frames available: {len(frames)}")
            print(f"   Current frame: {canvas.current_frame}")
            print(f"   Is video type: {canvas.is_video_content_type(content_type)}")
            
            if frame_count == expected_counts[content_type]:
                print(f"   ✅ {content_type} correctly initialized")
            else:
                print(f"   ❌ {content_type} incorrectly initialized")
        else:
            print(f"   📄 {content_type} is static content (correct)")
    
    print("\n🎯 Frame independence test complete!")
    

if __name__ == "__main__":
    test_content_type_frame_counts()
