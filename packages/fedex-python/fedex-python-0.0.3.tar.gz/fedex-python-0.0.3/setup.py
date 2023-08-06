#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Copyright 2020 fedex-python
# Author: Sergio Alvarado (sergioal18v@gmail.com)
# =============================================================================

# -----------------------------------------------------------------------------
# Libraries
# -----------------------------------------------------------------------------
# Core libs

# Third party libs
import setuptools

# Project libs
from fedex_python import VERSION
# -----------------------------------------------------------------------------
# Constants
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Classes
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Functions
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Main code
# -----------------------------------------------------------------------------
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='fedex-python',
    version=VERSION,
    description='NOT official module for use fedex web services with python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sr1871/fedex-python",
    author='Sergio Alvarado',
    author_email='sergioal18v@gmail.com',
    packages=setuptools.find_packages(),
    package_data={'fedex_python': ['wsdl/*.wsdl', 'wsdl/test/*.wsdl']},
    keywords=['FedEx', 'python'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['pydantic', 'zeep']
)