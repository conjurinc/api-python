PYENV_HOME=$WORKSPACE/.pyenv/
DOCDIR=$WORKSPACE/pydocs
# Delete previously built virtualenv
if [ -d $PYENV_HOME ]; then
    rm -rf $PYENV_HOME
fi
if [ -d $DOCDIR ]; then
    rm -rf $DOCDIR
fi
mkdir -p $DOCDIR

# Create virtualenv and install necessary packages
pip install virtualenv
virtualenv --no-site-packages $PYENV_HOME
. $PYENV_HOME/bin/activate
pip install --quiet nosexcover
pip install --quiet pylint
pip install --quiet $WORKSPACE/
for file in conjur/*.py ; do 
    module=` echo "$file" | sed -e 's/\//./' -e 's/.py//g' -e 's/\.__init__//' ` ;
    pydoc -w $module ;  
    mv "$module".html $DOCDIR
done
cp -v $DOCDIR/conjur.html $DOCDIR/index.html

pylint -f parseable conjur/ | tee pylint.out
nosetests --with-xcoverage --with-xunit --cover-package=conjur --cover-erase
