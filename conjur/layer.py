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

from conjur.util import urlescape, authzid
from conjur.exceptions import ConjurException


class Layer(object):
    def __init__(self, api, id, attrs=None):
        self.api = api
        self.id = id
        self._attrs = {} if attrs is None else attrs

    def add_host(self, host):
        hostid = authzid(host, 'role', with_account=False)
        self.api.post(self._hosts_url(), data={'hostid': hostid})

    def remove_host(self, host):
        hostid = authzid(host, 'role')
        self.api.delete(self._host_url(hostid))

    def exists(self):
        resp = self.api.get(self._url(), check_errors=False)
        if resp.status_code == 200:
            return True
        if resp.status_code == 404:
            return False
        raise ConjurException("Request Failed: {0}".format(resp.status_code))

    def _url(self):
        return "{0}/layers/{1}".format(self.api.config.core_url,
                                       urlescape(self.id))

    def _hosts_url(self):
        return "{0}/hosts".format(self._url())

    def _host_url(self, host_id):
        return "{0}/{1}".format(self._hosts_url(), urlescape(host_id))

    def _fetch(self):
        self._attrs = self.api.get(self._url()).json()

    def __getattr__(self, item):
        if self._attrs is None:
            self._fetch()
        try:
            return self._attrs[item]
        except KeyError:
            raise AttributeError(item)
