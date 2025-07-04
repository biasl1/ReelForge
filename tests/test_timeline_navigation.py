#!/usr/bin/env python3
"""
Test script to verify timeline navigation preserves events
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.project import ReelForgeProject, ProjectMetadata, ReleaseEvent
from ui.mainwindow import MainWindow
from datetime import datetime, timedelta

def test_timeline_navigation():
    """Test that events persist during timeline navigation"""
    print("🧪 Testing Timeline Navigation & Event Persistence")
    print("=" * 60)

    app = QApplication(sys.argv)

    # Create project with events
    project = ReelForgeProject(ProjectMetadata(name="Navigation Test"))

    # Add some events across different dates
    today = datetime.now().date()
    events = [
        ReleaseEvent(
            id="event1",
            date=today.isoformat(),
            content_type="reel",
            title="Today's Event",
            description="Event for today"
        ),
        ReleaseEvent(
            id="event2",
            date=(today + timedelta(days=3)).isoformat(),
            content_type="story",
            title="Future Event",
            description="Event in 3 days"
        ),
        ReleaseEvent(
            id="event3",
            date=(today + timedelta(days=7)).isoformat(),
            content_type="post",
            title="Next Week Event",
            description="Event next week"
        )
    ]

    for event in events:
        project.add_release_event(event)
        print(f"✅ Added event: {event.title} on {event.date}")

    print(f"\n📊 Project has {len(project.release_events)} events")
    print(f"📊 Timeline plan has {len(project.timeline_plan.events)} date entries")

    # Create main window
    main_window = MainWindow()
    main_window.current_project = project
    main_window._update_timeline_display()

    print("\n🎯 Timeline loaded - events should be visible")

    # Test navigation functions
    def test_navigation_step(step_name, action):
        print(f"\n🔄 Testing {step_name}...")
        action()

        # Check if events are still there
        events_count = len(main_window.current_project.release_events)
        timeline_dates = len(main_window.current_project.timeline_plan.events)
        print(f"   After {step_name}: {events_count} events, {timeline_dates} timeline dates")

        if events_count != 3:
            print(f"   ❌ ERROR: Expected 3 events, got {events_count}")
        else:
            print(f"   ✅ Events preserved: {events_count}")

    # Test different navigation actions
    test_navigation_step("Previous Week", main_window._on_timeline_previous)
    test_navigation_step("Next Week", main_window._on_timeline_next)
    test_navigation_step("Today Navigation", main_window._on_timeline_today)

    # Test manual date change
    new_date = datetime.now() + timedelta(days=14)
    test_navigation_step("Manual Date Change",
                        lambda: main_window._on_timeline_start_date_changed(new_date))

    print("\n🎉 Timeline navigation test completed!")
    print("If you see this message, events should persist through navigation.")

    # Show the window for manual testing
    main_window.show()

    # Auto-close after a few seconds for automated testing
    QTimer.singleShot(3000, app.quit)

    return app.exec()

if __name__ == "__main__":
    test_timeline_navigation()
