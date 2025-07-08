#!/usr/bin/env python3
"""
Debug script to understand what's happening with save/load
"""

import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ui.ai_template_editor import SimpleTemplateEditor
from core.project import ReelForgeProject

def debug_save_load():
    """Debug the save/load process"""
    app = QApplication(sys.argv)
    
    project = ReelForgeProject()
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Debugging save/load process...")
    
    # Switch to reel
    editor._on_content_type_changed('reel')
    
    print(f"\n1. Initial state:")
    print(f"PiP position: ({editor.visual_editor.pip_rect.x()}, {editor.visual_editor.pip_rect.y()})")
    print(f"Title position: ({editor.visual_editor.text_overlays['title']['rect'].x()}, {editor.visual_editor.text_overlays['title']['rect'].y()})")
    
    # Modify positions
    editor.visual_editor.pip_rect.moveTo(200, 150)
    editor.visual_editor.text_overlays['title']['rect'].moveTo(100, 250)
    editor.visual_editor.text_overlays['title']['content'] = "Test Modified"
    
    print(f"\n2. After modification:")
    print(f"PiP position: ({editor.visual_editor.pip_rect.x()}, {editor.visual_editor.pip_rect.y()})")
    print(f"Title position: ({editor.visual_editor.text_overlays['title']['rect'].x()}, {editor.visual_editor.text_overlays['title']['rect'].y()})")
    print(f"Title content: '{editor.visual_editor.text_overlays['title']['content']}'")
    
    # Save manually
    editor._save_all_current_settings()
    
    print(f"\n3. Content settings after save:")
    reel_settings = editor.content_settings['reel']
    print(f"Saved PiP position: {reel_settings['pip_rect']}")
    print(f"Saved title position: {reel_settings['text_overlays']['title']['rect']}")
    print(f"Saved title content: '{reel_settings['text_overlays']['title']['content']}'")
    
    # Get config
    config = editor.get_template_config()
    print(f"\n4. Template config:")
    print(f"Config PiP position: {config['content_settings']['reel']['pip_rect']}")
    print(f"Config title position: {config['content_settings']['reel']['text_overlays']['title']['rect']}")
    print(f"Config title content: '{config['content_settings']['reel']['text_overlays']['title']['content']}'")
    
    # Auto save to project
    editor._auto_save_to_project()
    print(f"\n5. Project simple_templates after auto-save:")
    if hasattr(project, 'simple_templates'):
        project_settings = project.simple_templates
        print(f"Project PiP position: {project_settings['content_settings']['reel']['pip_rect']}")
        print(f"Project title position: {project_settings['content_settings']['reel']['text_overlays']['title']['rect']}")
        print(f"Project title content: '{project_settings['content_settings']['reel']['text_overlays']['title']['content']}'")
    else:
        print("Project doesn't have simple_templates attribute")
    
    # Create new editor
    editor2 = SimpleTemplateEditor()
    editor2.set_project(project)
    
    print(f"\n6. New editor after loading project:")
    editor2._on_content_type_changed('reel')
    print(f"Loaded PiP position: ({editor2.visual_editor.pip_rect.x()}, {editor2.visual_editor.pip_rect.y()})")
    print(f"Loaded title position: ({editor2.visual_editor.text_overlays['title']['rect'].x()}, {editor2.visual_editor.text_overlays['title']['rect'].y()})")
    print(f"Loaded title content: '{editor2.visual_editor.text_overlays['title']['content']}'")
    
    print(f"\n7. New editor content_settings:")
    reel2_settings = editor2.content_settings['reel']
    print(f"Content settings PiP position: {reel2_settings['pip_rect']}")
    print(f"Content settings title position: {reel2_settings['text_overlays']['title']['rect']}")
    print(f"Content settings title content: '{reel2_settings['text_overlays']['title']['content']}'")
    
    app.quit()

if __name__ == "__main__":
    debug_save_load()
