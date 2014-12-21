#!/usr/bin/python3

import http.server

import html
import io
import math
import os
import socket
import socketserver
import sys
import urllib.parse

IPP = 10

class Handler(http.server.SimpleHTTPRequestHandler):
    def list_directory(self, path):
        ''' Overwriting SimpleHTTPRequestHandler.list_directory()
        '''
        try:
            list = os.listdir(path)
            list.sort(key=lambda a: a.lower())
            list.insert(0, '..')    #
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None
        r = []
        displaypath = html.escape(urllib.parse.unquote(self.path))
        enc = sys.getfilesystemencoding()
        title = '%s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html>\n<head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title>\n</head>' % title)
        r.append('<body>\n<h1>%s</h1>' % title)
        r.append('<hr>\n<ul>')

        list_image = []
        for name in list:
            ext = os.path.splitext(name)[1]
            if ext.lower() in ['.bmp', '.gif', '.jpeg', '.jpg', '.png']:
                list_image.append(name)
                continue
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Append / for directories or @ for symbolic links
            if os.path.isdir(fullname):
                displayname = name + "/"
                linkname = name + "/"
            if os.path.islink(fullname):
                displayname = name + "@"
                # Note: a link to a directory displays with @ and links with /
            r.append('<li><a href="%s">%s</a></li>'
                    % (urllib.parse.quote(linkname), html.escape(displayname)))
        r.append('</ul>\n<hr>')

        splits = urllib.parse.urlsplit(self.path)
        query = splits[3]
        while query.endswith('/'):
            query = query[:-1]
        querys = urllib.parse.parse_qs(query)
        page = int(querys.get('page', '0')[0])
        page_total = math.ceil(len(list_image) / IPP)
        if page <= 0:
            page = 0
            page_prev = 0
            page_next = 1
        elif page >= page_total:
            page = page_total
            page_prev = page_total - 1
            page_next = page_total
        else:
            page_prev = page - 1
            page_next = page + 1

        for name in list_image[IPP*page: IPP*(page+1)]:
            fullname = os.path.join(path, name)
            if os.path.isdir(fullname):
                continue
            r.append('<img src="%s"/><br/>'
                    % (urllib.parse.quote(name)))
        r.append('<h2><a href="%s">Prev Page</a>' % urllib.parse.urlunsplit((
                splits[0], splits[1], splits[2],
                "page=%d/" % page_prev, splits[4])))
        r.append('| {current}/{total} |'.format(
                current = page, total = page_total))
        r.append('<a href="%s">Next Page</a></h2>' % urllib.parse.urlunsplit((
                splits[0], splits[1], splits[2],
                "page=%d/" % page_next, splits[4])))
        r.append('</body>\n</html>\n')

        encoded = '\n'.join(r).encode(enc)
        f = io.BytesIO()
        f.write(encoded)
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=%s" % enc)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        return f

class TCPServer(socketserver.TCPServer):
    # IPv6 Support
    address_family =  socket.AF_INET6


if __name__=='__main__':
    httpd = TCPServer(("", 8000), Handler)
    print("Serving on 0.0.0.0:8000 ...")
    httpd.serve_forever()

