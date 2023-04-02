import logging
import logging.handlers
import os
from logger import setup_logging
from file_validation import is_valid_directory, is_valid_extension, get_files

log_file_path = 'file_renamer.log'

def get_user_input():
    while True:
        startdir = input("Enter start directory: ")
        if is_valid_directory(startdir):
            break
        print("Invalid directory. Please enter a valid directory.")

    while True:
        old_extension = input('Enter file extension to rename: ')
        if is_valid_extension(old_extension):
            break
        print("Invalid file extension. Please enter a valid file extension.")

    while True:
        new_extension = input("Enter new file extension: ")
        if is_valid_extension(new_extension):
            break
        print("Invalid file extension. Please enter a valid file extension.")

    ignore_default_exclusions = input("Ignore default exclusions? (yes/no): ").lower() == 'yes'

    if not ignore_default_exclusions:
        custom_exclusions = input("Enter your own comma-separated exclusions, or leave blank for none: ").split(',')
        if custom_exclusions != ['']:
            overwrite_existing_exclusions = input("Overwrite existing exclusions? (yes/no): ").lower() == 'yes'
        else:
            overwrite_existing_exclusions = False
    else:
        custom_exclusions = []
        overwrite_existing_exclusions = False

    return startdir, old_extension, new_extension, ignore_default_exclusions, custom_exclusions, overwrite_existing_exclusions

def rename_file(root, filename, old_extension, new_extension):
    infilename = os.path.join(root, filename)
    newname = os.path.join(root, filename.replace(old_extension, new_extension))

    try:
        os.rename(infilename, newname)
        message = f"Renamed file: {infilename} to {newname}"
        print(message)
        logging.info(message)
    except OSError as e:
        message = f"Error occurred: {e}"
        print(message)
        logging.error(message)

def rename_files(startdir, old_extension, new_extension, ignore_default_exclusions, custom_exclusions, overwrite_existing_exclusions, depth=0):
    default_exclude = [
        '.git', '.idea', 'target', '.pytest_cache', '.vscode', 'pycache',
        'node_modules', '.DS_Store', '.svn', '.hg', 'CVS'
    ]
    if ignore_default_exclusions:
        exclude = []
    elif overwrite_existing_exclusions:
        exclude = custom_exclusions
    else:
        exclude = default_exclude + custom_exclusions

    if depth > MAX_DEPTH:
        message = f"Maximum directory traversal depth ({MAX_DEPTH}) reached. Skipping: {startdir}"
        print(message)
        logging.warning(message)
        return

    try:
        for root, dirs, files in os.walk(startdir):
            dirs[:] = [d for d in dirs if d not in exclude]
            for filename in files:
                if filename.endswith(old_extension):
                    rename_file(root, filename, old_extension, new_extension)

            for subdir in dirs:
                subdir_path = os.path.join(root, subdir)
                rename_files(subdir_path, old_extension, new_extension, ignore_default_exclusions, custom_exclusions, overwrite_existing_exclusions, depth=depth+1)
    except FileNotFoundError as e:
        message = f"Error occurred: {e}"
        print(message)
        logging.error(message)


def main():
    global MAX_DEPTH
    MAX_DEPTH = int(os.environ.get('MAX_DEPTH', 5))
    setup_logging(log_file_path)
    startdir, old_extension, new_extension, ignore_default_exclusions, custom_exclusions, overwrite_existing_exclusions = get_user_input()
    logging.info(f"Starting directory: {startdir}")
    logging.info(f"Old file extension: {old_extension}")
    logging.info(f"New file extension: {new_extension}")
    logging.info(f"Ignore default exclusions: {ignore_default_exclusions}")
    logging.info(f"Custom exclusions: {custom_exclusions}")
    logging.info(f"Overwrite existing exclusions: {overwrite_existing_exclusions}")
    rename_files(startdir, old_extension, new_extension, ignore_default_exclusions, custom_exclusions, overwrite_existing_exclusions)


if __name__ == '__main__':
    main()
