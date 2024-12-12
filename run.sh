#!/bin/bash

cd gateway && sh bin/run.sh root/conf.yaml &

# Create virtual environment and install dependencies
python3 -m venv venv && . venv/bin/activate && venv/bin/pip install flask requests gunicorn

# Start Gunicorn with environment variables
gunicorn --bind 0.0.0.0:5056 --workers 2 --threads 4 --timeout 180 run:app