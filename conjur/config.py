#
# Copyright (C) 2014 Conjur Inc
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

import os

_DEFAULT = object()


def _setting(name, default=_DEFAULT, doc=''):
    def fget(self):
        return self.get(name, default)

    def fset(self, value):
        self.set(name, value)

    return property(fget, fset, doc=doc)


def _service_url(name, per_account=True, doc=''):
    def fget(self):
        return self.service_url(name, per_account)

    def fset(self, value):
        self.set(name + '_url', value)

    return property(fget=fget, fset=fset, doc=doc)


class Config:
    def __init__(self, **kwargs):
        self._config = {}
        self.update(kwargs)

    def load(self, input):
        import yaml

        if isinstance(input, str):
            input = open(input, 'r')
        conf = yaml.safe_load(input)
        self.update(conf)

    def update(self, *dicts, **kwargs):
        for d in dicts + (kwargs, ):
            self._config.update(d)

    def service_url(self, service, per_account=True):
        key = '%s_url' % service
        if key in self._config:
            return self._config[key]
        if not self.appliance_url:
            fmt = "https://%s-%s-conjur.herokuapp.com"
            if per_account:
                loc = self.account
            else:
                loc = self.stack
            return fmt % (service, loc)
        else:
            url_parts = [self.appliance_url]
            if service != "core":
                url_parts.append(service)
            return "/".join(url_parts)

    def get(self, key, default=_DEFAULT):
        if key in self._config:
            return self._config[key]
        env_key = 'CONJUR_' + key.upper()
        if env_key in os.environ:
            value = os.environ[env_key]
            self._config[key] = value
            return value
        if default is _DEFAULT:
            raise Exception("config setting %s is required" % key)
        return default

    def set(self, key, value):
        self._config[key] = value

    authn_url = _service_url('authn', doc='URL for the authn service')
    core_url = _service_url('core', doc='URL for the core service')
    authz_url = _service_url('authz', per_account=False, doc='URL for the authz service')
    pubkeys_url = _service_url('pubkeys', doc='URL for the pubkeys service')

    verify_ssl = _setting('verify_ssl', True, "Allows SSL verification to be disabled (development only!)")
    cert_file = _setting('cert_file', None, "Path to certificate to verify ssl requests to appliance")
    stack = _setting('stack', 'v4', 'Identifier for shared conjur services (hosted only)')
    account = _setting('account', 'conjur', 'Conjur account identifier')
    appliance_url = _setting('appliance_url', None, 'URL for Conjur appliance')


config = Config()

__all__ = ('Config', 'config')