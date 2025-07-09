#!/usr/bin/env python3
"""
Final test to verify frame addition sync works correctly.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.editor import TemplateEditor

def test_final_sync():
    """Test that adding frames syncs correctly."""
    app = QApplication(sys.argv)
    
    editor = TemplateEditor()
    timeline = editor.frame_timeline
    canvas = editor.canvas
    
    print("🧪 FINAL TEST: Testing _add_frame sync...")
    
    # Ensure reel is selected
    editor.set_content_type("reel")
    
    initial_timeline = timeline.get_frame_count()
    initial_canvas = canvas.get_content_type_frame_count('reel')
    print(f"📊 Initial counts - Timeline: {initial_timeline}, Canvas: {initial_canvas}")
    
    # Add a frame
    print("➕ Adding frame...")
    timeline._add_frame()
    
    # Check sync
    after_timeline = timeline.get_frame_count()
    after_canvas = canvas.get_content_type_frame_count('reel')
    print(f"📊 After add - Timeline: {after_timeline}, Canvas: {after_canvas}")
    
    if after_timeline == after_canvas and after_timeline == initial_timeline + 1:
        print("✅ SUCCESS: Frame addition sync is working!")
        return True
    else:
        print("❌ FAILURE: Frame addition sync is broken!")
        return False

if __name__ == "__main__":
    test_final_sync()
