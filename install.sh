#!/bin/bash
# Installs everything required by the project

# Sets up the environment for developing
echo "Creating virtual env folder in venv..."
virtualenv venv

echo "Activating the virtual env..."
source venv/bin/activate

# Installs any required packages
echo "Installing all requirements..."
pip install -r requirements.txt

# Adds the git hooks
echo "Linking post commit and merge hooks..."
cd .git/hooks
ln -s ../../hooks/pre-commit pre-commit
ln -s ../../hooks/post-merge post-merge
cd ../../

# Clones the latest release of the RBM library
echo "Cloning rbm lib..."
git clone https://github.com/fleurette/RBM.git rbm_website/libs/rbm_lib

# Creates the database
echo "Setting up database..."
rm database.sqlite3
python manage.py syncdb --noinput

# Cleans up the media folder and removes all data
echo "Cleaning media folder..."
cd  rbm_website/media
mv info.txt ../
rm -rf *
mv ../info.txt .

echo "Finished, activate the virtual env with ./activate or 'source venv/bin/activate' or 'source venv/bin/activate.csh'"
