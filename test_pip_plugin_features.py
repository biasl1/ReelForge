#!/usr/bin/env python3
"""
Test the new PiP element features: plugin aspect ratio and corner radius.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QSlider, QLabel, QCheckBox, QFileDialog
from PyQt6.QtCore import Qt
from ui.template_editor.canvas import TemplateCanvas

class PiPTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PiP Plugin Aspect Ratio & Corner Radius Test")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QHBoxLayout(main_widget)
        
        # Create canvas
        self.canvas = TemplateCanvas()
        layout.addWidget(self.canvas, stretch=3)
        
        # Create controls panel
        controls_widget = QWidget()
        controls_widget.setMaximumWidth(300)
        controls_layout = QVBoxLayout(controls_widget)
        layout.addWidget(controls_widget, stretch=1)
        
        # Title
        title = QLabel("PiP Controls")
        title.setStyleSheet("font-size: 16px; font-weight: bold; padding: 10px;")
        controls_layout.addWidget(title)
        
        # Plugin aspect ratio toggle
        self.plugin_aspect_checkbox = QCheckBox("Use Plugin Aspect Ratio")
        self.plugin_aspect_checkbox.toggled.connect(self.toggle_plugin_aspect)
        controls_layout.addWidget(self.plugin_aspect_checkbox)
        
        # Load .adsp file button
        load_plugin_btn = QPushButton("Load .adsp Plugin File")
        load_plugin_btn.clicked.connect(self.load_plugin_file)
        controls_layout.addWidget(load_plugin_btn)
        
        # Plugin info display
        self.plugin_info_label = QLabel("No plugin loaded")
        self.plugin_info_label.setStyleSheet("padding: 5px; background: #f0f0f0; border-radius: 3px;")
        self.plugin_info_label.setWordWrap(True)
        controls_layout.addWidget(self.plugin_info_label)
        
        # Corner radius slider
        controls_layout.addWidget(QLabel("Corner Radius:"))
        self.corner_slider = QSlider(Qt.Orientation.Horizontal)
        self.corner_slider.setRange(0, 50)
        self.corner_slider.setValue(8)
        self.corner_slider.valueChanged.connect(self.update_corner_radius)
        controls_layout.addWidget(self.corner_slider)
        
        self.corner_value_label = QLabel("8px")
        controls_layout.addWidget(self.corner_value_label)
        
        # Test buttons
        controls_layout.addWidget(QLabel("Test Aspect Ratios:"))
        
        test_ratios = [
            ("Euclyd (1.75:1)", 1.75),
            ("Wide (2.0:1)", 2.0),
            ("Square (1:1)", 1.0),
            ("Tall (0.8:1)", 0.8),
            ("Standard (1.6:1)", 1.6)
        ]
        
        for name, ratio in test_ratios:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, r=ratio: self.set_test_aspect_ratio(r))
            controls_layout.addWidget(btn)
        
        controls_layout.addStretch()
        
        # Initialize canvas
        self.canvas.set_content_type('reel')
        self.canvas.element_selected.connect(self.on_element_selected)
        
        # Select PiP by default
        if 'pip' in self.canvas.elements:
            self.canvas.selected_element = 'pip'
            self.update_controls()
    
    def on_element_selected(self, element_id):
        """Handle element selection."""
        if self.canvas.elements[element_id].get('type') == 'pip':
            self.update_controls()
    
    def update_controls(self):
        """Update controls based on selected PiP element."""
        if not self.canvas.selected_element:
            return
        
        element_id = self.canvas.selected_element
        properties = self.canvas.get_pip_properties(element_id)
        
        if properties:
            # Update checkbox
            self.plugin_aspect_checkbox.setChecked(properties.get('use_plugin_aspect_ratio', False))
            
            # Update corner slider
            corner_radius = properties.get('corner_radius', 0)
            self.corner_slider.setValue(corner_radius)
            self.corner_value_label.setText(f"{corner_radius}px")
            
            # Update plugin info
            plugin_path = properties.get('plugin_file_path', '')
            aspect_ratio = properties.get('plugin_aspect_ratio', 1.75)
            
            if plugin_path:
                plugin_name = os.path.basename(plugin_path)
                self.plugin_info_label.setText(f"Plugin: {plugin_name}\nAspect Ratio: {aspect_ratio:.2f}:1")
            else:
                self.plugin_info_label.setText(f"Default Aspect Ratio: {aspect_ratio:.2f}:1")
    
    def toggle_plugin_aspect(self, enabled):
        """Toggle plugin aspect ratio."""
        if self.canvas.selected_element:
            self.canvas.toggle_plugin_aspect_ratio(self.canvas.selected_element, enabled)
    
    def update_corner_radius(self, value):
        """Update corner radius."""
        self.corner_value_label.setText(f"{value}px")
        if self.canvas.selected_element:
            self.canvas.set_pip_corner_radius(self.canvas.selected_element, value)
    
    def load_plugin_file(self):
        """Load a .adsp plugin file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            "Load Plugin File", 
            "", 
            "ADSP Plugin Files (*.adsp);;All Files (*)"
        )
        
        if file_path and self.canvas.selected_element:
            success = self.canvas.load_plugin_aspect_ratio(self.canvas.selected_element, file_path)
            if success:
                self.update_controls()
                print(f"Loaded plugin: {file_path}")
            else:
                print(f"Failed to load plugin: {file_path}")
    
    def set_test_aspect_ratio(self, ratio):
        """Set a test aspect ratio."""
        if self.canvas.selected_element:
            element = self.canvas.elements[self.canvas.selected_element]
            element['plugin_aspect_ratio'] = ratio
            element['use_plugin_aspect_ratio'] = True
            self.canvas._apply_plugin_aspect_ratio(self.canvas.selected_element)
            self.plugin_aspect_checkbox.setChecked(True)
            self.update_controls()

def main():
    app = QApplication(sys.argv)
    
    # Create test window
    window = PiPTestWindow()
    window.show()
    
    print("PiP Plugin Aspect Ratio & Corner Radius Test")
    print("=" * 50)
    print("Instructions:")
    print("1. Select the PiP element by clicking on it")
    print("2. Use 'Load .adsp Plugin File' to load a plugin file")
    print("3. Toggle 'Use Plugin Aspect Ratio' to enable/disable")
    print("4. Adjust 'Corner Radius' slider for rounded corners")
    print("5. Try different test aspect ratios")
    print("6. Resize the PiP element to see aspect ratio maintained")
    print("=" * 50)
    
    # Try to load the Euclyd plugin automatically if it exists
    euclyd_path = "/Users/test/Documents/development/Artists in DSP/Audio Plugins/WORKING ON/Euclyd/Euclyd.adsp"
    if os.path.exists(euclyd_path):
        print(f"Auto-loading Euclyd plugin from: {euclyd_path}")
        if window.canvas.selected_element:
            success = window.canvas.load_plugin_aspect_ratio(window.canvas.selected_element, euclyd_path)
            if success:
                window.update_controls()
                print("Euclyd plugin loaded successfully!")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
