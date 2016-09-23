# Simulates host inventory-manager trying to add and remove a pet

import sys

import requests

sys.path.append('../..')
import conjur

PETSTORE_URL = 'http://localhost:8080'

conjur.config.url = 'http://localhost:3030'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')  # TODO: swap this with inventory_manager creds
key = api.role('host', 'inventory_manager').rotate_api_key()

api = conjur.new_from_key('host/inventory_manager', key)

response = requests.post(
    '{}/api/pets'.format(PETSTORE_URL),
    json={'name': 'Spot', 'type': 'Beagle'},
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())

print 'Removing pet'
response = requests.delete(
    '{}/api/pets/{}'.format(PETSTORE_URL, response.json()['id']),
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())