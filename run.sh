#!/bin/bash

# Start the gateway
cd gateway && sh bin/run.sh root/conf.yaml &

# Create virtual environment and install dependencies
python3 -m venv venv && . venv/bin/activate && venv/bin/pip install -r requirements.txt

# Start Gunicorn with environment variables
gunicorn --bind 0.0.0.0:5056 --timeout 180 run:app