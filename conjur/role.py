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
from conjur import ConjurException
import logging


class Role(object):
    def __init__(self, api, kind, identifier):
        self.api = api
        self.kind = kind
        self.identifier = identifier

    @classmethod
    def from_roleid(cls, api, roleid):
        tokens = authzid(roleid, 'role').split(':', 3)
        if len(tokens) == 3:
            tokens.pop(0)
        return cls(api, *tokens)

    @property
    def roleid(self):
        return ':'.join([self.api.config.account, self.kind, self.identifier])

    def is_permitted(self, resource, privilege):
        params = {
            'check': 'true',
            'resource_id': authzid(resource, 'resource'),
            'privilege': privilege
        }
        response = self.api.get(self._url(), params,
                                check_errors=False)
        if response.status_code < 300:
            return True
        elif response.status_code in (403, 404, 409):
            return False
        else:
            raise ConjurException("Request failed: %d" % response.status_code)

    def grant_to(self, member, admin=None):
        data = {}
        if admin is not None:
            data['admin'] = 'true' if admin else 'false'
        logging.info("Adding member with {} and data of {}".format(
            self._membership_url(member), repr(data)))
        self.api.put(self._membership_url(member), data=data)

    def revoke_from(self, member):
        self.api.delete(self._membership_url(member))

    def members(self):
        logging.info('Getting members from {}'.format(self._membership_url()))
        return self.api.get(self._membership_url()).json()

    def _membership_url(self, member=None):
        url = self._url() + "?members"
        if member is not None:
            memberid = authzid(member, 'role')
            url += "&member=" + urlescape(memberid)
        return url

    def _url(self, *args):
        return "/".join([self.api.config.authz_url,
                         self.api.config.account,
                         'roles',
                         self.kind,
                         self.identifier] + list(args))
