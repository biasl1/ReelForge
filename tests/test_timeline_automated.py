#!/usr/bin/env python3
"""
Automated test for timeline refresh functionality
Tests the specific cases that were causing refresh issues
"""

import sys
import os
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent


def test_event_update_functionality():
    """Test the event update functionality that was causing refresh issues"""

    print("🔍 Testing Event Update Functionality")
    print("=" * 50)

    # Create test project
    project = ReelForgeProject()

    # Initialize timeline
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=2)

    # Create test event
    original_event = ReleaseEvent(
        id="",  # Will be auto-generated
        title="Test Event",
        date=(start_date + timedelta(days=2)).date().isoformat(),
        content_type="reel",
        description="Original description"
    )

    # Add event to project
    if not project.add_release_event(original_event):
        print("❌ Failed to add original event")
        return False

    event_id = original_event.id
    original_date = original_event.date
    new_date = (start_date + timedelta(days=5)).date().isoformat()

    print(f"✅ Added event: {original_event.title} (ID: {event_id})")
    print(f"📅 Original date: {original_date}")
    print(f"📅 Target new date: {new_date}")

    # Verify event is in original date
    if original_date not in project.timeline_plan.events:
        print(f"❌ Event not found in timeline at original date {original_date}")
        return False

    if event_id not in project.timeline_plan.events[original_date]:
        print(f"❌ Event ID {event_id} not found in timeline events for {original_date}")
        return False

    print(f"✅ Event correctly placed at original date")

    # Test updating the event (change date)
    updated_event = ReleaseEvent(
        id=event_id,  # Keep same ID
        title="Updated Test Event",
        date=new_date,
        content_type="reel",
        description="Updated description"
    )

    print(f"\n🔄 Updating event to new date: {new_date}")

    # Use the update method that should properly handle date changes
    if not project.update_release_event(updated_event):
        print("❌ Failed to update event")
        return False

    print(f"✅ Event update completed")

    # Verify event was moved correctly
    print(f"\n🔍 Verifying event placement after update...")

    # Check that event is no longer at original date
    if original_date in project.timeline_plan.events:
        if event_id in project.timeline_plan.events[original_date]:
            print(f"❌ Event still found at original date {original_date}")
            return False
        print(f"✅ Event removed from original date {original_date}")
    else:
        print(f"✅ Original date {original_date} removed from timeline (no events)")

    # Check that event is now at new date
    if new_date not in project.timeline_plan.events:
        print(f"❌ New date {new_date} not found in timeline")
        return False

    if event_id not in project.timeline_plan.events[new_date]:
        print(f"❌ Event ID {event_id} not found at new date {new_date}")
        return False

    print(f"✅ Event correctly placed at new date {new_date}")

    # Verify event data was updated
    stored_event = project.release_events[event_id]
    if stored_event.date != new_date:
        print(f"❌ Stored event date {stored_event.date} doesn't match expected {new_date}")
        return False

    if stored_event.title != "Updated Test Event":
        print(f"❌ Stored event title '{stored_event.title}' doesn't match expected 'Updated Test Event'")
        return False

    print(f"✅ Event data correctly updated")

    # Test event deletion
    print(f"\n🗑️  Testing event deletion...")

    if not project.remove_release_event(event_id):
        print("❌ Failed to remove event")
        return False

    print(f"✅ Event removal completed")

    # Verify event was deleted correctly
    if event_id in project.release_events:
        print(f"❌ Event {event_id} still in release_events after deletion")
        return False

    print(f"✅ Event removed from release_events")

    # Verify timeline was cleaned up
    if new_date in project.timeline_plan.events:
        if event_id in project.timeline_plan.events[new_date]:
            print(f"❌ Event ID {event_id} still in timeline at {new_date}")
            return False
        if not project.timeline_plan.events[new_date]:
            print(f"✅ Empty date {new_date} cleaned up from timeline")
        else:
            print(f"✅ Event removed from timeline at {new_date}")
    else:
        print(f"✅ Date {new_date} cleaned up from timeline")

    print(f"\n🎉 All tests passed! Event update and deletion work correctly.")
    return True


def test_timeline_data_consistency():
    """Test that timeline data remains consistent during operations"""

    print("\n🔍 Testing Timeline Data Consistency")
    print("=" * 50)

    project = ReelForgeProject()
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=1)

    # Add multiple events
    events = []
    for i in range(3):
        event = ReleaseEvent(
            id="",
            title=f"Event {i+1}",
            date=(start_date + timedelta(days=i+1)).date().isoformat(),
            content_type="reel",
            description=f"Event {i+1} description"
        )
        events.append(event)
        project.add_release_event(event)

    print(f"✅ Added {len(events)} events")

    # Verify consistency
    timeline_event_count = sum(len(event_ids) for event_ids in project.timeline_plan.events.values())
    release_event_count = len(project.release_events)

    if timeline_event_count != release_event_count:
        print(f"❌ Inconsistency: {timeline_event_count} events in timeline, {release_event_count} in release_events")
        return False

    print(f"✅ Data consistency verified: {timeline_event_count} events")

    # Test updating one event's date
    event_to_update = events[1]  # Second event
    new_date = (start_date + timedelta(days=6)).date().isoformat()

    updated_event = ReleaseEvent(
        id=event_to_update.id,
        title=event_to_update.title + " Updated",
        date=new_date,
        content_type=event_to_update.content_type,
        description=event_to_update.description + " Updated"
    )

    project.update_release_event(updated_event)

    # Verify consistency after update
    timeline_event_count = sum(len(event_ids) for event_ids in project.timeline_plan.events.values())
    release_event_count = len(project.release_events)

    if timeline_event_count != release_event_count:
        print(f"❌ Inconsistency after update: {timeline_event_count} events in timeline, {release_event_count} in release_events")
        return False

    print(f"✅ Data consistency maintained after update: {timeline_event_count} events")

    # Test removing one event
    event_to_remove = events[0]  # First event
    project.remove_release_event(event_to_remove.id)

    # Verify consistency after removal
    timeline_event_count = sum(len(event_ids) for event_ids in project.timeline_plan.events.values())
    release_event_count = len(project.release_events)

    if timeline_event_count != release_event_count:
        print(f"❌ Inconsistency after removal: {timeline_event_count} events in timeline, {release_event_count} in release_events")
        return False

    print(f"✅ Data consistency maintained after removal: {timeline_event_count} events")

    return True


if __name__ == "__main__":
    print("🧪 Running Timeline Refresh Tests")
    print("=" * 60)

    success = True

    # Test event update functionality
    if not test_event_update_functionality():
        success = False

    # Test data consistency
    if not test_timeline_data_consistency():
        success = False

    print("\n" + "=" * 60)
    if success:
        print("🎉 ALL TESTS PASSED! Timeline refresh functionality is working correctly.")
        print("✅ Event updates and deletions should now refresh the UI immediately.")
    else:
        print("❌ SOME TESTS FAILED! There are still issues with timeline functionality.")

    sys.exit(0 if success else 1)
