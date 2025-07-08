#!/usr/bin/env python3
"""
Test script to verify subtitle elements exist in all content types.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from PyQt6.QtWidgets import QApplication
from ui.template_editor.canvas import TemplateCanvas

def test_subtitle_elements():
    """Test that all content types have subtitle elements."""
    print("🧪 TESTING SUBTITLE ELEMENTS IN ALL CONTENT TYPES")
    print("=" * 55)
    
    app = QApplication(sys.argv)
    canvas = TemplateCanvas()
    
    success = True
    
    for content_type in ['reel', 'story', 'post', 'teaser', 'tutorial']:
        canvas.set_content_type(content_type)
        elements = canvas.elements
        
        print(f"\n📝 {content_type.upper()}:")
        print(f"   Elements: {list(elements.keys())}")
        
        has_subtitle = 'subtitle' in elements
        print(f"   Has subtitle: {'✅' if has_subtitle else '❌'} {has_subtitle}")
        
        if has_subtitle:
            subtitle = elements['subtitle']
            enabled = subtitle.get('enabled', False)
            content = subtitle.get('content', '')
            print(f"   Subtitle enabled: {'✅' if enabled else '❌'} {enabled}")
            print(f"   Subtitle content: \"{content}\"")
            print(f"   Subtitle type: {subtitle.get('type', 'unknown')}")
        else:
            print("   ❌ MISSING SUBTITLE ELEMENT!")
            success = False
    
    print("\n" + "=" * 55)
    if success:
        print("🎉 ALL CONTENT TYPES HAVE SUBTITLE ELEMENTS!")
    else:
        print("❌ SOME CONTENT TYPES MISSING SUBTITLE ELEMENTS!")
    
    return success

if __name__ == "__main__":
    test_subtitle_elements()
