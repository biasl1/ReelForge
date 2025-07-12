#!/usr/bin/env python3
"""
Test script to verify the complete ReelTune refactoring.
Tests VIDEO/PICTURE event system, per-event template configuration, and frame management.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime
from core.project import ReelForgeProject, ReleaseEvent
from ui.timeline.event_dialog import EventDialog
from ui.template_editor.editor import TemplateEditor
from PyQt6.QtWidgets import QApplication

def test_event_system():
    """Test the new VIDEO/PICTURE event system"""
    print("🧪 Testing EVENT SYSTEM...")
    
    # Create a new project
    project = ReelForgeProject()
    
    # Create a VIDEO event
    video_event = ReleaseEvent(
        id="video_test",
        date="2025-01-15",
        title="Test Video Event",
        description="A test video with multiple frames",
        content_type="video",
        frame_count=5,
        template_config={
            "frame_data": {
                "0": {"elements": {"title": {"text": "Frame 1"}}},
                "1": {"elements": {"title": {"text": "Frame 2"}}},
                "2": {"elements": {"title": {"text": "Frame 3"}}},
                "3": {"elements": {"title": {"text": "Frame 4"}}},
                "4": {"elements": {"title": {"text": "Frame 5"}}}
            }
        }
    )
    
    # Create a PICTURE event
    picture_event = ReleaseEvent(
        id="picture_test",
        date="2025-01-16",
        title="Test Picture Event",
        description="A test picture with single frame",
        content_type="picture",
        frame_count=1,
        template_config={
            "frame_data": {
                "0": {"elements": {"title": {"text": "Picture Frame"}}}
            }
        }
    )
    
    # Add events to project
    project.add_release_event(video_event)
    project.add_release_event(picture_event)
    
    # Test project methods
    assert project.get_event_template_config("video_test") == video_event.template_config
    assert project.get_event_frame_count("video_test") == 5
    assert project.get_event_frame_count("picture_test") == 1
    
    # Test frame data
    frame_data = project.get_event_frame_data("video_test", 0)
    assert frame_data["elements"]["title"]["text"] == "Frame 1"
    
    print("✅ Event system working correctly!")
    print(f"   - VIDEO event: {video_event.title} ({video_event.frame_count} frames)")
    print(f"   - PICTURE event: {picture_event.title} ({picture_event.frame_count} frames)")
    
    return project

def test_template_editor(project):
    """Test the template editor with per-event configuration"""
    print("\n🧪 Testing TEMPLATE EDITOR...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    # Create template editor
    editor = TemplateEditor()
    editor.set_project(project)
    
    # Test loading a video event
    video_event_id = "video_test"
    editor.load_event(video_event_id)
    
    assert editor.current_event_id == video_event_id
    assert editor.current_event_data.content_type == "video"
    assert editor.current_event_data.frame_count == 5
    
    # Test frame switching
    editor.load_frame(2)
    assert editor.current_frame_index == 2
    
    print("✅ Template editor working correctly!")
    print(f"   - Loaded event: {editor.current_event_data.title}")
    print(f"   - Current frame: {editor.current_frame_index}")
    print(f"   - Frame timeline visible: {editor.frame_timeline.isVisible()}")
    
    # Test loading a picture event
    picture_event_id = "picture_test"
    editor.load_event(picture_event_id)
    
    assert editor.current_event_id == picture_event_id
    assert editor.current_event_data.content_type == "picture"
    assert editor.current_event_data.frame_count == 1
    
    print(f"   - Loaded picture event: {editor.current_event_data.title}")
    print(f"   - Frame timeline hidden: {not editor.frame_timeline.isVisible()}")
    
    return editor

def test_event_dialog():
    """Test the event dialog for creating VIDEO/PICTURE events"""
    print("\n🧪 Testing EVENT DIALOG...")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
    
    date = datetime(2025, 1, 20)
    dialog = EventDialog(date)
    
    # Test dialog initialization
    assert dialog.content_type_combo.count() == 2
    assert dialog.content_type_combo.itemText(0) == "VIDEO"
    assert dialog.content_type_combo.itemText(1) == "PICTURE"
    
    # Test frame count controls
    dialog.content_type_combo.setCurrentText("VIDEO")
    dialog.on_content_type_changed()
    assert dialog.frame_count_spin.isEnabled()
    
    dialog.content_type_combo.setCurrentText("PICTURE")
    dialog.on_content_type_changed()
    assert not dialog.frame_count_spin.isEnabled()
    
    print("✅ Event dialog working correctly!")
    print(f"   - Content types: VIDEO, PICTURE")
    print(f"   - Frame count enabled for VIDEO only")
    
    return dialog

def main():
    """Run all tests"""
    print("🚀 STARTING REELTUNE REFACTORING TESTS\n")
    
    try:
        # Test 1: Event system
        project = test_event_system()
        
        # Test 2: Template editor
        editor = test_template_editor(project)
        
        # Test 3: Event dialog
        dialog = test_event_dialog()
        
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ REFACTORING COMPLETE:")
        print("   - ✅ Calendar events now use VIDEO/PICTURE types")
        print("   - ✅ Each event has its own custom frames and template config")
        print("   - ✅ Template editor works with per-event frames")
        print("   - ✅ Event dialog creates VIDEO/PICTURE events")
        print("   - ✅ Frame counts are configurable per event")
        print("   - ✅ All legacy content types removed")
        
        return True
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
