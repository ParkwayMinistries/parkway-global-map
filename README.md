# Parkway Global Partners Map

Self-hosted replacement for the paid [Atlist](https://atlist.com) map embedded
on https://parkwaybaptist.org/global. No subscription, no API keys, no
Google Maps billing — one static HTML file with everything (including
partner photos) baked in, hosted free on GitHub Pages.

## Live site

Published via GitHub Pages from this repo's `main` branch, root folder.
The Squarespace page embeds it with an `<iframe>` the same way it used to
embed Atlist — just pointing at this repo's Pages URL instead.

## How it's built

- `data/partners.json` — the source of truth: one record per partner
  (name, category, lat/lng, location label, bio note, link, base64 photo).
- `data/raw-atlist-data.json` — original one-time export pulled from
  Atlist's API (categories + markers), kept for reference only.
- `template.html` — the actual page (map, sidebar, styling, JS). Contains
  the placeholder `__PARTNERS_JSON__` where the data gets injected.
- `index.html` — the generated, publishable file. **Don't hand-edit this**
  — run `build.py` instead, or your changes will be overwritten next build.
- `source-photos/original/` and `source-photos/thumbs/` — photo working
  files (original downloads + the cropped 300x300 JPEGs that get base64'd
  into partners.json). Not needed at runtime, kept so photos can be
  re-cropped later without re-downloading.

## Making changes

**Add/update a partner's text fields** (name, location, category, bio,
link): edit `data/partners.json` directly, then:

```bash
python3 build.py
```

**Add/replace a partner's photo:**

```bash
python3 set_photo.py <partner_id> /path/to/new/photo.jpg
python3 build.py
```

(`set_photo.py` crops it to a square, resizes to 300x300, and embeds it.)

**Add a brand new partner:** append a new object to `data/partners.json`
with the same shape as the others (id can be any unique string), run
`set_photo.py` if they have a photo, then `build.py`.

Categories must be one of: `planters` (Church Planters), `outreach`
(Gospel Outreach), `support` (Gospel Support) — see the `CATS` object in
`template.html` for labels/colors.

**Publish the change:**

```bash
git add -A
git commit -m "Update partner info"
git push
```

GitHub Pages redeploys automatically within a minute or two of the push.

## Map/marker notes for future edits

- Basemap: Esri `World_Light_Gray_Base` + `World_Light_Gray_Reference`
  (free, no API key). The reference (labels) layer only renders text above
  zoom level ~3 — that's why the default view starts at zoom 3, not lower.
- Marker pin tip alignment is exact: the `.pin` div is sized/anchored so
  Leaflet's `iconAnchor` lands precisely on the rotated-square pin's visual
  tip. If you resize the pin (`.pin`, `.ring` CSS, or `iconSize`/
  `iconAnchor` in `makeIcon()`), the math has to stay consistent or the tip
  will drift off the real coordinate again — see git history for the fix.
