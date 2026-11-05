#!/usr/bin/env python3
"""Change the admin login. Run: python3 tools/set_admin_password.py   Only a salted hash is stored, in site/admin/auth.js."""
import base64, getpass, hashlib, json, os, secrets
ITER = 200000
user = os.environ.get('SB_ADMIN_USER') or input('Username: ').strip()
pw = os.environ.get('SB_ADMIN_PASS') or getpass.getpass('Password: ')
salt = secrets.token_bytes(16)
h = hashlib.pbkdf2_hmac('sha256', f'{user}\n{pw}'.encode(), salt, ITER)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'admin', 'auth.js')
open(out, 'w').write('window.SB_AUTH = ' + json.dumps({'salt': base64.b64encode(salt).decode(), 'iter': ITER, 'hash': base64.b64encode(h).decode()}) + ';\n')
print('Admin login updated.')
