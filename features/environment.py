import conjur
from conjur.config import Config
import os
import random
import logging

'''
Expected envinronment:

Conjur Appliance is running at 'https://conjur/api' OR in CONJUR_APPLIANCE_URL

Conjur cert is stored in '/etc/ssl/conjur-cucumber.pem' OR in CONJUR_CERT_FILE

Credentials are admin:secret.

'''


def dump_config(cfg):
    print("*" * 20 + " CONJUR CONFIGURATION " + "*" * 20)
    for key in ('account', 'appliance_url', 'cert_file'):
        print("  {} = {}".format(key, cfg.get(key)))


def configure_logging():
    logging.basicConfig(level=logging.DEBUG)


def conjur_env(name, default=None):
    print("conjur_env {} {}".format(name, default))
    val = os.environ.get("CONJUR_{}".format(name.upper()), default)
    print("got {}".format(val))
    return val


def api():
    config = Config(
        account=conjur_env('account', 'cucumber'),
        url=conjur_env('url', 'http://possum.test'),
        cert_file=conjur_env('cert_file', '/opt/conjur/etc/ssl/conjur.pem')
    )

    print("config={}".format(repr(config._config)))

    login = 'alice'
    password = 'secret'

    return conjur.new_from_password(login, password, config)


def random_string(prefix, size=8):
    return "%s-%x" % (prefix, random.randrange(16 ** size))


def before_all(context):
    configure_logging()
    context.api = api()
    context.random_string = random_string
