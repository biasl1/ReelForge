"""
Plugin management and .adsp file handling for ReelTune
Integrates with Artista plugin metadata for content generation
"""

import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict, field
from datetime import datetime
from core.logging_config import log_info, log_error, log_warning, log_debug


@dataclass
class PluginInfo:
    """Plugin information extracted from .adsp files"""
    name: str
    title: str = ""
    tagline: str = ""
    version: str = ""
    company: str = ""
    code: str = ""

    # Descriptions
    short_description: str = ""
    long_description: str = ""
    unique: str = ""
    problem: str = ""
    wow: str = ""
    personality: str = ""
    one_word: str = ""

    # Technical info
    category: List[str] = field(default_factory=list)
    intended_use: List[str] = field(default_factory=list)
    input_type: str = ""
    has_sidechain: bool = False
    tech_summary: str = ""

    # Visual/branding
    highlight_color: List[int] = field(default_factory=list)
    plugin_size: List[int] = field(default_factory=list)

    # Parameters and components
    key_parameters: List[Dict] = field(default_factory=list)
    components: List[Dict] = field(default_factory=list)

    # Metadata
    changelog: List[str] = field(default_factory=list)
    source_folder: str = ""
    import_date: str = ""
    adsp_file_path: str = ""

    def __post_init__(self):
        if not self.import_date:
            self.import_date = datetime.now().isoformat()


class PluginManager:
    """Manages plugin information and .adsp file imports"""

    def __init__(self):
        self.plugins: Dict[str, PluginInfo] = {}

    def import_adsp_file(self, file_path: Path) -> Optional[PluginInfo]:
        """Import plugin information from .adsp file"""
        try:
            if not file_path.exists() or file_path.suffix.lower() != '.adsp':
                return None

            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Extract plugin information
            plugin_info = PluginInfo(
                name=data.get('pluginName', file_path.stem),
                title=data.get('pluginTitle', ''),
                tagline=data.get('pluginTagline', ''),
                version=data.get('pluginVersion', ''),
                company=self._extract_company_from_components(data.get('components', [])),
                code=data.get('pluginCode', ''),

                # Descriptions
                short_description=data.get('short_description', ''),
                long_description=data.get('long_description', ''),
                unique=data.get('unique', ''),
                problem=data.get('problem', ''),
                wow=data.get('wow', ''),
                personality=data.get('personality', ''),
                one_word=data.get('one_word', ''),

                # Technical
                category=data.get('category', []),
                intended_use=data.get('intended_use', []),
                input_type=data.get('input_type', ''),
                has_sidechain=data.get('has_sidechain', False),
                tech_summary=data.get('tech_summary', ''),

                # Visual
                highlight_color=data.get('highlightColor', []),
                plugin_size=data.get('pluginSize', []),

                # Components
                key_parameters=data.get('key_parameters', []),
                components=data.get('components', []),

                # Meta
                changelog=data.get('changelog', []),
                source_folder=data.get('source_folder', ''),
                adsp_file_path=str(file_path)
            )

            # Store plugin
            self.plugins[plugin_info.name] = plugin_info

            return plugin_info

        except Exception as e:
            log_error(f"Error importing .adsp file {file_path}: {e}")
            return None

    def _extract_company_from_components(self, components: List[Dict]) -> str:
        """Extract company name from header components"""
        for component in components:
            if component.get('type') == 'header_company':
                return component.get('display_name', '')
        return ''

    def get_plugin(self, name: str) -> Optional[PluginInfo]:
        """Get plugin by name"""
        return self.plugins.get(name)

    def get_all_plugins(self) -> List[PluginInfo]:
        """Get all imported plugins"""
        return list(self.plugins.values())

    def remove_plugin(self, name: str) -> bool:
        """Remove plugin from manager"""
        if name in self.plugins:
            del self.plugins[name]
            return True
        return False

    def get_content_generation_data(self, plugin_name: str) -> Optional[Dict[str, Any]]:
        """Get structured data for AI content generation"""
        plugin = self.get_plugin(plugin_name)
        if not plugin:
            return None

        return {
            "plugin_info": {
                "name": plugin.name,
                "title": plugin.title,
                "tagline": plugin.tagline,
                "company": plugin.company,
                "version": plugin.version,
                "one_word_description": plugin.one_word,
                "personality": plugin.personality
            },
            "marketing_content": {
                "short_description": plugin.short_description,
                "long_description": plugin.long_description,
                "unique_selling_point": plugin.unique,
                "problem_solved": plugin.problem,
                "wow_factor": plugin.wow,
                "categories": plugin.category,
                "use_cases": plugin.intended_use
            },
            "technical_specs": {
                "input_type": plugin.input_type,
                "has_sidechain": plugin.has_sidechain,
                "tech_summary": plugin.tech_summary,
                "key_parameters": plugin.key_parameters
            },
            "visual_branding": {
                "highlight_color": plugin.highlight_color,
                "plugin_size": plugin.plugin_size,
                "components": plugin.components
            },
            "version_info": {
                "changelog": plugin.changelog,
                "current_version": plugin.version
            }
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "plugins": {name: asdict(plugin) for name, plugin in self.plugins.items()}
        }

    def from_dict(self, data: Dict[str, Any]):
        """Load from dictionary"""
        self.plugins.clear()
        if "plugins" in data:
            for name, plugin_data in data["plugins"].items():
                plugin = PluginInfo(**plugin_data)
                self.plugins[name] = plugin





def generate_ai_prompts_for_plugin(plugin_info: PluginInfo, content_type: str = None) -> List[str]:
    """Generate AI prompts based purely on .adsp plugin metadata and parameters"""
    if not plugin_info:
        return []
        
    prompts = []
    
    # Core plugin information prompts
    prompts.append(f"Create content showcasing {plugin_info.name}")
    if plugin_info.tagline:
        prompts.append(f"Tagline: {plugin_info.tagline}")
    
    if plugin_info.short_description:
        prompts.append(f"Core message: {plugin_info.short_description}")
    
    if plugin_info.unique:
        prompts.append(f"Unique selling point: {plugin_info.unique}")
    
    # Parameter-focused prompts from .adsp metadata
    if plugin_info.key_parameters:
        prompts.append("Showcase key parameters:")
        # Show top 3 most important parameters
        sorted_params = sorted(
            plugin_info.key_parameters, 
            key=lambda x: int(x.get('importance', '999'))
        )[:3]
        
        for param in sorted_params:
            name = param.get('name', 'Parameter')
            desc = param.get('description', '').strip()
            prompts.append(f"  • {name}: {desc}")
    
    # Visual branding from .adsp
    if plugin_info.highlight_color:
        color_hex = '#' + ''.join([f'{c:02x}' for c in plugin_info.highlight_color[:3]])
        prompts.append(f"Brand highlight color: {color_hex}")
    
    # Problem/solution narrative
    if plugin_info.problem and plugin_info.wow:
        prompts.append(f"Problem: {plugin_info.problem}")
        prompts.append(f"Solution/Wow: {plugin_info.wow}")
    
    # Technical context
    if plugin_info.tech_summary:
        prompts.append(f"Technical context: {plugin_info.tech_summary[:200]}...")
    
    # Intended use cases from .adsp
    if plugin_info.intended_use:
        use_cases = ", ".join(plugin_info.intended_use[:3])
        prompts.append(f"Target use cases: {use_cases}")
    
    # Personality/tone
    if plugin_info.personality:
        prompts.append(f"Personality/tone: {plugin_info.personality}")
    elif plugin_info.one_word:
        prompts.append(f"Style keyword: {plugin_info.one_word}")
    
    return prompts


def extract_plugin_parameters_from_adsp(adsp_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract parameter information from .adsp file metadata"""
    parameters = []
    
    # Extract from key_parameters if available
    if "key_parameters" in adsp_data:
        for param in adsp_data["key_parameters"]:
            parameters.append({
                "name": param.get("name", ""),
                "description": param.get("description", "").strip(),
                "importance": param.get("importance", "0"),
                "type": "key_parameter"
            })
    
    # Extract from components for additional context
    if "components" in adsp_data:
        for component in adsp_data["components"]:
            if component.get("type") in ["dial", "slider", "button", "dropdown"]:
                param_id = component.get("param_id", "")
                display_name = component.get("display_name", "")
                if param_id and display_name:
                    parameters.append({
                        "name": display_name,
                        "param_id": param_id,
                        "component_type": component.get("type", ""),
                        "position": component.get("position", [0, 0]),
                        "size": component.get("size", [0, 0]),
                        "type": "ui_component"
                    })
    
    # Extract highlight colors if available
    highlight_info = {}
    if "pluginTheme" in adsp_data:
        theme = adsp_data["pluginTheme"]
        highlight_info = {
            "primary_color": theme.get("primaryColor", ""),
            "accent_color": theme.get("accentColor", ""), 
            "highlight_color": theme.get("highlightColor", ""),
            "background_color": theme.get("backgroundColor", "")
        }
    
    return {
        "parameters": parameters,
        "highlight_info": highlight_info,
        "plugin_metadata": {
            "name": adsp_data.get("pluginName", ""),
            "title": adsp_data.get("pluginTitle", ""),
            "tagline": adsp_data.get("pluginTagline", ""),
            "short_description": adsp_data.get("short_description", ""),
            "long_description": adsp_data.get("long_description", ""),
            "unique": adsp_data.get("unique", ""),
            "personality": adsp_data.get("personality", ""),
            "problem": adsp_data.get("problem", ""),
            "wow": adsp_data.get("wow", "")
        }
    }


def generate_adsp_based_prompts(adsp_data: Dict[str, Any]) -> List[str]:
    """Generate AI prompts specifically from .adsp file metadata"""
    extraction = extract_plugin_parameters_from_adsp(adsp_data)
    metadata = extraction["plugin_metadata"] 
    parameters = extraction["parameters"]
    highlight_info = extraction["highlight_info"]
    
    prompts = []
    
    # Core plugin identity
    plugin_name = metadata.get("name", "Plugin")
    tagline = metadata.get("tagline", "")
    if tagline:
        prompts.append(f"Create content for {plugin_name}: {tagline}")
    else:
        prompts.append(f"Create content showcasing {plugin_name}")
    
    # Key messaging
    if metadata.get("short_description"):
        prompts.append(f"Core message: {metadata['short_description']}")
    
    if metadata.get("unique"):
        prompts.append(f"Unique selling point: {metadata['unique']}")
    
    # Parameter focus (from .adsp metadata)
    key_params = [p for p in parameters if p["type"] == "key_parameter"]
    if key_params:
        prompts.append("Key parameters to showcase:")
        # Sort by importance and take top 3
        sorted_params = sorted(key_params, key=lambda x: int(x.get("importance", "999")))[:3]
        for param in sorted_params:
            prompts.append(f"  • {param['name']}: {param['description']}")
    
    # Visual style guidance
    if highlight_info.get("highlight_color"):
        prompts.append(f"Brand color palette: {highlight_info['highlight_color']} (highlight)")
    
    if metadata.get("personality"):
        prompts.append(f"Personality/tone: {metadata['personality']}")
    
    # Problem/solution narrative
    if metadata.get("problem") and metadata.get("wow"):
        prompts.append(f"Problem/Solution narrative: {metadata['problem']} → {metadata['wow']}")
    
    return prompts


def export_ai_generation_data(project_path: str) -> Dict[str, Any]:
    """Export project data formatted for AI content generation with .adsp-based prompts"""
    try:
        with open(project_path, 'r') as f:
            project_data = json.load(f)
        
        # Get plugin info from .adsp file
        plugin_file = project_data.get('plugin_file')
        if not plugin_file:
            # Check metadata for plugin_name
            metadata = project_data.get('metadata', {})
            plugin_name = metadata.get('plugin_name', '')
            if plugin_name:
                # Search for .adsp file in the same directory
                project_dir = os.path.dirname(project_path)
                plugin_file = os.path.join(project_dir, f"{plugin_name}.adsp")
                if not os.path.exists(plugin_file):
                    # Try the workspace root
                    workspace_root = os.path.dirname(project_dir)
                    plugin_file = os.path.join(workspace_root, f"{plugin_name}.adsp")
            
            # If still not found, search for any .adsp file
            if not plugin_file or not os.path.exists(plugin_file):
                # Try current directory first
                project_dir = os.path.dirname(project_path)
                for file in os.listdir(project_dir):
                    if file.endswith('.adsp'):
                        plugin_file = os.path.join(project_dir, file)
                        break
                
                # If not found, try workspace root
                if not plugin_file or not os.path.exists(plugin_file):
                    workspace_root = os.path.dirname(project_dir)
                    if os.path.exists(workspace_root):
                        for file in os.listdir(workspace_root):
                            if file.endswith('.adsp'):
                                plugin_file = os.path.join(workspace_root, file)
                                break
        
        plugin_info = None
        if plugin_file and os.path.exists(plugin_file):
            plugin_info = parse_plugin_file(plugin_file)
        
        return export_ai_generation_data_updated(project_data, plugin_info)
        
    except Exception as e:
        log_error(f"Failed to export AI generation data: {e}")
        import traceback
        log_error(f"Traceback: {traceback.format_exc()}")
        return {}


def discover_plugins() -> List[PluginInfo]:
    """Discover .adsp plugins in common directories"""
    plugins = []
    # This would search for .adsp files in common plugin directories
    # For now, return empty list as placeholder
    return plugins


def parse_plugin_file(file_path: str) -> Optional[PluginInfo]:
    """Parse a single .adsp plugin file"""
    try:
        manager = PluginManager()
        return manager.import_adsp_file(Path(file_path))
    except Exception as e:
        log_error(f"Error parsing plugin file {file_path}: {e}")
        return None


def export_ai_generation_data_updated(project_data: Dict[str, Any], plugin_info) -> Dict[str, Any]:
    """Export project data with .adsp-based AI prompts"""
    
    # Import here to avoid circular import
    from core.project import convert_enums
    
    # Extract project name from metadata or root level
    metadata = project_data.get('metadata', {})
    project_name = metadata.get('name') or project_data.get('name', 'Untitled Project')
    
    # Prepare export data with same structure as before
    export_data = {
        'project_name': project_name,
        'plugin_info': {
            'name': plugin_info.name if plugin_info else 'Unknown Plugin',
            'metadata': {
                'tagline': plugin_info.tagline if plugin_info else '',
                'short_description': plugin_info.short_description if plugin_info else '',
                'unique': plugin_info.unique if plugin_info else '',
                'parameters': plugin_info.key_parameters if plugin_info else [],
                'highlight_color': plugin_info.highlight_color if plugin_info else None,
                'problem': plugin_info.problem if plugin_info else '',
                'wow': plugin_info.wow if plugin_info else '',
                'intended_use': plugin_info.intended_use if plugin_info else [],
                'personality': plugin_info.personality if plugin_info else '',
                'one_word': plugin_info.one_word if plugin_info else ''
            }
        },
        'events': [],
        'ai_prompts': generate_ai_prompts_for_export(plugin_info) if plugin_info else []
    }
    
    # Process each release event
    events = project_data.get('release_events', {})
    # Handle both dict (new format) and list (legacy format)
    if isinstance(events, dict):
        events_list = list(events.values())
    else:
        events_list = events
        
    for event in events_list:
        event_data = {
            'id': event.get('id', ''),
            'type': event.get('content_type', event.get('type', '')),  # Handle both field names
            'date': event.get('date', ''),
            'frame_count': event.get('frame_count', 1)
        }
        
        # Extract template configuration for each frame (if exists)
        template_config = event.get('template_config', {})
        frames_data = []
        
        frame_count = event.get('frame_count', 1)
        for frame_idx in range(frame_count):
            frame_key = f"frame_{frame_idx}"
            frame_elements = template_config.get(frame_key, {}).get('elements', [])
            
            # Process elements with JSON serialization
            processed_elements = []
            for element in frame_elements:
                processed_element = convert_enums(element)
                processed_elements.append(processed_element)
            
            frames_data.append({
                'frame_index': frame_idx,
                'elements': processed_elements
            })
        
        event_data['frames'] = frames_data
        export_data['events'].append(event_data)
    
    return export_data


def get_supported_content_types() -> Dict[str, str]:
    """Return supported content types for backwards compatibility"""
    # Return basic event types instead of legacy content types
    return {
        'VIDEO': 'Video Content',
        'PICTURE': 'Picture Content'
    }


def get_plugin_info(plugin_name: str) -> Optional[Dict[str, Any]]:
    """Get plugin information by name"""
    # Placeholder for compatibility
    return None


def generate_ai_prompts_for_export(plugin_info) -> List[Dict[str, Any]]:
    """Generate structured AI prompts for export (returns dicts, not strings)"""
    if not plugin_info:
        return []
    
    prompts = []
    
    # Main creative prompt based on plugin personality and metadata
    creative_prompt = {
        'type': 'creative_direction',
        'context': f"Plugin: {plugin_info.name}",
        'prompt': f"Generate creative content for {plugin_info.name}: {plugin_info.tagline}. "
                 f"Focus on {plugin_info.short_description}. "
                 f"Unique selling point: {plugin_info.unique}. "
                 f"Target problem: {plugin_info.problem}. "
                 f"Wow factor: {plugin_info.wow}. "
                 f"Personality: {plugin_info.personality}. "
                 f"One word essence: {plugin_info.one_word}.",
        'style_guidance': {
            'highlight_color': plugin_info.highlight_color,
            'personality': plugin_info.personality,
            'essence': plugin_info.one_word
        }
    }
    prompts.append(creative_prompt)
    
    # Technical parameters prompt
    if plugin_info.key_parameters:
        # Handle both list of dicts and list of strings
        if isinstance(plugin_info.key_parameters, list) and plugin_info.key_parameters:
            if isinstance(plugin_info.key_parameters[0], dict):
                param_names = [p.get('name', '') for p in plugin_info.key_parameters]
            else:
                param_names = plugin_info.key_parameters
        else:
            param_names = []
            
        tech_prompt = {
            'type': 'technical_focus',
            'context': f"Plugin parameters for {plugin_info.name}",
            'prompt': f"Highlight these key technical features: {', '.join(param_names)}. "
                     f"Explain how these parameters solve: {plugin_info.problem}",
            'parameters': param_names
        }
        prompts.append(tech_prompt)
    
    # Use case prompt
    if plugin_info.intended_use:
        use_case_prompt = {
            'type': 'use_case_scenarios',
            'context': f"Applications for {plugin_info.name}",
            'prompt': f"Create content showcasing these use cases: {', '.join(plugin_info.intended_use)}. "
                     f"Demonstrate the {plugin_info.wow} in practical scenarios.",
            'use_cases': plugin_info.intended_use
        }
        prompts.append(use_case_prompt)
    
    return prompts
