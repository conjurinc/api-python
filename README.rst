Conjur Python API Client
========================

A Python client for the Conjur API.

Installation
------------

The Conjur Python API requires Python 2.7. While we love Python 3,
Python 2.x is the priority because of its widespread use by DevOps tools
such as Salt and Ansible.

Install from `PyPI <https://pypi.python.org/pypi/Conjur>`__

::

    pip install conjur

**Note:** If you have the ``pandoc`` package installed you may need to
uninstall it for the above command to work. You can do so with
``pip uninstall pypandoc``.

API Documentation
-----------------

See the `API documentation <https://conjurinc.github.io/api-python>`__
for details of all classes and methods.

Usage
-----

Configuration
~~~~~~~~~~~~~

.. code:: python

    # The `config` member of the conjur.config module is a "global" Configuration
    # used by new API instances by default.
    from conjur.config import config

    # Set the conjur appliance url.  This can also be provided
    # by the CONJUR_APPLIANCE_URL environment variable.
    config.appliance_url = 'https://conjur.example.com/api'

    # Set the (PEM) certificate file. This is also configurable with the
    # CONJUR_CERT_FILE environment variable.
    config.cert_file = '/path/to/conjur-account.pem'

Creating and Using an API Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    import conjur

    # For God's sake, don't put passwords in your source code!
    password = 'super-secret'
    login = 'alice'

    # Create an API instance that can perform actions as the user 'alice'
    api = conjur.new_from_key(login, password)

    # Use the API to fetch the value of a variable

    secret = api.variable('my-secret').value()

    print("The secret is '{}'".format(secret))

``new_from_key`` accepts a Conjur username and an api\_key or password
(`see the Conjur developer
documentation <http://developer.conjur.net/reference/services/authentication/authenticate.html>`__
for details about the distinction). This is useful if your script is
authenticating as an particular Conjur identity rather than acting on
behalf of a user who has provided their token.

When created using this method, the API will attempt to authenticate the
first time a method requiring authorization is called. To force it to
authenticate immediately, you can use the ``authenticate()`` method. An
instance created with ``new_from_key`` will cache it's auth token
indefinitely. Since Conjur auth tokens expire after 8 minutes, you can
force an api instance to update its token by calling
``api.authenticate(cached=False)`` or by setting ``api.token = None``.

Other Ways to Create an API Instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If the host running your application has been assigned a Conjur identity
``new_from_netrc`` is the easiest way to create an API instance.

.. code:: python

    import conjur
    from conjur.config import config

    config.load('/etc/conjur.conf')
    api = conjur.new_from_netrc('/etc/conjur.identity', config=config)

If you have an existing authentication token, for example when handling
an HTTP request that contains an end user's token, use
``new_from_token`` to create your API instance.

.. code:: python

    import conjur
    # ... some web magic

    api = conjur.new_from_token(request.get_json()['user_token'])
    salesforce_apikey = api.variable('sales/salesforce/api_key')

YAML file
~~~~~~~~~

Conjurized hosts will have this file placed at ``/etc/conjur.conf``.

Running locally this will be your ``~/.conjurrc`` file.

.. code:: python

    from conjur.config import config

    config.load('/etc/conjur.conf')

Variables
~~~~~~~~~

You can create, fetch and update variables like so:

.. code:: python

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

If no ``id`` is given, a unique id will be generated. If a value is
provided, it will be used to set the variable's initial value. When
fetching a variable, you can pass a ``version`` keyword argument to
``value()`` to retrieve a specific version.

Users
~~~~~

Create a user ``alice`` with password ``super-secret``.

.. code:: python

    alice = api.create_user('alice', password='super-secret')

Create a user ``bob`` without a password, and save the API key. When
creating a Conjur user, the API is available in the response. However,
retrieving the user in the future **will not** return the API key.

.. code:: python

    bob = api.create_user('bob')
    bob_api_key = bob.api_key

    print("Created user 'bob' with api key '{}'".format(bob_api_key))

Fetch a user named 'otto', and check whether or not it was found:

.. code:: python

    if api.user('otto').exists():
      print("Otto exists!")
    else:
      print("Sorry, otto doesn't exist :-(")

Groups
~~~~~~

Create a group named ``developers`` and add an existing user ``alice``
to it.

.. code:: python

    devs = api.create_group('developers')

Development
-----------

Clone this project and run:

::

    pip install -r requirements.txt -r requirements_dev.txt

Run tests and linting with:

::

    ./jenkins.sh

PyPi
~~~~

To publish to PyPi, you will need to convert this document to
restructured text using pandoc:

::

    pandoc --from=markdown --to=rst --output=README.rst README.md

Furthermore, you will likely need to have the ``pypandoc`` package
installed for the markup to appear correctly on the PyPi site.
