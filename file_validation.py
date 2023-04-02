import os
import re
import stat

def is_valid_directory(directory):
    # Check if directory exists
    if not os.path.isdir(directory):
        return False

    # Check if directory is not a protected system directory
    st = os.stat(directory)
    mode = st.st_mode
    return not bool(mode & (stat.S_IWOTH))

def is_valid_extension(extension):
    extension_pattern = r'^\w+$'
    return re.match(extension_pattern, extension, re.IGNORECASE)

def get_files(directory, extension):
    if not is_valid_directory(directory):
        raise ValueError('Directory must be a valid path and not a protected system directory')
    if not is_valid_extension(extension):
        raise ValueError('Extension must be a valid extension')
    return [
        file 
        for file in os.listdir(directory)
        if file.endswith('.' + extension)
    ]
