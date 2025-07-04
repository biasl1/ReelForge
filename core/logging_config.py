"""
Logging configuration for ReelTune
Provides structured logging instead of print statements
"""

import logging
import sys
from pathlib import Path
from datetime import datetime

class ReelTuneLogger:
    """Centralized logging for ReelTune application"""

    def __init__(self, name: str = "ReelTune"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)

        # Prevent duplicate handlers
        if not self.logger.handlers:
            self._setup_handlers()

    def _setup_handlers(self):
        """Setup console and file handlers"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File handler (optional)
        try:
            from PyQt6.QtCore import QStandardPaths
            app_data = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.AppDataLocation
            )
            log_dir = Path(app_data) / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)

            log_file = log_dir / f"reeltune_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)
        except Exception:
            # If file logging fails, continue with console only
            pass

    def info(self, message: str):
        """Log info level message"""
        self.logger.info(message)

    def debug(self, message: str):
        """Log debug level message"""
        self.logger.debug(message)

    def warning(self, message: str):
        """Log warning level message"""
        self.logger.warning(message)

    def error(self, message: str, exc_info: bool = False):
        """Log error level message"""
        self.logger.error(message, exc_info=exc_info)

# Global logger instance
logger = ReelTuneLogger()

# Convenience functions
def log_info(message: str):
    logger.info(message)

def log_debug(message: str):
    logger.debug(message)

def log_warning(message: str):
    logger.warning(message)

def log_error(message: str, exc_info: bool = False):
    logger.error(message, exc_info=exc_info)
