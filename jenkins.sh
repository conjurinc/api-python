#!/bin/bash

DOCDIR=${PWD}/pydocs

if [ -d ${DOCDIR} ]; then
    rm -rf ${DOCDIR}
fi
mkdir -p ${DOCDIR}

# Install necessary packages

pip install -r requirements.txt
pip install -r requirements_dev.txt
for file in conjur/*.py ; do
    module=` echo "$file" | sed -e 's/\//./' -e 's/.py//g' -e 's/\.__init__//' ` ;
    pydoc -w ${module} ;
    mv "$module".html ${DOCDIR}
done
cp -v ${DOCDIR}/conjur.html ${DOCDIR}/index.html

pylint -f parseable conjur tests | tee pylint.out
py.test --cov conjur --cov-report html --cov-report xml --junitxml=pytest.xml --instafail
