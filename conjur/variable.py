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

from conjur.util import urlescape


class Variable(object):
    def __init__(self, api, id, attrs=None):
        self.id = id
        self.api = api
        self._attrs = attrs

    def value(self, version=None):
        url = "%s/variables/%s/value" % (self.api.config.core_url, urlescape(self.id))
        if version is not None:
            url = "%s?version=%s" % (url, version)
        return self.api.get(url).text

    def add_value(self, value):
        # Invalidate _attrs since our version count is going to change
        self._attrs = None
        data = {'value': value}
        url = "%s/variables/%s/values" % (self.api.config.core_url, urlescape(self.id))
        self.api.post(url, data=data)

    def __getattr__(self, item):
        if self._attrs is None:
            self._fetch()
        try:
            return self._attrs[item]
        except KeyError:
            raise AttributeError(item)

    def _fetch(self):
        self._attrs = self.api.get(
            "{0}/variables/{1}".format(self.api.config.core_url,
                                       urlescape(self.id))
        ).json()

