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

import base64

from mock import patch, Mock
import requests

import conjur


@patch.object(requests, 'post')
def test_authenticate(mock_post):
    api = conjur.new_from_key("login", "api-key")
    api.config.authn_url = "https://example.com"
    mock_post.return_value = mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "token token token"
    token = api.authenticate()
    assert token == "token token token"
    mock_post.assert_called_with("https://example.com/users/login/authenticate",
                                 "api-key", verify=api.config.verify)


@patch.object(requests, 'post')
def test_authenticate_with_cached_token(mock_post):
    api = conjur.new_from_token("token token")
    assert api.authenticate() == "token token"
    mock_post.assert_not_called()


def test_auth_header():
    api = conjur.new_from_token("the token")
    expected = 'Token token="%s"' % (base64.b64encode("the token"))
    assert api.auth_header() == expected


@patch.object(requests, 'post')
def test_request_with_post(mock_post):
    api = conjur.new_from_token("the token")
    mock_post.return_value = resp = Mock()
    resp.status_code = 200
    assert api.request('post', 'https://example.com', data="foobar") == resp
    mock_post.assert_called_with('https://example.com', data="foobar",
                                 headers={"Authorization": api.auth_header()},
                                 verify=api.config.verify)
