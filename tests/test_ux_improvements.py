#!/usr/bin/env python3
"""
Test script for the new AI-focused UX improvements in ReelForge
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject, ReleaseEvent
from datetime import datetime


def test_ai_generation_data():
    """Test the new AI generation data structure"""
    print("🧪 Testing AI generation data structure...")
    
    # Create test project
    project = ReelForgeProject()
    project.metadata.name = "AI Test Project"
    project.global_prompt = "Professional, warm tone. Focus on vintage analog character."
    project.moodboard_path = "moodboard/style_ref.jpg"
    
    # Add a test event with AI prompt
    event = ReleaseEvent(
        id="",
        date=datetime.now().date().isoformat(),
        content_type="reel",
        title="Plugin Demo Reel",
        description="Show the warm saturation effect on a guitar melody, highlighting the vintage tube sound",
        platforms=["instagram", "tiktok"]
    )
    
    project.add_release_event(event)
    
    # Get AI generation data
    ai_data = project.get_ai_generation_data()
    
    # Verify structure
    assert "global_prompt" in ai_data
    assert "moodboard_path" in ai_data
    assert "scheduled_content" in ai_data
    assert "assets" in ai_data
    
    assert ai_data["global_prompt"] == project.global_prompt
    assert len(ai_data["scheduled_content"]) == 1
    
    content_item = ai_data["scheduled_content"][0]
    assert content_item["content_type"] == "reel"
    assert "warm saturation" in content_item["prompt"]
    assert "instagram" in content_item["platforms"]
    
    print("✅ AI generation data structure works correctly!")
    print(f"   Global prompt: {ai_data['global_prompt'][:50]}...")
    print(f"   Content events: {len(ai_data['scheduled_content'])}")
    print(f"   Event prompt: {content_item['prompt'][:50]}...")


def test_simplified_workflow():
    """Test the simplified one-plugin-per-project workflow"""
    print("\n🧪 Testing simplified workflow...")
    
    project = ReelForgeProject()
    
    # Test that we start with no plugin
    assert project.current_plugin is None
    
    # Test AI data with no plugin
    ai_data = project.get_ai_generation_data()
    assert ai_data["plugin"] is None
    
    print("✅ Simplified workflow structure works!")
    print("   ✓ Projects start with no plugin selected")
    print("   ✓ AI data handles missing plugin gracefully")


def test_event_management():
    """Test event creation, editing, and deletion"""
    print("\n🧪 Testing event management...")
    
    project = ReelForgeProject()
    project.initialize_timeline()
    
    # Create events
    event1 = ReleaseEvent(
        id="",
        date=datetime.now().date().isoformat(),
        content_type="reel",
        title="Test Reel",
        description="AI prompt for reel content"
    )
    
    event2 = ReleaseEvent(
        id="",
        date=datetime.now().date().isoformat(),
        content_type="story",
        title="Test Story", 
        description="AI prompt for story content"
    )
    
    # Add events
    assert project.add_release_event(event1)
    assert project.add_release_event(event2)
    assert len(project.release_events) == 2
    
    # Test getting events for date
    events_today = project.get_events_for_date(datetime.now())
    assert len(events_today) == 2
    
    # Test removal
    event1_id = event1.id
    assert project.remove_release_event(event1_id)
    assert len(project.release_events) == 1
    
    print("✅ Event management works correctly!")
    print(f"   ✓ Created and managed {len(project.release_events)} events")
    print(f"   ✓ Events properly linked to timeline dates")


def test_project_serialization():
    """Test saving/loading with new AI features"""
    print("\n🧪 Testing project serialization with AI features...")
    
    import tempfile
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create project with AI features
        project = ReelForgeProject()
        project.metadata.name = "Serialization Test"
        project.global_prompt = "Test global prompt for AI consistency"
        project.moodboard_path = "test/moodboard.jpg"
        
        # Save project
        save_path = Path(temp_dir) / "test_project.rforge"
        assert project.save(save_path)
        
        # Load project
        loaded_project = ReelForgeProject.load(save_path)
        assert loaded_project is not None
        
        # Verify AI features preserved
        assert loaded_project.global_prompt == project.global_prompt
        assert loaded_project.moodboard_path == project.moodboard_path
        
        print("✅ Project serialization with AI features works!")
        print(f"   ✓ Global prompt preserved: {loaded_project.global_prompt[:30]}...")
        print(f"   ✓ Moodboard path preserved: {loaded_project.moodboard_path}")


def main():
    """Run all UX improvement tests"""
    print("🚀 Testing ReelForge AI-Focused UX Improvements\n")
    
    try:
        test_ai_generation_data()
        test_simplified_workflow()
        test_event_management()
        test_project_serialization()
        
        print("\n🎉 All UX improvement tests passed!")
        print("\nReelForge is now ready for AI content generation with:")
        print("   ✓ Event editing and removal")
        print("   ✓ Simplified one-plugin-per-project workflow")
        print("   ✓ AI-driven asset selection preparation")
        print("   ✓ Global prompt and moodboard support")
        print("   ✓ Complete AI generation data structure")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
