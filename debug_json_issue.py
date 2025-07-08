#!/usr/bin/env python3
"""
Debug script to find the JSON serialization issue
"""

import json
from core.project import ReelForgeProject
from core.content_generation import ContentGenerationManager
from pathlib import Path

def debug_json_serialization():
    """Debug the JSON serialization issue"""
    
    # Load project
    project_path = Path("output/example_project.rforge")
    project = ReelForgeProject.load(project_path)
    
    if not hasattr(project, 'content_generation_manager'):
        project.content_generation_manager = ContentGenerationManager()
    
    # Get AI data
    ai_data = project.get_ai_generation_data()
    
    # Try to serialize each section to find the problem
    sections = ["plugin", "global_prompt", "moodboard_path", "assets", 
                "scheduled_content", "project_info", "generation_info", 
                "ai_instructions"]
    
    for section in sections:
        try:
            json.dumps(ai_data.get(section, {}))
            print(f"✅ {section}: OK")
        except Exception as e:
            print(f"❌ {section}: {e}")
    
    # Test content_generation section specifically
    try:
        content_gen = ai_data.get("content_generation", {})
        json.dumps(content_gen)
        print("✅ content_generation: OK")
    except Exception as e:
        print(f"❌ content_generation: {e}")
        
        # Test each template
        templates = content_gen.get("templates", {})
        for template_name, template_data in templates.items():
            try:
                json.dumps(template_data)
                print(f"  ✅ template {template_name}: OK")
            except Exception as e:
                print(f"  ❌ template {template_name}: {e}")
                
                # Test each section of the template
                for section_name, section_data in template_data.items():
                    try:
                        json.dumps(section_data)
                        print(f"    ✅ {section_name}: OK")
                    except Exception as e:
                        print(f"    ❌ {section_name}: {e}")

if __name__ == "__main__":
    debug_json_serialization()
