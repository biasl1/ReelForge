#!/usr/bin/env python3
"""
Test the new streamlined export with custom templates
"""
from pathlib import Path
from core.project import ReelForgeProject
from core.content_generation import ContentGenerationManager, ContentTemplate, SubtitleTemplate, OverlayTemplate, TimingTemplate


def test_with_custom_template():
    """Test export with a custom template to see the new practical layout"""
    print("=== Testing Export with Custom Template ===")
    
    # Load project
    project_path = Path("output/example_project.rforge")
    project = ReelForgeProject.load(project_path)
    if not project:
        print("❌ Failed to load project")
        return
    
    # Add content generation manager
    if not hasattr(project, 'content_generation_manager'):
        project.content_generation_manager = ContentGenerationManager()
    
    # Add a custom event-specific template
    custom_template = ContentTemplate(content_type="reel")
    project.content_generation_manager.event_templates["20e468b1"] = custom_template
    
    # Test export
    output_path = "test_export_with_template.json"
    success = project.export_ai_data_to_json(output_path)
    
    if success:
        print(f"✅ Export with custom template successful! Check: {output_path}")
        
        # Show what the template section looks like
        import json
        with open(output_path, 'r') as f:
            data = json.load(f)
        
        templates = data.get("content_generation", {}).get("templates", {})
        if templates:
            print(f"\n📋 Custom Templates Exported: {list(templates.keys())}")
            for template_name, template_data in templates.items():
                print(f"\n🎨 Template: {template_name}")
                print(f"  Content Type: {template_data.get('content_type')}")
                print(f"  Dimensions: {template_data.get('dimensions')}")
                layout = template_data.get('layout', {})
                if layout:
                    print(f"  Title Position: {layout.get('title', {}).get('position')}")
                    print(f"  Subtitle Position: {layout.get('subtitle', {}).get('position')}")
                    print(f"  PiP Position: {layout.get('pip_video', {}).get('position')}")
        else:
            print("✅ No custom templates = clean empty templates section")
    else:
        print("❌ Export failed")


if __name__ == "__main__":
    test_with_custom_template()
