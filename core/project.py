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
import enum

def convert_enums(obj):
    """Recursively convert all Enum objects to their string values for JSON serialization"""
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
    else:
        return obj

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

    def get_ai_generation_data(self, template_editor=None) -> Dict[str, Any]:
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
                "path": asset.file_path,
                "description": asset.description,
                "folder": asset.folder
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

        # Get content generation templates - always export practical layout info for all content types
        templates_data = {}
        
        # First priority: Get REAL layout data from UI template editor
        if template_editor and hasattr(template_editor, 'export_template_data'):
            content_types_used = set()
            for event in events_data:
                content_types_used.add(event["content_type"])
            
            # Export actual UI layout data for each content type
            for content_type in content_types_used:
                # Get the current content type from template editor
                current_type = template_editor.get_content_type()
                
                # Only set content type if it's different to avoid resetting elements
                if current_type != content_type:
                    template_editor.set_content_type(content_type)
                    real_layout_data = template_editor.export_template_data()
                    # Restore original content type
                    template_editor.set_content_type(current_type)
                else:
                    real_layout_data = template_editor.export_template_data()
                
                # Convert to expected format
                templates_data[content_type] = self._convert_ui_layout_to_export_format(real_layout_data, content_type)
        
        # Second priority: Export from ContentGenerationManager if it exists
        elif hasattr(self, 'content_generation_manager') and self.content_generation_manager:
            # Export all content type templates with REAL settings
            content_types_used = set()
            for event in events_data:
                content_types_used.add(event["content_type"])
            
            # Export actual configured templates for each content type used
            for content_type in content_types_used:
                actual_template = self.content_generation_manager.get_content_template(content_type)
                templates_data[content_type] = self._export_practical_template(actual_template, content_type.replace("_", " ").title())
            
            # Export project-wide template if customized
            if self.content_generation_manager.project_wide_template:
                templates_data["project_wide_custom"] = self._export_practical_template(
                    self.content_generation_manager.project_wide_template, "project_wide_custom"
                )
            
            # Export event-specific templates (these override content-type defaults)
            for event_id, template in self.content_generation_manager.event_templates.items():
                templates_data[f"event_{event_id}_custom"] = self._export_practical_template(template, f"event_{event_id}_custom")
        else:
            # Fallback: export basic layout for content types if no ContentGenerationManager
            content_types_used = set()
            for event in events_data:
                content_types_used.add(event["content_type"])
            
            for content_type in content_types_used:
                templates_data[content_type] = self._export_practical_layout(content_type)

        # Ensure content type consistency
        # Map calendar content types to template names
        content_type_mapping = {
            "reel": "reel",
            "story": "story", 
            "post": "post",
            "tutorial": "tutorial",
            "teaser": "teaser",
            "yt_short": "yt_short"
        }
        
        # Update events data with consistent content types
        for event in events_data:
            original_type = event["content_type"]
            event["template_key"] = content_type_mapping.get(original_type, original_type)

        return {
            "plugin": plugin_data,
            "global_prompt": self.global_prompt,
            "moodboard_path": self.moodboard_path,
            "assets": assets_data,
            "scheduled_content": events_data,
            "project_info": {
                "name": self.metadata.name,
                "format": self.metadata.format
            },
            "generation_info": {
                "export_date": datetime.now().isoformat(),
                "project_name": self.metadata.name,
                "version": "1.3.0",
                "format": self.metadata.format,
                "total_assets": len(assets_data),
                "total_events": len(events_data),
                "has_global_prompt": bool(self.global_prompt),
                "has_moodboard": bool(self.moodboard_path)
            },
            "content_generation": {
                "templates": templates_data
            },
            "ai_instructions": {
                "content_generation_workflow": [
                    "1. Use plugin info to understand the product and its unique features",
                    "2. Apply global_prompt for consistent brand voice and style",
                    "3. Use moodboard for visual style guidance (if provided)",
                    "4. Select appropriate assets from the assets list for each content piece",
                    "5. Generate content based on each scheduled_content item's prompt",
                    "6. Use template_key to match content with appropriate template settings",
                    "7. Ensure platform-specific optimization for each target platform"
                ],
                "content_requirements": {
                    "reel": "15-60 seconds, vertical 9:16, engaging hook in first 3 seconds",
                    "story": "15 seconds max, vertical 9:16, quick and engaging",
                    "post": "Static or short video, square 1:1, informative and branded",
                    "teaser": "10-15 seconds, any format, mysterious/exciting",
                    "tutorial": "60-300 seconds, landscape 16:9, educational and clear",
                    "yt_short": "15-60 seconds, vertical 9:16, optimized for YouTube"
                },
                "asset_selection_guidance": [
                    "Choose assets that best demonstrate the prompt requirements",
                    "Prefer audio assets for showcasing plugin sound",
                    "Use video assets for UI demonstrations",
                    "Combine multiple assets when needed for comprehensive content"
                ],
                "layout_guidance": [
                    "Use template layout coordinates for text and video positioning",
                    "Title text should be prominent and readable",
                    "Subtitle text provides context and calls-to-action",
                    "PiP video shows product in action",
                    "Respect platform-specific safe areas and aspect ratios"
                ]
            }
        }

    def _get_platform_for_content_type(self, content_type: str) -> str:
        """Get primary platform for a content type"""
        platform_mapping = {
            "reel": "instagram",
            "story": "instagram", 
            "post": "instagram",
            "tutorial": "youtube",
            "teaser": "instagram",
            "yt_short": "youtube"
        }
        return platform_mapping.get(content_type, "instagram")
        
    def export_ai_data_to_json(self, file_path: str, template_editor=None) -> bool:
        """Export AI generation data to a JSON file"""
        try:
            ai_data = self.get_ai_generation_data(template_editor=template_editor)
            
            # Convert any remaining enums to strings for safety
            converted_data = convert_enums(ai_data)
            
            with open(file_path, 'w') as f:
                json.dump(converted_data, f, indent=2)
            log_info(f"AI generation data exported to {file_path}")
            
            # Also export template config to a separate file
            config_path = file_path.replace('.json', '_config.json')
            self.export_template_config_to_json(config_path)
            
            return True
        except Exception as e:
            log_error(f"Failed to export AI generation data: {e}")
            import traceback
            traceback.print_exc()
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
                    print(f"Found ConfigMode at {path}.{k}: {v}")
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
                    print(f"Non-serializable at key '{k}': {e}")
                    print(f"Type: {type(v)}")
                    if hasattr(v, '__dict__'):
                        print(f"Attributes: {dir(v)}")
                    self._debug_find_non_serializable(v)
        elif isinstance(data, list):
            for i, item in enumerate(data):
                try:
                    json.dumps([item])
                except Exception as e:
                    print(f"Non-serializable at index {i}: {e}")
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
            "version": "1.3"  # Updated version for AI features
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

            # Ensure .rforge extension
            if target_path.suffix.lower() != '.rforge':
                target_path = target_path.with_suffix('.rforge')

            # Create directory if needed
            target_path.parent.mkdir(parents=True, exist_ok=True)

            # Save project data
            with open(target_path, 'w', encoding='utf-8') as f:
                json.dump(convert_enums(self.to_dict()), f, indent=2)

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
        """Export practical layout information for any content type"""
        # Get standard dimensions for content type
        dimensions = self._get_standard_dimensions(content_type)
        
        return {
            "name": content_type.replace("_", " ").title(),
            "content_type": content_type,
            "platform": self._get_platform_for_content_type(content_type),
            "dimensions": dimensions,
            "layout": {
                "title": {
                    "position": {"x": 50, "y": 100, "width": dimensions["width"] - 100, "height": 80},
                    "font_size": 32,
                    "font_weight": "bold",
                    "color": "#FFFFFF",
                    "alignment": "center",
                    "visible": True
                },
                "subtitle": {
                    "position": {"x": 50, "y": dimensions["height"] - 120, "width": dimensions["width"] - 100, "height": 60},
                    "font_size": 24,
                    "font_weight": "normal", 
                    "color": "#FFFFFF",
                    "alignment": "center",
                    "visible": True
                },
                "pip_video": {
                    "position": {"x": dimensions["width"] - 220, "y": 50, "width": 200, "height": 150},
                    "border_radius": 10,
                    "opacity": 0.9,
                    "visible": True
                }
            },
            "duration": self._get_content_duration(content_type),
            "animation": {
                "intro": "fade_in",
                "transition": "smooth",
                "outro": "fade_out"
            }
        }
    
    def _convert_ui_layout_to_export_format(self, ui_layout_data: Dict[str, Any], content_type: str) -> Dict[str, Any]:
        """Convert UI template editor layout data to export format"""
        elements = ui_layout_data.get('elements', {})
        settings = ui_layout_data.get('settings', {})
        
        # Get standard dimensions for content type
        dimensions = self._get_standard_dimensions(content_type)
        
        # Initialize layout with default structure
        layout = {}
        
        # Convert UI elements to layout format
        for element_id, element_data in elements.items():
            element_type = element_data.get('type', '')
            rect = element_data.get('rect', {})
            
            if element_type == 'text':
                # Map element_id directly to layout key
                if element_id == 'title':
                    layout_key = 'title'
                elif element_id == 'subtitle':
                    layout_key = 'subtitle'
                else:
                    # For other text elements, determine based on position
                    y_position = rect.get('y', 0)
                    if y_position < dimensions['height'] / 2:
                        layout_key = 'title'
                    else:
                        layout_key = 'subtitle'
                
                layout[layout_key] = {
                    "position": {
                        "x": rect.get('x', 50),
                        "y": rect.get('y', 100),
                        "width": rect.get('width', dimensions['width'] - 100),
                        "height": rect.get('height', 80)
                    },
                    "font_size": element_data.get('size', 24),
                    "font_weight": "bold" if element_data.get('style', '') == 'bold' else "normal",
                    "color": element_data.get('color', '#FFFFFF'),
                    "alignment": "center",
                    "visible": True
                }
                
            elif element_type == 'pip':
                layout['pip_video'] = {
                    "position": {
                        "x": rect.get('x', dimensions['width'] - 220),
                        "y": rect.get('y', 50),
                        "width": rect.get('width', 200),
                        "height": rect.get('height', 150)
                    },
                    "border_radius": element_data.get('corner_radius', 10),
                    "opacity": 0.9,
                    "visible": element_data.get('enabled', True)
                }
        
        # If no elements found, provide basic fallback layout
        if not layout.get('title'):
            layout['title'] = {
                "position": {"x": 50, "y": 100, "width": dimensions["width"] - 100, "height": 80},
                "font_size": 32,
                "font_weight": "bold",
                "color": "#FFFFFF",
                "alignment": "center",
                "visible": True
            }
        
        if not layout.get('subtitle'):
            layout['subtitle'] = {
                "position": {"x": 50, "y": dimensions["height"] - 120, "width": dimensions["width"] - 100, "height": 60},
                "font_size": 24,
                "font_weight": "normal",
                "color": "#FFFFFF",
                "alignment": "center",
                "visible": True
            }
        
        if not layout.get('pip_video'):
            layout['pip_video'] = {
                "position": {"x": dimensions["width"] - 220, "y": 50, "width": 200, "height": 150},
                "border_radius": 10,
                "opacity": 0.9,
                "visible": True
            }
        
        return {
            "name": content_type.replace("_", " ").title(),
            "content_type": content_type,
            "platform": self._get_platform_for_content_type(content_type),
            "dimensions": dimensions,
            "layout": layout,
            "duration": self._get_content_duration(content_type),
            "animation": {
                "intro": "fade_in",
                "transition": "smooth",
                "outro": "fade_out"
            }
        }
    
    def _get_standard_dimensions(self, content_type: str) -> Dict[str, int]:
        """Get standard dimensions for content types"""
        dimension_map = {
            "reel": {"width": 1080, "height": 1920},      # 9:16 vertical
            "story": {"width": 1080, "height": 1920},     # 9:16 vertical  
            "post": {"width": 1080, "height": 1080},      # 1:1 square
            "tutorial": {"width": 1920, "height": 1080},  # 16:9 landscape
            "teaser": {"width": 1080, "height": 1920},    # 9:16 vertical
            "yt_short": {"width": 1080, "height": 1920}   # 9:16 vertical
        }
        return dimension_map.get(content_type, {"width": 1080, "height": 1080})
    
    def _get_content_duration(self, content_type: str) -> str:
        """Get typical duration for content types"""
        duration_map = {
            "reel": "15-30s",
            "story": "5-15s", 
            "post": "30-60s",
            "tutorial": "60-300s",
            "teaser": "10-15s",
            "yt_short": "15-60s"
        }
        return duration_map.get(content_type, "30s")

    def save_template_editor_settings(self, template_editor):
        """Save template editor settings to project"""
        if not template_editor:
            return
            
        # Save all content type configurations
        template_settings = {}
        
        # Get current content type
        current_type = template_editor.get_content_type()
        
        # Save settings for each content type that has been configured
        content_types = ["reel", "story", "post", "tutorial", "teaser", "yt_short"]
        
        for content_type in content_types:
            # Switch to content type to get its settings
            template_editor.set_content_type(content_type)
            config = template_editor.get_template_config()
            
            if config and config.get("canvas_config"):
                template_settings[content_type] = config
        
        # Restore original content type
        template_editor.set_content_type(current_type)
        
        # Save to project
        self.template_editor_settings = template_settings
        self._is_modified = True

    def load_template_editor_settings(self, template_editor):
        """Load template editor settings from project"""
        if not template_editor or not hasattr(self, "template_editor_settings"):
            return
            
        template_settings = getattr(self, "template_editor_settings", {})
        
        # Get current content type
        current_type = template_editor.get_content_type()
        
        # Load settings for each content type
        for content_type, config in template_settings.items():
            template_editor.set_content_type(content_type)
            template_editor.set_template_config(config)
        
        # Restore original content type
        template_editor.set_content_type(current_type)



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
        return Path(app_data) / "reeltune_settings.json"

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

    def save_template_editor_settings(self, template_editor):
        """Save template editor settings to project"""
        if not template_editor:
            return
            
        # Save all content type configurations
        template_settings = {}
        
        # Get current content type
        current_type = template_editor.get_content_type()
        
        # Save settings for each content type that has been configured
        content_types = ['reel', 'story', 'post', 'tutorial', 'teaser', 'yt_short']
        
        for content_type in content_types:
            # Switch to content type to get its settings
            template_editor.set_content_type(content_type)
            config = template_editor.get_template_config()
            
            if config and config.get('canvas_config'):
                template_settings[content_type] = config
        
        # Restore original content type
        template_editor.set_content_type(current_type)
        
        # Save to project
        self.template_editor_settings = template_settings
        self._is_modified = True
        
    def load_template_editor_settings(self, template_editor):
        """Load template editor settings from project"""
        if not template_editor or not hasattr(self, 'template_editor_settings'):
            return
            
        template_settings = getattr(self, 'template_editor_settings', {})
        
        # Get current content type
        current_type = template_editor.get_content_type()
        
        # Load settings for each content type
        for content_type, config in template_settings.items():
            template_editor.set_content_type(content_type)
            template_editor.set_template_config(config)
        
        # Restore original content type
        template_editor.set_content_type(current_type)
