import requests
import base64
from conjur.variable import Variable

from conjur import ConjurException


class API(object):
    def __init__(self, credentials=None, token=None, config=None):
        if credentials:
            self.login, self.api_key = credentials
            self.token = None
        elif token:
            self.token = token
            self.login = self.api_key = None
        else:
            raise TypeError("must be given a credentials or token argument")
        if config:
            self.config = config
        else:
            from conjur.config import config
            self.config = config

    def authenticate(self, cached=True):
        """
        Authenticate with Conjur and return a token (str) that can be used
        to establish identity to Conjur services.
        """
        if cached and self.token:
            return self.token
        if not self.login or not self.api_key:
            raise ConjurException("API created without a token can't authenticate")
        url = "%s/users/%s/authenticate"%(self.config.authn_url, self.login)
        response = requests.post(url, self.api_key)
        if response.status_code != 200:
            raise Exception("Authentication failed: %d"%(response.status_code,))
        return response.text

    def auth_header(self):
        """
        Get the value of an Authorization header to make Conjur requests, performing
        authentication if necessary.
        """
        token = self.authenticate()
        enc = base64.b64encode(token)
        return 'Token token="%s"'%enc


    def request(self, method, url, **kwargs):
        """
        Make an authenticated request.  Additional arguments are passed
        to requests.method.
        """
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = self.auth_header()
        response = getattr(requests, method.lower())(url, **kwargs)
        if response.status_code >= 300:
            raise ConjurException("Request failed: %d"%response.status_code)
        return response

    def get(self, url, **kwargs):
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('post', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('put', url, **kwargs)

    def variable(self, id):
        return Variable(self, id)

    def create_variable(self, id=None, mime_type='text/plain', kind='secret'):
        data = {'mime_type': mime_type, 'kind': kind}
        if id:
            data['id'] = id
        attrs = self.post("%s/variables"%(self.config.core_url), data=data).json
        id = id or attrs['id']
        return Variable(self, id)

