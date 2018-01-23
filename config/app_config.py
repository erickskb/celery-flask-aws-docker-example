import logging

from flask import Flask

from config.flask_api import WorkflowEngineAPI
from config.config_objects import AWSConfig, CallbackTimeoutConfig
from magic_engine.status_endpoint import StatusEndpoint
from magic_engine.magical_endpoint import MagicalEndpoint


# basic logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# Flask app setup
app = Flask(__name__)

# flask-restful. PyCharm doesnt like the type here, but it is correct
api = WorkflowEngineAPI(app, catch_all_404s=True)

AWSConfig()
callback_config = CallbackTimeoutConfig()

api.add_resource(StatusEndpoint, '/status')
api.add_resource(MagicalEndpoint, '/workflow-entry')





