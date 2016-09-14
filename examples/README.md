# Python API examples

```sh-session
host$ cd possum/dev
host$ ./start.sh
possum$ possum db migrate
possum$ possum policy load example run/policy.yml
possum$ possum server -p 80
host$ docker build -t python-api:sandbox
host$ docker run --rm -it --name python-server --link possumdev_possum_1:possum.example api-python:sandbox bash
python-server$ cd examples; python authorization.py
host$ docker run --rm -it --name python-examples --link possumdev_possum_1:possum.example --link python-server:service.example api-python:sandbox bash
python-examples$ cd examples
python-examples$ export `cat env`
python-examples$ python directory.py
python-examples$ python secrets.py
python-examples$ python authorization_client.py
```

## directory.py

Logs in, lists groups and their members, then users and their public keys.

## secrets.py

Logs in, sets secrets on all resources with kind 'variable' and id like
'*password*' to a random value, then lists all the secrets.

## authorization.py

Starts a web server authorizing with possum resource.

## authorization_client.py

Client for the above webservice.
