"""
Template persistence for saving and loading template configurations.
"""
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

from PyQt6.QtCore import QRect
from PyQt6.QtGui import QColor


class TemplatePersistence:
    """
    Handles saving and loading template configurations to/from files.
    """
    
    def __init__(self):
        self.file_version = "1.0"
    
    def save_template(self, config: Dict[str, Any], filepath: str) -> bool:
        """
        Save template configuration to file.
        
        Args:
            config: Template configuration dictionary
            filepath: Path to save file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Prepare data for JSON serialization
            json_data = self._prepare_for_json(config)
            
            # Add metadata
            json_data['metadata'] = {
                'version': self.file_version,
                'created': datetime.now().isoformat(),
                'app': 'ReelTune Template Editor'
            }
            
            # Save to file
            filepath = Path(filepath)
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            
            return True
            
        except Exception as e:
            print(f"Error saving template: {e}")
            return False
    
    def load_template(self, filepath: str) -> Optional[Dict[str, Any]]:
        """
        Load template configuration from file.
        
        Args:
            filepath: Path to template file
            
        Returns:
            Template configuration dictionary or None if failed
        """
        try:
            filepath = Path(filepath)
            if not filepath.exists():
                print(f"Template file not found: {filepath}")
                return None
            
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
            
            # Check version compatibility
            metadata = json_data.get('metadata', {})
            version = metadata.get('version', '1.0')
            
            if version != self.file_version:
                print(f"Warning: Template version {version} may not be fully compatible")
            
            # Convert back from JSON
            config = self._restore_from_json(json_data)
            
            return config
            
        except Exception as e:
            print(f"Error loading template: {e}")
            return None
    
    def _prepare_for_json(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Prepare configuration for JSON serialization.
        Converts Qt objects to JSON-serializable types.
        """
        json_data = {}
        
        for key, value in config.items():
            if key == 'canvas_config':
                json_data[key] = self._convert_canvas_config(value)
            else:
                json_data[key] = self._convert_value(value)
        
        return json_data
    
    def _convert_canvas_config(self, canvas_config: Dict[str, Any]) -> Dict[str, Any]:
        """Convert canvas configuration for JSON."""
        result = {}
        
        for key, value in canvas_config.items():
            if key == 'elements':
                result[key] = self._convert_elements(value)
            else:
                result[key] = self._convert_value(value)
        
        return result
    
    def _convert_elements(self, elements: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Convert elements dictionary for JSON."""
        result = {}
        
        for element_id, element in elements.items():
            result[element_id] = {}
            
            for prop_name, prop_value in element.items():
                if prop_name == 'rect':
                    # Convert QRect to dict
                    rect = prop_value
                    result[element_id][prop_name] = {
                        'x': rect.x(),
                        'y': rect.y(),
                        'width': rect.width(),
                        'height': rect.height()
                    }
                elif prop_name == 'color' or prop_name.endswith('_color'):
                    # Convert QColor to rgba values
                    color = prop_value
                    result[element_id][prop_name] = {
                        'r': color.red(),
                        'g': color.green(),
                        'b': color.blue(),
                        'a': color.alpha()
                    }
                else:
                    result[element_id][prop_name] = self._convert_value(prop_value)
        
        return result
    
    def _convert_value(self, value: Any) -> Any:
        """Convert a single value for JSON serialization."""
        if isinstance(value, QRect):
            return {
                'x': value.x(),
                'y': value.y(),
                'width': value.width(),
                'height': value.height()
            }
        elif isinstance(value, QColor):
            return {
                'r': value.red(),
                'g': value.green(),
                'b': value.blue(),
                'a': value.alpha()
            }
        elif isinstance(value, (dict, list, str, int, float, bool, type(None))):
            return value
        else:
            # Convert unknown types to string representation
            return str(value)
    
    def _restore_from_json(self, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Restore configuration from JSON data.
        Converts JSON data back to Qt objects.
        """
        config = {}
        
        for key, value in json_data.items():
            if key == 'metadata':
                continue  # Skip metadata
            elif key == 'canvas_config':
                config[key] = self._restore_canvas_config(value)
            else:
                config[key] = self._restore_value(value)
        
        return config
    
    def _restore_canvas_config(self, canvas_config: Dict[str, Any]) -> Dict[str, Any]:
        """Restore canvas configuration from JSON."""
        result = {}
        
        for key, value in canvas_config.items():
            if key == 'elements':
                result[key] = self._restore_elements(value)
            else:
                result[key] = self._restore_value(value)
        
        return result
    
    def _restore_elements(self, elements: Dict[str, Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
        """Restore elements dictionary from JSON."""
        result = {}
        
        for element_id, element in elements.items():
            result[element_id] = {}
            
            for prop_name, prop_value in element.items():
                if prop_name == 'rect':
                    # Convert dict back to QRect
                    rect_data = prop_value
                    result[element_id][prop_name] = QRect(
                        rect_data['x'],
                        rect_data['y'],
                        rect_data['width'],
                        rect_data['height']
                    )
                elif prop_name == 'color' or prop_name.endswith('_color'):
                    # Convert rgba dict back to QColor
                    color_data = prop_value
                    result[element_id][prop_name] = QColor(
                        color_data['r'],
                        color_data['g'],
                        color_data['b'],
                        color_data['a']
                    )
                else:
                    result[element_id][prop_name] = self._restore_value(prop_value)
        
        return result
    
    def _restore_value(self, value: Any) -> Any:
        """Restore a single value from JSON."""
        if isinstance(value, dict):
            # Check if it's a special object
            if 'x' in value and 'y' in value and 'width' in value and 'height' in value:
                # It's a QRect
                return QRect(value['x'], value['y'], value['width'], value['height'])
            elif 'r' in value and 'g' in value and 'b' in value and 'a' in value:
                # It's a QColor
                return QColor(value['r'], value['g'], value['b'], value['a'])
            else:
                # Regular dict
                return value
        else:
            return value
    
    def export_for_content_generation(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Export template configuration in format suitable for content generation.
        This creates a simplified version without Qt objects.
        """
        canvas_config = config.get('canvas_config', {})
        
        export_data = {
            'content_type': canvas_config.get('content_type', 'video'),
            'settings': {
                'constrain_to_frame': canvas_config.get('constrain_to_frame', False)
            },
            'elements': {}
        }
        
        # Convert elements to simple format
        elements = canvas_config.get('elements', {})
        for element_id, element in elements.items():
            if not element.get('enabled', True):
                continue
            
            element_data = {
                'type': element['type']
            }
            
            # Add rect as simple dict
            if 'rect' in element:
                rect = element['rect']
                if isinstance(rect, QRect):
                    element_data['rect'] = {
                        'x': rect.x(),
                        'y': rect.y(),
                        'width': rect.width(),
                        'height': rect.height()
                    }
                else:
                    element_data['rect'] = rect
            
            # Add type-specific properties
            if element['type'] == 'text':
                element_data.update({
                    'content': element.get('content', ''),
                    'size': element.get('size', 24),
                    'style': element.get('style', 'normal')
                })
                
                # Convert color to hex string
                color = element.get('color')
                if isinstance(color, QColor):
                    element_data['color'] = color.name()
                else:
                    element_data['color'] = color
                    
            elif element['type'] == 'pip':
                element_data.update({
                    'shape': element.get('shape', 'square')
                })
                
                # Convert colors to hex strings
                for color_prop in ['color', 'border_color']:
                    color = element.get(color_prop)
                    if isinstance(color, QColor):
                        element_data[color_prop] = color.name()
                    else:
                        element_data[color_prop] = color
            
            export_data['elements'][element_id] = element_data
        
        return export_data
