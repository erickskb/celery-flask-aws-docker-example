import json
import uuid

from celery.utils.log import get_task_logger
import requests
import time

from celery_app.celery_app import worker_app
from config.config_objects import CallbackTimeoutConfig

callback_config = CallbackTimeoutConfig()


@worker_app.task(acks_late=True, track_started=True)
def make_magic(message, callback_url, request_id):
    task_logger = get_task_logger(__name__)

    task_logger.info('Processing request item: {}'.format(request_id))

    time.sleep(30)

    result_json = {'message': message,
                   'requestId': request_id}

    callback(callback_url, result_json, task_logger)

    return json.dumps(result_json)


def callback(callback_url, result_json, logger_t):
    attempts = 1
    done = False

    while attempts <= callback_config.retry_attempts and done is False:
        try:
            response = requests.post(callback_url, json.dumps(result_json), headers={"Content-type": "application/json"},
                                     verify=False, timeout=30)
            if response.status_code in [200, 202, 201, 204]:
                done = True
                logger_t.info("callback_debug_log: Callback successfully made to {} for request id {}".format(
                    callback_url, result_json['requestId']))
            elif response.status_code == 401 or response.status_code == 403:
                # log authentication failure, mark success as true in order to stop retrying indefinitely
                logger_t.error('Insufficient authentication to perform callback to {}. Response code {}'.format(
                    callback_url, str(response.status_code)))
                done = True
            else:
                logger_t.error('Failed to perform callback to {}. '
                               'Response code: {} Retrying in {} sec...'
                               .format(callback_url, str(response.status_code),
                                       callback_config.retry_interval))
        except Exception as error:
            logger_t.error('Failed to perform callback to {}. Error: {}'.format(callback_url, error.args[0]))
        finally:
            if not done and attempts < callback_config.retry_attempts:
                time.sleep(callback_config.retry_interval)
                attempts += 1
            elif not done and attempts == callback_config.retry_attempts:
                raise Exception(
                    'Failed to perform callback to {} after {} attempts'.format(
                        callback_url, callback_config.retry_attempts))


def generate_identifier(prefix=None, suffix='-HAM'):
    ident = str(uuid.uuid4())
    if prefix:
        ident = prefix + ident
    if suffix:
        ident += suffix
    return ident
