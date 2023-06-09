# [mlogconfig.py](mlogconfig.py)

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
[![PyPI](https://img.shields.io/pypi/v/mlogconfig?label=PyPI%20Package%20Version)](https://pypi.org/project/mlogconfig/)
![PyPI - Downloads](https://img.shields.io/pypi/dm/mlogconfig?color=blue)
[![CodeQL](https://github.com/talltechy/mlogconfig/actions/workflows/github-code-scanning/codeql/badge.svg?branch=main)](https://github.com/talltechy/mlogconfig/actions/workflows/github-code-scanning/codeql)

This module provides a configurable logging setup for Python applications. It supports logging to console, file, syslog (for Linux and macOS), and Windows Event Log. The user can enable or disable each logging method as needed.

## Features

- Logging to console, file, syslog, and Windows Event Log
- Enable or disable each logging method as needed
- Easy setup and configuration

## Requirements

- Python 3.9 or higher

For Windows Event Log support, the following packages are required:

- pywin32

Install the required packages by running:

```bash
pip install pywin32
```

## Usage

Here is a basic example of using MLogConfig to set up logging for your application:

```python
from mlogconfig import setup_logging
import logging

# Set up logging

setup_logging(
    log_file_path="logs/app.log",
    error_log_file_path="logs/app_error.log",
    console_logging=True,
    syslog_logging=True,
    windows_event_logging=True,
    log_level=logging.DEBUG,
)

# Use logging in your application

logging.info("This is an info log message.")
logging.error("This is an error log message.")
```

## Customization

To customize the logging configuration, modify the arguments passed to the `setup_logging` function. For example:

- `log_file_path`: Path to the log file
- `error_log_file_path`: Path to the error log file
- `console_logging`: Set to `True` to enable console logging, `False` otherwise
- `syslog_logging`: Set to `True` to enable syslog logging (Linux and macOS only), `False` otherwise
- `windows_event_logging`: Set to `True` to enable Windows Event Log logging, `False` otherwise
- `log_level`: Set the logging level (e.g., `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, `logging.ERROR`, `logging.CRITICAL`)

## Contributing

Contributions are welcome! Please read the [contributing guidelines](https://github.com/talltechy/mlogconfig/blob/main/CONTRIBUTING.md) before submitting pull requests or opening issues.

## License

MLogConfig is licensed under the [MIT License](https://github.com/talltechy/mlogconfig/blob/main/LICENSE.md).
