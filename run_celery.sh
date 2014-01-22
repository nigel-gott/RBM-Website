#!/bin/bash
# Runs the project

# Activates the virtual environment
echo "Activating the virtual env..."
source venv/bin/activate

# Starts celery 
echo "Spawning Celery "
python manage.py celeryd -s celery -l INFO

