import os
import sys

from setuptools import setup, find_packages

NAME = 'Conjur'
VERSION = '0.3.1'


# Publish Helper.
if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    package_data={},
    author='Jon Mason',
    author_email='jon@conjur.net',
    description='Python client for the Conjur API',
    long_description=open('README.md').read(),
    license='MIT',
    url='https://github.com/conjurinc/api-python',
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7'
    ]
)
