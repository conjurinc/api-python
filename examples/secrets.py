import conjur
import os
import random
import string

possum_url = os.environ['POSSUM_URL']
possum_account = os.environ['POSSUM_ACCOUNT']
possum_login = os.environ['POSSUM_LOGIN']
possum_password = os.environ['POSSUM_PASSWORD']

print('=========================================================================');
print('Base url :', possum_url);
print('Account  :', possum_account);
print('Login    :', possum_login);
print('Password :', possum_password);
print('=========================================================================');

conjur.config.url = possum_url
conjur.config.account = possum_account

client = conjur.new_from_password(possum_login, possum_password)

def random_password():
    # NOTE: just for example purposes.
    # Use strong crypto to generate actual passwords!
    return ''.join([random.choice(string.digits + string.letters + string.punctuation) for _ in range(12)])

def populate_some_variables(api):
    for password in [
        var for var in api.resources(kind='variable')
        if 'password' in var.identifier
    ]:
        pwd = random_password()
        print("Setting {} = {}".format(password.resourceid, pwd))
        password.add_secret(pwd)

def print_all_vars(api):
    for var in api.resources(kind='variable'):
        print("{} = {}".format(var.resourceid, var.secret()))

populate_some_variables(client)
print_all_vars(client)
