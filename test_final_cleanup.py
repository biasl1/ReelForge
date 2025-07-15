#!/usr/bin/env python3

"""
Final test script to verify the cleaned up ReelTune application
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def test_final_cleanup():
    """Test that the cleaned up application works correctly."""
    
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
    print(f"\n🤖 Testing AI export...")
    ai_data = project.get_ai_generation_data()
    
    # Save the final clean export
    output_file = "/Users/test/Documents/development/Artists in DSP/ReelTune/output/final_clean_export.json"
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    with open(output_file, 'w') as f:
        json.dump(ai_data, f, indent=2)
    
    print(f"✅ Clean AI export saved to: {output_file}")
    
    # Verify the export
    templates = ai_data.get('content_generation', {}).get('templates', {})
    print(f"\n📋 Final Export Summary:")
    print(f"   Total templates: {len(templates)}")
    
    for template_key, template_data in templates.items():
        event_title = template_data.get('event_title', 'Unknown')
        frame_count = template_data.get('frame_count', 0)
        
        print(f"\n   📄 Template: {template_key}")
        print(f"      Event: {event_title}")
        print(f"      Frame Count: {frame_count}")
        
        frame_data = template_data.get('template_config', {}).get('frame_data', {})
        print(f"      Exported Frames: {len(frame_data)}")
        
        if frame_count != len(frame_data):
            print(f"      ❌ Frame count mismatch!")
            return False
        
        # Check each frame for clean data
        for frame_key, frame_info in frame_data.items():
            elements = frame_info.get('elements', {})
            print(f"         Frame {frame_key}: {len(elements)} elements")
            
            # Check for clean data (no unnecessary properties)
            for element_id, element_data in elements.items():
                essential_props = {'type', 'content', 'font_size', 'position_preset', 'visible'}
                if element_data.get('type') == 'pip':
                    essential_props.add('corner_radius')
                
                actual_props = set(element_data.keys())
                unnecessary_props = actual_props - essential_props
                
                if unnecessary_props:
                    print(f"            ❌ Element {element_id} has unnecessary props: {unnecessary_props}")
                    return False
                else:
                    print(f"            ✅ Element {element_id} is clean")
    
    print(f"\n✅ All tests passed! ReelTune is clean and functional.")
    return True

if __name__ == "__main__":
    success = test_final_cleanup()
    sys.exit(0 if success else 1)
