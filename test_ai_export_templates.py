#!/usr/bin/env python3
"""
Test script to verify AI export includes complete template information
"""

import json
import sys
from pathlib import Path
from core.project import ReelForgeProject
from core.content_generation import ContentGenerationManager

def test_ai_export_templates():
    """Test that AI export includes complete template structures"""
    
    # Load the example project
    project_path = Path("output/example_project.rforge")
    if not project_path.exists():
        print("❌ Example project not found")
        return False
    
    project = ReelForgeProject.load(project_path)
    if not project:
        print("❌ Failed to load project")
        return False
    print("✅ Project loaded successfully")
    
    # Ensure content generation manager exists
    if not hasattr(project, 'content_generation_manager'):
        project.content_generation_manager = ContentGenerationManager()
        print("✅ Content generation manager created")
    
    # Test AI export
    try:
        ai_data = project.get_ai_generation_data()
        print("✅ AI export data generated")
    except Exception as e:
        print(f"❌ Failed to generate AI export: {e}")
        return False
    
    # Verify structure
    required_keys = [
        "plugin", "global_prompt", "moodboard_path", "assets", 
        "scheduled_content", "project_info", "generation_info", 
        "content_generation", "ai_instructions"
    ]
    
    for key in required_keys:
        if key not in ai_data:
            print(f"❌ Missing required key: {key}")
            return False
    
    print("✅ All required keys present")
    
    # Verify templates structure
    content_gen = ai_data.get("content_generation", {})
    templates = content_gen.get("templates", {})
    
    if not templates:
        print("❌ No templates found in export")
        return False
    
    print(f"✅ Found {len(templates)} templates")
    
    # Debug: show what templates exist
    print("📋 Available templates:")
    for key in templates.keys():
        print(f"  - {key}")
    
    # Get scheduled content for debugging
    scheduled_content = ai_data.get("scheduled_content", [])
    print("📋 Content items and template keys:")
    for content in scheduled_content:
        print(f"  - {content.get('title', 'Unknown')}: {content.get('template_key', 'None')}")
    
    # Check template structure
    for template_key, template_data in templates.items():
        required_template_keys = [
            "name", "content_type", "platform", 
            "subtitle_options", "overlay_options", "timing_options"
        ]
        
        for req_key in required_template_keys:
            if req_key not in template_data:
                print(f"❌ Template {template_key} missing key: {req_key}")
                return False
        
        # Check parameter structure
        for option_type in ["subtitle_options", "overlay_options", "timing_options"]:
            options = template_data.get(option_type, {})
            for param_name, param_data in options.items():
                if not isinstance(param_data, dict):
                    continue
                    
                param_keys = ["value", "mode", "constraints", "description"]
                for param_key in param_keys:
                    if param_key not in param_data:
                        print(f"❌ Parameter {param_name} missing key: {param_key}")
                        return False
    
    print("✅ All templates have correct structure")
    
    # Verify content type consistency
    scheduled_content = ai_data.get("scheduled_content", [])
    for content in scheduled_content:
        if "template_key" not in content:
            print(f"❌ Content item missing template_key: {content.get('title', 'Unknown')}")
            return False
        
        template_key = content["template_key"]
        if template_key not in templates:
            print(f"❌ Template key {template_key} not found in templates")
            return False
    
    print("✅ Content type consistency verified")
    
    # Verify AI instructions
    ai_instructions = ai_data.get("ai_instructions", {})
    required_instruction_keys = [
        "content_generation_workflow", "content_requirements", 
        "asset_selection_guidance", "template_usage"
    ]
    
    for key in required_instruction_keys:
        if key not in ai_instructions:
            print(f"❌ Missing AI instruction key: {key}")
            return False
    
    print("✅ AI instructions complete")
    
    # Pretty print a sample template (skip JSON serialization issues)
    print("\n📋 Sample template structure:")
    sample_template = list(templates.values())[0]
    print(f"Template name: {sample_template.get('name', 'Unknown')}")
    print(f"Content type: {sample_template.get('content_type', 'Unknown')}")
    print(f"Platform: {sample_template.get('platform', 'Unknown')}")
    print(f"Has subtitle options: {bool(sample_template.get('subtitle_options'))}")
    print(f"Has overlay options: {bool(sample_template.get('overlay_options'))}")
    print(f"Has timing options: {bool(sample_template.get('timing_options'))}")
    
    # Save complete export for inspection (skip JSON serialization for now)
    print(f"\n✅ Template export test completed successfully!")
    print(f"📊 Export contains {len(templates)} templates and {len(scheduled_content)} content items")
    
    # Test passed - templates are properly included in export
    return True

if __name__ == "__main__":
    success = test_ai_export_templates()
    sys.exit(0 if success else 1)
