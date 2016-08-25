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

from conjur.util import urlescape, authzid, split_id
from conjur.exceptions import ConjurException
import logging


class Role(object):
    """
    Represents a Conjur [role](https://developer.conjur.net/key_concepts/rbac.html#rbac-roles).

    An instance of this class does not know whether the role in question exists.

    Generally you should create instances of this class through the `conjur.API.role` method,
    or the `Role.from_roleid` classmethod.

    Roles can provide information about their members and can check whether the role they represent
    is allowed to perform certain operations on resources.

    `conjur.User` and `conjur.Group` objects have `role` members that reference the role corresponding
    to that Conjur asset.
    """
    def __init__(self, api, account=None, kind=None, id=None):
        self.api = api
        [self.account, self.kind, self.identifier] = split_id(id)
        self.account = self.account or account or api.config.account
        self.kind = self.kind or kind
        assert self.account and (not account or self.account == account)
        assert self.kind and (not kind or self.kind == kind)
        assert self.identifier

    @classmethod
    def from_roleid(cls, api, roleid):
        """
        Creates an instance of `conjur.Role` from a full role id string.

        `api` is an instance of `conjur.API`

        `roleid` is a fully or partially qualified Conjur identifier, for example,
        `"the-account:service:some-service"` or `"service:some-service"` resolve to the same role.
        """
        return cls(api, id=authzid(roleid, 'role'))

    @property
    def roleid(self):
        """
        Return the full role id as a string.

        Example:

            >>> role = api.role('user', 'bob')
            >>> role.roleid
            'the-account:user:bob'

         """
        return ':'.join([self.account, self.kind, self.identifier])

    def is_permitted(self, resource, privilege):
        """
        Check whether `resource` has `privilege` on this role.

        `resource` is a qualified identifier for the resource.

        `privilege` is a string like `"update"` or `"execute"`.


        Example:

            >>> role = api.role('user', 'alice')
            >>> if role.is_permitted('variable:db-password', 'execute'):
            ...     print("Alice can fetch the database password")
            ... else:
            ...     print("Alice cannot fetch the database password")

        """
        params = {
            'check': 'true',
            'resource': authzid(resource, 'resource'),
            'privilege': privilege
        }
        response = self.api.get(self.url(), params=params,
                                check_errors=False)
        if response.status_code == 204:
            return True
        elif response.status_code in (403, 404):
            return False
        else:
            raise ConjurException("Request failed: %d" % response.status_code)

    def info(self):
        """
        Return role information. This will be a `dict` with the following keys:

        * `'created_at'` timestamp of role creation (eg. last refresh of the
            policy that creates it)
        * `'id'` fully qualified role id
        * `'members'` members of the role (see `members` for details)
        """
        return self.api.get(self.url()).json()

    def members(self):
        """
        Return a list of members of this role.  Members are returned as `dict`s
        with the following keys:

        * `'member'` the fully qualified identifier of the member
        * `'role'` the fully qualified identifier of the group (redundant)
        * `'admin_option'` whether this member can grant membership in the group to other roles.
        """
        return self.info()['members']

    def url(self, *args):
        return "/".join([self.api.config.url,
                         'roles',
                         self.account,
                         self.kind,
                         self.identifier] + list(args))

    def _public_keys_url(self):
        return '/'.join([
            self.api.config.url,
            'public_keys',
            self.account,
            self.kind,
            self.identifier
        ])

    def public_keys(self):
        """
        Returns all SSH public keys for this role, if any, as a newline delimited string.
        """
        return self.api.get(self._public_keys_url()).text
