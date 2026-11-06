#!/usr/bin/env python3
"""
Crops+resizes a photo to a square thumbnail, embeds it as base64 in
data/partners.json for the given partner, and saves a copy of both the
original and the thumbnail under source-photos/.

Usage:
    python3 set_photo.py <partner_id> <path/to/photo.jpg>

Find a partner's id with:
    python3 -c "import json; [print(p['id'], p['name']) for p in json.load(open('data/partners.json'))]"
"""
import sys, json, os, base64, shutil
from PIL import Image

def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)

    partner_id, photo_path = sys.argv[1], sys.argv[2]

    with open('data/partners.json') as f:
        partners = json.load(f)

    match = next((p for p in partners if p['id'] == partner_id), None)
    if not match:
        print(f"No partner with id {partner_id!r}. Known ids:")
        for p in partners:
            print(" ", p['id'], '-', p['name'])
        sys.exit(1)

    os.makedirs('source-photos/original', exist_ok=True)
    os.makedirs('source-photos/thumbs', exist_ok=True)

    ext = os.path.splitext(photo_path)[1] or '.jpg'
    shutil.copy(photo_path, f'source-photos/original/{partner_id}{ext}')

    im = Image.open(photo_path).convert('RGB')
    w, h = im.size
    s = min(w, h)
    left, top = (w - s) // 2, (h - s) // 2
    im = im.crop((left, top, left + s, top + s)).resize((300, 300), Image.LANCZOS)
    thumb_path = f'source-photos/thumbs/{partner_id}.jpg'
    im.save(thumb_path, 'JPEG', quality=84, optimize=True)

    with open(thumb_path, 'rb') as fh:
        b64 = 'data:image/jpeg;base64,' + base64.b64encode(fh.read()).decode('ascii')

    match['photo'] = b64

    with open('data/partners.json', 'w') as f:
        json.dump(partners, f)

    print(f"Updated photo for {match['name']} ({partner_id}).")
    print("Now run: python3 build.py")

if __name__ == '__main__':
    main()
