#!/bin/bash
echo "Creating virtual env folder in venv..." 
virtualenv venv
echo "Activating the virtual env..."
source venv/bin/activate
echo "Installing all requirements..."
pip install -r requirements.txt
echo "Linking post commit and merge hooks..."
ln -s post-commit .git/hooks/post-commit
ln -s post-merge .git/hooks/post-merge
