class ConjurException(Exception): pass

def _config(given):
    if given is None:
        import conjur.config
        return conjur.config.config
    return given

def new_from_netrc(netrc_file=None, config=None):
    """
    Create a Conjur API using an identity loaded from netrc.  This method
    uses the identity stored for the host `config.authn_url`.

    :param netrc_file: An alternative path to the netrc formatted file.  Defaults
        to ~/.netrc on unixy systems.
    :param config: A `conjur.config.Config` instance used to determine the host
        in the netrc file, and also passed to the `conjur.new_from_key` method to
        create the API instance using the identity.
    """
    import netrc
    config = _config(config)
    auth = netrc.netrc(netrc_file).authenticators(config.authn_url)
    if auth is None:
        raise ValueError("No authenticators found for authn_url '%s' in %s" % (
            config.authn_url,
            (netrc_file or '~/.netrc')
        ))
    login, _, api_key = auth
    return new_from_key(login, api_key, config)



def new_from_key(login, api_key, config=None):
    """
    Create a Conjur API that will authenticate on demand as the identity given
    by login and api_key.

    :param login: The login Conjur of the Conjur user or host to authenticate as.
    :param api_key: The Conjur api key *or* password to use when authenticating.
    :param config: The Config instance for the api.  If not given the global Config instance
        (`conjur.config.config`) will be used.
    """

    import conjur.api
    return conjur.api.API(credentials=(login, api_key), config=_config(config))


def new_from_token(token, config=None):
    """
    Create a Conjur API that will authenticate using the given signed Conjur token.

    This is usefull if you want to act on behalf of a the identity of an
    HTTP request containing a user's signed token.

    :param token: The json formatted, *not* base64'd, Conjur authentication Token.
    :param config: Config instance for the api.  If not given, the global Config instance
        (`conjur.config.config`) will be used.
    """
    import conjur.api
    return conjur.api.API(token=token, config=_config(config))


