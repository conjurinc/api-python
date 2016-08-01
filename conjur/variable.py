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
    """
    A `Variable` represents a versioned secret stored in Conjur.

    Generally you will get an instance of this class by calling `conjur.API.create_variable`
    or `conjur.API.variable`.

    Instances of this class allow you to fetch values of the variable, and store new ones.

    Example:

        >>> # Print the current value of the variable `mysql-password`
        >>> variable = api.variable('mysql-password')
        >>> print("mysql-password is {}".format(variable.value()))

    Example:

        >>> # Print all versions of the same variable
        >>> variable = api.variable('mysql-password')
        >>> for i in range(1, variable.version_count + 1): # version numbers are 1 based
        ...     print("version {} of 'mysql-password' is {}".format(i, variable.value(i)))

    """
    def __init__(self, api, id, attrs=None):
        self.id = id
        self.api = api
        self._attrs = attrs

    def value(self, version=None):
        """
        Retrieve the secret stored in a variable.

        `version` is a *one based* index of the version to be retrieved.

        If no such version exists, a 404 error is raised.

        Returns the value of the variable as a string.
        """
        url = "%s/variables/%s/value" % (self.api.config.core_url,
                                         urlescape(self.id))
        if version is not None:
            url = "%s?version=%s" % (url, version)
        return self.api.get(url).text

    def add_value(self, value):
        """
        Stores a new version of the secret in this variable.

        `value` is a string giving the new value to store.

        This increments the variable's `version_count` member by one.
        """
        self._attrs = None
        data = {'value': value}
        url = "%s/variables/%s/values" % (self.api.config.core_url,
                                          urlescape(self.id))
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
