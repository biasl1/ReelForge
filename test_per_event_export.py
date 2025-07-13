#!/usr/bin/env python3
"""Test script to verify per-event template export functionality"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def test_per_event_export():
    """Test that each event gets its own template in export"""
    
    # Load the project
    project_path = "/Users/test/Documents/ReelForge Projects/Test1.rforge"
    project = ReelForgeProject()
    
    if not project.load_project(project_path):
        print("❌ Failed to load project")
        return False
    
    print(f"✅ Project loaded: {project.name}")
    print(f"📅 Events found: {len(project.release_events)}")
    
    # List events
    for event_id, event in project.release_events.items():
        print(f"  - Event {event_id}: {event.title} ({event.content_type})")
    
    # Export AI data
    ai_data = project.get_ai_generation_data()
    templates = ai_data.get('content_generation', {}).get('templates', {})
    
    print(f"\n📊 Templates exported: {len(templates)}")
    
    # Check if we have per-event templates
    for template_key, template_data in templates.items():
        print(f"  - Template '{template_key}':")
        print(f"    Event ID: {template_data.get('event_id', 'N/A')}")
        print(f"    Event Title: {template_data.get('event_title', 'N/A')}")
        print(f"    Content Type: {template_data.get('content_type', 'N/A')}")
        print(f"    Frame Count: {template_data.get('frame_count', 'N/A')}")
        print(f"    Has template_config: {'template_config' in template_data}")
        
        if 'template_config' in template_data:
            frame_data = template_data['template_config'].get('frame_data', {})
            print(f"    Frames: {len(frame_data)}")
    
    # Test if we have multiple events with different templates
    if len(templates) >= 2:
        print("\n✅ SUCCESS: Multiple per-event templates exported!")
        return True
    else:
        print("\n❌ FAIL: Only one template exported, should have per-event templates")
        return False

if __name__ == "__main__":
    success = test_per_event_export()
    sys.exit(0 if success else 1)
