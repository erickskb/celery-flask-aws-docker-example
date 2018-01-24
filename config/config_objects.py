import os
import configparser

config_file = os.path.join(os.path.dirname(__file__), 'local_config.cfg')
config_parser = configparser.ConfigParser()
config_parser.read(config_file)


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


class QueueConfig:
    def __init__(self):
        try:
            self.rabbit_host = config_parser.get('QueueConfig', 'rabbit_host')
            self.rabbit_user = config_parser.get('QueueConfig', 'rabbit_user')
            self.rabbit_password = config_parser.get('QueueConfig', 'rabbit_password')
            self.rabbit_vhost = config_parser.get('QueueConfig', 'rabbit_vhost')
            self.rabbit_queue = config_parser.get('QueueConfig', 'rabbit_queue')
            self.wait_time = config_parser.get('QueueConfig', 'wait_time')
        except Exception:
            self.rabbit_host = ''
            self.rabbit_user = ''
            self.rabbit_password = ''
            self.rabbit_vhost = ''
            self.rabbit_queue = ''
            self.wait_time = 10


class CallbackTimeoutConfig:
    def __init__(self):
        try:
            self.retry_attempts = config_parser.getint('CallbackTimeoutConfig', 'retry_attempts')
            self.retry_interval = config_parser.getint('CallbackTimeoutConfig', 'retry_interval')
            self.callback_dns = config_parser.get('CallbackTimeoutConfig', 'callback_dns')
        except Exception:
            self.retry_attempts = 3
            self.retry_interval = 10
            self.callback_dns = None
