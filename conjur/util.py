
# 2 vs 3 urlencode moved...
try:
    from urllib import urlencode, quote
except:
    from urllib.parse import urlencode, quote

def urlescape(s):
    return quote(s, '')