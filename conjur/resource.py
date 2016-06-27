#
# Copyright (C) 2014 Conjur Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal inre
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

from conjur.util import authzid
from conjur import ConjurException


class Resource(object):
    def __init__(self, api, kind, identifier):
        self.api = api
        self.kind = kind
        self.identifier = identifier

    @property
    def resourceid(self):
        return ":".join([self.api.config.account, self.kind, self.identifier])

    def check(self, privilege, role=None):
        '''
        Return True if +role+ has +privilege+ on this resource.

        +role+ may be a Role instance, an object with a +role+ method,
        or a role id as a string.
        '''

        params = {
            'check': True,
            'privilege': privilege
        }

        if role is not None:
            roleid = authzid(role)
            params['acting_as'] = roleid
        response = self.api.get(self.url(),
                                params=params,
                                check_errors=False)
        if response.status_code == 204:
            return True
        elif response.status_code in (404, 403, 409):
            return False
        else:
            raise ConjurException("Request failed: %d" % response.status_code)

    def url(self):
        return "/".join([
            self.api.config.authz_url,
            self.api.config.account,
            'resources',
            self.kind,
            self.identifier
        ])
