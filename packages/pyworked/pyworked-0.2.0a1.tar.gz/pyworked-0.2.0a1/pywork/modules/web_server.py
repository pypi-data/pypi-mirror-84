from http.server import HTTPServer, CGIHTTPRequestHandler

class Web:

    def __init__(self):
        pass

    def start(self, adr):
        httpd = HTTPServer(adr, CGIHTTPRequestHandler)
        httpd.serve_forever()

    def parse(self, file):
        f = open(file, 'r').read()
        return(f)

    def heading(self):
        return("Content-type: text/html")