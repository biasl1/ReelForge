#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor
from core.project import ReelForgeProject
import tempfile
import json

def debug_save_data():
    print("=== DEBUG SAVE DATA ===\n")
    
    # Initialize the application
    app = QApplication([])
    
    # Create editor and project
    editor = TemplateEditor()
    project = ReelForgeProject()
    
    print("1. Setting up REEL with custom descriptions...")
    
    # Set up reel with custom frames and descriptions
    editor.set_content_type('reel')
    
    # Remove a frame and set descriptions
    editor.frame_timeline.remove_frame(2)  # Now has 2 frames
    
    # Set frame 0 description
    editor.set_current_frame(0)
    editor.canvas.update_frame_description('REEL_DESC_1')
    
    # Set frame 1 description  
    editor.set_current_frame(1)
    editor.canvas.update_frame_description('REEL_DESC_2')
    
    print("2. Checking canvas state before save...")
    canvas_state = editor.canvas.content_states.get('reel', {})
    frames = canvas_state.get('frames', {})
    print(f"   Canvas has {len(frames)} frames:")
    for frame_idx, frame_data in frames.items():
        desc = frame_data.get('frame_description', 'NO DESCRIPTION')
        print(f"     Frame {frame_idx}: '{desc}'")
    
    print("\n3. Saving project...")
    project.save_template_editor_settings(editor)
    
    # Check what gets saved
    template_settings = getattr(project, 'template_editor_settings', {})
    reel_data = template_settings.get('reel', {})
    saved_frames = reel_data.get('frames', {})
    
    print("4. Checking saved data...")
    print(f"   Saved data has {len(saved_frames)} frames:")
    for frame_key, frame_data in saved_frames.items():
        desc = frame_data.get('frame_description', 'NO DESCRIPTION')
        print(f"     Frame {frame_key}: '{desc}'")
    
    # Save to temp file and check JSON
    with tempfile.NamedTemporaryFile(mode='w', suffix='.rforge', delete=False) as f:
        temp_path = f.name
        project.save(temp_path)
    
    print(f"\n5. Checking JSON file content...")
    with open(temp_path, 'r') as f:
        json_data = json.load(f)
    
    template_settings_json = json_data.get('template_editor_settings', {})
    reel_json = template_settings_json.get('reel', {})
    frames_json = reel_json.get('frames', {})
    
    print(f"   JSON has {len(frames_json)} frames:")
    for frame_key, frame_data in frames_json.items():
        desc = frame_data.get('frame_description', 'NO DESCRIPTION')
        print(f"     Frame {frame_key}: '{desc}'")
    
    # Clean up
    os.unlink(temp_path)
    
    print("\n=== DEBUG COMPLETE ===")

if __name__ == "__main__":
    debug_save_data()
