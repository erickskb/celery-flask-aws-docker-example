import requests
import urllib3
import json
from copy import deepcopy

from test.setup_for_tests import *

urllib3.disable_warnings()  # turn off annoying ssl warnings

BASIC_SNS_REQUEST = {
    "Type": "Notification",
    "MessageId": "da41e39f-ea4d-435a-b922-c6aae3915ebe",
    "TopicArn": "arn:aws:sns:us-west-2:123456789012:MyTopic",
    "Subject": "test",
    "Message": "test message",
    "Timestamp": "2012-04-25T21:49:25.719Z",
    "SignatureVersion": "1",
    "Signature": "Gpij7RCW7AW9vYYsSqIKRnFS94ilu7NFhUzLiieYr4BKHpdTmdD6c0esKEYBpabxDSc=",
    "SigningCertURL": "https://sns.us-west-2.amazonaws.com/Simple.pem",
    "UnsubscribeURL": "https://sns.us-west-2.amazonaws.com/fbf39-05c3-41de-beaa-fcfcc21c8f55"
}


def setup_module():
    start_test_server()


class TestWorkflowEntryEndpoint:
    def test_valid_request_returns_200(self):
        response = requests.post(test_url + WORKFLOW_ENTRY_ENDPOINT, json.dumps(BASIC_SNS_REQUEST))

        assert response.status_code == 200

    def test_failing_job_returns_200_synchronously_with_celery_500_without(self):
        request = deepcopy(BASIC_SNS_REQUEST)
        request['Message'] = 'fail'

        response = requests.post(test_url + WORKFLOW_ENTRY_ENDPOINT, json.dumps(request))

        if not debug_mode:
            assert response.status_code == 200
        else:
            assert response.status_code == 500

    def test_invalid_request_missing_message_returns_400(self):
        request = deepcopy(BASIC_SNS_REQUEST)
        del request['Message']

        response = requests.post(test_url + WORKFLOW_ENTRY_ENDPOINT, json.dumps(request))

        assert response.status_code == 400
        assert 'Request does not appear to be a valid SNS message' in response.text


class TestStatusEndpoint:
    def test_get_status_ok_returns_200(self):
        response = requests.get(test_url + STATUS_ENDPOINT)

        assert 200 == response.status_code

    def test_get_status_ok_responses(self):
        response = requests.get(test_url + STATUS_ENDPOINT)

        body = response.json()
        assert body['status'] == 'OK'
