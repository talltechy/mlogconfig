"""
mlogconfig.py
A simple logging setup utility that configures logging with file,
console, syslog, and Windows event log handlers.
"""

import os
import platform
import logging
import datetime

from logging import Formatter, getLogger
from logging.handlers import SysLogHandler

try:
    from logging.handlers import NTEventLogHandler
except ImportError:
    NTEventLogHandler = None

from logging import FileHandler, StreamHandler


def validate_log_file(log_file_path, mode="a"):
    """
    Validate the log file path and create a file handler for it.

    :param log_file_path: Path to the log file
    :param mode: File mode for the log file, either 'a' (append), 'w' (overwrite), or 'n' (new file)
    :return: File handler and the validated log file path
    :rtype: tuple
    """
    if mode not in ("a", "w", "n"):
        raise ValueError(
            "Invalid mode. Mode should be 'a' (append), 'w' (overwrite), or 'n' (new file)"
        )

    log_dir = os.path.dirname(log_file_path)

    # Create directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.access(log_dir, os.W_OK):
        raise PermissionError(f"The directory '{log_dir}' is not writeable.")

    if mode == "n":
        if os.path.exists(log_file_path):
            raise FileExistsError(
                f"The logfile '{log_file_path}' already exists. Please choose a different path for the new file."
            )
        else:
            mode = "a"

    file_handler = FileHandler(log_file_path, mode=mode)
    return file_handler, log_file_path


def setup_logging(
    log_file_path,
    error_log_file_path,
    console_logging=False,
    syslog_logging=False,
    windows_event_logging=False,
):
    """
    Set up logging with a file and optionally a syslog or Windows event log handler.

    :param log_file_path: Path to the log file
    :param error_log_file_path: Path to the error log file
    :param console_logging: Whether to enable console logging or not
    :param syslog_logging: Whether to enable syslog logging or not
    :param windows_event_logging: Whether to enable Windows event logging or not
    :rtype: None
    """
    file_handler, log_file_path = validate_log_file(log_file_path)

    root_logger = getLogger()
    root_logger.setLevel(logging.INFO)

    format_str = "%(asctime)s - %(levelname)s: %(message)s"
    formatter = Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_file_handler, error_log_file_path = validate_log_file(error_log_file_path)
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

    if windows_event_logging and platform.system() == "Windows" and NTEventLogHandler:
        nt_event_log_handler = NTEventLogHandler("Application")
        nt_event_log_handler.setFormatter(formatter)
        root_logger.addHandler(nt_event_log_handler)


if __name__ == "__main__":
    try:
        setup_logging(
            "./log_file.log",
            "./error_log_file.log",
            console_logging=True,
            syslog_logging=True,
            windows_event_logging=True,
        )
    except Exception as e:
        error_log_file_path = "./error_log_file.log"
        with open(error_log_file_path, "a") as error_log_file:
            error_log_file.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}\n"
            )
        raise
