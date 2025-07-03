#!/usr/bin/env python3
"""
Test script for ReelForge core functionality
Run this to verify the application foundation works correctly
"""

import sys
import tempfile
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject, ProjectMetadata, AssetReference, ProjectManager
from core.assets import AssetManager
from core.utils import validate_project_name, safe_filename


def test_project_creation():
    """Test project creation and basic operations"""
    print("🧪 Testing project creation...")
    
    # Create new project
    project = ReelForgeProject()
    assert project.project_name == "Untitled Project"
    assert len(project.get_all_assets()) == 0
    assert not project.is_modified
    
    print("✅ Project creation successful")


def test_project_serialization():
    """Test project save/load functionality"""
    print("🧪 Testing project serialization...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create and save project
        project = ReelForgeProject()
        project.metadata.name = "Test Project"
        project.metadata.description = "Test description"
        
        save_path = Path(temp_dir) / "test_project.rforge"
        success = project.save(save_path)
        assert success, "Failed to save project"
        assert save_path.exists(), "Project file not created"
        
        # Load project
        loaded_project = ReelForgeProject.load(save_path)
        assert loaded_project is not None, "Failed to load project"
        assert loaded_project.project_name == "Test Project"
        assert loaded_project.metadata.description == "Test description"
        
    print("✅ Project serialization successful")


def test_asset_management():
    """Test asset management functionality"""
    print("🧪 Testing asset management...")
    
    project = ReelForgeProject()
    
    # Add test asset
    asset = AssetReference(
        id="test_asset_1",
        name="test_video.mp4",
        file_path="assets/test_video.mp4",
        file_type="video",
        file_size=1024000
    )
    
    success = project.add_asset(asset)
    assert success, "Failed to add asset"
    assert len(project.get_all_assets()) == 1
    assert project.is_modified, "Project should be marked as modified"
    
    # Retrieve asset
    retrieved = project.get_asset("test_asset_1")
    assert retrieved is not None, "Failed to retrieve asset"
    assert retrieved.name == "test_video.mp4"
    
    # Remove asset
    removed = project.remove_asset("test_asset_1")
    assert removed, "Failed to remove asset"
    assert len(project.get_all_assets()) == 0
    
    print("✅ Asset management successful")


def test_validation_functions():
    """Test utility validation functions"""
    print("🧪 Testing validation functions...")
    
    # Test project name validation
    valid, msg = validate_project_name("Valid Project Name")
    assert valid, f"Valid name rejected: {msg}"
    
    valid, msg = validate_project_name("")
    assert not valid, "Empty name should be invalid"
    
    valid, msg = validate_project_name("Invalid<>Name")
    assert not valid, "Name with invalid characters should be rejected"
    
    # Test safe filename
    safe_name = safe_filename("Test Project: With Symbols!")
    assert "<" not in safe_name and ":" not in safe_name
    
    print("✅ Validation functions successful")


def test_project_manager():
    """Test project manager functionality"""
    print("🧪 Testing project manager...")
    
    manager = ProjectManager()
    templates = manager.get_project_templates()
    
    assert "Social Media - Square" in templates
    assert "Social Media - Vertical" in templates
    assert "YouTube - Landscape" in templates
    
    # Test template structure
    square_template = templates["Social Media - Square"]
    assert "format" in square_template
    assert "fps" in square_template
    assert "description" in square_template
    
    print("✅ Project manager successful")


def test_asset_manager():
    """Test asset manager functionality"""
    print("🧪 Testing asset manager...")
    
    manager = AssetManager()
    
    # Test file type detection
    assert manager._get_file_type(".mp4") == "video"
    assert manager._get_file_type(".jpg") == "image"
    assert manager._get_file_type(".wav") == "audio"
    assert manager._get_file_type(".txt") == "other"
    
    # Test file size formatting
    assert manager.format_file_size(1024) == "1.0 KB"
    assert manager.format_file_size(1048576) == "1.0 MB"
    assert manager.format_file_size(0) == "0 B"
    
    print("✅ Asset manager successful")


def main():
    """Run all tests"""
    print("🚀 Starting ReelForge Core Tests\n")
    
    try:
        test_project_creation()
        test_project_serialization()
        test_asset_management()
        test_validation_functions()
        test_project_manager()
        test_asset_manager()
        
        print("\n🎉 All tests passed! ReelForge core functionality is working correctly.")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
