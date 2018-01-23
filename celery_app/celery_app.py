from __future__ import absolute_import

from celery import Celery

from config.config_objects import AWSConfig, QueueConfig

aws_config = AWSConfig()
queue_config = QueueConfig()

worker_app = Celery('magic_engine',
                    broker='amqp://{}:{}@{}/{}'.format(queue_config.rabbit_user, queue_config.rabbit_password,
                                                       queue_config.rabbit_host,
                                                       queue_config.rabbit_vhost),
                    include=['magic_engine.magical_functions'])

worker_app.conf.worker_prefetch_multiplier = 1

# max timeout.  See "http://docs.celeryproject.org/en/latest/getting-started/brokers/sqs.html?highlight=sqs"
# worker_app.conf.broker_transport_options = {'region': aws_config.aws_region,
#                                             'visibility_timeout': 43200}
