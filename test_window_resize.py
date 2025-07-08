#!/usr/bin/env python3
"""
Test script to verify that window resizing maintains element positions correctly.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QHBoxLayout
from PyQt6.QtCore import QTimer
from ui.template_editor.canvas import TemplateCanvas

class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Resize Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create canvas
        self.canvas = TemplateCanvas()
        layout.addWidget(self.canvas)
        
        # Create control buttons
        button_layout = QHBoxLayout()
        
        resize_small_btn = QPushButton("Resize Small (600x400)")
        resize_small_btn.clicked.connect(lambda: self.resize(600, 400))
        button_layout.addWidget(resize_small_btn)
        
        resize_medium_btn = QPushButton("Resize Medium (800x600)")
        resize_medium_btn.clicked.connect(lambda: self.resize(800, 600))
        button_layout.addWidget(resize_medium_btn)
        
        resize_large_btn = QPushButton("Resize Large (1200x800)")
        resize_large_btn.clicked.connect(lambda: self.resize(1200, 800))
        button_layout.addWidget(resize_large_btn)
        
        layout.addLayout(button_layout)
        
        # Initialize canvas
        self.canvas.set_content_type('reel')
        
    def test_element_positions(self):
        """Test that element positions maintain correct proportions after resize."""
        print("\n=== Window Resize Test ===")
        
        # Get initial state
        initial_frame = self.canvas.content_frame
        initial_elements = {}
        for elem_id, elem in self.canvas.elements.items():
            if elem.get('enabled', True):
                rect = elem['rect']
                # Calculate relative position within frame
                rel_x = (rect.x() - initial_frame.x()) / initial_frame.width()
                rel_y = (rect.y() - initial_frame.y()) / initial_frame.height()
                rel_w = rect.width() / initial_frame.width()
                rel_h = rect.height() / initial_frame.height()
                initial_elements[elem_id] = (rel_x, rel_y, rel_w, rel_h)
        
        print(f"Initial frame: {initial_frame.width()}x{initial_frame.height()} at ({initial_frame.x()}, {initial_frame.y()})")
        print(f"Initial elements: {len(initial_elements)}")
        
        # Store original window size
        original_size = self.size()
        
        # Test sequence: resize to different sizes and check element positions
        test_sizes = [(600, 400), (1200, 800), (800, 600)]
        
        for width, height in test_sizes:
            print(f"\n--- Resizing to {width}x{height} ---")
            
            # Resize window
            self.resize(width, height)
            
            # Process events to update the canvas
            QApplication.processEvents()
            
            # Let the paint event occur
            self.canvas.update()
            QApplication.processEvents()
            
            # Check new frame and element positions
            new_frame = self.canvas.content_frame
            print(f"New frame: {new_frame.width()}x{new_frame.height()} at ({new_frame.x()}, {new_frame.y()})")
            
            # Verify element relative positions are maintained
            errors = []
            for elem_id, elem in self.canvas.elements.items():
                if elem.get('enabled', True) and elem_id in initial_elements:
                    rect = elem['rect']
                    
                    # Calculate new relative position
                    rel_x = (rect.x() - new_frame.x()) / new_frame.width()
                    rel_y = (rect.y() - new_frame.y()) / new_frame.height()
                    rel_w = rect.width() / new_frame.width()
                    rel_h = rect.height() / new_frame.height()
                    
                    # Compare with initial relative position
                    init_rel_x, init_rel_y, init_rel_w, init_rel_h = initial_elements[elem_id]
                    
                    # Allow small tolerance for floating point calculations
                    tolerance = 0.01
                    
                    x_diff = abs(rel_x - init_rel_x)
                    y_diff = abs(rel_y - init_rel_y)
                    w_diff = abs(rel_w - init_rel_w)
                    h_diff = abs(rel_h - init_rel_h)
                    
                    if (x_diff > tolerance or y_diff > tolerance or 
                        w_diff > tolerance or h_diff > tolerance):
                        errors.append(f"  {elem_id}: position drift x={x_diff:.3f}, y={y_diff:.3f}, w={w_diff:.3f}, h={h_diff:.3f}")
                    else:
                        print(f"  {elem_id}: ✓ position maintained")
            
            if errors:
                print("  ERRORS:")
                for error in errors:
                    print(error)
            else:
                print("  ✓ All elements maintained relative positions")
        
        # Restore original size
        self.resize(original_size)
        QApplication.processEvents()
        
        print("\n=== Test Complete ===")
        
        # Return to initial size for interactive testing
        return len(errors) == 0

def main():
    app = QApplication(sys.argv)
    
    # Create test window
    window = TestWindow()
    window.show()
    
    # Run automated test after a short delay
    def run_test():
        success = window.test_element_positions()
        print(f"\nTest Result: {'PASS' if success else 'FAIL'}")
        print("\nWindow is now ready for interactive testing.")
        print("Use the buttons to resize and observe element behavior.")
    
    QTimer.singleShot(1000, run_test)
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
