from conjur.util import urlescape

class Variable(object):
    def __init__(self, api, id):
        self.id = id
        self.api = api

    def value(self):
        url = "%s/variables/%s/value"%(self.api.config.core_url, urlescape(self.id))
        return self.api.get(url).text

    def add_value(self, value):
        data = {'value': value}
        url = "%s/variables/%s/values"%(self.api.config.core_url, urlescape(self.id))
        self.api.post(url, data=data)

