#!/bin/sh

echo "Running inside install.sh:"
echo "Installing the python package and dependencies..."

python setup.py bdist_wheel
python -m pip install dist/eazyserver-*
# pip install -e .
