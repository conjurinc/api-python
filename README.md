# Conjur Python2 API Client

A Python2 client for the Conjur API.

**If you are looking for Python3 API client, please go to our new project page at https://github.com/cyberark/conjur-api-python3.**

**IMPORTANT: THIS API CLIENT IS NOT CURRENTLY ACTIVELY BEING SUPPORTED**

## Installation

This Conjur Python2 API requires Python 2.7.  

Install from [PyPI](https://pypi.python.org/pypi/Conjur)

```
pip install conjur
```

**Note:** If you have the `pandoc` package installed you may need to uninstall it for the above command to work.  You
can do so with `pip uninstall pypandoc`.

## API Documentation

See the [API documentation](https://conjurinc.github.io/api-python) for details
of all classes and methods.


## Usage

### Configuration

```python
# The `config` member of the conjur.config module is a "global" Configuration
# used by new API instances by default.
from conjur.config import config

# Set the conjur appliance url.  This can also be provided
# by the CONJUR_APPLIANCE_URL environment variable.
config.appliance_url = 'https://conjur.example.com/api'

# Set the (PEM) certificate file. This is also configurable with the
# CONJUR_CERT_FILE environment variable.
config.cert_file = '/path/to/conjur-account.pem'
```

### Creating and Using an API Instance

```python
import conjur

# For God's sake, don't put passwords in your source code!
password = 'super-secret'
login = 'alice'

# Create an API instance that can perform actions as the user 'alice'
api = conjur.new_from_key(login, password)

# Use the API to fetch the value of a variable

secret = api.variable('my-secret').value()

print("The secret is '{}'".format(secret))

```

`new_from_key` accepts a Conjur username and an api_key or password
([see the Conjur developer documentation](http://developer.conjur.net/reference/services/authentication/authenticate.html) for details about the distinction).  This is useful if your script is authenticating as an particular Conjur identity rather than acting on behalf of a user who has provided their token.

When created using this method, the API will attempt to authenticate the first time a method requiring
authorization is called.  To force it to authenticate immediately, you can use the `authenticate()` method.
An instance created with `new_from_key` will cache it's auth token indefinitely.
Since Conjur auth tokens expire after 8 minutes, you can force an api instance to update its token
by calling `api.authenticate(cached=False)` or by setting `api.token = None`.



### Other Ways to Create an API Instance

If the host running your application has been assigned a Conjur identity
`new_from_netrc` is the easiest way to create an API instance.

```python
import conjur
from conjur.config import config

config.load('/etc/conjur.conf')
api = conjur.new_from_netrc('/etc/conjur.identity', config=config)
```


If you have an existing authentication token, for example when handling
an HTTP request that contains an end user's token, use `new_from_token` to create your API instance.

```python
import conjur
# ... some web magic

api = conjur.new_from_token(request.get_json()['user_token'])
salesforce_apikey = api.variable('sales/salesforce/api_key')
```

### YAML file

Conjurized hosts will have this file placed at `/etc/conjur.conf`.

Running locally this will be your `~/.conjurrc` file.

```python
from conjur.config import config

config.load('/etc/conjur.conf')
```

### Variables

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
a `version` keyword argument to `value()` to retrieve a specific version.


### Users

Create a user `alice` with password `super-secret`.

```python
alice = api.create_user('alice', password='super-secret')
```

Create a user `bob` without a password, and save the API key.  When creating
a Conjur user, the API is available in the response.  However, retrieving the
user in the future **will not** return the API key.

```python
bob = api.create_user('bob')
bob_api_key = bob.api_key

print("Created user 'bob' with api key '{}'".format(bob_api_key))
```

Fetch a user named 'otto', and check whether or not it was found:

```python
if api.user('otto').exists():
  print("Otto exists!")
else:
  print("Sorry, otto doesn't exist :-(")
```


### Groups

Create a group named `developers` and add an existing user `alice` to it.

```python
devs = api.create_group('developers')

```



## Development

Clone this project and run:

```
pip install -r requirements.txt -r requirements_dev.txt
```

Run tests and linting with:

```
./jenkins.sh
```

### PyPi

To publish to PyPi, you will need to convert this document to restructured
text using pandoc: 

```
pandoc --from=markdown --to=rst --output=README.rst README.md
```

Furthermore, you will likely need to have the `pypandoc` package installed
for the markup to appear correctly on the PyPi site.  

## License

Copyright 2016-2017 CyberArk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this software except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
