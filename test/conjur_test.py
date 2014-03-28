
import conjur
from conjur.config import Config, config

def test_new_from_key():
    api = conjur.new_from_key("login", "secret")
    assert api.token is None
    assert api.api_key == "secret"
    assert api.login == "login"
    assert api.config == config

def test_new_from_token():
    api = conjur.new_from_token("a token")
    assert api.token == "a token"
    assert api.api_key == None
    assert api.login == None
    assert api.config == config

def test_new_with_config():
    cfg = Config()
    api = conjur.new_from_key("login", "secret",cfg=cfg)
    assert cfg == api.config