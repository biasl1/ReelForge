#!/usr/bin/env python3

"""
Test timeline content type switching and frame count consistency
"""

import sys
import os
sys.path.append('/Users/test/Documents/development/Artists in DSP/ReelTune')

from PyQt6.QtWidgets import QApplication
from ui.template_editor.frame_timeline import FrameTimeline
from ui.template_editor.canvas import TemplateCanvas

def test_timeline_content_type_switching():
    """Test timeline content type switching and frame count"""
    app = QApplication([])
    
    # Create timeline and canvas
    timeline = FrameTimeline()
    canvas = TemplateCanvas()
    
    # Connect canvas to timeline
    timeline.set_canvas(canvas)
    
    print("\n🧪 Testing timeline content type switching...")
    
    # Test different content types
    content_types = ['reel', 'story', 'tutorial']
    
    for content_type in content_types:
        print(f"\n📋 Testing {content_type}:")
        
        # Switch timeline to content type
        timeline.set_content_type(content_type)
        
        # Check timeline state
        print(f"   Timeline content_type: {timeline.content_type}")
        print(f"   Timeline frame count: {len(timeline.frame_buttons)}")
        print(f"   Timeline current frame: {timeline.current_frame}")
        
        # Check canvas state  
        canvas_frame_count = canvas.get_content_type_frame_count()
        print(f"   Canvas frame count: {canvas_frame_count}")
        
        # Verify consistency
        if timeline.content_type != content_type:
            print(f"   ❌ ERROR: Timeline content_type mismatch! Expected {content_type}, got {timeline.content_type}")
        else:
            print(f"   ✅ Timeline content_type correct")
            
        if len(timeline.frame_buttons) != canvas_frame_count:
            print(f"   ❌ ERROR: Frame count mismatch! Timeline has {len(timeline.frame_buttons)}, Canvas has {canvas_frame_count}")
        else:
            print(f"   ✅ Frame count consistent")
    
    # Test specific tutorial issue
    print(f"\n🎯 Specific tutorial test:")
    timeline.set_content_type('tutorial')
    canvas.set_content_type('tutorial')
    
    print(f"   Timeline content_type after set: {timeline.content_type}")
    print(f"   Timeline frame buttons: {len(timeline.frame_buttons)}")
    print(f"   Canvas tutorial frames: {canvas.get_content_type_frame_count()}")
    
    # Check if they match
    timeline_shows = len(timeline.frame_buttons)
    canvas_has = canvas.get_content_type_frame_count()
    
    if timeline_shows == canvas_has and timeline.content_type == 'tutorial':
        print(f"   ✅ Tutorial timeline working correctly!")
    else:
        print(f"   ❌ Tutorial timeline still broken!")
        print(f"       Timeline thinks content_type = {timeline.content_type}")
        print(f"       Timeline shows {timeline_shows} frames")
        print(f"       Canvas has {canvas_has} frames")
    
    print("\n🏁 Test complete")

if __name__ == "__main__":
    test_timeline_content_type_switching()
