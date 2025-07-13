# ReelTune

**Professional Audio Plugin Content Creation & Planning Tool**

ReelTune is a modern PyQt6-based desktop application designed specifically for audio plugin developers and content creators. Built around intelligent .adsp plugin metadata integration, it streamlines the creation of professional marketing content for audio plugins with AI-ready data extraction and content planning workflows.

## 🚀 Core Features

### 🎛️ Plugin-Centric Design
- **Native .adsp Import**: Direct integration with Artista plugin metadata files
- **Parameter Intelligence**: Automatic extraction of key parameters, descriptions, and technical specs
- **Visual Branding**: Plugin highlight colors and visual identity integration
- **Metadata-Driven Content**: All content generation based on authentic plugin data

### 📅 Professional Content Planning
- **Timeline Canvas**: Interactive calendar-based content scheduling and management
- **Multi-Format Support**: Reels, Stories, Posts, Tutorials, and Teasers optimized for plugin content
- **Event-Based Templates**: Per-event template configuration with complete frame independence
- **Visual Planning**: Color-coded content types with comprehensive event details

### 🎨 Advanced Template Editor
- **Frame-Based Video Editing**: Independent frame management for video content with isolated element states
- **Interactive Canvas**: Real-time element manipulation with professional positioning tools
- **Parameter Showcase**: Template system designed specifically for audio plugin interface presentation
- **AI Export Ready**: Template data optimized for AI content generation workflows

### � Asset & Project Management
- **Smart Asset Organization**: Automatic categorization with thumbnail previews and type detection
- **Project Persistence**: JSON-based `.rforge` files with complete project state preservation
- **Professional Workflow**: Recent projects, dark theme UI, and intuitive navigation

## 🎯 Plugin-Focused AI Generation

ReelTune's AI content generation is built specifically for audio plugins:

### From .adsp Metadata
- **Parameter Documentation**: Automatic extraction of parameter names, descriptions, and importance rankings
- **Technical Specifications**: Plugin capabilities, input types, and compatibility information
- **Marketing Content**: Unique selling points, problem-solution narratives, and personality traits
- **Visual Identity**: Brand colors, component layouts, and interface design elements

### Content Type Optimization
- **Reel (15-30s)**: Interface showcase with parameter interaction and sound transformation
- **Story (15s)**: Quick feature highlights with strong visual appeal and branding
- **Post (Static/Loop)**: Clean interface presentation with professional parameter comparison
- **Tutorial (60-300s)**: Detailed parameter walkthrough with practical examples
- **Teaser (10-15s)**: Anticipation-building capability preview with mystery elements

### Smart Prompt Generation
```python
# Example AI prompt structure from .adsp metadata:
Create reel content for Euclyd: euclidean multitap delay engine
Core message: A Euclidean multitap delay engine that thinks in pulses, not echoes
Unique selling point: Uses Euclidean algorithms to place taps with mathematical balance
Showcase key parameters:
  • period: Sets the total duration of the cycle, in bars or milliseconds
  • steps: Defines how many time divisions make up one full cycle  
  • fills: Sets how many taps are placed within the cycle
Format: 1080x1920 (vertical) - 15-30s
Focus: Interface showcase with parameter interaction
Style: Dynamic, engaging, show sound transformation
Personality: Deliberate, mathematical, but deeply musical
```

## 🛠️ Technical Architecture

### Core Modules
- **`core/project.py`** - Enhanced project management with asset import, timeline integration, and structured logging
- **`core/assets.py`** - Asset management and file operations
- **`core/plugins.py`** - Plugin management and .adsp file handling
- **`core/logging_config.py`** - Centralized logging configuration
- **`core/utils.py`** - Utility functions and helpers

### UI Components
- **`ui/mainwindow.py`** - Main application with timeline integration and delayed event updates
- **`ui/enhanced_asset_panel.py`** - Professional asset panel with thumbnails and categorization
- **`ui/timeline/canvas.py`** - Timeline rendering and event management
- **`ui/timeline/controls.py`** - Timeline controls (duration fixed to 4 weeks)
- **`ui/template_editor/editor.py`** - Main template editor with canvas, controls, and frame timeline integration
- **`ui/template_editor/canvas.py`** - Interactive template canvas with element manipulation and frame state management
- **`ui/template_editor/frame_timeline.py`** - Frame timeline for video content types with independent frame management
- **`ui/template_editor/controls.py`** - Template controls panel for element properties and content type switching
- **`ui/startup_dialog.py`** - Project creation/opening dialog
- **`ui/menu.py`** - Menu bar management
- **`ui/style_utils.py`** - Dark theme styling

### Test Suite
- **`tests/`** - Comprehensive test suite for all core functionality
  - Timeline and event management tests
  - Asset import and categorization tests
  - Project loading and navigation tests
  - UI integration tests
- **`tests/run_tests.py`** - Test runner for automated validation

### Design Patterns
- **Modular Architecture** - Clean separation of concerns
- **Signal-Slot Pattern** - Loose coupling between components
- **JSON Serialization** - Human-readable project files
- **Path Management** - Robust file path handling

## 📋 Requirements

- **Python 3.8+**
- **PyQt6** - Modern Qt6 bindings for Python
- **macOS, Windows, or Linux**

## 🚀 Quick Start

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ReelTune
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python main.py
```

### Managing Plugin Information

1. **Import Plugin Data** - Click "Import .adsp" in the Plugin Dashboard
2. **Select .adsp File** - Choose your Artista plugin file (.adsp format)
3. **View Plugin Details**:
   - **Basic Info**: Name, version, categories, use cases
   - **Marketing**: Descriptions, unique selling points, problem solved
   - **Technical**: Specifications, parameters, capabilities
   - **AI Prompts**: Generated content prompts for different social media types
4. **Content Generation Preparation**:
   - All plugin data is structured for AI content generation
   - Prompts are customized based on plugin characteristics
   - Visual branding elements are preserved
   - Marketing content is ready for social media

### Creating Your First Timeline

1. **Launch ReelTune** - The startup dialog will appear
2. **Create or open a project** - Timeline automatically initializes
3. **Navigate the Timeline Canvas**:
   - Use duration controls to view 1-4 weeks
   - Click Previous/Next to navigate through time periods
   - Click "Today" to jump to current week
4. **Schedule Content**:
   - Double-click any day to open event creation dialog
   - Select content type (Reel, Story, Post, Teaser, Tutorial)
   - Add title, description, and hashtags
   - Link project assets to the event
   - Choose target platforms
   - Set status (Planned, Ready, Published)
5. **Visual Feedback**:
   - See color-coded indicators for scheduled content
   - Today is highlighted with blue accent
   - Weekends have darker styling

### Creating Your First Project

1. **Launch ReelTune** - The startup dialog will appear
2. **Choose "Create New Project"** in the right panel
3. **Enter project details**:
   - Name: Your project name
   - Description: Optional project description
   - Location: Where to save the project
4. **Select a template** from the dropdown
5. **Click "Create Project"**

### Importing Assets

- **Via Button**: Click "Import Assets..." in the Assets panel
- **Via Drag & Drop**: Drag files directly into the Assets panel
- **Supported Formats**: 
  - Video: `.mp4`, `.mov`, `.avi`, `.mkv`, `.webm`
  - Audio: `.mp3`, `.wav`, `.aac`, `.m4a`, `.flac`
  - Images: `.jpg`, `.png`, `.gif`, `.bmp`, `.webp`

## 📁 Project Structure

```
ReelTune/
├── core/                    # Core business logic
│   ├── __init__.py
│   ├── project.py          # Project management & timeline
│   ├── assets.py           # Asset handling
│   ├── plugins.py          # Plugin management & .adsp import
│   └── utils.py            # Utilities
├── ui/                     # User interface
│   ├── __init__.py
│   ├── mainwindow.py       # Main window
│   ├── startup_dialog.py   # Startup dialog
│   ├── plugin_dashboard.py # Plugin information dashboard
│   ├── timeline/           # Timeline components
│   │   ├── canvas.py       # Timeline canvas
│   │   ├── controls.py     # Timeline controls
│   │   └── event_dialog.py # Event scheduling dialog
│   ├── menu.py             # Menu management
│   └── style_utils.py      # Dark theme
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
├── test_timeline.py        # Timeline tests
├── test_plugins.py         # Plugin tests
└── README.md              # This file
```

## 🎨 UI Design Philosophy

### Color Scheme (VS Code Inspired)
- **Primary Background**: `#1e1e1e`
- **Secondary Background**: `#252526`
- **Accent Blue**: `#007acc`
- **Text Primary**: `#cccccc`
- **Border Colors**: `#464647` / `#3c3c3c`

### Layout Principles
- **Three-panel layout**: Assets | Timeline/Canvas | Plugin Dashboard
- **Consistent spacing**: 5px, 10px, 20px grid system
- **Professional typography**: System fonts with proper weights
- **Intuitive navigation**: Standard keyboard shortcuts

## 🔧 Configuration

### Project Files (.rforge)
Projects are saved as JSON files with the `.rforge` extension:

```json
{
  "metadata": {
    "name": "My Project",
    "description": "Project description",
    "format": "1920x1080",
    "fps": 30,
    "created_date": "2025-01-01T12:00:00",
    "version": "1.0"
  },
  "assets": {
    "asset_id": {
      "name": "video.mp4",
      "file_path": "assets/video.mp4",
      "file_type": "video",
      "file_size": 1048576
    }
  }
}
```

### Settings Location
- **macOS**: `~/Library/Application Support/ReelTune/`
- **Windows**: `%APPDATA%/ReelTune/`
- **Linux**: `~/.config/ReelTune/`

## 👥 Development Setup

### For New Contributors

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd ReelTune
   ```

2. **Run the setup script** (recommended):
   ```bash
   ./setup.sh
   ```
   This will:
   - Create a virtual environment
   - Install dependencies
   - Set up git hooks to prevent committing generated files
   - Clean up any existing artifacts

3. **Or manually set up**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   source .venv/bin/activate
   python main.py
   ```

### VS Code Development

This project includes VS Code tasks for easy development:

- **Cmd+Shift+P** → "Tasks: Run Task" → Choose:
  - `Run ReelTune` - Launch the application
  - `Run ReelTune (Debug)` - Launch with debug output
  - `Clean Generated Files` - Remove __pycache__ and temp files
  - `Setup Project (Full)` - Complete environment setup

### Important: Preventing Git Issues

The repository includes comprehensive `.gitignore` and git hooks to prevent committing:

- 🚫 **Generated files**: `__pycache__/`, `*.pyc`, `*.log`
- 🚫 **Project files**: `*.rforge`, `*.rtune` (user-specific)
- 🚫 **Temporary data**: `temp_*`, cache files, thumbnails
- 🚫 **IDE files**: `.vscode/settings.json`, `.idea/`

**If you're experiencing thousands of commits from generated files:**

1. Run the cleanup command:
   ```bash
   find . -name "__pycache__" -type d -exec rm -rf {} +
   find . -name "*.pyc" -delete
   ```

2. Remove from git tracking:
   ```bash
   git rm -r --cached __pycache__
   git rm --cached *.pyc *.log
   ```

3. Use the setup script for future clones to avoid this issue.

## 🚧 Roadmap

### Phase 1: Foundation ✅
- [x] Project management system
- [x] Asset import and organization
- [x] Dark theme UI
- [x] Basic file operations

### Phase 2: Timeline & Planning ✅
- [x] Timeline Canvas with calendar grid
- [x] Event scheduling and management
- [x] Content type planning
- [x] Multi-week navigation

### Phase 3: Plugin Integration ✅
- [x] .adsp file import from Artista
- [x] Plugin information dashboard
- [x] AI content preparation
- [x] Marketing data extraction

### Phase 4: Content Generation (Next)
- [ ] AI integration for content generation
- [ ] Automated video/image creation
- [ ] Social media post generation
- [ ] Content export and publishing

### Phase 5: Advanced Features
- [ ] Batch content generation
- [ ] Template management
- [ ] Analytics and performance tracking
- [ ] Collaboration features

## 🧪 Testing

To test the application:

```bash
# Run the application
python main.py

# Test core functionality
python test_core.py

# Test timeline features
python test_timeline.py

# Test plugin functionality
python test_plugins.py

# Complete workflow test:
1. Create a new project
2. Import some media files
3. Import a plugin (.adsp file)
4. Schedule content in timeline
5. Save the project
6. Close and reopen to verify persistence
```

## 🤝 Contributing

This is the foundation for a larger content creation tool. Key areas for contribution:

1. **AI Content Generation** - Integration with AI services for automated content creation
2. **Social Media APIs** - Direct publishing to Instagram, TikTok, YouTube
3. **Template System** - Pre-built content templates and layouts
4. **Analytics Integration** - Content performance tracking and optimization
5. **Collaboration Features** - Multi-user project management

## 📝 License

Copyright © 2025 Artists in DSP. All rights reserved.

---

**Built with ❤️ and PyQt6**