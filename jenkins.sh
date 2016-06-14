#!/bin/bash

rm -rf artifacts
docker build -t api-python .

docker run -Pi -v ${PWD}/artifacts:/artifacts \
api-python sh <<COMMANDS
find . -name '*.pyc' -delete
py.test --cov conjur --cov-report html --cov-report xml --junitxml=pytest.xml --instafail
pylint -f parseable conjur tests | tee pylint.out

cp -R coverage.xml pytest.xml htmlcov pylint.out /artifacts/.
COMMANDS