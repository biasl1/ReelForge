# ReelTune

**Professional AI-Ready Social Media Content Planning Tool**

ReelTune is a modern PyQt6-based desktop application designed for professional content creators and audio plugin developers. Originally ReelForge, it has been transformed into a comprehensive content planning and management system with AI integration capabilities, timeline scheduling, and enhanced asset management.

## 🚀 Features

### Core Foundation
- **Project Management**: Create, save, and load projects with JSON-based `.rforge` files
- **Enhanced Asset Panel**: Professional asset management with thumbnails, categorization, and import
- **Professional UI**: Dark theme with responsive design and intuitive workflow
- **Recent Projects**: Quick access to recently opened projects
- **AI-Ready Structure**: Comprehensive project data for AI content generation

### 🎯 Timeline & Event Management
- **Interactive Timeline Canvas**: Professional calendar-based content planning
- **Event Scheduling**: Create, edit, and delete content events with visual feedback
- **Duration Control**: Flexible 1-4 week timeline views with seamless transitions
- **Visual Event Display**: Color-coded content types with comprehensive event details
- **Timeline Navigation**: Smooth previous/next navigation with date controls
- **Event Persistence**: Reliable save/load with proper event-timeline synchronization

### 🖼️ Enhanced Asset Management
- **Visual Asset Panel**: Thumbnail previews for images, video previews, and professional icons
- **Smart Categorization**: Automatic grouping by Images, Videos, Audio, and Other files
- **Asset Import**: Drag-and-drop and button-based import with file type detection
- **Professional Design**: Responsive grid layout with category headers and modern styling
- **Asset Integration**: Link assets to timeline events for complete content planning

### 🔌 Plugin Integration
- **Artista .adsp Import**: Import plugin metadata from Artista plugin files
- **Plugin Information Dashboard**: Complete plugin details and management
- **AI Content Preparation**: Structured data for AI content generation
- **Marketing Content**: Extract descriptions, features, and selling points
- **Technical Specifications**: Plugin parameters, categories, and capabilities

## 🛠️ Technical Architecture

# ReelTune

**Professional AI-Ready Social Media Content Planning Tool**

ReelTune is a modern PyQt6-based desktop application designed for professional content creators and audio plugin developers. Originally ReelForge, it has been transformed into a comprehensive content planning and management system with AI integration capabilities, timeline scheduling, and enhanced asset management.

## 🚀 Features

### Core Foundation
- **Project Management**: Create, save, and load projects with JSON-based `.rforge` files
- **Enhanced Asset Panel**: Professional asset management with thumbnails, categorization, and import
- **Professional UI**: Dark theme with responsive design and intuitive workflow
- **Recent Projects**: Quick access to recently opened projects
- **AI-Ready Structure**: Comprehensive project data for AI content generation
- **Structured Logging**: Professional logging system replacing print statements for better debugging

### 🎯 Timeline & Event Management
- **Interactive Timeline Canvas**: Professional calendar-based content planning
- **Event Scheduling**: Create, edit, and delete content events with visual feedback
- **Fixed Duration**: Always 4-week timeline for consistent planning (duration selection removed)
- **Visual Event Display**: Color-coded content types with comprehensive event details
- **Timeline Navigation**: Smooth previous/next navigation with date controls
- **Event Persistence**: Reliable save/load with proper event-timeline synchronization
- **Robust Event Management**: Fixed timeline refresh and event deletion/editing bugs

### 🖼️ Enhanced Asset Management
- **Visual Asset Panel**: Thumbnail previews for images, video previews, and professional icons
- **Smart Categorization**: Automatic grouping by Images, Videos, Audio, and Other files
- **Asset Import**: Drag-and-drop and button-based import with file type detection
- **Professional Design**: Responsive grid layout with category headers and modern styling
- **Asset Integration**: Link assets to timeline events for complete content planning

### 🔌 Plugin Integration
- **Artista .adsp Import**: Import plugin metadata from Artista plugin files
- **Plugin Information Dashboard**: Complete plugin details and management
- **AI Content Preparation**: Structured data for AI content generation
- **Marketing Content**: Extract descriptions, features, and selling points
- **Technical Specifications**: Plugin parameters, categories, and capabilities

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

1. **Launch ReelForge** - The startup dialog will appear
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

1. **Launch ReelForge** - The startup dialog will appear
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
ReelForge/
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
- **macOS**: `~/Library/Application Support/ReelForge/`
- **Windows**: `%APPDATA%/ReelForge/`
- **Linux**: `~/.config/ReelForge/`

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