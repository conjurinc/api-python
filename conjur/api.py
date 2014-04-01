import requests
import base64
from conjur.variable import Variable
from conjur.user import User
from conjur import ConjurException
from conjur.util import urlescape
from conjur.role import Role

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
        self.token = response.text
        return self.token

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

    def delete(self, url, **kwargs):
        return self.request('delete', url, **kwargs)

    def role(self, kind, identifier):
        return Role(self, kind, identifier)


    def variable(self, id):
        return Variable(self, id)

    def create_variable(self, id=None, mime_type='text/plain', kind='secret', value=None):
        data = {'mime_type': mime_type, 'kind': kind}
        if id is not None:
            data['id'] = id
        if value is not None:
            data['value'] = value

        attrs = self.post("%s/variables"%self.config.core_url, data=data).json
        id = id or attrs['id']
        return Variable(self, id)

    def user(self, login):
        return User(self, login)

    def create_user(self, login, password=None):
        '''
        Create a Conjur user with the given login.  If password is not given,
        the user will only be able to authenticate using the generated api_key
        attribute of the returned User instance.
        '''
        data = {'login': login}
        if password is not None:
            data['password'] = password
        url = "{0}/users".format(self.config.core_url)
        return User(self, login, self.post(url, data=data).json)

    def _public_key_url(self, *args):
        return '/'.join([self.config.pubkeys_url] + [urlescape(arg) for arg in args])

    def add_public_key(self, username, key):
        """
        Upload an openssh formatted key to be made available for the given
        username.
        """
        self.post(self._public_key_url(username), data=key)

    def remove_public_key(self, username, keyname):
        """
        Remove a specific public key for this user.  The keyname
        indicates the name field in the openssh formatted key that was
        uploaded.
        """
        self.delete(self._public_key_url(username, keyname))

    def remove_public_keys(self, username):
        """
        Remove all of username's public keys.
        """
        for keyname in self.public_key_names(username):
            self.remove_public_key(username, keyname)

    def public_keys(self, username):
        """
        Returns all public keys for :username: as a newline separated
        str (because this is the format expected by the authorized-keys-command)
        """
        return self.get(self._public_key_url(username)).text

    def public_key(self, username, keyname):
        """
        Return the contents of a specific public key.  The name of the key
        is based on the name entry of the openssh formatted key that was uploaded.
        """
        return self.get(self._public_key_url(username, keyname)).text

    def public_key_names(self, username):
        """
        Return the names of public keys  for this user.
        """
        return [k.split(' ')[-1] for k in self.public_keys(username).split('\n')]



