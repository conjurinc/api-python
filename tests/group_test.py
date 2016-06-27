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
from mock import patch
import conjur

api = conjur.new_from_key('foo', 'bar')

group = api.group('v1/admins')


def test_group():
    assert group.role.kind == 'group'
    assert group.role.identifier == 'v1/admins'
    assert group.role.roleid == api.config.account + ':group:v1/admins'


@patch.object(group.role, 'grant_to')
def test_add_member(mock_grant_to):
    member = api.user('foo')
    group.add_member(member)
    mock_grant_to.assert_called_with(member, False)


@patch.object(group.role, 'grant_to')
def test_add_member_admin(mock_grant_to):
    member = api.role('something', 'else')
    group.add_member(member, True)
    mock_grant_to.assert_called_with(member, True)


@patch.object(group.role, 'revoke_from')
def test_remove_member(mock_revoke_from):
    member = api.user('foo')
    group.remove_member(member)
    mock_revoke_from.assert_called_with(member)
