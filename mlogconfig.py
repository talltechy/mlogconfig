"""
This module provides a configurable logging setup for Python applications.

It supports logging to console, file, syslog (for Linux and macOS), and Windows
Event Log. The user can enable or disable each logging method as needed.
"""

# Standard library imports
import os
import sys
import datetime
import platform
import logging
import argparse
from logging import Formatter, StreamHandler, FileHandler, getLogger
from logging.handlers import SysLogHandler
from typing import Tuple, Union


# Third-party imports
# The following imports are required for Windows Event Log support.
# If you see an import error in Pylance, it can be safely ignored.
if platform.system() == "Windows":
    try:
        import pywintypes
        import win32evtlog
        import win32security
        import winerror
        WINDOWS_AVAILABLE = True
    except ImportError:
        WINDOWS_AVAILABLE = False
else:
    WINDOWS_AVAILABLE = False

# Local application/library specific imports
# ...



class EventLogException(Exception):
    """
    Custom exception for Windows event log errors.
    """


class WindowsEventLogHandler(logging.Handler):
    """
    Handler for logging messages to the Windows Event Log.
    """

    def __init__(self, app_name: str):
        super().__init__()
        self.app_name = app_name

    def _logging_level_to_windows_event_type(self, level: int) -> int:
        """
        Maps the logging level to the corresponding Windows event type.
        """
        if level >= logging.ERROR:
            return win32evtlog.EVENTLOG_ERROR_TYPE
        elif level >= logging.WARNING:
            return win32evtlog.EVENTLOG_WARNING_TYPE
        else:
            return win32evtlog.EVENTLOG_INFORMATION_TYPE

    def emit(self, record: logging.LogRecord) -> None:
        if not WINDOWS_AVAILABLE:
            return

        try:
            sid = win32security.LookupAccountName("", os.environ["USERNAME"])[0]
            message = str(record.getMessage())
            event_type = self._logging_level_to_windows_event_type(record.levelno)
            event_id = 1  # Change this to the desired Event ID
            win32evtlog.ReportEvent(
                self.app_name,
                event_id,  # Replace the second argument with the Event ID
                0,
                event_type,
                sid,
                [message],
                b"",
            )
        except (EventLogException, pywintypes.error) as error:
            if isinstance(error, pywintypes.error) and error.winerror == winerror.ERROR_FILE_NOT_FOUND:
                raise FileNotFoundError(error.strerror) from None
            else:
                self.handleError(record)



def validate_log_file(log_file_path: str, mode: str = "a") -> Tuple[FileHandler, str]:
    """
    Validates the log file path and returns a FileHandler instance and the absolute log file path.
    """
    
    log_file_path = os.path.abspath(log_file_path)
    log_dir = os.path.dirname(log_file_path)

    os.makedirs(log_dir, exist_ok=True)

    if mode not in ("a", "w", "x"):
        raise ValueError(
            "Invalid mode. Mode should be 'a' (append), 'w' (overwrite), or 'x' (new file)"
        )

    if not os.access(log_dir, os.W_OK):
        raise PermissionError(f"The directory {log_dir!r} is not writeable.")

    return FileHandler(log_file_path, mode=mode), log_file_path


def setup_logging(
    log_file_path: str,
    error_log_file_path: str,
    console_logging: bool = False,
    syslog_logging: bool = False,
    windows_event_logging: bool = False,
    log_level: Union[int, str] = logging.INFO,
    file_mode: str = "a",
) -> None:
    """
    Sets up logging configuration for an application.
    """
    file_handler, log_file_path = validate_log_file(log_file_path, mode=file_mode)

    root_logger = getLogger()
    root_logger.setLevel(log_level)

    format_str = "%(asctime)s - %(levelname)s: %(message)s"
    formatter = Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_file_handler, error_log_file_path = validate_log_file(error_log_file_path, mode=file_mode)
    if os.path.abspath(log_file_path) == os.path.abspath(error_log_file_path):
        raise ValueError("log_file_path and error_log_file_path should be different.")
    error_file_handler.setFormatter(formatter)
    error_file_handler.setLevel(logging.ERROR)
    root_logger.addHandler(error_file_handler)
    if console_logging:
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if syslog_logging and (platform.system() in ("Linux", "Darwin")):
        syslog_address = (
            "/dev/log" if platform.system() == "Linux" else "/var/run/syslog"
        )
        syslog_handler = SysLogHandler(
            address=syslog_address, facility=SysLogHandler.LOG_USER
        )
        syslog_handler.setFormatter(formatter)
        root_logger.addHandler(syslog_handler)

    if windows_event_logging:
        nt_event_log_handler = WindowsEventLogHandler(app_name=os.path.basename(sys.argv[0]))
        root_logger.addHandler(nt_event_log_handler)

def main() -> None:
    """
    Main function to setup logging and handle command line arguments.
    """
    parser = argparse.ArgumentParser(description="Configurable logging setup for Python applications.")
    parser.add_argument("log_file_path", help="Path to the log file.")
    parser.add_argument("error_log_file_path", help="Path to the error log file.")
    args = parser.parse_args()

    log_file_path = args.log_file_path
    error_log_file_path = args.error_log_file_path

    try:
        setup_logging(
            log_file_path,
            error_log_file_path,
            console_logging=True,
            syslog_logging=True,
            windows_event_logging=True,
            log_level=logging.DEBUG,
        )
    except Exception as error:
        with open(error_log_file_path, "a", encoding="utf-8") as error_log_file:
            error_log_file.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {error}\n"
            )
        raise

if __name__ == "__main__":
    main()
