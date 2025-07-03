"""
Project data models and management for ReelTune
Handles creation, loading, and saving of .rforge project files
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
import uuid
from core.plugins import PluginManager
from core.logging_config import log_info, log_error, log_warning, log_debug


@dataclass
class ReleaseEvent:
    """A scheduled content release event"""
    id: str
    date: str  # ISO format date string
    content_type: str  # "reel", "story", "post", "teaser", "tutorial"
    title: str
    description: str = ""
    assets: List[str] = field(default_factory=list)  # Asset IDs
    platforms: List[str] = field(default_factory=list)  # "instagram", "tiktok", "youtube"
    status: str = "planned"  # "planned", "ready", "published"
    duration_seconds: int = 30  # Target content duration
    hashtags: List[str] = field(default_factory=list)
    created_date: str = ""
    
    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.created_date:
            self.created_date = datetime.now().isoformat()


@dataclass
class TimelinePlan:
    """Timeline configuration and events for content planning"""
    start_date: str  # ISO format date string
    duration_weeks: int = 4  # Fixed to 4 weeks
    events: Dict[str, List[str]] = field(default_factory=dict)  # date_string -> [event_ids]
    current_week_offset: int = 0  # For navigation
    
    def __post_init__(self):
        if not self.start_date:
            # Default to current Monday
            today = datetime.now()
            monday = today - timedelta(days=today.weekday())
            self.start_date = monday.date().isoformat()


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
    
    # Timeline-specific metadata
    plugin_name: str = ""
    plugin_version: str = ""
    release_date: str = ""  # Plugin release date
    target_platforms: List[str] = field(default_factory=list)
    
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
    """Main project class for ReelForge - AI-focused content generation"""
    
    def __init__(self, metadata: Optional[ProjectMetadata] = None):
        self.metadata = metadata or ProjectMetadata(name="Untitled Project")
        self.assets: Dict[str, AssetReference] = {}
        self.project_file_path: Optional[Path] = None
        self._is_modified = False
        
        # Timeline components
        self.timeline_plan: Optional[TimelinePlan] = None
        self.release_events: Dict[str, ReleaseEvent] = {}  # event_id -> event
        
        # Plugin management - simplified for one plugin per project
        self.plugin_manager = PluginManager()
        self.current_plugin: Optional[str] = None  # Name of current plugin
        
        # AI-focused features
        self.global_prompt: str = ""  # Global AI prompt for content generation
        self.moodboard_path: Optional[str] = None  # Path to moodboard image (relative to project)
        
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
    
    # Timeline Management Methods
    def initialize_timeline(self, start_date: Optional[datetime] = None, duration_weeks: int = 4):
        """Initialize timeline plan"""
        if start_date is None:
            # Default to current Monday
            today = datetime.now()
            start_date = today - timedelta(days=today.weekday())
            
        self.timeline_plan = TimelinePlan(
            start_date=start_date.date().isoformat(),
            duration_weeks=duration_weeks
        )
        self.mark_modified()
    
    def add_release_event(self, event: ReleaseEvent) -> bool:
        """Add a release event to the project"""
        try:
            if not self.timeline_plan:
                self.initialize_timeline()
                
            # Store the event
            self.release_events[event.id] = event
            
            # Add to timeline plan events for the specific date
            date_str = event.date
            if date_str not in self.timeline_plan.events:
                self.timeline_plan.events[date_str] = []
                
            if event.id not in self.timeline_plan.events[date_str]:
                self.timeline_plan.events[date_str].append(event.id)
                
            self.mark_modified()
            return True
            
        except Exception as e:
            log_error(f"Error adding release event: {e}")
            return False
    
    def remove_release_event(self, event_id: str) -> bool:
        """Remove a release event"""
        try:
            if event_id not in self.release_events:
                log_warning(f"Event {event_id} not found in release_events")
                return False
                
            event = self.release_events[event_id]
            log_info(f"Removing event: {event.title} (ID: {event_id}) from date: {event.date}")
            
            # Remove from timeline plan
            if self.timeline_plan and event.date in self.timeline_plan.events:
                if event_id in self.timeline_plan.events[event.date]:
                    self.timeline_plan.events[event.date].remove(event_id)
                    log_debug(f"Removed event from timeline_plan.events[{event.date}]")
                    
                # Clean up empty date entries
                if not self.timeline_plan.events[event.date]:
                    del self.timeline_plan.events[event.date]
                    log_debug(f"Cleaned up empty date entry: {event.date}")
            else:
                log_warning(f"Event date {event.date} not found in timeline_plan.events")
                    
            # Remove from events dict
            del self.release_events[event_id]
            log_debug(f"Event {event_id} removed from release_events")
            
            self.mark_modified()
            return True
            
        except Exception as e:
            log_error(f"Error removing release event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def update_release_event(self, event: ReleaseEvent) -> bool:
        """Update an existing release event"""
        try:
            if event.id not in self.release_events:
                log_warning(f"Event {event.id} not found for updating")
                return False
                
            old_event = self.release_events[event.id]
            old_date = old_event.date
            new_date = event.date
            
            log_info(f"Updating event: {event.title} (ID: {event.id})")
            log_debug(f"Date change: {old_date} -> {new_date}")
            
            # If date changed, update timeline plan
            if old_date != new_date and self.timeline_plan:
                # Remove from old date
                if old_date in self.timeline_plan.events and event.id in self.timeline_plan.events[old_date]:
                    self.timeline_plan.events[old_date].remove(event.id)
                    if not self.timeline_plan.events[old_date]:
                        del self.timeline_plan.events[old_date]
                        
                # Add to new date
                if new_date not in self.timeline_plan.events:
                    self.timeline_plan.events[new_date] = []
                if event.id not in self.timeline_plan.events[new_date]:
                    self.timeline_plan.events[new_date].append(event.id)
            
            # Update the event data
            self.release_events[event.id] = event
            
            self.mark_modified()
            log_debug(f"Event {event.id} updated successfully")
            return True
            
        except Exception as e:
            log_error(f"Error updating release event: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_events_for_date(self, date) -> List[ReleaseEvent]:
        """Get all events scheduled for a specific date"""
        try:
            # Convert datetime to date string for comparison
            if hasattr(date, 'date'):
                date_str = date.date().isoformat()
            elif hasattr(date, 'isoformat'):
                date_str = date.isoformat()
            else:
                date_str = str(date)
            
            # Find events matching the date
            matching_events = []
            for event in self.release_events.values():
                event_date_str = event.date
                if event_date_str == date_str:
                    matching_events.append(event)
            
            return matching_events
            
        except Exception as e:
            log_error(f"Error getting events for date: {e}")
            return []

    # Plugin Management Methods
    def import_plugin_info(self, adsp_file_path: Path) -> bool:
        """Import plugin information from .adsp file"""
        try:
            plugin_info = self.plugin_manager.import_adsp_file(adsp_file_path)
            if plugin_info:
                self.current_plugin = plugin_info.name
                self.mark_modified()
                return True
            return False
        except Exception as e:
            log_error(f"Error importing plugin info: {e}")
            return False
    
    def set_current_plugin(self, plugin_name: str) -> bool:
        """Set the current plugin for content generation"""
        if self.plugin_manager.get_plugin(plugin_name):
            self.current_plugin = plugin_name
            self.mark_modified()
            return True
        return False
    
    def get_current_plugin_info(self):
        """Get current plugin information"""
        if self.current_plugin:
            return self.plugin_manager.get_plugin(self.current_plugin)
        return None
    
    def get_content_generation_data(self) -> Optional[Dict[str, Any]]:
        """Get all data needed for AI content generation"""
        if not self.current_plugin:
            return None
            
        plugin_data = self.plugin_manager.get_content_generation_data(self.current_plugin)
        if not plugin_data:
            return None
            
        return {
            "plugin": plugin_data,
            "project": {
                "name": self.metadata.name,
                "description": self.metadata.description,
                "format": self.metadata.format,
                "target_platforms": self.metadata.target_platforms,
                "assets": [asdict(asset) for asset in self.get_all_assets()],
                "timeline_events": [asdict(event) for event in self.release_events.values()]
            },
            "generation_context": {
                "total_assets": len(self.assets),
                "scheduled_events": len(self.release_events),
                "timeline_duration": self.timeline_plan.duration_weeks if self.timeline_plan else 1,
                "project_created": self.metadata.created_date
            }
        }
    
    def get_ai_generation_data(self) -> Dict[str, Any]:
        """Get complete data package for AI content generation"""
        # Get plugin info
        plugin_info = self.get_current_plugin_info()
        plugin_data = None
        if plugin_info:
            plugin_data = {
                "name": plugin_info.name,
                "tagline": plugin_info.tagline,
                "description": plugin_info.short_description,
                "unique": plugin_info.unique,
                "personality": plugin_info.personality,
                "categories": plugin_info.category,
                "use_cases": plugin_info.intended_use
            }
        
        # Get all assets (AI will select appropriate ones)
        assets_data = []
        for asset in self.get_all_assets():
            assets_data.append({
                "id": asset.id,
                "name": asset.name,
                "type": asset.file_type,
                "path": asset.file_path
            })
        
        # Get all scheduled events with their prompts
        events_data = []
        for event in self.release_events.values():
            events_data.append({
                "date": event.date,
                "content_type": event.content_type,
                "title": event.title,
                "prompt": event.description,  # The AI prompt/description
                "platforms": event.platforms
            })
        
        return {
            "plugin": plugin_data,
            "global_prompt": self.global_prompt,
            "moodboard_path": self.moodboard_path,
            "assets": assets_data,
            "scheduled_content": events_data,
            "project_info": {
                "name": self.metadata.name,
                "format": self.metadata.format
            }
        }

    def import_asset(self, file_path: str) -> Optional[str]:
        """Import an asset from file path and return asset ID"""
        try:
            path = Path(file_path)
            if not path.exists():
                return None
                
            # Determine file type
            extension = path.suffix.lower()
            if extension in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']:
                file_type = 'image'
            elif extension in ['.mp4', '.mov', '.avi', '.mkv', '.webm']:
                file_type = 'video'
            elif extension in ['.mp3', '.wav', '.aac', '.m4a', '.flac']:
                file_type = 'audio'
            else:
                file_type = 'other'
                
            # Create asset reference
            asset_id = str(uuid.uuid4())[:8]
            asset = AssetReference(
                id=asset_id,
                name=path.name,
                file_path=str(path),
                file_type=file_type,
                file_size=path.stat().st_size if path.exists() else None
            )
            
            # Add to project
            if self.add_asset(asset):
                return asset_id
            return None
            
        except Exception as e:
            log_error(f"Error importing asset: {e}")
            return None

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
            "timeline_plan": asdict(self.timeline_plan) if self.timeline_plan else None,
            "release_events": {k: asdict(v) for k, v in self.release_events.items()},
            "plugin_data": self.plugin_manager.to_dict(),
            "current_plugin": self.current_plugin,
            "global_prompt": self.global_prompt,
            "moodboard_path": self.moodboard_path,
            "version": "1.3"  # Updated version for AI features
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
        
        # Load timeline plan
        if "timeline_plan" in data and data["timeline_plan"]:
            project.timeline_plan = TimelinePlan(**data["timeline_plan"])
            
        # Load release events
        if "release_events" in data:
            for event_id, event_data in data["release_events"].items():
                event = ReleaseEvent(**event_data)
                project.release_events[event_id] = event
        
        # Load plugin data
        if "plugin_data" in data:
            project.plugin_manager.from_dict(data["plugin_data"])
            
        # Load current plugin
        if "current_plugin" in data:
            project.current_plugin = data["current_plugin"]
            
        # Load AI features
        if "global_prompt" in data:
            project.global_prompt = data["global_prompt"]
            
        if "moodboard_path" in data:
            project.moodboard_path = data["moodboard_path"]
                
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
            log_error(f"Error saving project: {e}")
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
            log_error(f"Error loading project: {e}")
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
            log_error(f"Error creating project: {e}")
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
            log_error(f"Error saving recent projects: {e}")
            
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
