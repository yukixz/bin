#!/usr/bin/env python3

import argparse
import http.server

class Handler(http.server.SimpleHTTPRequestHandler):
    cookie = None

    def do_GET(self):
        print("-- Connection from %s:%s --" % self.client_address)
        print("Cookie: %s" % self.headers.get('Cookie', '(None)'))

        if self.cookie is None:
            self.send_response(500)
            self.end_headers()
        else:
            self.send_response(200)
            self.send_header("Cookie", self.cookie)
            self.end_headers()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description="A simple script for export and import cookie."
            )
    parser.add_argument("--cookie", help="new cookie to import")
    parser.add_argument("--port", help="port to serve (default 80)",
            type=int, default=80)
    args = parser.parse_args()

    address = ('0.0.0.0', args.port)
    if args.cookie is not None:
        Handler.cookie = args.cookie

    httpd = http.server.HTTPServer(address, Handler)
    print("Serving HTTP on %s:%s..." % address)
    httpd.serve_forever()

