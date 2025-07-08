"""
ReelTune Template Editor Package

A modular, clean template editor with zoom, pan, and unconstrained element placement.

This package provides:
- TemplateEditor: Main editor widget combining canvas and controls
- TemplateCanvas: Interactive canvas with zoom/pan and element manipulation
- TemplateControls: Controls panel for settings and element properties
- TemplatePersistence: Save/load functionality for templates

Usage:
    from ui.template_editor import TemplateEditor
    
    editor = TemplateEditor()
    editor.set_content_type("reel")
    
    # Get template configuration
    config = editor.get_template_config()
    
    # Save/load templates
    editor.save_template("my_template.json")
    editor.load_template("my_template.json")
"""

from .editor import TemplateEditor
from .canvas import TemplateCanvas
from .controls import TemplateControls
from .persistence import TemplatePersistence

# Import utilities for external use
from .utils import (
    CONTENT_DIMENSIONS,
    get_content_dimensions,
    get_canvas_size,
    CoordinateTransform
)

# Main export - the complete template editor
__all__ = [
    'TemplateEditor',
    'TemplateCanvas', 
    'TemplateControls',
    'TemplatePersistence',
    'CONTENT_DIMENSIONS',
    'get_content_dimensions',
    'get_canvas_size',
    'CoordinateTransform'
]

# For backward compatibility with existing code
from .compat import BackwardCompatibleTemplateEditor
SimpleTemplateEditor = BackwardCompatibleTemplateEditor
AITemplateEditor = BackwardCompatibleTemplateEditor
VisualTemplateEditor = TemplateCanvas
