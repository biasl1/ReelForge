#!/usr/bin/env python3
"""
Test script to verify save/load functionality with independent frame counts.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from ui.template_editor.canvas import TemplateCanvas
import copy


def test_save_load_with_frame_independence():
    """Test that save/load preserves independent frame counts and data."""
    app = QApplication(sys.argv)
    
    print("🎬 Testing save/load with independent frame counts...")
    
    canvas = TemplateCanvas()
    
    # Test each content type
    content_types = ['reel', 'story', 'tutorial', 'post', 'teaser']
    saved_configs = {}
    
    # Save configuration for each content type
    for content_type in content_types:
        print(f"\n📌 Testing {content_type}:")
        canvas.set_content_type(content_type)
        
        if canvas.is_video_content_type(content_type):
            # For video types, modify elements in different frames
            state = canvas.content_states[content_type]
            frame_count = state['frame_count']
            
            print(f"   📹 Video type with {frame_count} frames")
            
            # Modify elements in each frame to make them unique
            for frame_idx in range(frame_count):
                canvas.set_current_frame(frame_idx)
                
                # Modify PiP position to be unique per frame
                if 'pip' in canvas.elements:
                    canvas.elements['pip']['rect'] = QRect(100 + frame_idx * 50, 100 + frame_idx * 30, 120, 100)
                
                # Modify title content to be unique per frame  
                if 'title' in canvas.elements:
                    canvas.elements['title']['content'] = f"{content_type} Frame {frame_idx} Title"
                
                print(f"      Frame {frame_idx}: Modified elements")
            
            # Save current frame state
            canvas._save_current_frame_state()
        else:
            print(f"   📄 Static type")
            # For static types, just modify elements
            if 'pip' in canvas.elements:
                canvas.elements['pip']['rect'] = QRect(200, 200, 150, 120)
            if 'title' in canvas.elements:
                canvas.elements['title']['content'] = f"{content_type} Static Title"
            
            canvas._save_current_state()
        
        # Get the complete configuration
        config = canvas.get_element_config()
        saved_configs[content_type] = copy.deepcopy(config)
        
        print(f"   💾 Saved configuration for {content_type}")
        if canvas.is_video_content_type(content_type) and 'frames' in config:
            print(f"      Frames in config: {len(config['frames'])}")
        
    # Now test loading each configuration back
    print(f"\n🔄 Testing configuration loading...")
    
    for content_type, saved_config in saved_configs.items():
        print(f"\n📌 Loading {content_type}:")
        
        # Clear canvas and set different content type first
        canvas.set_content_type('reel' if content_type != 'reel' else 'story')
        
        # Load the saved configuration
        canvas.set_element_config(saved_config)
        
        # Verify the configuration was loaded correctly
        if canvas.is_video_content_type(content_type):
            state = canvas.content_states[content_type]
            expected_frame_count = canvas.get_content_type_frame_count(content_type)
            actual_frame_count = state.get('frame_count', 0)
            
            print(f"   📹 Expected {expected_frame_count} frames, got {actual_frame_count}")
            
            if actual_frame_count == expected_frame_count:
                print(f"   ✅ Frame count correct")
                
                # Check frame data
                frames = state.get('frames', {})
                for frame_idx in range(actual_frame_count):
                    if frame_idx in frames:
                        frame_data = frames[frame_idx]
                        elements = frame_data.get('elements', {})
                        if 'title' in elements:
                            title_content = elements['title'].get('content', '')
                            print(f"      Frame {frame_idx}: '{title_content}'")
                        print(f"      Frame {frame_idx}: {len(elements)} elements")
                    else:
                        print(f"      Frame {frame_idx}: MISSING")
            else:
                print(f"   ❌ Frame count mismatch")
        else:
            print(f"   📄 Static content loaded")
            if 'title' in canvas.elements:
                title_content = canvas.elements['title'].get('content', '')
                print(f"      Title: '{title_content}'")
    
    print(f"\n🎯 Save/load frame independence test complete!")


if __name__ == "__main__":
    test_save_load_with_frame_independence()
