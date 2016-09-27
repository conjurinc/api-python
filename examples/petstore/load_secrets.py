import sys

sys.path.insert(0, '../..')

import conjur

conjur.config.url = 'http://possum'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')

# Set the database password to a known value
api.resource('variable', 'dbpassword').add_secret('w^kftUagHmF2Ahph')
