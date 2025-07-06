#!/usr/bin/env python3
"""
Test script to verify that per-content-type visual settings are independent
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QRect
from ui.ai_template_editor import SimpleTemplateEditor

def test_independence():
    """Test that content type settings are independent"""
    app = QApplication(sys.argv)
    
    # Create editor
    editor = SimpleTemplateEditor()
    
    # Start with reel (default)
    print("=== Testing Content Type Independence ===")
    print(f"Initial content type: {editor.current_content_type}")
    
    # Set reel settings
    editor.visual_editor.pip_rect = QRect(100, 100, 150, 150)
    editor.visual_editor.text_rect = QRect(100, 300, 250, 60)
    editor._save_all_current_settings()
    print(f"REEL - PiP: {editor.visual_editor.pip_rect}, Text: {editor.visual_editor.text_rect}")
    
    # Switch to teaser
    editor._on_content_type_changed("teaser")
    print(f"Switched to: {editor.current_content_type}")
    print(f"TEASER - PiP: {editor.visual_editor.pip_rect}, Text: {editor.visual_editor.text_rect}")
    
    # Modify teaser settings
    editor.visual_editor.pip_rect = QRect(200, 200, 80, 80)
    editor.visual_editor.text_rect = QRect(200, 400, 180, 40)
    editor._save_all_current_settings()
    print(f"TEASER MODIFIED - PiP: {editor.visual_editor.pip_rect}, Text: {editor.visual_editor.text_rect}")
    
    # Switch back to reel
    editor._on_content_type_changed("reel")
    print(f"Switched back to: {editor.current_content_type}")
    print(f"REEL AFTER SWITCH - PiP: {editor.visual_editor.pip_rect}, Text: {editor.visual_editor.text_rect}")
    
    # Check if reel settings are preserved
    reel_pip = editor.visual_editor.pip_rect
    reel_text = editor.visual_editor.text_rect
    
    if (reel_pip.x() == 100 and reel_pip.y() == 100 and 
        reel_pip.width() == 150 and reel_pip.height() == 150):
        print("✅ REEL PiP settings preserved correctly!")
    else:
        print("❌ REEL PiP settings NOT preserved!")
    
    if (reel_text.x() == 100 and reel_text.y() == 300 and 
        reel_text.width() == 250 and reel_text.height() == 60):
        print("✅ REEL Text settings preserved correctly!")
    else:
        print("❌ REEL Text settings NOT preserved!")
    
    # Switch back to teaser to verify its settings
    editor._on_content_type_changed("teaser")
    teaser_pip = editor.visual_editor.pip_rect
    teaser_text = editor.visual_editor.text_rect
    
    print(f"TEASER FINAL CHECK - PiP: {teaser_pip}, Text: {teaser_text}")
    
    if (teaser_pip.x() == 200 and teaser_pip.y() == 200 and 
        teaser_pip.width() == 80 and teaser_pip.height() == 80):
        print("✅ TEASER PiP settings preserved correctly!")
    else:
        print("❌ TEASER PiP settings NOT preserved!")
    
    if (teaser_text.x() == 200 and teaser_text.y() == 400 and 
        teaser_text.width() == 180 and teaser_text.height() == 40):
        print("✅ TEASER Text settings preserved correctly!")
    else:
        print("❌ TEASER Text settings NOT preserved!")
    
    print("=== Test Complete ===")
    app.quit()

if __name__ == "__main__":
    test_independence()
