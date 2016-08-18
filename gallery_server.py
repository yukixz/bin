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

IMAGE_PER_PAGE = 20


class Handler(http.server.SimpleHTTPRequestHandler):
    def send_head(self):
        ''' Overwriting SimpleHTTPRequestHandler.send_head()
            Remove redirect of path not endswith '/'
            Remove display of index.html
        '''

        path = self.translate_path(self.path)
        if os.path.isdir(path):
            return self.list_directory(path)

        ctype = self.guess_type(path)
        try:
            f = open(path, 'rb')
        except OSError:
            self.send_error(404, "File not found")
            return None
        try:
            self.send_response(200)
            self.send_header("Content-type", ctype)
            fs = os.fstat(f.fileno())
            self.send_header("Content-Length", str(fs[6]))
            self.send_header("Last-Modified",
                             self.date_time_string(fs.st_mtime))
            self.end_headers()
            return f
        except:
            f.close()
            raise

    def list_directory(self, path):
        ''' Overwriting SimpleHTTPRequestHandler.list_directory()
        '''

        # make html header
        r = []
        displaypath = html.escape(urllib.parse.unquote(self.path))
        enc = sys.getfilesystemencoding()
        title = '%s' % displaypath
        r.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" '
                 '"http://www.w3.org/TR/html4/strict.dtd">')
        r.append('<html><head>')
        r.append('<meta http-equiv="Content-Type" '
                 'content="text/html; charset=%s">' % enc)
        r.append('<title>%s</title></head>' % title)
        r.append('<body><h1>%s</h1>' % title)

        # make file list
        try:
            list = os.listdir(path)
            list.sort(key=lambda a: a.lower())
            list.insert(0, '..')    # Add link to parent directory.
        except os.error:
            self.send_error(404, "No permission to list directory")
            return None

        # make image list and file list
        image_list = []
        file_list = []
        for name in list:
            ext = os.path.splitext(name)[1].lower()
            if ext in ['.bmp', '.gif', '.jpeg', '.jpg', '.png']:
                image_list.append(name)
            else:
                file_list.append(name)

        # make file html
        r.append('<hr><ul>')
        for name in file_list:
            fullname = os.path.join(path, name)
            displayname = linkname = name
            # Skip non-directroy
            if not os.path.isdir(fullname):
                continue

            displayname = name + "/"
            linkname = name + "/"
            r.append('<li><a href="%s">%s</a></li>' % (
                urllib.parse.quote(linkname), html.escape(displayname)))
        r.append('</ul><hr>')

        # image paging
        splits = urllib.parse.urlsplit(self.path)
        query = splits[3]
        if query.endswith('/'):
            query = query[:-1]
        querys = urllib.parse.parse_qs(query)
        page = int(querys.get('page', '1')[0])
        page_total = math.ceil(len(image_list) / IMAGE_PER_PAGE)
        if page <= 1:
            page = 1
            page_prev = 1
            page_next = 2
        elif page >= page_total:
            page = page_total
            page_prev = page_total - 1
            page_next = page_total
        else:
            page_prev = page - 1
            page_next = page + 1

        # make image html
        first_index = IMAGE_PER_PAGE * (page - 1)
        last_index = IMAGE_PER_PAGE * page
        for name in image_list[first_index:last_index]:
            r.append('<img src="%s"/><br/>' % (urllib.parse.quote(name)))
        r.append('<h1><a href="%s">Prev Page</a>' % urllib.parse.urlunsplit((
                splits[0], splits[1], splits[2],
                "page=%d" % page_prev, splits[4])))
        r.append('| {current}/{total} |'.format(
                current=page, total=page_total))
        r.append('<a href="%s">Next Page</a></h1>' % urllib.parse.urlunsplit((
                splits[0], splits[1], splits[2],
                "page=%d" % page_next, splits[4])))

        # make html footer
        r.append('</body></html>')

        # response
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
    address_family = socket.AF_INET6


if __name__ == '__main__':
    addr = ("", 8000)
    httpd = TCPServer(addr, Handler)
    print("Serving on %s:%d ..." % addr)
    httpd.serve_forever()
