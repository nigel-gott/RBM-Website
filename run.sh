#!/bin/bash
# Activates the virtual environment
echo "Activating the virtual env..."
source venv/bin/activate

# Spawns the celery worker terminal
echo "Spawning celery terminal..."
gnome-terminal --tab -e "python manage.py celeryd -s celery -l INFO"

# Starts the running website
echo "Running website..."
python manage.py runserver

# Prints on close
echo "Closed..."

