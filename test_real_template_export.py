#!/usr/bin/env python3
"""
Test script to verify that the export now uses real template data from the UI
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ProjectManager, ReelForgeProject
from pathlib import Path
from ui.template_editor.editor import TemplateEditor
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect
import json

def test_real_template_export():
    """Test that export uses real template data"""
    app = QApplication([])
    
    # Load test project
    project_file = "output/example_project.rforge"
    if not os.path.exists(project_file):
        print(f"Project file {project_file} not found!")
        return False
    
    print(f"Loading project: {project_file}")
    project = ReelForgeProject.load(Path(project_file))
    if not project:
        print("Failed to load project!")
        return False
    
    print(f"Project loaded: {project.metadata.name}")
    
    # Create template editor and configure it
    template_editor = TemplateEditor()
    
    # Set up a reel template with custom positions
    template_editor.set_content_type("reel")
    
    # Get the canvas and modify element positions to test real data export
    canvas = template_editor.canvas
    
    # Modify title position
    if 'title' in canvas.elements:
        canvas.elements['title']['rect'] = QRect(100, 150, 880, 120)  # Custom position
        canvas.elements['title']['size'] = 48  # Custom size
        canvas.elements['title']['color'] = '#FFD700'  # Gold color
        print("Modified title: position (100, 150, 880, 120), size 48, color #FFD700")
    
    # Modify subtitle position  
    if 'subtitle' in canvas.elements:
        canvas.elements['subtitle']['rect'] = QRect(100, 1700, 880, 100)  # Custom position
        canvas.elements['subtitle']['size'] = 28  # Custom size
        canvas.elements['subtitle']['color'] = '#00FF00'  # Green color
        print("Modified subtitle: position (100, 1700, 880, 100), size 28, color #00FF00")
    
    # Modify PiP position
    if 'pip' in canvas.elements:
        canvas.elements['pip']['rect'] = QRect(50, 50, 300, 200)  # Custom position
        canvas.elements['pip']['corner_radius'] = 25  # Custom border radius
        print("Modified PiP: position (50, 50, 300, 200), border radius 25")
    
    # Test export with template editor
    print("\nExporting with real template data...")
    
    # First, let's see what the template editor exports
    export_data = template_editor.export_template_data()
    print(f"Template editor exports elements: {list(export_data.get('elements', {}).keys())}")
    for elem_id, elem_data in export_data.get('elements', {}).items():
        print(f"  {elem_id}: type={elem_data.get('type')}, rect={elem_data.get('rect')}")
    
    ai_data = project.get_ai_generation_data(template_editor=template_editor)
    
    # Check if the exported data contains our custom positions
    templates = ai_data.get('content_generation', {}).get('templates', {})
    reel_template = templates.get('reel', {})
    layout = reel_template.get('layout', {})
    
    print("\nExported layout data:")
    print(f"Templates found: {list(templates.keys())}")
    
    if 'reel' in templates:
        reel_layout = templates['reel'].get('layout', {})
        print(f"Reel template found with layout keys: {list(reel_layout.keys())}")
        
        # Check title
        if 'title' in reel_layout:
            title_pos = reel_layout['title']['position']
            print(f"Title position: x={title_pos['x']}, y={title_pos['y']}, w={title_pos['width']}, h={title_pos['height']}")
            print(f"Title font_size: {reel_layout['title']['font_size']}")
            print(f"Title color: {reel_layout['title']['color']}")
            
            # Verify it's our custom data
            if title_pos['x'] == 100 and title_pos['y'] == 150:
                print("✅ REAL template data detected! Custom title position found.")
            else:
                print("❌ Still using fallback data for title")
        
        # Check subtitle
        if 'subtitle' in reel_layout:
            subtitle_pos = reel_layout['subtitle']['position']
            print(f"Subtitle position: x={subtitle_pos['x']}, y={subtitle_pos['y']}, w={subtitle_pos['width']}, h={subtitle_pos['height']}")
            print(f"Subtitle font_size: {reel_layout['subtitle']['font_size']}")
            print(f"Subtitle color: {reel_layout['subtitle']['color']}")
            
            # Verify it's our custom data
            if subtitle_pos['x'] == 100 and subtitle_pos['y'] == 1700:
                print("✅ REAL template data detected! Custom subtitle position found.")
            else:
                print("❌ Still using fallback data for subtitle")
        
        # Check PiP
        if 'pip_video' in reel_layout:
            pip_pos = reel_layout['pip_video']['position']
            print(f"PiP position: x={pip_pos['x']}, y={pip_pos['y']}, w={pip_pos['width']}, h={pip_pos['height']}")
            print(f"PiP border_radius: {reel_layout['pip_video']['border_radius']}")
            
            # Verify it's our custom data
            if pip_pos['x'] == 50 and pip_pos['y'] == 50:
                print("✅ REAL template data detected! Custom PiP position found.")
            else:
                print("❌ Still using fallback data for PiP")
    else:
        print("❌ No reel template found in export")
    
    # Save export to file for inspection
    output_path = "test_real_template_export.json"
    with open(output_path, 'w') as f:
        json.dump(ai_data, f, indent=2)
    print(f"\nFull export saved to: {output_path}")
    
    app.quit()
    return True

if __name__ == "__main__":
    print("Testing real template data export...")
    test_real_template_export()
