import conjur
from conjur.config import config
import os
import random


def admin_password():
    if 'CONJUR_ADMIN_PASSWORD' not in os.environ:
        if 'CONJUR_ADMIN_PASSWORD_FILE' in os.environ:
            with open(os.environ['CONJUR_ADMIN_PASSWORD_FILE']) as f:
                os.environ['CONJUR_ADMIN_PASSWORD'] = f.read()
    try:
        return os.environ['CONJUR_ADMIN_PASSWORD']
    except KeyError:
        raise Exception("You need to set CONJUR_ADMIN_PASSWORD or " +
                        "CONJUR_ADMIN_PASSWORD_FILE before running features")


def conjur_env(name):
    return os.environ.get("CONJUR_%s" % (name.upper(), ), None)


def api():
    config.stack = config.account = 'ci'
    appliance_url = conjur_env('appliance_url')
    if appliance_url is not None:
        config.appliance_url = appliance_url
        cert_file = conjur_env('cert_file')
        if cert_file is not None:
            config.cert_file = cert_file
    return conjur.new_from_key('admin', admin_password())


def random_string(prefix, size=8):
    return "%s-%030x" % (prefix, random.randrange(16 ** size))


def before_all(context):
    context.api = api()
    context.random_string = random_string
