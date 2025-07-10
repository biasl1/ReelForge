#!/usr/bin/env python3
"""
Quick verification that the simplified export structure is working
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.project import ProjectManager
import json

def main():
    print("🔍 Testing simplified export structure...")
    
    project_manager = ProjectManager()
    
    # Test templates format
    templates = project_manager.get_project_templates()
    print(f"\n✅ Templates returned as dict: {type(templates) == dict}")
    print(f"📝 Template keys: {list(templates.keys())}")
    
    for name, template in templates.items():
        print(f"   - {name}: {template['format']} @ {template['fps']}fps")
    
    # Try to load an existing project and test export 
    try:
        project_path = "/Users/test/Documents/ReelForge Projects/euclyd.rforge"
        if os.path.exists(project_path):
            from core.project import ReelForgeProject
            project = ReelForgeProject.load(project_path)
            print(f"\n✅ Loaded existing project: {project.metadata.name}")
            
            # Test the simplified export by creating a temporary file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                temp_file = f.name
            
            success = project.export_ai_data_to_json(temp_file)
            print(f"\n✅ Export successful: {success}")
            
            if success and os.path.exists(temp_file):
                with open(temp_file, 'r') as f:
                    exported_data = json.load(f)
                
                print("\n🔍 Simplified export structure:")
                print(f"📊 Top-level keys: {list(exported_data.keys())}")
                
                # Look specifically at content_generation which should have our templates
                if 'content_generation' in exported_data:
                    content_gen = exported_data['content_generation']
                    print(f"\n📄 content_generation structure:")
                    print(f"   Type: {type(content_gen)}")
                    
                    if isinstance(content_gen, dict):
                        print(f"   Keys: {list(content_gen.keys())}")
                        
                        for content_type, content_data in content_gen.items():
                            print(f"\n📄 {content_type}:")
                            print(f"   Type: {type(content_data)}")
                            if content_data is None:
                                print("   Content is None - skipping")
                                continue
                            if not isinstance(content_data, dict):
                                print(f"   Content is {type(content_data)} - skipping")
                                continue
                                
                            print(f"   content_type: {content_data.get('content_type')}")
                            print(f"   is_video_content: {content_data.get('is_video_content')}")
                            
                            if 'frames' in content_data:
                                print(f"   frames: {len(content_data['frames'])}")
                                for i, frame in enumerate(content_data['frames'][:2]):  # Show first 2 frames
                                    if 'layout' in frame:
                                        layout_keys = list(frame['layout'].keys())
                                        print(f"     Frame {i} layout keys: {layout_keys}")
                            elif 'layout' in content_data:
                                layout_keys = list(content_data['layout'].keys())
                                print(f"   layout keys: {layout_keys}")
                else:
                    print("⚠️ No content_generation section found")
                
                # Clean up temp file
                os.unlink(temp_file)
                print("\n✅ Export structure verification complete!")
            
        else:
            print("⚠️ No existing project found to test export")
            
    except Exception as e:
        print(f"❌ Error testing export: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
