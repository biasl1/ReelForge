"""
Timeline Canvas Widget
Main visual timeline for content planning with clickable day cells
"""

from datetime import datetime, timedelta
from typing import List, Dict, Optional
from PyQt6.QtWidgets import (
    QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QLabel, 
    QFrame, QPushButton, QScrollArea, QSizePolicy
)
from PyQt6.QtCore import pyqtSignal, Qt, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QPen, QBrush, QMouseEvent

from core.project import ReleaseEvent


class DayCell(QFrame):
    """Individual day cell in the timeline"""
    
    clicked = pyqtSignal(datetime)
    double_clicked = pyqtSignal(datetime)
    edit_event_requested = pyqtSignal(object)  # ReleaseEvent
    delete_event_requested = pyqtSignal(object)  # ReleaseEvent
    
    def __init__(self, date: datetime, parent=None):
        super().__init__(parent)
        self.date = date
        self.events: List[ReleaseEvent] = []
        self.is_selected = False
        self.is_today = date.date() == datetime.now().date()
        
        self.setup_ui()
        self.setup_styling()
        
    def setup_ui(self):
        """Setup the day cell UI"""
        self.setMinimumSize(120, 100)
        self.setMaximumSize(200, 150)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(2)
        
        # Day number and name
        self.day_label = QLabel(f"{self.date.day}")
        self.day_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        self.day_label.setFont(font)
        layout.addWidget(self.day_label)
        
        # Day name (Mon, Tue, etc.)
        day_name = self.date.strftime("%a")
        self.name_label = QLabel(day_name)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.name_label.setStyleSheet("color: #969696; font-size: 10px;")
        layout.addWidget(self.name_label)
        
        # Events container
        self.events_container = QWidget()
        self.events_layout = QVBoxLayout(self.events_container)
        self.events_layout.setContentsMargins(0, 0, 0, 0)
        self.events_layout.setSpacing(1)
        layout.addWidget(self.events_container)
        
        layout.addStretch()
        
    def setup_styling(self):
        """Setup cell styling"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(1)
        self.update_style()
        
    def update_style(self):
        """Update styling based on state"""
        if self.is_selected:
            border_color = "#007acc"
            bg_color = "#094771"
        elif self.is_today:
            border_color = "#007acc"
            bg_color = "#252526"
        else:
            border_color = "#464647"
            bg_color = "#252526"
            
        # Darker background for weekends
        if self.date.weekday() >= 5:  # Saturday = 5, Sunday = 6
            bg_color = "#1e1e1e"
            
        style = f"""
        DayCell {{
            border: 1px solid {border_color};
            background-color: {bg_color};
            border-radius: 3px;
        }}
        DayCell:hover {{
            border: 1px solid #007acc;
            background-color: #2a2d2e;
        }}
        """
        self.setStyleSheet(style)
        
        # Update day label color
        if self.is_today:
            self.day_label.setStyleSheet("color: #007acc; font-weight: bold;")
        elif self.date.weekday() >= 5:
            self.day_label.setStyleSheet("color: #969696;")
        else:
            self.day_label.setStyleSheet("color: #cccccc;")
            
    def set_events(self, events: List[ReleaseEvent]):
        """Set events for this day"""
        self.events = events
        self.update_events_display()
        
    def update_events_display(self):
        """Update the visual display of events"""
        # Clear existing event widgets safely
        for i in reversed(range(self.events_layout.count())):
            child = self.events_layout.itemAt(i)
            if child:
                widget = child.widget()
                if widget:
                    self.events_layout.removeWidget(widget)
                    widget.deleteLater()
                    
        # Add event indicators
        for event in self.events[:3]:  # Show max 3 events
            event_widget = self.create_event_indicator(event)
            self.events_layout.addWidget(event_widget)
            
        # Show count if more events
        if len(self.events) > 3:
            more_label = QLabel(f"+{len(self.events) - 3} more")
            more_label.setStyleSheet("color: #007acc; font-size: 9px; font-style: italic;")
            more_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.events_layout.addWidget(more_label)
            
    def create_event_indicator(self, event: ReleaseEvent) -> QWidget:
        """Create visual indicator for an event"""
        indicator = QLabel()
        indicator.setMaximumHeight(16)
        indicator.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Color coding by content type
        colors = {
            "reel": "#ff4444",      # Red
            "story": "#9c27b0",     # Purple  
            "post": "#2196f3",      # Blue
            "teaser": "#ff9800",    # Orange
            "tutorial": "#4caf50"   # Green
        }
        
        color = colors.get(event.content_type, "#cccccc")
        
        # Create styled indicator
        indicator.setText(f"● {event.content_type.title()}")
        indicator.setStyleSheet(f"""
            color: {color};
            font-size: 9px;
            font-weight: bold;
            padding: 1px 3px;
            border-radius: 2px;
            background-color: rgba{tuple(QColor(color).getRgb()[:3]) + (40,)};
        """)
        
        indicator.setToolTip(f"{event.title}\n{event.description}")
        
        return indicator
        
    def set_selected(self, selected: bool):
        """Set selection state"""
        self.is_selected = selected
        self.update_style()
        
    def mousePressEvent(self, event: QMouseEvent):
        """Handle mouse press"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit(self.date)
        super().mousePressEvent(event)
        
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """Handle double click"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.double_clicked.emit(self.date)
        super().mouseDoubleClickEvent(event)
        
    def contextMenuEvent(self, event):
        """Handle right-click context menu"""
        from PyQt6.QtWidgets import QMenu
        
        menu = QMenu(self)
        
        if self.events:
            # If there are events, show edit/delete options
            if len(self.events) == 1:
                edit_action = menu.addAction(f"Edit '{self.events[0].title}'")
                edit_action.triggered.connect(lambda: self.edit_event(self.events[0]))
                
                delete_action = menu.addAction(f"Delete '{self.events[0].title}'")
                delete_action.triggered.connect(lambda: self.delete_event(self.events[0]))
            else:
                # Multiple events - show submenu
                edit_menu = menu.addMenu("Edit Event")
                delete_menu = menu.addMenu("Delete Event")
                
                for event_item in self.events:
                    edit_action = edit_menu.addAction(f"'{event_item.title}'")
                    edit_action.triggered.connect(lambda checked, e=event_item: self.edit_event(e))
                    
                    delete_action = delete_menu.addAction(f"'{event_item.title}'")
                    delete_action.triggered.connect(lambda checked, e=event_item: self.delete_event(e))
            
            menu.addSeparator()
        
        # Always show "Add Event" option
        add_action = menu.addAction("Add Event")
        add_action.triggered.connect(lambda: self.double_clicked.emit(self.date))
        
        menu.exec(event.globalPos())
        
    def edit_event(self, event):
        """Signal to edit an event"""
        self.edit_event_requested.emit(event)
        
    def delete_event(self, event):
        """Signal to delete an event"""
        self.delete_event_requested.emit(event)


class TimelineCanvas(QScrollArea):
    """Main timeline canvas widget"""
    
    day_selected = pyqtSignal(datetime)
    day_double_clicked = pyqtSignal(datetime)
    edit_event_requested = pyqtSignal(object)  # ReleaseEvent
    delete_event_requested = pyqtSignal(object)  # ReleaseEvent
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.current_start_date = datetime.now()
        self.duration_weeks = 1
        self.selected_date: Optional[datetime] = None
        self.day_cells: Dict[str, DayCell] = {}
        
        self.setup_ui()
        self.rebuild_timeline()
        
    def setup_ui(self):
        """Setup the timeline canvas UI"""
        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Create main content widget
        self.content_widget = QWidget()
        self.setWidget(self.content_widget)
        
        # Main layout
        self.main_layout = QVBoxLayout(self.content_widget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        
    def rebuild_timeline(self):
        """Rebuild the timeline grid"""
        # Clear existing layout
        while self.main_layout.count():
            child = self.main_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        self.day_cells.clear()
        
        # Calculate date range
        start_date = self.current_start_date
        # Ensure start date is Monday
        start_date = start_date - timedelta(days=start_date.weekday())
        
        # Create week grids
        for week in range(self.duration_weeks):
            week_widget = self.create_week_widget(start_date + timedelta(weeks=week))
            self.main_layout.addWidget(week_widget)
            
        self.main_layout.addStretch()
        
    def create_week_widget(self, week_start: datetime) -> QWidget:
        """Create a widget for one week"""
        week_widget = QFrame()
        week_widget.setFrameStyle(QFrame.Shape.Box)
        week_widget.setStyleSheet("""
            QFrame {
                border: 1px solid #3c3c3c;
                border-radius: 5px;
                background-color: #1e1e1e;
                margin: 2px;
            }
        """)
        
        layout = QVBoxLayout(week_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(5)
        
        # Week header
        week_label = QLabel(f"Week of {week_start.strftime('%B %d, %Y')}")
        week_label.setStyleSheet("color: #cccccc; font-weight: bold; font-size: 12px;")
        layout.addWidget(week_label)
        
        # Days grid
        days_layout = QHBoxLayout()
        days_layout.setSpacing(5)
        
        for day in range(7):  # Monday to Sunday
            current_date = week_start + timedelta(days=day)
            day_cell = DayCell(current_date)
            
            # Connect signals
            day_cell.clicked.connect(self.on_day_clicked)
            day_cell.double_clicked.connect(self.day_double_clicked)
            day_cell.edit_event_requested.connect(self.edit_event_requested)
            day_cell.delete_event_requested.connect(self.delete_event_requested)
            
            # Store reference
            date_key = current_date.date().isoformat()
            self.day_cells[date_key] = day_cell
            
            days_layout.addWidget(day_cell)
            
        layout.addLayout(days_layout)
        
        return week_widget
        
    def on_day_clicked(self, date: datetime):
        """Handle day cell click"""
        # Update selection
        if self.selected_date:
            old_key = self.selected_date.date().isoformat()
            if old_key in self.day_cells:
                self.day_cells[old_key].set_selected(False)
                
        self.selected_date = date
        date_key = date.date().isoformat()
        if date_key in self.day_cells:
            self.day_cells[date_key].set_selected(True)
            
        self.day_selected.emit(date)
        
    def set_duration(self, weeks: int):
        """Set timeline duration"""
        if 1 <= weeks <= 4 and weeks != self.duration_weeks:
            self.duration_weeks = weeks
            self.rebuild_timeline()
            
    def set_start_date(self, date: datetime):
        """Set timeline start date"""
        if date != self.current_start_date:
            self.current_start_date = date
            self.rebuild_timeline()
        
    def update_events(self, events_by_date: Dict[str, List[ReleaseEvent]]):
        """Update events display on timeline"""
        # First, clear all existing events from all day cells
        for day_cell in self.day_cells.values():
            day_cell.set_events([])
            
        # Then set events for dates that have them
        for date_str, events in events_by_date.items():
            if date_str in self.day_cells:
                self.day_cells[date_str].set_events(events)
                
    def clear_selection(self):
        """Clear current selection"""
        if self.selected_date:
            date_key = self.selected_date.date().isoformat()
            if date_key in self.day_cells:
                self.day_cells[date_key].set_selected(False)
            self.selected_date = None
            
    def get_selected_date(self) -> Optional[datetime]:
        """Get currently selected date"""
        return self.selected_date
