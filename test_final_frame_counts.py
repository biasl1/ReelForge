#!/usr/bin/env python3
"""
Final test to demonstrate independent frame counts per content type are working perfectly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.canvas import TemplateCanvas
from ui.template_editor.frame_timeline import FrameTimeline


def test_independent_frame_counts_complete():
    """Complete test demonstrating independent frame counts work perfectly."""
    app = QApplication(sys.argv)
    
    print("🎯 FINAL TEST: Independent Frame Counts Per Content Type")
    print("=" * 60)
    
    # Test data
    content_types = {
        'reel': {'expected_frames': 1, 'description': 'Single frame reel'},
        'story': {'expected_frames': 5, 'description': 'Multi-frame story'},  
        'tutorial': {'expected_frames': 8, 'description': 'Step-by-step tutorial'},
        'post': {'expected_frames': 1, 'description': 'Static post'},
        'teaser': {'expected_frames': 1, 'description': 'Static teaser'}
    }
    
    canvas = TemplateCanvas()
    timeline = FrameTimeline()
    
    all_passed = True
    
    for content_type, info in content_types.items():
        expected_frames = info['expected_frames']
        description = info['description']
        
        print(f"\n📌 Testing {content_type.upper()}: {description}")
        print(f"   Expected frame count: {expected_frames}")
        
        # Test canvas frame count
        canvas_frame_count = canvas.get_content_type_frame_count(content_type)
        print(f"   Canvas reports: {canvas_frame_count} frames")
        
        # Test timeline frame count
        timeline.set_content_type_frames(content_type)
        timeline_frame_count = timeline.get_frame_count()
        print(f"   Timeline reports: {timeline_frame_count} frames")
        
        # Test canvas content type switching
        canvas.set_content_type(content_type)
        if canvas.is_video_content_type(content_type):
            state = canvas.content_states.get(content_type, {})
            actual_frame_count = state.get('frame_count', 0)
            frames = state.get('frames', {})
            print(f"   Canvas state: {actual_frame_count} frames, {len(frames)} frame data")
        else:
            print(f"   Canvas state: Static content (correct)")
        
        # Verify all counts match
        if (canvas_frame_count == expected_frames and 
            timeline_frame_count == expected_frames):
            print(f"   ✅ {content_type.upper()} PASSED - All frame counts match!")
        else:
            print(f"   ❌ {content_type.upper()} FAILED - Frame count mismatch!")
            all_passed = False
    
    print(f"\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL TESTS PASSED! Independent frame counts working perfectly!")
        print("✅ Each content type has its own independent frame count:")
        print("   • reel: 1 frame (single frame video)")
        print("   • story: 5 frames (multi-frame story)")
        print("   • tutorial: 8 frames (step-by-step guide)")
        print("   • post: 1 frame (static content)")
        print("   • teaser: 1 frame (static content)")
        print("\n🎯 TASK COMPLETED SUCCESSFULLY!")
    else:
        print("❌ Some tests failed!")
    
    return all_passed


if __name__ == "__main__":
    success = test_independent_frame_counts_complete()
    sys.exit(0 if success else 1)
