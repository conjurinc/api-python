
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

# 2 vs 3 urlencode moved...
try:
    from urllib import quote
except:
    from urllib.parse import quote


def urlescape(s):
    return quote(s, '')


def authzid(obj, kind, with_account=True):
    if isinstance(obj, (str, unicode)):  # noqa F821 (flake8 doesn't know about unicode)
        if not with_account:
            return ':'.join(obj.split(':')[1:])
        return obj
    for attr in (kind, kind + 'id'):
        if hasattr(obj, attr):
            return authzid(getattr(obj, attr), kind)
    raise TypeError("Can't get {0}id from {1}".format(kind, obj))
