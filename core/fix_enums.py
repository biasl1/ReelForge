"""
Fix for ConfigMode JSON serialization issue
Run this once to patch the issue
"""

import json
import enum
from pathlib import Path
import os
import sys

# Add parent directory to path so we can import the modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# We need to import the modules but only check them
from core.content_generation import ConfigParameter, SubtitleTemplate, OverlayTemplate, TimingTemplate, ContentTemplate, ConfigMode

# Create a test instance of each class
subtitle = SubtitleTemplate()
overlay = OverlayTemplate()
timing = TimingTemplate()

# Convert them to dict
subtitle_dict = subtitle.to_dict()
overlay_dict = overlay.to_dict()
timing_dict = timing.to_dict()

print("Testing JSON serialization of each template type...")

# Test if they can be converted to JSON
try:
    json.dumps(subtitle_dict)
    print("✓ SubtitleTemplate is serializable")
except Exception as e:
    print(f"✗ SubtitleTemplate is not serializable: {e}")
    
try:
    json.dumps(overlay_dict)
    print("✓ OverlayTemplate is serializable")
except Exception as e:
    print(f"✗ OverlayTemplate is not serializable: {e}")
    
try:
    json.dumps(timing_dict)
    print("✓ TimingTemplate is serializable")
except Exception as e:
    print(f"✗ TimingTemplate is not serializable: {e}")

# Define the fixed function
def convert_enums(obj):
    """Recursively convert all Enum objects to their string values for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_enums(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_enums(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_enums(i) for i in tuple)
    elif isinstance(obj, set):
        return {convert_enums(i) for i in obj}
    elif isinstance(obj, enum.Enum):
        print(f"Found enum: {type(obj).__name__}.{obj.name} = {obj.value}")
        return obj.value
    else:
        return obj

# Create test data
test_data = {
    "mode": ConfigMode.FIXED,
    "nested": {
        "mode": ConfigMode.GUIDED,
        "list_of_enums": [ConfigMode.FREE, ConfigMode.FIXED],
    }
}

# Convert with our function
converted = convert_enums(test_data)
print("\nTest converting enum directly:")
print(f"Before: {test_data}")
print(f"After: {converted}")

# Try serializing
try:
    json_str = json.dumps(converted)
    print("✓ Converted data is serializable!")
except Exception as e:
    print(f"✗ Converted data is still not serializable: {e}")

# Create test instances
print("\nTesting conversion of template class instances:")
subtitle_fixed = convert_enums(subtitle.to_dict())
overlay_fixed = convert_enums(overlay.to_dict())
timing_fixed = convert_enums(timing.to_dict())

# Test if they can be converted to JSON after fixing
try:
    json.dumps(subtitle_fixed)
    print("✓ Fixed SubtitleTemplate is serializable")
except Exception as e:
    print(f"✗ Fixed SubtitleTemplate is still not serializable: {e}")
    
try:
    json.dumps(overlay_fixed)
    print("✓ Fixed OverlayTemplate is serializable")
except Exception as e:
    print(f"✗ Fixed OverlayTemplate is still not serializable: {e}")
    
try:
    json.dumps(timing_fixed)
    print("✓ Fixed TimingTemplate is serializable")
except Exception as e:
    print(f"✗ Fixed TimingTemplate is still not serializable: {e}")

print("\nSUMMARY:")
print("If any templates are not serializable even after conversion,")
print("you need to update their to_dict() methods to return primitive types.")
print("\nIf the fixed versions are serializable, use convert_enums() before JSON serialization.")
print("\nExample fix for export_ai_data_to_json:")
print("""
def export_ai_data_to_json(self, file_path: str) -> bool:
    try:
        ai_data = self.get_ai_generation_data()
        ai_data = convert_enums(ai_data)  # <-- This is the key line
        with open(file_path, 'w') as f:
            json.dump(ai_data, f, indent=2)
        return True
    except Exception as e:
        log_error(f"Failed to export AI generation data: {e}")
        return False
""")

print("\nEnsure convert_enums is used in all export methods that use to_dict()")
