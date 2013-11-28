#!/bin/bash
echo "Activating the virtual env..."
source venv/bin/activate
echo "Spawning celery terminal..."
gnome-terminal --tab -e "python manage.py celeryd -s celery -l INFO"
echo "Running website..."
python manage.py runserver
echo "Closed..."
