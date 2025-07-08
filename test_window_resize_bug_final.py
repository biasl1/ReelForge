#!/usr/bin/env python3
"""
Comprehensive test to verify that the window resize bug is completely fixed.
This test simulates the exact scenario described by the user.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer, QRect
from ui.template_editor.canvas import TemplateCanvas

class WindowResizeBugTest(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Window Resize Bug Test")
        self.setGeometry(100, 100, 800, 600)
        
        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Create canvas
        self.canvas = TemplateCanvas()
        layout.addWidget(self.canvas)
        
        # Initialize canvas with reel content
        self.canvas.set_content_type('reel')
        
        # Set up initial custom positions
        self.setup_custom_positions()
        
    def setup_custom_positions(self):
        """Set up custom element positions to test preservation."""
        # Wait for initial layout
        QTimer.singleShot(100, self._setup_positions)
        
    def _setup_positions(self):
        """Actually set up the positions after initial layout."""
        print("Setting up custom element positions...")
        
        # Get current frame
        frame = self.canvas.content_frame
        print(f"Initial frame: {frame.width()}x{frame.height()} at ({frame.x()}, {frame.y()})")
        
        # Position PiP at 30%/20% of frame
        pip_x = frame.x() + int(frame.width() * 0.3)
        pip_y = frame.y() + int(frame.height() * 0.2)
        pip_size = 80
        self.canvas.elements['pip']['rect'] = QRect(pip_x, pip_y, pip_size, pip_size)
        
        # Position title at 15%/70% of frame
        title_x = frame.x() + int(frame.width() * 0.15)
        title_y = frame.y() + int(frame.height() * 0.7)
        self.canvas.elements['title']['rect'] = QRect(title_x, title_y, 180, 50)
        
        # Position subtitle at 20%/85% of frame
        subtitle_x = frame.x() + int(frame.width() * 0.2)
        subtitle_y = frame.y() + int(frame.height() * 0.85)
        self.canvas.elements['subtitle']['rect'] = QRect(subtitle_x, subtitle_y, 160, 30)
        
        print(f"PiP positioned at: ({pip_x}, {pip_y}) - 30%/20% of frame")
        print(f"Title positioned at: ({title_x}, {title_y}) - 15%/70% of frame")
        print(f"Subtitle positioned at: ({subtitle_x}, {subtitle_y}) - 20%/85% of frame")
        
        # Save the state
        self.canvas._save_current_state()
        self.canvas.update()
        
        # Start the test after a short delay
        QTimer.singleShot(500, self.run_comprehensive_test)
        
    def run_comprehensive_test(self):
        """Run the comprehensive window resize test."""
        print("\n" + "="*60)
        print("COMPREHENSIVE WINDOW RESIZE BUG TEST")
        print("="*60)
        
        # Record initial relative positions
        initial_frame = self.canvas.content_frame
        initial_positions = {}
        
        for elem_id, elem in self.canvas.elements.items():
            if elem.get('enabled', True):
                rect = elem['rect']
                rel_x = (rect.x() - initial_frame.x()) / initial_frame.width()
                rel_y = (rect.y() - initial_frame.y()) / initial_frame.height()
                rel_w = rect.width() / initial_frame.width()
                rel_h = rect.height() / initial_frame.height()
                initial_positions[elem_id] = {
                    'rel_x': rel_x, 'rel_y': rel_y, 
                    'rel_w': rel_w, 'rel_h': rel_h,
                    'abs_rect': QRect(rect)
                }
                print(f"{elem_id}: {rel_x:.1%} x {rel_y:.1%} ({rect.x()}, {rect.y()}) {rect.width()}x{rect.height()}")
        
        # Test multiple resize scenarios
        test_scenarios = [
            ("Small Window", 600, 400),
            ("Tall Window", 700, 900),
            ("Wide Window", 1400, 500),
            ("Large Window", 1200, 800),
            ("Back to Original", 800, 600)
        ]
        
        all_passed = True
        
        for scenario_name, width, height in test_scenarios:
            print(f"\n--- {scenario_name}: {width}x{height} ---")
            
            # Resize the window
            self.resize(width, height)
            QApplication.processEvents()
            
            # Force a repaint to trigger frame recalculation
            self.canvas.update()
            QApplication.processEvents()
            
            # Check the new frame and element positions
            new_frame = self.canvas.content_frame
            print(f"New frame: {new_frame.width()}x{new_frame.height()} at ({new_frame.x()}, {new_frame.y()})")
            
            # Verify each element maintains its relative position
            scenario_passed = True
            for elem_id, elem in self.canvas.elements.items():
                if elem.get('enabled', True) and elem_id in initial_positions:
                    rect = elem['rect']
                    
                    # Calculate current relative position
                    rel_x = (rect.x() - new_frame.x()) / new_frame.width()
                    rel_y = (rect.y() - new_frame.y()) / new_frame.height()
                    rel_w = rect.width() / new_frame.width()
                    rel_h = rect.height() / new_frame.height()
                    
                    # Compare with initial relative position
                    initial = initial_positions[elem_id]
                    
                    # Check for significant drift (more than 1%)
                    x_drift = abs(rel_x - initial['rel_x'])
                    y_drift = abs(rel_y - initial['rel_y'])
                    w_drift = abs(rel_w - initial['rel_w'])
                    h_drift = abs(rel_h - initial['rel_h'])
                    
                    max_drift = max(x_drift, y_drift, w_drift, h_drift)
                    
                    if max_drift > 0.01:  # 1% tolerance
                        print(f"  ❌ {elem_id}: POSITION DRIFT! max={max_drift:.1%}")
                        print(f"     Expected: {initial['rel_x']:.1%} x {initial['rel_y']:.1%}")
                        print(f"     Actual:   {rel_x:.1%} x {rel_y:.1%}")
                        scenario_passed = False
                        all_passed = False
                    else:
                        print(f"  ✅ {elem_id}: {rel_x:.1%} x {rel_y:.1%} (drift: {max_drift:.2%})")
            
            if scenario_passed:
                print(f"  🎯 {scenario_name}: ALL ELEMENTS MAINTAIN POSITION")
            else:
                print(f"  💥 {scenario_name}: POSITION DRIFT DETECTED")
        
        # Final result
        print("\n" + "="*60)
        if all_passed:
            print("🎉 WINDOW RESIZE BUG TEST: PASSED!")
            print("✅ All elements maintain correct relative positions")
            print("✅ No position drift detected during window resize")
            print("🔥 THE WINDOW RESIZE BUG IS FIXED! 🔥")
        else:
            print("💥 WINDOW RESIZE BUG TEST: FAILED!")
            print("❌ Elements lost their relative positions")
            print("🐛 Window resize bug still exists")
        print("="*60)
        
        return all_passed

def main():
    app = QApplication(sys.argv)
    
    # Create test window
    window = WindowResizeBugTest()
    window.show()
    
    # Keep the window open for manual inspection
    print("\nTest window will remain open for manual inspection.")
    print("You can manually resize the window to verify the fix.")
    
    # Run the application
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
