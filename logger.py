"""
A simple logging setup utility that configures logging with file,
console, syslog, and Windows event log handlers.
"""

import os
import platform
import socket
import logging

from logging import Formatter, getLogger
from logging.handlers import SysLogHandler

try:
    from logging.handlers import NTEventLogHandler
except ImportError:
    NTEventLogHandler = None

from logging import FileHandler, StreamHandler


def validate_log_file(log_file_path):
    """
    Validate the log file path and create a file handler for it.

    :param log_file_path: Path to the log file
    :return: File handler and the validated log file path
    """
    retries = 3
    file_handler = None
    while retries > 0:
        try:
            log_dir = os.path.dirname(log_file_path)
            if not os.access(log_dir, os.W_OK):
                raise PermissionError(
                    f"The directory '{log_dir}' is not writeable.")

            if os.path.exists(log_file_path):
                retries_choice = 3
                while retries_choice > 0:
                    mode_map = {1: 'Append', 2: 'Overwrite', 3: 'New file'}
                    choices = [f'{i}: {c}' for i, c in mode_map.items()]
                    choice = int(
                        input(
                            (f"The logfile '{log_file_path}' already exists. "
                             "Please choose an action:\n") +
                            f"{', '.join(choices)}\n"
                            "Enter the number corresponding to your choice: "
                        ).strip()
                    )


                    if choice in mode_map:
                        action = mode_map[choice]
                        if action == 'New file':
                            new_path = input(
                                "Please enter a new path for the logfile: ")
                            if os.path.exists(new_path):
                                print(
                                    "The new file path already exists. Please enter a new path.")
                                retries_choice -= 1
                                continue
                            else:
                                log_file_path = new_path
                        else:
                            mode = 'a' if action == 'Append' else 'w'
                            file_handler = FileHandler(
                                log_file_path, mode=mode)
                            break
                    else:
                        print(
                            "Invalid choice. Please choose an action by entering a number.")
                        retries_choice -= 1
                if retries_choice == 0:
                    raise ValueError("Too many invalid choices.")

            else:
                file_handler = FileHandler(log_file_path, mode='w')
                break
        except (PermissionError, ValueError) as error:
            retries -= 1
            print(str(error))
            if retries > 0:
                log_file_path = input("Please enter a valid log file path: ")

    if file_handler is None:
        raise FileNotFoundError("Could not validate the log file path.")

    return file_handler, log_file_path


def setup_logging(log_file_path, console_logging=False,
                  syslog_logging=False, windows_event_logging=False):
    """
    Set up logging with a file and optionally a syslog or Windows event log handler.

    :param log_file_path: Path to the log file
    :param console_logging: Whether to enable console logging or not
    :param syslog_logging: Whether to enable syslog logging or not
    :param windows_event_logging: Whether to enable Windows event logging or not
    """
    file_handler, log_file_path = validate_log_file(log_file_path)

    root_logger = getLogger()
    root_logger.setLevel(logging.INFO)

    format_str = '%(asctime)s - %(levelname)s: %(message)s'
    formatter = Formatter(format_str, datefmt='%Y-%m-%d %H:%M:%S')

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    if console_logging:
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    if syslog_logging and (platform.system() == 'Linux' or platform.system() == 'Darwin'):
        try:
            syslog_address = '/dev/log' if platform.system() == 'Linux' else '/var/run/syslog'
            syslog_handler = SysLogHandler(address=syslog_address)
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")

    if windows_event_logging and platform.system() == 'Windows':
        if NTEventLogHandler is not None:
            try:
                nt_event_log_handler = NTEventLogHandler("Application")
                nt_event_log_handler.setFormatter(formatter)
                root_logger.addHandler(nt_event_log_handler)
            except (socket.error, OSError, ValueError) as error:
                print(f"Could not create Windows event log handler. {error}")
        else:
            print("NTEventLogHandler is not supported on platforms other than Windows.")


if __name__ == "__main__":
    setup_logging("./log_file.log", console_logging=True,
                  syslog_logging=True, windows_event_logging=True)
