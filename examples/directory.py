import conjur
import os

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

for group in client.resources(kind='group'):
    print("Group {}; members:".format(group.resourceid))
    for mem in group.role().members():
        roleid = mem["member"]
        print(" - {}".format(roleid))

for user in client.resources(kind='user'):
    print("User {}".format(user.resourceid))
    keys = user.role().public_keys()
    if len(keys):
        print("   public keys:")
        for key in keys:
            print("    - {}".format(key))
