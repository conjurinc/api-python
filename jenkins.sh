#!/bin/bash -ex

CONJUR_VERSION=${CONJUR_VERSION:-"latest"}
DOCKER_IMAGE=${DOCKER_IMAGE:-"conjurinc/possum:$CONJUR_VERSION"}
NOKILL=${NOKILL:-"1"}
PULL=${PULL:-"0"}
CMD_PREFIX=""

function finish {
  # Stop and remove the Conjur container if env var NOKILL != "1"
  if [ "$NOKILL" != "1" ]; then
      docker rm -f ${pg} || true
      docker rm -f ${cid} || true
  fi
}
trap finish EXIT

job=$JOB_NAME
if [ -z $job ]; then
       job=sandbox
fi

tag=api-python:$job

docker build -t api-python:$job .

rm -rf report
mkdir report

if [ "$PULL" == "1" ]; then
    docker pull $DOCKER_IMAGE
fi

if [ ! -f data_key ]; then
    echo "Generating data key"
    docker run --rm ${DOCKER_IMAGE} data-key generate > data_key
fi

export POSSUM_DATA_KEY="$(cat data_key)"

pg=$(docker run -d postgres:9.3)

# Launch and configure a Conjur container
cid=$(docker run -d \
    -e DATABASE_URL=postgresql://postgres@pg/postgres \
    -e POSSUM_DATA_KEY \
    -e POSSUM_ADMIN_PASSWORD=secret \
    -e CONJUR_PASSWORD_ALICE=secret \
    -v $PWD/features/policy:/run/possum/policy/ \
    --link ${pg}:pg \
    ${DOCKER_IMAGE} \
    server -a cucumber -f /run/possum/policy/conjur.yml)
>&2 echo "Container id:"
>&2 echo $cid

sleep 10

docker run --rm -Pi \
  -v ${PWD}:/app \
  --link $cid:possum.test \
  $tag sh <<COMMANDS
umask 000
set -x

find . -name '*.pyc' -delete

py.test --cov conjur --junitxml=pytest.xml --instafail

# Runs cukes with coverage
coverage run --source='conjur/' -a -m behave --junit \
 --junit-directory=/artifacts/ \
 --tags ~@wip
 
coverage xml -o './coverage.xml'
coverage html
# pylint -f parseable conjur tests | tee pylint.out

# Generate html documentation
PYTHONPATH=/app pdoc --html --html-dir docs --overwrite conjur

cp -r coverage.xml pytest.xml htmlcov docs /artifacts/.

COMMANDS
