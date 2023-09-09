#!/bin/bash
# Run the command and capture the output
python manage.py check && \
python manage.py makemigrations && \
python manage.py migrate && \
python manage.py runserver 0.0.0.0:8000