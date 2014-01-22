#!/bin/bash
# Runs the project

# Activates the virtual environment
echo "Activating the virtual env..."
source venv/bin/activate

# Starts the running website
echo "Running website..."
python manage.py runserver 0.0.0.0:8000

