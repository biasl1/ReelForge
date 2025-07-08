#!/usr/bin/env python3
"""
Test drag and resize saving
"""
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from ui.template_editor import SimpleTemplateEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QMouseEvent

def test_drag_resize_save():
    """Test that drag and resize saves to project"""
    
    app = QApplication([])
    
    # Create project and editor
    project = ReelForgeProject()
    project.metadata.name = "Drag Test Project"
    
    editor = SimpleTemplateEditor()
    editor.set_project(project)
    
    print("Initial PiP rect:", editor.visual_editor.pip_rect)
    print("Initial text rect:", editor.visual_editor.text_rect)
    
    # Simulate dragging PiP
    original_pip = editor.visual_editor.pip_rect
    
    # Start drag
    editor.visual_editor.pip_dragging = True
    editor.visual_editor.last_mouse_pos = QPoint(100, 100)
    
    # Move
    editor.visual_editor.pip_rect.translate(50, 30)
    
    # Call mouseReleaseEvent while flags are still set (they get cleared in the method)
    mock_event = type('MockEvent', (), {})()
    editor.visual_editor.mouseReleaseEvent(mock_event)
    
    print("After drag PiP rect:", editor.visual_editor.pip_rect)
    
    # Check if it was saved to project
    if hasattr(project, 'simple_templates'):
        saved_rect = project.simple_templates['content_settings']['reel']['pip_rect']
        print("Saved PiP rect in project:", saved_rect)
        
        current_rect = [
            editor.visual_editor.pip_rect.x(),
            editor.visual_editor.pip_rect.y(),
            editor.visual_editor.pip_rect.width(),
            editor.visual_editor.pip_rect.height()
        ]
        
        if saved_rect == current_rect:
            print("✅ PiP position correctly saved to project!")
        else:
            print("❌ PiP position NOT saved to project")
            print(f"Expected: {current_rect}")
            print(f"Got: {saved_rect}")
    else:
        print("❌ No simple_templates found in project")

if __name__ == "__main__":
    test_drag_resize_save()
