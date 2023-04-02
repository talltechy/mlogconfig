# Python Scripts

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/eebf57d6dea24a9f9db25f7428e88d7b)](https://app.codacy.com/gh/talltechy/Python-Scripts/dashboard?utm_source=gh&utm_medium=referral&utm_content=&utm_campaign=Badge_grade)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Modules

### [logger.py](logger.py)

This Python module provides a convenient way to set up logging for your applications. It configures logging to output messages to a file, console, and optionally to a syslog server (on Linux and macOS) or Windows Event Log (on Windows). The module contains two functions:

1. `validate_log_file(log_file_path)`: Validates and handles the provided log file path.
2. `setup_logging(log_file_path, syslog_address=None)`: Sets up logging with a file and, if applicable, a syslog or Windows event log handler.

#### Installation

1. Copy the logger.py file to your project directory.
2. Import the setup_logging function in your main script:

```python
from logger import setup_logging
```

#### Usage

To use the module in your code, follow these steps:

1. Import the setup_logging function from the module:

```python
from logger import setup_logging
```

2. Call the setup_logging function with the desired log file path and, optionally, the address of your syslog server (for Linux and macOS) or leave it empty for Windows Event Log:

```python
log_file = 'myapp.log'
syslog_server = '192.168.1.10'  # Optional: replace with the IP address of your syslog server
setup_logging(log_file, syslog_address=syslog_server)
```

3. Use the standard logging module to log messages in your application:

```python
import logging

logging.info('Application started')
logging.warning('An error occurred')
logging.error('A critical error occurred')
```

#### Example

Here's an example of how to use the module in a Python script:

```python
from logger import setup_logging
import logging

if __name__ == '__main__':
    log_file = 'myapp.log'
    syslog_server = '192.168.1.10'  # Optional: replace with the IP address of your syslog server
    setup_logging(log_file, syslog_address=syslog_server)

    logging.info('Application started')
    logging.warning('An error occurred')
    logging.error('A critical error occurred')
```

This example configures logging to output messages to a file, console, and a syslog server (on Linux and macOS) or Windows Event Log (on Windows).

### [file_validation.py](file_validation.py)

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
