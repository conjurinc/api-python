# Example of using Possum with Flask

Example project showing how to use the [Conjur API client](https://pypi.python.org/pypi/Conjur) to
fetch secrets from Possum and use them in a Flask web application.

## Requirements

* Docker and docker-compose
* Python 2.7+ and pip

## Example

First, launch a local Possum instance:

```
./start.sh
```

Possum has now loaded [policy.yml](policy.yml) and is running and listening on
local port `3030`. For this example, the `admin` user's password is
`secret`.

Now that Possum is running, run the Flask app from this directory:

```
pip install -r requirements.txt
python app.py
```

The Flask web app is now listening on port `8080`.
Open [localhost:8080](http://localhost:8080) in your browser.
Notice that the secrets have no value yet.

![secrets with no values](https://i.imgur.com/5blnU8O.png)

Load new secrets with:

```
python load_secrets.py
```

Reload the page at `localhost:8080` to see that the secret values
have now been fetched and are displayed in the browser.

![secrets with values](https://i.imgur.com/WRrS8Ih.png)

Secrets have been fetched from Possum and passed through to the Flask template.

To stop the possum server run:

```
./stop.sh
```
