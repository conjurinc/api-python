
class ConjurException(Exception): pass


def new_from_key(login, api_key, cfg=None):
    import conjur.api
    if not cfg:
        from conjur.config import config
        cfg = config
    return conjur.api.API(credentials=(login, api_key), config=cfg)


def new_from_token(token, cfg=None):
    import conjur.api
    if not cfg:
        from conjur.config import config
        cfg = config
    return conjur.api.API(token=token, config=cfg)


