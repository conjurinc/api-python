from wsgiref.simple_server import make_server
import conjur

conjur.config.update(
    url = "http://possum.example",
    account = "example"
)

possum_resource = 'example:host:myapp-01'

def simple_app(environ, start_response):
    # use authorization header supplied by the client
    possum = conjur.new_from_header(environ['HTTP_AUTHORIZATION'])

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
