#!/bin/bash -ex

function cleanup {
   docker rm -f $(cat conjur-cid)
   rm conjur-cid
}
trap cleanup EXIT

APPLIANCE_VERSION=4.8-stable


rm -rf artifacts

docker build -t api-python .

docker run -d \
  --cidfile=conjur-cid \
  -p 443:443 \
  --add-host=conjur:127.0.0.1 \
  registry.tld/conjur-appliance-cuke-master:$APPLIANCE_VERSION

docker exec $(cat conjur-cid) /opt/conjur/evoke/bin/wait_for_conjur


mkdir -p ${PWD}/certs

docker cp $(cat conjur-cid):/opt/conjur/etc/ssl/cuke-master.pem ${PWD}/certs

docker run --rm -Pi \
  -v ${PWD}/certs:/certs \
  -v ${PWD}/artifacts:/artifacts \
  --link $(cat conjur-cid):conjur \
api-python sh <<COMMANDS
find . -name '*.pyc' -delete

export CONJUR_CERT_FILE=/certs/cuke-master.pem

py.test --cov conjur --cov-report html --cov-report xml --junitxml=pytest.xml --instafail
pylint -f parseable conjur tests | tee pylint.out
behave

cp coverage.xml pytest.xml htmlcov pylint.out /artifacts/.


COMMANDS
