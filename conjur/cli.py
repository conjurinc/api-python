from netrc import netrc
from urlparse import urlparse
import argparse
import sys
import os
import conjur
import inflection
from tabulate import tabulate

def netrc_path():
  try:
    return os.environ['CONJURRC']
  except KeyError:
    return os.path.expanduser('~/.netrc')

def credentials_from_netrc():
  creds = netrc(netrc_path())
  result = creds.authenticators(conjur.config.url)
  try:
    return ( result[0], result[2] )
  except TypeError:
    raise Exception("Conjur URL %s is not in %s, therefore you're not logged in" % ( conjur.config.url, netrc_path() ))

def credentials():
  try:
    ( os.environ['CONJUR_AUTHN_LOGIN'], os.environ['CONJUR_AUTHN_API_KEY'] )
  except KeyError:
    return credentials_from_netrc()

def connect():
  return conjur.new_from_key(*credentials())

def find_object(kind, id):
  api = connect()
  if len(id.split(':')) > 0:
    return api.resource_qualified(id)
  else:
    return api.resource(kind, id)

def find_variable(id):
  return find_object('variable', id)

def find_policy(id):
  return find_object('policy', id)

def authenticate_handler(args):
  import base64
  token = connect().authenticate()
  if args.H:
    token = base64.b64encode(token)
  print token

def whoami_handler(args):
  api = connect()
  api.authenticate()
  print ':'.join(( conjur.config.account, conjur.util.login_kind(api.login), conjur.util.login_identifier(api.login) ))

def list_handler(args):
  def flatten_record(record):
    result = [ record['id'], record['owner'] ]
    if 'policy' in record.keys():
      result.append(record['policy'])
    return result

  api = connect()
  resources = [ flatten_record(resource) for resource in api.get(api._resources_url(kind=args.kind)).json() ]
  print tabulate(resources, headers=['Id', 'Owner', 'Policy'])

def show_handler(args):
  api = connect()
  resource = api.resource_qualified(args.id)
  resource = resource.api.get(resource.url()).json()
  keys = resource.keys()
  keys.sort()
  data  =[ ( inflection.camelize(key), resource[key] ) for key in keys ]
  print tabulate(data)

def policy_load_handler(args):
  if args.policy == '-':
    value = sys.stdin.read()
  else:
    value = args.policy
  policy = find_policy(args.id)
  url = [
    policy.api.config.url,
    'policies',
    policy.account,
    policy.kind,
    conjur.util.urlescape(policy.identifier)
  ]

  policy.api.post(url, data=value)

def fetch_handler(args):
  print find_variable(args.id).secret(args.version)

def store_handler(args):
  if args.value == '-':
    value = sys.stdin.read()
  else:
    value = args.value
  find_variable(args.id).add_secret(value)
  print "Value added"

parser = argparse.ArgumentParser(description='Possum command-line client.')
subparsers = parser.add_subparsers()

whoami = subparsers.add_parser('whoami')
whoami.set_defaults(func=whoami_handler)

authenticate = subparsers.add_parser('authenticate')
authenticate.add_argument('-H', action='store_true')
authenticate.set_defaults(func=authenticate_handler)

list_ = subparsers.add_parser('list')
list_.add_argument('-k', '--kind', help='Resource kind')
list_.set_defaults(func=list_handler)

show = subparsers.add_parser('show')
show.add_argument('id')
show.set_defaults(func=show_handler)

policy_load = subparsers.add_parser('policy:load')
policy_load.add_argument('id')
policy_load.add_argument('policy')
policy_load.set_defaults(func=policy_load_handler)

store = subparsers.add_parser('store')
store.add_argument('id')
store.add_argument('value')
store.set_defaults(func=store_handler)

fetch = subparsers.add_parser('fetch')
fetch.add_argument('id')
fetch.add_argument('-V', '--version', help='Variable version')
fetch.set_defaults(func=fetch_handler)

args = parser.parse_args()
args.func(args)
