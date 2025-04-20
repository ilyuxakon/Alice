#!/bin/bash

# Exit early on errors
set -eu

# Python buffers stdout. Without this, you won't see what you "print" in the Activity Logs
export PYTHONUNBUFFERED=true

# Install Python 3 virtual env
VIRTUALENV=./venv

if [ ! -d $VIRTUALENV ]; then
  python3 -m venv $VIRTUALENV
fi

# Install pip into virtual environment
if [ ! -f $VIRTUALENV/Scripts/pip.exe ]; then
  curl --silent --show-error --retry 5 https://bootstrap.pypa.io/pip/3.7/get-pip.py | $VIRTUALENV/Scripts/python.exe
fi

# Install the requirements
pip3 install -r requirements.txt

# Run your glorious application
python3 server.py