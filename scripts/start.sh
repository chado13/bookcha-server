#!/bin/bash

# Run migrations
python manage.py migrate

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-3000} --reload