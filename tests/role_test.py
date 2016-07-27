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

from mock import patch, Mock
from conjur import Config, new_from_key
config = Config()
api = new_from_key('login', 'pass', config)
config.account = 'the-account'
config.appliance_url = 'https://example.com/api'


def test_roleid():
    role = api.role('some-kind', 'the-id')
    assert role.roleid == 'the-account:some-kind:the-id'


@patch.object(api, 'put')
def test_role_grant_to_without_admin(mock_put):
    role = api.role('some-kind', 'the-id')
    role.grant_to('some-other-role')
    mock_put.assert_called_with(
        '{0}/the-account/roles/some-kind/the-id?members&member={1}'.format(
            config.authz_url,
            'some-other-role'
        ),
        data={}
    )


@patch.object(api, 'put')
def test_role_grant_to_with_admin_true(mock_put):
    role = api.role('some-kind', 'the-id')
    role.grant_to('some-other-role', True)
    mock_put.assert_called_with(
        '{0}/the-account/roles/some-kind/the-id?members&member={1}'.format(
            config.authz_url,
            'some-other-role'
        ),
        data={'admin': 'true'}
    )


@patch.object(api, 'put')
def test_role_grant_to_with_admin_false(mock_put):
    role = api.role('some-kind', 'the-id')
    role.grant_to('some-other-role', False)
    mock_put.assert_called_with(
        '{0}/the-account/roles/some-kind/the-id?members&member={1}'.format(
            config.authz_url,
            'some-other-role'
        ),
        data={'admin': 'false'}
    )


@patch.object(api, 'delete')
def test_role_revoke_from(mock_del):
    role = api.role('some-kind', 'the-id')
    role.revoke_from('some-other-role')
    mock_del.assert_called_with(
        '{0}/the-account/roles/some-kind/the-id?members&member={1}'.format(
            config.authz_url,
            'some-other-role'
        )
    )


@patch.object(api, 'get')
def test_role_members(mock_get):
    members = ['foo', 'bar']
    mock_get.return_value = Mock(json=lambda: members)
    role = api.role('blah', 'boo')
    assert role.members() == members
    mock_get.assert_called_with(
        '{0}/the-account/roles/blah/boo?members'.format(config.authz_url)
    )


@patch.object(api, 'put')
def test_role_grant_to_user(mock_put):
    role = api.role('somekind', 'admins')
    user = api.user('somebody')
    role.grant_to(user)
    mock_put.assert_called_with(
        '{0}/the-account/roles/somekind/admins?members&member={1}'.format(
            config.authz_url,
            'the-account%3Auser%3Asomebody'
        ),
        data={}
    )
