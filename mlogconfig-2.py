import os
import platform
import logging
from logging import Formatter, StreamHandler, FileHandler
import datetime
import sys
import pywintypes

try:
    import win32evtlog
    import win32security
    import winerror
    WIN32_AVAILABLE = True
except ImportError:
    WIN32_AVAILABLE = False

from logging.handlers import SysLogHandler


class EventLogException(Exception):
    """Custom exception for Windows event log errors."""
    pass


class WindowsEventLogHandler(logging.Handler):
    def __init__(self, appName):
        """Initialize the Windows event log handler.

        Args:
            appName (str): The application name for the event log.
        """
        super().__init__()
        self.appName = appName

    def emit(self, record):
        """Emit a log record to the Windows event log.

        Args:
            record (logging.LogRecord): The log record to emit.
        """
        if not WIN32_AVAILABLE:
            return

        try:
            sid = win32security.LookupAccountName("", os.environ["USERNAME"])[0]
            message = str(record.getMessage())
            win32evtlog.ReportEvent(
                self.appName,
                1,
                0,
                record.levelno,
                sid,
                [message],
                b"",
            )
        except (EventLogException, pywintypes.error) as e:
            if isinstance(e, pywintypes.error) and e.winerror == winerror.ERROR_FILE_NOT_FOUND:
                raise FileNotFoundError(e.strerror) from None
            else:
                self.handleError(record)
        except Exception:
            self.handleError(record)


def validate_log_file(log_file_path, mode="a"):
    """
    Validate the log file path and create a file handler for it.

    Args:
        log_file_path (str): Path to the log file.
        mode (str, optional): File mode for the log file. Defaults to 'a'.
    Returns:
        tuple: File handler and the validated log file path.
    """
    log_file_path = os.path.abspath(log_file_path)
    log_dir = os.path.dirname(log_file_path)

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(log_file_path):
        open(log_file_path, 'w').close()

    if not os.path.isfile(log_file_path):
        raise ValueError(f"'{log_file_path}' is not a valid file path.")

    if mode not in ("a", "w", "x"):
        raise ValueError(
            "Invalid mode. Mode should be 'a' (append), 'w' (overwrite), or 'x' (new file)"
        )

    if not os.access(log_dir, os.W_OK):
        raise PermissionError(f"The directory '{log_dir}' is not writeable.")

    file_handler = FileHandler(log_file_path, mode=mode)
    return file_handler, log_file_path


def setup_logging(
    log_file_path,
    error_log_file_path,
    console_logging=False,
    syslog_logging=False,
    windows_event_logging=False,
    log_level=logging.INFO,
):
    """
    Set up logging with a file and optionally a syslog or Windows event log handler.

    Args:
        log_file_path (str): Path to the log file.
        error_log_file_path (str): Path to the error log file.
        console_logging (bool, optional): Whether to enable console logging or not. Defaults to False.
        syslog_logging (bool, optional): Whether to enable syslog logging or not. Defaults to False.
        windows_event_logging (bool, optional): Whether to enable Windows event logging or not. Defaults to False.
        log_level (int, optional): Logging level. Defaults to logging.INFO.
    """
    file_handler, log_file_path = validate_log_file(log_file_path)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    format_str = "%(asctime)s - %(levelname)s: %(message)s"
    formatter = Formatter(format_str, datefmt="%Y-%m-%d %H:%M:%S")

    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    error_file_handler, error_log_file_path = validate_log_file(error_log_file_path)
    if os.path.abspath(log_file_path) == os.path.abspath(error_log_file_path):
        raise ValueError("log_file_path and error_log_file_path should be different.")
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

    if windows_event_logging:
        nt_event_log_handler = WindowsEventLogHandler(appName="mlogconfig")
        root_logger.addHandler(nt_event_log_handler)


def main():
    if len(sys.argv) < 3:
        print("Usage: python mlogconfig.py <log_file_path> <error_log_file_path>")
        sys.exit(1)

    log_file_path = sys.argv[1]
    error_log_file_path = sys.argv[2]

    try:
        setup_logging(
            log_file_path,
            error_log_file_path,
            console_logging=True,
            syslog_logging=True,
            windows_event_logging=True,
            log_level=logging.DEBUG,
        )
    except Exception as e:
        with open(error_log_file_path, "a", encoding="utf-8") as error_log_file:
            error_log_file.write(
                f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - ERROR: {str(e)}\n"
            )
        raise


if __name__ == "__main__":
    main()
