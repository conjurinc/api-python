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
from mock import patch, Mock, call
import conjur

api = conjur.new_from_key('fakeid', 'fakepass')


@patch.object(api, 'get')
def test_public_keys(mock_get):
    response = "a b key1\na b key2"
    mock_get.return_value = Mock(text=response)
    assert api.public_keys('foo bar') == response
    mock_get.assert_called_with(
        '{0}/foo%20bar'.format(api.config.pubkeys_url)
    )


@patch.object(api, 'get')
def test_public_key(mock_get):
    mock_get.return_value = Mock(text="a b c")
    assert api.public_key('foo bar', 'keyname') == 'a b c'
    mock_get.assert_called_with(
        '{0}/foo%20bar/keyname'.format(api.config.pubkeys_url))


@patch.object(api, 'get')
def test_public_key_names(mock_get):
    response = "a b key1\na b key2"
    mock_get.return_value = Mock(text=response)
    assert list(api.public_key_names('foo bar')) == ['key1', 'key2']
    mock_get.assert_called_with(
        '{0}/foo%20bar'.format(api.config.pubkeys_url)
    )


@patch.object(api, 'post')
def test_add_public_key(mock_post):
    api.add_public_key('foo', 'a b c')
    mock_post.assert_called_with(api.config.pubkeys_url + '/foo', data='a b c')


@patch.object(api, 'delete')
def test_remove_public_key(mock_del):
    api.remove_public_key('foo', 'bar')
    mock_del.assert_called_with(api.config.pubkeys_url + '/foo/bar')


@patch.object(api, 'delete')
@patch.object(api, 'get')
def test_remove_public_keys(mock_get, mock_del):
    mock_get.return_value = Mock(text="a b key1\na b key2")
    api.remove_public_keys('foo')
    mock_del.assert_has_calls([
        call(api.config.pubkeys_url + '/foo/key1'),
        call(api.config.pubkeys_url + '/foo/key2')
        ])
