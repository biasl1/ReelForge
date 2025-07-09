#!/usr/bin/env python3
"""
Test script to verify content type isolation for frame descriptions
"""

import sys
sys.path.append('.')
from ui.template_editor.editor import TemplateEditor
from PyQt6.QtWidgets import QApplication

def test_content_isolation():
    # Create app
    app = QApplication([])

    # Create template editor
    template_editor = TemplateEditor()

    print('🧪 TESTING CONTENT TYPE ISOLATION:')
    print('=' * 50)

    # 1. Set content type to reel
    template_editor.set_content_type('reel')
    print('✅ 1. Set content type to REEL')

    # 2. Edit description for reel frame 1 (index 0)
    template_editor.frame_timeline.frame_description_edit.setText('MY CUSTOM REEL DESCRIPTION FOR FRAME 1')
    template_editor.frame_timeline._on_description_changed()
    print('✅ 2. Set reel frame 1 description: "MY CUSTOM REEL DESCRIPTION FOR FRAME 1"')

    # 3. Check the description in canvas for reel
    reel_desc = template_editor.canvas.get_frame_description(0)
    print(f'✅ 3. Canvas reel frame 1 description: "{reel_desc}"')

    # 4. Switch to story content type
    template_editor.set_content_type('story')
    print('✅ 4. Switched content type to STORY')

    # 5. Check description field (should be different)
    story_ui_desc = template_editor.frame_timeline.frame_description_edit.text()
    print(f'✅ 5. Story UI description field: "{story_ui_desc}"')

    # 6. Check the description in canvas for story
    story_desc = template_editor.canvas.get_frame_description(0)
    print(f'✅ 6. Canvas story frame 1 description: "{story_desc}"')

    # 7. Set a different description for story
    template_editor.frame_timeline.frame_description_edit.setText('MY CUSTOM STORY DESCRIPTION FOR FRAME 1')
    template_editor.frame_timeline._on_description_changed()
    print('✅ 7. Set story frame 1 description: "MY CUSTOM STORY DESCRIPTION FOR FRAME 1"')

    # 8. Switch back to reel
    template_editor.set_content_type('reel')
    print('✅ 8. Switched back to REEL')

    # 9. Check if reel description was preserved
    reel_desc_after = template_editor.canvas.get_frame_description(0)
    reel_ui_desc_after = template_editor.frame_timeline.frame_description_edit.text()
    print(f'✅ 9. Reel canvas description after switch: "{reel_desc_after}"')
    print(f'✅ 10. Reel UI description after switch: "{reel_ui_desc_after}"')

    # 10. Final verification - switch back to story
    template_editor.set_content_type('story')
    story_desc_final = template_editor.canvas.get_frame_description(0)
    story_ui_desc_final = template_editor.frame_timeline.frame_description_edit.text()
    print(f'✅ 11. Story canvas description final: "{story_desc_final}"')
    print(f'✅ 12. Story UI description final: "{story_ui_desc_final}"')

    print('')
    print('🔍 RESULTS:')
    if reel_desc_after == 'MY CUSTOM REEL DESCRIPTION FOR FRAME 1' and story_desc_final == 'MY CUSTOM STORY DESCRIPTION FOR FRAME 1':
        print('✅ SUCCESS: Content types are properly isolated!')
        return True
    else:
        print('❌ FAILURE: Content types are still cross-contaminating!')
        print(f'   Expected reel: "MY CUSTOM REEL DESCRIPTION FOR FRAME 1"')
        print(f'   Got reel: "{reel_desc_after}"')
        print(f'   Expected story: "MY CUSTOM STORY DESCRIPTION FOR FRAME 1"')
        print(f'   Got story: "{story_desc_final}"')
        return False

    app.quit()

if __name__ == '__main__':
    test_content_isolation()
