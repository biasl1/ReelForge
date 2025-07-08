"""
Content Generation Template System for ReelTune
Manages universal templates, AI prompt generation, and config resolution
"""

import json
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
from dataclasses import dataclass, asdict, field
from datetime import datetime
from enum import Enum

from core.logging_config import log_info, log_error, log_debug


class ReelTuneJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder for ReelTune objects"""
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        if hasattr(obj, 'to_dict') and callable(getattr(obj, 'to_dict')):
            return obj.to_dict()
        return super().default(obj)


class ConfigMode(Enum):
    """Configuration parameter modes"""
    FIXED = "fixed"      # 🔒 Always use this exact value
    GUIDED = "guided"    # 🎯 AI chooses within constraints  
    FREE = "free"        # 🤖 AI has complete creative freedom


@dataclass
class ConfigParameter:
    """Individual configuration parameter with mode and constraints"""
    value: Any
    mode: ConfigMode = ConfigMode.FIXED
    constraints: Optional[Dict[str, Any]] = None  # For GUIDED mode (min, max, options)
    description: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "value": self.value,
            "mode": self.mode.value,
            "constraints": self.constraints,
            "description": self.description
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ConfigParameter':
        """Create from dictionary"""
        return cls(
            value=data.get("value"),
            mode=ConfigMode(data.get("mode", "fixed")),
            constraints=data.get("constraints"),
            description=data.get("description", "")
        )


@dataclass
class SubtitleTemplate:
    """Subtitle configuration template"""
    font_size: ConfigParameter = field(default_factory=lambda: ConfigParameter("24px"))
    font_family: ConfigParameter = field(default_factory=lambda: ConfigParameter("Arial"))
    color: ConfigParameter = field(default_factory=lambda: ConfigParameter("white"))
    position: ConfigParameter = field(default_factory=lambda: ConfigParameter("bottom"))
    stroke_width: ConfigParameter = field(default_factory=lambda: ConfigParameter("2px"))
    stroke_color: ConfigParameter = field(default_factory=lambda: ConfigParameter("black"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, ConfigParameter):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SubtitleTemplate':
        """Create from dictionary"""
        return cls(**{k: ConfigParameter.from_dict(v) for k, v in data.items()})


@dataclass
class OverlayTemplate:
    """Overlay and visual effects template"""
    background_style: ConfigParameter = field(default_factory=lambda: ConfigParameter("transparent"))
    animation_style: ConfigParameter = field(default_factory=lambda: ConfigParameter("fade_in"))
    overlay_elements: ConfigParameter = field(default_factory=lambda: ConfigParameter("none"))
    branding_elements: ConfigParameter = field(default_factory=lambda: ConfigParameter("logo"))
    color_scheme: ConfigParameter = field(default_factory=lambda: ConfigParameter("brand"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, ConfigParameter):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'OverlayTemplate':
        """Create from dictionary"""
        return cls(**{k: ConfigParameter.from_dict(v) for k, v in data.items()})


@dataclass
class TimingTemplate:
    """Timing and pacing template"""
    duration: ConfigParameter = field(default_factory=lambda: ConfigParameter("30s"))
    intro_duration: ConfigParameter = field(default_factory=lambda: ConfigParameter("2s"))
    outro_duration: ConfigParameter = field(default_factory=lambda: ConfigParameter("3s"))
    segment_count: ConfigParameter = field(default_factory=lambda: ConfigParameter(4))
    transition_style: ConfigParameter = field(default_factory=lambda: ConfigParameter("smooth"))
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = {}
        for key, value in asdict(self).items():
            if isinstance(value, ConfigParameter):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TimingTemplate':
        """Create from dictionary"""
        return cls(**{k: ConfigParameter.from_dict(v) for k, v in data.items()})


@dataclass
class ContentTemplate:
    """Complete content template for a specific content type"""
    content_type: str
    subtitle: SubtitleTemplate = field(default_factory=SubtitleTemplate)
    overlay: OverlayTemplate = field(default_factory=OverlayTemplate)
    timing: TimingTemplate = field(default_factory=TimingTemplate)
    custom_parameters: Dict[str, ConfigParameter] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            "content_type": self.content_type,
            "subtitle": self.subtitle.to_dict(),
            "overlay": self.overlay.to_dict(),
            "timing": self.timing.to_dict(),
            "custom_parameters": {k: v.to_dict() for k, v in self.custom_parameters.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentTemplate':
        """Create from dictionary"""
        return cls(
            content_type=data.get("content_type", ""),
            subtitle=SubtitleTemplate.from_dict(data.get("subtitle", {})),
            overlay=OverlayTemplate.from_dict(data.get("overlay", {})),
            timing=TimingTemplate.from_dict(data.get("timing", {})),
            custom_parameters={k: ConfigParameter.from_dict(v) for k, v in data.get("custom_parameters", {}).items()}
        )


class ContentGenerationManager:
    """Manages content generation templates and AI configuration"""
    
    def __init__(self):
        self.project_wide_template: Optional[ContentTemplate] = None
        self.content_type_templates: Dict[str, ContentTemplate] = {}
        self.event_templates: Dict[str, ContentTemplate] = {}  # event_id -> template
        
        # Initialize default content type templates
        self._initialize_default_templates()
    
    def _initialize_default_templates(self):
        """Initialize default templates for common content types"""
        content_types = ["reel", "story", "post", "tutorial"]
        
        for content_type in content_types:
            template = ContentTemplate(content_type=content_type)
            
            # Set content-type-specific defaults
            if content_type == "reel":
                template.timing.duration.value = "15-30s"
                template.subtitle.position.value = "bottom"
            elif content_type == "story":
                template.timing.duration.value = "5-15s"
                template.subtitle.position.value = "center"
            elif content_type == "post":
                template.timing.duration.value = "30-60s"
                template.subtitle.position.value = "bottom"
            elif content_type == "tutorial":
                template.timing.duration.value = "60-120s"
                template.subtitle.position.value = "bottom"
                template.timing.segment_count.value = 6
            
            self.content_type_templates[content_type] = template
    
    def get_content_template(self, content_type: str) -> ContentTemplate:
        """Get template for specific content type"""
        if content_type not in self.content_type_templates:
            # Create new template if it doesn't exist
            self.content_type_templates[content_type] = ContentTemplate(content_type=content_type)
        
        return self.content_type_templates[content_type]
    
    def set_project_wide_template(self, template: ContentTemplate):
        """Set project-wide template"""
        self.project_wide_template = template
    
    def set_event_template(self, event_id: str, template: ContentTemplate):
        """Set template for specific event"""
        self.event_templates[event_id] = template
    
    def resolve_config(self, content_type: str, event_id: Optional[str] = None) -> Dict[str, Any]:
        """Resolve final configuration for content generation"""
        final_config = {}
        
        # Start with project-wide template
        if self.project_wide_template:
            final_config.update(self._template_to_config(self.project_wide_template))
        
        # Override with content-type template
        if content_type in self.content_type_templates:
            content_config = self._template_to_config(self.content_type_templates[content_type])
            final_config.update(content_config)
        
        # Override with event-specific template
        if event_id and event_id in self.event_templates:
            event_config = self._template_to_config(self.event_templates[event_id])
            final_config.update(event_config)
        
        return final_config
    
    def _template_to_config(self, template: ContentTemplate) -> Dict[str, Any]:
        """Convert template to config dictionary"""
        config = {}
        
        # Process subtitle settings
        for key, param in template.subtitle.to_dict().items():
            if param["mode"] == ConfigMode.FIXED.value:
                config[f"subtitle_{key}"] = param["value"]
        
        # Process overlay settings
        for key, param in template.overlay.to_dict().items():
            if param["mode"] == ConfigMode.FIXED.value:
                config[f"overlay_{key}"] = param["value"]
        
        # Process timing settings
        for key, param in template.timing.to_dict().items():
            if param["mode"] == ConfigMode.FIXED.value:
                config[f"timing_{key}"] = param["value"]
        
        # Process custom parameters
        for key, param in template.custom_parameters.items():
            if param.mode == ConfigMode.FIXED:
                config[f"custom_{key}"] = param.value
        
        return config
    
    def generate_ai_prompt(self, content_type: str, event_id: Optional[str] = None, 
                          base_prompt: str = "") -> str:
        """Generate AI prompt with template constraints"""
        prompt_parts = [base_prompt] if base_prompt else []
        
        # Collect all relevant templates
        templates = []
        if self.project_wide_template:
            templates.append(("project-wide", self.project_wide_template))
        if content_type in self.content_type_templates:
            templates.append((f"{content_type}", self.content_type_templates[content_type]))
        if event_id and event_id in self.event_templates:
            templates.append((f"event-{event_id}", self.event_templates[event_id]))
        
        # Generate constraint instructions
        fixed_constraints = []
        guided_constraints = []
        free_parameters = []
        
        for template_name, template in templates:
            # Process subtitle parameters
            for key, param_dict in template.subtitle.to_dict().items():
                param = ConfigParameter.from_dict(param_dict)
                if param.mode == ConfigMode.FIXED:
                    fixed_constraints.append(f"Subtitle {key} must be: {param.value}")
                elif param.mode == ConfigMode.GUIDED:
                    guided_constraints.append(f"Subtitle {key}: {param.description} (constraints: {param.constraints})")
                elif param.mode == ConfigMode.FREE:
                    free_parameters.append(f"Subtitle {key}: AI decides")
            
            # Process overlay parameters
            for key, param_dict in template.overlay.to_dict().items():
                param = ConfigParameter.from_dict(param_dict)
                if param.mode == ConfigMode.FIXED:
                    fixed_constraints.append(f"Overlay {key} must be: {param.value}")
                elif param.mode == ConfigMode.GUIDED:
                    guided_constraints.append(f"Overlay {key}: {param.description} (constraints: {param.constraints})")
                elif param.mode == ConfigMode.FREE:
                    free_parameters.append(f"Overlay {key}: AI decides")
            
            # Process timing parameters
            for key, param_dict in template.timing.to_dict().items():
                param = ConfigParameter.from_dict(param_dict)
                if param.mode == ConfigMode.FIXED:
                    fixed_constraints.append(f"Timing {key} must be: {param.value}")
                elif param.mode == ConfigMode.GUIDED:
                    guided_constraints.append(f"Timing {key}: {param.description} (constraints: {param.constraints})")
                elif param.mode == ConfigMode.FREE:
                    free_parameters.append(f"Timing {key}: AI decides")
        
        # Build constraint sections
        if fixed_constraints:
            prompt_parts.append("\n## REQUIRED SETTINGS (must follow exactly):")
            prompt_parts.extend([f"- {constraint}" for constraint in fixed_constraints])
        
        if guided_constraints:
            prompt_parts.append("\n## GUIDED SETTINGS (follow constraints):")
            prompt_parts.extend([f"- {constraint}" for constraint in guided_constraints])
        
        if free_parameters:
            prompt_parts.append("\n## CREATIVE FREEDOM:")
            prompt_parts.extend([f"- {param}" for param in free_parameters])
        
        return "\n".join(prompt_parts)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert manager to dictionary for serialization"""
        return {
            "project_wide_template": self.project_wide_template.to_dict() if self.project_wide_template else None,
            "content_type_templates": {k: v.to_dict() for k, v in self.content_type_templates.items()},
            "event_templates": {k: v.to_dict() for k, v in self.event_templates.items()}
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ContentGenerationManager':
        """Create manager from dictionary"""
        manager = cls()
        
        if data.get("project_wide_template"):
            manager.project_wide_template = ContentTemplate.from_dict(data["project_wide_template"])
        
        manager.content_type_templates = {
            k: ContentTemplate.from_dict(v) 
            for k, v in data.get("content_type_templates", {}).items()
        }
        
        manager.event_templates = {
            k: ContentTemplate.from_dict(v)
            for k, v in data.get("event_templates", {}).items()
        }
        
        return manager
