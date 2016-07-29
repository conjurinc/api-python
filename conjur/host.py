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

from conjur.util import urlescape
from conjur.exceptions import ConjurException


class Host(object):
    """
    A Conjur `Host` is a role corresponding to a machine or machine identity.

    The `Host` class provides the ability to check for existence and read attributes of the
    host.

    Attributes (such as the `ownerid`) are fetched lazily.

    Newly created hosts, as returned by `conjur.API.create_host`, have an `api_key` attribute,
    but existing hosts retrieved with `conjur.API.host` or the constructor of this class *do not*
    have one.

    Example:

        >>> # Create a host and save it's api key to a file.
        >>> host = api.create_host('jenkins')
        >>> api_key = host.api_key
        >>> with open('/etc/conjur.identity') as f:
        ...     f.write(api_key)

    Example:

        >>> # See if a host named `jenkins` exists:
        >>> if api.host('jenkins').exists():
        ...     print("Host 'jenkins' exists")
        ... else:
        ...     print("Host 'jenkins' does not exist")

    """
    def __init__(self, api, id, attrs=None):
        self.api = api
        self.id = id
        self._attrs = attrs
        self.role = self.api.role('host', self.id)

    def exists(self):
        """
        Return `True` if this host exists.
        """
        status = self.api.get(self._url(), check_errors=False).status_code
        if status == 200:
            return True
        if status == 404:
            return False
        raise ConjurException("Request Failed: {0}".format(status))

    def _fetch(self):
        self._attrs = self.api.get(self._url()).json()

    def _url(self):
        return "{0}/hosts/{1}".format(self.api.config.core_url,
                                      urlescape(self.id))

    def __getattr__(self, item):
        if self._attrs is None:
            self._fetch()
        try:
            return self._attrs[item]
        except KeyError:
            raise AttributeError(item)
