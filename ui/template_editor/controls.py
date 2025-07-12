"""
UI controls and settings panel for the template editor.
"""
import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel,
    QComboBox, QPushButton, QCheckBox, QSpinBox, QSlider,
    QColorDialog, QLineEdit, QFormLayout, QDoubleSpinBox
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor

from .utils import CONTENT_DIMENSIONS


class TemplateControls(QWidget):
    """
    Controls panel for template editing settings.
    """
    
    # Signals
    event_changed = pyqtSignal(str)  # event_id
    constraint_mode_changed = pyqtSignal(bool)
    element_property_changed = pyqtSignal(str, str, object)  # element_id, property, value
    reset_positions_requested = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMaximumWidth(300)
        self.setMinimumWidth(250)
        
        self.current_element = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Set up the control panel UI."""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Content type selection
        content_group = self._create_content_type_group()
        layout.addWidget(content_group)
        
        # Constraint settings
        constraint_group = self._create_constraint_group()
        layout.addWidget(constraint_group)
        
        # Reset Positions button
        reset_btn = QPushButton("Reset All Positions")
        reset_btn.setToolTip("Reset all elements to their default positions for this content type.")
        reset_btn.clicked.connect(self.reset_positions_requested.emit)
        layout.addWidget(reset_btn)
        
        # Element properties
        self.element_group = self._create_element_properties_group()
        layout.addWidget(self.element_group)
        
        layout.addStretch()
    
    def _create_content_type_group(self) -> QGroupBox:
        """Create calendar event selection group."""
        group = QGroupBox("Calendar Event")
        layout = QVBoxLayout(group)
        
        self.event_combo = QComboBox()
        self.event_combo.addItem("No event selected", None)
        self.event_combo.currentTextChanged.connect(self._on_event_changed)
        layout.addWidget(self.event_combo)
        
        # Note: Frame navigation is handled by the frame timeline at the bottom
        # No frame selector needed here - it was redundant and confusing
        
        return group
    
    def _create_constraint_group(self) -> QGroupBox:
        """Create constraint settings group."""
        group = QGroupBox("Element Constraints")
        layout = QVBoxLayout(group)
        
        self.constrain_checkbox = QCheckBox("Constrain elements to content frame")
        self.constrain_checkbox.setToolTip(
            "When enabled, elements cannot be moved outside the content frame. "
            "When disabled, elements can be placed anywhere on the canvas."
        )
        self.constrain_checkbox.toggled.connect(self.constraint_mode_changed.emit)
        layout.addWidget(self.constrain_checkbox)
        
        # Add info label
        info_label = QLabel("Unchecked: Free placement mode\nChecked: Constrained to frame")
        info_label.setStyleSheet("color: #888; font-size: 11px;")
        layout.addWidget(info_label)
        
        return group
    
    def _create_element_properties_group(self) -> QGroupBox:
        """Create element properties group."""
        group = QGroupBox("Element Properties")
        layout = QVBoxLayout(group)
        
        self.no_selection_label = QLabel("Select an element to edit properties")
        self.no_selection_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.no_selection_label.setStyleSheet("color: #888; padding: 20px;")
        layout.addWidget(self.no_selection_label)
        
        # Properties will be added dynamically based on selected element
        self.properties_widget = QWidget()
        self.properties_layout = QFormLayout(self.properties_widget)
        layout.addWidget(self.properties_widget)
        
        self.properties_widget.hide()
        
        return group
    
    def _on_event_changed(self):
        """Handle event selection change."""
        event_id = self.event_combo.currentData()
        if event_id:
            self.event_changed.emit(event_id)
    
    def set_content_type(self, content_type: str):
        """Set the current content type - now determined by selected event."""
        # Content type is now determined by the selected event, not a separate control
        pass
    
    def set_constraint_mode(self, constrain: bool):
        """Set constraint mode."""
        self.constrain_checkbox.setChecked(constrain)
    
    def _update_element_properties(self, element_id: str, element_data: dict):
        """Update the properties panel for the selected element."""
        # Clear existing properties
        for i in reversed(range(self.properties_layout.count())):
            child = self.properties_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        element_type = element_data.get('type', 'unknown')
        
        # Only add simplified controls - no complex positioning
        
        # Add type-specific properties
        if element_type == 'text':
            self._add_text_properties(element_data)
        elif element_type == 'pip':
            self._add_pip_properties(element_data)
        
        # Enable/disable checkbox (always show this for all elements)
        enabled_checkbox = QCheckBox("Visible")
        enabled_checkbox.setChecked(element_data.get('enabled', True))
        enabled_checkbox.toggled.connect(
            lambda checked: self.element_property_changed.emit(element_id, 'enabled', checked)
        )
        self.properties_layout.addRow("", enabled_checkbox)  # No label, just the checkbox
        
        self.no_selection_label.hide()
        self.properties_widget.show()
    
    def _add_position_controls(self, element_data: dict):
        """Add position controls."""
        rect = element_data.get('rect')
        if not rect:
            return
        
        # X position
        x_spin = QSpinBox()
        x_spin.setRange(-9999, 9999)
        x_spin.setValue(rect.x())
        x_spin.valueChanged.connect(
            lambda value: self._update_rect_property('x', value)
        )
        self.properties_layout.addRow("X:", x_spin)
        
        # Y position
        y_spin = QSpinBox()
        y_spin.setRange(-9999, 9999)
        y_spin.setValue(rect.y())
        y_spin.valueChanged.connect(
            lambda value: self._update_rect_property('y', value)
        )
        self.properties_layout.addRow("Y:", y_spin)
    
    def _add_size_controls(self, element_data: dict):
        """Add size controls."""
        rect = element_data.get('rect')
        if not rect:
            return
        
        # Width
        width_spin = QSpinBox()
        width_spin.setRange(10, 9999)
        width_spin.setValue(rect.width())
        width_spin.valueChanged.connect(
            lambda value: self._update_rect_property('width', value)
        )
        self.properties_layout.addRow("Width:", width_spin)
        
        # Height
        height_spin = QSpinBox()
        height_spin.setRange(10, 9999)
        height_spin.setValue(rect.height())
        height_spin.valueChanged.connect(
            lambda value: self._update_rect_property('height', value)
        )
        self.properties_layout.addRow("Height:", height_spin)
    
    def _add_text_properties(self, element_data: dict):
        """Add simplified text-specific properties."""
        # Content
        content_edit = QLineEdit()
        content_edit.setText(element_data.get('content', ''))
        content_edit.textChanged.connect(
            lambda text: self.element_property_changed.emit(self.current_element, 'content', text)
        )
        self.properties_layout.addRow("Text:", content_edit)
        
        # Font size
        size_spin = QSpinBox()
        size_spin.setRange(8, 200)
        size_spin.setValue(element_data.get('size', 24))
        size_spin.valueChanged.connect(
            lambda value: self.element_property_changed.emit(self.current_element, 'size', value)
        )
        self.properties_layout.addRow("Font Size:", size_spin)
        
        # Color
        color_btn = QPushButton("Choose Color")
        color = element_data.get('color', QColor(255, 255, 255))
        color_btn.setStyleSheet(f"background-color: {color.name()};")
        color_btn.clicked.connect(lambda: self._choose_color(color_btn))
        self.properties_layout.addRow("Color:", color_btn)
        
        # Simplified Position (Top/Middle/Bottom)
        position_combo = QComboBox()
        position_combo.addItems(["Top", "Middle", "Bottom"])
        
        # Determine current position based on Y coordinate - handle rect format safely
        rect = element_data.get('rect')
        current_position = "Middle"  # default
        if rect:
            # Handle different rect formats safely
            y_pos = 300  # default middle position
            if hasattr(rect, 'y'):  # QRect object
                y_pos = rect.y()
            elif isinstance(rect, dict):
                y_pos = rect.get('y', 300)
            elif isinstance(rect, list) and len(rect) >= 2:
                y_pos = rect[1]  # Y is second element
            
            # Rough approximation based on content dimensions
            if y_pos < 200:
                current_position = "Top"
            elif y_pos > 400:
                current_position = "Bottom"
        
        position_combo.setCurrentText(current_position)
        position_combo.currentTextChanged.connect(
            lambda text: self.element_property_changed.emit(self.current_element, 'position_preset', text)
        )
        self.properties_layout.addRow("Position:", position_combo)
    
    def _add_pip_properties(self, element_data: dict):
        """Add simplified PiP-specific properties - always centered with 16:9 aspect ratio."""
        
        # Info label explaining the simplified PiP behavior
        info_label = QLabel("📹 Plugin video preview (always centered, 16:9 aspect ratio)")
        info_label.setStyleSheet("color: #666; font-style: italic; margin-bottom: 10px;")
        info_label.setWordWrap(True)
        self.properties_layout.addRow(info_label)
        
        # Corner radius slider (kept for visual customization)
        corner_radius = element_data.get('corner_radius', 0)
        corner_slider = QSlider(Qt.Orientation.Horizontal)
        corner_slider.setRange(0, 50)
        corner_slider.setValue(corner_radius)
        corner_slider.setToolTip(f"Adjust corner roundness (0-50px). Current: {corner_radius}px")
        corner_slider.valueChanged.connect(
            lambda value: self._update_corner_radius(value)
        )
        
        corner_value_label = QLabel(f"{corner_radius}px")
        corner_value_label.setStyleSheet("color: #666; font-family: monospace; min-width: 40px;")
        
        corner_layout = QHBoxLayout()
        corner_layout.addWidget(corner_slider)
        corner_layout.addWidget(corner_value_label)
        
        corner_widget = QWidget()
        corner_widget.setLayout(corner_layout)
        self.properties_layout.addRow("Corner Radius:", corner_widget)
        
        # Store references for updates
        self.corner_slider = corner_slider
        self.corner_value_label = corner_value_label
    
    def _choose_color(self, button: QPushButton, property_name: str = 'color'):
        """Open color chooser dialog."""
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()};")
            self.element_property_changed.emit(self.current_element, property_name, color)
    
    def _update_rect_property(self, property_name: str, value: int):
        """Update a rectangle property."""
        # This would need to communicate back to get current rect and update it
        # For now, emit a signal that the parent can handle
        self.element_property_changed.emit(self.current_element, f'rect_{property_name}', value)
    
    def _update_corner_radius(self, value: int):
        """Update corner radius and the display label."""
        if hasattr(self, 'corner_value_label'):
            self.corner_value_label.setText(f"{value}px")
        
        if hasattr(self, 'corner_slider'):
            self.corner_slider.setToolTip(f"Adjust corner roundness (0-50px). Current: {value}px")
        
        if self.current_element:
            self.element_property_changed.emit(self.current_element, 'corner_radius', value)
    
    def update_element_position(self, element_id: str, new_rect):
        """Update element position display (placeholder)."""
        # This could update position displays in the UI if needed
        pass
    
    def update_element_size(self, element_id: str, new_rect):
        """Update element size display (placeholder)."""
        # This could update size displays in the UI if needed
        pass
    
    def set_events(self, events: list):
        """Set the available calendar events."""
        self.event_combo.clear()
        self.event_combo.addItem("No event selected", None)
        
        for event in events:
            display_name = f"{event.title} ({event.content_type.upper()}) - {event.date}"
            self.event_combo.addItem(display_name, event.id)
    
    def refresh_events(self, events_dict: dict):
        """Refresh the event list from a dictionary of events."""
        events = list(events_dict.values())
        self.set_events(events)
    
    def set_current_event(self, event_id: str, event_data: dict):
        """Set the current event being edited."""
        # Find and select the event in the combo box
        for i in range(self.event_combo.count()):
            if self.event_combo.itemData(i) == event_id:
                self.event_combo.setCurrentIndex(i)
                break
    
    def clear_selection(self):
        """Clear element selection."""
        self.current_element = None
        self.no_selection_label.show()
        self.properties_widget.hide()
        print("🔄 Controls cleared element selection")
    
    def set_selected_element(self, element_id: str, element_data: dict = None):
        """Set the currently selected element and optionally show its properties."""
        self.current_element = element_id
        print(f"🎯 Controls set selected element: {element_id}")
        
        if element_data:
            print(f"   Properties: visible={element_data.get('visible', True)}, enabled={element_data.get('enabled', True)}")
            
            if element_data.get('type') == 'text':
                print(f"   Text properties: content='{element_data.get('content', '')}', size={element_data.get('size', 24)}")
            elif element_data.get('type') == 'pip':
                print(f"   PiP properties: corner_radius={element_data.get('corner_radius', 0)}")
                
            self._update_element_properties(element_id, element_data)
        else:
            print("   (Properties will be loaded separately)")
    
    def update_selected_element_properties(self, element_data: dict):
        """Update properties for the currently selected element."""
        if self.current_element:
            self._update_element_properties(self.current_element, element_data)
