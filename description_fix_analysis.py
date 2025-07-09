#!/usr/bin/env python3
"""
Direct fix for the frame description persistence issue.
"""

# The issue is in the loading sequence:
# 1. Canvas loads frames with correct descriptions ✅
# 2. Timeline loads its config and overwrites with stale descriptions ❌
# 
# Fix: Modify the project loading to sync timeline descriptions with canvas after both are loaded

print("""
🔧 FRAME DESCRIPTION PERSISTENCE FIX

The issue: Timeline loading overwrites canvas frame descriptions with stale data.

Root cause: In load_template_editor_settings, the sequence is:
1. Canvas loads with correct descriptions  
2. Timeline loads and overwrites with old descriptions
3. User edits are lost on restart

Solution: After loading, sync timeline descriptions with canvas descriptions.
""")

# Let me implement this fix by modifying the loading process
