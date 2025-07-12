#!/usr/bin/env python3
"""
Test the AI export functionality to verify QSize serialization fix.
"""
import sys
import os
import json

# Add the project root to Python path
sys.path.insert(0, '/Users/test/Documents/development/Artists in DSP/ReelTune')

from PyQt6.QtCore import QSize
from core.project import convert_enums

def test_qsize_conversion():
    """Test QSize object conversion."""
    test_size = QSize(498, 600)
    converted = convert_enums(test_size)
    print(f"Original QSize: {test_size}")
    print(f"Converted: {converted}")
    
    # Should be [width, height] array
    expected = [498, 600]
    if converted == expected:
        print("✅ QSize conversion working correctly!")
        return True
    else:
        print(f"❌ QSize conversion failed. Expected {expected}, got {converted}")
        return False

def test_complex_structure():
    """Test conversion of complex structure with QSize."""
    test_data = {
        "frame_settings": {
            "canvas_size": QSize(498, 600),
            "background_color": None
        },
        "metadata": {
            "name": "test"
        }
    }
    
    converted = convert_enums(test_data)
    print(f"\nOriginal structure: {test_data}")
    print(f"Converted structure: {converted}")
    
    # Check if QSize was properly converted
    canvas_size = converted.get("frame_settings", {}).get("canvas_size")
    if canvas_size == [498, 600]:
        print("✅ Complex structure QSize conversion working!")
        return True
    else:
        print(f"❌ Complex structure conversion failed. canvas_size = {canvas_size}")
        return False

def test_json_serialization():
    """Test full JSON serialization."""
    test_data = {
        "frame_settings": {
            "canvas_size": QSize(498, 600),
            "background_color": None
        }
    }
    
    try:
        converted = convert_enums(test_data)
        json_str = json.dumps(converted, indent=2)
        parsed_back = json.loads(json_str)
        
        print(f"\nJSON serialization test:")
        print(f"Converted data: {converted}")
        print(f"JSON string: {json_str}")
        print(f"Parsed back: {parsed_back}")
        
        # Verify QSize was converted to array
        if parsed_back["frame_settings"]["canvas_size"] == [498, 600]:
            print("✅ Full JSON serialization working!")
            return True
        else:
            print("❌ JSON serialization failed!")
            return False
            
    except Exception as e:
        print(f"❌ JSON serialization error: {e}")
        return False

def main():
    print("🧪 Testing QSize serialization fix...")
    
    tests = [
        test_qsize_conversion,
        test_complex_structure, 
        test_json_serialization
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with error: {e}")
            results.append(False)
    
    success_count = sum(results)
    total_count = len(results)
    
    print(f"\n📊 Test Results: {success_count}/{total_count} passed")
    
    if success_count == total_count:
        print("🎉 All tests passed! QSize serialization is working perfectly!")
        return True
    else:
        print("❌ Some tests failed. QSize serialization needs more work.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
