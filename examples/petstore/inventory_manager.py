# Simulates host inventory-manager trying to add and remove a pet

import sys
import json
import requests

sys.path.append('../..')
import conjur

PETSTORE_URL = 'http://app:8080'

conjur.config.url = 'http://possum'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')
key = api.role('host', 'inventory_manager').rotate_api_key()
api = conjur.new_from_key('host/inventory_manager', key)

response = requests.post(
    '{}/api/pets'.format(PETSTORE_URL),
    data=json.dumps({'name': 'Spot', 'type': 'Beagle'}),
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())

print 'Removing pet'
response = requests.delete(
    '{}/api/pets/{}'.format(PETSTORE_URL, response.json()['id']),
    headers={'Authorization': api.auth_header()}
)

print '{}: {}'.format(response.status_code, response.json())
