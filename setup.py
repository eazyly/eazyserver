#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages
import os
import glob
import shutil
from collections import OrderedDict


description = "A simple python web framework for creating RESTful and JSON-RPC services"


package_version_file = "src/eazyserver/VERSION"
with open("VERSION") as version_file:
    version = version_file.read().strip()
    shutil.copyfile("VERSION", package_version_file)

with open("README.rst") as readme_file:
    readme = readme_file.read()

with open("HISTORY.rst") as history_file:
    history = history_file.read()

with open("AUTHORS.rst") as authors_file:
    authors = authors_file.read()

with open("CONTRIBUTING.rst") as contributing_file:
    contributing = contributing_file.read()

requirements = ["Click>=7.0"]
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup_requirements = ["pytest-runner"]

test_requirements = ["pytest>=3"]

setup(
    author="Ashutosh Mishra",
    author_email="ashutoshdtu@gmail.com",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GPL-2.0",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description=description,
    entry_points={
        "console_scripts": [
            "eazyserver=eazyserver.cli:cli",
        ],
    },
    install_requires=requirements,
    license="GPL-2.0",
    long_description=readme + "\n\n" + history,
    keywords="eazyserver",
    name="eazyserver",
    packages=find_packages("src", include=["eazyserver"]),
    package_dir={"": "src"},
    py_modules=[
        os.path.splitext(os.path.basename(i))[0] for i in glob.glob("src/*.py")
    ],
    include_package_data=True,
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    url="https://github.com/eazyly/eazyserver",
    project_urls=OrderedDict(
        (
            ("Documentation", "http://eazyserver.readthedocs.io"),
            ("Code", "https://github.com/eazyly/eazyserver"),
            ("Issue tracker", "https://github.com/eazyly/eazyserver/issues"),
        )
    ),
    version=version,
    zip_safe=False,
)
