import conjur
import httplib

conjur.config.update(
    url = "http://possum.example",
    account = "example"
)

conn = httplib.HTTPConnection("service.example:8000")

possum = conjur.new_from_password('admin', 'admin')
conn.request("GET", "/", None, {"Authorization": possum.auth_header()})

response = conn.getresponse()
print response.status, response.reason
print response.read()
