#!/usr/bin/env python3
"""
Debug script to see what's being saved
"""
import sys
import tempfile
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.ai_template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication

def debug_template_save():
    """Debug what's being saved"""
    
    app = QApplication([])
    
    # Create a new project
    project = ReelForgeProject()
    project.metadata.name = "Debug Template Project"
    
    # Create template editor and set project
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Original settings:")
    print(json.dumps(editor.content_settings["reel"], indent=2))
    
    # Modify some template settings
    editor.current_content_type = "reel"
    editor.content_settings["reel"]["fixed_intro"] = True
    editor.content_settings["reel"]["pip_shape"] = "rectangle"
    editor.content_settings["reel"]["text_size"] = 36
    
    print("\nAfter modification:")
    print(json.dumps(editor.content_settings["reel"], indent=2))
    
    # Get template config
    config = editor.get_template_config()
    print("\nTemplate config:")
    print(json.dumps(config, indent=2))
    
    # Set to project
    project.simple_templates = config
    print("\nProject simple_templates:")
    print(json.dumps(project.simple_templates, indent=2))
    
    # Convert to dict (what gets saved)
    project_dict = project.to_dict()
    print("\nProject dict simple_templates:")
    print(json.dumps(project_dict["simple_templates"], indent=2))

if __name__ == "__main__":
    debug_template_save()
