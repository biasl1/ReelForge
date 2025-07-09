#!/usr/bin/env python3
"""
Quick test to verify the fixed save/load system
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
import tempfile

from ui.template_editor.editor import TemplateEditor
from core.project import ReelForgeProject

def test_fixed_save_load():
    print("=== TESTING FIXED SAVE/LOAD ===")
    
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
        
        # Step 2: Set up TUTORIAL with 4 frames and custom descriptions
        print("2. Setting up TUTORIAL...")
        editor.set_content_type('tutorial')
        
        # Add one more frame to get 4 total
        editor.frame_timeline._add_frame()
        
        # Set custom descriptions
        tutorial_descriptions = [
            'Tutorial step 1',
            'Tutorial step 2', 
            'Tutorial step 3',
            'Tutorial finale'
        ]
        
        for i, desc in enumerate(tutorial_descriptions):
            editor.frame_timeline.set_current_frame(i)
            editor.canvas.set_frame_description(i, desc)
            print(f"   Set tutorial frame {i}: '{desc}'")
        
        # Step 3: Set up REEL with 2 frames and custom descriptions
        print("3. Setting up REEL...")
        editor.set_content_type('reel')
        
        reel_descriptions = ['Custom reel frame 1', 'Custom reel frame 2']
        
        for i, desc in enumerate(reel_descriptions):
            editor.frame_timeline.set_current_frame(i)
            editor.canvas.set_frame_description(i, desc)
            print(f"   Set reel frame {i}: '{desc}'")
        
        # Step 4: Save project
        print("4. Saving project...")
        project = ReelForgeProject()
        project.project_file_path = temp_project_path
        project.save_template_editor_settings(editor)
        project.save()
        
        # Step 5: Load project into new editor
        print("5. Loading project...")
        new_editor = TemplateEditor()
        new_project = ReelForgeProject.load(temp_project_path)
        if new_project:
            new_project.load_template_editor_settings(new_editor)
        
        # Step 6: Verify TUTORIAL descriptions
        print("6. Verifying TUTORIAL...")
        new_editor.set_content_type('tutorial')
        
        tutorial_success = True
        for i, expected_desc in enumerate(tutorial_descriptions):
            new_editor.frame_timeline.set_current_frame(i)
            actual_desc = new_editor.canvas.get_frame_description()
            if actual_desc == expected_desc:
                print(f"   ✅ Tutorial frame {i}: '{actual_desc}'")
            else:
                print(f"   ❌ Tutorial frame {i}: expected '{expected_desc}', got '{actual_desc}'")
                tutorial_success = False
        
        # Step 7: Verify REEL descriptions
        print("7. Verifying REEL...")
        new_editor.set_content_type('reel')
        
        reel_success = True
        for i, expected_desc in enumerate(reel_descriptions):
            new_editor.frame_timeline.set_current_frame(i)
            actual_desc = new_editor.canvas.get_frame_description()
            if actual_desc == expected_desc:
                print(f"   ✅ Reel frame {i}: '{actual_desc}'")
            else:
                print(f"   ❌ Reel frame {i}: expected '{expected_desc}', got '{actual_desc}'")
                reel_success = False
        
        # Final result
        print("\n=== FINAL RESULT ===")
        if tutorial_success and reel_success:
            print("✅ SUCCESS: All descriptions preserved correctly!")
            return True
        else:
            print("❌ FAILURE: Some descriptions were not preserved")
            return False
            
    finally:
        # Cleanup
        try:
            os.unlink(temp_project_path)
        except:
            pass

if __name__ == "__main__":
    success = test_fixed_save_load()
    sys.exit(0 if success else 1)
