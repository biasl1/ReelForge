#!/usr/bin/env python3

"""
Test script to export complete AI data and show the results
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def test_complete_ai_export():
    """Test complete AI export with all frames and clean data."""
    
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
    
    # Test AI export
    print(f"\n🤖 Generating complete AI export...")
    ai_data = project.get_ai_generation_data()
    
    # Save to file for inspection
    output_file = "/Users/test/Documents/development/Artists in DSP/ReelTune/output/complete_ai_export.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(ai_data, f, indent=2)
    
    print(f"✅ AI export saved to: {output_file}")
    
    # Show summary
    templates = ai_data.get('content_generation', {}).get('templates', {})
    print(f"\n📋 Export Summary:")
    print(f"   Total templates: {len(templates)}")
    
    for template_key, template_data in templates.items():
        event_title = template_data.get('event_title', 'Unknown')
        frame_count = template_data.get('frame_count', 0)
        
        print(f"\n   📄 Template: {template_key}")
        print(f"      Event: {event_title}")
        print(f"      Frame Count: {frame_count}")
        
        frame_data = template_data.get('template_config', {}).get('frame_data', {})
        print(f"      Exported Frames: {len(frame_data)}")
        
        # Check each frame
        for frame_key, frame_info in frame_data.items():
            elements = frame_info.get('elements', {})
            print(f"         Frame {frame_key}: {len(elements)} elements")
            
            # Check for clean data (no unnecessary properties)
            for element_id, element_data in elements.items():
                unnecessary_props = []
                for prop in ['rect', 'enabled', 'color', 'border_color', 'size']:
                    if prop in element_data:
                        unnecessary_props.append(prop)
                
                if unnecessary_props:
                    print(f"            ❌ Element {element_id} has unnecessary props: {unnecessary_props}")
                else:
                    print(f"            ✅ Element {element_id} is clean")
    
    # Show just the templates section for reference
    print(f"\n📋 Templates section preview:")
    templates_json = json.dumps(templates, indent=2)
    
    # Show first few lines
    lines = templates_json.split('\n')
    for i, line in enumerate(lines[:50]):  # Show first 50 lines
        print(f"   {line}")
    
    if len(lines) > 50:
        print(f"   ... ({len(lines) - 50} more lines)")
    
    return True

if __name__ == "__main__":
    success = test_complete_ai_export()
    sys.exit(0 if success else 1)
