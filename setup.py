from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="mlogconfig",
    version="0.2.0",
    author="Matt Wyen",
    author_email="matt@mattwyen.me",
    description="A simple logging setup utility that configures logging with file, console, syslog, and Windows event log handlers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/talltechy/mlogconfig",
    packages=find_packages(),
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
        # Add any package dependencies here, if needed
    ],
)
