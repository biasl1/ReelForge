#!/usr/bin/env python3
"""
Complete ReelTune Demo
Showcases all the enhanced features and improvements
"""

import sys
import tempfile
import shutil
from pathlib import Path
from datetime import datetime, timedelta
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.project import ReelForgeProject, ReleaseEvent
from ui.mainwindow import MainWindow

def create_demo_project():
    """Create a demo project with sample data"""
    print("🎯 Creating demo project with all features...")
    
    # Create project
    project = ReelForgeProject()
    project.metadata.name = "ReelTune Complete Demo"
    project.metadata.description = "Showcasing professional content planning features"
    
    # Set global AI prompt
    project.global_prompt = "Professional, modern tone with focus on creativity and innovation. Target audience: content creators and musicians."
    
    # Add some sample events
    today = datetime.now()
    
    # Event 1: Reel for today
    event1 = ReleaseEvent(
        id="demo_event_1",
        date=today.date().isoformat(),
        content_type="reel",
        title="Creative Process Behind the Beat",
        description="Show the step-by-step creative process, focus on the unique workflow and inspiration",
        platforms=["instagram", "tiktok"]
    )
    
    # Event 2: Story for tomorrow
    event2 = ReleaseEvent(
        id="demo_event_2",
        date=(today + timedelta(days=1)).date().isoformat(),
        content_type="story",
        title="Behind the Scenes",
        description="Casual, authentic look at the studio setup and creative environment",
        platforms=["instagram"]
    )
    
    # Event 3: Tutorial for next week
    event3 = ReleaseEvent(
        id="demo_event_3",
        date=(today + timedelta(days=7)).date().isoformat(),
        content_type="tutorial",
        title="Advanced Mixing Techniques",
        description="Deep dive into professional mixing techniques, educational content for aspiring producers",
        platforms=["youtube", "instagram"]
    )
    
    # Add events to project
    project.add_release_event(event1)
    project.add_release_event(event2)
    project.add_release_event(event3)
    
    print(f"✅ Created project with {len(project.release_events)} scheduled events")
    return project

def create_sample_assets():
    """Create some sample assets for demonstration"""
    print("📁 Creating sample assets...")
    
    # Create temporary directory for demo assets
    demo_dir = Path(tempfile.gettempdir()) / "reeltune_demo"
    demo_dir.mkdir(exist_ok=True)
    
    # Create sample files (empty for demo)
    sample_files = [
        demo_dir / "beat_v1.wav",
        demo_dir / "studio_shot.jpg", 
        demo_dir / "process_video.mp4",
        demo_dir / "track_stems.zip"
    ]
    
    for file_path in sample_files:
        if not file_path.exists():
            file_path.write_text("Demo file content")
            
    print(f"✅ Created {len(sample_files)} sample assets")
    return list(sample_files)

def main():
    """Run the complete demo"""
    print("🚀 ReelTune Complete Feature Demo")
    print("="*50)
    
    app = QApplication(sys.argv)
    
    # Create demo project
    project = create_demo_project()
    
    # Create sample assets
    sample_assets = create_sample_assets()
    
    # Add assets to project using proper import method
    for asset_path in sample_assets:
        asset_id = project.import_asset(str(asset_path))
        if asset_id:
            print(f"✅ Imported asset: {asset_path.name}")
        else:
            print(f"❌ Failed to import: {asset_path.name}")
    
    print(f"📊 Project Summary:")
    print(f"   • Name: {project.metadata.name}")
    print(f"   • Events: {len(project.release_events)}")
    print(f"   • Assets: {len(project.get_all_assets())}")
    print(f"   • Global Prompt: {project.global_prompt[:50]}...")
    
    # Create and show main window
    print("\n🎨 Launching Enhanced ReelTune Interface...")
    print("="*50)
    
    main_window = MainWindow()
    
    # Load the demo project
    main_window.project = project
    
    # Update window title
    title = f"ReelTune Demo - {project.metadata.name}"
    main_window.setWindowTitle(title)
    
    # Update all UI components
    main_window.asset_panel.set_project(project)
    if hasattr(main_window, 'timeline_widget'):
        main_window.timeline_widget.set_project(project)
        main_window.timeline_widget.refresh_timeline()
    
    main_window.show()
    
    # Auto-close after demo
    def close_demo():
        print("\n🎉 Demo completed!")
        print("="*30)
        print("✨ Features Demonstrated:")
        print("   • Enhanced Asset Panel with thumbnails")
        print("   • Professional timeline with event management") 
        print("   • AI-ready project structure")
        print("   • Plugin integration system")
        print("   • Modern, responsive UI design")
        print("   • Complete content planning workflow")
        app.quit()
    
    # Close after 10 seconds
    QTimer.singleShot(10000, close_demo)
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(main())
