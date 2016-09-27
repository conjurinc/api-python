#!/bin/bash -ex

docker build -t api-python .

docker tag -f api-python conjurinc/api-python
