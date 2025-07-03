# 🤖 AI JSON Export Guide

## Overview

ReelForge now includes a powerful **AI JSON Export** feature that generates a complete data package for AI content generation. This JSON file contains everything an AI system needs to automatically create professional social media content for your audio plugins.

## 🚀 How to Use

### 1. **Prepare Your Project**
1. **Create/Open Project** in ReelForge
2. **Import Plugin** (.adsp file) via Plugin Dashboard → "Import .adsp File" 
3. **Set Global Prompt** (optional but recommended)
4. **Upload Moodboard** (optional visual style reference)
5. **Import Assets** (audio, video, images)
6. **Schedule Content** on timeline with AI prompts

### 2. **Export AI Data**
1. Go to **Plugin Dashboard** panel
2. Click **"🚀 Generate AI Data JSON"** button
3. Choose export location and filename
4. JSON file is generated with complete AI data package

### 3. **Use with AI Services**
- Feed the JSON to AI services (OpenAI, Claude, etc.)
- AI generates content based on the structured data
- Review and publish generated content

---

## 📋 JSON Structure

The exported JSON contains:

### **Core Data**
```json
{
  "plugin": {
    "name": "Euclyd",
    "description": "Euclidean multitap delay engine", 
    "personality": "Deliberate, mathematical, but deeply musical",
    "categories": ["Delay", "Modulation"],
    "unique": "Mathematical delay placement algorithm..."
  },
  "global_prompt": "Professional, warm tone. Focus on vintage character...",
  "moodboard_path": "moodboard/style_reference.jpg",
  "assets": [
    {"id": "audio_001", "type": "audio", "path": "demo.wav"},
    {"id": "video_001", "type": "video", "path": "plugin_ui.mp4"}
  ],
  "scheduled_content": [
    {
      "date": "2025-07-05",
      "content_type": "reel",
      "prompt": "Show warm saturation on guitar melody...",
      "platforms": ["instagram", "tiktok"]
    }
  ]
}
```

### **AI Instructions**
- **Content generation workflow** - Step-by-step process
- **Content requirements** - Technical specs per content type
- **Asset selection guidance** - How to choose appropriate media

### **Generation Metadata**
- Export date, project info, data summary
- Validation flags for completeness checking

---

## 🎯 Content Types & Requirements

### **Reels** (15-60 seconds, 9:16 vertical)
- Engaging hook in first 3 seconds
- High energy, quick cuts
- Perfect for plugin demos and reactions

### **Stories** (15 seconds max, 9:16 vertical) 
- Quick tips and behind-the-scenes
- Simple, focused message
- Casual, authentic feel

### **Posts** (Static/short video, 1:1 square)
- Product showcases and infographics
- Clean, branded visuals
- Educational content

### **Tutorials** (60-300 seconds, 16:9 landscape)
- Detailed explanations and walkthroughs
- Multiple examples and techniques
- Professional, educational tone

### **Teasers** (10-15 seconds, any format)
- Coming soon announcements
- Mystery/intrigue building
- Quick sound previews

---

## 🤖 AI Integration Examples

### **OpenAI Integration**
```python
import openai
import json

# Load ReelForge AI data
with open('project_ai_data.json') as f:
    ai_data = json.load(f)

# Generate video script
prompt = f"""
Plugin: {ai_data['plugin']['name']}
Global Style: {ai_data['global_prompt']}
Content: {ai_data['scheduled_content'][0]['prompt']}

Generate a 30-second video script for Instagram Reel.
"""

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[{"role": "user", "content": prompt}]
)

script = response.choices[0].message.content
```

### **Content Generation Workflow**
1. **Script Generation** - AI writes video scripts based on prompts
2. **Visual Planning** - AI selects assets and plans shots  
3. **Audio Processing** - AI processes plugin audio demos
4. **Video Assembly** - AI generates edited video content
5. **Platform Optimization** - AI adapts content for each platform

---

## 💡 Pro Tips

### **Better Prompts = Better Content**
- Be specific about desired outcomes
- Include technical details for tutorials
- Mention emotions and reactions for demos
- Specify visual elements and style preferences

### **Global Prompt Strategy**
- Define your brand voice consistently
- Include color preferences and visual style
- Mention target audience and tone
- Specify any brand guidelines or restrictions

### **Asset Organization**
- Include variety: UI footage, audio demos, behind-the-scenes
- Name files descriptively for AI selection
- Ensure high quality source material
- Consider different plugin states and settings

### **Timeline Planning**
- Space content releases appropriately  
- Consider content dependencies and themes
- Plan for different content types and platforms
- Allow time for AI generation and review

---

## 🔧 Technical Details

### **File Format**
- **UTF-8 encoded JSON** with pretty formatting
- **Cross-platform compatible** paths and data
- **Version tracked** for future compatibility
- **Validation metadata** for completeness checking

### **Data Validation**
The export process validates:
- ✅ Plugin information imported
- ✅ At least one scheduled event
- ✅ All event prompts are non-empty
- ✅ Valid content types and platforms
- ✅ Project structure integrity

### **Error Handling**
- **Missing plugin** - Warning with option to continue
- **No scheduled content** - Confirmation dialog
- **Export failures** - Detailed error messages
- **File access issues** - Alternative save locations

---

## 🚀 Future Enhancements

### **Planned Features**
- **Direct AI service integration** - One-click generation
- **Content preview system** - Review before publishing
- **Batch processing** - Generate multiple pieces simultaneously
- **Social media APIs** - Direct platform publishing
- **Analytics integration** - Performance-based optimization

### **AI Service Connectors**
- OpenAI GPT-4 for script generation
- Midjourney for visual content creation  
- ElevenLabs for voiceovers and narration
- RunwayML for video generation and editing

---

## 📞 Support

For questions about AI JSON export:
1. Check the validation messages in the export dialog
2. Review the generated JSON structure
3. Test with sample data using `demo_ai_export.py`
4. Verify all required project data is present

**Happy AI content generation!** 🎬✨
