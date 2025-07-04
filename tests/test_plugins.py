#!/usr/bin/env python3
"""
Test script for ReelForge plugin functionality
Tests .adsp file import and plugin information management
"""

import sys
import tempfile
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject
from core.plugins import PluginManager, PluginInfo


def create_test_adsp_file(temp_dir: Path) -> Path:
    """Create a test .adsp file for testing"""
    test_data = {
        "pluginName": "TestPlugin",
        "pluginTitle": "test plugin",
        "pluginTagline": "a test plugin for content generation",
        "pluginVersion": "1.0.0",
        "pluginCode": "TEST1",
        "short_description": "A simple test plugin for ReelForge testing",
        "long_description": "This is a longer description of the test plugin that explains what it does in more detail.",
        "unique": "This plugin is unique because it's specifically designed for testing ReelForge.",
        "problem": "Solves the problem of not having test data",
        "wow": "The wow factor is that it generates perfect test scenarios",
        "personality": "Helpful and reliable",
        "one_word": "Reliable",
        "category": ["Test", "Development"],
        "intended_use": ["Testing", "Development", "QA"],
        "input_type": "Stereo",
        "has_sidechain": False,
        "tech_summary": "Test plugin with minimal functionality for ReelForge validation",
        "highlightColor": [0, 123, 204],
        "pluginSize": [800, 600],
        "components": [
            {
                "type": "header_company",
                "display_name": "Test Company"
            }
        ],
        "key_parameters": [
            {"name": "volume", "importance": "1"},
            {"name": "filter", "importance": "2"}
        ],
        "changelog": ["v1.0.0 - Initial test version"]
    }

    test_file = temp_dir / "test_plugin.adsp"
    with open(test_file, 'w') as f:
        json.dump(test_data, f, indent=2)

    return test_file


def test_plugin_manager():
    """Test PluginManager functionality"""
    print("🧪 Testing Plugin Manager...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test .adsp file
        adsp_file = create_test_adsp_file(temp_path)

        # Test import
        manager = PluginManager()
        plugin_info = manager.import_adsp_file(adsp_file)

        assert plugin_info is not None, "Failed to import .adsp file"
        assert plugin_info.name == "TestPlugin"
        assert plugin_info.version == "1.0.0"
        assert plugin_info.company == "Test Company"
        assert len(plugin_info.category) == 2

        # Test retrieval
        retrieved = manager.get_plugin("TestPlugin")
        assert retrieved is not None, "Failed to retrieve plugin"
        assert retrieved.name == "TestPlugin"

        # Test content generation data
        gen_data = manager.get_content_generation_data("TestPlugin")
        assert gen_data is not None, "Failed to get generation data"
        assert "plugin_info" in gen_data
        assert "marketing_content" in gen_data
        assert "technical_specs" in gen_data

    print("✅ Plugin Manager tests passed")


def test_project_plugin_integration():
    """Test plugin integration with ReelForge project"""
    print("🧪 Testing Project-Plugin Integration...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test project
        project = ReelForgeProject()
        project.metadata.name = "Plugin Test Project"

        # Create and import test plugin
        adsp_file = create_test_adsp_file(temp_path)
        success = project.import_plugin_info(adsp_file)

        assert success, "Failed to import plugin to project"
        assert project.current_plugin == "TestPlugin"

        # Test plugin retrieval
        plugin_info = project.get_current_plugin_info()
        assert plugin_info is not None, "Failed to get current plugin info"
        assert plugin_info.name == "TestPlugin"

        # Test content generation data
        gen_data = project.get_content_generation_data()
        assert gen_data is not None, "Failed to get generation data from project"
        assert "plugin" in gen_data
        assert "project" in gen_data

    print("✅ Project-Plugin Integration tests passed")


def test_project_serialization_with_plugins():
    """Test project save/load with plugin data"""
    print("🧪 Testing Project Serialization with Plugins...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create project with plugin
        project = ReelForgeProject()
        project.metadata.name = "Serialization Test"

        # Import plugin
        adsp_file = create_test_adsp_file(temp_path)
        project.import_plugin_info(adsp_file)

        # Save project
        project_file = temp_path / "test_project.rforge"
        save_success = project.save(project_file)
        assert save_success, "Failed to save project with plugin"

        # Load project
        loaded_project = ReelForgeProject.load(project_file)
        assert loaded_project is not None, "Failed to load project"

        # Verify plugin data was preserved
        assert loaded_project.current_plugin == "TestPlugin"

        plugin_info = loaded_project.get_current_plugin_info()
        assert plugin_info is not None, "Plugin info not preserved"
        assert plugin_info.name == "TestPlugin"
        assert plugin_info.version == "1.0.0"

        # Verify generation data still works
        gen_data = loaded_project.get_content_generation_data()
        assert gen_data is not None, "Generation data not available after load"

    print("✅ Project Serialization with Plugins tests passed")


def test_ai_prompt_generation():
    """Test AI prompt generation functionality"""
    print("🧪 Testing AI Prompt Generation...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        # Create test plugin
        adsp_file = create_test_adsp_file(temp_path)
        manager = PluginManager()
        plugin_info = manager.import_adsp_file(adsp_file)

        # Test prompt generation for different content types
        from core.plugins import generate_ai_prompts_for_plugin

        for content_type in ["reel", "story", "post", "teaser", "tutorial"]:
            prompts = generate_ai_prompts_for_plugin(plugin_info, content_type)
            assert len(prompts) > 0, f"No prompts generated for {content_type}"

            # Check that prompts contain plugin-specific information
            plugin_mentioned = any(plugin_info.name in prompt for prompt in prompts)
            assert plugin_mentioned, f"Plugin name not mentioned in {content_type} prompts"

    print("✅ AI Prompt Generation tests passed")


def test_adsp_file_parsing():
    """Test parsing of real .adsp file structure"""
    print("🧪 Testing .adsp File Parsing...")

    # Test with the Euclyd2.adsp file if it exists
    euclyd_file = Path(__file__).parent / "Euclyd2.adsp"

    if euclyd_file.exists():
        manager = PluginManager()
        plugin_info = manager.import_adsp_file(euclyd_file)

        if plugin_info:
            assert plugin_info.name == "Euclyd"
            assert plugin_info.tagline == "euclidean multitap delay engine"
            assert plugin_info.company == "Artists in DSP"
            print(f"  ✓ Imported real plugin: {plugin_info.name} v{plugin_info.version}")
        else:
            print("  ⚠️ Could not import Euclyd2.adsp (may not be valid format)")
    else:
        print("  ⚠️ Euclyd2.adsp file not found, skipping real file test")

    print("✅ .adsp File Parsing tests completed")


def main():
    """Run all plugin tests"""
    print("🚀 Starting ReelForge Plugin Tests\n")

    try:
        test_plugin_manager()
        test_project_plugin_integration()
        test_project_serialization_with_plugins()
        test_ai_prompt_generation()
        test_adsp_file_parsing()

        print("\n🎉 All plugin tests passed! Plugin functionality is working correctly.")
        print("\n📋 Plugin System Features Verified:")
        print("  ✅ .adsp file import and parsing")
        print("  ✅ Plugin information management")
        print("  ✅ Project-plugin integration")
        print("  ✅ Plugin data serialization/deserialization")
        print("  ✅ AI prompt generation for content types")
        print("  ✅ Content generation data preparation")

        return True

    except Exception as e:
        print(f"\n❌ Plugin test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
