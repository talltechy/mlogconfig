"""
This module provides a configurable logging setup for Python applications.

It supports logging to console, file, syslog (for Linux and macOS), and Windows
Event Log(temporarily removed). The user can enable or disable each logging method as needed.
"""

# Standard library imports
import os
import datetime
import platform
import logging
import argparse
from logging import Formatter, StreamHandler, getLogger
from logging.handlers import SysLogHandler
from typing import Union
from .modules.validate import validate_file

def setup_logging(
    file_path: str,
    error_log_file_path: str,
    console_logging: bool = False,
    syslog_logging: bool = False,
    log_level: Union[int, str] = logging.INFO,
    file_mode: str = "a",
) -> None:
    """
    Sets up logging configuration for an application.

    :param file_path: Path to the log file.
    :param error_log_file_path: Path to the error log file.
    :param console_logging: Whether to enable logging to console.
    :param syslog_logging: Whether to enable logging to syslog.
    :param log_level: Logging level to use.
    :param file_mode: File mode to use when opening log files.
    """
    file_handler, file_path = validate_file(file_path, mode=file_mode)

    root_logger = getLogger()
    root_logger.setLevel(log_level)

    format_str = "%(asctime)s - %(levelname)s: %(message)s"
    formatter = Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_file_handler, error_log_file_path = validate_file(
        error_log_file_path, mode=file_mode
    )
    if os.path.abspath(file_path) == os.path.abspath(error_log_file_path):
        raise ValueError("file_path and error_log_file_path should be different.")
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


def main() -> None:
    """
    Main function to setup logging and handle command line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Configurable logging setup for Python applications."
    )
    parser.add_argument("file_path", help="Path to the log file.")
    parser.add_argument("error_log_file_path", help="Path to the error log file.")
    args = parser.parse_args()

    file_path = args.log_file_path
    error_log_file_path = args.error_log_file_path

    try:
        setup_logging(
            file_path,
            error_log_file_path,
            console_logging=True,
            syslog_logging=True,
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
