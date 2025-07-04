#!/usr/bin/env python3
"""
Demo script to test the enhanced asset panel with thumbnails
"""

import sys
import os
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.project import ReelForgeProject, AssetReference
from ui.enhanced_asset_panel import EnhancedAssetPanel


def create_demo_project():
    """Create a demo project with sample assets"""
    project = ReelForgeProject()
    project.metadata.name = "Enhanced Asset Panel Demo"

    # Create some sample assets (you can add real files later)
    sample_assets = [
        AssetReference(
            id="demo_image_1",
            name="sample_image.jpg",
            file_path="/System/Library/Desktop Pictures/Sonoma.heic",  # macOS default wallpaper
            file_type="image",
            file_size=2048000
        ),
        AssetReference(
            id="demo_video_1",
            name="sample_video.mp4",
            file_path="/System/Library/Compositions/Drifting.mov",  # macOS screensaver
            file_type="video",
            file_size=50000000
        ),
        AssetReference(
            id="demo_audio_1",
            name="sample_audio.wav",
            file_path="/System/Library/Sounds/Hero.aiff",  # macOS system sound
            file_type="audio",
            file_size=128000
        ),
        AssetReference(
            id="demo_other_1",
            name="readme.txt",
            file_path="/usr/share/doc/README",
            file_type="other",
            file_size=4096
        )
    ]

    # Add sample assets that exist on the system
    for asset in sample_assets:
        if Path(asset.file_path).exists():
            project.add_asset(asset)
            print(f"✅ Added demo asset: {asset.name}")
        else:
            print(f"⚠️  Skipped missing asset: {asset.file_path}")

    return project


def demo_enhanced_asset_panel():
    """Demo the enhanced asset panel"""

    print("🎨 Enhanced Asset Panel Demo")
    print("=" * 50)

    app = QApplication(sys.argv)

    # Create demo project
    project = create_demo_project()

    # Create enhanced asset panel
    asset_panel = EnhancedAssetPanel()
    asset_panel.setWindowTitle("ReelForge - Enhanced Asset Panel Demo")
    asset_panel.resize(600, 800)

    # Set project
    asset_panel.set_project(project)

    # Connect signals for demo
    def on_asset_selected(asset_id):
        print(f"📁 Asset selected: {asset_id}")

    def on_asset_double_clicked(asset_id):
        print(f"🖱️  Asset double-clicked: {asset_id}")

    asset_panel.asset_selected.connect(on_asset_selected)
    asset_panel.asset_double_clicked.connect(on_asset_double_clicked)

    # Show panel
    asset_panel.show()

    print("\n🎯 Demo Features:")
    print("=" * 50)
    print("✨ Beautiful thumbnail previews for images")
    print("🎬 Video thumbnails with play button overlay")
    print("🎵 Professional icons for audio files")
    print("📄 Clean icons for other file types")
    print("🖱️  Click to select, double-click to open")
    print("📱 Responsive grid layout")
    print("🎨 Professional dark theme styling")

    print("\n⚠️  Note:")
    print("- Video thumbnails require ffmpeg to be installed")
    print("- Some demo files may not exist on your system")
    print("- You can drag & drop real files to test")

    print("\n🚀 The asset panel is now 10000x better!")

    return app.exec()


if __name__ == "__main__":
    print("🚀 Starting Enhanced Asset Panel Demo")
    print("   This shows off the beautiful new thumbnail previews!")
    print()

    try:
        result = demo_enhanced_asset_panel()
        print(f"\n✅ Demo completed with exit code: {result}")
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
