import logging
import json

from flask import request, Response
from flask_restful import Resource

from celery_app.celery_app import queue_config
from magic_engine.service_exceptions import RequestException
from magic_engine.magical_functions import make_magic, generate_identifier

logger = logging.getLogger()


class MagicalEndpoint(Resource):
    def post(self):
        body = json.loads(request.data.decode())

        try:
            message = body['Message']
            callback_url = body['callbackURL']
        except KeyError as key_error:
            raise RequestException('Request does not appear to be a valid celery spike request: {}'.format(key_error),
                                   status_code=400)

        request_id = generate_identifier()

        logger.info('Sending magical task {} to Celery queue {}'.format(request_id,
                                                                        queue_config.rabbit_queue))
        result = make_magic.apply_async(args=(message, callback_url, request_id,), queue=queue_config.rabbit_queue)
        response = ("Magical task {} sent to Celery queue {}. Celery ID: {}".format(request_id,
                                                                                    queue_config.rabbit_queue,
                                                                                    result))
        logger.info(response)

        return Response(json.dumps(response), mimetype='hal+json', status=202)
