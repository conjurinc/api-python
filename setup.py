from setuptools import setup, find_packages

setup(
    name = "Conjur",
    version = "0.2.2",
    packages = find_packages(),
    install_requires = ['mock', 'requests >= 2.2.1', 'pyyaml', 'behave'],
    package_data = {},
    author = "Jon Mason",
    author_email = "jon@conjur.net",
    description = "Python client for the Conjur API",
    license = "MIT"
)
