# Python Scripts

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/eebf57d6dea24a9f9db25f7428e88d7b)](https://app.codacy.com/gh/talltechy/Python-Scripts/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Modules

### `logger.py`

To use the `setup_logging` function in another script, first import the `setup_logging` function from this module. Then, call the function and provide the path to the log file that you want to create as an argument. Once the function is called, logs will be written to the file and printed to the console. If you are on a Linux, macOS, or Windows system, logs will also be written to the system log.

Example usage in another script:

```python
from logger import setup_logging

log_file_path = '/path/to/log/file.log'
setup_logging(log_file_path)

# begin logging events
```

### `file_validation.py`

To use the `file_validation` module in other scripts you will need to import the `file_validation` module by including the following statement:

```python
import file_validation
```

You can now use the functions of the `file_validation` module in your script. For example, to check if a directory is valid, you can use the function `is_valid_directory` by calling it like this:

```python
if not file_validation.is_valid_directory(directory):
    print('Directory is not valid')
```

Similarly, to get a list of files with a specific extension, you can use the function `get_files` by calling it like this:

```python
files = file_validation.get_files(directory, extension)
```

Make sure you also handle the exception messages raised in the `is_valid_directory` and `is_valid_extension` functions.
