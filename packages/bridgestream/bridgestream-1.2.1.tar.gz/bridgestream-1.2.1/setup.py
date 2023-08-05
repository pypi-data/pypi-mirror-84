#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pip install twine

import io
import os
import re

from setuptools import find_packages, setup

# Package meta-data.
NAME = "bridgestream"
DESCRIPTION = "Packet Serializer "
URL = "https://gitlab.com/gnarly-games/python-bridgestream"
EMAIL = "gnarlygames@gmail.com"
AUTHOR = "Gnarly Games"
REQUIRES_PYTHON = ">=3.8.0"

REQUIRED = []

here = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = "\n" + f.read()


def read_version():
    regexp = re.compile(r'^__version__\W*=\W*"(\d+.\d+.\d+)"')
    init_py = os.path.join(os.path.dirname(__file__), "bridgestream", "__init__.py")
    with open(init_py) as f:
        for line in f:
            match = regexp.match(line)
            if match is not None:
                return match.group(1)
        raise RuntimeError("Cannot find version in bridgestream/__init__.py")


# Where the magic happens:
setup(
    name=NAME,
    version=read_version(),
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=("tests", "tests")),
    install_requires=REQUIRED,
    include_package_data=True,
    license="Apache 2",
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.8",
        "Operating System :: POSIX",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
