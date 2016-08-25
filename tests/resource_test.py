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
bob = api.role('user', 'bob')


def test_resource_id():
    assert resource.resourceid == api.config.account + ':food:bacon'


@patch.object(api, 'get')
def test_permitted_with_role(mock_get):
    mock_get.return_value = Mock(status_code=204)
    assert resource.permitted('fry', bob)

    mock_get.assert_called_with(
        'http://possum.test/roles/conjur/user/bob',
        params={'privilege': 'fry', 'check': 'true',
                'resource': 'conjur:food:bacon'},
        check_errors=False
    )


def test_fq_resource():
    res = api.resource_qualified('foo:bar:baz')
    assert res.url() == 'http://possum.test/resources/foo/bar/baz'

def test_role_of_resource():
    res = api.resource_qualified('foo:bar:baz')
    assert res.role().roleid == 'foo:bar:baz'

@patch.object(api, 'get')
def test_permitted_self_role(mock_get):
    mock_get.return_value = Mock(status_code=204)
    assert resource.permitted('fry')
    mock_get.assert_called_with(
        'http://possum.test/resources/conjur/food/bacon',
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

@patch.object(api, 'get')
def test_get_secret_value(mock_get):
    mock_get.return_value = resp = Mock()
    resp.status_code = 200
    resp.text = 'teh value'
    assert resource.secret() == 'teh value'
    mock_get.assert_called_with(
        '%s/secrets/conjur/food/bacon' % api.config.url
    )

@patch.object(api, 'post')
def test_add_secret_value(mock_post):
    mock_post.return_value = resp = Mock()
    resp.status_code = 201
    resource.add_secret('boo')
    mock_post.assert_called_with(
        '%s/secrets/conjur/food/bacon' % api.config.url,
        data='boo',
    )


@patch.object(api, 'get')
def test_resource_listing(mock_get):
    resources = ['conjur:foo:bar', 'conjur:baz:bar']
    mock_get.return_value = resp = Mock(
        json=lambda: [{"id": r} for r in resources],
        status_code=200
    )
    resources_list = api.resources()
    assert set(r.resourceid for r in resources_list) == set(resources)
    mock_get.assert_called_with('http://possum.test/resources/conjur')


@patch.object(api, 'get')
def test_resource_listing_filtered(mock_get):
    resources = ['conjur:foo:bar']
    mock_get.return_value = resp = Mock(
        json=lambda: [{"id": r} for r in resources],
        status_code=200
    )
    resources_list = api.resources(kind='foo')
    assert set(r.resourceid for r in resources_list) == set(resources)
    mock_get.assert_called_with('http://possum.test/resources/conjur/foo')
