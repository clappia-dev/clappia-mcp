import sys
from datetime import datetime
from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class LogLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4


class Logger:
    def __init__(
        self,
        name: str = "Logger",
        level: LogLevel = LogLevel.INFO,
        timestamp_format: str = "%Y-%m-%d %H:%M:%S"
    ):
        self.name = name
        self.level = level
        self.timestamp_format = timestamp_format
        
        self.colors = {
            LogLevel.DEBUG: bcolors.OKBLUE,      # Blue
            LogLevel.INFO: bcolors.OKGREEN,      # Green
            LogLevel.WARNING: bcolors.WARNING,   # Yellow
            LogLevel.ERROR: bcolors.FAIL,        # Red
            LogLevel.CRITICAL: bcolors.HEADER    # Magenta
        }
        self.reset_color = bcolors.ENDC
    
    def _should_log(self, level: LogLevel) -> bool:
        """Check if message should be logged based on current log level."""
        return level.value >= self.level.value
    
    def _format_message(self, level: LogLevel, message: str) -> str:
        """Format the log message with timestamp and level."""
        timestamp = datetime.now().strftime(self.timestamp_format)
        return f"[{timestamp}] [{self.name}] [{level.name}] {message}"
    
    def _log(self, level: LogLevel, message: str):
        """Internal logging method."""
        if not self._should_log(level):
            return
        
        message_str = str(message)
        formatted_message = self._format_message(level, message_str)
        
        supports_color = hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()
        
        if supports_color:
            color = self.colors.get(level, '')
            colored_message = f"{color}{formatted_message}{self.reset_color}"
        else:
            colored_message = formatted_message
        
        output_stream = sys.stderr if level.value >= LogLevel.WARNING.value else sys.stdout
        print(colored_message, file=output_stream)
    
    def debug(self, message: str):
        """Log a debug message."""
        self._log(LogLevel.DEBUG, message)
    
    def info(self, message: str):
        """Log an info message."""
        self._log(LogLevel.INFO, message)
    
    def warning(self, message: str):
        """Log a warning message."""
        self._log(LogLevel.WARNING, message)
    
    def error(self, message: str):
        """Log an error message."""
        self._log(LogLevel.ERROR, message)
    
    def critical(self, message: str):
        """Log a critical message."""
        self._log(LogLevel.CRITICAL, message)
    
    def set_level(self, level: LogLevel):
        """Set the minimum log level."""
        self.level = level


_default_logger = Logger()

def get_logger(name: str = "Logger", level: LogLevel = LogLevel.INFO) -> Logger:
    """Get a new logger instance."""
    return Logger(name, level)

def debug(message: str):
    """Log a debug message using default logger."""
    _default_logger.debug(message)

def info(message: str):
    """Log an info message using default logger."""
    _default_logger.info(message)

def warning(message: str):
    """Log a warning message using default logger."""
    _default_logger.warning(message)

def error(message: str):
    """Log an error message using default logger."""
    _default_logger.error(message)

def critical(message: str):
    """Log a critical message using default logger."""
    _default_logger.critical(message)

def set_level(level: LogLevel):
    """Set the level for the default logger."""
    _default_logger.set_level(level)


__all__ = ["get_logger", "set_level", "debug", "info", "warning", "error", "critical", "LogLevel"]