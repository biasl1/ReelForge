#!/usr/bin/env python3
"""
Test that verifies the complete export functionality works end-to-end
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
from ui.template_editor.editor import TemplateEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor
from pathlib import Path
import json

def test_complete_export_functionality():
    """Test the complete export functionality"""
    app = QApplication([])
    
    # Load real project
    project_file = "output/example_project.rforge"
    if not os.path.exists(project_file):
        print(f"❌ Project file {project_file} not found!")
        return False
    
    print(f"📂 Loading project: {project_file}")
    project = ReelForgeProject.load(Path(project_file))
    if not project:
        print("❌ Failed to load project!")
        return False
    
    print(f"✅ Project loaded: {project.metadata.name}")
    print(f"   Events: {len(project.release_events)}")
    print(f"   Assets: {len(project.get_all_assets())}")
    
    # Create template editor
    template_editor = TemplateEditor()
    print("🎨 Template editor created")
    
    # Configure custom template layouts for different content types
    test_configurations = {
        "reel": {
            "title": {"rect": QRect(80, 120, 920, 140), "size": 52, "color": "#FF6B35"},
            "subtitle": {"rect": QRect(80, 1650, 920, 120), "size": 32, "color": "#4ECDC4"},
            "pip": {"rect": QRect(40, 40, 320, 240), "corner_radius": 20}
        },
        "story": {
            "title": {"rect": QRect(60, 100, 960, 120), "size": 48, "color": "#A8E6CF"},
            "subtitle": {"rect": QRect(60, 1700, 960, 100), "size": 28, "color": "#FFEAA7"},
            "pip": {"rect": QRect(800, 60, 220, 160), "corner_radius": 15}
        },
        "tutorial": {
            "title": {"rect": QRect(100, 80, 1720, 160), "size": 64, "color": "#74B9FF"},
            "subtitle": {"rect": QRect(100, 900, 1720, 120), "size": 36, "color": "#E17055"},
            "pip": {"rect": QRect(1600, 100, 280, 200), "corner_radius": 25}
        }
    }
    
    print("🔧 Configuring custom layouts...")
    
    # Configure each content type
    for content_type, config in test_configurations.items():
        print(f"   Configuring {content_type}...")
        template_editor.set_content_type(content_type)
        
        # Apply custom configurations
        canvas = template_editor.canvas
        
        if 'title' in canvas.elements and 'title' in config:
            title_config = config['title']
            canvas.elements['title']['rect'] = title_config['rect']
            canvas.elements['title']['size'] = title_config['size']
            canvas.elements['title']['color'] = title_config['color']
            print(f"     Title: {title_config['rect'].x()},{title_config['rect'].y()} {title_config['rect'].width()}x{title_config['rect'].height()} size={title_config['size']} color={title_config['color']}")
        
        if 'subtitle' in canvas.elements and 'subtitle' in config:
            subtitle_config = config['subtitle']
            canvas.elements['subtitle']['rect'] = subtitle_config['rect']
            canvas.elements['subtitle']['size'] = subtitle_config['size']
            canvas.elements['subtitle']['color'] = subtitle_config['color']
            print(f"     Subtitle: {subtitle_config['rect'].x()},{subtitle_config['rect'].y()} {subtitle_config['rect'].width()}x{subtitle_config['rect'].height()} size={subtitle_config['size']} color={subtitle_config['color']}")
        
        if 'pip' in canvas.elements and 'pip' in config:
            pip_config = config['pip']
            canvas.elements['pip']['rect'] = pip_config['rect']
            canvas.elements['pip']['corner_radius'] = pip_config['corner_radius']
            print(f"     PiP: {pip_config['rect'].x()},{pip_config['rect'].y()} {pip_config['rect'].width()}x{pip_config['rect'].height()} radius={pip_config['corner_radius']}")
    
    # Reset to reel to test
    template_editor.set_content_type("reel")
    print("🎬 Set to reel content type for testing")
    
    # Export with template editor
    print("\n📤 Exporting with real template data...")
    ai_data = project.get_ai_generation_data(template_editor=template_editor)
    
    # Verify export results
    print("🔍 Verifying export results...")
    templates = ai_data.get('content_generation', {}).get('templates', {})
    
    success_count = 0
    total_checks = 0
    
    for content_type, expected_config in test_configurations.items():
        if content_type in templates:
            template_data = templates[content_type]
            layout = template_data.get('layout', {})
            
            print(f"\n✏️  Checking {content_type} template:")
            
            # Check title
            if 'title' in layout and 'title' in expected_config:
                title_pos = layout['title']['position']
                expected_title = expected_config['title']
                total_checks += 1
                
                if (title_pos['x'] == expected_title['rect'].x() and 
                    title_pos['y'] == expected_title['rect'].y() and
                    layout['title']['font_size'] == expected_title['size'] and
                    layout['title']['color'] == expected_title['color']):
                    print(f"   ✅ Title: REAL data detected!")
                    success_count += 1
                else:
                    print(f"   ❌ Title: Using fallback data")
                    print(f"      Expected: {expected_title['rect'].x()},{expected_title['rect'].y()} size={expected_title['size']} color={expected_title['color']}")
                    print(f"      Got: {title_pos['x']},{title_pos['y']} size={layout['title']['font_size']} color={layout['title']['color']}")
            
            # Check subtitle  
            if 'subtitle' in layout and 'subtitle' in expected_config:
                subtitle_pos = layout['subtitle']['position']
                expected_subtitle = expected_config['subtitle']
                total_checks += 1
                
                if (subtitle_pos['x'] == expected_subtitle['rect'].x() and 
                    subtitle_pos['y'] == expected_subtitle['rect'].y() and
                    layout['subtitle']['font_size'] == expected_subtitle['size'] and
                    layout['subtitle']['color'] == expected_subtitle['color']):
                    print(f"   ✅ Subtitle: REAL data detected!")
                    success_count += 1
                else:
                    print(f"   ❌ Subtitle: Using fallback data")
                    print(f"      Expected: {expected_subtitle['rect'].x()},{expected_subtitle['rect'].y()} size={expected_subtitle['size']} color={expected_subtitle['color']}")
                    print(f"      Got: {subtitle_pos['x']},{subtitle_pos['y']} size={layout['subtitle']['font_size']} color={layout['subtitle']['color']}")
            
            # Check PiP
            if 'pip_video' in layout and 'pip' in expected_config:
                pip_pos = layout['pip_video']['position']
                expected_pip = expected_config['pip']
                total_checks += 1
                
                if (pip_pos['x'] == expected_pip['rect'].x() and 
                    pip_pos['y'] == expected_pip['rect'].y() and
                    pip_pos['width'] == expected_pip['rect'].width() and
                    pip_pos['height'] == expected_pip['rect'].height() and
                    layout['pip_video']['border_radius'] == expected_pip['corner_radius']):
                    print(f"   ✅ PiP: REAL data detected!")
                    success_count += 1
                else:
                    print(f"   ❌ PiP: Using fallback data")
                    print(f"      Expected: {expected_pip['rect'].x()},{expected_pip['rect'].y()} {expected_pip['rect'].width()}x{expected_pip['rect'].height()} radius={expected_pip['corner_radius']}")
                    print(f"      Got: {pip_pos['x']},{pip_pos['y']} {pip_pos['width']}x{pip_pos['height']} radius={layout['pip_video']['border_radius']}")
        else:
            print(f"   ❌ {content_type} template not found in export")
    
    # Save full export
    output_path = "test_complete_export.json"
    with open(output_path, 'w') as f:
        json.dump(ai_data, f, indent=2)
    
    print(f"\n📄 Full export saved to: {output_path}")
    
    # Final result
    print(f"\n🎯 FINAL RESULT:")
    print(f"   ✅ Successful checks: {success_count}/{total_checks}")
    print(f"   📊 Success rate: {(success_count/total_checks*100):.1f}%" if total_checks > 0 else "   📊 No checks performed")
    
    if success_count == total_checks and total_checks > 0:
        print("   🎉 ALL CHECKS PASSED! Real template data export is working perfectly!")
    elif success_count > 0:
        print("   🟡 PARTIAL SUCCESS: Some real template data is being exported.")
    else:
        print("   ❌ FAILURE: Export is still using fallback data.")
    
    app.quit()
    return success_count == total_checks and total_checks > 0

if __name__ == "__main__":
    print("🧪 Testing complete export functionality...")
    print("=" * 60)
    success = test_complete_export_functionality()
    print("=" * 60)
    if success:
        print("🎉 TEST PASSED: Export is working with real template data!")
    else:
        print("❌ TEST FAILED: Export issues detected.")
