import conjur
from mock import patch, Mock
import requests

@patch.object(requests, 'post')
def test_create_variable(mock_post):
    mock_post.return_value = mock_response = Mock()
    mock_response.status_code = 201
    mock_response.json = {'id':'foobar'} # No attribute support now
    api = conjur.new_from_token('token')
    v = api.create_variable(mime_type='mimey', kind='something')
    assert v.id == 'foobar'
    mock_post.assert_called_with(
        '%s/variables'%api.config.core_url,
        data={'mime_type': 'mimey', 'kind': 'something'},
        headers={'Authorization': api.auth_header()}
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
        '%s/variables/my-id/value'%api.config.core_url,
        headers={ 'Authorization': api.auth_header() }
    )

@patch.object(requests, 'post')
def test_add_variable_value(mock_post):
    mock_post.return_value = resp = Mock()
    resp.status_code = 201
    api = conjur.new_from_token('token')
    v = api.variable('var')
    v.add_value('boo')
    mock_post.assert_called_with(
        '%s/variables/var/values'%api.config.core_url,
        headers={'Authorization': api.auth_header()},
        data={'value': 'boo'}
    )
