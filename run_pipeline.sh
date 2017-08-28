#!/usr/bin/env bash
python3 start_celery.py &
gunicorn --config gunicorn.conf -b 0.0.0.0 --timeout 180 workflow_engine_gunicorn:app
