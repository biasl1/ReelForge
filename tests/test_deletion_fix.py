#!/usr/bin/env python3
"""
Quick test to verify event deletion works after fixing the widget cleanup issue
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent


def test_event_deletion_basic():
    """Basic test of event deletion functionality"""

    print("🧪 Testing Basic Event Deletion")
    print("=" * 40)

    # Create project
    project = ReelForgeProject()
    project.initialize_timeline()

    # Add test event
    event = ReleaseEvent(
        id="",
        title="Test Event",
        date=datetime.now().date().isoformat(),
        content_type="reel",
        description="Test event for deletion"
    )

    # Add event
    if not project.add_release_event(event):
        print("❌ Failed to add event")
        return False

    event_id = event.id
    print(f"✅ Added event with ID: {event_id}")

    # Verify event exists
    if event_id not in project.release_events:
        print("❌ Event not found in release_events after adding")
        return False

    # Delete event
    if not project.remove_release_event(event_id):
        print("❌ Failed to remove event")
        return False

    print(f"✅ Event {event_id} removed successfully")

    # Verify event was deleted
    if event_id in project.release_events:
        print("❌ Event still exists in release_events after deletion")
        return False

    print("✅ Event properly removed from release_events")

    return True


if __name__ == "__main__":
    if test_event_deletion_basic():
        print("\n🎉 Event deletion test PASSED! The backend functionality works.")
        print("   You can now test the UI by opening the app and trying to delete events.")
    else:
        print("\n❌ Event deletion test FAILED!")

    print("\n📝 To test the UI:")
    print("1. Run: python main.py")
    print("2. Create a new project or open an existing one")
    print("3. Add some events to the timeline")
    print("4. Right-click on an event and select 'Delete'")
    print("5. Verify the event disappears from the timeline")
