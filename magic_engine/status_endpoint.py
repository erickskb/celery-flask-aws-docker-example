import json

from flask import Response
from flask_restful import Resource


class StatusEndpoint(Resource):
    def get(self):
        response_body = dict()  # change body from list to dictionary
        response_body['status'] = 'OK'

        return Response(json.dumps(response_body), mimetype='application/json')
