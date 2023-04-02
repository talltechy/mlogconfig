import os
import re
import logging
import logging.handlers
import platform
import sys

def setup_logging():
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

    file_handler = logging.FileHandler('file_renamer.log')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    if platform.system() == 'Linux':
        try:
            syslog_handler = logging.handlers.SysLogHandler(address='/dev/log')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            pass
    elif platform.system() == 'Darwin':
        try:
            syslog_handler = logging.handlers.SysLogHandler(address='/var/run/syslog')
            syslog_handler.setFormatter(formatter)
            root_logger.addHandler(syslog_handler)
        except FileNotFoundError:
            pass
    elif platform.system() == 'Windows':
        try:
            nt_event_log_handler = logging.handlers.NTEventLogHandler("FileRenamer")
            nt_event_log_handler.setFormatter(formatter)
            root_logger.addHandler(nt_event_log_handler)
        except ImportError:
            print("win32api not found, please install it using: pip install pywin32", file=sys.stderr)
            sys.exit(1)


def is_valid_directory(directory):
    if not os.path.isdir(directory):
        print("Invalid directory. Please enter a valid directory.")
        return False
    return True

def is_valid_extension(extension):
    extension_pattern = r'^\.\w+$'
    if not re.match(extension_pattern, extension):
        print("Invalid file extension. Please enter a valid file extension.")
        return False
    return True

def add_dot_if_needed(extension):
    if not extension.startswith('.'):
        extension = '.' + extension
    return extension

def get_user_input():
    startdir = input("Enter start directory: ")
    while not is_valid_directory(startdir):
        startdir = input("Enter start directory: ")

    old_extension = add_dot_if_needed(input('Enter file extension to rename: '))
    while not is_valid_extension(old_extension):
        old_extension = add_dot_if_needed(input('Enter file extension to rename: '))

    new_extension = add_dot_if_needed(input("Enter new file extension: "))
    while not is_valid_extension(new_extension):
        new_extension = add_dot_if_needed(input("Enter new file extension: "))

    ignore_default_exclusions = input("Ignore default exclusions? (yes/no): ").lower()
    while ignore_default_exclusions not in ['yes', 'no']:
        ignore_default_exclusions = input("Ignore default exclusions? (yes/no): ").lower()

    ignore_default_exclusions = ignore_default_exclusions == 'yes'

    return startdir, old_extension, new_extension, ignore_default_exclusions

def rename_files(startdir, old_extension, new_extension, ignore_default_exclusions):
    default_exclude = [
        '.git', '.idea', 'target', '.pytest_cache', '.vscode', '__pycache__',
        'node_modules', '.DS_Store', '.svn', '.hg', 'CVS'
    ]

    exclude = [] if ignore_default_exclusions else default_exclude

    for root, dirs, files in os.walk(startdir):
        dirs[:] = [d for d in dirs if d not in exclude]
        for filename in files:
            if filename.endswith(old_extension):
                infilename = os.path.join(root, filename)
                newname = os.path.join(root, filename.replace(old_extension, new_extension))

                if not os.access(infilename, os.W_OK):
                    message = f"Permission denied to modify file: {infilename}"
                    print(message)
                    logging.warning(message)
                    continue

                try:
                    os.rename(infilename, newname)
                    message = f"Renamed file: {infilename} to {newname}"
                    print(message)
                    logging.info(message)
                except OSError as e:
                    message = f"Error occurred: {e}"
                    print(message)
                    logging.error(message)

def main():
    setup_logging()
    startdir, old_extension, new_extension, ignore_default_exclusions = get_user_input()
    logging.info(f"Starting directory: {startdir}")
    logging.info(f"Old file extension: {old_extension}")
    logging.info(f"New file extension: {new_extension}")
    logging.info(f"Ignore default exclusions: {ignore_default_exclusions}")
    rename_files(startdir, old_extension, new_extension, ignore_default_exclusions)

if __name__ == "__main__":
    main()
