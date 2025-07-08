#!/usr/bin/env python3
"""
Test script to verify element position stability during save operations.
This simulates the exact save workflow that happens when user presses Cmd+S.
"""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from pathlib import Path
import json

# Mock the Qt objects for testing
class MockQRect:
    def __init__(self, x, y, w, h):
        self._x, self._y, self._w, self._h = x, y, w, h
    def x(self): return self._x
    def y(self): return self._y
    def width(self): return self._w
    def height(self): return self._h
    def __repr__(self):
        return f"QRect({self._x}, {self._y}, {self._w}, {self._h})"

class MockQColor:
    def __init__(self, r, g, b, a=255):
        self._r, self._g, self._b, self._a = r, g, b, a
    def red(self): return self._r
    def green(self): return self._g
    def blue(self): return self._b
    def alpha(self): return self._a

class MockCanvas:
    def __init__(self):
        self.content_type = 'reel'
        self.elements = {
            'title': {
                'type': 'text',
                'rect': MockQRect(100, 50, 200, 30),
                'content': 'Test Title',
                'size': 24,
                'color': MockQColor(255, 255, 255)
            },
            'subtitle': {
                'type': 'text', 
                'rect': MockQRect(100, 90, 200, 20),
                'content': 'Test Subtitle',
                'size': 16,
                'color': MockQColor(200, 200, 200)
            }
        }
        self.content_frame = MockQRect(50, 50, 300, 500)
        self.constrain_to_frame = True
        
        # Initialize content states
        self.content_states = {
            'reel': {
                'elements': dict(self.elements),  # Copy current elements
                'content_frame': self.content_frame,
                'constrain_to_frame': self.constrain_to_frame
            },
            'story': {
                'elements': {
                    'title': {
                        'type': 'text',
                        'rect': MockQRect(75, 40, 150, 25),
                        'content': 'Story Title',
                        'size': 20,
                        'color': MockQColor(255, 255, 255)
                    }
                },
                'content_frame': MockQRect(40, 40, 250, 400),
                'constrain_to_frame': False
            }
        }
    
    def _save_current_state(self):
        """Mock save current state"""
        print(f"Mock: Saving current state for {self.content_type}")
        if self.content_type in self.content_states:
            self.content_states[self.content_type]['elements'] = dict(self.elements)
            self.content_states[self.content_type]['content_frame'] = self.content_frame
            self.content_states[self.content_type]['constrain_to_frame'] = self.constrain_to_frame
    
    def get_element_config(self):
        """Mock get element config with deep copy"""
        import copy
        return {
            'content_type': self.content_type,
            'constrain_to_frame': self.constrain_to_frame,
            'elements': copy.deepcopy(dict(self.elements))
        }

class MockTemplateEditor:
    def __init__(self):
        self.canvas = MockCanvas()
    
    def get_content_type(self):
        return self.canvas.content_type
    
    def get_template_config(self):
        """Mock get template config"""
        return {
            'canvas_config': self.canvas.get_element_config()
        }

def test_save_position_stability():
    """Test that the new save method preserves element positions"""
    
    print("🧪 Testing save position stability...")
    
    # Import after setting up mocks
    from core.project import ReelForgeProject
    
    # Create a test project
    project = ReelForgeProject()
    project._project_name = "Position Test"
    project.project_file_path = "/tmp/position_test.rforge"
    
    # Create mock template editor
    template_editor = MockTemplateEditor()
    
    # Capture original positions
    original_positions = {}
    for content_type, state in template_editor.canvas.content_states.items():
        original_positions[content_type] = {}
        for elem_name, elem_data in state['elements'].items():
            rect = elem_data['rect']
            original_positions[content_type][elem_name] = (rect.x(), rect.y(), rect.width(), rect.height())
    
    print("📊 Original positions:")
    for content_type, positions in original_positions.items():
        print(f"  {content_type}:")
        for elem_name, pos in positions.items():
            print(f"    {elem_name}: ({pos[0]}, {pos[1]}, {pos[2]}, {pos[3]})")
    
    # Perform save operation
    print("\n💾 Performing save operation...")
    project.save_template_editor_settings(template_editor)
    
    # Check positions after save
    after_save_positions = {}
    for content_type, state in template_editor.canvas.content_states.items():
        after_save_positions[content_type] = {}
        for elem_name, elem_data in state['elements'].items():
            rect = elem_data['rect']
            after_save_positions[content_type][elem_name] = (rect.x(), rect.y(), rect.width(), rect.height())
    
    print("\n📊 Positions after save:")
    for content_type, positions in after_save_positions.items():
        print(f"  {content_type}:")
        for elem_name, pos in positions.items():
            print(f"    {elem_name}: ({pos[0]}, {pos[1]}, {pos[2]}, {pos[3]})")
    
    # Compare positions
    positions_stable = True
    for content_type in original_positions:
        if content_type in after_save_positions:
            for elem_name in original_positions[content_type]:
                if elem_name in after_save_positions[content_type]:
                    orig = original_positions[content_type][elem_name]
                    after = after_save_positions[content_type][elem_name]
                    if orig != after:
                        print(f"❌ Position changed for {content_type}.{elem_name}: {orig} -> {after}")
                        positions_stable = False
    
    if positions_stable:
        print("✅ All element positions remained stable during save!")
    else:
        print("❌ Element positions shifted during save!")
        return False
    
    # Test project save/load cycle
    print("\n💾 Testing full save/load cycle...")
    
    try:
        # Save project to file
        success = project.save()
        if not success:
            print("❌ Project save failed")
            return False
        
        # Create new project and load
        project2 = ReelForgeProject()
        project2.project_file_path = project.project_file_path
        loaded = project2.load(Path(project.project_file_path))
        
        if not loaded:
            print("❌ Project load failed")
            return False
        
        # Create new template editor and load settings
        template_editor2 = MockTemplateEditor()
        project2.load_template_editor_settings(template_editor2)
        
        # Check if settings were loaded
        if not hasattr(project2, 'template_editor_settings'):
            print("❌ No template settings found after load")
            return False
        
        print("✅ Save/load cycle completed successfully")
        
    except Exception as e:
        print(f"❌ Save/load cycle failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = test_save_position_stability()
    if success:
        print("\n🎉 All position stability tests passed!")
        sys.exit(0)
    else:
        print("\n💥 Position stability tests failed!")
        sys.exit(1)
