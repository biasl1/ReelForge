#!/usr/bin/env python3
"""
Migration script to update imports from old template editor to new modular one.
"""
import re
from pathlib import Path


def update_imports_in_file(file_path: Path):
    """Update imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Replace import statements
        replacements = [
            (r'from ui\.ai_template_editor import SimpleTemplateEditor', 
             'from ui.template_editor import TemplateEditor'),
            (r'from ui\.ai_template_editor import AITemplateEditor', 
             'from ui.template_editor import TemplateEditor'),
            (r'from ui\.ai_template_editor import VisualTemplateEditor', 
             'from ui.template_editor import TemplateCanvas'),
            (r'from ui\.ai_template_editor import SimpleTemplateEditor, VisualTemplateEditor', 
             'from ui.template_editor import TemplateEditor, TemplateCanvas'),
            
            # Replace class usage
            (r'\bSimpleTemplateEditor\b', 'TemplateEditor'),
            (r'\bAITemplateEditor\b', 'TemplateEditor'),
            (r'\bVisualTemplateEditor\b', 'TemplateCanvas'),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        # Only write if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Updated {file_path}")
            return True
        
        return False
        
    except Exception as e:
        print(f"❌ Error updating {file_path}: {e}")
        return False


def main():
    """Main migration function."""
    print("🔄 Migrating imports to new template editor...")
    print("=" * 50)
    
    project_root = Path(__file__).parent
    
    # Files to update
    files_to_update = [
        # Test files
        project_root / "test_visual_independence.py",
        project_root / "test_template_save.py", 
        project_root / "test_drag_save.py",
        project_root / "test_comprehensive_visual.py",
        project_root / "test_complete_workflow.py",
        project_root / "test_persistence.py",
        project_root / "test_position_persistence.py",
        project_root / "test_visual_constraints.py",
        project_root / "test_zoom_pan_unconstrained.py",
        
        # Demo files
        project_root / "demo_ai_template_editor.py",
        project_root / "demo_super_smart_ai_template_editor.py",
        project_root / "demo_beautiful_ai_template.py",
        
        # Debug files
        project_root / "debug_template_save.py",
        project_root / "debug_new_editor.py",
        project_root / "debug_save_load.py",
    ]
    
    updated_count = 0
    
    for file_path in files_to_update:
        if file_path.exists():
            if update_imports_in_file(file_path):
                updated_count += 1
        else:
            print(f"⚠️  File not found: {file_path}")
    
    print(f"\n✅ Migration complete! Updated {updated_count} files.")
    print("\nNext steps:")
    print("1. Test that updated files still work")
    print("2. Delete old duplicate template editor files")
    print("3. Commit the cleaned-up codebase")


if __name__ == "__main__":
    main()
