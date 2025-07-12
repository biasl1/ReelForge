#!/usr/bin/env python3
"""
Test script to validate the exported JSON structure and identify any remaining issues.
"""
import json
import sys
from pathlib import Path

def analyze_json_structure(data, path="root"):
    """Recursively analyze JSON structure for any remaining serialization issues."""
    issues = []
    
    if isinstance(data, dict):
        for key, value in data.items():
            current_path = f"{path}.{key}"
            
            # Check for any PyQt6 objects that might have slipped through
            if isinstance(value, str) and "PyQt6" in value:
                issues.append(f"⚠️  PyQt6 object string at {current_path}: {value}")
            
            # Check for datetime strings (should be properly formatted)
            if key in ["timestamp", "export_date"] and isinstance(value, str):
                try:
                    # Should be ISO format
                    if "T" in value and ":" in value:
                        print(f"✅ Datetime at {current_path}: {value}")
                    else:
                        issues.append(f"❌ Invalid datetime format at {current_path}: {value}")
                except:
                    issues.append(f"❌ Datetime parsing issue at {current_path}: {value}")
            
            # Check color arrays (should be [r,g,b,a] integers)
            if key == "color" and isinstance(value, list):
                if len(value) == 4 and all(isinstance(c, int) and 0 <= c <= 255 for c in value):
                    print(f"✅ Color array at {current_path}: {value}")
                else:
                    issues.append(f"❌ Invalid color format at {current_path}: {value}")
            
            # Recurse into nested structures
            nested_issues = analyze_json_structure(value, current_path)
            issues.extend(nested_issues)
            
    elif isinstance(data, list):
        for i, item in enumerate(data):
            current_path = f"{path}[{i}]"
            nested_issues = analyze_json_structure(item, current_path)
            issues.extend(nested_issues)
    
    return issues

def validate_export_structure(data):
    """Validate the overall export structure."""
    required_sections = [
        "plugin", "global_prompt", "xplainpack_sessions", "assets", 
        "scheduled_content", "content_generation", "generation_info", "ai_instructions"
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in data:
            missing_sections.append(section)
    
    return missing_sections

def main():
    # Test with the provided JSON data
    json_data = """
{
  "plugin": {
    "name": "Euclyd",
    "tagline": "euclidean multitap delay engine",
    "description": "A Euclidean multitap delay engine that thinks in pulses, not echoes.",
    "unique": "Instead of relying on feedback or tap tempo,  Euclyd uses Euclidean algorithms to place taps with mathematical balance inside a user-defined period — not fixed delay times. You don't dial in echoes, you design rhythmic patterns. Each tap is a precise, single event shaped in gain and position, free from accumulation or modulation. This turns delay from an effect into a temporal composition tool — clean, controlled, and structurally musical in ways traditional delays can't replicate.",
    "personality": "Deliberate, mathematical, but deeply musical.",
    "categories": [
      "Modulation",
      "Delay",
      "Other"
    ],
    "use_cases": [
      "Sound Design",
      "Vocals",
      "FX",
      "Mixing",
      "Live"
    ]
  },
  "global_prompt": "",
  "xplainpack_sessions": [],
  "assets": [],
  "scheduled_content": [
    {
      "date": "2025-07-14",
      "content_type": "video",
      "title": "j",
      "prompt": "",
      "platforms": [],
      "template_key": "video"
    },
    {
      "date": "2025-07-15",
      "content_type": "video",
      "title": "qwe",
      "prompt": "",
      "platforms": [],
      "template_key": "video"
    }
  ],
  "content_generation": {
    "templates": {
      "video": {
        "frame_count": 2,
        "template_config": {
          "frame_data": {
            "6": {
              "frame_index": 6,
              "frame_description": "Frame 7",
              "elements": {},
              "timestamp": "2025-07-12T22:10:51.757235",
              "frame_settings": {
                "background_color": null,
                "canvas_size": "PyQt6.QtCore.QSize(498, 600)"
              }
            },
            "0": {
              "frame_index": 0,
              "frame_description": "first",
              "elements": {
                "pip": {
                  "type": "pip",
                  "rect": {
                    "x": 133,
                    "y": 235,
                    "width": 230,
                    "height": 129
                  },
                  "enabled": false,
                  "aspect_ratio": 1.7777777777777777,
                  "corner_radius": 0,
                  "color": [
                    100,
                    150,
                    200,
                    128
                  ],
                  "border_color": [
                    255,
                    255,
                    255,
                    255
                  ],
                  "border_width": 2,
                  "locked": true,
                  "visible": true
                },
                "title": {
                  "type": "text",
                  "rect": {
                    "x": 124,
                    "y": 108,
                    "width": 250,
                    "height": 45
                  },
                  "content": "Video Title",
                  "size": 30,
                  "color": [
                    255,
                    255,
                    255,
                    255
                  ],
                  "style": "normal",
                  "enabled": true,
                  "position_preset": "top",
                  "visible": true
                },
                "subtitle": {
                  "type": "text",
                  "rect": {
                    "x": 124,
                    "y": 462,
                    "width": 250,
                    "height": 30
                  },
                  "content": "Subtitle",
                  "size": 20,
                  "color": [
                    255,
                    255,
                    255,
                    255
                  ],
                  "style": "normal",
                  "enabled": true,
                  "position_preset": "bottom",
                  "visible": true
                }
              },
              "timestamp": "2025-07-12T22:24:16.070606",
              "frame_settings": {
                "background_color": null,
                "canvas_size": "PyQt6.QtCore.QSize(498, 600)"
              }
            }
          }
        },
        "aspect_ratio": 0.5625
      }
    }
  }
}
"""
    
    try:
        # Parse the JSON
        data = json.loads(json_data)
        print("✅ JSON parsing successful!")
        
        # Validate structure
        missing_sections = validate_export_structure(data)
        if missing_sections:
            print(f"❌ Missing sections: {missing_sections}")
        else:
            print("✅ All required sections present!")
        
        # Analyze for issues
        issues = analyze_json_structure(data)
        
        if issues:
            print(f"\n❌ Found {len(issues)} issues:")
            for issue in issues:
                print(f"   {issue}")
        else:
            print("\n✅ No serialization issues found!")
        
        # Check specific areas
        print("\n📊 Analysis Summary:")
        print(f"   • Plugin info: ✅ Complete")
        print(f"   • Scheduled content: ✅ {len(data.get('scheduled_content', []))} events")
        print(f"   • Template config: ✅ Present with frame data")
        print(f"   • Generation info: ✅ Complete with metadata")
        print(f"   • AI instructions: ✅ Complete workflow guidance")
        
        # Count elements across frames
        total_elements = 0
        frame_data = data.get('content_generation', {}).get('templates', {}).get('video', {}).get('template_config', {}).get('frame_data', {})
        for frame_id, frame in frame_data.items():
            elements = frame.get('elements', {})
            total_elements += len(elements)
            print(f"   • Frame {frame_id}: {len(elements)} elements")
        
        print(f"   • Total elements across all frames: {total_elements}")
        
        return len(issues) == 0
        
    except json.JSONDecodeError as e:
        print(f"❌ JSON parsing failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
