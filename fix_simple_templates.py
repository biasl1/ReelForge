#!/usr/bin/env python3
"""
Fix script for ReelTune ConfigMode serialization issue
This script will load your project file, find any ConfigMode enums in the simple_templates,
convert them to strings, and save the file back.
"""

import json
import sys
import os
from pathlib import Path
import enum
from typing import Any, Dict, List, Optional

# Add the parent directory to the path so we can import the project modules
sys.path.append(os.path.dirname(__file__))

# Import only after adding to path
from core.project import ReelForgeProject, convert_enums
from core.logging_config import log_info, log_error, log_debug

def find_and_fix_enums_in_templates(project_path: str) -> bool:
    """Load the project file, find ConfigMode enums, and fix them"""
    print(f"Loading project from: {project_path}")
    project = ReelForgeProject.load(Path(project_path))
    
    if not project:
        print(f"Failed to load project from {project_path}")
        return False
    
    print("Project loaded successfully")
    
    # Check if simple_templates exists and has content
    if not hasattr(project, 'simple_templates') or not project.simple_templates:
        print("No simple_templates found in the project")
        return True
    
    # Log the contents before conversion
    print("\nSimple templates before conversion:")
    print("----------------------------------")
    try:
        json_str = json.dumps(project.simple_templates)
        print("Templates are already JSON serializable")
    except Exception as e:
        print(f"Templates are not JSON serializable: {e}")
    
    # Convert enums in simple_templates
    print("\nConverting any enums in templates...")
    project.simple_templates = convert_enums(project.simple_templates)
    
    # Check if it worked
    print("\nSimple templates after conversion:")
    print("----------------------------------")
    try:
        json_str = json.dumps(project.simple_templates)
        print("Templates are now JSON serializable!")
    except Exception as e:
        print(f"Templates are still not JSON serializable: {e}")
        return False
    
    # Save the project
    print("\nSaving fixed project...")
    success = project.save()
    if success:
        print(f"Project saved successfully to: {project.project_file_path}")
        return True
    else:
        print("Failed to save project")
        return False

def test_export_functions(project_path: str) -> bool:
    """Test the export functions to ensure they work correctly"""
    print(f"Testing export functions with project: {project_path}")
    project = ReelForgeProject.load(Path(project_path))
    
    if not project:
        print(f"Failed to load project from {project_path}")
        return False
    
    # Test AI data export
    ai_output = Path(project_path).parent / "ai_export_test.json"
    print(f"Testing export_ai_data_to_json to {ai_output}")
    ai_result = project.export_ai_data_to_json(str(ai_output))
    
    if ai_result:
        print("✓ AI data export successful")
    else:
        print("✗ AI data export failed")
    
    # Test template config export
    config_output = Path(project_path).parent / "template_config_test.json"
    print(f"Testing export_template_config_to_json to {config_output}")
    config_result = project.export_template_config_to_json(str(config_output))
    
    if config_result:
        print("✓ Template config export successful")
    else:
        print("✗ Template config export failed")
    
    return ai_result and config_result

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python fix_simple_templates.py <project_file_path>")
        return
    
    project_path = sys.argv[1]
    if not os.path.exists(project_path):
        print(f"Project file not found: {project_path}")
        return
    
    # Fix enums in templates
    if find_and_fix_enums_in_templates(project_path):
        print("\nTemplate fixes completed successfully")
        
        # Test export functions
        print("\nTesting export functions...")
        if test_export_functions(project_path):
            print("\nAll tests passed! Your project should now export correctly.")
        else:
            print("\nSome export tests failed. You may need further fixes.")
    else:
        print("\nFailed to fix templates")

if __name__ == "__main__":
    main()
