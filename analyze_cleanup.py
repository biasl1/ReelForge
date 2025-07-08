#!/usr/bin/env python3
"""
Cleanup script to identify and remove unused artifacts from ReelTune codebase
"""

import os
import re
from pathlib import Path

def identify_cleanup_candidates():
    """Identify files that can be removed"""
    root_dir = Path(".")
    
    # Test files that are likely outdated/unused
    test_patterns = [
        "test_*.py",
        "debug_*.py", 
        "demo_*.py",
        "*_test.py",
        "*_demo.py",
        "fix_*.py",
        "cleanup_*.py",
        "migrate_*.py"
    ]
    
    # Files to definitely keep (core functionality)
    keep_files = {
        "main.py",
        "test_templates.py",  # Main test file
        "run_tests.py",       # Test runner
        "test_complete_export.py"  # Latest comprehensive test
    }
    
    cleanup_candidates = []
    
    # Find test/debug files
    for pattern in test_patterns:
        for file_path in root_dir.glob(pattern):
            if file_path.name not in keep_files:
                cleanup_candidates.append(file_path)
    
    return cleanup_candidates

def check_ui_modules():
    """Check UI modules for unused components"""
    ui_dir = Path("ui")
    if not ui_dir.exists():
        return []
    
    ui_files = list(ui_dir.glob("*.py"))
    unused_ui = []
    
    # Check if UI files are imported anywhere
    for ui_file in ui_files:
        if ui_file.name == "__init__.py":
            continue
            
        module_name = ui_file.stem
        is_used = False
        
        # Check if imported in main files
        for check_file in ["main.py", "ui/mainwindow.py"]:
            if Path(check_file).exists():
                with open(check_file, 'r') as f:
                    content = f.read()
                    if module_name in content:
                        is_used = True
                        break
        
        if not is_used:
            unused_ui.append(ui_file)
    
    return unused_ui

def analyze_core_modules():
    """Analyze core modules for unused code"""
    core_dir = Path("core")
    analysis = {}
    
    for core_file in core_dir.glob("*.py"):
        if core_file.name == "__init__.py":
            continue
            
        with open(core_file, 'r') as f:
            content = f.read()
            
        # Count classes and functions
        classes = re.findall(r'^class\s+(\w+)', content, re.MULTILINE)
        functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
        
        analysis[core_file.name] = {
            "classes": classes,
            "functions": functions,
            "size_kb": core_file.stat().st_size / 1024
        }
    
    return analysis

if __name__ == "__main__":
    print("🧹 REELTUNE CODEBASE CLEANUP ANALYSIS")
    print("=" * 50)
    
    # Find cleanup candidates
    print("\n📁 CLEANUP CANDIDATES:")
    candidates = identify_cleanup_candidates()
    for candidate in candidates:
        size_kb = candidate.stat().st_size / 1024
        print(f"  🗑️  {candidate} ({size_kb:.1f} KB)")
    
    print(f"\nTotal files to clean: {len(candidates)}")
    
    # Check UI modules
    print("\n🎨 UI MODULE ANALYSIS:")
    unused_ui = check_ui_modules()
    for ui_file in unused_ui:
        size_kb = ui_file.stat().st_size / 1024
        print(f"  ❓ {ui_file} - Potentially unused ({size_kb:.1f} KB)")
    
    # Analyze core modules
    print("\n⚙️  CORE MODULE ANALYSIS:")
    core_analysis = analyze_core_modules()
    for module, info in core_analysis.items():
        print(f"  📦 {module} ({info['size_kb']:.1f} KB)")
        print(f"     Classes: {len(info['classes'])}, Functions: {len(info['functions'])}")
    
    print("\n🎯 RECOMMENDATIONS:")
    print("1. Remove test/debug files listed above")
    print("2. Check unused UI modules")
    print("3. Review core modules for dead code")
    print("4. Consolidate similar functionality")
