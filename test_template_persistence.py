#!/usr/bin/env python3
"""
Test template settings persistence - verify that template configurations are 
properly saved and loaded with projects
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, ProjectMetadata
from ui.template_editor.editor import TemplateEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor
from pathlib import Path
import json
import tempfile
import shutil

def test_template_settings_persistence():
    """Test that template settings are saved and loaded correctly"""
    app = QApplication([])
    
    print("🧪 TESTING TEMPLATE SETTINGS PERSISTENCE")
    print("=" * 50)
    
    # Create a temporary directory for test
    temp_dir = Path(tempfile.mkdtemp())
    test_project_path = temp_dir / "test_project.rforge"
    
    try:
        # 1. Create new project
        print("\n1. 📁 Creating new project...")
        project = ReelForgeProject()
        project.metadata = ProjectMetadata(
            name="Template Test Project",
            description="Test project for template persistence"
        )
        
        # 2. Create template editor and configure custom layouts
        print("2. 🎨 Setting up template editor...")
        template_editor = TemplateEditor()
        
        # Configure custom layouts for different content types
        test_configs = {
            "reel": {
                "title": {"rect": QRect(120, 200, 840, 100), "size": 48, "color": "#FF5722"},
                "subtitle": {"rect": QRect(120, 1600, 840, 80), "size": 24, "color": "#2196F3"},
                "pip": {"rect": QRect(60, 80, 300, 180), "corner_radius": 15}
            },
            "story": {
                "title": {"rect": QRect(80, 160, 920, 120), "size": 52, "color": "#9C27B0"},
                "subtitle": {"rect": QRect(80, 1720, 920, 100), "size": 28, "color": "#FF9800"},
                "pip": {"rect": QRect(760, 40, 280, 200), "corner_radius": 20}
            },
            "tutorial": {
                "title": {"rect": QRect(150, 100, 1620, 140), "size": 56, "color": "#4CAF50"},
                "subtitle": {"rect": QRect(150, 800, 1620, 100), "size": 32, "color": "#F44336"},
                "pip": {"rect": QRect(1500, 120, 360, 240), "corner_radius": 30}
            }
        }
        
        # Apply configurations
        for content_type, config in test_configs.items():
            print(f"   Configuring {content_type}...")
            template_editor.set_content_type(content_type)
            canvas = template_editor.canvas
            
            # Configure elements
            for element_name, element_config in config.items():
                if element_name in canvas.elements:
                    element = canvas.elements[element_name]
                    if element_name in ["title", "subtitle"]:
                        element['rect'] = element_config['rect']
                        element['size'] = element_config['size']
                        element['color'] = element_config['color']
                    elif element_name == "pip":
                        element['rect'] = element_config['rect']
                        element['corner_radius'] = element_config['corner_radius']
        
        template_editor.set_content_type("reel")  # Reset to reel
        print("   ✅ Template configurations applied")
        
        # 3. Save template settings to project
        print("3. 💾 Saving template settings to project...")
        project.save_template_editor_settings(template_editor)
        
        # 4. Save project to file
        print("4. 📝 Saving project to file...")
        success = project.save(test_project_path)
        if not success:
            print("❌ Failed to save project")
            return False
        print(f"   ✅ Project saved to: {test_project_path}")
        
        # 5. Load project from file
        print("5. 📂 Loading project from file...")
        loaded_project = ReelForgeProject.load(test_project_path)
        if not loaded_project:
            print("❌ Failed to load project")
            return False
        print("   ✅ Project loaded successfully")
        
        # 6. Create new template editor and load settings
        print("6. 🔄 Loading template settings into new editor...")
        new_template_editor = TemplateEditor()
        loaded_project.load_template_editor_settings(new_template_editor)
        print("   ✅ Template settings loaded")
        
        # 7. Verify that settings were preserved
        print("7. 🔍 Verifying template settings...")
        
        success_count = 0
        total_checks = 0
        
        for content_type, expected_config in test_configs.items():
            print(f"\n   Checking {content_type}:")
            new_template_editor.set_content_type(content_type)
            canvas = new_template_editor.canvas
            
            for element_name, expected in expected_config.items():
                if element_name in canvas.elements:
                    element = canvas.elements[element_name]
                    total_checks += 1
                    
                    if element_name in ["title", "subtitle"]:
                        # Check position, size, and color
                        actual_rect = element['rect']
                        actual_size = element.get('size', 24)
                        actual_color = element.get('color', '#FFFFFF')
                        
                        expected_rect = expected['rect']
                        expected_size = expected['size']
                        expected_color = expected['color']
                        
                        if (actual_rect.x() == expected_rect.x() and 
                            actual_rect.y() == expected_rect.y() and
                            actual_rect.width() == expected_rect.width() and
                            actual_rect.height() == expected_rect.height() and
                            actual_size == expected_size and
                            actual_color == expected_color):
                            print(f"     ✅ {element_name}: PRESERVED")
                            success_count += 1
                        else:
                            print(f"     ❌ {element_name}: CHANGED")
                            print(f"        Expected: {expected_rect.x()},{expected_rect.y()} {expected_rect.width()}x{expected_rect.height()} size={expected_size} color={expected_color}")
                            print(f"        Actual: {actual_rect.x()},{actual_rect.y()} {actual_rect.width()}x{actual_rect.height()} size={actual_size} color={actual_color}")
                            
                    elif element_name == "pip":
                        # Check position and corner radius
                        actual_rect = element['rect']
                        actual_radius = element.get('corner_radius', 10)
                        
                        expected_rect = expected['rect']
                        expected_radius = expected['corner_radius']
                        
                        if (actual_rect.x() == expected_rect.x() and 
                            actual_rect.y() == expected_rect.y() and
                            actual_rect.width() == expected_rect.width() and
                            actual_rect.height() == expected_rect.height() and
                            actual_radius == expected_radius):
                            print(f"     ✅ {element_name}: PRESERVED")
                            success_count += 1
                        else:
                            print(f"     ❌ {element_name}: CHANGED")
                            print(f"        Expected: {expected_rect.x()},{expected_rect.y()} {expected_rect.width()}x{expected_rect.height()} radius={expected_radius}")
                            print(f"        Actual: {actual_rect.x()},{actual_rect.y()} {actual_rect.width()}x{actual_rect.height()} radius={actual_radius}")
        
        # 8. Test export with loaded settings
        print(f"\n8. 📤 Testing export with loaded settings...")
        ai_data = loaded_project.get_ai_generation_data(template_editor=new_template_editor)
        templates = ai_data.get('content_generation', {}).get('templates', {})
        
        export_success = 0
        for content_type in templates:
            if content_type in test_configs:
                layout = templates[content_type].get('layout', {})
                if layout.get('title') and layout.get('subtitle') and layout.get('pip_video'):
                    export_success += 1
        
        print(f"   ✅ Export successful for {export_success}/{len(test_configs)} content types")
        
        # Final results
        print(f"\n🎯 FINAL RESULTS:")
        print(f"   Template elements checked: {total_checks}")
        print(f"   Successfully preserved: {success_count}")
        print(f"   Success rate: {(success_count/total_checks*100):.1f}%" if total_checks > 0 else "   No checks performed")
        print(f"   Export test: {export_success}/{len(test_configs)} content types")
        
        overall_success = (success_count == total_checks and total_checks > 0 and export_success == len(test_configs))
        
        if overall_success:
            print("   🎉 ALL TESTS PASSED! Template persistence is working perfectly!")
        else:
            print("   ❌ SOME TESTS FAILED! Template persistence needs attention.")
        
        return overall_success
        
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        app.quit()

if __name__ == "__main__":
    success = test_template_settings_persistence()
    if success:
        print("\n✅ TEMPLATE PERSISTENCE TEST PASSED")
    else:
        print("\n❌ TEMPLATE PERSISTENCE TEST FAILED")
