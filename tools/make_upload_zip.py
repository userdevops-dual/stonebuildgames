#!/usr/bin/env python3
"""Creates hostinger-upload.zip with the finished website, for manual upload to public_html."""
import os, zipfile
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
SITE = os.path.join(ROOT, 'site')
with zipfile.ZipFile(os.path.join(ROOT, 'hostinger-upload.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
    for d, _, files in os.walk(SITE):
        for f in files:
            if f == '.DS_Store': continue
            p = os.path.join(d, f); z.write(p, os.path.relpath(p, SITE))
print('hostinger-upload.zip ready')
