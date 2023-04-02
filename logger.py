# This code sets up the logging module for a script. It will write logs to a file, to the console, and to the system log if the platform supports it.
# It takes a single argument, which is the path to the log file that it will write to.
# The log file is set to log at the INFO level, so all messages logged at the INFO level or above will be written to the log file.
# The console is set to log at the INFO level, so all messages logged at the INFO level or above will be written to the console.
# The system log is set to log at the INFO level, so all messages logged at the INFO level or above will be written to the system log.
# The file path is passed to the script as an argument, so it is provided by the user.

import logging
from logging import Formatter, FileHandler, StreamHandler, getLogger
from logging.handlers import SysLogHandler, NTEventLogHandler
import platform

def setup_logging(log_file_path):
    # Get the root logger.
    root_logger = getLogger()

    # Set the root logger level to INFO.
    root_logger.setLevel(logging.INFO)

    # Create a formatter to use for the handlers.
    formatter = Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Create a file handler and set the formatter.
    file_handler = FileHandler(log_file_path)
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger.
    root_logger.addHandler(file_handler)

    # Create a console handler and set the formatter.
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger.
    root_logger.addHandler(console_handler)

    # If on Linux, try to create a syslog handler and add it to the root logger.
    if platform.system() == 'Linux':
        try:
            syslog_handler = SysLogHandler(address='/dev/log')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")
    # If on macOS, try to create a syslog handler and add it to the root logger.
    elif platform.system() == 'Darwin':
        try:
            syslog_handler = SysLogHandler(address='/var/run/syslog')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")
    # If on Windows, try to create a syslog handler and add it to the root logger.
    elif platform.system() == 'Windows':
        try:
            nt_event_log_handler = NTEventLogHandler("Application")
            nt_event_log_handler.setFormatter(formatter)
            root_logger.addHandler(nt_event_log_handler)
        except ImportError:
            print("pywin32 is required to write to Windows event log. Please install it using: pip install pywin32")