"""
This module provides a configurable logging setup for Python applications.

It supports logging to console, file, syslog (for Linux and macOS), and Windows
Event Log. The user can enable or disable each logging method as needed.
"""

import os
import platform
import logging
from logging import Formatter, StreamHandler, FileHandler, getLogger
from logging.handlers import SysLogHandler
import sys

WIN32_AVAILABLE = platform.system() == "Windows"
if WIN32_AVAILABLE:
    try:
        import pywintypes
        import win32evtlog
        import win32security
        import winerror
    except ImportError:
        WIN32_AVAILABLE = False


class EventLogException(Exception):
    """
    Custom exception for Windows event log errors.
    """
    pass


class WindowsEventLogHandler(logging.Handler):
    """
    Handler for logging messages to the Windows Event Log.
    """

    def __init__(self, appName):
        super().__init__()
        self.appName = appName

    def emit(self, record):
        if not WIN32_AVAILABLE:
            return

        try:
            sid = win32security.LookupAccountName("", os.environ["USERNAME"])[0]
            message = str(record.getMessage())
            win32evtlog.ReportEvent(
                self.appName,
                1,
                0,
                record.levelno,
                sid,
                [message],
                b"",
            )
        except (EventLogException, pywintypes.error) as e:
            if isinstance(e, pywintypes.error) and e.winerror == winerror.ERROR_FILE_NOT_FOUND:
                raise FileNotFoundError(e.strerror) from None
            else:
                self.handleError(record)
        except Exception:
            self.handleError(record)


def validate_log_file(log_file_path, mode="a"):
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
        raise PermissionError(f"The directory '{log_dir}' is not writeable.")

    file_handler = FileHandler(log_file_path, mode=mode)
    return file_handler, log_file_path


def setup_logging(
    log_file_path,
    error_log_file_path,
    console_logging=False,
    syslog_logging=False,
    windows_event_logging=False,
    log_level=logging.INFO,
):
    """
    Sets up logging configuration for an application.
    """
    file_handler, log_file_path = validate_log_file(log_file_path)

    root_logger = getLogger()
    root_logger.setLevel(log_level)

    format_str = "%(asctime)s - %(levelname)s: %(message)s"
    formatter = Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_file_handler, error_log_file_path = validate_log_file(error_log_file_path)
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
        nt_event_log_handler = WindowsEventLogHandler(appName="mlogconfig")
        root_logger.addHandler(nt_event_log_handler)


def main():
    """
    Main function to setup logging and handle command line arguments.
    """
    if len(sys.argv) < 3:
        print("Usage: python mlogconfig.py <log_file_path> <error_log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    error_log_file_path = sys.argv[2]

    try:
        setup_logging(
            log_file_path,
            error_log_file_path,
            console_logging=True,
            syslog_logging=True,
            windows_event_logging=True,
            log_level=logging.DEBUG,
        )
    except Exception as e:
        with open(error_log_file_path, "a", encoding="utf-8") as error_log_file:
            error_log_file.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}\n"
            )
        raise


if __name__ == "__main__":
    main()
