import logging
import logging.handlers
import platform

def setup_logging(log_file_path):
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    if platform.system() == 'Linux':
        try:
            syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")
    elif platform.system() == 'Darwin':
        try:
            syslog_handler = logging.handlers.SysLogHandler(address='/var/run/syslog')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            print("Syslog not available on this platform.")
    elif platform.system() == 'Windows':
        try:
            nt_event_log_handler = logging.handlers.NTEventLogHandler("Application")
            nt_event_log_handler.setFormatter(formatter)
            root_logger.addHandler(nt_event_log_handler)
        except ImportError:
            print("pywin32 is required to write to Windows event log. Please install it using: pip install pywin32")
