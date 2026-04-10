#!/usr/bin/env python3
"""Simple HTTP server with correct MIME types for 3D files."""

import http.server
import socketserver
import sys
import os

PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8080

MIME_MAP = {
    '.stl': 'application/octet-stream',
    '.obj': 'application/octet-stream',
    '.3mf': 'application/octet-stream',
}

class Handler(http.server.SimpleHTTPRequestHandler):
    def guess_type(self, path):
        base, ext = os.path.splitext(path)
        ext = ext.lower()
        if ext in MIME_MAP:
            return MIME_MAP[ext]
        return super().guess_type(path)

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Serving at http://localhost:{PORT}")
    httpd.serve_forever()
