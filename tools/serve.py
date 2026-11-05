#!/usr/bin/env python3
"""Local preview without browser caching, so edits always show. Run: python3 tools/serve.py"""
import functools, http.server, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site')
class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
http.server.ThreadingHTTPServer(('', 8787), functools.partial(H, directory=ROOT)).serve_forever()
