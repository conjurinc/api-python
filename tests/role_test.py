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
config.url = 'http://possum.test'


def test_roleid():
    role = api.role('some-kind', 'the-id')
    assert role.roleid == 'the-account:some-kind:the-id'


def test_role_qualified():
    role = api.role_qualified('foo:bar:baz')
    assert role.url() == 'http://possum.test/roles/foo/bar/baz'


role_info = {
    u'id': u'cucumber:group:everyone',
    u'members': [
        {
            u'member': u'cucumber:user:admin',
            u'role': u'cucumber:group:everyone',
            u'grantor': u'cucumber:group:everyone',
            u'admin_option': True
        }, {
            u'member': u'cucumber:user:alice',
            u'role': u'cucumber:group:everyone',
            u'grantor': u'cucumber:group:everyone',
            u'admin_option': False
        }
    ]
}

@patch.object(api, 'get')
def test_role_members(mock_get):
    mock_get.return_value = Mock(json=lambda: role_info)
    role = api.role('blah', 'boo')
    assert role.members() == role_info['members']
    mock_get.assert_called_with(
        'http://possum.test/roles/the-account/blah/boo'
    )
@patch.object(api, 'get')
def test_public_keys(mock_get):
    response = "a b key1\na b key2"
    mock_get.return_value = Mock(text=response)
    user = api.role('user', 'somebody')
    assert user.public_keys() == response
    mock_get.assert_called_with(
        'http://possum.test/public_keys/the-account/user/somebody'
    )
