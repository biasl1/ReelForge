#!/usr/bin/env python3
"""
Test script for the template editor workflow.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.project import ReelForgeProject
from ui.template_editor.editor import TemplateEditor
from core.logging_config import setup_logging

def test_template_editor():
    """Test the template editor workflow."""
    app = QApplication(sys.argv)
    setup_logging()
    
    # Create a test project
    project = ReelForgeProject("test_project")
    
    # Create some test events
    from datetime import datetime, timedelta
    from core.project import ReleaseEvent
    
    # Create a video event
    video_event = ReleaseEvent(
        id="video_1",
        title="Test Video",
        description="A test video event",
        content_type="video",
        date=datetime.now().date(),
        time=datetime.now().time(),
        duration=60,
        frame_count=3
    )
    project.add_event(video_event)
    
    # Create a picture event
    picture_event = ReleaseEvent(
        id="picture_1",
        title="Test Picture",
        description="A test picture event",
        content_type="picture",
        date=(datetime.now() + timedelta(days=1)).date(),
        time=datetime.now().time(),
        duration=30,
        frame_count=1
    )
    project.add_event(picture_event)
    
    # Create template editor
    template_editor = TemplateEditor()
    template_editor.set_project(project)
    template_editor.show()
    
    # Test refresh_events method
    print("Testing refresh_events...")
    template_editor.refresh_events()
    
    # Test event selection
    print("Testing event selection...")
    template_editor.set_current_event("video_1")
    
    print("Template editor test completed successfully!")
    print(f"Project has {len(project.release_events)} events")
    print(f"Events: {list(project.release_events.keys())}")
    
    # Schedule exit after 3 seconds
    QTimer.singleShot(3000, app.quit)
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_template_editor())
