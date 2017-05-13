#!/usr/bin/env bash

clear
echo "Installing and activating virtual environment..."
virtualenv env
source env/bin/activate
pip install -r requirements.txt

echo "Installing Wordplease..."
python manage.py migrate

echo "Creating users (including admin)..."
python manage.py loaddata users
echo "Password for all users is: 'seguridad'"

echo "Creating categories..."
python manage.py loaddata categories

echo "Creating blogs..."
python manage.py loaddata blogs

echo "Creating media folder..."
mkdir media

echo "Deactivating virtual environment..."
deactivate

echo "There you go! Happy blogging!"
echo ""
echo "Run the following commands to see the magic:"
echo "$ source env/bin/activate  # activates the virtual environment"
echo "$ python manage.py runserver  # runs Django test server"
echo "In a different terminal:"
echo "$ source env/bin/activate  # activates the virtual environment"
echo "$ celery worker -A wordplease # runs celery worker"
