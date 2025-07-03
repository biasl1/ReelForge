"""
Project data models and management for ReelForge
Handles creation, loading, and saving of .rforge project files
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class ProjectMetadata:
    """Project metadata structure"""
    name: str
    description: str = ""
    format: str = "1080p"  # Default format
    fps: int = 30
    created_date: str = ""
    modified_date: str = ""
    version: str = "1.0"
    
    def __post_init__(self):
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        self.modified_date = datetime.now().isoformat()


@dataclass  
class AssetReference:
    """Reference to an asset file"""
    id: str
    name: str
    file_path: str
    file_type: str  # 'video', 'audio', 'image', 'other'
    duration: Optional[float] = None  # For video/audio
    dimensions: Optional[tuple] = None  # For images/video
    file_size: Optional[int] = None
    import_date: str = ""
    
    def __post_init__(self):
        if not self.import_date:
            self.import_date = datetime.now().isoformat()


class ReelForgeProject:
    """Main project class for ReelForge"""
    
    def __init__(self, metadata: Optional[ProjectMetadata] = None):
        self.metadata = metadata or ProjectMetadata(name="Untitled Project")
        self.assets: Dict[str, AssetReference] = {}
        self.project_file_path: Optional[Path] = None
        self._is_modified = False
        
    @property
    def is_modified(self) -> bool:
        """Check if project has unsaved changes"""
        return self._is_modified
        
    @property
    def project_name(self) -> str:
        """Get project name"""
        return self.metadata.name
        
    @property 
    def project_directory(self) -> Optional[Path]:
        """Get project directory path"""
        if self.project_file_path:
            return self.project_file_path.parent
        return None
        
    def mark_modified(self):
        """Mark project as modified"""
        self._is_modified = True
        self.metadata.modified_date = datetime.now().isoformat()
        
    def add_asset(self, asset: AssetReference) -> bool:
        """Add asset to project"""
        try:
            if asset.id in self.assets:
                return False  # Asset ID already exists
                
            self.assets[asset.id] = asset
            self.mark_modified()
            return True
        except Exception:
            return False
            
    def remove_asset(self, asset_id: str) -> bool:
        """Remove asset from project"""
        try:
            if asset_id in self.assets:
                del self.assets[asset_id]
                self.mark_modified()
                return True
            return False
        except Exception:
            return False
            
    def get_asset(self, asset_id: str) -> Optional[AssetReference]:
        """Get asset by ID"""
        return self.assets.get(asset_id)
        
    def get_all_assets(self) -> List[AssetReference]:
        """Get all assets as list"""
        return list(self.assets.values())
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary for JSON serialization"""
        return {
            "metadata": asdict(self.metadata),
            "assets": {k: asdict(v) for k, v in self.assets.items()},
            "version": "1.0"
        }
        
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ReelForgeProject':
        """Create project from dictionary"""
        project = cls()
        
        # Load metadata
        if "metadata" in data:
            project.metadata = ProjectMetadata(**data["metadata"])
            
        # Load assets
        if "assets" in data:
            for asset_id, asset_data in data["assets"].items():
                asset = AssetReference(**asset_data)
                project.assets[asset_id] = asset
                
        project._is_modified = False
        return project
        
    def save(self, file_path: Optional[Path] = None) -> bool:
        """Save project to file"""
        try:
            target_path = file_path or self.project_file_path
            if not target_path:
                raise ValueError("No file path specified")
                
            # Ensure .rforge extension
            if target_path.suffix.lower() != '.rforge':
                target_path = target_path.with_suffix('.rforge')
                
            # Create directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save project data
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=2)
                
            self.project_file_path = target_path
            self._is_modified = False
            
            return True
            
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
            
    @classmethod
    def load(cls, file_path: Path) -> Optional['ReelForgeProject']:
        """Load project from file"""
        try:
            if not file_path.exists():
                return None
                
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            project = cls.from_dict(data)
            project.project_file_path = file_path
            project._is_modified = False
            
            return project
            
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
            
    def create_new(self, name: str, location: Path, 
                   description: str = "", format_preset: str = "1080p") -> bool:
        """Create new project"""
        try:
            # Update metadata
            self.metadata.name = name
            self.metadata.description = description
            self.metadata.format = format_preset
            self.metadata.created_date = datetime.now().isoformat()
            
            # Set project file path
            project_file = location / f"{name}.rforge"
            
            # Save new project
            return self.save(project_file)
            
        except Exception as e:
            print(f"Error creating project: {e}")
            return False


class ProjectManager:
    """Manages recent projects and templates"""
    
    def __init__(self):
        self.recent_projects: List[str] = []
        self.max_recent = 10
        self._load_recent_projects()
        
    def _get_settings_path(self) -> Path:
        """Get path to settings file"""
        from PyQt6.QtCore import QStandardPaths
        app_data = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.AppDataLocation
        )
        return Path(app_data) / "reelforge_settings.json"
        
    def _load_recent_projects(self):
        """Load recent projects from settings"""
        try:
            settings_path = self._get_settings_path()
            if settings_path.exists():
                with open(settings_path, 'r') as f:
                    data = json.load(f)
                    self.recent_projects = data.get('recent_projects', [])
        except Exception:
            self.recent_projects = []
            
    def _save_recent_projects(self):
        """Save recent projects to settings"""
        try:
            settings_path = self._get_settings_path()
            settings_path.parent.mkdir(parents=True, exist_ok=True)
            
            data = {'recent_projects': self.recent_projects}
            with open(settings_path, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving recent projects: {e}")
            
    def add_recent_project(self, project_path: str):
        """Add project to recent list"""
        if project_path in self.recent_projects:
            self.recent_projects.remove(project_path)
            
        self.recent_projects.insert(0, project_path)
        self.recent_projects = self.recent_projects[:self.max_recent]
        self._save_recent_projects()
        
    def get_recent_projects(self) -> List[str]:
        """Get list of recent project paths that still exist"""
        existing_projects = []
        for path in self.recent_projects:
            if Path(path).exists():
                existing_projects.append(path)
                
        # Update list if some projects no longer exist
        if len(existing_projects) != len(self.recent_projects):
            self.recent_projects = existing_projects
            self._save_recent_projects()
            
        return existing_projects
        
    def clear_recent_projects(self):
        """Clear recent projects list"""
        self.recent_projects = []
        self._save_recent_projects()
        
    @staticmethod
    def get_project_templates() -> Dict[str, Dict[str, Any]]:
        """Get available project templates"""
        return {
            "Social Media - Square": {
                "format": "1080x1080",
                "fps": 30,
                "description": "Perfect for Instagram posts and stories"
            },
            "Social Media - Vertical": {
                "format": "1080x1920", 
                "fps": 30,
                "description": "Optimized for TikTok, Instagram Reels, YouTube Shorts"
            },
            "YouTube - Landscape": {
                "format": "1920x1080",
                "fps": 30,
                "description": "Standard YouTube video format"
            },
            "Custom": {
                "format": "1920x1080",
                "fps": 30,
                "description": "Custom project settings"
            }
        }
