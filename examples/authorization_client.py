import conjur
import httplib

conjur.config.update(
    url = "http://possum",
    account = "example"
)

conn = httplib.HTTPConnection("localhost:8000")

possum = conjur.new_from_password('admin', 'secret')
conn.request("GET", "/", None, {"Authorization": possum.auth_header()})

response = conn.getresponse()
print response.status, response.reason
print response.read()
