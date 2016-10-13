from __future__ import print_function
from netrc import netrc
from urlparse import urlparse
import getpass
import argparse
import sys
import os
import conjur
import inflection
import json
from tabulate import tabulate

def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)

def netrc_path():
  try:
    return os.environ['CONJURRC']
  except KeyError:
    return os.path.expanduser('~/.netrc')

def touch_netrc():
  path = netrc_path()
  with open(path, 'a'):
    os.utime(path, None)
  os.chmod(path, 0o600)

def netrc_str(netrc):
  """Dump the class data in the format of a .netrc file."""
  rep = ""
  for host in netrc.hosts.keys():
    attrs = netrc.hosts[host]
    rep = rep + "machine "+ host + "\n\tlogin " + str(attrs[0]) + "\n"
    if attrs[1]:
      rep = rep + "account " + str(attrs[1])
    rep = rep + "\tpassword " + str(attrs[2]) + "\n"
  for macro in netrc.macros.keys():
    rep = rep + "macdef " + macro + "\n"
    for line in netrc.macros[macro]:
      rep = rep + line
      rep = rep + "\n"
  return rep

def credentials_from_netrc():
  try:
    creds = netrc(netrc_path())
  except IOError:
    raise Exception("Not logged in. File %s does not exist" % netrc_path())

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

def current_roleid():
  # Ensure the login is valid
  api = connect()
  api.authenticate()
  username = api.login
  account = conjur.config.account
  if username.find('/') != -1:
    kind, _, id = username.partition('/')
  else:
    kind, id = ( 'user', username)
  return "%s:%s:%s" % ( account, kind, id )

def find_object(kind, id):
  api = connect()
  if len(id.split(':')) > 1:
    return api.resource_qualified(id)
  else:
    return api.resource(kind, id)

def find_variable(id):
  return find_object('variable', id)

def find_policy(id):
  return find_object('policy', id)

def interpret_login(role):
  tokens = role.split(':', 1)
  if len(tokens) == 2:
    return tokens
  else:
    return ( 'user', tokens[0] )

def login_handler(args):
  role = args.role
  if not role:
    eprint("Enter your username to log into Possum: ", end="")
    role = raw_input()
  kind, identifier = interpret_login(role)
  username = '/'.join((kind, identifier))

  if args.rotate:
    api = connect()
    role = conjur.Role.from_roleid(api, ":".join((kind, identifier)))
    api_key = role.rotate_api_key()
  else:
    password = getpass.getpass("Enter password for %s %s (it will not be echoed): " % ( kind, identifier ))
    api_key = conjur.new_from_password(username, password).api_key

  save_api_key(username, api_key)
  print("Logged in")

def save_api_key(username, api_key):
  touch_netrc()
  logins = netrc(netrc_path())
  logins.hosts[conjur.config.url] = ( username, None, api_key )
  with open(netrc_path(), 'w') as f:
    f.write(netrc_str(logins))

def authenticate_handler(args):
  import base64
  token = connect().authenticate()
  if args.H:
    token = base64.b64encode(token)
  print(token)

def whoami_handler(args):
  print(current_roleid())

def rotate_api_key_handler(args):
  api = connect()
  role = conjur.Role.from_roleid(api, args.role or current_roleid())
  api_key = role.rotate_api_key()
  if not args.role:
    save_api_key(api.login, api_key)
  print(api_key)

def list_handler(args):
  def flatten_record(record):
    result = [ record['id'], record['owner'] ]
    if 'policy' in record.keys():
      result.append(record['policy'])
    return result

  api = connect()
  resources = [ flatten_record(resource) for resource in api.get(api._resources_url(kind=args.kind)).json() ]
  print(tabulate(resources, headers=['Id', 'Owner', 'Policy']))

def show_handler(args):
  api = connect()
  resource = api.resource_qualified(args.id)
  resource = resource.api.get(resource.url()).json()
  keys = resource.keys()
  keys.sort()
  def format_value(value):
    if isinstance(value, basestring):
      return value
    else:
      return json.dumps(value)

  data  = [ ( inflection.camelize(key), format_value(resource[key]) ) for key in keys ]
  print(tabulate(data))

def policy_load_handler(args):
  if args.policy == '-':
    value = sys.stdin.read()
  else:
    value = args.policy
  policy = find_policy(args.id)
  url = '/'.join([
    policy.api.config.url,
    'policies',
    policy.api.config.account,
    'policy',
    conjur.util.urlescape(policy.identifier)
  ])

  response = policy.api.post(url, data=value).json()
  created_roles = response['created_roles']
  print("")
  print("Loaded policy version %s" % response['version'])
  print("Created %s roles" % len(created_roles))
  if len(created_roles) > 0:
    print("")
    print(tabulate([ ( record['id'], record['api_key'] ) for record in created_roles.values() ], ("Id", "API Key")))
    print("")

def fetch_handler(args):
  print(find_variable(args.id).secret(args.version))

def store_handler(args):
  if args.value == '-':
    value = sys.stdin.read()
  else:
    value = args.value
  find_variable(args.id).add_secret(value)
  print("Value added")

parser = argparse.ArgumentParser(description='Possum command-line interface.')
subparsers = parser.add_subparsers()

login = subparsers.add_parser('login')
login.add_argument('-r', '--role')
login.add_argument('--rotate', action='store_true')
login.set_defaults(func=login_handler)

whoami = subparsers.add_parser('whoami')
whoami.set_defaults(func=whoami_handler)

authenticate = subparsers.add_parser('authenticate')
authenticate.add_argument('-H', action='store_true')
authenticate.set_defaults(func=authenticate_handler)

rotate_api_key = subparsers.add_parser('rotate_api_key')
rotate_api_key.add_argument('-r', '--role')
rotate_api_key.set_defaults(func=rotate_api_key_handler)

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
