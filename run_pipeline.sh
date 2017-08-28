#!/usr/bin/env bash
python3 start_celery.py &
gunicorn -b 0.0.0.0 --timeout 180 workflow_engine_gunicorn:app
