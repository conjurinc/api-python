# Conjur Python API Client

A Python client for the Conjur API.

## Installation

Install from [PyPI](https://pypi.python.org/pypi/Conjur)

```
pip install conjur
```

## Basic Usage

```python
import os
import conjur

api = conjur.new_from_key(login='danny', api_key=os.getenv('CONJUR_API_KEY'))
mongo_password = api.variable('service_a/mongodb_password').value()
```

`new_from_key` accepts a Conjur username and an api_key or password
([see the Conjur developer documentation](http://developer.conjur.net/reference/services/authentication/authenticate.html) for details about the distinction).  This is useful if your script is authenticating as an particular Conjur identity rather than acting on behalf of a user who has provided their token.

When created using this method, the API will attempt to authenticate the first time a method requiring
authorization is called.  To force it to authenticate immediately, you can use the `authenticate()` method.
An instance created with `new_from_key` will cache it's auth token indefinitely.
Since Conjur auth tokens expire after 8 minutes, you can force an api instance to update its token
by calling `api.authenticate(cached=False)` or by setting `api.token = None`.

## Advanced Usage

If the host running your application has been assigned a Conjur identity
`new_from_netrc` is the easiest way to create an API instance.

```python
import conjur
from conjur.config import config

config.load('/etc/conjur.conf')
api = conjur.new_from_netrc('/etc/conjur.identity', config=config)
```

---

If you have an existing authentication token, for example when handling
an HTTP request that contains an end user's token, use `new_from_token` to create your API instance.

```python
import conjur
# ... some web magic

api = conjur.new_from_token(request.get_json()['user_token'])
salesforce_apikey = api.variable('sales/salesforce/api_key')
```

##Configuration

Conjur requires endpoint configuration, which can be provided via environment variables or a YAML configuration file.

### Environment variables

Setting `CONJURRC` and `CONJUR_APPLIANCE_URL` variables will allow you to to connect.

Other available variables are named by capitalizing the corresponding config variable and
prefixing it with `'CONJUR_'`.  For example, the `appliance_url` variable can be configured with `CONJUR_APPLIANCE_URL`. See all variables [at the bottom here](conjur/config.py)

For development purposes you can provide service specific urls, for example, `CONJUR_AUTHN_URL`.

### YAML file

Conjurized hosts will have this file placed at `/etc/conjur.conf`.

Running locally this will be your `~/.conjurrc` file.

```python
from conjur.config import config

config.load('/etc/conjur.conf')
```

## Variables

You can create, fetch and update variables like so:

```python
import os
import conjur

api = conjur.new_from_key(login='danny', api_key=os.getenv('CONJUR_API_KEY'))

loggly_token = api.create_variable(
    id='monitoring/loggly.com/api-token',
    value='dEet7Hib1oSh9g'
)

gis_database_password = api.variable('gis/postgres/password')
print(gis_database_password.value())

gis_database_password.add_value('lij6det8eJ7pIx')
```

If no `id` is given, a unique id will be generated.  If a value is provided, it will
be used to set the variable's initial value. When fetching a variable, you can pass
`version` to `value()` to retrieve a specific version.

## Other Conjur resources

Layers, hosts, groups, users and pubkeys can be created/fetched/updated by other methods
on the [API class](conjur/api.py).

---

## Development

Clone this project and run:

```
pip install -r requirements.txt -r requirements_dev.txt
```

Run tests and linting with:

```
./jenkins.sh
```
