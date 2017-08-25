from celery_app.celery_app import start_celery_worker
from config.config_objects import AWSConfig

aws_config = AWSConfig()
start_celery_worker()
