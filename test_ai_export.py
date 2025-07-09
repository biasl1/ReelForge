#!/usr/bin/env python3
"""
Test AI export to ensure frame descriptions and element data are properly exported.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject
from pathlib import Path
from PyQt6.QtWidgets import QApplication

def test_ai_export():
    """Test the AI export functionality."""
    app = QApplication(sys.argv)
    
    # Load the project
    project_path = "/Users/test/Documents/ReelForge Projects/euclyd.rforge"
    project = ReelForgeProject.load(Path(project_path))
    
    if not project:
        print("❌ Failed to load project")
        return
    
    print("✅ Project loaded successfully")
    
    # Create a template editor to get full data
    from ui.template_editor.editor import TemplateEditor
    template_editor = TemplateEditor()
    
    # Load template editor settings from project
    project.load_template_editor_settings(template_editor)
    
    # Test AI export with template editor
    content_types = ['reel', 'story', 'tutorial']
    
    for content_type in content_types:
        print(f"\n🔍 Testing AI export for {content_type}:")
        
        # Switch to this content type in the template editor
        template_editor.set_content_type(content_type)
        
        try:
            ai_data = project.get_ai_generation_data(template_editor=template_editor)
            print(f"  ✅ Export successful for {content_type}")
            
            # Check if frames are included
            if 'frames' in ai_data:
                frames = ai_data['frames']
                print(f"  📊 Found {len(frames)} frames")
                
                # Check each frame for description and elements
                for frame_idx, frame_data in frames.items():
                    description = frame_data.get('frame_description', 'No description')
                    elements = frame_data.get('elements', {})
                    print(f"    Frame {frame_idx}: '{description}' with {len(elements)} elements")
                    
                    # Check if elements have positions
                    for elem_name, elem_data in elements.items():
                        if 'rect' in elem_data:
                            rect = elem_data['rect']
                            print(f"      {elem_name}: position {rect}")
            else:
                print(f"  ❌ No frames found in AI data for {content_type}")
            
            # Check global description
            global_desc = ai_data.get('description', 'No global description')
            print(f"  📝 Global description: '{global_desc}'")
            
            # Check content type description
            content_desc = ai_data.get('content_type_description', 'No content type description')
            print(f"  📝 Content type description: '{content_desc}'")
            
        except Exception as e:
            print(f"  ❌ Export failed for {content_type}: {e}")
            import traceback
            traceback.print_exc()
    
    app.quit()

if __name__ == "__main__":
    test_ai_export()
