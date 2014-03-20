import base64
import json


class Token(object):

    def __init__(self, data):
        self._data = data
        self._parsed = json.loads(data)

    def header(self):
        """
        Return a header value that can be used to authenticate with this token.
        """
        return 'Token token="%s"' % (base64.b64encode(self._data),)

    def valid(self):
        # TODO check validity based on expiration
        return True
