#!/bin/bash
# Activates the virtual environment
echo "Activating the virtual env..."
source venv/bin/activate

# Spawns the celery worker terminal
echo "Spawning celery terminal..."
# python manage.py celeryd -s celery -l INFO &

# Starts the running website
echo "Running website..."
sudo python manage.py runserver 0.0.0.0:80

# Prints on close
echo "Closed..."

