# Tools

## `prepare-images.sh`

Run on the folder of originals Mark sends. Resizes to 2400px, converts to sRGB, strips
metadata, compresses to quality 82, and writes a matching WebP alongside each JPEG.

```
./tools/prepare-images.sh ~/Downloads/special-green-photos
```

**It strips EXIF, and that matters.** Photos taken at customers' homes carry GPS coordinates
in the file. Publishing those publishes their addresses. The `-strip` flag removes them.

## `make-placeholders.py` and `slots.json`

Generates the dark tonal placeholders in `assets/images/`. They are SVG, a few hundred bytes
each, and have no depicted content on purpose: no houses, no people, no work. A site that
shows invented projects is worse than one that shows nothing.

`prepare-images.sh` switches a slot from `NAME.svg` to `NAME.jpg` the moment a real photograph
for that slot lands, and deletes the placeholder it replaced. Slots without a photo yet keep
their placeholder, so the page is never broken mid-way through a shoot.

Once every slot has a real photograph, this script and `slots.json` can be deleted.

## Turning WebP on

The markup serves JPEG only right now, because shipping a `<picture>` element whose WebP
source is missing produces a broken image rather than a fallback. Once `prepare-images.sh`
has written `.webp` files for every slot, each `<img>` in `index.html` can be wrapped:

```html
<picture>
  <source type="image/webp" srcset="assets/images/NAME.webp">
  <img src="assets/images/NAME.jpg" alt="..." width="W" height="H" decoding="async" loading="lazy">
</picture>
```

Only do this when the WebP file for that slot actually exists. JPEG at quality 82 is already
fast; WebP is worth roughly 25 to 35 percent on top of it, not a rescue.
