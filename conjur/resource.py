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
from conjur.role import Role
from conjur.exceptions import ConjurException


class Resource(object):
    """
    A `Resource` represents an object on which `Role`s can
    be permitted to perform certain actions.

    Generally you will not construct these directly, but call the `conjur.API.role` method
    to do so.
    """
    def __init__(self, api, kind, identifier):
        self.api = api
        self.kind = kind
        self.identifier = identifier

    @property
    def resourceid(self):
        """
        The fully qualified resource id as a string, like `'the-account:variable:db-password`.
        """
        return ":".join([self.api.config.account, self.kind, self.identifier])

    def permit(self, role, privilege, grant_option=False):
        """
        Permit `role` to perform `privilege` on this resource.

        `role` is a qualified conjur identifier (e.g. `'user:alice`') or an object
            with a `role` attribute or `roleid` method, such as a `conjur.User` or
            `conjur.Group`.

        If `grant_option` is True, the role will be able to grant this
        permission to other resources.

        You must own the resource or have the permission with `grant_option`
        to call this method.
        """
        data = {}
        params = {
            'permit': 'true',
            'privilege': privilege,
            'role': authzid(role, 'role')
        }
        if grant_option:
            data['grant_option'] = 'true'

        self.api.post(self.url(), data=data, params=params)

    def deny(self, role, privilege):
        """
        Deny `role` permission to perform `privilege` on this resource.

        You must own the resource or have the permission with `grant_option`
        on it to call this method.
        """
        params = {
            'permit': 'true',
            'privilege': privilege,
            'role': authzid(role)
        }

        self.api.post(self.url(), params=params)

    def permitted(self, privilege, role=None):
        """
        Return True if `role` has `privilege` on this resource.

        `role` may be a `conjur.Role` instance, an object with a `role` method,
        or a qualified role id as a string.

        If `role` is not given, check the permission for the currently
        authenticated role.

        Example: Check that the currently authenticated role is allowed to `'read'`
            a resource.

            >>> service = api.resource('service', 'gateway')
            >>> if service.permitted('read'):
            ...     print("I can read 'service:gateway'")
            ... else:
            ...     print("I cannot read 'service:gateway'")

        Example: Check whether members of group 'security_admin' can 'update'
            a resource.

            >>> service = api.resource('service', 'gateway')
            >>> security_admin = api.group('security_admin')
            >>> if service.permitted('update', security_admin):
            ...     print("security_admin members can update service:gateway")
            >>> else:
            ...     print("security_admin members cannot update service:gateway")
        """

        if role is None:
            # Handle self role check
            response = self.api.get(self.url(),
                                    params={'check': 'true',
                                            'privilege': privilege},
                                    check_errors=False)
            if response.status_code == 204:
                return True
            elif response.status_code in (404, 403):
                return False
            else:
                raise ConjurException("Request failed: %d" % response.status_code)
        else:
            # Otherwise call role.is_permitted
            return Role.from_roleid(self.api, role).is_permitted(self, privilege)

    def url(self):
        """
        Internal method to return a url for this object as a string.
        """
        return "/".join([
            self.api.config.authz_url,
            self.api.config.account,
            'resources',
            self.kind,
            self.identifier
        ])
