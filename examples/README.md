# Python API examples

These examples show how to use the Python API.

A docker-compose environment is included for ease of use. Note it needs
[conjurinc/possum-example](https://github.com/conjurinc/possum-example)
and [conjurinc/possum](https://github.com/conjurinc/possum) images available
in docker repository.

To start, use `./start.sh`:

```sh-session
$ ./start.sh
+ docker-compose build
pg uses an image, skipping
example uses an image, skipping
possum uses an image, skipping
Building api
[...]
+ POSSUM_DATA_KEY=40jLjbr3O2n1Z//MgU6G3SzFVjuO/fv6zQkeyzu1sxU=
+ docker-compose up -d pg possum
Creating examples_example_1
Creating examples_pg_1
Creating examples_possum_1
+ docker-compose run --rm api
Starting examples_example_1
root@0d85ff261d5d:/app#
```

## directory.py

Logs in, lists groups and their members, then users and their public keys:

```sh-session
# python examples/directory.py
=========================================================================
('Base url :', 'http://possum.example')
('Account  :', 'example')
('Login    :', 'admin')
('Password :', 'secret')
=========================================================================
Group example:group:security_admin; members:
 - example:user:admin
Group example:group:field-admin; members:
 - example:group:security_admin
 - example:user:kyle.wheeler
 - example:user:marin.dubois
[...]
User example:user:kyle.wheeler
User example:user:marin.dubois
User example:user:carol.rodriquez
[...]
```

## secrets.py

Logs in, sets secrets on all resources with kind 'variable' and id like
'*password*' to a random value, then lists all the secrets.

```sh-session
# python examples/secrets.py
=========================================================================
('Base url :', 'http://possum.example')
('Account  :', 'example')
('Login    :', 'admin')
('Password :', 'secret')
=========================================================================
Setting example:variable:prod/analytics/v1/redshift/master_user_password = jdPa8)sOW#XM
Setting example:variable:prod/frontend/v1/mongo/password = ,xV:An%3cmSE
Setting example:variable:prod/user-database/v1/postgres/master_user_password = (Y`{5(y3uRUK
[...]
example:variable:prod/user-database/v1/postgres/master_user_name = None
example:variable:prod/user-database/v1/postgres/master_user_password = (Y`{5(y3uRUK
example:variable:prod/user-database/v1/postgres/database_name = None
example:variable:prod/user-database/v1/postgres/database_url = None
```

## authorization.py and authorization_client.py

A web server authorizing with possum resource:

```sh-session
# python examples/authorization.py &
[1] 14
Serving on port 8000...
# python examples/authorization_client.py
127.0.0.1 - - [15/Sep/2016 14:19:13] "GET / HTTP/1.1" 200 24
200 OK
You are authorized!!!!!
```
