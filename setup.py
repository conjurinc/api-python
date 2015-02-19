import os
import sys

from setuptools import setup, find_packages

NAME = 'Conjur'
VERSION = '0.3.2'

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    install_requires=open('requirements.txt').readlines(),
    package_data={},
    author='Jon Mason',
    author_email='jon@conjur.net',
    description='Python client for the Conjur API',
    long_description=long_description,
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
