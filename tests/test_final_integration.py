#!/usr/bin/env python3
"""
Final test to verify the timeline refresh fixes are working correctly
"""

import sys
import os
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ReleaseEvent
from ui.mainwindow import MainWindow


def test_ui_integration():
    """Test the UI integration with real timeline updates"""

    print("🎯 Final Integration Test")
    print("=" * 40)

    app = QApplication(sys.argv)

    # Create main window
    window = MainWindow()

    # Create project with timeline
    project = ReelForgeProject()
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    project.initialize_timeline(start_date, duration_weeks=1)

    # Add test events
    events = []
    for i in range(3):
        event = ReleaseEvent(
            id="",
            title=f"Test Event {i+1}",
            date=(start_date + timedelta(days=i+1)).date().isoformat(),
            content_type="reel",
            description=f"Event {i+1} description"
        )
        events.append(event)
        project.add_release_event(event)

    print(f"✅ Created project with {len(events)} events")

    # Load project in window
    window.current_project = project
    window._update_timeline_display()

    print("✅ Loaded project in main window")
    print("✅ Timeline display updated")

    # Show window
    window.show()

    print("\n🎯 UI Test Instructions:")
    print("=" * 40)
    print("1. You should see 3 events on the timeline")
    print("2. Try right-clicking on an event → 'Delete'")
    print("3. The event should disappear immediately")
    print("4. Try right-clicking on an event → 'Edit'")
    print("5. Change the date and save")
    print("6. The event should move to the new date immediately")
    print("\n⚠️  If any of these don't work, there's still an issue")
    print("✅ If all work correctly, the bug is fixed!")

    # Use a timer to close after a few seconds if running automated
    def auto_close():
        print("\n🔄 Auto-closing test window...")
        window.close()
        app.quit()

    # Auto-close after 10 seconds for automated testing
    timer = QTimer()
    timer.timeout.connect(auto_close)
    timer.start(10000)  # 10 seconds

    # Start the app
    result = app.exec()
    return result


if __name__ == "__main__":
    print("🚀 Starting Final Timeline Integration Test")
    print("   This will open the app with test events loaded")
    print("   Test the event deletion and editing manually")
    print()

    try:
        result = test_ui_integration()
        print(f"\n✅ Test completed with exit code: {result}")
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
