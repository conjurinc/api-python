
import conjur.config

config = conjur.config.Config()

def connect(login, api_key, cfg=config):
    import conjur.connection
    return conjur.connection.Connection(login, api_key, cfg)

