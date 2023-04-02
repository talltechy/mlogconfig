# Description: This file contains the setup_logging function that sets up the logging for the application.

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