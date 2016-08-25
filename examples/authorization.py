from wsgiref.simple_server import make_server
import conjur
from base64 import b64decode

conjur.config.update(
    url = "http://possum.example",
    account = "example"
)

possum_resource = 'example:webservice:prod/analytics/v1'

def simple_app(environ, start_response):
    # Usually you'd use some utility for extracting auth, but let's keep it simple
    username, password = b64decode(environ['HTTP_AUTHORIZATION'].split(' ')[1]).split(':')

    try:
        # can also use API key or token directly
        possum = conjur.new_from_password(username, password)
    except conjur.ConjurException:
        start_response("401 Unauthorized", [])
        return ["Unauthorized\r\n"]

    if not possum.resource_qualified(possum_resource).permitted('execute'):
        start_response("403 Forbidden", [])
        return ["Forbidden\r\n"]
    else:
        status = '200 OK'
        headers = [('Content-type', 'text/plain')]

        start_response(status, headers)

        return 'You are authorized!!!!!\n'

httpd = make_server('', 8000, simple_app)
print "Serving on port 8000..."
httpd.serve_forever()
