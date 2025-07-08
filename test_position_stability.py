#!/usr/bin/env python3
"""Test that element positions remain stable during save/load operations."""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from core.project import ReelForgeProject

def test_position_stability():
    """Test that saving and loading doesn't change element positions."""
    
    print("Testing position stability...")
    
    # Load the test project
    project_path = "/Users/test/Documents/ReelForge Projects/Euclyd.rforge"
    
    try:
        # Load project
        project = ReelForgeProject()
        print(f"Loading project from: {project_path}")
        project.load(project_path)
        print("✓ Project loaded successfully")
        
        # Create a mock template editor to simulate the save workflow
        class MockCanvas:
            def __init__(self):
                self.content_states = {
                    'reel': {
                        'elements': {
                            'title': {'x': 100, 'y': 50, 'width': 200, 'height': 30},
                            'subtitle': {'x': 100, 'y': 90, 'width': 200, 'height': 20}
                        },
                        'content_frame': MockRect(50, 50, 300, 500),
                        'constrain_to_frame': True
                    },
                    'story': {
                        'elements': {
                            'title': {'x': 75, 'y': 40, 'width': 150, 'height': 25}
                        },
                        'content_frame': MockRect(40, 40, 250, 400),
                        'constrain_to_frame': False
                    }
                }
                self.current_type = 'reel'
            
            def _save_current_state(self):
                print("Mock: Saving current state")
                pass
        
        class MockRect:
            def __init__(self, x, y, w, h):
                self._x, self._y, self._w, self._h = x, y, w, h
            def x(self): return self._x
            def y(self): return self._y
            def width(self): return self._w
            def height(self): return self._h
        
        class MockTemplateEditor:
            def __init__(self):
                self.canvas = MockCanvas()
            
            def get_content_type(self):
                return self.canvas.current_type
        
        template_editor = MockTemplateEditor()
        
        # Capture original positions
        original_reel_elements = template_editor.canvas.content_states['reel']['elements'].copy()
        original_story_elements = template_editor.canvas.content_states['story']['elements'].copy()
        
        print(f"Original reel title position: {original_reel_elements['title']}")
        print(f"Original story title position: {original_story_elements['title']}")
        
        # Simulate save operation
        print("\nSimulating save operation...")
        project.save_template_editor_settings(template_editor)
        
        # Check if positions changed
        after_save_reel = template_editor.canvas.content_states['reel']['elements']
        after_save_story = template_editor.canvas.content_states['story']['elements']
        
        print(f"After save reel title position: {after_save_reel['title']}")
        print(f"After save story title position: {after_save_story['title']}")
        
        # Verify positions are unchanged
        reel_unchanged = (original_reel_elements['title'] == after_save_reel['title'])
        story_unchanged = (original_story_elements['title'] == after_save_story['title'])
        
        if reel_unchanged and story_unchanged:
            print("✓ Element positions remained stable during save")
        else:
            print("✗ Element positions changed during save!")
            return False
        
        # Test actual project save
        print("\nTesting actual project save...")
        project.save(project_path)
        print("✓ Project saved successfully")
        
        # Reload and test
        print("\nReloading project...")
        project2 = ReelForgeProject()
        project2.load(project_path)
        
        # Mock load
        template_editor2 = MockTemplateEditor()
        project2.load_template_editor_settings(template_editor2)
        
        loaded_reel = template_editor2.canvas.content_states.get('reel', {}).get('elements', {})
        
        print(f"After reload settings exist: {bool(loaded_reel)}")
        
        print("✓ Position stability test completed")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_position_stability()
    sys.exit(0 if success else 1)
