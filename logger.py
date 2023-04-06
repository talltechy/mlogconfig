import os
import logging
from logging import Formatter, FileHandler, StreamHandler, getLogger
from logging.handlers import SysLogHandler, NTEventLogHandler
import platform


# Function to validate the log file path
def validate_log_file(log_file_path):
    retries = 3
    file_handler = None
    while retries > 0:
        try:
            # Check if the directory can be accessed and is writeable.
            log_dir = os.path.dirname(log_file_path)
            if not os.access(log_dir, os.W_OK):
                raise Exception(f"The directory '{log_dir}' is not writeable.")

            # Check if the log file exists and if so, ask for a desired action to take
            if os.path.exists(log_file_path):
                mode_map = {1: 'Append', 2: 'Overwrite', 3: 'New file'}
                choices = [f'{i}: {c}' for i, c in mode_map.items()]
                choice = int(input(f"The logfile '{log_file_path}' already exists. Please choose an action:\n"
                                   f"{', '.join(choices)}\n"
                                   "Enter the number corresponding to your choice: ").strip())

                if choice in mode_map.keys():
                    action = mode_map[choice]
                    if action == 'New file':
                        new_path = input("Please enter a new path for the logfile: ")
                        log_file_path = new_path
                    else:
                        mode = 'a' if action == 'Append' else 'w'
                        file_handler = FileHandler(log_file_path, mode=mode)
                        break
                else:
                    print("Invalid choice. Please choose an action by entering a number.")
                    continue
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


# Function to setup logging with a file and optionally a syslog or Windows event log handler
def setup_logging(log_file_path, console_logging=False, syslog_logging=False, windows_event_logging=False):
    # Validate the log file path
    file_handler, log_file_path = validate_log_file(log_file_path)

    # Get the root logger
    root_logger = getLogger()

    # Set the root logger level to INFO
    root_logger.setLevel(logging.INFO)

    # Create a formatter to use for the handlers
    format_str = '%(asctime)s - %(levelname)s: %(message)s'
    formatter = Formatter(format_str, datefmt='%Y-%m-%d %H:%M:%S')

    # Set the formatter for the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger
    root_logger.addHandler(file_handler)

    if console_logging:
        # Create a console handler and set the formatter
        console_handler = StreamHandler()
        console_handler.setFormatter(formatter)

        # Add the console handler to the root logger
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
        try:
            nt_event_log_handler = NTEventLogHandler("Application")
            root_logger.addHandler(nt_event_log_handler)
        except ImportError:
            print("NTEventLogHandler is not supported on platforms other than Windows.")
            pass
        except Exception as e:
            print(f"Could not create Windows event log handler. {e}")
            pass


if __name__ == "__main__":
    setup_logging("./log_file.log", console_logging=True, syslog_logging=True, windows_event_logging=True)
