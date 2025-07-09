#!/usr/bin/env python3
"""
CRASH TEST: Verify that our _add_frame crash test executes when called.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_add_frame_crash_test():
    """Test that our crash test in _add_frame executes."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    timeline = editor.frame_timeline
    canvas = editor.canvas
    
    print("🧪 CRASH TEST: Testing _add_frame execution...")
    
    # Ensure reel is selected
    editor.set_content_type("reel")
    
    print(f"Initial: timeline={timeline.get_frame_count()}, canvas={canvas.get_content_type_frame_count('reel')}")
    
    # Check if canvas is connected
    print(f"Timeline has canvas: {hasattr(timeline, 'canvas') and timeline.canvas is not None}")
    
    try:
        # This should trigger our crash test
        print("➕ Calling timeline._add_frame() - should crash with our test...")
        timeline._add_frame()
        print("❌ UNEXPECTED: No crash occurred - code may not be executing!")
        return False
    except Exception as e:
        print(f"🔥 CRASH TEST SUCCESS: {e}")
        return True
    print("Adding frame...")
    timeline._add_frame()
    
    print(f"After add: timeline={timeline.get_frame_count()}, canvas={canvas.get_content_type_frame_count('reel')}")
    
    # Add another frame
    print("Adding another frame...")
    timeline._add_frame()
    
    print(f"After 2nd add: timeline={timeline.get_frame_count()}, canvas={canvas.get_content_type_frame_count('reel')}")

if __name__ == "__main__":
    test_add_frame_crash_test()
