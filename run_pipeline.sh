#!/usr/bin/env bash
python3 start_celery.py &
gunicorn --config gunicorn.conf --timeout 180 workflow_engine_gunicorn:app
