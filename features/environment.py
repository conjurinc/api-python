import conjur
from conjur.config import config
import os

def admin_password():
    if 'CONJUR_ADMIN_PASSWORD' not in os.environ:
        if 'CONJUR_ADMIN_PASSWORD_FILE' in os.environ:
            with open(os.environ['CONJUR_ADMIN_PASSWORD_FILE']) as f:
                os.environ['CONJUR_ADMIN_PASSWORD'] = f.read()
    return os.environ['CONJUR_ADMIN_PASSWORD']

def api():
    config.stack = config.account = 'ci'
    return conjur.new_from_key('admin', admin_password())

def before_all(context):
    context.api = api()
