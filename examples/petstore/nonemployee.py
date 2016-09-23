# Simulates Kate, a non-employee trying to add a pet to the pet store

import requests

PETSTORE_URL = 'http://localhost:8080'

print 'Adding pet'
response = requests.post(
    '{}/api/pets'.format(PETSTORE_URL),
    json={'name': 'Johnny', 'type': 'Gibbon'}
)

print '{}: {}'.format(response.status_code, response.json())
