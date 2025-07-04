"""
Timeline Controls Widget
Provides navigation and configuration controls for the timeline
"""

from datetime import datetime, timedelta
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QComboBox,
    QLabel, QDateEdit, QButtonGroup, QRadioButton, QFrame
)
from PyQt6.QtCore import pyqtSignal, QDate, Qt
from PyQt6.QtGui import QFont


class TimelineControls(QWidget):
    """Controls for timeline navigation and configuration"""

    # Signals
    duration_changed = pyqtSignal(int)  # weeks
    start_date_changed = pyqtSignal(datetime)
    previous_period = pyqtSignal()
    next_period = pyqtSignal()
    today_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_start_date = datetime.now()
        self.current_duration = 4  # Fixed to 4 weeks

        self.setup_ui()
        self.setup_connections()

    def setup_ui(self):
        """Setup the control interface"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        layout.setSpacing(15)

        # Navigation controls
        nav_frame = self.create_navigation_controls()
        layout.addWidget(nav_frame)

        # Separator
        separator2 = QFrame()
        separator2.setFrameShape(QFrame.Shape.VLine)
        separator2.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separator2)

        # Date selection
        date_frame = self.create_date_controls()
        layout.addWidget(date_frame)

        layout.addStretch()

        # Quick actions
        quick_frame = self.create_quick_actions()
        layout.addWidget(quick_frame)

        # Remove the entire create_duration_controls method as it's no longer needed

    def create_navigation_controls(self):
        """Create timeline navigation controls"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Label
        label = QLabel("Navigation")
        label.setStyleSheet("font-weight: bold; color: #cccccc;")
        layout.addWidget(label)

        # Navigation buttons
        nav_layout = QHBoxLayout()
        nav_layout.setSpacing(5)

        self.prev_btn = QPushButton("◀ Previous")
        self.prev_btn.setToolTip("Go to previous period")
        nav_layout.addWidget(self.prev_btn)

        self.next_btn = QPushButton("Next ▶")
        self.next_btn.setToolTip("Go to next period")
        nav_layout.addWidget(self.next_btn)

        layout.addLayout(nav_layout)
        return frame

    def create_date_controls(self):
        """Create date selection controls"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Label
        label = QLabel("Start Date")
        label.setStyleSheet("font-weight: bold; color: #cccccc;")
        layout.addWidget(label)

        # Date picker
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setToolTip("Select timeline start date")
        layout.addWidget(self.date_edit)

        return frame

    def create_quick_actions(self):
        """Create quick action buttons"""
        frame = QFrame()
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Label
        label = QLabel("Quick Actions")
        label.setStyleSheet("font-weight: bold; color: #cccccc;")
        layout.addWidget(label)

        # Buttons
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)

        self.today_btn = QPushButton("Today")
        self.today_btn.setToolTip("Jump to current week")
        button_layout.addWidget(self.today_btn)

        layout.addLayout(button_layout)
        return frame

    def setup_connections(self):
        """Setup signal connections"""
        self.prev_btn.clicked.connect(self.previous_period)
        self.next_btn.clicked.connect(self.next_period)
        self.today_btn.clicked.connect(self.on_today_clicked)
        self.date_edit.dateChanged.connect(self.on_date_changed)

        # Remove duration change method as duration is now fixed

    def on_date_changed(self, qdate):
        """Handle date change"""
        date = datetime(qdate.year(), qdate.month(), qdate.day())
        # Adjust to Monday of the week
        monday = date - timedelta(days=date.weekday())
        self.current_start_date = monday
        self.start_date_changed.emit(monday)

    def on_today_clicked(self):
        """Handle today button click"""
        today = datetime.now()
        monday = today - timedelta(days=today.weekday())

        # Update date picker
        self.date_edit.setDate(QDate(monday.year, monday.month, monday.day))
        self.current_start_date = monday

        self.today_clicked.emit()

    def set_start_date(self, date: datetime):
        """Set the current start date"""
        old_date = self.current_start_date
        self.current_start_date = date
        self.date_edit.setDate(QDate(date.year, date.month, date.day))

        # Emit signal if date actually changed
        if old_date != date:
            self.start_date_changed.emit(date)

    def set_duration(self, weeks: int):
        """Set the current duration - now always 4 weeks"""
        # Duration is fixed to 4 weeks, but keep method for compatibility
        pass

    def get_current_settings(self):
        """Get current timeline settings"""
        return {
            "start_date": self.current_start_date,
            "duration_weeks": self.current_duration
        }
