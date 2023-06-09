"""
This module provides a class with a method to validate the file path and return a FileHandler instance and the absolute log file path.
"""

import os
from logging import FileHandler
from typing import Tuple


def validate_file(file_path: str, mode: str = "a") -> Tuple[FileHandler, str]:
    """
    Validates the file path and returns a FileHandler instance and the absolute log file path.
    """

    file_path = os.path.realpath(file_path)
    file_dir = os.path.dirname(file_path)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir)

    if mode not in ("a", "w", "x"):
        raise ValueError(
            "Invalid mode. Mode should be 'a' (append), 'w' (overwrite), or 'x' (new file)"
        )

    if not os.access(file_dir, os.W_OK):
        raise PermissionError(f"The directory {file_dir!r} is not writeable.")

    return FileHandler(file_path, mode=mode), file_path
