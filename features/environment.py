import conjur
from conjur.config import config
import os
import random


def admin_password():
    if 'CONJUR_ADMIN_PASSWORD' not in os.environ:
        if 'CONJUR_ADMIN_PASSWORD_FILE' in os.environ:
            with open(os.environ['CONJUR_ADMIN_PASSWORD_FILE']) as f:
                os.environ['CONJUR_ADMIN_PASSWORD'] = f.read()
    return os.environ['CONJUR_ADMIN_PASSWORD']


def appliance_url():
    return os.environ.get('CONJUR_APPLIANCE_URL', None)


def api():
    config.stack = config.account = 'ci'
    url = appliance_url()
    if url is not None:
        config.appliance_url = url
    return conjur.new_from_key('admin', admin_password())


def random_string(prefix, size=8):
    return "%s-%030x" % (prefix, random.randrange(16 ** size))


def before_all(context):
    context.api = api()
    context.random_string = random_string
