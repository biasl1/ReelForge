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
from core.content_generation import ReelTuneJSONEncoder
from core.xplainpack import XplainPackManager
import enum

def convert_enums(obj):
    """Recursively convert all Enum objects and Qt objects to their serializable values for JSON serialization"""
    if isinstance(obj, dict):
        return {k: convert_enums(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_enums(i) for i in obj]
    elif isinstance(obj, tuple):
        return tuple(convert_enums(i) for i in obj)
    elif isinstance(obj, set):
        return {convert_enums(i) for i in obj}
    elif isinstance(obj, enum.Enum):
        return obj.value
    elif hasattr(obj, '__class__') and 'PyQt6' in str(obj.__class__):
        # Handle Qt objects that might not be JSON serializable
        if hasattr(obj, 'toRect'):  # QRect
            rect = obj.toRect()
            return [rect.x(), rect.y(), rect.width(), rect.height()]
        elif hasattr(obj, 'width') and hasattr(obj, 'height') and not hasattr(obj, 'x'):  # QSize
            return [obj.width(), obj.height()]
        elif hasattr(obj, 'x') and hasattr(obj, 'y'):  # QPoint, QRect, etc.
            if hasattr(obj, 'width') and hasattr(obj, 'height'):  # QRect
                return [obj.x(), obj.y(), obj.width(), obj.height()]
            else:  # QPoint
                return [obj.x(), obj.y()]
        elif hasattr(obj, 'red') and hasattr(obj, 'green') and hasattr(obj, 'blue'):  # QColor
            return [obj.red(), obj.green(), obj.blue(), obj.alpha()]
        else:
            # For other Qt objects, try to convert to string
            return str(obj)
    elif isinstance(obj, datetime):
        # Convert datetime objects to ISO format strings
        return obj.isoformat()
    else:
        return obj

@dataclass
class ReleaseEvent:
    """A scheduled content release event - now supports flexible VIDEO/PICTURE types"""
    id: str
    date: str  # ISO format date string
    content_type: str  # "video" or "picture" 
    title: str
    description: str = ""
    assets: List[str] = field(default_factory=list)  # Asset IDs
    platforms: List[str] = field(default_factory=list)  # "instagram", "tiktok", "youtube"
    status: str = "planned"  # "planned", "ready", "published"
    duration_seconds: int = 30  # Target content duration (for videos)
    hashtags: List[str] = field(default_factory=list)
    created_date: str = ""
    session_id: Optional[str] = None  # XplainPack session ID for synchronized content
    
    # NEW: Per-event template configuration
    template_config: Dict[str, Any] = field(default_factory=dict)  # Frame layouts specific to this event
    frame_count: int = 1  # Number of frames for this event (videos can have multiple frames)

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())[:8]
        if not self.created_date:
            self.created_date = datetime.now().isoformat()
        
        # Set sensible defaults based on content type
        if self.content_type == "picture":
            self.frame_count = 1  # Pictures always have 1 frame
            self.duration_seconds = 0  # Pictures don't have duration
        elif self.content_type == "video" and not self.template_config:
            self.frame_count = 1  # Default to 1 frame for videos (user can add more)


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
    description: str = ""  # User description for AI context
    folder: str = ""  # Folder organization (e.g., "intro", "demos", "outro")

    def __post_init__(self):
        if not self.import_date:
            self.import_date = datetime.now().isoformat()


class ReelForgeProject:
    """Main project class for ReelTune - AI-focused content generation"""

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
        self.simple_templates: Dict[str, Any] = {}  # Template settings for AI generation
        
        # XplainPack sessions for enhanced AI content generation
        self.xplainpack_manager: Optional[XplainPackManager] = None

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

    def _initialize_xplainpack_manager(self):
        """Initialize XplainPack manager when project directory is available"""
        if self.project_directory and not self.xplainpack_manager:
            self.xplainpack_manager = XplainPackManager(self.project_directory)
            log_info("Initialized XplainPack manager")
        elif not self.project_directory:
            log_warning("Cannot initialize XplainPackManager: no project directory")
        else:
            log_debug("XplainPackManager already initialized")

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

    def get_ai_generation_data(self, template_editor=None) -> Dict[str, Any]:
        """Get complete data package for AI content generation"""
        # Get plugin info
        plugin_info = self.get_current_plugin_info()
        plugin_data = None
        raw_adsp_data = None
        
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
            
            # Get raw .adsp data if available
            if plugin_info.adsp_file_path and os.path.exists(plugin_info.adsp_file_path):
                try:
                    with open(plugin_info.adsp_file_path, 'r') as f:
                        raw_adsp_data = json.load(f)
                except Exception as e:
                    log_error(f"Failed to load raw .adsp data: {e}")
                    raw_adsp_data = None

        # Get all assets (AI will select appropriate ones)
        assets_data = []
        for asset in self.get_all_assets():
            assets_data.append({
                "id": asset.id,
                "name": asset.name,
                "type": asset.file_type,
                "path": asset.file_path,
                "description": asset.description,
                "folder": asset.folder
            })

        # Get all scheduled events with their prompts
        events_data = []
        for event in self.release_events.values():
            event_data = {
                "date": event.date,
                "content_type": event.content_type,
                "title": event.title,
                "prompt": event.description,  # The AI prompt/description
                "platforms": event.platforms,
                "template_key": event.content_type  # Template reference
            }
            
            # Add session reference if event is linked to an XplainPack
            if event.session_id:
                session = self.get_xplainpack_session(event.session_id)
                if session:
                    event_data["session_id"] = event.session_id
                
            events_data.append(event_data)

        # Get content generation templates from per-event configurations
        templates_data = {}
        
        # Extract template data from events (per-event system)
        for event in self.release_events.values():
            # Use event ID as the template key for per-event templates
            event_key = f"{event.content_type}_{event.id}"
            # Clean and convert template_config to ensure only essential properties
            cleaned_template_config = self._clean_template_config_for_export(event.template_config)
            serializable_template_config = convert_enums(cleaned_template_config)
            templates_data[event_key] = {
                "event_id": event.id,
                "event_title": event.title,
                "content_type": event.content_type,
                "frame_count": event.frame_count,
                "template_config": serializable_template_config,
                "aspect_ratio": 9/16 if event.content_type == 'video' else 1.0
            }
            log_info(f"Exported template for event {event.title} (ID: {event.id})")
        # If no events have templates, provide defaults
        if not templates_data:
            templates_data = {
                "video": {
                    "frame_count": 3,
                    "template_config": {},
                    "aspect_ratio": 9/16
                },
                "picture": {
                    "frame_count": 1,
                    "template_config": {},
                    "aspect_ratio": 1.0
                }
            }

        # Map calendar content types to template names (modernized)
        content_type_mapping = {
            "video": "video",
            "picture": "picture"
        }
        
        # Update events data with consistent content types
        for event in events_data:
            original_type = event["content_type"]
            event["template_key"] = content_type_mapping.get(original_type, original_type)

        return {
            "plugin": plugin_data,
            "raw_adsp_data": raw_adsp_data,  # ALL the .adsp metadata
            "global_prompt": self.global_prompt,
            "xplainpack_sessions": [session.to_dict() for session in (self.xplainpack_manager.get_all_sessions() if self.xplainpack_manager else [])],
            "assets": assets_data,
            "scheduled_content": events_data,
            "content_generation": {
                "templates": templates_data
            }
        }


        
    def export_ai_data_to_json(self, file_path: str, template_editor=None) -> bool:
        """Export AI generation data to a JSON file"""
        try:
            log_info("Starting AI generation data export...")
            ai_data = self.get_ai_generation_data(template_editor=template_editor)
            log_info("AI generation data retrieved successfully")
            
            # Inspect and fix templates data structure before conversion
            if 'content_generation' in ai_data and 'templates' in ai_data['content_generation']:
                templates = ai_data['content_generation']['templates']
                log_info(f"Inspecting templates data: {len(templates)} templates found")
                
                # Check each content type template
                for content_type, template_data in list(templates.items()):
                    if not isinstance(template_data, dict):
                        log_error(f"Template data for {content_type} is not a dict! Type: {type(template_data)}")
                        # Remove corrupted template
                        del templates[content_type]
                        continue
                    
                    # For video content, check frames structure
                    if template_data.get('is_video_content') and 'frames' in template_data:
                        frames = template_data['frames']
                        if not isinstance(frames, dict):
                            log_error(f"Frames for {content_type} is not a dict! Type: {type(frames)}")
                            # Try to fix frames if it's a list
                            if isinstance(frames, list):
                                log_error(f"Converting frames list to dict for {content_type}")
                                frames_dict = {}
                                for i, item in enumerate(frames):
                                    frames_dict[f"frame_{i}"] = item
                                template_data['frames'] = frames_dict
            
            # Convert any remaining enums to strings for safety
            log_info("Converting data for JSON serialization...")
            converted_data = convert_enums(ai_data)
            log_info("Data conversion completed")
            
            # Final check for dictionary structure integrity
            def validate_dict_structure(obj, path="root"):
                """Validate that objects that should be dicts are actually dicts"""
                if isinstance(obj, dict):
                    for key, value in obj.items():
                        validate_dict_structure(value, f"{path}.{key}")
                elif isinstance(obj, list):
                    for i, item in enumerate(obj):
                        validate_dict_structure(item, f"{path}[{i}]")
                
                # Only check specific critical paths that must be dicts
                critical_dict_paths = [
                    '.frames',
                    '.elements',
                    'canvas_config',
                    'settings'
                ]
                
                # Check if this is a critical path that must be a dict
                is_critical_path = False
                for critical_path in critical_dict_paths:
                    if path.endswith(critical_path):
                        is_critical_path = True
                        break
                
                # For critical paths, ensure we have a dictionary
                if is_critical_path and not isinstance(obj, dict) and obj is not None:
                    log_error(f"CRITICAL ERROR: Expected dict at {path} but got {type(obj)}")
            
            validate_dict_structure(converted_data)
            log_info("Validated data structure integrity")
            
            with open(file_path, 'w') as f:
                json.dump(converted_data, f, indent=2)
            log_info(f"AI generation data exported to {file_path}")
            
            # Also export template config to a separate file
            config_path = file_path.replace('.json', '_config.json')
            self.export_template_config_to_json(config_path)
            
            return True
        except Exception as e:
            log_error(f"Failed to export AI generation data: {e}")
            log_error(f"Error type: {type(e)}")
            import traceback
            error_traceback = traceback.format_exc()
            log_error(f"Full traceback: {error_traceback}")
            
            # Additional debugging for the specific list/get error
            if "'list' object has no attribute 'get'" in str(e):
                log_error("DETECTED: 'list' object has no attribute 'get' error!")
                log_error("This indicates that somewhere in the export process, a list is being treated as a dict")
                log_error("Check the frame data structures and element data structures for corruption")
                
                # Try to pinpoint where in the stack trace this occurred
                trace_lines = error_traceback.split('\n')
                for line in trace_lines:
                    if 'get' in line and '.py' in line:
                        log_error(f"Potential error location: {line.strip()}")
            
            return False
            
    def export_template_config_to_json(self, file_path: str) -> bool:
        """Export the template config (simple_templates) to a JSON file"""
        try:
            config_data = getattr(self, 'simple_templates', {})
            config_data = convert_enums(config_data)
            with open(file_path, 'w') as f:
                json.dump(config_data, f, indent=2)
            log_info(f"Template config exported to {file_path}")
            return True
        except Exception as e:
            log_error(f"Failed to export template config: {e}")
            import traceback
            traceback.print_exc()
            return False

    def _find_config_mode_in_data(self, data, path="root"):
        """Debug helper to find ConfigMode enums in complex data structures"""
        import enum
        if isinstance(data, dict):
            for k, v in data.items():
                if isinstance(v, enum.Enum) and v.__class__.__name__ == "ConfigMode":
                    log_debug(f"Found ConfigMode at {path}.{k}: {v}")
                else:
                    self._find_config_mode_in_data(v, f"{path}.{k}")
        elif isinstance(data, list):
            for i, item in enumerate(data):
                self._find_config_mode_in_data(item, f"{path}[{i}]")
                
    def _debug_find_non_serializable(self, data):
        """Debug helper to find non-serializable objects"""
        if isinstance(data, dict):
            for k, v in data.items():
                try:
                    json.dumps({k: v})
                except Exception as e:
                    log_debug(f"Non-serializable at key '{k}': {e}")
                    log_debug(f"Type: {type(v)}")
                    if hasattr(v, '__dict__'):
                        log_debug(f"Attributes: {dir(v)}")
                    self._debug_find_non_serializable(v)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                try:
                    json.dumps([item])
                except Exception as e:
                    log_debug(f"Non-serializable at index {i}: {e}")
                    self._debug_find_non_serializable(item)

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

    def update_asset_description(self, asset_id: str, description: str) -> bool:
        """Update asset description for AI context"""
        if asset_id in self.assets:
            self.assets[asset_id].description = description
            self.mark_modified()
            return True
        return False

    def update_asset_folder(self, asset_id: str, folder: str) -> bool:
        """Update asset folder for organization"""
        if asset_id in self.assets:
            self.assets[asset_id].folder = folder
            self.mark_modified()
            return True
        return False

    def delete_asset(self, asset_id: str) -> bool:
        """Delete an asset from the project"""
        try:
            if asset_id not in self.assets:
                return False

            asset = self.assets[asset_id]

            # Remove from all events
            for event in self.release_events.values():
                if asset_id in event.assets:
                    event.assets.remove(asset_id)

            # Remove asset file if it exists in project directory
            if self.project_file_path:
                project_dir = self.project_file_path.parent
                asset_path = project_dir / asset.file_path
                if asset_path.exists():
                    asset_path.unlink()

            # Remove from assets dict
            del self.assets[asset_id]
            self.mark_modified()
            return True

        except Exception as e:
            log_error(f"Error deleting asset {asset_id}: {e}")
            return False

    def get_asset_folders(self) -> List[str]:
        """Get list of all asset folders for organization"""
        folders = set()
        for asset in self.assets.values():
            if asset.folder:
                folders.add(asset.folder)
        return sorted(list(folders))

    def get_assets_in_folder(self, folder: str) -> List[AssetReference]:
        """Get all assets in a specific folder"""
        return [asset for asset in self.assets.values() if asset.folder == folder]

    def get_assets_without_folder(self) -> List[AssetReference]:
        """Get all assets not in any folder"""
        return [asset for asset in self.assets.values() if not asset.folder]

    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary for JSON serialization"""
        project_dict = {
            "metadata": asdict(self.metadata),
            "assets": {k: asdict(v) for k, v in self.assets.items()},
            "timeline_plan": asdict(self.timeline_plan) if self.timeline_plan else None,
            "release_events": {k: asdict(v) for k, v in self.release_events.items()},
            "plugin_data": self.plugin_manager.to_dict(),
            "current_plugin": self.current_plugin,
            "global_prompt": self.global_prompt,
            "moodboard_path": self.moodboard_path,
            "simple_templates": getattr(self, 'simple_templates', {}),
            "xplainpack_sessions": self.xplainpack_manager.to_dict() if self.xplainpack_manager else {},
            "version": "1.4"  # Updated version for XplainPack features
        }
        
        # Save template editor settings if available
        if hasattr(self, 'template_editor_settings'):
            project_dict["template_editor_settings"] = self.template_editor_settings
            
        return project_dict

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
            
        # Load template settings
        if "simple_templates" in data:
            project.simple_templates = data["simple_templates"]
            
        # Load XplainPack sessions - defer this until after project_file_path is set
        project._pending_xplainpack_sessions = data.get("xplainpack_sessions", {})
            
        # Load template editor settings
        if "template_editor_settings" in data:
            project.template_editor_settings = data["template_editor_settings"]

        project._is_modified = False
        return project

    def save(self, file_path: Optional[Path] = None) -> bool:
        """Save project to file"""
        try:
            target_path = file_path or self.project_file_path
            if not target_path:
                raise ValueError("No file path specified")

            # Convert string to Path if needed
            if isinstance(target_path, str):
                target_path = Path(target_path)

            # Ensure .rforge extension
            if target_path.suffix.lower() != '.rforge':
                target_path = target_path.with_suffix('.rforge')

            # Create directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Initialize XplainPackManager if not already done
            if not self.xplainpack_manager:
                self._initialize_xplainpack_manager()

            log_info(f"Saving project to: {target_path}")
            log_debug(f"Project data keys: {list(self.to_dict().keys())}")

            # Save project data
            with open(target_path, 'w', encoding='utf-8') as f:
                project_data = convert_enums(self.to_dict())
                json.dump(project_data, f, indent=2, ensure_ascii=False)

            self.project_file_path = target_path
            self._is_modified = False

            log_info(f"Project saved successfully to: {target_path}")
            return True

        except Exception as e:
            log_error(f"Error saving project: {e}")
            import traceback
            traceback.print_exc()
            return False

    @classmethod
    def load(cls, file_path) -> Optional['ReelForgeProject']:
        """Load project from file"""
        try:
            # Convert string to Path if needed
            if isinstance(file_path, str):
                file_path = Path(file_path)

            log_info(f"Loading project from: {file_path}")
            
            if not file_path.exists():
                log_error(f"File does not exist: {file_path}")
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            log_debug(f"Loaded project data keys: {list(data.keys())}")

            project = cls.from_dict(data)
            project.project_file_path = file_path
            project._is_modified = False

            # Initialize XplainPackManager now that we have the project directory
            project._initialize_xplainpack_manager()
            
            # Load pending XplainPack sessions now that manager is initialized
            if hasattr(project, '_pending_xplainpack_sessions') and project._pending_xplainpack_sessions:
                if project.xplainpack_manager:
                    log_info(f"Loading {len(project._pending_xplainpack_sessions)} XplainPack sessions")
                    project.xplainpack_manager.from_dict(project._pending_xplainpack_sessions)
                    log_info(f"Loaded {len(project.xplainpack_manager.sessions)} sessions into manager")
                    delattr(project, '_pending_xplainpack_sessions')  # Clean up temporary attribute
                else:
                    log_warning("XplainPackManager not available for loading sessions")

            log_info(f"Project loaded successfully: {project.project_name}")
            return project

        except Exception as e:
            log_error(f"Error loading project: {e}")
            import traceback
            traceback.print_exc()
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

    def _export_practical_template(self, template, template_name: str) -> Dict[str, Any]:
        """Export template as practical layout information for AI"""
        content_type = getattr(template, 'content_type', 'unknown')
        
        # Get standard dimensions for content type
        dimensions = self._get_standard_dimensions(content_type)
        
        # Extract REAL template settings
        subtitle_config = template.subtitle.to_dict() if hasattr(template, 'subtitle') else {}
        overlay_config = template.overlay.to_dict() if hasattr(template, 'overlay') else {}
        timing_config = template.timing.to_dict() if hasattr(template, 'timing') else {}
        custom_config = {k: v.to_dict() for k, v in template.custom_parameters.items()} if hasattr(template, 'custom_parameters') else {}
        
        return {
            "name": template_name,
            "content_type": content_type,
            "platform": self._get_platform_for_content_type(content_type),
            "dimensions": dimensions,
            "subtitle_settings": subtitle_config,
            "overlay_settings": overlay_config,
            "timing_settings": timing_config,
            "custom_settings": custom_config,
            "duration": timing_config.get("duration", {}).get("value", self._get_content_duration(content_type))
        }
    
    def _export_practical_layout(self, content_type: str) -> Dict[str, Any]:
        """Export SIMPLIFIED practical layout information for VIDEO/PICTURE content types"""
        return {
            "content_type": content_type,
            "is_video_content": content_type == 'video',
            "layout": {
                "title": {"position": {"y": 100}},      # Default title position
                "subtitle": {"position": {"y": 400}},   # Default subtitle position
                "pip_video": {"visible": True}          # Default PiP visibility
            }
        }
    
    def _convert_ui_layout_to_export_format(self, ui_layout_data: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Convert UI template editor layout data to SIMPLIFIED export format with only essential fields"""
        # Ensure ui_layout_data is a dict
        if not isinstance(ui_layout_data, dict):
            log_error(f"ERROR: ui_layout_data is not a dict, it's a {type(ui_layout_data)}")
            ui_layout_data = {}
            
        canvas_config = ui_layout_data.get('canvas_config', {})
        
        # Ensure canvas_config is a dict
        if not isinstance(canvas_config, dict):
            log_error(f"ERROR: canvas_config is not a dict, it's a {type(canvas_config)}")
            canvas_config = {}
            
        # Check if this is a video content type with frames
        frames_data = canvas_config.get('frames', {})
        
        # Ensure frames_data is a dict, not a list
        if isinstance(frames_data, list):
            log_error(f"ERROR: frames_data is a list, converting to dict")
            frames_dict = {}
            for i, item in enumerate(frames_data):
                frames_dict[str(i)] = {'elements': {}, 'frame_description': f'Recovered frame {i}'}
            frames_data = frames_dict
        elif not isinstance(frames_data, dict):
            log_error(f"ERROR: frames_data is not a dict, it's a {type(frames_data)}")
            frames_data = {}
            
        is_video_content = content_type == 'video'
        
        if is_video_content and frames_data:
            # For video content types, export SIMPLIFIED frame structure
            frame_sections = {}
            
            for frame_index, frame_data in frames_data.items():
                # Ensure frame_data is a dict
                if not isinstance(frame_data, dict):
                    log_error(f"Frame data corruption detected! Frame {frame_index} is {type(frame_data)}, expected dict")
                    frame_data = {
                        'elements': {},
                        'frame_description': f'Recovered frame {frame_index}'
                    }
                
                # Get elements safely
                frame_elements = frame_data.get('elements', {})
                if not isinstance(frame_elements, dict):
                    log_error(f"Frame elements is not a dict! Type: {type(frame_elements)}")
                    frame_elements = {}
                
                frame_description = frame_data.get('frame_description', f'Frame {frame_index}')
                
                # Extract ONLY the essential layout info that AI actually uses
                title_y = self._extract_title_y_position(frame_elements)
                subtitle_y = self._extract_subtitle_y_position(frame_elements)
                pip_visible = self._extract_pip_visibility(frame_elements)
                title_size = self._extract_title_font_size(frame_elements)
                subtitle_size = self._extract_subtitle_font_size(frame_elements)
                
                frame_sections[f"frame_{frame_index}"] = {
                    "frame_description": frame_description,
                    "layout": {
                        "title": {"position": {"y": title_y}, "font_size": title_size},
                        "subtitle": {"position": {"y": subtitle_y}, "font_size": subtitle_size},
                        "pip_video": {"visible": pip_visible}
                    }
                }
            
            # Return SIMPLIFIED structure with only essential fields
            return {
                "content_type": content_type,
                "is_video_content": True,
                "total_frames": len(frames_data),
                "frames": frame_sections
            }
        else:
            # For static content types, export SIMPLIFIED single layout
            elements = canvas_config.get('elements', {})
            title_y = self._extract_title_y_position(elements)
            subtitle_y = self._extract_subtitle_y_position(elements)
            pip_visible = self._extract_pip_visibility(elements)
            title_size = self._extract_title_font_size(elements)
            subtitle_size = self._extract_subtitle_font_size(elements)
            
            return {
                "content_type": content_type,
                "is_video_content": False,
                "layout": {
                    "title": {"position": {"y": title_y}, "font_size": title_size},
                    "subtitle": {"position": {"y": subtitle_y}, "font_size": subtitle_size},
                    "pip_video": {"visible": pip_visible}
                }
            }
    

    def _extract_title_y_position(self, elements: dict) -> str:
        """Extract title position preset (top, center, bottom) from elements"""
        if 'title' in elements:
            element = elements['title']
            if 'position_preset' in element:
                return element['position_preset']
        return "top"

    def _extract_subtitle_y_position(self, elements: dict) -> str:
        """Extract subtitle position preset (top, center, bottom) from elements"""
        if 'subtitle' in elements:
            element = elements['subtitle']
            if 'position_preset' in element:
                return element['position_preset']
        return "bottom"

    def _extract_pip_visibility(self, elements: dict) -> bool:
        """Extract PiP visibility from elements"""
        if 'pip' in elements:
            element = elements['pip']
            return element.get('visible', True)
        return False

    def _extract_title_font_size(self, elements: dict) -> int:
        """Extract title font size from elements"""
        if 'title' in elements:
            element = elements['title']
            return element.get('font_size', element.get('size', 24))
        return 24

    def _extract_subtitle_font_size(self, elements: dict) -> int:
        """Extract subtitle font size from elements"""
        if 'subtitle' in elements:
            element = elements['subtitle']
            return element.get('font_size', element.get('size', 18))
        return 18
    

    def save_template_editor_settings(self, template_editor):
        """Save template editor settings for current event"""
        if not template_editor.current_event_id:
            log_warning("No current event selected in template editor")
            return False
        
        # Save current frame
        template_editor._save_current_frame()
        
        log_info(f"Saved template editor settings for event {template_editor.current_event_id}")
        return True

    def load_template_editor_settings(self, template_editor):
        """Load template editor settings - compatibility method"""
        # This method is called by MainWindow for compatibility
        # The actual loading is now handled by the per-event system
        log_info("Template editor settings loading - using per-event system")
        return True

    # XplainPack Management Methods
    def get_all_xplainpack_sessions(self) -> List[Dict[str, Any]]:
        """Get all XplainPack sessions"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            return [session.to_dict() for session in self.xplainpack_manager.get_all_sessions()]
        return []

    def get_xplainpack_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get XplainPack session by ID"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            session = self.xplainpack_manager.get_session(session_id)
            return session.to_dict() if session else None
        return None

    def update_xplainpack_session(self, session_id: str, updated_data: Dict[str, Any]) -> bool:
        """Update XplainPack session data"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            return self.xplainpack_manager.update_session(session_id, **updated_data)
        return False

    def import_xplainpack(self, pack_path: Path) -> Optional[str]:
        """Import an XplainPack and return the session ID"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            session_id = self.xplainpack_manager.import_xplainpack(pack_path)
            if session_id:
                self.mark_modified()
                return session_id
        return None

    def add_xplainpack_session(self, session_data: Dict[str, Any]) -> bool:
        """Add XplainPack session data (for backward compatibility)"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            # Convert dict to XplainPackSession and add
            from core.xplainpack import XplainPackSession
            try:
                session = XplainPackSession.from_dict(session_data)
                self.xplainpack_manager.sessions[session.id] = session
                self.mark_modified()
                return True
            except Exception as e:
                log_error(f"Error adding XplainPack session: {e}")
        return False

    def remove_xplainpack_session(self, session_id: str) -> bool:
        """Remove XplainPack session"""
        if not self.xplainpack_manager:
            self._initialize_xplainpack_manager()
        
        if self.xplainpack_manager:
            if self.xplainpack_manager.remove_session(session_id):
                self.mark_modified()
                return True
        return False

    # Event Template Management Methods (NEW ARCHITECTURE)
    def get_event_template_config(self, event_id: str) -> Dict[str, Any]:
        """Get template configuration for a specific event"""
        if event_id in self.release_events:
            return self.release_events[event_id].template_config
        return {}
    
    def set_event_template_config(self, event_id: str, config: Dict[str, Any]) -> bool:
        """Set template configuration for a specific event"""
        if event_id in self.release_events:
            self.release_events[event_id].template_config = config
            self.mark_modified()
            return True
        return False
    
    def get_event_frame_count(self, event_id: str) -> int:
        """Get number of frames for a specific event"""
        if event_id in self.release_events:
            return self.release_events[event_id].frame_count
        return 1
    
    def set_event_frame_count(self, event_id: str, frame_count: int) -> bool:
        """Set number of frames for a specific event"""
        if event_id in self.release_events:
            self.release_events[event_id].frame_count = max(1, frame_count)
            # Initialize frame data if needed
            if 'frame_data' not in self.release_events[event_id].template_config:
                self.release_events[event_id].template_config['frame_data'] = {}
            self.mark_modified()
            return True
        return False
    
    def get_event_frame_data(self, event_id: str, frame_index: int) -> Dict[str, Any]:
        """Get frame data for a specific event and frame"""
        if event_id in self.release_events:
            frame_data = self.release_events[event_id].template_config.get('frame_data', {})
            return frame_data.get(str(frame_index), {})
        return {}
    
    def set_event_frame_data(self, event_id: str, frame_index: int, frame_data: Dict[str, Any]) -> bool:
        """Set frame data for a specific event and frame"""
        if event_id in self.release_events:
            if 'frame_data' not in self.release_events[event_id].template_config:
                self.release_events[event_id].template_config['frame_data'] = {}
            self.release_events[event_id].template_config['frame_data'][str(frame_index)] = frame_data
            self.mark_modified()
            return True
        return False
    
    def create_event_with_template(self, date: str, content_type: str, title: str, 
                                 description: str = "", frame_count: int = None) -> str:
        """Create a new event with default template configuration"""
        # Determine default frame count based on content type
        if frame_count is None:
            frame_count = 1 if content_type == "picture" else 3
        
        # Create the event
        event = ReleaseEvent(
            id="",  # Will be auto-generated
            date=date,
            content_type=content_type,
            title=title,
            description=description,
            frame_count=frame_count,
            template_config={"frame_data": {}}
        )
        
        # Add to release events
        self.release_events[event.id] = event
        
        # Add to timeline
        if not self.timeline_plan:
            self.initialize_timeline()
        
        if date not in self.timeline_plan.events:
            self.timeline_plan.events[date] = []
        self.timeline_plan.events[date].append(event.id)
        
        self.mark_modified()
        log_info(f"Created {content_type} event: {title} ({event.id})")
        return event.id

    def _clean_template_config_for_export(self, template_config: dict) -> dict:
        """Clean template config to remove unnecessary properties for export."""
        if 'frame_data' not in template_config:
            return template_config
        
        frame_data = template_config['frame_data']
        cleaned_frame_data = {}
        
        for frame_key, frame_info in frame_data.items():
            if not isinstance(frame_info, dict):
                continue
                
            elements = frame_info.get('elements', {})
            cleaned_elements = {}
            
            for element_id, element_data in elements.items():
                if not isinstance(element_data, dict):
                    continue
                    
                # Only keep essential properties
                cleaned_element = {
                    'type': element_data.get('type', 'text'),
                    'content': element_data.get('content', ''),
                    'font_size': element_data.get('font_size', element_data.get('size', 12)),
                    'position_preset': element_data.get('position_preset', 'center'),
                    'visible': element_data.get('visible', True)
                }
                
                # Add PiP-specific properties
                if element_data.get('type') == 'pip':
                    cleaned_element['corner_radius'] = element_data.get('corner_radius', 0)
                
                cleaned_elements[element_id] = cleaned_element
            
            cleaned_frame_data[frame_key] = {
                'frame_index': frame_info.get('frame_index', 0),
                'frame_description': frame_info.get('frame_description', ''),
                'elements': cleaned_elements,
                'timestamp': frame_info.get('timestamp', datetime.now().isoformat())
            }
        
        return {
            'frame_data': cleaned_frame_data
        }

class ProjectManager:
    """Project management utilities for ReelTune"""
    
    def __init__(self):
        self.recent_projects_file = Path.home() / ".reeltune" / "recent_projects.json"
        self.templates_dir = Path.home() / ".reeltune" / "templates"
        self._ensure_directories()
    
    def _ensure_directories(self):
        """Ensure configuration directories exist"""
        self.recent_projects_file.parent.mkdir(parents=True, exist_ok=True)
        self.templates_dir.mkdir(parents=True, exist_ok=True)
    
    def get_recent_projects(self) -> List[str]:
        """Get list of recent project file paths"""
        try:
            if not self.recent_projects_file.exists():
                return []
            
            with open(self.recent_projects_file, 'r') as f:
                recent = json.load(f)
                
            # Filter out projects that no longer exist
            existing_projects = []
            for project_path in recent.get('projects', []):
                if Path(project_path).exists():
                    existing_projects.append(project_path)
            
            return existing_projects[:10]  # Limit to 10 most recent
            
        except Exception as e:
            log_error(f"Error loading recent projects: {e}")
            return []
    
    def add_recent_project(self, project_path: str):
        """Add a project to the recent projects list"""
        try:
            recent_projects = self.get_recent_projects()
            
            # Remove if already in list
            if project_path in recent_projects:
                recent_projects.remove(project_path)
            
            # Add to front
            recent_projects.insert(0, project_path)
            
            # Keep only 10 most recent
            recent_projects = recent_projects[:10]
            
            # Save back
            with open(self.recent_projects_file, 'w') as f:
                json.dump({'projects': recent_projects}, f, indent=2)
                
        except Exception as e:
            log_error(f"Error saving recent project: {e}")
    
    def get_project_templates(self) -> Dict[str, Dict[str, Any]]:
        """Get available project templates"""
        templates = {
            "Basic Project": {
                "name": "Basic Project",
                "description": "A basic ReelTune project with default settings",
                "template_id": "basic",
                "format": "1080x1920",
                "fps": 30
            },
            "Social Media Campaign": {
                "name": "Social Media Campaign", 
                "description": "Pre-configured for Instagram reels and stories",
                "template_id": "social_media",
                "format": "1080x1920",
                "fps": 30
            },
            "Tutorial Series": {
                "name": "Tutorial Series",
                "description": "Set up for educational content creation", 
                "template_id": "tutorial",
                "format": "1920x1080",
                "fps": 30
            }
        }
        return templates
