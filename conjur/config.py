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
    def core_url(self):
        return self.service_url('core')

    @core_url.setter
    def core_url(self, value):
        self.set('core_url', value)

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