# Pet Store - Using Possum with Python's Flask web framework

This example project illustrates how to:

* Fetch a secret (database password) using the [Conjur Python API client](https://pypi.python.org/pypi/Conjur)
* Authorize traffic from other clients that want to call this web service [TODO]

The scenario for this example:

> A local pet store wants to be able to display all pets that they have available to the general public.
Pet info is fetched from a PostgreSQL database and displayed on a website page. The pet store wants to be able
to add and remove pets from their inventory securely. Only their employees should be able to add and remove pets.
The pet store also has an inventory manager, another web service that can be used to add or remove pets as needed. 
When the `pet store` service receives a request from `employees` or the `inventory manager`, it authenticates and authorizes the
request with Possum.

![Pet store diagram](http://i.imgur.com/HLSO2VB.png)

## Requirements

* Docker and docker-compose
* Python 2.7+ and pip

## Example

First, set up your environment.

```
./start.sh
```

Possum has now loaded [policy.yml](policy.yml) and is running and listening on
local port `3030`. For this example, the `admin` user's password is
`secret`.

The `petstore` database has also been created, with user `petstore`.
The database user's password has been loaded into the `dbpassword` variable
in Possum with [load_secrets.py](load_secrets.py).

Now that Possum is running, run the Flask app from this directory:

```
pip install -r requirements.txt
python app.py
```

The Flask web app is now listening on port `8080`.
Open [localhost:8080](http://localhost:8080) in your browser.
You will notice that there are no pets displayed.

Pets can be added and removed by using the pet store's API.

* add pet: `POST` `/api/pets`, JSON body with `name` and `type` fields
* remove pet: `DELETE` `/api/pets/<id>` with pet ID

TODO: add section on traffic auth for users and hosts


To stop the possum server run:

```
./stop.sh
```
