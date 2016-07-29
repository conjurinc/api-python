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
    def __init__(self, api, kind, identifier):
        """
        Create a role to represent the Conjur role with id `<kind>:<identifier>`.  For
        example, to represent the role associated with a user named bob,

            role = Role(api, 'user', 'bob')

        `api` must be a `conjur.API` instance, used to implement this classes interactions with Conjur

        `kind` is a string giving the role kind

        `identifier` is the unqualified identifier of the role.
        """

        self.api = api
        """
        The `conjur.API` instance used to implement our methods.
        """

        self.kind = kind
        """
        The `kind` portion of the role's id.
        """

        self.identifier = identifier
        """
        The `identifier` portion of the role's id.
        """

    @classmethod
    def from_roleid(cls, api, roleid):
        """
        Creates an instance of `conjur.Role` from a full role id string.

        `api` is an instance of `conjur.API`

        `roleid` is a fully or partially qualified Conjur identifier, for example,
        `"the-account:service:some-service"` or `"service:some-service"` resolve to the same role.
        """
        tokens = authzid(roleid, 'role').split(':', 3)
        if len(tokens) == 3:
            tokens.pop(0)
        return cls(api, *tokens)

    @property
    def roleid(self):
        """
        Return the full role id as a string.

        Example:

            >>> role = api.role('user', 'bob')
            >>> role.roleid
            'the-account:user:bob'

         """
        return ':'.join([self.api.config.account, self.kind, self.identifier])

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
            'resource_id': authzid(resource, 'resource'),
            'privilege': privilege
        }
        response = self.api.get(self._url(), params=params,
                                check_errors=False)
        if response.status_code == 204:
            return True
        elif response.status_code in (403, 404):
            return False
        else:
            raise ConjurException("Request failed: %d" % response.status_code)

    def grant_to(self, member, admin=None):
        """
        Grant this role to `member`.

        `member` is a string or object with a `role` attribute or `roleid` method,
            such as a `conjur.User` or `conjur.Group`.

        `admin` whether the member can grant this role to others.

        """
        data = {}
        if admin is not None:
            data['admin'] = 'true' if admin else 'false'
        self.api.put(self._membership_url(member), data=data)

    def revoke_from(self, member):
        """
        The inverse of `conjur.Role.grant_to`.  Removes `member` from the members of this
        role.

        `member` is a string or object with a `role` attribute or `roleid` method,
            such as a `conjur.User` or `conjur.Group`.
        """
        self.api.delete(self._membership_url(member))

    def members(self):
        """
        Return a list of members of this role.  Members are returned as `dict`s
        with the following keys:

        * `'member'` the fully qualified identifier of the group
        * `'role'` the fully qualified identifier of the group (redundant)
        * `'grantor'` the role that granted the membership
        * `'admin_option'` whether this member can grant membership in the group to other roles.
        """
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
