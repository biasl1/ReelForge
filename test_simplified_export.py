#!/usr/bin/env python3
"""Test script to check the simplified AI export format"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
import json

def test_simplified_export():
    """Test that the export format is simplified"""
    print("🧪 Testing simplified AI export format...")
    
    # Load the test project
    project_path = "/Users/test/Documents/ReelForge Projects/Test1.rforge"
    
    try:
        project = ReelForgeProject()
        project.load_from_file(project_path)
        
        # Export to a test file
        output_path = "/tmp/test_export.json"
        success = project.export_ai_data_to_json(output_path)
        
        if not success:
            print("❌ Export failed")
            return False
            
        # Read the exported data
        with open(output_path, 'r') as f:
            exported_data = json.load(f)
        
        # Check content_generation structure
        if 'content_generation' in exported_data and 'templates' in exported_data['content_generation']:
            templates = exported_data['content_generation']['templates']
            
            print(f"📊 Found {len(templates)} templates")
            
            # Check first template
            for template_key, template_data in templates.items():
                print(f"\n🔍 Checking template: {template_key}")
                
                # Check if it has frame_data
                if 'template_config' in template_data and 'frame_data' in template_data['template_config']:
                    frame_data = template_data['template_config']['frame_data']
                    
                    # Check first frame
                    if '0' in frame_data:
                        frame_0 = frame_data['0']
                        elements = frame_0.get('elements', {})
                        
                        print(f"📋 Frame 0 elements: {list(elements.keys())}")
                        
                        # Check PiP element
                        if 'pip' in elements:
                            pip_element = elements['pip']
                            print(f"🎬 PiP element properties: {list(pip_element.keys())}")
                            
                            # Check if it has the simplified properties
                            has_visible = 'visible' in pip_element
                            has_enabled = 'enabled' in pip_element
                            has_rect = 'rect' in pip_element
                            
                            print(f"   ✅ Has 'visible': {has_visible}")
                            print(f"   ❌ Has 'enabled': {has_enabled}")
                            print(f"   ❌ Has 'rect': {has_rect}")
                            
                            if has_visible:
                                print(f"   📍 PiP visible: {pip_element['visible']}")
                            
                            if has_enabled:
                                print(f"   ⚠️  PiP enabled: {pip_element['enabled']} (should be removed)")
                                
                            if has_rect:
                                print(f"   ⚠️  PiP rect: {pip_element['rect']} (should be removed)")
                        
                        # Check text elements
                        for element_id in ['title', 'subtitle']:
                            if element_id in elements:
                                element = elements[element_id]
                                print(f"📝 {element_id} element properties: {list(element.keys())}")
                                
                                has_visible = 'visible' in element
                                has_enabled = 'enabled' in element
                                has_rect = 'rect' in element
                                has_font_size = 'font_size' in element
                                has_size = 'size' in element
                                
                                print(f"   ✅ Has 'visible': {has_visible}")
                                print(f"   ❌ Has 'enabled': {has_enabled}")
                                print(f"   ❌ Has 'rect': {has_rect}")
                                print(f"   ✅ Has 'font_size': {has_font_size}")
                                print(f"   ⚠️  Has 'size': {has_size}")
                                
                                if has_font_size:
                                    print(f"   📏 Font size: {element['font_size']}")
                                if has_size:
                                    print(f"   📏 Size: {element['size']}")
                
                # Only check first template for now
                break
                
        print("\n✅ Export format test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_simplified_export()
    sys.exit(0 if success else 1)
