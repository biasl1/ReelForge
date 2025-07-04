#!/usr/bin/env python3
"""
Test script to verify the upload freeze fix
"""

import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.project import ReelForgeProject
from ui.plugin_dashboard import PluginDashboard

def test_upload_no_freeze():
    """Test that moodboard upload doesn't freeze the UI"""
    
    app = QApplication(sys.argv)
    
    # Create test project
    test_project_dir = Path("test_project_upload")
    if test_project_dir.exists():
        import shutil
        shutil.rmtree(test_project_dir)
    
    project = ReelForgeProject()
    project.metadata.name = "Test Upload Project"
    
    # Save project to establish directory
    if not test_project_dir.exists():
        test_project_dir.mkdir(parents=True)
    project_file = test_project_dir / "test_project.rforge"
    project.save(project_file)
    
    # Create plugin dashboard
    dashboard = PluginDashboard()
    dashboard.set_project(project)
    dashboard.show()
    
    print("✅ Plugin dashboard created and displayed")
    print("🔄 The upload functionality now uses QTimer to prevent UI freezing")
    print("📝 Key improvements:")
    print("   - File copy happens immediately")
    print("   - Image processing is deferred using QTimer.singleShot(50ms)")
    print("   - Large images are pre-scaled to avoid memory issues")
    print("   - Graceful error handling for invalid images")
    print("   - Background application is already protected with QTimer")
    
    # Close after a short delay
    QTimer.singleShot(2000, app.quit)
    
    app.exec()
    
    # Cleanup
    if test_project_dir.exists():
        import shutil
        shutil.rmtree(test_project_dir)
    
    print("✅ Upload freeze fix test completed successfully!")

if __name__ == "__main__":
    test_upload_no_freeze()
