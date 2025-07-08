# ReelTune Template Editor Codebase Cleanup Plan

## Current Mess (6,500+ lines of duplicated code)

### Files to Delete (Complete Duplicates):
- `ui/ai_template_editor_verbose.py` (2,124 lines) - Bloated duplicate of main editor
- `ui/ai_template_editor_clean.py` (412 lines) - Incomplete stub version
- Demo files with outdated/duplicate implementations

### Files to Keep & Refactor:
- `ui/ai_template_editor.py` (1,699 lines) - **MAIN FILE** - Has all working features
- `ui/content_template_view.py` (533 lines) - Different UI approach, keep as reference
- `ui/visual_template_editor.py` (868 lines) - WYSIWYG layer system, keep as reference

## New Modular Architecture

### Core Modules:
1. **`ui/template_editor/`** - Main template editor package
   - `__init__.py` - Public API exports
   - `editor.py` - Main template editor widget (clean version of current)
   - `canvas.py` - Interactive canvas with zoom/pan/constraints
   - `controls.py` - UI controls and settings panel
   - `persistence.py` - Save/load and state management

2. **`ui/template_editor/components/`** - Reusable UI components
   - `overlay_controls.py` - Text overlay management
   - `pip_controls.py` - Picture-in-picture controls
   - `timeline.py` - Timeline component (if needed)
   - `layers.py` - Layer management (from WYSIWYG versions)

3. **`ui/template_editor/utils/`** - Utilities
   - `coordinates.py` - Coordinate transformation for zoom/pan
   - `constraints.py` - Constraint logic for element placement
   - `dimensions.py` - Content type dimensions and aspect ratios

## Cleanup Process:
1. ✅ Commit current working state
2. Create new modular structure 
3. Extract and refactor main functionality
4. Migrate tests to use new structure
5. Delete duplicate files
6. Update imports across codebase
7. Verify all functionality still works

## Benefits:
- Single source of truth for template editing
- Maintainable, focused modules
- Reusable components
- Clear separation of concerns
- Easier testing and debugging
- No more massive 2000+ line files
