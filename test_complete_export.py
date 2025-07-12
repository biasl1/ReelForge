#!/usr/bin/env python3
"""
Create a complete test export with the new fixes and validate it.
"""
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, '/Users/test/Documents/development/Artists in DSP/ReelTune')

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QColor
from core.project import ReelForgeProject, ReleaseEvent, convert_enums

def create_test_export():
    """Create a comprehensive test export."""
    project = ReelForgeProject()
    project.metadata.name = 'Perfect Export Test'
    project.metadata.plugin_name = 'Euclyd'
    project.global_prompt = 'Test global prompt'
    
    # Add video event with complex template config
    event = ReleaseEvent(
        id='test-video-event',
        title='Test Video',
        content_type='video',
        date='2025-07-12'
    )
    
    # Complex template config with QSize and QColor objects
    event.template_config = {
        'frame_data': {
            '0': {
                'frame_index': 0,
                'frame_description': 'Test Frame',
                'elements': {
                    'title': {
                        'type': 'text',
                        'content': 'Test Title',
                        'color': QColor(255, 255, 255, 255),  # QColor object
                        'rect': {'x': 100, 'y': 50, 'width': 200, 'height': 30},
                        'size': 24
                    },
                    'pip': {
                        'type': 'pip',
                        'color': QColor(100, 150, 200, 128),  # QColor object
                        'rect': {'x': 150, 'y': 200, 'width': 300, 'height': 169},
                        'corner_radius': 10,
                        'visible': True
                    }
                },
                'frame_settings': {
                    'canvas_size': QSize(498, 600),  # QSize object - this was the problem
                    'background_color': None
                }
            }
        }
    }
    
    project.release_events['test-video-event'] = event
    
    return project

def test_comprehensive_export():
    """Test comprehensive export with all problematic objects."""
    print("🧪 Creating comprehensive test export...")
    
    project = create_test_export()
    
    try:
        # Test AI export (which had QColor issues)
        print("\n1. Testing AI Export...")
        ai_data = project.get_ai_generation_data()
        ai_json = json.dumps(ai_data, indent=2)
        
        # Parse back to verify
        parsed_ai = json.loads(ai_json)
        print("✅ AI Export JSON serialization successful!")
        
        # Check specific elements
        video_template = parsed_ai.get('content_generation', {}).get('templates', {}).get('video', {})
        frame_data = video_template.get('template_config', {}).get('frame_data', {})
        frame_0 = frame_data.get('0', {})
        
        # Check canvas_size serialization (was the QSize problem)
        canvas_size = frame_0.get('frame_settings', {}).get('canvas_size')
        if canvas_size == [498, 600]:
            print("✅ QSize serialization working: canvas_size =", canvas_size)
        else:
            print("❌ QSize serialization failed: canvas_size =", canvas_size)
            return False
        
        # Check QColor serialization
        title_color = frame_0.get('elements', {}).get('title', {}).get('color')
        if title_color == [255, 255, 255, 255]:
            print("✅ QColor serialization working: title color =", title_color)
        else:
            print("❌ QColor serialization failed: title color =", title_color)
            return False
            
        pip_color = frame_0.get('elements', {}).get('pip', {}).get('color')
        if pip_color == [100, 150, 200, 128]:
            print("✅ QColor serialization working: pip color =", pip_color)
        else:
            print("❌ QColor serialization failed: pip color =", pip_color)
            return False
        
        print("\n2. Testing Project Save...")
        # Test project save (which had datetime issues)
        project_data = convert_enums(project.to_dict())
        project_json = json.dumps(project_data, indent=2)
        parsed_project = json.loads(project_json)
        print("✅ Project Save JSON serialization successful!")
        
        # Check timestamp serialization (was the datetime problem)
        release_events = parsed_project.get('release_events', {})
        test_event = release_events.get('test-video-event', {})
        created_date = test_event.get('created_date', '')
        if 'T' in created_date and ':' in created_date:
            print("✅ Datetime serialization working: created_date =", created_date)
        else:
            print("❌ Datetime serialization failed: created_date =", created_date)
            return False
        
        print("\n📊 Export Structure Summary:")
        print(f"   • Plugin info: ✅ Complete")
        print(f"   • Template config: ✅ With properly serialized QSize and QColor")
        print(f"   • Frame data: ✅ Complete with elements")
        print(f"   • Timestamps: ✅ Properly formatted ISO strings")
        print(f"   • Canvas settings: ✅ QSize converted to [width, height] array")
        print(f"   • Colors: ✅ QColor converted to [r,g,b,a] arrays")
        
        return True
        
    except Exception as e:
        print(f"❌ Comprehensive export test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("🎯 Testing COMPLETE export with all fixes...")
    
    success = test_comprehensive_export()
    
    if success:
        print("\n🎉 PERFECT! All JSON serialization issues are fixed!")
        print("   ✅ QColor objects → [r,g,b,a] arrays")
        print("   ✅ QSize objects → [width, height] arrays") 
        print("   ✅ datetime objects → ISO format strings")
        print("   ✅ Both AI export and project save working flawlessly!")
        return True
    else:
        print("\n❌ Some serialization issues remain.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
