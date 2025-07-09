#!/usr/bin/env python3
"""
Final verification test for description persistence across save/load cycles.
This test will:
1. Create a project with multiple content types
2. Add frames and set custom descriptions for each
3. Save the project
4. Load the project 
5. Verify all descriptions are preserved exactly
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
import tempfile
import json

from ui.template_editor.editor import TemplateEditor
from core.project import ReelForgeProject

def test_description_persistence():
    """Test that descriptions persist through save/load cycles"""
    print("=== Final Description Persistence Test ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Create temporary project file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.rforge', delete=False) as f:
        temp_project_path = f.name
    
    try:
        # Step 1: Create and setup editor
        print("1. Creating template editor...")
        editor = TemplateEditor()
        
        # Step 2: Test multiple content types with custom descriptions
        test_data = {
            'reel': {
                'frame_count': 3,
                'descriptions': ['Custom reel frame 1', 'Custom reel frame 2', 'Custom reel frame 3']
            },
            'story': {
                'frame_count': 2, 
                'descriptions': ['Story intro frame', 'Story conclusion frame']
            },
            'tutorial': {
                'frame_count': 4,
                'descriptions': ['Tutorial step 1', 'Tutorial step 2', 'Tutorial step 3', 'Tutorial finale']
            }
        }
        
        print("2. Setting up content types with custom descriptions...")
        for content_type, data in test_data.items():
            print(f"   Setting up {content_type}...")
            
            # Switch to content type
            editor.set_content_type(content_type)
            
            # Add frames to reach desired count
            current_count = editor.frame_timeline.get_frame_count()
            while current_count < data['frame_count']:
                editor.frame_timeline._add_frame()
                current_count += 1
            
            # Set descriptions for each frame
            for i, description in enumerate(data['descriptions']):
                editor.frame_timeline.set_current_frame(i)
                editor.frame_timeline.frame_description_edit.setText(description)
                editor.frame_timeline._on_description_changed()
                print(f"     Frame {i}: '{description}'")
        
        # Step 3: Save project
        print("3. Saving project...")
        project = ReelForgeProject()
        project.project_file_path = temp_project_path
        project.save_template_editor_settings(editor)
        project.save()
        print(f"   Saved to: {temp_project_path}")
        
        # Step 4: Create new editor and load project
        print("4. Creating new editor and loading project...")
        editor2 = TemplateEditor()
        project2 = ReelForgeProject.load(temp_project_path)
        if project2:
            project2.load_template_editor_settings(editor2)
        else:
            print("   ERROR: Failed to load project")
            return False
        
        # Step 5: Verify all descriptions are preserved
        print("5. Verifying descriptions...")
        all_correct = True
        
        for content_type, data in test_data.items():
            print(f"   Checking {content_type}...")
            
            # Switch to content type
            editor2.set_content_type(content_type)
            
            # Check frame count
            actual_count = editor2.frame_timeline.get_frame_count()
            expected_count = data['frame_count']
            if actual_count != expected_count:
                print(f"     ERROR: Frame count mismatch! Expected {expected_count}, got {actual_count}")
                all_correct = False
                continue
            
            # Check each frame's description
            for i, expected_desc in enumerate(data['descriptions']):
                editor2.frame_timeline.set_current_frame(i)
                actual_desc = editor2.frame_timeline.frame_description_edit.text()
                
                if actual_desc == expected_desc:
                    print(f"     Frame {i}: ✓ '{actual_desc}'")
                else:
                    print(f"     Frame {i}: ✗ Expected '{expected_desc}', got '{actual_desc}'")
                    all_correct = False
        
        # Step 6: Final result
        print("\n=== FINAL RESULT ===")
        if all_correct:
            print("✓ SUCCESS: All descriptions preserved correctly!")
            print("✓ Frame independence working properly!")
            print("✓ Save/load cycle complete!")
        else:
            print("✗ FAILURE: Some descriptions were not preserved correctly")
            
        return all_correct
        
    finally:
        # Cleanup
        try:
            os.unlink(temp_project_path)
        except:
            pass

if __name__ == "__main__":
    success = test_description_persistence()
    sys.exit(0 if success else 1)
