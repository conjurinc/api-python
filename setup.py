from setuptools import setup, find_packages

setup(
    name='Conjur',
    version='0.3.1',
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    package_data={},
    author='Jon Mason',
    author_email='jon@conjur.net',
    description='Python client for the Conjur API',
    license='MIT'
)
