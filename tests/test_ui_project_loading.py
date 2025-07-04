#!/usr/bin/env python3
"""
UI test to verify events are displayed immediately when loading a project
"""

import sys
import os
from datetime import datetime, timedelta
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent
from ui.mainwindow import MainWindow


def create_test_project_file():
    """Create a test project file with events"""
    project = ReelForgeProject()
    project.metadata.name = "UI Test Project"

    # Initialize timeline
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=1)

    # Add test events
    events = [
        ReleaseEvent(
            id="",
            title="Today's Event",
            date=start_date.date().isoformat(),
            content_type="reel",
            description="Event for today"
        ),
        ReleaseEvent(
            id="",
            title="Tomorrow's Event",
            date=(start_date + timedelta(days=1)).date().isoformat(),
            content_type="post",
            description="Event for tomorrow"
        ),
        ReleaseEvent(
            id="",
            title="Weekend Event",
            date=(start_date + timedelta(days=5)).date().isoformat(),
            content_type="story",
            description="Weekend event"
        )
    ]

    for event in events:
        project.add_release_event(event)

    # Save to temp file
    test_file = Path("/tmp/ui_test_project.rforge")
    project.save(test_file)
    return test_file


def test_ui_project_loading():
    """Test loading project in UI and verifying timeline display"""

    print("🎯 UI Project Loading Test")
    print("=" * 40)

    app = QApplication(sys.argv)

    # Create test project file
    test_file = create_test_project_file()
    print(f"✅ Created test project: {test_file}")

    # Create main window
    window = MainWindow()

    # Load the project using the same method as the UI
    print(f"📂 Loading project using UI method...")
    window._open_project(str(test_file))

    # Check if project was loaded
    if not window.current_project:
        print("❌ Project not loaded in UI")
        return False

    print(f"✅ Project loaded: {window.current_project.metadata.name}")
    print(f"📊 Project has {len(window.current_project.release_events)} events")

    # Check timeline plan
    if not window.current_project.timeline_plan:
        print("❌ No timeline plan in loaded project")
        return False

    timeline_events = window.current_project.timeline_plan.events
    print(f"📅 Timeline has events on dates: {list(timeline_events.keys())}")

    # Show window
    window.show()

    print("\n🎯 UI Verification:")
    print("=" * 40)
    print("✅ Window is now open with the loaded project")
    print("🔍 Check if the timeline shows the 3 events immediately:")
    print("   - Today's Event (red reel indicator)")
    print("   - Tomorrow's Event (blue post indicator)")
    print("   - Weekend Event (purple story indicator)")
    print("\n⚠️  If events are NOT visible immediately, the bug persists")
    print("✅ If events ARE visible immediately, the bug is FIXED!")

    # Auto-close after 15 seconds
    def auto_close():
        print("\n🔄 Auto-closing test window...")
        test_file.unlink()
        window.close()
        app.quit()

    timer = QTimer()
    timer.timeout.connect(auto_close)
    timer.start(15000)  # 15 seconds

    return app.exec()


if __name__ == "__main__":
    print("🚀 Starting UI Project Loading Test")
    print("   This will create a project with events and load it in the UI")
    print("   Check if events are immediately visible on the timeline")
    print()

    try:
        result = test_ui_project_loading()
        print(f"\n✅ Test completed with exit code: {result}")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
