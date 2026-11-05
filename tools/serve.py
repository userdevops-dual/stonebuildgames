#!/usr/bin/env python3
"""Local preview with admin saving. Run: python3 tools/serve.py   (admin: http://localhost:8787/admin/)
Only listens on this computer. Saving writes into site/ and rebuilds the pages; use git to publish."""
import base64, functools, http.server, json, os, re, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SITE = os.path.join(ROOT, 'site')
PORT = int(os.environ.get('PORT', '8787'))
ALLOWED = re.compile(r'^site/(data/games\.json|assets/games/[a-z0-9-]+/[a-z0-9._-]+\.(webp|jpg|png))$')

def safe(path):
    if not ALLOWED.match(path) or '..' in path:
        raise ValueError('Path not allowed: ' + path)
    return os.path.join(ROOT, path)

class H(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()
    def reply(self, code, obj):
        body = json.dumps(obj).encode()
        self.send_response(code); self.send_header('Content-Type', 'application/json'); self.send_header('Content-Length', str(len(body))); self.end_headers(); self.wfile.write(body)
    def do_GET(self):
        if self.path == '/__admin/ping': return self.reply(200, {'ok': True})
        super().do_GET()
    def do_POST(self):
        origin = self.headers.get('Origin', '')
        if self.path != '/__admin/commit' or self.headers.get('X-Admin-Local') != '1' or not re.match(r'^http://(localhost|127\.0\.0\.1):\d+$', origin):
            return self.reply(403, {'error': 'Forbidden'})
        try:
            req = json.loads(self.rfile.read(int(self.headers.get('Content-Length', 0))))
            for f in req.get('files', []):
                p = safe(f['path']); os.makedirs(os.path.dirname(p), exist_ok=True)
                with open(p, 'wb') as out: out.write(base64.b64decode(f['content']))
            for d in req.get('deletes', []):
                p = safe(d)
                if os.path.exists(p): os.remove(p)
            r = subprocess.run([sys.executable, os.path.join(HERE, 'build_pages.py')], capture_output=True, text=True)
            if r.returncode: return self.reply(500, {'error': r.stderr[-600:]})
            self.reply(200, {'ok': True})
        except Exception as e:
            self.reply(400, {'error': str(e)})

http.server.ThreadingHTTPServer(('127.0.0.1', PORT), functools.partial(H, directory=SITE)).serve_forever()
