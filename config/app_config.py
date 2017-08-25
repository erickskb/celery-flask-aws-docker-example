import logging

from flask import Flask

from config.flask_api import WorkflowEngineAPI
from config.config_objects import AWSConfig
from workflow_engine.status_endpoint import StatusEndpoint
from workflow_engine.workflow_entry_endpoint import WorkflowEntryEndpoint


# basic logging setup
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


# Flask app setup
app = Flask(__name__)

# flask-restful. PyCharm doesnt like the type here, but it is correct
api = WorkflowEngineAPI(app, catch_all_404s=True)

AWSConfig()

api.add_resource(StatusEndpoint, '/status')
api.add_resource(WorkflowEntryEndpoint, '/workflow-entry')





