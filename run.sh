#!/bin/bash
# Runs the project

# Activates the virtual environment
echo "Activating the virtual env..."
source venv/bin/activate

# Spawns the celery worker terminal
echo "Spawning celery terminal..."
# python manage.py celeryd -s celery -l INFO &

# Starts the running website
echo "Running website..."
python manage.py runserver 0.0.0.0:8000

# Prints on close
echo "Closed..."

