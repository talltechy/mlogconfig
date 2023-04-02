import os
import logging
from logging import Formatter, FileHandler, StreamHandler, getLogger
from logging.handlers import SysLogHandler, WIN32EventLogHandler
import platform

# Function to validate the log file path
def validate_log_file(log_file_path):
    retries = 3
    while retries > 0:
        try:
            # Check if the directory can be accessed and is writeable.
            log_dir = os.path.dirname(log_file_path)
            if not os.access(log_dir, os.W_OK):
                raise Exception(f"The directory '{log_dir}' is not writeable.")

            # Check if the log file exists and if so, ask for a desired action to take
            if os.path.exists(log_file_path):
                mode_map = {1: 'a', 2: 'w', 3: 'n'}
                choice = int(input(f"The logfile '{log_file_path}' already exists. Please choose an action: {[f'{i}: {c}' for i, c in mode_map.items()]} ").strip())

                if choice in mode_map:
                    mode = mode_map[choice]
                    if mode == 'n':
                        new_path = input("Please enter a new path for the logfile: ")
                        log_file_path = new_path
                        continue
                    else:
                        file_handler = FileHandler(log_file_path, mode=mode)
                else:
                    print("Invalid choice. Please choose an action by entering a number.")
                    continue
            else:
                file_handler = FileHandler(log_file_path, mode='w')

            return file_handler
        except Exception as e:
            retries -= 1
            print(str(e))
            if retries > 0:
                log_file_path = input("Please enter a valid log file path: ")
            else:
                raise Exception("Could not validate the log file path.")

# Function to setup logging with a file and optionally a syslog or Windows event log handler
def setup_logging(log_file_path, syslog_address=None):
    # Validate the log file path
    file_handler = validate_log_file(log_file_path)

    # Get the root logger
    root_logger = getLogger()

    # Set the root logger level to INFO
    root_logger.setLevel(logging.INFO)

    # Create a formatter to use for the handlers
    formatter = Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Set the formatter for the file handler
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger
    root_logger.addHandler(file_handler)

    # Create a console handler and set the formatter
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger
    root_logger.addHandler(console_handler)

    # If on Linux or macOS, try to create a syslog handler and add it to the root logger
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        try:
            if syslog_address is None:
                if platform.system() == 'Linux':
                    syslog_address = '/dev/log'
                elif platform.system() == 'Darwin':
                    syslog_address = '/var/run/syslog'

            syslog_handler = SysLogHandler(address=syslog_address)
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")
    # If on Windows, try to create a Windows event log handler and add it to the root logger
    elif platform.system() == 'Windows':
        try:
            # Import the required win32evtlog package
            from win32evtlog import ReadEventLog
        except ImportError:
            print("pywin32 is required to write to Windows event log. Please install it using: pip install pywin32")
            return

        nt_event_log_handler = WIN32EventLogHandler("Application")
        nt_event_log_handler.setFormatter(formatter)
        root_logger.addHandler(nt_event_log_handler)

# Sample usage of the functions
if __name__ == '__main__':
    log_file = 'myapp.log'
    syslog_server = '192.168.1.10'  # Optional: replace with the IP address of your syslog server
    setup_logging(log_file, syslog_address=syslog_server)
    logging.info('Application started')
    logging.warning('An error occurred')
    logging.error('A critical error occurred')

