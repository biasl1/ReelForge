#!/usr/bin/env python3
"""
Demo script to show AI JSON export functionality
Creates a sample project and generates AI data JSON
"""

import sys
import json
import tempfile
from pathlib import Path
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from core.project import ReelForgeProject, ReleaseEvent


def create_sample_project():
    """Create a sample project with AI-ready data"""
    print("🎬 Creating sample project for AI content generation...")
    
    # Create project
    project = ReelForgeProject()
    project.metadata.name = "Euclyd Plugin Demo"
    project.metadata.description = "Social media content for Euclyd delay plugin"
    
    # Set AI features
    project.global_prompt = """
Professional music production content with a warm, analog aesthetic. 
Focus on the mathematical precision meets musical creativity theme.
Show real studio scenarios and genuine artist reactions.
Use warm color grading and vintage-inspired visuals.
Emphasize the unique euclidean rhythm patterns and their musical applications.
"""
    
    project.moodboard_path = "moodboard/vintage_studio_aesthetic.jpg"
    
    # Initialize timeline
    project.initialize_timeline()
    
    # Add sample events with detailed AI prompts
    events = [
        {
            "date": "2025-07-05",
            "content_type": "reel",
            "title": "Euclidean Magic Demo",
            "description": """
Show a producer discovering the Euclyd plugin for the first time. 
Start with a simple guitar loop, then reveal how Euclyd creates perfect rhythmic delays. 
Focus on the producer's reaction when they hear the euclidean pattern emerge.
Include close-ups of the plugin interface showing the steps/fills parameters.
End with the full musical result showcasing the mathematical beauty.
""",
            "platforms": ["instagram", "tiktok"]
        },
        {
            "date": "2025-07-06", 
            "content_type": "story",
            "title": "Quick Tip",
            "description": """
15-second quick tip: 'The secret to perfect delay patterns? Mathematics!'
Show the Euclyd interface with steps set to 16 and fills to 5.
Quick before/after audio comparison.
End with text overlay: 'Euclidean rhythms = instant musical magic'
""",
            "platforms": ["instagram"]
        },
        {
            "date": "2025-07-07",
            "content_type": "tutorial", 
            "title": "Complete Euclyd Walkthrough",
            "description": """
Full 3-minute tutorial covering:
1. What are euclidean rhythms and why they're musically powerful
2. Loading Euclyd and understanding the interface
3. Setting up steps and fills for different musical effects
4. Using the rotation parameter for variation
5. Practical examples: drums, guitars, synths
6. How to integrate with other effects
Show multiple real-world use cases and producer techniques.
""",
            "platforms": ["youtube"]
        },
        {
            "date": "2025-07-08",
            "content_type": "post",
            "title": "Feature Spotlight",
            "description": """
Static post showcasing the Euclyd plugin interface.
Clean product shot with key features highlighted:
- Euclidean algorithm visualization
- Steps and fills controls
- Rotation parameter
- Clean/musical delay output
Include brief text explaining the mathematical approach to musical delays.
Professional lighting, high contrast, brand colors.
""",
            "platforms": ["instagram", "facebook"]
        }
    ]
    
    # Add events to project
    for event_data in events:
        event = ReleaseEvent(
            id="",
            date=event_data["date"],
            content_type=event_data["content_type"],
            title=event_data["title"],
            description=event_data["description"],
            platforms=event_data["platforms"]
        )
        project.add_release_event(event)
    
    print(f"✅ Created project with {len(project.release_events)} scheduled content events")
    return project


def generate_ai_data_json(project, output_path):
    """Generate AI data JSON file"""
    print("🤖 Generating AI data JSON...")
    
    # Get AI generation data
    ai_data = project.get_ai_generation_data()
    
    # Add metadata and instructions (same as in the UI)
    ai_data["generation_info"] = {
        "export_date": datetime.now().isoformat(),
        "project_name": project.project_name,
        "version": "1.3.0",
        "format": project.metadata.format,
        "total_assets": len(ai_data.get("assets", [])),
        "total_events": len(ai_data.get("scheduled_content", [])),
        "has_global_prompt": bool(ai_data.get("global_prompt")),
        "has_moodboard": bool(ai_data.get("moodboard_path"))
    }
    
    ai_data["ai_instructions"] = {
        "content_generation_workflow": [
            "1. Use plugin info to understand the product and its unique features",
            "2. Apply global_prompt for consistent brand voice and style", 
            "3. Use moodboard for visual style guidance (if provided)",
            "4. Select appropriate assets from the assets list for each content piece",
            "5. Generate content based on each scheduled_content item's prompt",
            "6. Ensure platform-specific optimization for each target platform"
        ],
        "content_requirements": {
            "reel": "15-60 seconds, vertical 9:16, engaging hook in first 3 seconds",
            "story": "15 seconds max, vertical 9:16, quick and engaging", 
            "post": "Static or short video, square 1:1, informative and branded",
            "teaser": "10-15 seconds, any format, mysterious/exciting",
            "tutorial": "60-300 seconds, landscape 16:9, educational and clear"
        },
        "asset_selection_guidance": [
            "Choose assets that best demonstrate the prompt requirements",
            "Prefer audio assets for showcasing plugin sound",
            "Use video assets for UI demonstrations", 
            "Combine multiple assets when needed for comprehensive content"
        ]
    }
    
    # Export JSON
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ai_data, f, indent=2, ensure_ascii=False)
        
    print(f"✅ AI data JSON exported to: {output_path}")
    return ai_data


def analyze_ai_data(ai_data):
    """Analyze and display the AI data structure"""
    print("\n📊 AI Data Analysis:")
    print("=" * 50)
    
    # Plugin info
    plugin = ai_data.get("plugin")
    if plugin:
        print(f"🔌 Plugin: {plugin.get('name', 'Unknown')}")
        print(f"   Personality: {plugin.get('personality', 'Not specified')}")
        print(f"   Categories: {', '.join(plugin.get('categories', []))}")
    else:
        print("🔌 Plugin: None (would need to import .adsp file)")
    
    # Global prompt
    global_prompt = ai_data.get("global_prompt", "")
    print(f"\n🎨 Global Prompt: {len(global_prompt)} characters")
    if global_prompt:
        print(f"   Preview: {global_prompt[:100]}...")
    
    # Moodboard
    moodboard = ai_data.get("moodboard_path")
    print(f"\n🖼️  Moodboard: {'✓ ' + moodboard if moodboard else '✗ None'}")
    
    # Assets
    assets = ai_data.get("assets", [])
    print(f"\n📁 Assets: {len(assets)} available")
    
    # Scheduled content
    content = ai_data.get("scheduled_content", [])
    print(f"\n📅 Scheduled Content: {len(content)} events")
    
    for i, event in enumerate(content, 1):
        print(f"   {i}. {event['content_type'].upper()} - {event['date']}")
        print(f"      Platforms: {', '.join(event['platforms'])}")
        print(f"      Prompt: {len(event['prompt'])} characters")
        
    # Generation info
    gen_info = ai_data.get("generation_info", {})
    print(f"\n📋 Generation Info:")
    print(f"   Project: {gen_info.get('project_name', 'Unknown')}")
    print(f"   Export Date: {gen_info.get('export_date', 'Unknown')}")
    print(f"   Has Global Prompt: {gen_info.get('has_global_prompt', False)}")
    print(f"   Has Moodboard: {gen_info.get('has_moodboard', False)}")


def main():
    """Demo the AI JSON export functionality"""
    print("🚀 ReelForge AI JSON Export Demo\n")
    
    try:
        # Create sample project
        project = create_sample_project()
        
        # Generate AI data JSON
        output_path = Path("ai_generation_data_demo.json")
        ai_data = generate_ai_data_json(project, output_path)
        
        # Analyze the data
        analyze_ai_data(ai_data)
        
        print(f"\n🎉 Demo complete!")
        print(f"\nThe AI JSON file '{output_path}' contains everything needed for content generation:")
        print("  ✓ Plugin information and personality")
        print("  ✓ Global brand prompt for consistency") 
        print("  ✓ Individual event prompts with specific requirements")
        print("  ✓ Platform targeting and format specifications")
        print("  ✓ AI processing instructions and guidelines")
        
        print(f"\n💡 Next steps:")
        print("  1. Use this JSON with AI services (OpenAI, Claude, etc.)")
        print("  2. Generate video scripts, visual concepts, and audio demos") 
        print("  3. Create platform-optimized content automatically")
        print("  4. Return generated content back to ReelForge for review")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
