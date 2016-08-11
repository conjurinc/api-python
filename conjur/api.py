#
# Copyright (C) 2014-2016 Conjur Inc
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

import base64

import requests

from conjur.role import Role
from conjur.resource import Resource
from conjur.util import urlescape
from conjur.exceptions import ConjurException

class API(object):
    def __init__(self, credentials=None, token=None, config=None):
        """
        Creates an API instance configured with the given credentials or token
        and config.

        Generally you should use `conjur.new_from_key`, `conjur.new_from_password`,
        or `conjur.new_from_token` to get an API instance instead of calling
        this constructor directly.

        `credentials` should be a `(login,api_key)` tuple if present.

        `token` should be a string containing a Conjur JSON token to use when authenticating.

        `config` should be a `conjur.Config` instance, and defaults to `conjur.config`.
        """
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
            from conjur.config import config as default_config

            self.config = default_config

    def authenticate(self, cached=True):
        """
        Authenticate with Conjur and return a token (str) that can be used
        to establish identity to Conjur services.

        Returns the json formatted signed Conjur authentication Token.

        It is an error to call this method if the API was created with a token
        rather than a login and api key.

        When `cached` is True, a cached token value will be used if it is
        available, otherwise the token will be fetched whether or not a
        cached value is present.
        """
        if cached and self.token:
            return self.token

        if not self.login or not self.api_key:
            raise ConjurException(
                "API created without credentials can't authenticate")

        url = "%s/authn/%s/%s/authenticate" % (self.config.url,
                                            self.config.account,
                                            urlescape(self.login))

        self.token = self._request('post', url, self.api_key).text
        return self.token

    def auth_header(self):
        """
        Get the value of an Authorization header to make Conjur requests,
        performing authentication if necessary.

        Returns a string suitable for use as an `Authorization` header value.
        """
        token = self.authenticate()
        enc = base64.b64encode(token)
        return 'Token token="%s"' % enc

    def request(self, method, url, **kwargs):
        """
        Make an authenticated request with the given method and url.
        Additional arguments are passed to requests.<method>.

        Returns a `requests.Response` object.

        If the response status is not 2xx, raises a `conjur.ConjurException`.

        `method` is of the standard HTTP verbs (case insensitive).

        `url` is the full url to request.

        If `kwargs['check_errors']` is `True`, non-2xx responses will raise a `conjur.ConjurException`.
        Otherwise, it is the callers responsibility to check the status of the returned `requests.Response`.

        Additional are passed through to the requests.<method> call after adding an `Authorization`
        header and HTTPS verification settings.
        """
        headers = kwargs.setdefault('headers', {})
        headers['Authorization'] = self.auth_header()

        return self._request(method, url, **kwargs)

    def _request(self, method, url, *args, **kwargs):
        if 'verify' not in kwargs:
            kwargs['verify'] = self.config.verify
        check_errors = kwargs.pop('check_errors', True)

        response = getattr(requests, method.lower())(url, *args, **kwargs)
        if check_errors and response.status_code >= 300:
            raise ConjurException("Request failed: %d" % response.status_code)

        return response

    def get(self, url, **kwargs):
        """
        **NOTE** You will generally not need to use this method directly.

        Makes an authenticated GET request to the given :url:.

        Returns a requests.Response object.

        If the response status is not 2xx, raises a ConjurException.

        `url` is the full url to request.
         Keyword arguments are passed through to `requests.get`.
        """
        return self.request('get', url, **kwargs)

    def post(self, url, **kwargs):
        """
        **NOTE** You will generally not need to use this method directly.

        Makes an authenticated `POST` request to the given `url`

        Returns a `requests.Response` object.

        If the response status is not 2xx, raises a `conjur.ConjurException`.

        `url` is the full url to request.
         Keyword arguments are passed through to `requests.post`.
        """
        return self.request('post', url, **kwargs)

    def put(self,url, **kwargs):
        """
        **NOTE** You will generally not need to use this method directly.

        Makes an authenticated `PUT` request to the given `url`

        Returns a `requests.Response` object.

        If the response status is not 2xx, raises a `conjur.ConjurException`.

        `url` is the full url to request.
         Keyword arguments are passed through to `requests.put`.
        """
        return self.request('put', url, **kwargs)

    def delete(self, url, **kwargs):
        """
        **NOTE** You will generally not need to use this method directly.

        Makes an authenticated `DELETE` request to the given `url`

        Returns a `requests.Response` object.

        If the response status is not 2xx, raises a `conjur.ConjurException`.

        `url` is the full url to request.
         Keyword arguments are passed through to `requests.delete`.
        """
        return self.request('delete', url, **kwargs)

    def role(self, kind, identifier):
        """
        Return a `conjur.Role` object with the given kind and id.

        This method neither creates nor checks for the roles's existence.

        `kind` should be the role kind - for example, `"group"`, `"user"`,
        or `"host"`.

        `identifier` should be the *unqualified* Conjur id.  For example, to
        get the role for a user named bub, you would call `api.role('user', 'bub')`.
        """
        return Role(self, kind, identifier)

    def resource(self, kind, identifier):
        """
        Return a `conjur.Resource` object with the given kind and id.

        This method neither creates nor checks for the resource's existence.

        `kind` should be the resource kind - for example, `"variable"`, `"webservice"`,
        or `"configuration"`.

        `identifier` should be the *unqualified* Conjur id.  For example, to
        get the resource for a user variable named db_password, you would call
        `api.resource('variable', 'db_password')`.
        """
        return Resource(self, kind, identifier)
