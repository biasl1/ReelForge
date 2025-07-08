# REELTUNE CODEBASE OVERVIEW

## 🏗️ Core Architecture

### Core Modules (`core/`)
- `project.py` - Project management, save/load, AI export (44.6 KB)
- `content_generation.py` - Content generation templates and AI integration (15.4 KB)
- `plugins.py` - Plugin system and .adsp file handling (9.7 KB)
- `assets.py` - Asset management (8.2 KB)
- `utils.py` - Utility functions (2.9 KB)
- `logging_config.py` - Logging configuration (2.4 KB)

### UI Modules (`ui/`)
- `mainwindow.py` - Main application window
- `plugin_dashboard.py` - Plugin information panel
- `template_editor/` - Visual template editor system
  - `editor.py` - Main template editor widget
  - `canvas.py` - Interactive canvas for template editing
  - `controls.py` - Control panel for element properties
  - `persistence.py` - Template save/load functionality
  - `utils.py` - Template editor utilities
- `enhanced_asset_panel.py` - Asset management UI
- `startup_dialog.py` - Project selection dialog
- `style_utils.py` - UI styling utilities
- `ux_improvements.py` - UX enhancement components (19.1 KB)

### Test System (`tests/`)
- `test_templates.py` - Main template system tests
- `test_complete_export.py` - Comprehensive export verification
- `run_all_verification_tests.py` - Test runner
- `integration/` - Integration tests
- `unit/` - Unit tests
- `demos/` - Demo scripts

## 🎯 Key Features

### 1. Template Editor System
- Visual WYSIWYG editor for content templates
- Support for 4 content types: reel, story, post, tutorial
- Real-time element positioning and styling
- Export to AI-compatible JSON format

### 2. Project Management
- .rforge file format for project persistence
- Asset management with metadata
- Timeline planning with scheduled content
- Plugin integration (.adsp file support)

### 3. AI Export System
- Exports real template data (not hardcoded values)
- Includes pixel-perfect positions, fonts, colors
- Supports multiple content types
- Platform-specific optimization

### 4. Plugin System
- .adsp file parsing and validation
- Plugin metadata extraction
- Content type recommendations
- AI prompt generation

## 🔧 Development Guidelines

### Adding New Features
1. Core logic goes in `core/` modules
2. UI components go in `ui/` modules  
3. Add tests in `tests/` directory
4. Update this overview file

### Template System
- All templates are managed by `TemplateEditor`
- Real UI positions are exported (no hardcoded fallbacks)
- Template settings are saved with projects
- Element types: text, pip, background

### Export System
- Priority: UI template data > ContentGenerationManager > fallback
- Real pixel positions and styling preserved
- Content-type specific dimensions and platforms
- AI-friendly JSON structure

## 📝 Recent Major Changes
- Fixed template export to use real UI data
- Added comprehensive template editor
- Integrated template settings persistence
- Removed 28+ unused test/debug files
- Consolidated UI components
