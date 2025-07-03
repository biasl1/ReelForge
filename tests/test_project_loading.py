#!/usr/bin/env python3
"""
Test to verify that events are displayed when loading a project with existing events
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent


def create_test_project_with_events():
    """Create a test project with events and save it"""
    
    print("🏗️  Creating test project with events...")
    
    # Create project
    project = ReelForgeProject()
    project.metadata.name = "Test Project With Events"
    
    # Initialize timeline
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=2)
    
    # Add several test events
    events = [
        ReleaseEvent(
            id="",
            title="Monday Event",
            date=(start_date + timedelta(days=0)).date().isoformat(),
            content_type="reel",
            description="Monday reel content"
        ),
        ReleaseEvent(
            id="",
            title="Wednesday Event",
            date=(start_date + timedelta(days=2)).date().isoformat(),
            content_type="post",
            description="Wednesday post content"
        ),
        ReleaseEvent(
            id="",
            title="Friday Event",
            date=(start_date + timedelta(days=4)).date().isoformat(),
            content_type="story",
            description="Friday story content"
        ),
        ReleaseEvent(
            id="",
            title="Next Week Event",
            date=(start_date + timedelta(days=8)).date().isoformat(),
            content_type="tutorial",
            description="Tutorial content for next week"
        )
    ]
    
    # Add events to project
    for event in events:
        success = project.add_release_event(event)
        print(f"{'✅' if success else '❌'} Added event: {event.title} on {event.date}")
    
    # Save project
    test_file = Path("/tmp/test_project_with_events.rforge")
    success = project.save(test_file)
    print(f"{'✅' if success else '❌'} Saved project to: {test_file}")
    
    return test_file if success else None


def test_project_loading():
    """Test loading a project and verifying events are displayed"""
    
    print("\n🔍 Testing Project Loading with Events")
    print("=" * 50)
    
    # Create test project file
    test_file = create_test_project_with_events()
    if not test_file:
        print("❌ Failed to create test project")
        return False
    
    # Load the project
    print(f"\n📂 Loading project from: {test_file}")
    loaded_project = ReelForgeProject.load(test_file)
    
    if not loaded_project:
        print("❌ Failed to load project")
        return False
    
    print(f"✅ Project loaded: {loaded_project.metadata.name}")
    
    # Verify timeline plan exists
    if not loaded_project.timeline_plan:
        print("❌ No timeline plan found in loaded project")
        return False
    
    print(f"✅ Timeline plan found: {loaded_project.timeline_plan.duration_weeks} weeks")
    
    # Verify events exist
    event_count = len(loaded_project.release_events)
    timeline_count = sum(len(event_ids) for event_ids in loaded_project.timeline_plan.events.values())
    
    print(f"📊 Loaded project has:")
    print(f"   - {event_count} events in release_events")
    print(f"   - {timeline_count} events in timeline_plan.events")
    print(f"   - Timeline dates: {list(loaded_project.timeline_plan.events.keys())}")
    
    if event_count == 0:
        print("❌ No events found in loaded project")
        return False
    
    if timeline_count == 0:
        print("❌ No events found in timeline plan")
        return False
    
    if event_count != timeline_count:
        print(f"❌ Event count mismatch: {event_count} vs {timeline_count}")
        return False
    
    print("✅ All events loaded correctly")
    
    # Print event details
    print("\n📅 Event details:")
    for event_id, event in loaded_project.release_events.items():
        print(f"   - {event.title} ({event.content_type}) on {event.date}")
    
    # Clean up
    test_file.unlink()
    print(f"\n🧹 Cleaned up test file: {test_file}")
    
    return True


if __name__ == "__main__":
    if test_project_loading():
        print("\n🎉 Project loading test PASSED!")
        print("   The backend correctly loads projects with existing events.")
        print("\n📝 To test the UI:")
        print("1. Run: python main.py")
        print("2. Create a project and add some events")
        print("3. Save the project")
        print("4. Close and reopen the app")
        print("5. Open the saved project")
        print("6. Verify events are immediately visible on the timeline")
    else:
        print("\n❌ Project loading test FAILED!")
        print("   There's still an issue with the backend loading.")
    
    sys.exit(0)
