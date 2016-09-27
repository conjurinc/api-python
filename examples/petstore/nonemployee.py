# Simulates Kate, a non-employee trying to add a pet to the pet store

import requests
import json

PETSTORE_URL = 'http://app:8080'

print 'Adding pet'
response = requests.post(
    '{}/api/pets'.format(PETSTORE_URL),
    data=json.dumps({'name': 'Johnny', 'type': 'Gibbon'})
)

print '{}: {}'.format(response.status_code, response.json())
