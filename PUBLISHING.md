# How to Publish to pypi

Our login for [testpypi](https://testpypi.python.org/pypi) and [pypi](https://pypi.python.org/pypi) is stored in conjur at

```
pypi.python.org/username
pypi.python.org/password
```

Create a `~/.pypirc` file with this content:

```
[distutils]
index-servers =
    pypi-conjur
    pypitest-conjur

[pypi-conjur]
repository: https://pypi.python.org/pypi
username: {{your_username}}
password: {{your_password}}

[pypitest-conjur]
repository: https://testpypi.python.org/pypi
username: {{your_username}}
password: {{your_password}}
```

pandoc is a dependency to convert the README to ReST format, can be brew-installed on OSX.

Try out the package upload on testpypi first to make sure we're set. Otherwise we'll have to create a new release.

```
python setup.py sdist upload -r pypitest-conjur
```

If the package doesn't look right delete it from pypitest and try again.

Once you're happy with it, upload it to live pypi:

```
python setup.py sdist upload -r pypi-conjur
```

Make sure to pip install the new package to ensure all is okay!

