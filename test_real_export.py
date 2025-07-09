#!/usr/bin/env python3
"""
Test the exact export path that's failing in the UI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from core.project import ReelForgeProject, ReleaseEvent
from ui.template_editor.editor import TemplateEditor
from datetime import datetime
import traceback

def main():
    print("=== Testing Real Export Path ===")
    app = QApplication(sys.argv)
    
    try:
        # Create a project with events to trigger template export
        project = ReelForgeProject()
        project.metadata.name = "Test Export Project"
        
        # Add a test event
        event = ReleaseEvent(
            id="test_event_1", 
            date=datetime.now().date().isoformat(),
            content_type="reel",
            title="Test Reel",
            description="Test prompt",
            platforms=["instagram"]
        )
        project.add_release_event(event)
        
        # Create and configure template editor
        template_editor = TemplateEditor()
        template_editor.set_content_type("reel")
        
        # Add some elements to trigger frame creation
        template_editor.canvas.elements['title'] = {
            'type': 'text',
            'rect': QRect(50, 100, 300, 80),
            'content': "Test Title",
            'color': QRect(255, 255, 255, 255),  # Intentionally wrong - this should cause issues
            'size': 24,
            'enabled': True
        }
        
        # Manually trigger save to create frame data
        template_editor.canvas._save_current_frame_state()
        
        print("Template editor state:")
        config = template_editor.get_template_config()
        print(f"Config keys: {list(config.keys())}")
        
        if 'canvas_config' in config:
            canvas_config = config['canvas_config']
            print(f"Canvas config keys: {list(canvas_config.keys())}")
            
            if 'frames' in canvas_config:
                frames = canvas_config['frames']
                print(f"Frames type: {type(frames)}")
                print(f"Frames keys: {list(frames.keys())}")
                
                for key, frame_data in frames.items():
                    print(f"Frame {key} type: {type(frame_data)}")
                    if hasattr(frame_data, 'keys'):
                        print(f"  Frame {key} keys: {list(frame_data.keys())}")
                        
                        # Check if frame_data has .get method
                        if hasattr(frame_data, 'get'):
                            print(f"  Frame {key} has .get() method ✓")
                            try:
                                elements = frame_data.get('elements', {})
                                print(f"  Frame {key} elements retrieved successfully ✓")
                            except Exception as e:
                                print(f"  Frame {key} .get() failed: {e}")
                        else:
                            print(f"  Frame {key} MISSING .get() method ✗")
                            print(f"  Frame {key} actual type: {type(frame_data)}")
                            print(f"  Frame {key} value: {frame_data}")
        
        # Now try the full export that's failing
        print("\n=== Attempting Export ===")
        result = project.export_ai_data_to_json("test_export_debug.json", template_editor)
        print(f"Export result: {result}")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    main()
