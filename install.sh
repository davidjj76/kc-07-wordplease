#!/usr/bin/env bash

clear
if [ -d "env" ]; then
    echo "Removing 'env' folder..."
    rm -rf env
fi
echo "Installing and activating virtual environment..."
virtualenv env
source env/bin/activate
pip install -r requirements.txt --no-cache-dir

if [ -e "db.sqlite3" ]; then
    echo "Removing database..."
    rm -r db.sqlite3
fi
echo "Installing Wordplease..."
python manage.py migrate

echo "Creating users (including admin)..."
python manage.py loaddata users
echo "Password for all users is 'seguridad'"

echo "Creating categories..."
python manage.py loaddata categories

echo "Creating blogs..."
python manage.py loaddata blogs

echo "Creating posts..."
python manage.py loaddata posts

if [ -d "media" ]; then
    echo "Removing 'media' folder..."
    rm -rf media
fi
echo "Creating media folder..."
mkdir media

if [ -d "logs" ]; then
    echo "Removing 'logs' folder..."
    rm -rf logs
fi
echo "Creating logs folder..."
mkdir logs

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
