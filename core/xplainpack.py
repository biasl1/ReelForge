"""
XplainPack Session Management

A focused module for handling XplainPack sessions - specialized folders containing
synchronized video/audio pairs plus metadata for AI content generation.

XplainPack Structure:
- video file (.mov, .mp4, etc.)
- audio file (.mp3, .wav, etc.)
- metadata.json (optional - transcript, transients, etc.)
"""

import json
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

from core.logging_config import log_info, log_error, log_warning


@dataclass
class XplainPackSession:
    """Represents an XplainPack session with metadata"""
    id: str
    name: str
    description: str
    folder_path: str
    video_file: str
    audio_file: str
    metadata_file: Optional[str] = None
    duration: Optional[float] = None
    transcript: Optional[str] = None
    transients: Optional[List[float]] = None
    created_at: str = ""
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'XplainPackSession':
        """Create from dictionary"""
        return cls(**data)


class XplainPackManager:
    """Manages XplainPack sessions for a project"""
    
    def __init__(self, project_directory: Path):
        self.project_directory = project_directory
        self.sessions: Dict[str, XplainPackSession] = {}
    
    def validate_xplainpack(self, folder_path: Path) -> tuple[bool, str]:
        """
        Validate if a folder is a valid XplainPack
        Returns: (is_valid, error_message)
        """
        if not folder_path.is_dir():
            return False, "Path is not a directory"
        
        # Look for video file
        video_extensions = ['.mov', '.mp4', '.avi', '.mkv', '.m4v']
        video_files = []
        for ext in video_extensions:
            video_files.extend(folder_path.glob(f'*{ext}'))
            video_files.extend(folder_path.glob(f'*{ext.upper()}'))
        
        if not video_files:
            return False, "No video file found"
        
        # Look for audio file
        audio_extensions = ['.mp3', '.wav', '.aac', '.m4a', '.flac']
        audio_files = []
        for ext in audio_extensions:
            audio_files.extend(folder_path.glob(f'*{ext}'))
            audio_files.extend(folder_path.glob(f'*{ext.upper()}'))
        
        if not audio_files:
            return False, "No audio file found"
        
        return True, "Valid XplainPack"
    
    def import_xplainpack(self, folder_path: Path) -> Optional[str]:
        """
        Import an XplainPack session
        Returns: session_id if successful, None if failed
        """
        try:
            # Validate
            is_valid, error_msg = self.validate_xplainpack(folder_path)
            if not is_valid:
                log_error(f"Invalid XplainPack: {error_msg}")
                return None
            
            # Find files
            video_files = []
            audio_files = []
            
            for ext in ['.mov', '.mp4', '.avi', '.mkv', '.m4v']:
                video_files.extend(folder_path.glob(f'*{ext}'))
                video_files.extend(folder_path.glob(f'*{ext.upper()}'))
            
            for ext in ['.mp3', '.wav', '.aac', '.m4a', '.flac']:
                audio_files.extend(folder_path.glob(f'*{ext}'))
                audio_files.extend(folder_path.glob(f'*{ext.upper()}'))
            
            video_file = str(video_files[0])
            audio_file = str(audio_files[0])
            
            # Look for metadata
            metadata_file = None
            metadata_path = folder_path / "metadata.json"
            transcript = None
            transients = None
            
            if metadata_path.exists():
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        transcript = metadata.get('transcript', '')
                        transients = metadata.get('transients', [])
                        metadata_file = str(metadata_path)
                except Exception as e:
                    log_warning(f"Could not read metadata file: {e}")
            
            # Create session
            session_id = str(uuid.uuid4())
            session = XplainPackSession(
                id=session_id,
                name=folder_path.name,
                description=f"XplainPack session from {folder_path.name}",
                folder_path=str(folder_path),
                video_file=video_file,
                audio_file=audio_file,
                metadata_file=metadata_file,
                transcript=transcript,
                transients=transients,
                created_at=str(Path(video_file).stat().st_mtime)
            )
            
            # Store session
            self.sessions[session_id] = session
            
            log_info(f"Imported XplainPack session: {session.name} ({session_id})")
            return session_id
            
        except Exception as e:
            log_error(f"Error importing XplainPack {folder_path}: {e}")
            return None
    
    def get_session(self, session_id: str) -> Optional[XplainPackSession]:
        """Get session by ID"""
        return self.sessions.get(session_id)
    
    def get_all_sessions(self) -> List[XplainPackSession]:
        """Get all sessions"""
        return list(self.sessions.values())
    
    def update_session(self, session_id: str, **kwargs) -> bool:
        """Update session metadata"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
        
        log_info(f"Updated XplainPack session: {session_id}")
        return True
    
    def remove_session(self, session_id: str) -> bool:
        """Remove session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            log_info(f"Removed XplainPack session: {session_id}")
            return True
        return False
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize all sessions"""
        return {
            session_id: session.to_dict()
            for session_id, session in self.sessions.items()
        }
    
    def from_dict(self, data: Dict[str, Any]) -> None:
        """Deserialize sessions"""
        self.sessions = {
            session_id: XplainPackSession.from_dict(session_data)
            for session_id, session_data in data.items()
        }
