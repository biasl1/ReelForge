#!/usr/bin/env python3
"""
Test script for exporting AI generation data with the fixed JSON serialization
"""

import json
import sys
from pathlib import Path
from core.project import ReelForgeProject

def test_ai_export():
    """Test AI data export with custom JSON encoder"""
    
    # Load the example project
    project_path = Path("output/example_project.rforge")
    project = ReelForgeProject.load(project_path)
    if not project:
        print("❌ Failed to load project")
        return False
    
    # Export AI data
    output_path = "ai_export_fixed.json"
    success = project.export_ai_data_to_json(output_path)
    
    if success:
        print(f"✅ AI data exported successfully to {output_path}")
        return True
    else:
        print("❌ Failed to export AI data")
        return False

if __name__ == "__main__":
    success = test_ai_export()
    sys.exit(0 if success else 1)
