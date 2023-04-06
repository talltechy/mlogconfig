import os
import logging
from logging import Formatter, FileHandler, StreamHandler, getLogger
from logging.handlers import SysLogHandler
import platform

try:
    from logging.handlers import NTEventLogHandler
except ImportError:
    NTEventLogHandler = None


def validate_log_file(log_file_path):
    """
    Validate the log file path, check if the directory is writeable and
    ask the user for the desired action if the log file exists.
    
    Args:
        log_file_path (str): The path to the log file.
    
    Returns:
        tuple: The FileHandler object and the updated log file path.
    """
    retries = 3
    file_handler = None
    while retries > 0:
        try:
            log_dir = os.path.dirname(log_file_path)
            if not os.access(log_dir, os.W_OK):
                raise Exception(f"The directory '{log_dir}' is not writeable.")

            if os.path.exists(log_file_path):
                retries_choice = 3
                while retries_choice > 0:
                    mode_map = {1: 'Append', 2: 'Overwrite', 3: 'New file'}
                    choices = [f'{i}: {c}' for i, c in mode_map.items()]
                    choice = int(input(f"The logfile '{log_file_path}' already exists. Please choose an action:\n"
                                       f"{', '.join(choices)}\n"
                                       "Enter the number corresponding to your choice: ").strip())

                    if choice in mode_map.keys():
                        action = mode_map[choice]
                        if action == 'New file':
                            new_path = input("Please enter a new path for the logfile: ")
                            if os.path.exists(new_path):
                                print("The new file path already exists. Please enter a new path.")
                                retries_choice -= 1
                                continue
                            else:
                                log_file_path = new_path
                        else:
                            mode = 'a' if action == 'Append' else 'w'
                            file_handler = FileHandler(log_file_path, mode=mode)
                            break
                    else:
                        print("Invalid choice. Please choose an action by entering a number.")
                        retries_choice -= 1
                if retries_choice == 0:
                    raise Exception("Too many invalid choices.")
                    
            else:
                file_handler = FileHandler(log_file_path, mode='w')
                break
        except Exception as e:
            retries -= 1
            print(str(e))
            if retries > 0:
                log_file_path = input("Please enter a valid log file path: ")

    if file_handler is None:
        raise Exception("Could not validate the log file path.")

    return file_handler, log_file_path


def setup_logging(log_file_path, console_logging=False, syslog_logging=False, windows_event_logging=False):
    """
    Set up logging with a file handler and optionally a console, syslog or Windows event log handler.
    
    Args:
        log_file_path (str): The path to the log file.
        console_logging (bool, optional): Enable console logging. Defaults to False.
        syslog_logging (bool, optional): Enable syslog logging. Defaults to False.
        windows_event_logging (bool, optional): Enable Windows event logging. Defaults to False.
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
            except Exception as e:
                print(f"Could not create Windows event log handler. {e}")
                pass
        else:
            print("NTEventLogHandler is not supported on platforms other than Windows.")


if __name__ == "__main__":
    setup_logging("./log_file.log", console_logging=True, syslog_logging=True, windows_event_logging=True)
