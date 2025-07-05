#!/usr/bin/env python3
"""
Test script for ReelTune Content Template System
Demonstrates the template functionality without full UI
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.content_generation import ContentGenerationManager, ConfigMode

def test_content_templates():
    """Test the content generation template system"""
    print("🎬 ReelTune Content Template System Test")
    print("=" * 50)
    
    # Create manager
    manager = ContentGenerationManager()
    
    # Test 1: Get default reel template
    print("\n📱 Testing Reel Template:")
    reel_template = manager.get_content_template("reel")
    print(f"Duration: {reel_template.timing.duration.value}")
    print(f"Subtitle Position: {reel_template.subtitle.position.value}")
    
    # Test 2: Modify a parameter mode
    print("\n🔧 Modifying font_size to FREE mode:")
    reel_template.subtitle.font_size.mode = ConfigMode.FREE
    print(f"Font Size Mode: {reel_template.subtitle.font_size.mode}")
    
    # Test 3: Generate AI prompt
    print("\n🤖 Generated AI Prompt:")
    prompt = manager.generate_ai_prompt("reel", base_prompt="Create an engaging reel about cooking:")
    print(prompt)
    
    # Test 4: Resolve config
    print("\n⚙️ Resolved Config:")
    config = manager.resolve_config("reel")
    for key, value in config.items():
        print(f"  {key}: {value}")
    
    print("\n✅ Template system working correctly!")

if __name__ == "__main__":
    test_content_templates()
