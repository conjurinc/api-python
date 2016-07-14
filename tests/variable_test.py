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
def test_create_variable(mock_post):
    mock_post.return_value = mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json = lambda: {'id': 'foobar'}  # No attribute support now
    api = conjur.new_from_token('token')
    v = api.create_variable(mime_type='mimey', kind='something')
    assert v.id == 'foobar'
    mock_post.assert_called_with(
        '%s/variables' % api.config.core_url,
        data={'mime_type': 'mimey', 'kind': 'something'},
        headers={'Authorization': api.auth_header()},
        verify=api.config.verify
    )


@patch.object(requests, 'get')
def test_get_variable_value(mock_get):
    mock_get.return_value = resp = Mock()
    resp.status_code = 200
    resp.text = 'teh value'
    api = conjur.new_from_token('token')
    v = api.variable('my-id')
    assert v.value() == 'teh value'
    mock_get.assert_called_with(
        '%s/variables/my-id/value' % api.config.core_url,
        headers={'Authorization': api.auth_header()},
        verify=api.config.verify
    )


@patch.object(requests, 'post')
def test_add_variable_value(mock_post):
    mock_post.return_value = resp = Mock()
    resp.status_code = 201
    api = conjur.new_from_token('token')
    v = api.variable('var')
    v.add_value('boo')
    mock_post.assert_called_with(
        '%s/variables/var/values' % api.config.core_url,
        headers={'Authorization': api.auth_header()},
        data={'value': 'boo'},
        verify=api.config.verify
    )
