#!/usr/bin/env python3
"""
Test script to verify that both QColor and datetime objects are properly 
handled in JSON serialization for the new per-event template system.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from datetime import datetime
from PyQt6.QtGui import QColor
from core.project import convert_enums, Project
import json

def test_qcolor_serialization():
    """Test that QColor objects are properly converted for JSON export."""
    print("🎨 Testing QColor serialization...")
    
    # Create test data with QColor
    test_data = {
        'element': {
            'type': 'text',
            'content': 'Test Text',
            'color': QColor(255, 128, 64),  # Orange color
            'background': QColor(0, 0, 0, 128)  # Semi-transparent black
        }
    }
    
    # Convert using our function
    converted = convert_enums(test_data)
    
    # Try to serialize to JSON
    try:
        json_str = json.dumps(converted, indent=2)
        print("✅ QColor serialization successful!")
        print(f"   Color values: {converted['element']['color']}")
        print(f"   Background values: {converted['element']['background']}")
        return True
    except Exception as e:
        print(f"❌ QColor serialization failed: {e}")
        return False

def test_datetime_serialization():
    """Test that datetime objects are properly converted for JSON export."""
    print("\n⏰ Testing datetime serialization...")
    
    # Create test data with datetime
    test_data = {
        'created_date': datetime.now(),
        'modified_date': datetime(2025, 7, 12, 14, 30, 0),
        'events': [
            {
                'date': datetime.now(),
                'title': 'Test Event'
            }
        ]
    }
    
    # Convert using our function
    converted = convert_enums(test_data)
    
    # Try to serialize to JSON
    try:
        json_str = json.dumps(converted, indent=2)
        print("✅ Datetime serialization successful!")
        print(f"   Created date: {converted['created_date']}")
        print(f"   Modified date: {converted['modified_date']}")
        return True
    except Exception as e:
        print(f"❌ Datetime serialization failed: {e}")
        return False

def test_combined_serialization():
    """Test mixed QColor and datetime serialization (real-world scenario)."""
    print("\n🔄 Testing combined QColor + datetime serialization...")
    
    # Create realistic template data
    template_data = {
        'event_id': 'test-event-123',
        'created_date': datetime.now(),
        'template_config': {
            'frame_0': {
                'elements': {
                    'title': {
                        'type': 'text',
                        'content': 'Video Title',
                        'color': QColor(255, 255, 255),
                        'rect': [100, 50, 400, 60],
                        'size': 30
                    },
                    'subtitle': {
                        'type': 'text',
                        'content': 'Subtitle',
                        'color': QColor(200, 200, 200),
                        'rect': [100, 120, 400, 40],
                        'size': 20
                    }
                }
            }
        },
        'modified_date': datetime.now()
    }
    
    # Convert using our function
    converted = convert_enums(template_data)
    
    # Try to serialize to JSON
    try:
        json_str = json.dumps(converted, indent=2)
        print("✅ Combined serialization successful!")
        print(f"   Template has {len(converted['template_config']['frame_0']['elements'])} elements")
        return True
    except Exception as e:
        print(f"❌ Combined serialization failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing JSON serialization for ReelTune per-event template system\n")
    
    results = []
    results.append(test_qcolor_serialization())
    results.append(test_datetime_serialization())
    results.append(test_combined_serialization())
    
    print(f"\n📊 Test Results: {sum(results)}/{len(results)} passed")
    
    if all(results):
        print("🎉 All JSON serialization tests passed! Both QColor and datetime objects are properly handled.")
    else:
        print("⚠️  Some serialization tests failed. Check the errors above.")
        sys.exit(1)
