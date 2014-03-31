from setuptools import setup, find_packages

setup(
    name = "Conjur",
    version = "0.1.0",
    packages = find_packages(),
    install_requires = ['mock', 'requests', 'pyyaml'],
    package_data = {},
    author = "Jon Mason",
    author_email = "jon@conjur.net",
    description = "Python client for the Conjur API",
    license = "MIT"
)