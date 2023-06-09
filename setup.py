"""
A setuptools-based setup module for mlogconfig.

mlogconfig is a simple logging setup utility that configures logging with file,
console, syslog, and Windows event log handlers.
"""

from setuptools import setup, find_packages

version = "0.2.5"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlogconfig",
    version=version,
    author="Matt Wyen",
    author_email="matt@mattwyen.me",
    description="A simple logging setup utility that configures logging with file, console, syslog, and Windows event log handlers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talltechy/mlogconfig",
    download_url="https://github.com/talltechy/mlogconfig/archive/{}.tar.gz".format(version),
    packages=find_packages(),
    keywords=["logging", "log", "logger", "syslog", "windows event log"],
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11"
    ],
    python_requires=">=3.9",
    install_requires=[
        "pywin32; sys_platform=='win32'",
    ],
)
