from flask_restful import Api


# custom error handling setup
class WorkflowEngineAPI(Api):
    def handle_error(self, handled_exception):
        code = getattr(handled_exception, 'status_code', None)
        # try the other field name possibility
        if code is None:
            code = getattr(handled_exception, 'code', 500)
        message = getattr(handled_exception, 'message', None)
        if message is None:
            message = getattr(handled_exception, 'description', None)
        if message is None:
            message = handled_exception.args[0]
        exception = getattr(handled_exception, 'exception', None)
        if exception is not None:
            return self.make_response({'message': str(message), 'exception': str(exception)}, code)
        else:
            return self.make_response({'message': str(message)}, code)


