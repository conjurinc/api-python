import random
import string

import conjur


def random_value():
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(20))

conjur.config.url = 'http://localhost:3030'
conjur.config.account = 'example'

api = conjur.new_from_password('admin', 'secret')


# Set random values for secrets
api.resource('variable', 'dbpassword').add_secret('w^kftUagHmF2Ahph')
