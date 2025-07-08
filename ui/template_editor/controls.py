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
    content_type_changed = pyqtSignal(str)
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
        """Create content type selection group."""
        group = QGroupBox("Content Type")
        layout = QVBoxLayout(group)
        
        self.content_combo = QComboBox()
        for content_type, dims in CONTENT_DIMENSIONS.items():
            self.content_combo.addItem(dims["name"], content_type)
        
        self.content_combo.currentTextChanged.connect(self._on_content_type_changed)
        layout.addWidget(self.content_combo)
        
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
    
    def _on_content_type_changed(self):
        """Handle content type change."""
        content_type = self.content_combo.currentData()
        if content_type:
            self.content_type_changed.emit(content_type)
    
    def set_content_type(self, content_type: str):
        """Set the current content type."""
        for i in range(self.content_combo.count()):
            if self.content_combo.itemData(i) == content_type:
                self.content_combo.setCurrentIndex(i)
                break
    
    def set_constraint_mode(self, constrain: bool):
        """Set constraint mode."""
        self.constrain_checkbox.setChecked(constrain)
    
    def set_selected_element(self, element_id: str, element_data: dict):
        """Set the currently selected element and show its properties."""
        self.current_element = element_id
        self._update_element_properties(element_id, element_data)
    
    def clear_selection(self):
        """Clear element selection."""
        self.current_element = None
        self.no_selection_label.show()
        self.properties_widget.hide()
    
    def _update_element_properties(self, element_id: str, element_data: dict):
        """Update the properties panel for the selected element."""
        # Clear existing properties
        for i in reversed(range(self.properties_layout.count())):
            child = self.properties_layout.itemAt(i).widget()
            if child:
                child.deleteLater()
        
        element_type = element_data.get('type', 'unknown')
        
        # Add common properties
        self._add_position_controls(element_data)
        self._add_size_controls(element_data)
        
        # Add type-specific properties
        if element_type == 'text':
            self._add_text_properties(element_data)
        elif element_type == 'pip':
            self._add_pip_properties(element_data)
        
        # Enable/disable checkbox
        enabled_checkbox = QCheckBox("Enabled")
        enabled_checkbox.setChecked(element_data.get('enabled', True))
        enabled_checkbox.toggled.connect(
            lambda checked: self.element_property_changed.emit(element_id, 'enabled', checked)
        )
        self.properties_layout.addRow("Visible:", enabled_checkbox)
        
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
        """Add text-specific properties."""
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
        
        # Style
        style_combo = QComboBox()
        style_combo.addItems(["normal", "bold"])
        style_combo.setCurrentText(element_data.get('style', 'normal'))
        style_combo.currentTextChanged.connect(
            lambda text: self.element_property_changed.emit(self.current_element, 'style', text)
        )
        self.properties_layout.addRow("Style:", style_combo)
    
    def _add_pip_properties(self, element_data: dict):
        """Add PiP-specific properties."""
        # Shape
        shape_combo = QComboBox()
        shape_combo.addItems(["square", "rectangle"])
        shape_combo.setCurrentText(element_data.get('shape', 'square'))
        shape_combo.currentTextChanged.connect(
            lambda text: self.element_property_changed.emit(self.current_element, 'shape', text)
        )
        self.properties_layout.addRow("Shape:", shape_combo)
        
        # Corner Radius Section
        style_label = QLabel("🎨 Visual Style")
        style_label.setStyleSheet("font-weight: bold; color: #ff6b35; margin-top: 10px;")
        self.properties_layout.addRow(style_label)
        
        # Corner radius slider
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
