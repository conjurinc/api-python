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
import requests

import conjur


@patch.object(requests, 'post')
def test_create_user(mock_post):
    api = conjur.new_from_token('token')
    mock_post.return_value = resp = Mock()
    resp.status_code = 200
    resp.json = lambda:  {'login': 'foo', 'api_key': 'apikey'}

    user_no_pass = api.create_user('foo')
    assert user_no_pass.login == 'foo'
    assert user_no_pass.api_key == 'apikey'
    mock_post.assert_called_with(
        '{0}/users'.format(api.config.core_url),
        data={'login': 'foo'},
        headers={'Authorization': api.auth_header()},
        verify=api.config.verify
    )

    api.create_user('foo', 'bar')
    mock_post.assert_called_with(
        '{0}/users'.format(api.config.core_url),
        data={'login': 'foo', 'password': 'bar'},
        headers={'Authorization': api.auth_header()},
        verify=api.config.verify
    )


@patch.object(requests, 'get')
def test_user(mock_get):
    api = conjur.new_from_token('token')
    mock_get.return_value = Mock(status_code=200, json=lambda: {'foo': 'bar'})
    user = api.user('login')
    assert user.foo == 'bar'
    mock_get.assert_called_with(
        '{0}/users/login'.format(api.config.core_url),
        headers={'Authorization': api.auth_header()},
        verify=api.config.verify
    )


def test_user_role():
    user = conjur.new_from_key('foo', 'bar').user('someone')
    role = user.role
    assert role.kind == 'user'
    assert role.identifier == 'someone'
