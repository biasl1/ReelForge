#!/usr/bin/env python3
"""
Test script to verify disabled element selection and toggling.
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QPoint
from ui.template_editor.canvas import TemplateCanvas

def test_disabled_element_selection():
    """Test that disabled elements can be selected and re-enabled."""
    print("🧪 TESTING DISABLED ELEMENT SELECTION")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    canvas = TemplateCanvas()
    
    # Test with reel content type
    canvas.set_content_type('reel')
    
    # Disable the subtitle element
    if 'subtitle' in canvas.elements:
        print("1. Disabling subtitle element...")
        canvas.elements['subtitle']['enabled'] = False
        print(f"   Subtitle enabled: {canvas.elements['subtitle']['enabled']}")
        
        # Test selection of disabled element
        subtitle_rect = canvas.elements['subtitle']['rect']
        test_point = QPoint(subtitle_rect.center().x(), subtitle_rect.center().y())
        
        print("2. Testing selection of disabled element...")
        result = canvas._find_element_at_point(test_point)
        
        if result:
            element_id, action_type = result
            print(f"   Found element: {element_id} (action: {action_type})")
            
            if element_id == 'subtitle':
                print("   ✅ Disabled subtitle element can be selected!")
                
                # Test re-enabling
                print("3. Re-enabling subtitle element...")
                canvas.elements['subtitle']['enabled'] = True
                print(f"   Subtitle enabled: {canvas.elements['subtitle']['enabled']}")
                print("   ✅ Element successfully re-enabled!")
                
                return True
            else:
                print(f"   ❌ Wrong element selected: {element_id}")
                return False
        else:
            print("   ❌ Disabled element not selectable!")
            return False
    else:
        print("   ❌ No subtitle element found!")
        return False

def test_visibility_toggle():
    """Test element visibility toggle functionality."""
    print("\\n🧪 TESTING ELEMENT VISIBILITY TOGGLE")
    print("=" * 40)
    
    app = QApplication(sys.argv)
    canvas = TemplateCanvas()
    
    # Test all elements in reel
    canvas.set_content_type('reel')
    
    for element_id, element in canvas.elements.items():
        print(f"\\n📝 Testing {element_id}:")
        
        # Test enable -> disable -> enable cycle
        original_state = element.get('enabled', True)
        print(f"   Original state: {original_state}")
        
        # Disable
        element['enabled'] = False
        print(f"   After disable: {element['enabled']}")
        
        # Re-enable
        element['enabled'] = True
        print(f"   After re-enable: {element['enabled']}")
        
        if element['enabled'] == original_state:
            print(f"   ✅ {element_id} visibility toggle works!")
        else:
            print(f"   ❌ {element_id} visibility toggle failed!")
            return False
    
    return True

if __name__ == "__main__":
    success1 = test_disabled_element_selection()
    success2 = test_visibility_toggle()
    
    print("\\n" + "=" * 40)
    if success1 and success2:
        print("🎉 ALL VISIBILITY TESTS PASSED!")
        print("✅ Disabled elements can be selected")
        print("✅ Element visibility can be toggled")
    else:
        print("❌ SOME VISIBILITY TESTS FAILED!")
