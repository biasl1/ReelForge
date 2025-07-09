"""
Add the _handle_frame_description_change method to TemplateEditor class.
This is a temporary file that will be used to fix the editor.py file.
"""

def _handle_frame_description_change(self, frame_index: int, description: str):
    """Update the canvas with the new frame description from the timeline UI."""
    self.canvas.set_frame_description(frame_index, description)
    self._emit_template_changed()
