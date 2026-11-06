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

- Basemap: MapLibre GL JS rendering OpenFreeMap's free, no-API-key vector
  tiles (OpenMapTiles schema, `https://tiles.openfreemap.org/planet`). The
  `MAP_STYLE` object in `template.html` is a trimmed-down copy of
  OpenFreeMap's "positron" style — only background/water/borders/labels are
  kept (roads, buildings, landuse are dropped) — with land/water/label
  colors overridden to match the brand palette (`LAND`, `WATER`, `BORDER`,
  `LABEL_INK` constants near the top of the map script). To change the
  map's colors, edit those constants or the relevant layer's `paint` block
  and rebuild.
- Zoom numbers: MapLibre's vector tiles are 512px (vs. the old Esri raster
  tiles' 256px), so its zoom levels are offset by exactly 1 from "normal"
  slippy-map zoom — e.g. what used to be zoom 3 now looks the same at
  zoom 2. Keep this in mind if you ever change the default `zoom`/`minZoom`
  or the row-click `flyTo` zoom.
- Marker pin tip alignment is exact: the `.pin` div is sized so a
  MapLibre `Marker` with `anchor: 'bottom'` lands precisely on the
  rotated-square pin's visual tip. If you resize the pin (`.pin`, `.ring`
  CSS, or the marker's `anchor`/offset in `makeMarkerEl()`), the math has
  to stay consistent or the tip will drift off the real coordinate again —
  see git history for the original fix (done for the old Leaflet markers,
  same principle applies).
- Panning past the poles: MapLibre already refuses to show empty space
  beyond the poles on its own at most zoom levels; a small `map.on('move', ...)`
  handler clamps latitude to ±85° as a backstop at zoom levels where it
  wouldn't otherwise. Longitude is left unbounded so the map still scrolls
  continuously East/West.
