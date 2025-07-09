#!/usr/bin/env python3
"""
Comprehensive final test - shows what's happening with frame descriptions 
during save/load with extensive debugging
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

def test_comprehensive_description_persistence():
    """Test exactly what happens with descriptions during save/load"""
    print("=== COMPREHENSIVE DESCRIPTION PERSISTENCE TEST ===")
    
    app = QApplication.instance()
    if app is None:
        app = QApplication([])
    
    # Create temporary project file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.rforge', delete=False) as f:
        temp_project_path = f.name
    
    try:
        print("\n1. SETUP: Creating and configuring editor...")
        editor = TemplateEditor()
        
        # Test with simpler data to isolate the issue
        test_data = {
            'reel': {
                'frame_count': 2,
                'descriptions': ['REEL_DESC_1', 'REEL_DESC_2']
            },
            'story': {
                'frame_count': 2, 
                'descriptions': ['STORY_DESC_1', 'STORY_DESC_2']
            }
        }
        
        print("\n2. INPUT: Setting up content types...")
        for content_type, data in test_data.items():
            print(f"\n--- Setting up {content_type.upper()} ---")
            editor.set_content_type(content_type)
            
            # Ensure we have the right number of frames
            current_count = editor.frame_timeline.get_frame_count()
            print(f"   Current frame count: {current_count}")
            
            # Add frames if needed
            while current_count < data['frame_count']:
                editor.frame_timeline._add_frame()
                current_count += 1
                print(f"   Added frame, now have: {current_count}")
            
            # Remove frames if we have too many
            while current_count > data['frame_count']:
                editor.frame_timeline._remove_frame_at_index(current_count - 1)
                current_count -= 1
                print(f"   Removed frame, now have: {current_count}")
            
            # Set descriptions for each frame
            for i, description in enumerate(data['descriptions']):
                print(f"   Frame {i}: Setting '{description}'")
                editor.frame_timeline.set_current_frame(i)
                editor.frame_timeline.frame_description_edit.setText(description)
                editor.frame_timeline._on_description_changed()
                
                # Verify it was set
                actual = editor.frame_timeline.frame_description_edit.text()
                print(f"   Frame {i}: Verified '{actual}'")
        
        print("\n3. PRE-SAVE STATE: Checking what's in canvas...")
        for content_type in test_data.keys():
            editor.set_content_type(content_type)
            if hasattr(editor.canvas, 'content_states'):
                state = editor.canvas.content_states.get(content_type, {})
                frames = state.get('frames', {})
                print(f"\n   {content_type.upper()} canvas state:")
                print(f"     Frame count: {len(frames)}")
                for frame_idx, frame_data in frames.items():
                    desc = frame_data.get('frame_description', 'NO_DESC')
                    print(f"     Frame {frame_idx}: '{desc}'")
        
        print("\n4. SAVE: Saving project...")
        project = ReelForgeProject()
        project.project_file_path = temp_project_path
        project.save_template_editor_settings(editor)
        success = project.save()
        if not success:
            print("   ERROR: Save failed!")
            return False
        print(f"   ✅ Saved to: {temp_project_path}")
        
        print("\n5. LOAD: Loading project...")
        editor2 = TemplateEditor()
        project2 = ReelForgeProject.load(temp_project_path)
        if not project2:
            print("   ERROR: Load failed!")
            return False
        
        project2.load_template_editor_settings(editor2)
        print("   ✅ Loaded template settings")
        
        print("\n6. POST-LOAD STATE: Checking what's in canvas...")
        for content_type in test_data.keys():
            editor2.set_content_type(content_type)
            if hasattr(editor2.canvas, 'content_states'):
                state = editor2.canvas.content_states.get(content_type, {})
                frames = state.get('frames', {})
                print(f"\n   {content_type.upper()} canvas state:")
                print(f"     Frame count: {len(frames)}")
                for frame_idx, frame_data in frames.items():
                    desc = frame_data.get('frame_description', 'NO_DESC')
                    print(f"     Frame {frame_idx}: '{desc}'")
        
        print("\n7. VERIFICATION: Checking UI descriptions...")
        all_correct = True
        
        for content_type, data in test_data.items():
            print(f"\n   Checking {content_type.upper()}...")
            editor2.set_content_type(content_type)
            
            # Check frame count
            actual_count = editor2.frame_timeline.get_frame_count()
            expected_count = data['frame_count']
            if actual_count != expected_count:
                print(f"     ❌ Frame count: expected {expected_count}, got {actual_count}")
                all_correct = False
                continue
            else:
                print(f"     ✅ Frame count: {actual_count}")
            
            # Check each frame's description
            for i, expected_desc in enumerate(data['descriptions']):
                editor2.frame_timeline.set_current_frame(i)
                actual_desc = editor2.frame_timeline.frame_description_edit.text()
                
                if actual_desc == expected_desc:
                    print(f"     ✅ Frame {i}: '{actual_desc}'")
                else:
                    print(f"     ❌ Frame {i}: Expected '{expected_desc}', got '{actual_desc}'")
                    all_correct = False
        
        print("\n=== FINAL RESULT ===")
        if all_correct:
            print("✅ SUCCESS: All descriptions preserved correctly!")
        else:
            print("❌ FAILURE: Some descriptions were not preserved correctly")
            
        return all_correct
        
    finally:
        # Cleanup
        try:
            os.unlink(temp_project_path)
        except:
            pass

if __name__ == "__main__":
    success = test_comprehensive_description_persistence()
    sys.exit(0 if success else 1)
