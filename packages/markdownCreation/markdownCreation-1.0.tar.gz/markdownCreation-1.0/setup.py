import packageupload

from setuptools import setup
from os import path
with open(path.join(path.abspath(path.dirname(__file__)), 'README.md'), encoding='utf-8') as f:
    readme_description = f.read()
setup(
name = "markdownCreation",
packages = ["markdownCreation"],
version = "1.0",
license = "MIT",
description = "A markdown file creation module for Python!",
author = "Anime no Sekai",
author_email = "niichannomail@gmail.com",
url = "https://github.com/Animenosekai/markdown-creation",
download_url = "https://github.com/Animenosekai/markdown-creation/archive/v1.0.0.tar.gz",
keywords = ['markdown', ' md', ' readme', ' html'],
install_requires = ['markdown', 'beautifulsoup4', 'htmlmin'],
classifiers = ['Development Status :: 4 - Beta', 'License :: OSI Approved :: MIT License', 'Programming Language :: Python :: 3', 'Programming Language :: Python :: 3.4', 'Programming Language :: Python :: 3.5', 'Programming Language :: Python :: 3.6', 'Programming Language :: Python :: 3.7', 'Programming Language :: Python :: 3.8', 'Programming Language :: Python :: 3.9'],
long_description = readme_description,
long_description_content_type = "text/markdown",
include_package_data=True,
)
