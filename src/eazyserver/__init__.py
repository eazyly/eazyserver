# -*- coding: utf-8 -*-

"""
    eazyserver
    ~~~~~~~~~~~~

    A simple python web framework for creating RESTful and JSON-RPC services
    Based on Python Eve, Python Flask.

    License:
        GPL-2.0, see LICENSE for more details.
"""

import os
from .eazy import Eazy

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
VERSION_FILE = os.path.join(BASE_DIR, "VERSION")
with open(VERSION_FILE) as version_file:
    version = version_file.read().strip()

__author__ = """Ashutosh Mishra"""
__email__ = "ashutoshdtu@gmail.com"
__version__ = version
