# ReelTune Copilot Instructions

## Architecture Overview

**ReelTune** is a PyQt6-based content planning tool with a **per-event template system**. The app recently underwent major refactoring from content-type-based to event-based templates.

### Core Architecture Pattern
- **Event-Driven**: Each calendar event (VIDEO/PICTURE) has independent template configuration
- **Frame Independence**: Video events support multiple frames with complete data isolation
- **Signal-Slot Communication**: PyQt6 signals connect UI components without tight coupling
- **JSON Persistence**: `.rforge` files store projects with template configurations per event

### Key Data Flow
```
MainWindow → TemplateEditor → (Canvas, Controls, FrameTimeline)
           → Project → ReleaseEvents → template_config (per event)
```

## Critical Components

### Template Editor System (`ui/template_editor/`)
- **Editor**: Main coordinator widget with event/frame management
- **Canvas**: Interactive element manipulation with rect format conversion
- **Controls**: Property panels that dynamically update based on selected element
- **FrameTimeline**: Frame navigation for video content with add/remove capabilities

### Data Models (`core/project.py`)
- **ReleaseEvent**: Each event has `template_config` dict and `frame_count`
- **Per-event storage**: No global content types - each event is independent
- **Default frame_count**: Videos default to 1 frame (user can add more)

### Rect Format Handling (Critical Pattern)
Elements store `rect` in multiple formats - always use helper methods:
```python
# WRONG: element['rect'].x()  # May be dict, not QRect
# RIGHT: self._get_qrect_from_element(element)
```

## Development Workflows

### Running the App
```bash
# VS Code Task (Cmd+Shift+P → "Tasks: Run Task")
"Run ReelTune"

# Terminal
source .venv/bin/activate && python main.py
```

### Frame Independence Testing
1. Select a video event
2. Add frames using frame timeline
3. Click different frames - each should maintain independent elements
4. Modify elements in one frame - other frames should be unaffected
5. Save/load project - frame data should persist

### Element Property Flow
1. Click element on canvas → `element_selected` signal
2. Editor calls `get_element_data()` and passes to controls
3. Controls show properties based on element type (`text`, `pip`)
4. Property changes emit `element_property_changed` signal
5. Editor updates canvas and saves to current frame

## Project-Specific Patterns

### Element Property Updates
```python
# Controls emit property changes
self.element_property_changed.emit(element_id, 'content', new_text)

# Editor handles updates
def _handle_element_property_change(self, element_id, property_name, value):
    self.canvas.update_element_property(element_id, property_name, value)
```

### Frame Loading Pattern
```python
# Always check for recursion in frame operations
if self._loading_frame:
    return
self._loading_frame = True
try:
    # Frame loading logic
finally:
    self._loading_frame = False
```

### Signal Connection Pattern
All UI components communicate via signals - never direct method calls:
```python
# In TemplateEditor.__init__()
self.controls.event_changed.connect(self.load_event)
self.canvas.element_selected.connect(self._handle_element_selection)
```

## Common Issues & Solutions

### Rect Format Errors
**Problem**: `AttributeError: 'dict' object has no attribute 'x'`
**Solution**: Always use `_ensure_qrect()` or `_get_qrect_from_element()`

### Missing Element Properties
**Problem**: Click element but properties don't show
**Solution**: Ensure `_handle_element_selection()` passes element data to controls

### Frame Count Issues
**Problem**: New events default to wrong frame count
**Solution**: Check `ReleaseEvent.__post_init__()` - videos should default to 1 frame

## Testing Strategy

### Manual Testing Workflow
1. Create new video event (should default to 1 frame)
2. Click elements - properties should appear
3. Add frames - each should be independent
4. Modify elements per frame
5. Save/load - verify frame independence persists

### VS Code Tasks
- `Run ReelTune`: Launch app
- `Run ReelTune (Debug)`: Launch with verbose output
- `Clean Generated Files`: Remove pycache

## Key Files to Understand
- `ui/template_editor/editor.py` - Event/frame coordination
- `ui/template_editor/canvas.py` - Element manipulation and rect handling
- `core/project.py` - Data models and persistence (ReleaseEvent class)
- `ui/mainwindow.py` - App structure and view switching
- `.vscode/tasks.json` - Development commands
