# [mlogconfig.py](mlogconfig.py)

[![Pylint](https://github.com/talltechy/logger/actions/workflows/pylint.yml/badge.svg)](https://github.com/talltechy/logger/actions/workflows/pylint.yml)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

This is a Python script for configuring logging with various handlers such as console, file, syslog, and Windows event log. The script defines two functions; validate_log_file() and setup_logging(). The validate_log_file() takes in a log file path and validates it. It checks if the directory exists, is accessible and writable, and also checks if the log file already exists. If the log file already exists, the function asks the user what to do with it; append to it, overwrite it or create a new file. If the user chooses to create a new file, the function prompts for a new path. If the user chooses to append or overwrite, the function sets up a file handler accordingly and returns it. The file handler and the log file path are returned by the function.

The setup_logging() function takes in a log file path, boolean values of console_logging, syslog_logging, and windows_event_logging. It calls the validate_log_file() function to validate the log file path and creates a file handler. The function adds the file handler to the root logger and sets the log level to INFO. It also creates a formatter to use for all the handlers. If console_logging is True, the function creates a console handler, sets the formatter for it, and adds the handler to the root logger. If syslog_logging is True and the platform running is either Linux or Darwin, the function creates a SysLogHandler and sets the formatter for it. If windows_event_logging is True and the platform running is Windows, the function creates an NTEventLogHandler and adds it to the root logger.

Finally, if the script is run directly (not imported as a module), it calls the setup_logging() function with default values of log_file_path, console_logging, syslog_logging, and windows_event_logging. It sets console_logging, syslog_logging, and windows_event_logging to True. The log file path is set to "./log_file.log".

The module contains two functions:

1. `validate_log_file(log_file_path)`: Validates and handles the provided log file path. In the `validate_log_file` function, the mode parameter refers to the mode in which the log file should be opened. You can pass the desired mode directly as a parameter to control how the log file will be opened and used. There are three possible modes:
   1. 'a' - Append: In this mode, new log entries will be added to the existing log file, preserving the existing content. If the file does not exist, it will be created. This is the default mode, as it ensures that existing log data is not lost.
   2. 'w' - Overwrite: In this mode, if the log file already exists, its content will be erased, and new log entries will overwrite the previous content. If the file does not exist, it will be created. This mode is useful when you want to start a new log session and discard previous log data.
   3. 'n' - New file: In this mode, if the log file already exists, an error will be raised, prompting the user to choose a different file path for the new log file. This mode is useful when you want to create a new log file and avoid accidentally overwriting or appending to an existing log file.
1. `setup_logging(log_file_path, syslog_address=None)`: Sets up logging with a file and, if applicable, a syslog or Windows event log handler.

## Requirements

The program requires the following:

- Python 3.x
- A valid file path for logging.

## Installation

To use this program, follow the steps below:

1. Clone this repository
2. Navigate to the cloned directory
3. Run `python mlogconfig.py` with valid values for parameters.

### **Parameters**

- `log_file_path`: A valid file path for logging. This parameter is required.
- `console_logging`: If True, console logging will be enabled. Defaults to False.
- `syslog_logging`: If True and running on a Linux or MacOS system, syslog logging will be enabled. Defaults to False.
- `windows_event_logging`: If True and running on a Windows system, Windows Event logging will be enabled. Defaults to False.

1. Copy the mlogconfig.py file to your project directory.
2. Import the setup_logging function in your main script:

```python
from mlogconfig import setup_logging
```

## Usage

### Example 1

The following code sets up logging with only a file handler, using the default log file path "./log_file.log". Console_logging, Syslog_logging, and Windows_event_logging are all set to False.

```python
setup_logging("./log_file.log")
```

### Example 2

The following code sets up logging with a file handler, and also adds a console handler. In this example, console_logging is set to True, while the other two logging parameters remain False.

```python
setup_logging("./log_file.log", console_logging=True)
```

### Example 3

The following code sets up logging with a file handler and a syslog handler. In this example, syslog_logging is set to True, while console_logging and windows_event_logging are set to False.

```python
setup_logging("./log_file.log", syslog_logging=True)
```

### Example 4

The following code sets up logging with a file handler, a console handler, and a syslog handler. In this example, all three logging parameters are set to True.

```python
setup_logging("./log_file.log", console_logging=True, syslog_logging=True)
```

### Example 5

The following code sets up logging with a file handler and a Windows event log handler. In this example, windows_event_logging is set to True, while console_logging and syslog_logging are set to False.

```python
setup_logging("./log_file.log", windows_event_logging=True)
```

### Example Python Script

Here's an example of how to use the module in a Python script:

```python
import mlogconfig

# Set up logging with file, console, syslog and Windows event log handlers
mlogconfig.setup_logging("./log_file.log", console_logging=True, syslog_logging=True, windows_event_logging=True)

# Log an info message
mlogconfig.getLogger().info("This is an info message")

# Log an error message
mlogconfig.getLogger().error("This is an error message")
```

This will set up the logging configuration with the specified handlers, and then log an info message and an error message using the logger that was created in the `setup_logging` function. The messages will be written to the log file, displayed on the console, and sent to the syslog and Windows event log, depending on which handlers were enabled.

## License

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[MIT License](LICENSE.md)
