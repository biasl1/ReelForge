#!/usr/bin/env python3
"""
Test script to verify timeline refresh functionality
Tests event deletion and editing to ensure proper UI updates
"""

import sys
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent
from ui.mainwindow import MainWindow


def test_timeline_refresh():
    """Test timeline refresh after event operations"""
    
    print("🔍 Testing Timeline Refresh Functionality")
    print("=" * 50)
    
    app = QApplication(sys.argv)
    
    # Create main window
    window = MainWindow()
    
    # Create a test project
    project = ReelForgeProject()
    
    # Set up timeline
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=2)
    
    # Create test events
    events = [
        ReleaseEvent(
            id="",  # Will be auto-generated
            title="Test Event 1",
            date=(start_date + timedelta(days=1)).date().isoformat(),
            content_type="reel",
            description="First test event"
        ),
        ReleaseEvent(
            id="",  # Will be auto-generated
            title="Test Event 2", 
            date=(start_date + timedelta(days=3)).date().isoformat(),
            content_type="post",
            description="Second test event"
        ),
        ReleaseEvent(
            id="",  # Will be auto-generated
            title="Test Event 3",
            date=(start_date + timedelta(days=5)).date().isoformat(), 
            content_type="story",
            description="Third test event"
        )
    ]
    
    # Add events to project
    for event in events:
        if project.add_release_event(event):
            print(f"✅ Added event: {event.title} on {event.date}")
        else:
            print(f"❌ Failed to add event: {event.title}")
    
    # Load project in window
    window.current_project = project
    window._update_timeline_display()
    
    print(f"\n📊 Project has {len(project.release_events)} events")
    print(f"📅 Timeline events by date: {dict(project.timeline_plan.events)}")
    
    # Show window
    window.show()
    
    print("\n🎯 Manual Testing Instructions:")
    print("1. Verify all 3 events are visible on the timeline")
    print("2. Right-click on an event and select 'Edit'")
    print("3. Change the event's date and save")
    print("4. Verify the event moves to the new date immediately")
    print("5. Right-click on an event and select 'Delete'")
    print("6. Verify the event disappears immediately")
    print("7. Check that days with no events show as empty")
    
    print("\n⚠️  If events don't update immediately, the bug is still present")
    print("✅ If events update immediately, the bug is fixed!")
    
    # Start event loop
    return app.exec()


if __name__ == "__main__":
    result = test_timeline_refresh()
    sys.exit(result)
