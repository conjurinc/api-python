#
# Copyright (C) 2016 Conjur Inc
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
import conjur
import pytest

api = conjur.new_from_key('admin', 'secret')
resource = api.resource('food', 'bacon')
bob = api.user('bob')


def test_resource_id():
    assert resource.resourceid == api.config.account + ':food:bacon'


@patch.object(api, 'get')
def test_permitted_with_role(mock_get):
    mock_get.return_value = Mock(status_code=204)
    assert resource.permitted('fry', bob)

    mock_get.assert_called_with(
        'https://example.com/api/authz/conjur/roles/user/bob',
        params={'privilege': 'fry', 'check': 'true',
                'resource_id': 'conjur:food:bacon'},
        check_errors=False
    )


@patch.object(api, 'get')
def test_permitted_self_role(mock_get):
    mock_get.return_value = Mock(status_code=204)
    assert resource.permitted('fry')
    mock_get.assert_called_with(
        'https://example.com/api/authz/conjur/resources/food/bacon',  # noqa E501 (line too long)
        params={'privilege': 'fry', 'check': 'true'},
        check_errors=False
    )


@patch.object(api, 'get')
def test_permitted_fails_with_self_role(mock_get):
    mock_get.return_value = Mock(status_code=403)
    assert not resource.permitted('fry')


@patch.object(api, 'get')
def test_permitted_fails_with_role(mock_get):
    mock_get.return_value = Mock(status_code=403)
    assert not resource.permitted('fry', bob)


@patch.object(api, 'get')
def test_permitted_error_self_role(mock_get):
    mock_get.return_value = Mock(status_code=401)
    with pytest.raises(conjur.ConjurException):
        resource.permitted('fry')


@patch.object(api, 'get')
def test_permitted_error_with_role(mock_get):
    mock_get.return_value = Mock(status_code=401)
    with pytest.raises(conjur.ConjurException):
        resource.permitted('fry', bob)
