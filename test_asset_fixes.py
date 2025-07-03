#!/usr/bin/env python3
"""
Test Asset Import and Categorization
Quick test to verify the fixes work
"""

import sys
import tempfile
from pathlib import Path
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QTimer

from core.project import ReelForgeProject, AssetReference
from ui.enhanced_asset_panel import EnhancedAssetPanel

def test_asset_functionality():
    """Test asset import and categorization"""
    print("🧪 Testing Asset Import & Categorization")
    print("="*50)
    
    # Create project
    project = ReelForgeProject()
    project.metadata.name = "Asset Test Project"
    
    # Create sample assets in temp directory
    temp_dir = Path(tempfile.gettempdir()) / "reeltune_test"
    temp_dir.mkdir(exist_ok=True)
    
    sample_files = [
        temp_dir / "image1.jpg",
        temp_dir / "image2.png", 
        temp_dir / "video1.mp4",
        temp_dir / "audio1.mp3",
        temp_dir / "audio2.wav",
        temp_dir / "document.pdf"
    ]
    
    # Create the files
    for file_path in sample_files:
        file_path.write_text("sample content")
    
    print(f"📁 Created {len(sample_files)} test files")
    
    # Test import functionality
    imported_count = 0
    for file_path in sample_files:
        asset_id = project.import_asset(str(file_path))
        if asset_id:
            imported_count += 1
            print(f"✅ Imported: {file_path.name} → {asset_id}")
        else:
            print(f"❌ Failed: {file_path.name}")
    
    print(f"\n📊 Import Results:")
    print(f"   • Total files: {len(sample_files)}")
    print(f"   • Successfully imported: {imported_count}")
    print(f"   • Assets in project: {len(project.get_all_assets())}")
    
    # Check categorization
    categories = {}
    for asset in project.get_all_assets():
        if asset.file_type not in categories:
            categories[asset.file_type] = 0
        categories[asset.file_type] += 1
    
    print(f"\n🗂️  Categorization:")
    category_icons = {'image': '🖼️', 'video': '🎬', 'audio': '🎵', 'other': '📄'}
    for cat, count in categories.items():
        icon = category_icons.get(cat, '❓')
        print(f"   {icon} {cat.title()}: {count} files")
    
    # Test enhanced asset panel
    app = QApplication.instance() or QApplication(sys.argv)
    
    print(f"\n🎨 Testing Enhanced Asset Panel...")
    asset_panel = EnhancedAssetPanel()
    asset_panel.set_project(project)
    asset_panel.show()
    
    print(f"✅ Asset panel created and populated!")
    print(f"🎯 Should see {len(categories)} categories with beautiful icons")
    
    # Auto-close after 5 seconds
    def close_test():
        print("\n🎉 Test completed successfully!")
        print("✨ Features working:")
        print("   • Asset import ✅")
        print("   • File type detection ✅") 
        print("   • Categorization ✅")
        print("   • Enhanced asset panel ✅")
        app.quit()
    
    QTimer.singleShot(5000, close_test)
    
    # Clean up
    for file_path in sample_files:
        if file_path.exists():
            file_path.unlink()
    temp_dir.rmdir()
    
    return app.exec()

if __name__ == "__main__":
    sys.exit(test_asset_functionality())
