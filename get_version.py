"""
A script to extract the version number from a setup.py file.
"""

import re

def read_setup_py(file_path):
    """
    Read the content of a setup.py file.

    Args:
        file_path (str): Path to the setup.py file.

    Returns:
        str: Content of the setup.py file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

def extract_version(setup_py_content):
    """
    Extract the version number from the content of a setup.py file.

    Args:
        setup_py_content (str): Content of the setup.py file.

    Returns:
        str: Version number if found, else 'Version not found'.
    """
    pattern = re.compile(r"version=['\"](.+?)['\"]")
    match = pattern.search(setup_py_content)

    if match:
        return match.group(1)
    return "Version not found"

def main():
    """
    Main function to execute the script.
    """
    setup_py_content = read_setup_py("setup.py")
    version = extract_version(setup_py_content)
    print(version)

if __name__ == "__main__":
    main()
