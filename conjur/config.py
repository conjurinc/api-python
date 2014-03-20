class Config:
    def __init__(self):
        pass

    @property
    def authn_url(self):
        return self.service_url('authn')

    @property
    def stack(self): return self.get('stack')

    @stack.setter
    def stack(self, value): self.set('stack', value)

    @property
    def account(self): return self.get('account')

    @account.setter
    def account(self, value): self.set('account', value)

    def service_url(self, service, per_account=True):
        if not self.appliance_url:
            fmt = "https://%s-%s-conjur.herokuapp.com"
            if per_account: loc = self.account
            else: loc = self.stack
            return fmt%(service, loc)
        else:
            # Appliance
            url_parts = [ self.appliance_url ]
            if service != "core": url_parts += ["api", service]
            return "/".join(url_parts)


config = Config()

__all__ = ('config', 'Config')