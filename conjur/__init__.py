#
# Copyright (C) 2014 Conjur Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
import os

from config import Config
from api import API
from group import Group
from user import User
from host import Host
from layer import Layer
from resource import Resource
from role import Role
from variable import Variable
from exceptions import ConjurException

from config import config

def _config(given):
    if given is None:
        env_config_file = os.getenv('CONJURRC')
        if env_config_file is not None:
            config.load(env_config_file)
        return config
    return given


def configure(**kwargs):
    """
    Convenience function to merge multiple settings into the default global
    config.

    Example:

        >>> import conjur
        >>> conjur.configure(appliance_url='https://conjur.example.com/api',
        ...              account='example',
        ...              cert_path='/path/to/cert.pem')

    """
    config.update(**kwargs)
    return config


def new_from_netrc(netrc_file=None, configuration=None):
    """
    Create a `conjur.API` instance using an identity loaded from netrc.  This method
    uses the identity stored for the host `config.authn_url`.

    `netrc_file` is an alternative path to the netrc formatted file.  Defaults
    to ~/.netrc on unixy systems.

    `configuration` is a `conjur.Config` instance used to determine the host
    in the netrc file, and also passed to the `conjur.new_from_key` method to
    create the API instance using the identity.
    """
    import netrc

    configuration = _config(configuration)
    auth = netrc.netrc(netrc_file).authenticators(configuration.authn_url)
    if auth is None:
        raise ValueError("No authenticators found for authn_url '%s' in %s" % (
            configuration.authn_url,
            (netrc_file or '~/.netrc')
        ))
    login, _, api_key = auth
    return new_from_key(login, api_key, configuration)


def new_from_key(login, api_key, configuration=None):
    """
    Create a `conjur.API` instance that will authenticate on demand as the identity given
    by `login` and `api_key`.

    `login` is the identity of the Conjur user or host to authenticate as.

    `api_key` is the api key *or* password to use when authenticating.

    `configuration` is a `conjur.Config` instance for the api.  If not given the global
        `Config` instance (`conjur.config`) will be used.
    """

    return API(credentials=(login, api_key), config=_config(configuration))


def new_from_token(token, configuration=None):
    """
    Create a `conjur.API` instance that will authenticate using the given signed Conjur
    token.

    This is useful if you want to act on behalf of a the identity of an
    HTTP request containing a user's signed token.

    `token` is the json formatted, *not* base64'd, Conjur authentication Token.

    `configuration` is a conjur.Config instance for the api.  If not given, the global Config
    instance (`conjur.config`) will be used.
    """
    return API(token=token, config=_config(configuration))

__all__ = (
    'config', 'Config', 'Group', 'API', 'User', 'Host', 'Layer', 'Resource', 'Role', 'Variable',
    'new_from_key', 'new_from_netrc', 'new_from_token', 'configure', 'ConjurException'
)