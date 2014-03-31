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

# TODO remember how to use metaprogramming in python to DRY this shit up a bit...
class Config:
    # TODO docstrings
    def __init__(self):
        self._config = {}

    def load(self, input):
        import yaml
        if isinstance(input, str):
            input = open(input, 'r')
        conf = yaml.safe_load(input)
        for k,v in conf:
            self._config[k] = v


    @property
    def authn_url(self):
        return self.service_url('authn')

    @authn_url.setter
    def authn_url(self, value):
        self.set('authn_url', value)

    @property
    def core_url(self):
        return self.service_url('core')

    @core_url.setter
    def core_url(self, value):
        self.set('core_url', value)

    @property
    def pubkeys_url(self):
        return self.service_url('pubkeys')

    @pubkeys_url.setter
    def pubkeys_url(self, value):
        self.set('pubkeys_url', value)

    @property
    def authz_url(self):
        return self.service_url('authz', False)

    @authz_url.setter
    def authz_url(self, value):
        self.set('authz_url', value)

    @property
    def stack(self):
        return self.get('stack')

    @stack.setter
    def stack(self, value):
        self.set('stack', value)

    @property
    def account(self):
        return self.get('account')

    @account.setter
    def account(self, value):
        self.set('account', value)

    @property
    def appliance_url(self):
        return self.get('appliance_url')

    @appliance_url.setter
    def appliance_url(self, value):
        self.set('appliance_url', value)

    def service_url(self, service, per_account=True):
        key = '%s_url'%service
        if key in self._config:
            return self._config[key]
        if not self.appliance_url:
            fmt = "https://%s-%s-conjur.herokuapp.com"
            if per_account: loc = self.account
            else: loc = self.stack
            return fmt%(service, loc)
        else:
            url_parts = [ self.appliance_url ]
            if service != "core": url_parts += ["api", service]
            return "/".join(url_parts)

    def get(self, key, default=None):
        if key in self._config: return self._config[key]
        env_key = 'CONJUR_' + key.upper()
        if env_key in os.environ:
            value = os.environ[env_key]
            self._config[key] = value
            return value
        return default

    def set(self, key, value):
        self._config[key] = value

config = Config()

__all__ = ('Config','config')