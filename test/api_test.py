import conjur
from mock import patch, Mock
import requests
import base64

@patch.object(requests, 'post')
def test_authenticate(mock_post):
    api = conjur.new_from_key("login", "api-key")
    api.config.authn_url = "https://example.com"
    mock_post.return_value = mock_response = Mock()
    mock_response.status_code = 200
    mock_response.text = "token token token"
    token = api.authenticate()
    assert token == "token token token"
    mock_post.assert_called_with("https://example.com/users/login/authenticate", "api-key")

@patch.object(requests, 'post')
def test_authenticate_with_cached_token(mock_post):
    api = conjur.new_from_token("token token")
    assert api.authenticate() == "token token"
    mock_post.assert_not_called()

def test_auth_header():
    api = conjur.new_from_token("the token")
    expected = 'Token token="%s"'%(base64.b64encode("the token"))
    assert api.auth_header() == expected

@patch.object(requests, 'post')
def test_request_with_post(mock_post):
    api = conjur.new_from_token("the token")
    mock_post.return_value = resp = Mock()
    assert api.request('post', 'https://example.com', data="foobar") == resp
    mock_post.assert_called_with('https://example.com', data="foobar", headers={"Authorization": api.auth_header()})