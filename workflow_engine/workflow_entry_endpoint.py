import logging
import json

from flask import request, Response
from flask_restful import Resource
from celery.utils.log import get_task_logger

from celery_app.celery_app import worker_app, celery_config
from config.config_objects import DebugConfig
from workflow_engine.service_exceptions import RequestException

debug_config = DebugConfig()

logger = logging.getLogger()


@worker_app.task(acks_late=True, track_started=True)
def ingest_item(message):
    task_logger = get_task_logger(__name__)

    if 'fail' in message:
        raise Exception('failure test')

    task_logger.info('Processing request item')

    import time
    time.sleep(30)

    return 'TEST_RESULT'


class WorkflowEntryEndpoint(Resource):
    def post(self):
        body = json.loads(request.data.decode())

        try:
            message_id = body['MessageId']
            message = body['Message']
        except KeyError as key_error:
            raise RequestException('Request does not appear to be a valid SNS message: {}'.format(key_error),
                                   status_code=400)

        if not debug_config.debug_mode:
            logger.info('Sending Ingest Item task {} to Celery queue {}'.format(message_id,
                                                                                celery_config.sqs_queue_name))
            result = ingest_item.apply_async(args=(message,), queue=celery_config.sqs_queue_name)
            logger.info("Ingest Item task {} sent to Celery queue {}. SQS ID: {}".format(message_id,
                                                                                         celery_config.sqs_queue_name,
                                                                                         result))
        elif debug_config.debug_mode:
            ingest_item(message)

        return Response(status=200)
