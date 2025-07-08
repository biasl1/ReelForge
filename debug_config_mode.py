#!/usr/bin/env python3
"""
Debug script to find and fix ConfigMode serialization issue
"""
import json
import sys
from pathlib import Path
from core.project import ReelForgeProject, convert_enums
from core.content_generation import ContentGenerationManager, ConfigMode, ConfigParameter


def test_config_mode_serialization():
    """Test ConfigMode serialization directly"""
    print("=== Testing ConfigMode Serialization ===")
    
    # Test direct enum
    try:
        test_mode = ConfigMode.FIXED
        json.dumps(test_mode)
        print("❌ ERROR: ConfigMode.FIXED should not be JSON serializable!")
    except TypeError as e:
        print(f"✅ EXPECTED: ConfigMode.FIXED is not JSON serializable: {e}")
    
    # Test enum value
    try:
        test_value = ConfigMode.FIXED.value
        json.dumps(test_value)
        print(f"✅ SUCCESS: ConfigMode.FIXED.value '{test_value}' is JSON serializable")
    except TypeError as e:
        print(f"❌ ERROR: ConfigMode.FIXED.value should be serializable: {e}")
    
    # Test convert_enums function
    try:
        test_data = {"mode": ConfigMode.FIXED, "list": [ConfigMode.GUIDED, ConfigMode.FREE]}
        converted = convert_enums(test_data)
        json.dumps(converted)
        print(f"✅ SUCCESS: convert_enums works: {converted}")
    except Exception as e:
        print(f"❌ ERROR: convert_enums failed: {e}")


def test_config_parameter():
    """Test ConfigParameter serialization"""
    print("\n=== Testing ConfigParameter Serialization ===")
    
    # Test ConfigParameter
    param = ConfigParameter(value="test", mode=ConfigMode.FIXED)
    try:
        json.dumps(param)
        print("❌ ERROR: ConfigParameter object should not be JSON serializable!")
    except TypeError as e:
        print(f"✅ EXPECTED: ConfigParameter object is not JSON serializable: {e}")
    
    # Test ConfigParameter.to_dict()
    try:
        param_dict = param.to_dict()
        json.dumps(param_dict)
        print(f"✅ SUCCESS: ConfigParameter.to_dict() is JSON serializable: {param_dict}")
    except Exception as e:
        print(f"❌ ERROR: ConfigParameter.to_dict() failed: {e}")


def test_project_with_templates():
    """Test project with content generation manager"""
    print("\n=== Testing Project with Templates ===")
    
    # Create a project with content generation manager
    project = ReelForgeProject()
    project.content_generation_manager = ContentGenerationManager()
    
    # Add some simple templates with raw enums (this is likely the issue)
    project.simple_templates = {
        "test_config": ConfigMode.FIXED,  # This is the problem!
        "nested": {
            "mode": ConfigMode.GUIDED,
            "settings": [ConfigMode.FREE, ConfigMode.FIXED]
        }
    }
    
    print("Added problematic simple_templates with raw ConfigMode enums")
    
    # Test export
    try:
        ai_data = project.get_ai_generation_data()
        json.dumps(ai_data)
        print("❌ ERROR: AI data should not be serializable with raw enums!")
    except TypeError as e:
        print(f"✅ EXPECTED: AI data with raw enums fails: {e}")
        
        # Now fix it with convert_enums
        try:
            converted_data = convert_enums(ai_data)
            json.dumps(converted_data)
            print("✅ SUCCESS: convert_enums fixed the AI data")
        except Exception as e2:
            print(f"❌ ERROR: convert_enums still failed: {e2}")
    
    # Test simple_templates directly
    try:
        json.dumps(project.simple_templates)
        print("❌ ERROR: simple_templates should not be serializable with raw enums!")
    except TypeError as e:
        print(f"✅ EXPECTED: simple_templates with raw enums fails: {e}")
        
        # Fix simple_templates
        try:
            fixed_templates = convert_enums(project.simple_templates)
            json.dumps(fixed_templates)
            print(f"✅ SUCCESS: convert_enums fixed simple_templates: {fixed_templates}")
        except Exception as e2:
            print(f"❌ ERROR: convert_enums on simple_templates failed: {e2}")


def find_config_modes_in_project():
    """Search for any existing project files and check for ConfigMode issues"""
    print("\n=== Searching for Project Files ===")
    
    project_files = list(Path(".").glob("**/*.rforge"))
    if not project_files:
        print("No .rforge files found in current directory")
        return
    
    for project_file in project_files:
        print(f"Checking project file: {project_file}")
        try:
            with open(project_file, 'r') as f:
                data = json.load(f)
            
            print(f"✅ Project file {project_file} loads successfully")
            
            # Check simple_templates
            simple_templates = data.get("simple_templates", {})
            if simple_templates:
                print(f"Found simple_templates: {simple_templates}")
                try:
                    json.dumps(simple_templates)
                    print("✅ simple_templates is JSON serializable")
                except Exception as e:
                    print(f"❌ simple_templates has serialization issues: {e}")
            
        except Exception as e:
            print(f"❌ Error loading {project_file}: {e}")


if __name__ == "__main__":
    test_config_mode_serialization()
    test_config_parameter()
    test_project_with_templates()
    find_config_modes_in_project()
    
    print("\n=== Summary ===")
    print("The issue is likely that ConfigMode enums are being stored directly")
    print("in the project.simple_templates dictionary without being converted to strings.")
    print("This happens when the UI creates ConfigParameter objects and stores them")
    print("but the project save/load doesn't properly convert the enums to strings.")
