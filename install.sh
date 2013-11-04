#!/bin/bash
echo "Creating virtual env folder in venv..." 
virtualenv venv
echo "Activating the virtual env..."
source venv/bin/activate
echo "Installing all requirements..."
pip install -r requirements.txt
echo "Linking post commit and merge hooks..."
cd .git/hooks
ln -s ../../hooks/post-commit post-commit
ln -s ../../hooks/post-merge post-merge
echo "Finished, activate the virtual env with 'source venv/bin/activate' or 'source venv/bin/activate.csh'"
