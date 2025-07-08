#!/usr/bin/env python3
"""
Debug the new editor loading part
"""
import sys
import tempfile
from pathlib import Path
import json

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.template_editor import TemplateEditor
from PyQt6.QtWidgets import QApplication

def debug_new_editor_loading():
    """Debug new editor loading"""
    
    app = QApplication([])
    
    # Create and setup first editor (same as before)
    project = ReelForgeProject()
    project.metadata.name = "Debug Template Project"
    
    editor = TemplateEditor()
    editor.set_project(project)
    
    # Modify settings
    editor.current_content_type = "reel"
    editor.content_settings["reel"]["fixed_intro"] = True
    editor.content_settings["reel"]["pip_shape"] = "rectangle"
    editor.content_settings["reel"]["text_size"] = 36
    
    # Save to project
    config = editor.get_template_config()
    project.simple_templates = config
    
    # Save to file
    with tempfile.NamedTemporaryFile(suffix='.rforge', delete=False) as tmp:
        tmp_path = Path(tmp.name)
    
    project.save(tmp_path)
    loaded_project = ReelForgeProject.load(tmp_path)
    
    print("Loaded project simple_templates reel settings:")
    print(json.dumps(loaded_project.simple_templates['content_settings']['reel'], indent=2))
    
    # Now test new editor
    print("\nCreating new editor...")
    new_editor = TemplateEditor()
    
    print("New editor initial settings:")
    print(json.dumps(new_editor.content_settings["reel"], indent=2))
    
    print("\nSetting project on new editor...")
    new_editor.set_project(loaded_project)
    
    print("New editor settings after setting project:")
    print(json.dumps(new_editor.content_settings["reel"], indent=2))
    
    # Clean up
    tmp_path.unlink()

if __name__ == "__main__":
    debug_new_editor_loading()
