#!/usr/bin/env python3
"""Debug XplainPack saving issue"""

import json
from pathlib import Path
from core.project import ReelForgeProject
from core.xplainpack import XplainPackSession

def test_xplainpack_save():
    """Test XplainPack session saving"""
    
    # Create a test project
    project = ReelForgeProject()
    project.metadata.name = "Test Project"
    project.project_file_path = Path("/tmp/test_project.rforge")
    
    # Initialize XplainPackManager
    project._initialize_xplainpack_manager()
    
    # Create a test XplainPack session
    test_session = XplainPackSession(
        id="test-session-1",
        name="Test Session",
        description="Test XplainPack session",
        folder_path="/tmp/test_xplainpack",
        video_file="/tmp/test_xplainpack/video.mp4",
        audio_file="/tmp/test_xplainpack/audio.mp3",
        metadata_file="/tmp/test_xplainpack/metadata.json",
        transcript="Test transcript",
        transients=[1.0, 2.0, 3.0],
        created_at="2025-07-10"
    )
    
    # Add session to manager
    project.xplainpack_manager.sessions[test_session.id] = test_session
    
    print(f"XplainPackManager initialized: {project.xplainpack_manager is not None}")
    print(f"Number of sessions: {len(project.xplainpack_manager.sessions)}")
    
    # Test to_dict
    project_dict = project.to_dict()
    print(f"Project dict keys: {list(project_dict.keys())}")
    print(f"XplainPack sessions in dict: {len(project_dict.get('xplainpack_sessions', {}))}")
    
    # Test JSON serialization
    try:
        json_str = json.dumps(project_dict, indent=2)
        print("JSON serialization successful")
        
        # Parse back to verify
        parsed = json.loads(json_str)
        print(f"Parsed keys: {list(parsed.keys())}")
        
        if 'xplainpack_sessions' in parsed:
            print(f"XplainPack sessions preserved: {len(parsed['xplainpack_sessions'])}")
            print(f"Session data: {parsed['xplainpack_sessions']}")
        else:
            print("ERROR: XplainPack sessions missing from JSON!")
            
    except Exception as e:
        print(f"JSON serialization error: {e}")
        
    # Test save method
    test_file = Path("/tmp/test_project.rforge")
    if test_file.exists():
        test_file.unlink()
        
    success = project.save(test_file)
    print(f"Save successful: {success}")
    
    if test_file.exists():
        with open(test_file, 'r') as f:
            saved_data = json.load(f)
        print(f"Saved file keys: {list(saved_data.keys())}")
        if 'xplainpack_sessions' in saved_data:
            print(f"XplainPack sessions in saved file: {len(saved_data['xplainpack_sessions'])}")
        else:
            print("ERROR: XplainPack sessions missing from saved file!")

if __name__ == "__main__":
    test_xplainpack_save()
