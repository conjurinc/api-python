from conjur.util import urlescape


class User(object):
    def __init__(self, api, login, attrs=None):
        self.api = api
        self.login = login
        self._attrs = attrs

    def __getattr__(self, item):
        if self._attrs is None:
            self._fetch()
        try:
            return self._attrs[item]
        except KeyError:
            raise AttributeError(item)

    def _fetch(self):
        self._attrs = self.api.get(
            "{0}/users/{1}".format(self.api.config.core_url,
                                   urlescape(self.login))
        ).json

