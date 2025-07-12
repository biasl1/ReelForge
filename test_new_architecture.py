#!/usr/bin/env python3
"""
Test script for the new VIDEO/PICTURE event architecture
"""

import sys
import os
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from core.project import ReelForgeProject, ReleaseEvent, ProjectMetadata
    from core.logging_config import log_info, log_error, log_warning
    
    def test_new_architecture():
        """Test the new VIDEO/PICTURE event architecture"""
        print("🧪 Testing new VIDEO/PICTURE event architecture...")
        
        # Create a test project
        project = ReelForgeProject()
        project.metadata = ProjectMetadata(
            name="Test Project",
            description="Testing VIDEO/PICTURE architecture"
        )
        
        print("✅ Created test project")
        
        # Test creating VIDEO events
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        # Create VIDEO event
        video_event_id = project.create_event_with_template(
            date=today.isoformat(),
            content_type="video",
            title="Test Video Event",
            description="A test video event with multiple frames",
            frame_count=3
        )
        
        print(f"✅ Created VIDEO event: {video_event_id}")
        
        # Create PICTURE event
        picture_event_id = project.create_event_with_template(
            date=tomorrow.isoformat(),
            content_type="picture",
            title="Test Picture Event",
            description="A test picture event"
        )
        
        print(f"✅ Created PICTURE event: {picture_event_id}")
        
        # Test event template management
        video_frame_count = project.get_event_frame_count(video_event_id)
        picture_frame_count = project.get_event_frame_count(picture_event_id)
        
        assert video_frame_count == 3, f"Expected 3 frames for video, got {video_frame_count}"
        assert picture_frame_count == 1, f"Expected 1 frame for picture, got {picture_frame_count}"
        
        print("✅ Frame counts are correct")
        
        # Test setting frame data
        frame_data = {
            "elements": {
                "title": {"text": "Test Title", "position": {"x": 100, "y": 50}},
                "subtitle": {"text": "Test Subtitle", "position": {"x": 100, "y": 400}}
            },
            "frame_description": "Test frame description"
        }
        
        success = project.set_event_frame_data(video_event_id, 0, frame_data)
        assert success, "Failed to set frame data"
        
        # Test getting frame data
        retrieved_data = project.get_event_frame_data(video_event_id, 0)
        assert retrieved_data == frame_data, "Retrieved frame data doesn't match"
        
        print("✅ Frame data management works")
        
        # Test getting events for dates
        today_events = project.get_events_for_date(today)
        tomorrow_events = project.get_events_for_date(tomorrow)
        
        assert len(today_events) == 1, f"Expected 1 event for today, got {len(today_events)}"
        assert len(tomorrow_events) == 1, f"Expected 1 event for tomorrow, got {len(tomorrow_events)}"
        
        assert today_events[0].content_type == "video", "Today's event should be VIDEO"
        assert tomorrow_events[0].content_type == "picture", "Tomorrow's event should be PICTURE"
        
        print("✅ Event retrieval by date works")
        
        # Test save/load cycle
        with tempfile.TemporaryDirectory() as temp_dir:
            test_file = Path(temp_dir) / "test_project.rforge"
            
            # Save project
            save_success = project.save(test_file)
            assert save_success, "Failed to save project"
            
            print("✅ Project saved successfully")
            
            # Load project
            loaded_project = ReelForgeProject.load(test_file)
            assert loaded_project is not None, "Failed to load project"
            
            # Verify loaded data
            loaded_today_events = loaded_project.get_events_for_date(today)
            loaded_tomorrow_events = loaded_project.get_events_for_date(tomorrow)
            
            assert len(loaded_today_events) == 1, "Loaded project missing today's event"
            assert len(loaded_tomorrow_events) == 1, "Loaded project missing tomorrow's event"
            
            assert loaded_today_events[0].content_type == "video", "Loaded VIDEO event type incorrect"
            assert loaded_tomorrow_events[0].content_type == "picture", "Loaded PICTURE event type incorrect"
            
            # Test frame data persistence
            loaded_frame_data = loaded_project.get_event_frame_data(
                loaded_today_events[0].id, 0
            )
            assert loaded_frame_data == frame_data, "Frame data not persisted correctly"
            
            print("✅ Project load/save cycle works")
        
        print("\n🎉 All tests passed! The new VIDEO/PICTURE architecture is working correctly.")
        return True
        
    if __name__ == "__main__":
        try:
            test_new_architecture()
            print("\n✨ Architecture refactoring complete and tested!")
        except Exception as e:
            print(f"\n❌ Test failed: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
            
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("Make sure you're running this from the project root directory")
    sys.exit(1)
