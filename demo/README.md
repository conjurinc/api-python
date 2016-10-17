# Possum Demo

## Description

See [https://conjurinc.github.io/possum/demo.html](https://conjurinc.github.io/possum/demo.html) for a detailed walkthrough.

The policies used in the demo are available in this directory.

## Running

To run a Possum server and command-line client in Docker containers, simply run `./start.sh`:

```sh-session
$ ./start.sh
pg uses an image, skipping
possum uses an image, skipping
Step 1 : FROM python:2.7-slim
 ---> 4947dfe5e830
...
Creating demo_pg_1
Creating demo_possum_1
root@5c2b6208380e:/app# possum -h
usage: possum [-h]
              {login,whoami,authenticate,rotate_api_key,list,show,policy:load,store,fetch}
              ...

Possum command-line interface.
```
