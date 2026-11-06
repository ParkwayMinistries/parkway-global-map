#!/usr/bin/env python3
"""
Rebuilds index.html from template.html + data/partners.json.

Run this after editing data/partners.json (or re-running the photo
pipeline) to regenerate the self-contained, publishable index.html.
"""
import json

with open('data/partners.json') as f:
    partners = json.load(f)

with open('template.html') as f:
    tpl = f.read()

out = tpl.replace('__PARTNERS_JSON__', json.dumps(partners))

with open('index.html', 'w') as f:
    f.write(out)

print(f"Built index.html ({len(out) // 1024} KB) from {len(partners)} partners.")
