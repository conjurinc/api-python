import os

class Config:
    def __init__(self):
        self._config = {}

    @property
    def authn_url(self):
        return self.service_url('authn')

    @authn_url.setter
    def authn_url(self, value):
        self.set('authn_url', value)

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

    def service_url(self, service, per_account=True):
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
        if os.environ.has_key(env_key):
            value = os.environ[env_key]
            self._config[key] = value
            return value
        return default

    def set(self, key, value):
        self._config[key] = value


__all__ = ('Config',)