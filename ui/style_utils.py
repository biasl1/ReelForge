"""
Dark theme styling for ReelForge application
VS Code inspired color scheme
"""

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPalette, QColor


# VS Code inspired color palette
class DarkTheme:
    # Background colors
    BACKGROUND_PRIMARY = "#1e1e1e"      # Main background
    BACKGROUND_SECONDARY = "#252526"    # Secondary panels
    BACKGROUND_TERTIARY = "#2d2d30"     # Dialogs, popups
    
    # Text colors  
    TEXT_PRIMARY = "#cccccc"            # Main text
    TEXT_SECONDARY = "#969696"          # Secondary text
    TEXT_DISABLED = "#656565"           # Disabled text
    
    # Accent colors
    ACCENT_BLUE = "#007acc"             # Primary accent
    ACCENT_BLUE_HOVER = "#1177bb"       # Hover state
    ACCENT_BLUE_PRESSED = "#005a9e"     # Pressed state
    
    # Border colors
    BORDER_LIGHT = "#464647"            # Light borders
    BORDER_DARK = "#3c3c3c"             # Dark borders
    
    # Status colors
    SUCCESS = "#4caf50"
    WARNING = "#ff9800" 
    ERROR = "#f44336"
    INFO = "#2196f3"
    
    # Selection colors
    SELECTION = "#094771"               # Selected items
    SELECTION_INACTIVE = "#37373d"      # Inactive selection


def get_app_stylesheet() -> str:
    """Get the main application stylesheet with VS Code dark theme"""
    return f"""
    QMainWindow {{
        background-color: {DarkTheme.BACKGROUND_PRIMARY};
        color: {DarkTheme.TEXT_PRIMARY};
    }}
    
    QMenuBar {{
        background-color: {DarkTheme.BACKGROUND_PRIMARY};
        color: {DarkTheme.TEXT_PRIMARY};
        border-bottom: 1px solid {DarkTheme.BORDER_DARK};
    }}
    
    QMenuBar::item {{
        background-color: transparent;
        padding: 4px 8px;
    }}
    
    QMenuBar::item:selected {{
        background-color: {DarkTheme.SELECTION};
    }}
    
    QMenu {{
        background-color: {DarkTheme.BACKGROUND_TERTIARY};
        color: {DarkTheme.TEXT_PRIMARY};
        border: 1px solid {DarkTheme.BORDER_DARK};
    }}
    
    QMenu::item {{
        padding: 5px 20px;
    }}
    
    QMenu::item:selected {{
        background-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QStatusBar {{
        background-color: {DarkTheme.ACCENT_BLUE};
        color: white;
        border-top: 1px solid {DarkTheme.BORDER_DARK};
    }}
    
    QDialog {{
        background-color: {DarkTheme.BACKGROUND_TERTIARY};
        color: {DarkTheme.TEXT_PRIMARY};
    }}
    
    QLabel {{
        color: {DarkTheme.TEXT_PRIMARY};
    }}
    
    QLineEdit {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        padding: 5px;
        border-radius: 3px;
    }}
    
    QLineEdit:focus {{
        border-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QTextEdit {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        border-radius: 3px;
    }}
    
    QTextEdit:focus {{
        border-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QPushButton {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        padding: 8px 16px;
        border-radius: 4px;
        font-weight: 500;
    }}
    
    QPushButton:hover {{
        background-color: {DarkTheme.BORDER_LIGHT};
    }}
    
    QPushButton:pressed {{
        background-color: {DarkTheme.BORDER_DARK};
    }}
    
    QPushButton:default {{
        background-color: {DarkTheme.ACCENT_BLUE};
        border-color: {DarkTheme.ACCENT_BLUE};
        color: white;
    }}
    
    QPushButton:default:hover {{
        background-color: {DarkTheme.ACCENT_BLUE_HOVER};
    }}
    
    QPushButton:default:pressed {{
        background-color: {DarkTheme.ACCENT_BLUE_PRESSED};
    }}
    
    QComboBox {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        padding: 5px;
        border-radius: 3px;
    }}
    
    QComboBox:focus {{
        border-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QComboBox::drop-down {{
        border: none;
        width: 20px;
    }}
    
    QComboBox::down-arrow {{
        border: none;
    }}
    
    QComboBox QAbstractItemView {{
        background-color: {DarkTheme.BACKGROUND_TERTIARY};
        border: 1px solid {DarkTheme.BORDER_DARK};
        selection-background-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QListWidget {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        border-radius: 3px;
    }}
    
    QListWidget::item {{
        padding: 8px;
        border-bottom: 1px solid {DarkTheme.BORDER_DARK};
    }}
    
    QListWidget::item:selected {{
        background-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QTreeWidget {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        color: {DarkTheme.TEXT_PRIMARY};
        border-radius: 3px;
    }}
    
    QTreeWidget::item {{
        padding: 4px;
    }}
    
    QTreeWidget::item:selected {{
        background-color: {DarkTheme.ACCENT_BLUE};
    }}
    
    QSplitter::handle {{
        background-color: {DarkTheme.BORDER_DARK};
    }}
    
    QSplitter::handle:horizontal {{
        width: 2px;
    }}
    
    QSplitter::handle:vertical {{
        height: 2px;
    }}
    
    QGroupBox {{
        font-weight: bold;
        border: 1px solid {DarkTheme.BORDER_LIGHT};
        border-radius: 4px;
        margin-top: 8px;
        padding-top: 8px;
    }}
    
    QGroupBox::title {{
        subcontrol-origin: margin;
        left: 8px;
        padding: 0 4px 0 4px;
    }}
    
    QScrollBar:vertical {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        width: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical {{
        background-color: {DarkTheme.BORDER_LIGHT};
        min-height: 20px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:vertical:hover {{
        background-color: {DarkTheme.TEXT_SECONDARY};
    }}
    
    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
        border: none;
        background: none;
    }}
    
    QScrollBar:horizontal {{
        background-color: {DarkTheme.BACKGROUND_SECONDARY};
        height: 12px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal {{
        background-color: {DarkTheme.BORDER_LIGHT};
        min-width: 20px;
        border-radius: 6px;
    }}
    
    QScrollBar::handle:horizontal:hover {{
        background-color: {DarkTheme.TEXT_SECONDARY};
    }}
    
    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
        border: none;
        background: none;
    }}
    """


def apply_dark_theme(app: QApplication):
    """Apply dark theme to the application"""
    
    # Set application style
    app.setStyle("Fusion")
    
    # Create dark palette
    palette = QPalette()
    
    # Window colors
    palette.setColor(QPalette.ColorRole.Window, QColor(DarkTheme.BACKGROUND_PRIMARY))
    palette.setColor(QPalette.ColorRole.WindowText, QColor(DarkTheme.TEXT_PRIMARY))
    
    # Base colors (input fields, etc.)
    palette.setColor(QPalette.ColorRole.Base, QColor(DarkTheme.BACKGROUND_SECONDARY))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor(DarkTheme.BACKGROUND_TERTIARY))
    
    # Text colors
    palette.setColor(QPalette.ColorRole.Text, QColor(DarkTheme.TEXT_PRIMARY))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    
    # Button colors
    palette.setColor(QPalette.ColorRole.Button, QColor(DarkTheme.BACKGROUND_SECONDARY))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor(DarkTheme.TEXT_PRIMARY))
    
    # Highlight colors
    palette.setColor(QPalette.ColorRole.Highlight, QColor(DarkTheme.ACCENT_BLUE))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    
    # Disabled colors
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.WindowText, 
                    QColor(DarkTheme.TEXT_DISABLED))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.Text, 
                    QColor(DarkTheme.TEXT_DISABLED))
    palette.setColor(QPalette.ColorGroup.Disabled, QPalette.ColorRole.ButtonText, 
                    QColor(DarkTheme.TEXT_DISABLED))
    
    # Apply palette
    app.setPalette(palette)
    
    # Apply the stylesheet as well
    app.setStyleSheet(get_app_stylesheet())