# AI Export Format Documentation

## Overview
This document describes the JSON format used when exporting project data for AI content generation tools.

## Data Structure

### Plugin Information
```json
{
  "plugin": {
    "name": "Plugin Name",
    "tagline": "Brief description",
    "description": "Detailed description of the plugin",
    "unique": "What makes this plugin unique",
    "personality": "Plugin's brand personality",
    "categories": ["Category1", "Category2"],
    "use_cases": ["UseCase1", "UseCase2"]
  }
}
```

### Global Configuration
```json
{
  "global_prompt": "Global brand voice and style instructions",
  "moodboard_path": "/path/to/moodboard/file.jpg",
  "project_info": {
    "name": "project_name",
    "format": "1080x1080"
  }
}
```

### Assets
```json
{
  "assets": [
    {
      "id": "unique_asset_id",
      "name": "Asset Name",
      "type": "image|video|audio",
      "path": "/full/path/to/asset"
    }
  ]
}
```

### Scheduled Content
```json
{
  "scheduled_content": [
    {
      "date": "YYYY-MM-DD",
      "content_type": "reel|story|post|teaser|tutorial|yt_short",
      "title": "Content Title",
      "prompt": "AI generation prompt",
      "platforms": ["instagram", "tiktok", "youtube"],
      "template_key": "instagram_reel|instagram_story|youtube_tutorial|etc"
    }
  ]
}
```

### Content Generation Templates
```json
{
  "content_generation": {
    "templates": {
      "instagram_reel": {
        "name": "Instagram Reel",
        "content_type": "reel",
        "platform": "instagram",
        "subtitle_options": {
          "position": {
            "value": "bottom",
            "mode": "fixed|guided|free",
            "constraints": null,
            "description": "Position description"
          },
          "font_size": {
            "value": 24,
            "mode": "guided",
            "constraints": {"min": 20, "max": 30},
            "description": "Readable font size"
          },
          "color": {
            "value": "#FFFFFF",
            "mode": "fixed",
            "constraints": null,
            "description": "Brand white color"
          }
        },
        "overlay_options": {
          "corner_radius": {
            "value": 15,
            "mode": "fixed",
            "constraints": null,
            "description": "Brand corner radius"
          },
          "opacity": {
            "value": 0.8,
            "mode": "guided",
            "constraints": {"min": 0.6, "max": 1.0},
            "description": "Semi-transparent overlay"
          }
        },
        "timing_options": {
          "duration": {
            "value": "15-30s",
            "mode": "guided",
            "constraints": {"min": "15s", "max": "30s"},
            "description": "Instagram reel duration"
          },
          "intro_duration": {
            "value": "2s",
            "mode": "fixed",
            "constraints": null,
            "description": "Fixed intro length"
          }
        },
        "custom_settings": {}
      }
    }
  }
}
```

### Generation Metadata
```json
{
  "generation_info": {
    "export_date": "ISO timestamp",
    "project_name": "project_name",
    "version": "1.3.0",
    "format": "1080x1080",
    "total_assets": 1,
    "total_events": 3,
    "has_global_prompt": false,
    "has_moodboard": false
  }
}
```

### AI Instructions
```json
{
  "ai_instructions": {
    "content_generation_workflow": [
      "1. Use plugin info to understand the product and its unique features",
      "2. Apply global_prompt for consistent brand voice and style",
      "3. Use moodboard for visual style guidance (if provided)",
      "4. Select appropriate assets from the assets list for each content piece",
      "5. Generate content based on each scheduled_content item's prompt",
      "6. Use template_key to match content with appropriate template settings",
      "7. Ensure platform-specific optimization for each target platform"
    ],
    "content_requirements": {
      "reel": "15-60 seconds, vertical 9:16, engaging hook in first 3 seconds",
      "story": "15 seconds max, vertical 9:16, quick and engaging",
      "post": "Static or short video, square 1:1, informative and branded",
      "teaser": "10-15 seconds, any format, mysterious/exciting",
      "tutorial": "60-300 seconds, landscape 16:9, educational and clear",
      "yt_short": "15-60 seconds, vertical 9:16, optimized for YouTube"
    },
    "asset_selection_guidance": [
      "Choose assets that best demonstrate the prompt requirements",
      "Prefer audio assets for showcasing plugin sound",
      "Use video assets for UI demonstrations",
      "Combine multiple assets when needed for comprehensive content"
    ],
    "template_usage": [
      "Use template settings to determine visual style constraints",
      "FIXED mode parameters must be used exactly as specified",
      "GUIDED mode parameters should stay within given constraints",
      "FREE mode parameters can be chosen by AI",
      "Event-specific templates override content-type templates",
      "Project-wide templates provide base settings for all content"
    ]
  }
}
```

## Template Parameter Modes

Each template parameter has a `mode` that determines how AI should handle it:

### Fixed Mode (`"fixed"`)
- **Usage**: `"mode": "fixed"`
- **Behavior**: AI must use the exact value specified
- **Example**: Brand colors, required text positions, fixed durations

### Guided Mode (`"guided"`)
- **Usage**: `"mode": "guided"`
- **Behavior**: AI chooses within specified constraints
- **Constraints**: `{"min": value, "max": value}` or `{"options": [...]}`
- **Example**: Font sizes within readable range, durations within platform limits

### Free Mode (`"free"`)
- **Usage**: `"mode": "free"`
- **Behavior**: AI has complete creative freedom
- **Example**: Creative transitions, optional overlays, dynamic text styling

## Content Type Consistency

### Calendar → Template Mapping
- `"reel"` → `"instagram_reel"`
- `"story"` → `"instagram_story"`
- `"post"` → `"instagram_post"`
- `"tutorial"` → `"youtube_tutorial"`
- `"teaser"` → `"instagram_teaser"`
- `"yt_short"` → `"youtube_short"`

### Template Keys
Each scheduled content item includes a `template_key` that maps to the appropriate template in the `content_generation.templates` object.

## Usage

This format is designed to provide AI content generation tools with comprehensive context about:

1. **Plugin Identity**: What the plugin is and what makes it unique
2. **Brand Voice**: Global prompts and moodboard for consistent styling
3. **Available Assets**: All media files available for content creation
4. **Content Schedule**: What content to create, when, and for which platforms
5. **Template System**: Detailed visual and timing constraints for each content type
6. **Generation Guidelines**: Specific requirements and workflows for AI tools

## Template System Integration

The template system provides three levels of control:

1. **Project-wide templates**: Base settings applied to all content
2. **Content-type templates**: Specific settings for reels, stories, etc.
3. **Event-specific templates**: Override settings for individual pieces

AI tools should:
1. Start with project-wide template settings
2. Apply content-type template settings (using `template_key`)
3. Override with event-specific settings if available
4. Respect parameter modes (fixed/guided/free)
5. Stay within constraints for guided parameters

## Content Types

- **reel**: Short vertical videos (15-60 seconds) for Instagram/TikTok
- **story**: Very short vertical content (15 seconds max) for Instagram Stories
- **post**: Square format content for social media posts
- **teaser**: Short preview content to build anticipation
- **tutorial**: Longer educational content explaining plugin features

## Platform Specifications

- **Instagram**: Vertical 9:16 for reels/stories, square 1:1 for posts
- **TikTok**: Vertical 9:16 format
- **YouTube**: Landscape 16:9 for tutorials, vertical 9:16 for shorts

## Integration

AI tools should:
1. Parse the plugin information to understand the product
2. Apply the global prompt for consistent brand voice
3. Use the moodboard (if available) for visual style guidance
4. Select appropriate assets from the assets list
5. Generate content according to the scheduled content prompts
6. Use the template_key to find the appropriate template settings
7. Follow template parameter modes (fixed/guided/free)
8. Respect constraints for guided parameters
9. Follow platform-specific requirements for format and duration
10. Use the content_generation_workflow for proper sequencing

## Example Workflow

```python
# 1. Load export data
data = load_ai_export_data()

# 2. For each scheduled content item
for content in data["scheduled_content"]:
    # 3. Get template settings
    template_key = content["template_key"]
    template = data["content_generation"]["templates"][template_key]
    
    # 4. Process template parameters
    settings = process_template_parameters(template)
    
    # 5. Generate content with constraints
    generated_content = generate_content(
        prompt=content["prompt"],
        assets=data["assets"],
        settings=settings,
        plugin_info=data["plugin"]
    )
```
