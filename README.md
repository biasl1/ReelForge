# ReelForge

**Professional Content Creation Tool**

ReelForge is a modern PyQt6-based desktop application designed for creating and managing social media content projects. Built with a clean, extensible architecture and featuring a VS Code-inspired dark theme.

## 🚀 Features

### Core Foundation (MVP)
- **Project Management**: Create, save, and load projects with JSON-based `.rforge` files
- **Asset Management**: Import and organize media files (video, audio, images)
- **Professional UI**: VS Code-inspired dark theme with intuitive layout
- **Recent Projects**: Quick access to recently opened projects
- **Drag & Drop**: Easy asset import via drag and drop
- **File Browser**: Organized asset tree with type categorization

### Project Templates
- **Social Media - Square** (1080x1080) - Instagram posts
- **Social Media - Vertical** (1080x1920) - TikTok, Reels, Shorts
- **YouTube - Landscape** (1920x1080) - Standard YouTube
- **Custom** - User-defined dimensions

## 🛠️ Technical Architecture

### Core Modules
- **`core/project.py`** - Project data models and management
- **`core/assets.py`** - Asset management and file operations
- **`core/utils.py`** - Utility functions and helpers

### UI Components
- **`ui/mainwindow.py`** - Main application window
- **`ui/startup_dialog.py`** - Project creation/opening dialog
- **`ui/menu.py`** - Menu bar management
- **`ui/style_utils.py`** - Dark theme styling

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
│   ├── project.py          # Project management
│   ├── assets.py           # Asset handling
│   └── utils.py            # Utilities
├── ui/                     # User interface
│   ├── __init__.py
│   ├── mainwindow.py       # Main window
│   ├── startup_dialog.py   # Startup dialog
│   ├── menu.py             # Menu management
│   └── style_utils.py      # Dark theme
├── main.py                 # Application entry point
├── requirements.txt        # Dependencies
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
- **Three-panel layout**: Assets | Timeline/Canvas | Properties
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

### Phase 2: Timeline (Next)
- [ ] Timeline interface
- [ ] Asset arrangement
- [ ] Basic editing operations
- [ ] Preview functionality

### Phase 3: Effects & Export
- [ ] Transitions and effects
- [ ] Text overlays
- [ ] Export functionality
- [ ] Render queue

### Phase 4: Advanced Features
- [ ] Audio mixing
- [ ] Color correction
- [ ] Plugin system
- [ ] Collaboration features

## 🧪 Testing

To test the application:

```bash
# Run the application
python main.py

# Test project creation
1. Create a new project
2. Import some media files
3. Save the project
4. Close and reopen to verify persistence
```

## 🤝 Contributing

This is the foundation for a larger content creation tool. Key areas for contribution:

1. **Timeline Implementation** - Core editing interface
2. **Media Processing** - Video/audio handling with FFmpeg
3. **Export System** - Multiple format support
4. **Plugin Architecture** - Extensible effects system

## 📝 License

Copyright © 2025 Artists in DSP. All rights reserved.

---

**Built with ❤️ and PyQt6**