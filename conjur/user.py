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


class User(object):
    def __init__(self, api, login, attrs=None):
        self.api = api
        self.login = login
        # support as_role
        self.role = api.role('user', login)
        self._attrs = attrs

    def exists(self):
        resp = self.api.get(self.url(), check_errors=False)
        return resp.status_code != 404

    def __getattr__(self, item):
        if self._attrs is None:
            self._fetch()
        try:
            return self._attrs[item]
        except KeyError:
            raise AttributeError(item)

    def _fetch(self):
        self._attrs = self.api.get(self.url()).json()

    def url(self):
        return "{0}/users/{1}".format(self.api.config.core_url,
                                      urlescape(self.login))
