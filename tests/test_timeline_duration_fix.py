#!/usr/bin/env python3
"""
Test Timeline Duration Fix
Verify that timeline duration changes work correctly and events are shown
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.project import ReelForgeProject, ReleaseEvent
from ui.mainwindow import MainWindow

def test_timeline_duration_fix():
    """Test timeline duration changes and save/load"""
    print("🧪 Testing Timeline Duration Fix")
    print("="*50)

    # Create project
    project = ReelForgeProject()
    project.metadata.name = "Timeline Duration Test"

    # Create timeline with 1 week duration
    start_date = datetime.now()
    project.initialize_timeline(start_date, duration_weeks=1)
    print(f"✅ Initialized timeline: {project.timeline_plan.duration_weeks} weeks")

    # Add test events across multiple weeks
    today = start_date.date()
    week1_date = today.isoformat()
    week2_date = (today + timedelta(days=7)).isoformat()
    week3_date = (today + timedelta(days=14)).isoformat()
    week4_date = (today + timedelta(days=21)).isoformat()

    events = [
        ReleaseEvent(id="week1", date=week1_date, content_type="reel", title="Week 1 Content"),
        ReleaseEvent(id="week2", date=week2_date, content_type="story", title="Week 2 Content"),
        ReleaseEvent(id="week3", date=week3_date, content_type="post", title="Week 3 Content"),
        ReleaseEvent(id="week4", date=week4_date, content_type="tutorial", title="Week 4 Content")
    ]

    for event in events:
        project.add_release_event(event)
        print(f"✅ Added event: {event.title} on {event.date}")

    print(f"\n📊 Project state:")
    print(f"   • Timeline duration: {project.timeline_plan.duration_weeks} weeks")
    print(f"   • Total events: {len(project.release_events)}")
    print(f"   • Events by date: {len(project.timeline_plan.events)} dates")

    # Test save/load
    temp_file = Path(tempfile.gettempdir()) / "timeline_duration_test.rforge"
    print(f"\n💾 Testing save/load...")

    if project.save(temp_file):
        print(f"✅ Project saved to {temp_file}")

        # Load project
        loaded_project = ReelForgeProject.load(temp_file)
        if loaded_project:
            print(f"✅ Project loaded successfully")
            print(f"   • Loaded duration: {loaded_project.timeline_plan.duration_weeks} weeks")
            print(f"   • Loaded events: {len(loaded_project.release_events)}")

            # Test UI
            app = QApplication.instance() or QApplication(sys.argv)

            print(f"\n🎨 Testing UI with different durations...")
            main_window = MainWindow()
            main_window.current_project = loaded_project
            main_window._update_timeline_display()
            main_window.show()

            def test_durations():
                print("\n🔄 Testing duration changes...")

                # Test 1 week
                print("Testing 1 week duration...")
                main_window.timeline_controls.duration_group.button(1).click()

                # Test 2 weeks
                print("Testing 2 weeks duration...")
                main_window.timeline_controls.duration_group.button(2).click()

                # Test 3 weeks
                print("Testing 3 weeks duration...")
                main_window.timeline_controls.duration_group.button(3).click()

                # Test 4 weeks
                print("Testing 4 weeks duration...")
                main_window.timeline_controls.duration_group.button(4).click()

                # Check if events are visible
                canvas_events = {}
                for date_str, day_cell in main_window.timeline_canvas.day_cells.items():
                    if day_cell.events:
                        canvas_events[date_str] = len(day_cell.events)

                print(f"\n📋 Events visible on canvas: {len(canvas_events)} dates")
                for date_str, count in canvas_events.items():
                    print(f"   • {date_str}: {count} events")

                print(f"\n🎯 Timeline canvas duration: {main_window.timeline_canvas.duration_weeks} weeks")
                print(f"🎯 Project duration: {main_window.current_project.timeline_plan.duration_weeks} weeks")

                # Test save after duration change
                print(f"\n💾 Testing save after duration change...")
                if main_window.current_project.save():
                    print("✅ Project saved successfully")

                    # Reload and check
                    reloaded = ReelForgeProject.load(temp_file)
                    if reloaded:
                        print(f"✅ Reloaded duration: {reloaded.timeline_plan.duration_weeks} weeks")
                        print(f"✅ Reloaded events: {len(reloaded.release_events)}")

                print("\n🎉 Timeline duration fix test completed!")
                app.quit()

            # Run duration tests after UI loads
            QTimer.singleShot(1000, test_durations)

            # Clean up
            temp_file.unlink()

            return app.exec()

    return 0

if __name__ == "__main__":
    sys.exit(test_timeline_duration_fix())
