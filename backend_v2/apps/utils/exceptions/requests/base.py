class QuerySetException(Exception):
    def __init__(self, errors, message):
        self.errors= errors
        self.message = message
        
class RequestException(Exception):
    def __init__(self, message):
        self.message = message

class JWTException(Exception):
    def __init__(self, message):
        self.message = message