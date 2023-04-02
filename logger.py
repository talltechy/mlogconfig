import os
import logging
from logging import Formatter, FileHandler, StreamHandler, getLogger
from logging.handlers import SysLogHandler, NTEventLogHandler
import platform

def validate_log_file(log_file_path):
    retries = 3
    while retries > 0:
        try:
            # Check if the directory exists and is writeable.
            log_dir = os.path.dirname(log_file_path)
            if not os.access(log_dir, os.W_OK):
                raise Exception(f"The directory '{log_dir}' is not writeable.")
            
            # Check if the file already exists.
            if os.path.exists(log_file_path):
                choices = ['append', 'overwrite', 'select new name']
                choice = input(f"The logfile '{log_file_path}' already exists. Please choose an action: {[f'{i+1}: {c}' for i, c in enumerate(choices)]} ").strip()
                if choice.isdigit() and int(choice) in range(1, len(choices) + 1):
                    choice_index = int(choice) - 1
                    if choice_index == 0:
                        file_handler = FileHandler(log_file_path, mode='a')
                    elif choice_index == 1:
                        file_handler = FileHandler(log_file_path, mode='w')
                    elif choice_index == 2:
                        new_path = input("Please enter a new path for the logfile: ")
                        log_file_path = new_path
                        continue
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

def setup_logging(log_file_path, syslog_address=None):
    # Validate the log file.
    file_handler = validate_log_file(log_file_path)

    # Get the root logger.
    root_logger = getLogger()

    # Set the root logger level to INFO.
    root_logger.setLevel(logging.INFO)

    # Create a formatter to use for the handlers.
    formatter = Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    # Set the formatter for the file handler.
    file_handler.setFormatter(formatter)

    # Add the file handler to the root logger.
    root_logger.addHandler(file_handler)

    # Create a console handler and set the formatter.
    console_handler = StreamHandler()
    console_handler.setFormatter(formatter)

    # Add the console handler to the root logger.
    root_logger.addHandler(console_handler)

    # If on Linux or macOS, try to create a syslog handler and add it to the root logger.
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
    # If on Windows, try to create a Windows event log handler and add it to the root logger.
    elif platform.system() == 'Windows':
        try:
            import win32evtlog
        except ImportError:
            print("pywin32 is required to write to Windows event log. Please install it using: pip install pywin32")
            return
            
        nt_event_log_handler = NTEventLogHandler("Application")
        nt_event_log_handler.setFormatter(formatter)
        root_logger.addHandler(nt_event_log_handler)
