import requests
import conjur.token as token

class Connection(object):
    def __init__(self, login, api_key, config):
        self.login = login
        self.api_key = api_key
        self.config = config
        self._token = None

    def token(self, cached=True):
        if cached and self._token and self._token.valid(): return self._token
        self.authenticate()
        return self._token

    def authenticate(self):
        url = "%s/users/%s/authenticate"%(self.config.authn_url, self.login)
        response = requests.post(url, self.api_key)
        if response.code != 200:
            raise Exception("Authentication failed: %d"%(response.code))
        return token.Token(response.text)

    def user(self, id):
        pass

    def role(self, id):
        pass

    def resource(self, id):
        pass

    def group(self, id):
        pass

    def variable(self, id):
        pass