#!/usr/bin/env python3
"""
Test script for ReelForge timeline functionality
Run this to verify the timeline canvas works correctly
"""

import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject, ReleaseEvent, TimelinePlan


def test_timeline_initialization():
    """Test timeline plan initialization"""
    print("🧪 Testing timeline initialization...")
    
    project = ReelForgeProject()
    assert project.timeline_plan is None
    
    # Initialize timeline
    project.initialize_timeline()
    assert project.timeline_plan is not None
    assert project.timeline_plan.duration_weeks == 1
    assert project.timeline_plan.start_date is not None
    
    print("✅ Timeline initialization successful")


def test_event_management():
    """Test release event management"""
    print("🧪 Testing event management...")
    
    project = ReelForgeProject()
    project.initialize_timeline()
    
    # Create test event
    event = ReleaseEvent(
        id="",
        date=datetime.now().date().isoformat(),
        content_type="reel",
        title="Test Reel",
        description="A test reel for our plugin",
        platforms=["instagram", "tiktok"],
        hashtags=["#plugin", "#music"]
    )
    
    # Add event
    success = project.add_release_event(event)
    assert success, "Failed to add event"
    assert len(project.release_events) == 1
    assert event.date in project.timeline_plan.events
    
    # Get events for date
    events = project.get_events_for_date(datetime.now())
    assert len(events) == 1
    assert events[0].title == "Test Reel"
    
    # Remove event
    removed = project.remove_release_event(event.id)
    assert removed, "Failed to remove event"
    assert len(project.release_events) == 0
    
    print("✅ Event management successful")


def test_timeline_serialization():
    """Test timeline data save/load"""
    print("🧪 Testing timeline serialization...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create project with timeline
        project = ReelForgeProject()
        project.metadata.name = "Timeline Test Project"
        project.initialize_timeline()
        
        # Add test event
        event = ReleaseEvent(
            id="",
            date=(datetime.now() + timedelta(days=1)).date().isoformat(),
            content_type="story",
            title="Test Story",
            description="Instagram story for plugin launch"
        )
        project.add_release_event(event)
        
        # Save project
        save_path = Path(temp_dir) / "timeline_test.rforge"
        success = project.save(save_path)
        assert success, "Failed to save project with timeline"
        
        # Load project
        loaded_project = ReelForgeProject.load(save_path)
        assert loaded_project is not None, "Failed to load project"
        assert loaded_project.timeline_plan is not None, "Timeline plan not loaded"
        assert len(loaded_project.release_events) == 1, "Events not loaded"
        
        # Verify event data
        loaded_event = list(loaded_project.release_events.values())[0]
        assert loaded_event.title == "Test Story"
        assert loaded_event.content_type == "story"
        
    print("✅ Timeline serialization successful")


def test_date_range_queries():
    """Test date range event queries"""
    print("🧪 Testing date range queries...")
    
    project = ReelForgeProject()
    project.initialize_timeline()
    
    # Add events for different dates
    today = datetime.now()
    for i in range(5):
        event_date = today + timedelta(days=i)
        event = ReleaseEvent(
            id="",
            date=event_date.date().isoformat(),
            content_type="post",
            title=f"Day {i+1} Post",
            description=f"Content for day {i+1}"
        )
        project.add_release_event(event)
    
    # Test range query
    start_date = today
    end_date = today + timedelta(days=2)
    events_in_range = project.get_events_in_range(start_date, end_date)
    
    assert len(events_in_range) == 3, f"Expected 3 events, got {len(events_in_range)}"
    
    print("✅ Date range queries successful")


def test_timeline_navigation():
    """Test timeline duration and navigation"""
    print("🧪 Testing timeline navigation...")
    
    project = ReelForgeProject()
    project.initialize_timeline()
    
    # Test duration update
    original_duration = project.timeline_plan.duration_weeks
    project.update_timeline_duration(3)
    assert project.timeline_plan.duration_weeks == 3
    assert project.is_modified
    
    # Test invalid duration
    project.update_timeline_duration(5)  # Should be clamped to 4
    assert project.timeline_plan.duration_weeks == 4
    
    print("✅ Timeline navigation successful")


def main():
    """Run all timeline tests"""
    print("🚀 Starting ReelForge Timeline Tests\n")
    
    try:
        test_timeline_initialization()
        test_event_management()
        test_timeline_serialization()
        test_date_range_queries()
        test_timeline_navigation()
        
        print("\n🎉 All timeline tests passed! Timeline functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Timeline test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
