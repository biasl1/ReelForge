#!/usr/bin/env python3

"""
Test script to manually trigger frame creation for missing frames
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def fix_missing_frames():
    """Fix missing frames by manually creating them."""
    
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
    
    # Find the event with missing frames
    problem_event = None
    for event_id, event in project.release_events.items():
        frame_data = event.template_config.get('frame_data', {})
        exported_frames = len(frame_data)
        
        if event.frame_count != exported_frames:
            problem_event = event
            break
    
    if not problem_event:
        print("✅ No missing frames found")
        return True
    
    print(f"\n🔧 Found event with missing frames: {problem_event.title}")
    print(f"   Frame count: {problem_event.frame_count}")
    print(f"   Exported frames: {len(problem_event.template_config.get('frame_data', {}))}")
    
    # Manually create missing frames
    frame_data = problem_event.template_config.get('frame_data', {})
    if 'frame_data' not in problem_event.template_config:
        problem_event.template_config['frame_data'] = {}
    
    # Create default elements for video content type
    default_elements = {
        "pip": {
            "type": "pip",
            "content": "",
            "font_size": 12,
            "position_preset": "center",
            "visible": True,
            "corner_radius": 0
        },
        "title": {
            "type": "text",
            "content": "Video Title",
            "font_size": 30,
            "position_preset": "top",
            "visible": True
        },
        "subtitle": {
            "type": "text",
            "content": "Subtitle",
            "font_size": 20,
            "position_preset": "bottom",
            "visible": True
        }
    }
    
    # Create all missing frames
    for i in range(problem_event.frame_count):
        frame_key = str(i)
        if frame_key not in frame_data:
            print(f"   🔧 Creating frame {i}")
            
            new_frame_data = {
                "frame_index": i,
                "frame_description": f"Video frame {i + 1}",
                "elements": default_elements.copy(),
                "timestamp": "2025-07-15T14:15:00.000000"
            }
            
            problem_event.template_config['frame_data'][frame_key] = new_frame_data
        else:
            print(f"   ✅ Frame {i} already exists")
    
    # Save the project
    project.save()
    print(f"✅ Project saved with all frames created")
    
    # Test the export again
    print(f"\n🤖 Testing AI export after fix...")
    ai_data = project.get_ai_generation_data()
    
    templates = ai_data.get('content_generation', {}).get('templates', {})
    
    for template_key, template_data in templates.items():
        if template_data.get('event_id') == problem_event.id:
            print(f"\n   Template: {template_key}")
            print(f"   Event ID: {template_data.get('event_id')}")
            print(f"   Frame Count: {template_data.get('frame_count')}")
            
            frame_data = template_data.get('template_config', {}).get('frame_data', {})
            exported_frames = len(frame_data)
            
            print(f"   Exported Frames: {exported_frames}")
            print(f"   Frame Keys: {list(frame_data.keys())}")
            
            expected_frame_count = template_data.get('frame_count', 1)
            if expected_frame_count != exported_frames:
                print(f"   ❌ STILL MISMATCH: Expected {expected_frame_count} frames but got {exported_frames}")
                return False
            else:
                print(f"   ✅ Frame count now matches exported frames!")
    
    return True

if __name__ == "__main__":
    success = fix_missing_frames()
    sys.exit(0 if success else 1)
