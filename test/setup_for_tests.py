import time
from multiprocessing import Process

from config.app_config import app
from config.config_objects import DebugConfig

STATUS_ENDPOINT = '/status'
WORKFLOW_ENTRY_ENDPOINT = '/workflow-entry'

host = '127.0.0.1'  # local host for tests
valid_port = '5000'  # default port for tests
test_url = "http://" + host + ":" + valid_port

debug_config = DebugConfig()
debug_mode = debug_config.debug_mode


def run_server():
    app.run()

# server process for testing
server = Process(target=run_server)
server.daemon = True


def start_test_server():
    if not server.is_alive():
        server.start()
        time.sleep(5)  # wait for server to start
