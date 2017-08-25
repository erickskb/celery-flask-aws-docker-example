from __future__ import absolute_import

from celery import Celery

from config.config_objects import AWSConfig, CeleryConfig

aws_config = AWSConfig()
celery_config = CeleryConfig()

worker_app = Celery('workflow_engine',
                    broker='sqs://',
                    backend='dynamodb://{}:{}@{}/{}'.format(aws_config.aws_access_key, aws_config.aws_access_key_secret,
                                                            aws_config.aws_region, celery_config.results_table),
                    include=['workflow_engine.workflow_entry_endpoint'])

# max timeout.  See "http://docs.celeryproject.org/en/latest/getting-started/brokers/sqs.html?highlight=sqs"
worker_app.conf.broker_transport_options = {'region': aws_config.aws_region,
                                            'visibility_timeout': 43200}

# pre-fetch only 1 task at a time
worker_app.conf.worker_prefetch_multiplier = 1


def start_celery_worker():
    worker_name = '-n {}'.format(celery_config.sqs_queue_name)
    worker_name += '@%h'  # %h gives hostname + domain name

    argv = ['worker', '-Q{}'.format(celery_config.sqs_queue_name), '-lINFO', worker_name]

    worker_app.worker_main(argv)
