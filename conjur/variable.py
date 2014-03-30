
class Variable(object):
    def __init__(self, api, id, attrs=None):
        self.id = id
        self.api = api
        self._attrs = attrs

    def value(self):
        url = "%s/variables/%s/value"%(self.api.config.core_url, self.id)
        return self.api.get(url).text

    def add_value(self, value):
        url = "%s/variables/%s/values"%(self.api.config.core_url, self.id)

    def fetch(self):
        self._attrs = self.api.get('%s/variables/%s'%(self.api.config.core_url, self.id)).json

    def url(self, *extras, **query):
        parts = [self.api.config.core_url, "variables", self.id].extend(extras)

    @property
    def attrs(self):
        if self._attrs is not None: return self._attrs
        self.fetch()
        return self._attrs

    def __getattr__(self, item):
        try:
            return self.attrs[item]
        except KeyError:
            raise AttributeError(item)


