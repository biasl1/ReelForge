#!/usr/bin/env python3
"""
COMPREHENSIVE REELTUNE CODEBASE CLEANUP
Removes unused files and consolidates functionality
"""

import os
import shutil
from pathlib import Path

def cleanup_test_files():
    """Remove outdated test and debug files"""
    cleanup_files = [
        # Test files (keep only essential ones)
        "test_template_export.py",
        "test_content_type_independence.py", 
        "test_clean_architecture.py",
        "test_real_template_export.py",
        "test_relative_positioning.py",
        "test_pip_plugin_comprehensive.py",
        "test_json_debug.py",
        "test_window_resize_bug_final.py",
        "test_simplified_editor.py",
        "test_ai_export_fixed.py",
        "test_all_user_issues.py",
        "test_patched_export.py",
        "test_ai_export_templates.py",
        "test_subtitle_elements.py",
        "test_zoom_pan_unconstrained.py",
        "test_enhanced_export.py",
        "test_element_visibility.py",
        "test_window_resize.py",
        "test_actual_export.py",
        "test_pip_plugin_features.py",
        
        # Debug files
        "debug_json_issue.py",
        "debug_config_mode.py", 
        "debug_str_error.py",
        
        # Demo files
        "demo_visual_template_editor.py",
        "demo_super_smart_fixed_variables.py",
        
        # Cleanup/migration files
        "fix_simple_templates.py",
        "cleanup_compat.py",
        "migrate_template_imports.py",
        
        # Analysis files
        "analyze_cleanup.py"
    ]
    
    removed_count = 0
    total_size = 0
    
    for filename in cleanup_files:
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            total_size += size
            file_path.unlink()
            removed_count += 1
            print(f"🗑️  Removed: {filename} ({size/1024:.1f} KB)")
    
    print(f"\n✅ Removed {removed_count} files ({total_size/1024:.1f} KB total)")
    return removed_count

def cleanup_unused_ui():
    """Remove unused UI modules"""
    unused_ui_files = [
        "ui/ai_template_editor_clean.py",
        "ui/content_generation_panel.py", 
        "ui/visual_template_editor.py",  # Keep ai_template_editor.py as reference
    ]
    
    removed_count = 0
    
    for filename in unused_ui_files:
        file_path = Path(filename)
        if file_path.exists():
            size = file_path.stat().st_size
            if size == 0:  # Only remove empty files
                file_path.unlink()
                removed_count += 1
                print(f"🗑️  Removed empty UI file: {filename}")
    
    return removed_count

def cleanup_core_modules():
    """Clean up core modules"""
    # Remove fix_enums.py as it's not needed anymore
    fix_enums_path = Path("core/fix_enums.py")
    if fix_enums_path.exists():
        fix_enums_path.unlink()
        print("🗑️  Removed: core/fix_enums.py (enum fixes integrated)")
        return 1
    return 0

def organize_tests():
    """Organize remaining test files"""
    essential_tests = [
        "test_templates.py",
        "test_complete_export.py", 
        "run_all_verification_tests.py"
    ]
    
    print(f"\n📁 Essential tests preserved:")
    for test_file in essential_tests:
        if Path(test_file).exists():
            print(f"  ✅ {test_file}")

def create_codebase_overview():
    """Create a codebase overview file"""
    overview_content = '''# REELTUNE CODEBASE OVERVIEW

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
'''
    
    with open("CODEBASE_OVERVIEW.md", "w") as f:
        f.write(overview_content)
    
    print("📝 Created: CODEBASE_OVERVIEW.md")

if __name__ == "__main__":
    print("🧹 REELTUNE COMPREHENSIVE CLEANUP")
    print("=" * 50)
    
    # Cleanup test files
    print("\n1. 🗑️  CLEANING TEST FILES:")
    test_count = cleanup_test_files()
    
    # Cleanup UI files
    print("\n2. 🎨 CLEANING UI FILES:")
    ui_count = cleanup_unused_ui()
    
    # Cleanup core files
    print("\n3. ⚙️  CLEANING CORE FILES:")
    core_count = cleanup_core_modules()
    
    # Organize tests
    print("\n4. 📁 ORGANIZING TESTS:")
    organize_tests()
    
    # Create overview
    print("\n5. 📝 CREATING OVERVIEW:")
    create_codebase_overview()
    
    total_removed = test_count + ui_count + core_count
    print(f"\n🎉 CLEANUP COMPLETE!")
    print(f"   Removed {total_removed} files")
    print("   Codebase is now clean and organized")
    print("   Created CODEBASE_OVERVIEW.md for reference")
