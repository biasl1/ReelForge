"""
Plugin management and .adsp file handling for ReelTune
Integrates with Artista plugin metadata for content generation
"""

import json
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


def get_supported_content_types() -> Dict[str, Dict[str, Any]]:
    """Get supported content types for AI generation"""
    return {
        "reel": {
            "name": "Instagram Reel",
            "format": "1080x1920",
            "duration": "15-60s",
            "ai_prompts": [
                "Show plugin interface with key parameters",
                "Demonstrate sound transformation",
                "Quick tutorial on main features",
                "Before/after audio comparison"
            ]
        },
        "story": {
            "name": "Instagram Story",
            "format": "1080x1920",
            "duration": "15s",
            "ai_prompts": [
                "Plugin showcase with branding",
                "Quick tip or feature highlight",
                "Behind-the-scenes development",
                "User testimonial format"
            ]
        },
        "post": {
            "name": "Instagram Post",
            "format": "1080x1080",
            "duration": "static or 15-30s",
            "ai_prompts": [
                "Clean plugin interface shot",
                "Feature comparison graphic",
                "Educational infographic",
                "Brand announcement"
            ]
        },
        "teaser": {
            "name": "Teaser Video",
            "format": "1080x1920 or 1920x1080",
            "duration": "10-15s",
            "ai_prompts": [
                "Coming soon announcement",
                "Preview of plugin capabilities",
                "Mystery/intrigue building",
                "Quick sound preview"
            ]
        },
        "tutorial": {
            "name": "Tutorial Video",
            "format": "1920x1080",
            "duration": "60-300s",
            "ai_prompts": [
                "Step-by-step parameter explanation",
                "Creative usage examples",
                "Integration with other plugins",
                "Production techniques"
            ]
        }
    }


def generate_ai_prompts_for_plugin(plugin_info: PluginInfo, content_type: str) -> List[str]:
    """Generate AI prompts based on plugin info and content type"""
    base_prompts = get_supported_content_types().get(content_type, {}).get("ai_prompts", [])

    # Customize prompts with plugin-specific information
    customized_prompts = []

    for prompt in base_prompts:
        # Replace generic terms with plugin-specific info
        customized = prompt.replace("plugin", plugin_info.name)

        # Add plugin-specific context
        if plugin_info.unique:
            customized += f" (Highlight: {plugin_info.unique[:100]}...)"

        if plugin_info.one_word:
            customized += f" (Style: {plugin_info.one_word})"

        customized_prompts.append(customized)

    # Add plugin-specific prompts
    if plugin_info.problem:
        customized_prompts.append(f"Show how {plugin_info.name} solves: {plugin_info.problem}")

    if plugin_info.wow:
        customized_prompts.append(f"Demonstrate the wow factor: {plugin_info.wow}")

    return customized_prompts
