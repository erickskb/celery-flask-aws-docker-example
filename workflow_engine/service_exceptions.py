class RequestException(Exception):
    def __init__(self, message, status_code=None, exception=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        if exception is not None:
            self.exception = exception
