import conjur
from mock import patch, Mock
import requests

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
