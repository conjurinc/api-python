# Simulates an employee trying to add and remove a pet

import sys

import requests

sys.path.append('../..')
import conjur

PETSTORE_URL = 'http://localhost:8080'

conjur.config.url = 'http://localhost:3030'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')
key = api.role('user', 'dan').rotate_api_key()

api = conjur.new_from_key('dan', key)


print 'Adding pet'
response = requests.post(
    '{}/api/pets'.format(PETSTORE_URL),
    json={'name': 'Clarence', 'type': 'Fur Seal'},
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())

print 'Removing pet'
response = requests.delete(
    '{}/api/pets/{}'.format(PETSTORE_URL, response.json()['id']),
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())
