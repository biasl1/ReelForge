#!/usr/bin/env python3
"""
Test script for enhanced asset management features
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer
from core.project import ReelForgeProject, AssetReference
from ui.enhanced_asset_panel import EnhancedAssetPanel

def test_asset_management():
    """Test asset management panel with descriptions and folders"""

    app = QApplication(sys.argv)

    # Create test project with sample assets
    project = ReelForgeProject()
    project.metadata.name = "Test Asset Management Project"

    # Add sample assets with descriptions and folders
    sample_assets = [
        AssetReference(
            id="asset1",
            name="intro_video.mp4",
            file_path="assets/intro_video.mp4",
            file_type="video",
            description="Introduction video showing plugin overview and key features",
            folder="intro"
        ),
        AssetReference(
            id="asset2",
            name="demo_audio.wav",
            file_path="assets/demo_audio.wav",
            file_type="audio",
            description="Clean audio sample demonstrating the plugin's processing capabilities",
            folder="demos"
        ),
        AssetReference(
            id="asset3",
            name="logo.png",
            file_path="assets/logo.png",
            file_type="image",
            description="Company logo for branding consistency",
            folder=""  # No folder
        ),
        AssetReference(
            id="asset4",
            name="outro_music.mp3",
            file_path="assets/outro_music.mp3",
            file_type="audio",
            description="Background music for video endings",
            folder="outro"
        )
    ]

    for asset in sample_assets:
        project.assets[asset.id] = asset

    # Create and show asset management panel
    panel = EnhancedAssetPanel()
    panel.set_project(project)
    panel.show()

    print("Asset Management Panel Features Test")
    print("====================================")
    print("")
    print("Features implemented:")
    print("• Asset cards with edit and delete buttons")
    print("• Description editing dialog for AI context")
    print("• Folder organization system")
    print("• Folder filter dropdown")
    print("• Professional, clean interface (no inappropriate content)")
    print("")
    print("Sample data loaded:")
    print(f"• {len(sample_assets)} test assets")
    print(f"• {len(project.get_asset_folders())} folders: {', '.join(project.get_asset_folders())}")
    print("")
    print("Try the following:")
    print("1. Use folder filter to view assets by category")
    print("2. Click 'Edit' on any asset to modify description/folder")
    print("3. Click 'Delete' to remove an asset")
    print("4. Click 'New Folder' to create organization folders")

    # Close after showing for a while
    QTimer.singleShot(8000, app.quit)

    app.exec()

    print("Asset management test completed!")

if __name__ == "__main__":
    test_asset_management()
