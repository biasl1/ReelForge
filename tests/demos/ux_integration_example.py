"""
Quick integration example for existing ReelTune main window
Shows how to add UX improvements to the current app
"""

from ui.ux_improvements import QuickActionToolbar, AutoSaveIndicator, ProjectProgressIndicator


def add_ux_improvements_to_main_window(main_window):
    """Add UX improvements to existing main window"""

    # 1. Add Quick Action Toolbar above timeline
    if hasattr(main_window, 'center_panel'):
        layout = main_window.center_panel.layout()

        # Create and connect toolbar
        quick_toolbar = QuickActionToolbar()
        quick_toolbar.quick_event_requested.connect(
            lambda content_type: create_quick_event(main_window, content_type)
        )

        # Insert at top of layout
        layout.insertWidget(0, quick_toolbar)
        print("✅ Quick Action Toolbar added")

    # 2. Enhance status bar
    if hasattr(main_window, 'status_bar'):
        # Add auto-save indicator
        save_indicator = AutoSaveIndicator()
        main_window.status_bar.addPermanentWidget(save_indicator)

        # Add progress indicator
        progress_indicator = ProjectProgressIndicator()
        main_window.status_bar.addPermanentWidget(progress_indicator)

        # Store references for later use
        main_window.save_indicator = save_indicator
        main_window.progress_indicator = progress_indicator
        print("✅ Enhanced status bar with indicators")


def create_quick_event(main_window, content_type):
    """Create a quick event with template"""
    try:
        from datetime import datetime
        from core.project import ReleaseEvent
        from ui.ux_improvements import ContentTypeTemplates

        if not main_window.current_project:
            print("No project loaded")
            return

        # Get plugin name for template
        plugin_name = "Your Plugin"
        if main_window.current_project.current_plugin:
            plugin_info = main_window.current_project.get_current_plugin_info()
            if plugin_info:
                plugin_name = plugin_info.name

        # Get template
        template = ContentTypeTemplates.get_template(content_type, plugin_name)

        # Create event for today
        today = datetime.now().date().isoformat()
        event = ReleaseEvent(
            id="",  # Auto-generated
            date=today,
            content_type=content_type,
            title=template.get("title", f"New {content_type.title()}"),
            description=template.get("description", ""),
            duration_seconds=template.get("duration_seconds", 30),
            platforms=template.get("platforms", []),
            hashtags=template.get("hashtags", [])
        )

        # Add to project
        success = main_window.current_project.add_release_event(event)
        if success:
            main_window._update_timeline_display()

            # Update status indicators
            if hasattr(main_window, 'save_indicator'):
                main_window.save_indicator.set_unsaved_changes()
            if hasattr(main_window, 'progress_indicator'):
                update_progress_display(main_window)

            print(f"✅ Quick created {content_type} event: {event.title}")

    except Exception as e:
        print(f"❌ Error creating quick event: {e}")


def update_progress_display(main_window):
    """Update the progress indicator"""
    if not hasattr(main_window, 'progress_indicator') or not main_window.current_project:
        return

    project = main_window.current_project
    total_events = len(project.release_events)
    completed_events = len([e for e in project.release_events.values() if e.status == "published"])

    main_window.progress_indicator.update_progress(total_events, completed_events)


# Usage example:
"""
# In your main window __init__ method, add:
add_ux_improvements_to_main_window(self)

# The improvements will be automatically integrated!
"""
