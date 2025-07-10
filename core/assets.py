"""
Asset management utilities for ReelTune
Handles file operations, validation, and metadata extraction
"""

import os
import mimetypes
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


# Supported file types
SUPPORTED_VIDEO_FORMATS = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v'}
SUPPORTED_AUDIO_FORMATS = {'.mp3', '.wav', '.aac', '.m4a', '.flac', '.ogg'}
SUPPORTED_IMAGE_FORMATS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}

ALL_SUPPORTED_FORMATS = SUPPORTED_VIDEO_FORMATS | SUPPORTED_AUDIO_FORMATS | SUPPORTED_IMAGE_FORMATS


@dataclass
class XplainPackInfo:
    """XplainPack information structure"""
    path: Path
    name: str
    video_file: Optional[Path] = None
    audio_file: Optional[Path] = None
    metadata_file: Optional[Path] = None
    description: str = ""
    tags: List[str] = None
    transcript: str = ""
    transients: List[float] = None
    is_valid: bool = False
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = []
        if self.transients is None:
            self.transients = []


@dataclass
class FileInfo:
    """File information structure"""
    path: Path
    name: str
    size: int
    mime_type: str
    file_type: str  # 'video', 'audio', 'image', 'xplainpack', 'other'
    extension: str
    is_supported: bool
    xplainpack_info: Optional[XplainPackInfo] = None


class AssetManager:
    """Manages project assets and file operations"""

    def __init__(self, project_directory: Optional[Path] = None):
        self.project_directory = project_directory

    def set_project_directory(self, directory: Path):
        """Set the project directory"""
        self.project_directory = directory

    def validate_file(self, file_path: Path) -> FileInfo:
        """Validate and get info about a file"""
        try:
            if not file_path.exists():
                raise FileNotFoundError(f"File not found: {file_path}")

            # Check if it's an XplainPack first
            if file_path.is_dir():
                xplainpack_info = self._validate_xplainpack(file_path)
                if xplainpack_info.is_valid:
                    return FileInfo(
                        path=file_path,
                        name=file_path.name,
                        size=self._get_directory_size(file_path),
                        mime_type="application/x-xplainpack",
                        file_type="xplainpack",
                        extension=".xplainpack",
                        is_supported=True,
                        xplainpack_info=xplainpack_info
                    )

            # Regular file validation
            stat = file_path.stat()
            extension = file_path.suffix.lower()

            # Determine file type
            file_type = self._get_file_type(extension)
            is_supported = extension in ALL_SUPPORTED_FORMATS

            # Get MIME type
            mime_type, _ = mimetypes.guess_type(str(file_path))
            mime_type = mime_type or "application/octet-stream"

            return FileInfo(
                path=file_path,
                name=file_path.name,
                size=stat.st_size,
                mime_type=mime_type,
                file_type=file_type,
                extension=extension,
                is_supported=is_supported
            )

        except Exception as e:
            raise ValueError(f"Failed to validate file: {e}")

    def _validate_xplainpack(self, pack_path: Path) -> XplainPackInfo:
        """Validate and analyze an XplainPack directory"""
        pack_info = XplainPackInfo(path=pack_path, name=pack_path.name)
        
        try:
            # Check if it's a proper XplainPack directory
            if not (pack_path.name.endswith('.xplainpack') or 
                   any(pack_path.glob('*.mov')) and any(pack_path.glob('*.mp3') or pack_path.glob('*.wav'))):
                return pack_info
            
            # Find video file (.mov preferred)
            video_files = list(pack_path.glob('*.mov'))
            if not video_files:
                video_files = [f for f in pack_path.iterdir() if f.suffix.lower() in SUPPORTED_VIDEO_FORMATS]
            
            if video_files:
                pack_info.video_file = video_files[0]
            
            # Find audio file
            audio_files = [f for f in pack_path.iterdir() if f.suffix.lower() in SUPPORTED_AUDIO_FORMATS]
            if audio_files:
                pack_info.audio_file = audio_files[0]
            
            # Check for metadata file
            metadata_files = list(pack_path.glob('metadata.json')) or list(pack_path.glob('*.json'))
            if metadata_files:
                pack_info.metadata_file = metadata_files[0]
                pack_info = self._load_xplainpack_metadata(pack_info)
            
            # XplainPack is valid if it has both video and audio
            pack_info.is_valid = pack_info.video_file is not None and pack_info.audio_file is not None
            
            return pack_info
            
        except Exception as e:
            print(f"Error validating XplainPack: {e}")
            return pack_info

    def _load_xplainpack_metadata(self, pack_info: XplainPackInfo) -> XplainPackInfo:
        """Load metadata from XplainPack JSON file"""
        try:
            if not pack_info.metadata_file or not pack_info.metadata_file.exists():
                return pack_info
                
            with open(pack_info.metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
            
            # Extract metadata fields
            pack_info.description = metadata.get('description', '')
            pack_info.tags = metadata.get('tags', [])
            pack_info.transcript = metadata.get('transcript', '')
            pack_info.transients = metadata.get('transients', [])
            
            return pack_info
            
        except Exception as e:
            print(f"Error loading XplainPack metadata: {e}")
            return pack_info

    def _get_directory_size(self, directory: Path) -> int:
        """Get total size of all files in directory"""
        total_size = 0
        try:
            for file_path in directory.rglob('*'):
                if file_path.is_file():
                    total_size += file_path.stat().st_size
        except Exception:
            pass
        return total_size

    def create_xplainpack_session(self, pack_info: XplainPackInfo) -> Dict[str, any]:
        """Create XplainPack session data for export"""
        try:
            session_data = {
                "id": f"session_{self.generate_asset_id(pack_info.path)[:8]}",
                "name": pack_info.name.replace('.xplainpack', ''),
                "path": str(pack_info.path),
                "description": pack_info.description,
                "tags": pack_info.tags,
                "files": {
                    "video": str(pack_info.video_file) if pack_info.video_file else None,
                    "audio": str(pack_info.audio_file) if pack_info.audio_file else None,
                    "metadata": str(pack_info.metadata_file) if pack_info.metadata_file else None
                },
                "transcript": pack_info.transcript,
                "transients": pack_info.transients,
                "duration": self._get_xplainpack_duration(pack_info),
                "is_valid": pack_info.is_valid
            }
            
            return session_data
            
        except Exception as e:
            print(f"Error creating XplainPack session: {e}")
            return {}

    def _get_xplainpack_duration(self, pack_info: XplainPackInfo) -> Optional[float]:
        """Get duration of XplainPack content"""
        try:
            # For now, return None - would need media analysis library
            # TODO: Add ffprobe or similar for duration extraction
            return None
        except Exception:
            return None

    def scan_for_xplainpacks(self, directory: Path) -> List[XplainPackInfo]:
        """Scan directory for XplainPack folders"""
        xplainpacks = []
        try:
            # Look for .xplainpack directories
            for pack_dir in directory.glob('*.xplainpack'):
                if pack_dir.is_dir():
                    pack_info = self._validate_xplainpack(pack_dir)
                    if pack_info.is_valid:
                        xplainpacks.append(pack_info)
            
            # Also look for directories with video + audio pairs
            for item in directory.iterdir():
                if item.is_dir() and not item.name.endswith('.xplainpack'):
                    pack_info = self._validate_xplainpack(item)
                    if pack_info.is_valid:
                        xplainpacks.append(pack_info)
                        
        except Exception as e:
            print(f"Error scanning for XplainPacks: {e}")
            
        return xplainpacks

    def _get_file_type(self, extension: str) -> str:
        """Determine file type from extension"""
        if extension in SUPPORTED_VIDEO_FORMATS:
            return "video"
        elif extension in SUPPORTED_AUDIO_FORMATS:
            return "audio"
        elif extension in SUPPORTED_IMAGE_FORMATS:
            return "image"
        else:
            return "other"

    def generate_asset_id(self, file_path: Path) -> str:
        """Generate unique asset ID based on file path and content"""
        try:
            # Use file path and size for ID generation
            content = f"{file_path.name}_{file_path.stat().st_size}"
            return hashlib.md5(content.encode()).hexdigest()[:12]
        except Exception:
            # Fallback to timestamp-based ID
            import time
            return f"asset_{int(time.time() * 1000)}"

    def copy_asset_to_project(self, source_path: Path,
                            asset_name: Optional[str] = None) -> Optional[Path]:
        """Copy asset file to project directory"""
        try:
            if not self.project_directory:
                raise ValueError("No project directory set")

            # Create assets directory
            assets_dir = self.project_directory / "assets"
            assets_dir.mkdir(exist_ok=True)

            # Determine target filename
            if asset_name:
                target_name = asset_name
                if not target_name.endswith(source_path.suffix):
                    target_name += source_path.suffix
            else:
                target_name = source_path.name

            target_path = assets_dir / target_name

            # Handle name conflicts
            counter = 1
            original_target = target_path
            while target_path.exists():
                stem = original_target.stem
                suffix = original_target.suffix
                target_path = assets_dir / f"{stem}_{counter}{suffix}"
                counter += 1

            # Copy file
            import shutil
            shutil.copy2(source_path, target_path)

            return target_path

        except Exception as e:
            print(f"Error copying asset: {e}")
            return None

    def get_relative_path(self, file_path: Path) -> str:
        """Get relative path from project directory"""
        try:
            if self.project_directory and file_path.is_relative_to(self.project_directory):
                return str(file_path.relative_to(self.project_directory))
            else:
                return str(file_path.absolute())
        except Exception:
            return str(file_path)

    def resolve_asset_path(self, relative_path: str) -> Path:
        """Resolve relative path to absolute path"""
        try:
            path = Path(relative_path)
            if path.is_absolute():
                return path
            elif self.project_directory:
                return self.project_directory / path
            else:
                return path.absolute()
        except Exception:
            return Path(relative_path)

    def scan_directory(self, directory: Path,
                      recursive: bool = True) -> List[FileInfo]:
        """Scan directory for supported media files"""
        try:
            files = []

            if recursive:
                pattern = "**/*"
            else:
                pattern = "*"

            for file_path in directory.glob(pattern):
                if file_path.is_file():
                    try:
                        file_info = self.validate_file(file_path)
                        if file_info.is_supported:
                            files.append(file_info)
                    except Exception:
                        continue  # Skip problematic files

            return files

        except Exception as e:
            print(f"Error scanning directory: {e}")
            return []

    def get_file_preview_info(self, file_path: Path) -> Dict[str, any]:
        """Get preview information for a file (dimensions, duration, etc.)"""
        try:
            file_info = self.validate_file(file_path)
            preview_info = {
                "name": file_info.name,
                "size": file_info.size,
                "type": file_info.file_type,
                "mime_type": file_info.mime_type
            }

            # Add type-specific info
            if file_info.file_type == "image":
                preview_info.update(self._get_image_info(file_path))
            elif file_info.file_type in ["video", "audio"]:
                preview_info.update(self._get_media_info(file_path))

            return preview_info

        except Exception as e:
            return {"error": str(e)}

    def _get_image_info(self, file_path: Path) -> Dict[str, any]:
        """Get image-specific information"""
        try:
            # For now, return basic info
            # TODO: Add PIL/Pillow for image dimensions
            return {
                "dimensions": None,
                "color_mode": None
            }
        except Exception:
            return {}

    def _get_media_info(self, file_path: Path) -> Dict[str, any]:
        """Get video/audio-specific information"""
        try:
            # For now, return basic info
            # TODO: Add ffprobe or similar for media metadata
            return {
                "duration": None,
                "bitrate": None,
                "codec": None
            }
        except Exception:
            return {}

    @staticmethod
    def format_file_size(size_bytes: int) -> str:
        """Format file size in human-readable format"""
        if size_bytes == 0:
            return "0 B"

        size_names = ["B", "KB", "MB", "GB", "TB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)

        return f"{s} {size_names[i]}"

    @staticmethod
    def is_supported_format(file_path: Path) -> bool:
        """Check if file format is supported"""
        return file_path.suffix.lower() in ALL_SUPPORTED_FORMATS
