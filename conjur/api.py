import requests
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
        if cached and self.token:
            return self.token
        if not self.login or not self.api_key:
            raise ConjurException("API created without a token can't authenticate")
        url = "%s/users/%s/authenticate"%(self.config.authn_url, self.login)
        response = requests.post(url, self.api_key)
        if response.status_code != 200:
            raise Exception("Authentication failed: %d"%(response.status_code))
        return response.text
