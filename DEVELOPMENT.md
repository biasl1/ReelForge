# ReelForge Development

## Development Setup

1. **Create virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application**:
   ```bash
   python main.py
   ```

## VS Code Tasks

Use **Ctrl+Shift+P** → **Tasks: Run Task** to access:

- **Run ReelForge** - Launch the application
- **Run ReelForge (Debug)** - Launch with debug output
- **Install Dependencies** - Install/update Python packages
- **Create Virtual Environment** - Set up .venv

## Architecture Notes

### Key Design Patterns

1. **Model-View Separation**: Core logic in `core/`, UI in `ui/`
2. **Signal-Slot Communication**: Loose coupling between components
3. **JSON Project Files**: Human-readable, version-controllable
4. **Path Abstraction**: Relative paths within projects

### Adding New Features

1. **Core Logic**: Add to appropriate `core/` module
2. **UI Components**: Create in `ui/` with proper styling
3. **Signals**: Connect components via Qt signals/slots
4. **Testing**: Verify save/load functionality

### File Organization

```
core/
  project.py     # Project management, serialization
  assets.py      # File handling, validation, metadata
  utils.py       # Shared utilities, helpers

ui/
  mainwindow.py  # Main interface, layout management
  startup_dialog.py  # Project creation/opening
  menu.py        # Menu bar, keyboard shortcuts
  style_utils.py # Dark theme, consistent styling
```

## Debugging Tips

1. **Console Output**: Check terminal for error messages
2. **Qt Debug**: Use `QLoggingCategory` for detailed Qt logs
3. **Project Files**: Examine `.rforge` JSON for data integrity
4. **Settings**: Check app data directory for configuration issues

## Next Implementation Steps

1. **Timeline Widget**: Video/audio track representation
2. **Media Preview**: Video player with scrubbing
3. **Export System**: FFmpeg integration for rendering
4. **Effects Pipeline**: Modular effect application system
