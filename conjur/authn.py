import requests
from conjur.config import config

class Authn:
    def __init__(self, login, api_key):
        self.login = login
        self.api_key = api_key

    def authenticate(self):
        """
        Return an token that can be used to authenticate
        requests to other Conjur services.
        """
        response = requests.post(self.url(), self.api_key)
        if response.code != 200:
            raise Exception("Authentication failed")
        return response.text

    def url(self):
        """
        Return the url used to retreive Conjur authn tokens.
        """
        return "%s/users/%s/authenticate"%(config.authn_url, self.login)
