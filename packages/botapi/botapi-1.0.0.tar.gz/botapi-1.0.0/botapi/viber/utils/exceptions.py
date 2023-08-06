class ApiViberException(Exception):
    def __init__(self, method, result):
        super().__init__(
            "Error code: {0}. Method: {1}. Message: {2}. Description: {3}".format(
                result['code'], method, result['message'], result['description']
            ))


class ApiHttpException(Exception):
    def __init__(self, status, reason, text):
        super().__init__(
            "The server returned HTTP {0} {1}. Response body:\n[{2}]".format(
                status, reason, text
            ))


class ApiInvalidJsonException(Exception):
    def __init__(self, result):
        super().__init__(
            "The server returned an invalid JSON response. \
            Response body:\n[{0}]".format(
                result.text.encode('utf8')
            ))
