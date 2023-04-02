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
