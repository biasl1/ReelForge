#!/usr/bin/env python3

"""
Test script to verify frame count export issue is fixed
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def test_frame_count_export():
    """Test that all frames are properly exported even when some frames have no data."""
    
    # Load the project
    project_path = "/Users/test/Documents/ReelForge Projects/Test1.rforge"
    
    if not os.path.exists(project_path):
        print(f"❌ Project file not found: {project_path}")
        return False
    
    project = ReelForgeProject.load(project_path)
    
    if not project:
        print("❌ Failed to load project")
        return False
    
    print(f"✅ Loaded project: {project.project_name}")
    
    # Check each event's frame count vs exported frames
    for event_id, event in project.release_events.items():
        print(f"\n📋 Event: {event.title} (ID: {event_id})")
        print(f"   Content Type: {event.content_type}")
        print(f"   Frame Count: {event.frame_count}")
        
        # Check frame data in template_config
        frame_data = event.template_config.get('frame_data', {})
        exported_frames = len(frame_data)
        
        print(f"   Exported Frames: {exported_frames}")
        print(f"   Frame Keys: {list(frame_data.keys())}")
        
        if event.frame_count != exported_frames:
            print(f"   ❌ MISMATCH: frame_count={event.frame_count} but exported={exported_frames}")
            
            # Show what frames are missing
            for i in range(event.frame_count):
                frame_key = str(i)
                if frame_key not in frame_data:
                    print(f"      ❌ Missing frame {i}")
                else:
                    elements = frame_data[frame_key].get('elements', {})
                    print(f"      ✅ Frame {i}: {len(elements)} elements")
        else:
            print(f"   ✅ Frame count matches exported frames")
    
    # Test AI export
    print(f"\n🤖 Testing AI export...")
    ai_data = project.get_ai_generation_data()
    
    templates = ai_data.get('content_generation', {}).get('templates', {})
    print(f"   Exported {len(templates)} templates")
    
    for template_key, template_data in templates.items():
        print(f"\n   Template: {template_key}")
        print(f"   Event ID: {template_data.get('event_id')}")
        print(f"   Frame Count: {template_data.get('frame_count')}")
        
        frame_data = template_data.get('template_config', {}).get('frame_data', {})
        exported_frames = len(frame_data)
        
        print(f"   Exported Frames: {exported_frames}")
        
        expected_frame_count = template_data.get('frame_count', 1)
        if expected_frame_count != exported_frames:
            print(f"   ❌ MISMATCH: Expected {expected_frame_count} frames but got {exported_frames}")
            return False
        else:
            print(f"   ✅ Frame count matches exported frames")
    
    print(f"\n✅ All frame count tests passed!")
    return True

if __name__ == "__main__":
    success = test_frame_count_export()
    sys.exit(0 if success else 1)
