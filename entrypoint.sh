#!/bin/bash

echo "Running migrations..."
python manage.py makemigrations

echo "Starting server..."
python manage.py runserver 0.0.0.0:8000