# Pet Store - Using Possum with Python's Flask web framework

This example project illustrates how to:

* Fetch a secret (database password) using the [Conjur Python API client](https://pypi.python.org/pypi/Conjur)
* Authorize traffic from other clients that want to call this web service

The scenario for this example:

> A local pet store wants to be able to display all pets that they have available to the general public.
Pet info is fetched from a PostgreSQL database and displayed on a website page. The pet store wants to be able
to add and remove pets from their inventory securely. Only their employees should be able to add pets.
The pet store also has an inventory manager, another web service that can be used to add or remove pets as needed. 
When the `pet store` service receives a request from `employees` or the `inventory manager`, it authenticates and authorizes the
request with Possum.

![Pet store diagram](http://i.imgur.com/HLSO2VB.png)

## Requirements

* Docker and docker-compose

## Example

First, set up your environment.

```
./start.sh
```

Possum has now loaded [policy.yml](policy.yml) and is running and listening in the `possum` container. For this example, the `admin` user's password is
`secret`.

The `petstore` database has also been created, with user `petstore`.
The database user's password has been loaded into the `dbpassword` variable
in Possum with [load_secrets.py](load_secrets.py).

Also, there is a Flask app running in the `app` container and listening on the host port `8080`. Open [localhost:8080](http://localhost:8080) in your browser.
You will notice that there are no pets displayed.

## Policy

[policy.yml](policy.yml) is loaded when Possum starts up. The policy defines:

* variable `dbpassword` - Variable resource holds, the `petstore` database password
* host `petstore` - Host role for the `petstore` app
* host `inventory_manager` - Host role for the `inventory_manager` app
* group `employees` - Group role with three users

The host `petstore` is granted `execute` (read) access to the `dbpassword` variable. `petstore` fetches this password from Possum when starting up.
`inventory_manager` is granted `add_pet` and `remove_pet` privileges on the`petstore` host. Members of group `employees` are granted `add_pet` permission on the `petstore` host. Removing pets is a more privileged operation than adding them.

Pets can be added and removed by using the pet store's API.

* **add pet** `POST` `/api/pets`, JSON body with `name` and `type` fields
* **remove pet** `DELETE` `/api/pets/<id>` with pet id

The add and remove views are protected with the `validate_privilege` decorator
in [app.py](app.py). A user or machine must pass an `Authorization` header
when calling the `petstore` host. `petstore` consults Possum to ensure
that the caller has the required privilege on the `petstore` host. 
If so, the request proceeds. If not, an error message is returned.

## Demo

Simulate calling the `petstore` host as different identities:

```sh-session
# non-employee
$ python nonemployee.py
Adding pet
401: {u'msg': u'Authorization header missing', u'ok': False}

# employee
$ python employee.py
Adding pet
201: {u'ok': True, u'id': 7}
Removing pet
403: {u'msg': u'Not authorized', u'ok': False}

# inventory_manager
$ python inventory_manager.py
Adding pet
201: {u'ok': True, u'id': 8}
Removing pet
200: {u'ok': True, u'id': u'8'}
```

As expected, non-employees cannot update the pet inventory at all. Users in group
`employees` can add pets, but not remove them. Finally, the `inventory_manager` service
can add and remove pets.

To stop the possum local environment run:

```
./stop.sh
```

## Conclusion

In this example, we simulated a pet store system where anyone can view the
pets available but only trusted people and machines are allowed to manage
pet inventory. Different tiers of access are easily defined and implemented 
using Possum's YAML policy.
