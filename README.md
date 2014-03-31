Conjur Python API
=================

A Python client for the Conjur API.

##Installation

Clone or download the source, then run

```
python setup.py install
```

##Basic Usage

To create an `API` instance, use either `conjur.new_from_token(token)` or `conjur.new_from_key(login, api_key)`.

`conjur.new_from_token` accepts an existing authentication token, which is useful if, for example,
you are handling an HTTP request that contains an end user's token.

`conjur.new_from_key` accepts a Conjur username and an api_key or password (see the Conjur developer
documentation for details about the distinction).  This is useful if your script is authenticating
as an particular Conjur identity rather than acting on behalf of a user who has provided their token.
When created using this method, the api will attempt to authenticate the first time a method requiring
authorization is called.  To force it to authenticate immediately, you can use the `authenticate()` method.
An instance created with `new_from_key` will cache it's auth token indefinitely.  Since Conjur auth tokens
expire after 8 minutes, you can force an api instance to update its token by calling `authenticate(False)`,
or by setting `api.token = None`.

##Configuration

Conjur requires endpoint configuration, which can be provided via environment variables or a yaml configuration
file.  If you want to use a configuration file, you must load it at the begining of your script, like this:

```python
from conjur.config import config
config.load('/path/to/config/file.yaml')
```

Environment variables may also be used, and are named by capitalizing the corresponding config variable and
prefixing it with `'CONJUR_'`.  For example, the `appliance_url` variable can be configured with `CONJUR_APPLIANCE_URL`.

`API` instances can be created with a particular `conjur.config.Config`, which defaults to the globaly available value
`conjur.config.config`.  You may configure either programatically if config files or environment variables are not
appropriate for your use case.

When using appliance based Conjur, you only need to provide the `appliance_url` setting.  For hosted Conjur, you will
provide the `stack` and `account` values supplied by Conjur when your hosted system is created.  For development purposes,
you can also provide service specific urls, for example, `authn_url`.

##Variables API

Conjur stores encrypted secrets in `variables`.  A variable is versioned, so values are never actually overwritten, and
has a `mime_type` attribute that can be used to specify the `Content-Type` header when the variables value is returned, as
well as a `kind` attribute that can be used to indicate the type of content the variable contains (although it is ignored
by Conjur).  You can create a variable using the `api.create_variable(id=None, mime_type='text/plain', kind='secret', value=None)`
method.  All parameters are optional.  If no `id` is given, a unique id will be generated.  If value is provided, it will
be used to set the variable's initial value.

To retrieve a variable by id, use the `api.variable(id)` method.  Variable objects are also returned by the `create_variable` method.
A Variable object's value can be fetched using the `value(version=None)` method, which returns the latest version if no
version parameter is specified.  It's value can be updated (creating a new version) using the `add_value(value)` method.
