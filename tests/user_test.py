from mock import patch, Mock
import conjur
import requests

@patch.object(requests, 'post')
def test_create_user(mock_post):
    api = conjur.new_from_token('token')
    mock_post.return_value = resp = Mock()
    resp.status_code = 200
    resp.json = {'login': 'foo', 'api_key': 'apikey'}

    user_no_pass = api.create_user('foo')
    assert user_no_pass.login == 'foo'
    assert user_no_pass.api_key == 'apikey'
    mock_post.assert_called_with(
        '{0}/users'.format(api.config.core_url),
        data={'login': 'foo'},
        headers={'Authorization': api.auth_header()}
    )

    api.create_user('foo', 'bar')
    mock_post.assert_called_with(
        '{0}/users'.format(api.config.core_url),
        data={'login': 'foo', 'password': 'bar'},
        headers={'Authorization': api.auth_header()}
    )


@patch.object(requests, 'get')
def test_user(mock_get):
    api = conjur.new_from_token('token')
    mock_get.return_value = Mock(status_code=200, json={'foo': 'bar'})
    user = api.user('login')
    assert user.foo == 'bar'
    mock_get.assert_called_with(
        '{0}/users/login'.format(api.config.core_url),
        headers={'Authorization': api.auth_header()}
    )



