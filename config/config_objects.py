import os
import configparser

config_file = os.path.join(os.path.dirname(__file__), 'local_config.cfg')
config_parser = configparser.ConfigParser()
config_parser.read(config_file)


class CeleryConfig:
    def __init__(self):
        self.sqs_queue_name = os.getenv('SQS_QUEUE_NAME')
        if self.sqs_queue_name is None:
            self.sqs_queue_name = config_parser.get('CeleryConfig', 'sqs_queue_name')
        self.results_table = os.getenv('CELERY_RESULTS_TABLE')
        if self.results_table is None:
            self.results_table = config_parser.get('CeleryConfig', 'results_table')


class AWSConfig:
    def __init__(self):
        try:
            self.aws_access_key = config_parser.get('AWSConfig', 'aws_access_key')
            self.aws_access_key_secret = config_parser.get('AWSConfig', 'aws_access_key_secret')
            self.aws_region = config_parser.get('AWSConfig', 'aws_region')

            # set these for boto3
            os.environ['AWS_ACCESS_KEY_ID'] = self.aws_access_key
            os.environ['AWS_SECRET_ACCESS_KEY'] = self.aws_access_key_secret
            os.environ['AWS_DEFAULT_REGION'] = self.aws_region
        except:
            # these hopefully exist in the env
            pass


class DebugConfig:
    def __init__(self):
        try:
            self.debug_mode = config_parser.getboolean('DebugConfig', 'debug_mode')
        except:
            self.debug_mode = False
