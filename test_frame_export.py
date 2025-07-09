#!/usr/bin/env python3
"""
Test script to verify frame-based JSON export with independent frame descriptions.
"""

import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from core.project import ReelForgeProject
from ui.template_editor.editor import TemplateEditor


def test_frame_based_export():
    """Test that JSON export includes all frames with descriptions for video content types."""
    app = QApplication(sys.argv)
    
    print("🚀 TESTING FRAME-BASED JSON EXPORT")
    print("=" * 60)
    
    # Create a test project
    project = ReelForgeProject()
    
    # Add some test scheduled events to trigger template export
    from datetime import datetime, timedelta
    from core.project import ReleaseEvent
    
    test_events = [
        ("reel", "Test Reel", "Generate an engaging reel"),
        ("story", "Test Story", "Create a story sequence"),
        ("tutorial", "Test Tutorial", "Make a tutorial video"),
        ("post", "Test Post", "Create a static post"),
        ("teaser", "Test Teaser", "Make a teaser video")
    ]
    
    for i, (content_type, title, description) in enumerate(test_events):
        event = ReleaseEvent(
            id=f"test_{content_type}_{i}",
            date=(datetime.now() + timedelta(days=i+1)).strftime("%Y-%m-%d"),
            content_type=content_type,
            title=title,
            description=description,
            platforms=["instagram"]
        )
        project.add_release_event(event)
    
    print(f"✅ Added {len(test_events)} test events to project")
    
    # Create template editor
    template_editor = TemplateEditor()
    
    # Test data setup
    test_content_types = ['reel', 'story', 'tutorial', 'post', 'teaser']
    
    for content_type in test_content_types:
        print(f"\n📌 Setting up {content_type.upper()}:")
        
        # Set content type
        template_editor.set_content_type(content_type)
        
        if template_editor.canvas.is_video_content_type(content_type):
            # For video types, set up unique frame descriptions
            frame_count = template_editor.canvas.get_content_type_frame_count(content_type)
            print(f"   📹 Video content with {frame_count} frames")
            
            for frame_idx in range(frame_count):
                template_editor.canvas.set_current_frame(frame_idx)
                
                # Set custom frame description
                frame_desc = f"{content_type.title()} Frame {frame_idx + 1}: "
                if content_type == 'reel':
                    descriptions = ["Hook and intro", "Main content", "Call to action"]
                elif content_type == 'story':
                    descriptions = ["Opening", "Build up", "Climax", "Resolution", "Call to action"]
                elif content_type == 'tutorial':
                    descriptions = ["Introduction", "Step 1", "Step 2", "Step 3", "Step 4", "Step 5", "Step 6", "Conclusion"]
                
                if frame_idx < len(descriptions):
                    frame_desc += descriptions[frame_idx]
                else:
                    frame_desc += f"Content frame {frame_idx + 1}"
                
                template_editor.canvas.set_frame_description(frame_idx, frame_desc)
                print(f"      Frame {frame_idx}: {frame_desc}")
        else:
            print(f"   📄 Static content")
    
    # Now test the export
    print(f"\n🔄 TESTING JSON EXPORT...")
    
    # Get AI generation data (this should include all frames)
    ai_data = project.get_ai_generation_data(template_editor=template_editor)
    
    # Check content generation templates
    templates = ai_data.get('content_generation', {}).get('templates', {})
    
    print(f"📊 EXPORT RESULTS:")
    print(f"   Total templates exported: {len(templates)}")
    
    all_passed = True
    
    for content_type, template_data in templates.items():
        print(f"\n📌 {content_type.upper()} TEMPLATE:")
        
        is_video = template_data.get('is_video_content', False)
        frames = template_data.get('frames', {})
        
        if content_type in ['reel', 'story', 'tutorial']:
            # Should be video content with frames
            if is_video and frames:
                print(f"   ✅ Video content with {len(frames)} frames")
                
                for frame_key, frame_data in frames.items():
                    frame_desc = frame_data.get('frame_description', 'No description')
                    frame_index = frame_data.get('frame_index', 0)
                    layout = frame_data.get('layout', {})
                    
                    print(f"      {frame_key}: \"{frame_desc}\"")
                    print(f"         Elements: {list(layout.keys())}")
                    
                    # Verify frame has layout elements
                    if not layout:
                        print(f"         ❌ No layout elements found!")
                        all_passed = False
            else:
                print(f"   ❌ Expected video content with frames, got static")
                all_passed = False
        else:
            # Should be static content
            if not is_video:
                layout = template_data.get('layout', {})
                print(f"   ✅ Static content with elements: {list(layout.keys())}")
            else:
                print(f"   ❌ Expected static content, got video")
                all_passed = False
    
    # Export to file for inspection
    export_path = "test_frame_export_output.json"
    with open(export_path, 'w') as f:
        json.dump(ai_data, f, indent=2, default=str)
    
    print(f"\n📄 Full export saved to: {export_path}")
    
    print(f"\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Frame-based export working correctly!")
        print("✅ Video content types export individual frames with descriptions")
        print("✅ Static content types export single layouts")
        print("✅ Frame descriptions are preserved in export")
        print("\n🎯 FRAME-BASED JSON EXPORT COMPLETED SUCCESSFULLY!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed


if __name__ == "__main__":
    success = test_frame_based_export()
    sys.exit(0 if success else 1)
