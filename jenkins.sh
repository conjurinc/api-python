#!/bin/bash -ex

function cleanup {
   docker rm -f $(cat conjur-cid)
   rm conjur-cid
}

if [ -z "$KEEP" ] ; then
    trap cleanup EXIT
fi

APPLIANCE_VERSION=4.8-stable


rm -rf artifacts

docker build -t api-python .

docker run -d \
  --cidfile=conjur-cid \
  -p 443:443 \
  -v ${PWD}/ci:/ci \
  --add-host=conjur:127.0.0.1 \
  registry.tld/conjur-appliance-cuke-master:$APPLIANCE_VERSION

docker exec $(cat conjur-cid) /opt/conjur/evoke/bin/wait_for_conjur


mkdir -p ${PWD}/certs

docker cp $(cat conjur-cid):/opt/conjur/etc/ssl/cuke-master.pem ${PWD}/certs

docker exec $(cat conjur-cid) /ci/setup.sh

docker run --rm -Pi \
  -v ${PWD}/certs:/certs \
  -v ${PWD}/artifacts:/artifacts \
  --link $(cat conjur-cid):conjur \
api-python sh <<COMMANDS
find . -name '*.pyc' -delete

export CONJUR_CERT_FILE=/certs/cuke-master.pem

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
