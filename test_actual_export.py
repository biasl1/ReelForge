#!/usr/bin/env python3
"""
Test actual export function to identify ConfigMode issue
"""
import sys
import traceback
from pathlib import Path
from core.project import ReelForgeProject
from core.content_generation import ContentGenerationManager


def test_actual_export():
    """Test the actual export_ai_data_to_json function"""
    print("=== Testing Actual Export Function ===")
    
    # Load the existing project
    project_path = Path("output/example_project.rforge")
    if not project_path.exists():
        print("❌ No existing project file found")
        return
        
    print(f"Loading project: {project_path}")
    project = ReelForgeProject.load(project_path)
    if not project:
        print("❌ Failed to load project")
        return
        
    print("✅ Project loaded successfully")
    
    # Add content generation manager (this is likely where the issue comes from)
    print("Adding ContentGenerationManager...")
    if not hasattr(project, 'content_generation_manager'):
        project.content_generation_manager = ContentGenerationManager()
        print("✅ ContentGenerationManager added")
    else:
        print("✅ ContentGenerationManager already exists")
    
    # Test export
    output_path = "test_export.json"
    print(f"Testing export to: {output_path}")
    
    try:
        success = project.export_ai_data_to_json(output_path)
        if success:
            print("✅ Export successful!")
        else:
            print("❌ Export failed")
    except Exception as e:
        print(f"❌ Export failed with error: {e}")
        traceback.print_exc()


def test_specific_data_parts():
    """Test specific parts of the AI generation data"""
    print("\n=== Testing Specific Data Parts ===")
    
    # Load project
    project_path = Path("output/example_project.rforge")
    project = ReelForgeProject.load(project_path)
    if not project:
        print("❌ Failed to load project")
        return
    
    # Add content generation manager
    if not hasattr(project, 'content_generation_manager'):
        project.content_generation_manager = ContentGenerationManager()
    
    # Test different parts of get_ai_generation_data
    import json
    
    print("Testing plugin data...")
    plugin_info = project.get_current_plugin_info()
    try:
        json.dumps(plugin_info)
        print("✅ Plugin data is serializable")
    except Exception as e:
        print(f"❌ Plugin data failed: {e}")
    
    print("Testing assets data...")
    assets_data = []
    for asset in project.get_all_assets():
        assets_data.append({
            "id": asset.id,
            "name": asset.name,
            "type": asset.file_type,
            "path": asset.file_path
        })
    try:
        json.dumps(assets_data)
        print("✅ Assets data is serializable")
    except Exception as e:
        print(f"❌ Assets data failed: {e}")
    
    print("Testing events data...")
    events_data = []
    for event in project.release_events.values():
        events_data.append({
            "date": event.date,
            "content_type": event.content_type,
            "title": event.title,
            "prompt": event.description,
            "platforms": event.platforms
        })
    try:
        json.dumps(events_data)
        print("✅ Events data is serializable")
    except Exception as e:
        print(f"❌ Events data failed: {e}")
    
    print("Testing templates data...")
    templates_data = {}
    if hasattr(project, 'content_generation_manager') and project.content_generation_manager:
        # This is where the issue likely is!
        try:
            for content_type, template in project.content_generation_manager.content_type_templates.items():
                templates_data[content_type] = {
                    "name": template.content_type.replace("_", " ").title(),
                    "content_type": template.content_type,
                    "platform": project._get_platform_for_content_type(template.content_type),
                    "subtitle_options": template.subtitle.to_dict(),
                    "overlay_options": template.overlay.to_dict(),
                    "timing_options": template.timing.to_dict(),
                    "custom_settings": {k: v.to_dict() for k, v in template.custom_parameters.items()}
                }
            json.dumps(templates_data)
            print("✅ Templates data is serializable")
        except Exception as e:
            print(f"❌ Templates data failed: {e}")
            # Find which template is causing the issue
            for content_type, template in project.content_generation_manager.content_type_templates.items():
                try:
                    test_data = {
                        "subtitle_options": template.subtitle.to_dict(),
                        "overlay_options": template.overlay.to_dict(),
                        "timing_options": template.timing.to_dict(),
                    }
                    json.dumps(test_data)
                    print(f"✅ Template {content_type} is OK")
                except Exception as e2:
                    print(f"❌ Template {content_type} failed: {e2}")
                    
                    # Test each part separately
                    try:
                        json.dumps(template.subtitle.to_dict())
                        print(f"  ✅ {content_type} subtitle OK")
                    except Exception as e3:
                        print(f"  ❌ {content_type} subtitle failed: {e3}")
                    
                    try:
                        json.dumps(template.overlay.to_dict())
                        print(f"  ✅ {content_type} overlay OK")
                    except Exception as e3:
                        print(f"  ❌ {content_type} overlay failed: {e3}")
                    
                    try:
                        json.dumps(template.timing.to_dict())
                        print(f"  ✅ {content_type} timing OK")
                    except Exception as e3:
                        print(f"  ❌ {content_type} timing failed: {e3}")


if __name__ == "__main__":
    test_actual_export()
    test_specific_data_parts()
