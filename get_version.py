import re
import codecs
from setuptools import setup, find_packages

with codecs.open("setup.py", "r", "utf-8") as f:
    setup_py = f.read()

version = re.search(r"version=['\"](.+?)['\"]", setup_py).group(1)
print(version)
