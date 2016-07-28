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


class Group(object):
    """
    Represents a Conjur [group](https://developer.conjur.net/reference/services/directory/group).

    Generally you won't create instances of this class, but use the `conjur.API.group(id)` method.

    A group is a role that contains other roles, typically users and other groups.  A `conjur.Group`
    object can list its members with the `members` method, and also manage them with the `add_member`
    and `remove_member` methods.
    """
    def __init__(self, api, id):
        self.api = api
        """
        Instance of `conjur.API` used to implement Conjur operations.
        """

        self.id = id
        """
        Identifier (unqualified) of the group.
        """

        self.role = api.role('group', id)
        """
        Represents the `conjur.Role` associated with this group.
        """

    def members(self):
        """
        Return a list of members of this group.  Members are returned as `dict`s
        with the following keys:

        * `'member'` the fully qualified identifier of the group
        * `'role'` the fully qualified identifier of the group (redundant)
        * `'grantor'` the role that granted the membership
        * `'admin_option'` whether this member can grant membership in the group to other roles.

        Example: print member ids (fully qualified) and whether they are admins of the group.
            >>> group = api.group('security_admin')
            >>> for member in group.members():
            ...     print('{} is a member of security_admin ({} admin option)'.format(
            ...         member['member'],
            ...         'with' if member['admin_option'] else 'without'
            ...     ))
        """
        return self.role.members()

    def add_member(self, member, admin=False):
        """
        Add a member to this group.

        `member` is the member we want to add to the group, and  should be a qualified Conjur id,
            or an object with a `role` attribute or a `roleid` method.  Examples of such objects
            include `conjur.User`, `conjur.Role`, and `conjur.Group`.

        If `admin` is True, the member will be allowed to add other members to this group.
        """
        self.role.grant_to(member, admin)

    def remove_member(self, member):
        """
        Remove a member from the group.

        `member` is the member to remove, and  should be a qualified Conjur id,
            or an object with a `role` attribute or a `roleid` method.  Examples of such objects
            include `conjur.User`, `conjur.Role`, and `conjur.Group`.
        """
        self.role.revoke_from(member)
