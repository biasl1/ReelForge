#!/usr/bin/env python3
"""
Comprehensive test for PiP plugin aspect ratio and corner radius features.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QRect, QPoint
from ui.template_editor.canvas import TemplateCanvas

def test_pip_plugin_features():
    """Test the new PiP plugin features comprehensively."""
    app = QApplication([])
    
    print("🧪 TESTING PiP PLUGIN FEATURES")
    print("=" * 50)
    
    # Create canvas
    canvas = TemplateCanvas()
    canvas.set_content_type('reel')
    
    # Test 1: Basic PiP properties
    print("\n1. Testing basic PiP properties...")
    pip_props = canvas.get_pip_properties('pip')
    print(f"   Default use_plugin_aspect_ratio: {pip_props.get('use_plugin_aspect_ratio', False)}")
    print(f"   Default plugin_aspect_ratio: {pip_props.get('plugin_aspect_ratio', 1.75)}")
    print(f"   Default corner_radius: {pip_props.get('corner_radius', 0)}")
    
    # Test 2: Corner radius
    print("\n2. Testing corner radius...")
    canvas.set_pip_corner_radius('pip', 15)
    pip_props = canvas.get_pip_properties('pip')
    corner_radius = pip_props.get('corner_radius', 0)
    print(f"   Set corner radius to 15: {corner_radius}")
    assert corner_radius == 15, f"Expected 15, got {corner_radius}"
    
    # Test boundary values
    canvas.set_pip_corner_radius('pip', -5)  # Should clamp to 0
    pip_props = canvas.get_pip_properties('pip')
    corner_radius = pip_props.get('corner_radius', 0)
    print(f"   Negative value clamped to: {corner_radius}")
    assert corner_radius == 0, f"Expected 0, got {corner_radius}"
    
    canvas.set_pip_corner_radius('pip', 100)  # Should clamp to 50
    pip_props = canvas.get_pip_properties('pip')
    corner_radius = pip_props.get('corner_radius', 0)
    print(f"   Large value clamped to: {corner_radius}")
    assert corner_radius == 50, f"Expected 50, got {corner_radius}"
    
    # Test 3: Plugin aspect ratio toggle
    print("\n3. Testing plugin aspect ratio toggle...")
    original_rect = canvas.elements['pip']['rect']
    print(f"   Original rect: {original_rect.width()}x{original_rect.height()}")
    
    canvas.toggle_plugin_aspect_ratio('pip', True)
    pip_props = canvas.get_pip_properties('pip')
    enabled = pip_props.get('use_plugin_aspect_ratio', False)
    print(f"   Plugin aspect ratio enabled: {enabled}")
    assert enabled, "Plugin aspect ratio should be enabled"
    
    new_rect = canvas.elements['pip']['rect']
    aspect_ratio = new_rect.width() / new_rect.height()
    expected_ratio = pip_props.get('plugin_aspect_ratio', 1.75)
    print(f"   New rect: {new_rect.width()}x{new_rect.height()}")
    print(f"   Actual aspect ratio: {aspect_ratio:.2f}")
    print(f"   Expected aspect ratio: {expected_ratio:.2f}")
    
    # Allow small tolerance for rounding
    assert abs(aspect_ratio - expected_ratio) < 0.1, f"Aspect ratio mismatch: {aspect_ratio} vs {expected_ratio}"
    
    # Test 4: Load plugin file (if Euclyd exists)
    print("\n4. Testing plugin file loading...")
    euclyd_path = "/Users/test/Documents/development/Artists in DSP/Audio Plugins/WORKING ON/Euclyd/Euclyd.adsp"
    if os.path.exists(euclyd_path):
        success = canvas.load_plugin_aspect_ratio('pip', euclyd_path)
        print(f"   Euclyd plugin loading: {'SUCCESS' if success else 'FAILED'}")
        
        if success:
            pip_props = canvas.get_pip_properties('pip')
            plugin_path = pip_props.get('plugin_file_path', '')
            plugin_ratio = pip_props.get('plugin_aspect_ratio', 1.75)
            enabled = pip_props.get('use_plugin_aspect_ratio', False)
            
            print(f"   Plugin path: {os.path.basename(plugin_path)}")
            print(f"   Plugin aspect ratio: {plugin_ratio:.2f}")
            print(f"   Automatically enabled: {enabled}")
            
            # Check if aspect ratio is applied
            rect = canvas.elements['pip']['rect']
            actual_ratio = rect.width() / rect.height()
            print(f"   Applied aspect ratio: {actual_ratio:.2f}")
            
            assert enabled, "Plugin aspect ratio should be automatically enabled"
            assert abs(actual_ratio - plugin_ratio) < 0.1, f"Aspect ratio not applied correctly"
    else:
        print(f"   Euclyd plugin not found at: {euclyd_path}")
        print("   Testing with manual aspect ratio setting...")
        
        # Test manual aspect ratio setting
        canvas.elements['pip']['plugin_aspect_ratio'] = 2.0
        canvas.elements['pip']['use_plugin_aspect_ratio'] = True
        canvas._apply_plugin_aspect_ratio('pip')
        
        rect = canvas.elements['pip']['rect']
        actual_ratio = rect.width() / rect.height()
        print(f"   Manual 2.0:1 aspect ratio applied: {actual_ratio:.2f}")
        assert abs(actual_ratio - 2.0) < 0.1, f"Manual aspect ratio not applied correctly"
    
    # Test 5: Content type independence with plugin properties
    print("\n5. Testing content type independence with plugin properties...")
    
    # Set up REEL with specific plugin settings
    canvas.set_content_type('reel')
    canvas.set_pip_corner_radius('pip', 20)
    canvas.toggle_plugin_aspect_ratio('pip', True)
    canvas.elements['pip']['plugin_aspect_ratio'] = 1.5
    canvas._apply_plugin_aspect_ratio('pip')
    
    reel_props = canvas.get_pip_properties('pip')
    print(f"   REEL corner radius: {reel_props.get('corner_radius', 0)}")
    print(f"   REEL plugin ratio enabled: {reel_props.get('use_plugin_aspect_ratio', False)}")
    print(f"   REEL plugin ratio: {reel_props.get('plugin_aspect_ratio', 1.75)}")
    
    # Switch to POST and check independence
    canvas.set_content_type('post')
    post_props = canvas.get_pip_properties('image')  # POST uses 'image' element
    print(f"   POST corner radius: {post_props.get('corner_radius', 0)}")
    print(f"   POST plugin ratio enabled: {post_props.get('use_plugin_aspect_ratio', False)}")
    print(f"   POST plugin ratio: {post_props.get('plugin_aspect_ratio', 1.75)}")
    
    # POST should have different default settings
    assert post_props.get('corner_radius', 0) != reel_props.get('corner_radius', 0), "Corner radius should be independent"
    
    # Switch back to REEL and verify settings preserved
    canvas.set_content_type('reel')
    restored_props = canvas.get_pip_properties('pip')
    print(f"   Restored REEL corner radius: {restored_props.get('corner_radius', 0)}")
    print(f"   Restored REEL plugin ratio: {restored_props.get('plugin_aspect_ratio', 1.75)}")
    
    assert restored_props.get('corner_radius', 0) == 20, "REEL corner radius should be preserved"
    assert abs(restored_props.get('plugin_aspect_ratio', 1.75) - 1.5) < 0.01, "REEL plugin ratio should be preserved"
    
    # Test 6: Resize with aspect ratio maintenance
    print("\n6. Testing resize with aspect ratio maintenance...")
    
    # Set up a specific size
    canvas.elements['pip']['rect'] = QRect(100, 100, 200, 100)  # 2:1 ratio
    canvas.elements['pip']['plugin_aspect_ratio'] = 2.0
    canvas.elements['pip']['use_plugin_aspect_ratio'] = True
    
    # Simulate resizing
    canvas.resizing_element = 'pip'
    old_rect = QRect(100, 100, 200, 100)
    new_rect = canvas._calculate_resize(old_rect, old_rect.bottomRight() + QPoint(50, 25), "bottom-right")
    
    new_aspect = new_rect.width() / new_rect.height()
    print(f"   Original size: {old_rect.width()}x{old_rect.height()}")
    print(f"   New size: {new_rect.width()}x{new_rect.height()}")
    print(f"   New aspect ratio: {new_aspect:.2f}")
    print(f"   Expected aspect ratio: 2.00")
    
    assert abs(new_aspect - 2.0) < 0.1, f"Aspect ratio not maintained during resize: {new_aspect}"
    
    print("\n🎉 ALL PiP PLUGIN FEATURE TESTS PASSED!")
    print("✅ Corner radius control works correctly")
    print("✅ Plugin aspect ratio toggle works")
    print("✅ Plugin file loading works (when available)")
    print("✅ Content type independence preserved")
    print("✅ Aspect ratio maintained during resize")
    print("✅ Boundary value handling works")
    
    return True

def main():
    try:
        success = test_pip_plugin_features()
        if success:
            print(f"\n🔥 PiP PLUGIN FEATURES VERIFICATION PASSED! 🔥")
            print("🎯 Ready for integration with UI controls!")
        return 0 if success else 1
    except Exception as e:
        print(f"\n💥 TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
