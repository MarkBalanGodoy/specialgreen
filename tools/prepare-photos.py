#!/usr/bin/env python3
"""
Special Green - turn real photographs into live site images.

THE PROBLEM THIS SOLVES
    assets/README.md promised that dropping a correctly named .jpg into assets/
    would put it on the site with no code changes. It would not have. index.html
    references .svg placeholders in assets/images/, so a photo dropped as the
    README described would have been ignored completely.

WHAT THIS DOES
    Drop photos into assets/incoming/ named after the slot they belong to
    (hero-outdoor-living.jpg, crew-group.jpg, ...). Any common format works,
    and the extension does not matter. Then run:

        python3 tools/prepare-photos.py

    For each photo it crops to the slot's aspect ratio, resizes to the spec
    width, writes a JPEG and a WebP into assets/images/, and rewrites the
    matching <img> in index.html into a <picture> that serves WebP with a JPEG
    fallback. Slots with no photo keep their placeholder illustration.

    Re-run it whenever new photos land. It is idempotent: running it twice
    changes nothing the second time, and a slot already switched to a photo is
    updated in place rather than duplicated.

        python3 tools/prepare-photos.py --check     report status, change nothing
        python3 tools/prepare-photos.py --revert    put every slot back on its
                                                    placeholder illustration

CROPPING
    Photos are cropped from the centre by default, which is right most of the
    time. When it is not, add a gravity hint to the filename:

        crew-group--top.jpg      keep the top of the frame
        hero-outdoor-living--bottom.jpg
        project-front-yard--left.jpg / --right.jpg

    Nothing is upscaled. A photo smaller than the target width is used at its
    own size and a warning is printed, because a stretched photo looks worse
    than a slightly soft one.
"""

import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INCOMING = os.path.join(ROOT, "assets", "incoming")
IMAGES = os.path.join(ROOT, "assets", "images")
INDEX = os.path.join(ROOT, "index.html")

JPEG_QUALITY = 76
WEBP_QUALITY = 72

# Slot name -> (target width, target height).
#
# These are display sizes, not the design's nominal sizes. Every slot is sized
# to how large it actually renders, doubled for retina. The before/after halves
# render at roughly 200 CSS pixels, so shipping 1536px into them was sending
# about four times the pixels a phone could ever show. Aspect ratios are
# identical to the design's, so the crops are unchanged.
SLOTS = {
    # full-bleed bands, 16:9
    "hero-outdoor-living":     (1920, 1080),
    "commercial-crew-trucks":  (1920, 1080),
    "customer-crew-leader":    (1920, 1080),
    "cta-sunset":              (1920, 1080),
    # vertical, 4:5
    "crew-portrait":           (960, 1200),
    "mobile-break-01":         (900, 1125),
    "mobile-break-02":         (900, 1125),
    # 4:3
    "crew-group":              (1100, 825),
    "service-lawn-care":       (900, 675),
    "service-landscaping":     (900, 675),
    "service-irrigation":      (900, 675),
    # square details
    "crew-trimmer":            (700, 700),
    "crew-truck-load":         (700, 700),
    "detail-edging":           (700, 700),
    "detail-trimmer":          (700, 700),
    "detail-blower":           (700, 700),
    "detail-irrigation-valve": (700, 700),
    # project cards, 16:11
    "project-patio-landscape": (1200, 825),
    "project-front-yard":      (1200, 825),
    "project-irrigation":      (1200, 825),
    "project-office-park":     (1200, 825),
    # before/after halves render small; 4:3
    "before-01-before":        (600, 450),
    "before-01-after":         (600, 450),
    "before-02-before":        (600, 450),
    "before-02-after":         (600, 450),
    "before-03-before":        (600, 450),
    "before-03-after":         (600, 450),
}

READABLE = (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff", ".bmp", ".heic", ".heif")
GRAVITIES = ("top", "bottom", "left", "right", "center")


def find_dropped():
    """Map slot name -> (path, gravity) for everything in the drop folder."""
    found = {}
    if not os.path.isdir(INCOMING):
        return found
    for fn in sorted(os.listdir(INCOMING)):
        stem, ext = os.path.splitext(fn)
        if ext.lower() not in READABLE or fn.startswith("."):
            continue
        gravity = "center"
        if "--" in stem:
            stem, _, hint = stem.rpartition("--")
            if hint.lower() in GRAVITIES:
                gravity = hint.lower()
            else:
                print("  ! %s: unknown crop hint '%s', using centre" % (fn, hint))
        if stem not in SLOTS:
            print("  ! %s: '%s' is not a slot name, skipped" % (fn, stem))
            continue
        found[stem] = (os.path.join(INCOMING, fn), gravity)
    return found


def crop_resize(im, tw, th, gravity):
    """Cover-crop to the target aspect ratio, then scale down to size."""
    from PIL import Image

    sw, sh = im.size
    target = tw / float(th)
    have = sw / float(sh)
    if have > target:                      # too wide: trim the sides
        nw = int(round(sh * target))
        if gravity == "left":
            box = (0, 0, nw, sh)
        elif gravity == "right":
            box = (sw - nw, 0, sw, sh)
        else:
            box = ((sw - nw) // 2, 0, (sw - nw) // 2 + nw, sh)
    else:                                  # too tall: trim top/bottom
        nh = int(round(sw / target))
        if gravity == "top":
            box = (0, 0, sw, nh)
        elif gravity == "bottom":
            box = (0, sh - nh, sw, sh)
        else:
            box = (0, (sh - nh) // 2, sw, (sh - nh) // 2 + nh)
    im = im.crop(box)
    if im.size[0] > tw:                    # never upscale
        im = im.resize((tw, th), Image.LANCZOS)
    return im


def process(slot, src, gravity):
    from PIL import Image, ImageOps

    tw, th = SLOTS[slot]
    im = Image.open(src)
    im = ImageOps.exif_transpose(im)       # honour phone rotation
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    elif im.mode == "L":
        im = im.convert("RGB")
    ow, oh = im.size
    im = crop_resize(im, tw, th, gravity)
    # Judge softness on the cropped result, not the source. A 3000x1000 photo is
    # wider than a 1600px target but only yields 1333px once cropped to 4:3.
    soft = im.size[0] < tw
    jpg = os.path.join(IMAGES, slot + ".jpg")
    webp = os.path.join(IMAGES, slot + ".webp")
    im.save(jpg, "JPEG", quality=JPEG_QUALITY, optimize=True, progressive=True)
    im.save(webp, "WEBP", quality=WEBP_QUALITY, method=6)
    # WebP usually wins, but not always: on noisy phone photos of foliage it can
    # come out larger than JPEG. Serving it then would cost bytes for nothing, so
    # keep it only when it actually saves something worth a second file.
    jpg_kb = os.path.getsize(jpg) / 1024.0
    webp_kb = os.path.getsize(webp) / 1024.0
    keep_webp = webp_kb < jpg_kb * 0.95
    if not keep_webp:
        os.remove(webp)
    return {
        "slot": slot, "src": os.path.basename(src), "from": (ow, oh),
        "to": im.size, "soft": soft, "webp": keep_webp,
        "jpg_kb": jpg_kb, "webp_kb": webp_kb if keep_webp else 0.0,
    }


# --- index.html rewriting ----------------------------------------------------
# The <img> for a slot is either bare (still on the placeholder) or already
# wrapped in a <picture> from a previous run. Both are matched so the script
# stays idempotent and can be re-run or reverted freely.

def _img_re(slot):
    return re.compile(
        r'<img\s+src="assets/images/%s\.(?:svg|jpg)"(?P<rest>[^>]*)/?>' % re.escape(slot))


def _picture_re(slot):
    return re.compile(
        r'<picture data-slot="%s">.*?</picture>' % re.escape(slot), re.S)


def switch_to_photo(html, slot):
    """Point a slot at its photo, wrapped in a <picture> for the WebP."""
    pic = _picture_re(slot)
    m = pic.search(html)
    if m:
        inner = _img_re(slot).search(m.group(0))
        rest = inner.group("rest") if inner else ""
        block = _build_picture(slot, rest)
        return html[:m.start()] + block + html[m.end():], True
    m = _img_re(slot).search(html)
    if not m:
        return html, False
    return html[:m.start()] + _build_picture(slot, m.group("rest")) + html[m.end():], True


def _build_picture(slot, rest):
    rest = rest.rstrip().rstrip("/")
    src = ""
    if os.path.exists(os.path.join(IMAGES, slot + ".webp")):
        src = '<source srcset="assets/images/%s.webp" type="image/webp"/>' % slot
    return (
        '<picture data-slot="%s">%s<img src="assets/images/%s.jpg"%s/></picture>'
    ) % (slot, src, slot, rest)


def revert_to_placeholder(html, slot):
    """Unwrap a <picture> and put the slot back on its .svg illustration."""
    m = _picture_re(slot).search(html)
    if not m:
        return html, False
    inner = _img_re(slot).search(m.group(0))
    rest = inner.group("rest").rstrip().rstrip("/") if inner else ""
    img = '<img src="assets/images/%s.svg"%s/>' % (slot, rest)
    return html[:m.start()] + img + html[m.end():], True


BANNER_RE = re.compile(r'(<div class="staging-bar" role="status">)(.*?)(</div>)', re.S)
BANNER_MIXED = ("Preview build &mdash; some images are still placeholder illustrations, "
                "not real project photos. Figures not yet verified")
BANNER_ALL_ILLUSTRATION = ("Preview build &mdash; images are placeholder illustrations, "
                           "not real project photos. Figures not yet verified")
BANNER_ALL_PHOTO = "Preview build &mdash; figures not yet verified"


def update_banner(html, state):
    """Keep the staging banner honest about what the reader is looking at.

    The banner is a disclosure, so it has to track reality rather than be
    remembered by hand: it overclaims once real photos land and underclaims
    while any placeholder is left.
    """
    on_photo = sum(1 for v in state.values() if v == "photo")
    if on_photo == 0:
        text = BANNER_ALL_ILLUSTRATION
    elif on_photo < len(SLOTS):
        text = BANNER_MIXED
    else:
        text = BANNER_ALL_PHOTO
    return BANNER_RE.sub(lambda m: m.group(1) + text + m.group(3), html, count=1)


def current_state(html):
    """slot -> 'photo' or 'placeholder', read straight from the markup."""
    state = {}
    for slot in SLOTS:
        if _picture_re(slot).search(html):
            state[slot] = "photo"
        elif re.search(r'assets/images/%s\.svg' % re.escape(slot), html):
            state[slot] = "placeholder"
        else:
            state[slot] = "missing"
    return state


def main():
    ap = argparse.ArgumentParser(description="Put real photographs on the Special Green site.")
    ap.add_argument("--check", action="store_true", help="report status, change nothing")
    ap.add_argument("--revert", action="store_true", help="put every slot back on its placeholder")
    args = ap.parse_args()

    html = open(INDEX, encoding="utf-8").read()
    state = current_state(html)

    if args.revert:
        n = 0
        for slot in SLOTS:
            html, ok = revert_to_placeholder(html, slot)
            n += ok
        html = update_banner(html, current_state(html))
        open(INDEX, "w", encoding="utf-8").write(html)
        print("Reverted %d slot(s) to placeholder illustrations." % n)
        print("The .jpg/.webp files are left in assets/images/; delete them if you want them gone.")
        return 0

    dropped = find_dropped()

    if args.check:
        on_photo = [s for s, v in state.items() if v == "photo"]
        print("Slots: %d total | %d on real photos | %d on placeholders"
              % (len(SLOTS), len(on_photo), len(SLOTS) - len(on_photo)))
        print("Drop folder: %s" % (("%d usable file(s)" % len(dropped)) if dropped
                                   else "empty (assets/incoming/)"))
        if on_photo:
            print("\nOn real photos:")
            for s in sorted(on_photo):
                print("  %s" % s)
        waiting = [s for s in SLOTS if state[s] != "photo" and s not in dropped]
        if waiting:
            print("\nStill waiting on a photograph (%d):" % len(waiting))
            for s in sorted(waiting):
                print("  %-26s %dx%d" % (s, *SLOTS[s]))
        return 0

    if not dropped:
        os.makedirs(INCOMING, exist_ok=True)
        print("Nothing to do: no usable photos in assets/incoming/.")
        print("Drop photos there named after the slot, e.g. crew-group.jpg, then re-run.")
        print("Run with --check to see which slots are still waiting.")
        return 0

    try:
        import PIL  # noqa: F401
    except ImportError:
        print("Pillow is required:  pip install Pillow", file=sys.stderr)
        return 1

    os.makedirs(IMAGES, exist_ok=True)
    results, changed = [], 0
    for slot in sorted(dropped):
        src, gravity = dropped[slot]
        try:
            r = process(slot, src, gravity)
        except Exception as e:                       # a bad file should not stop the batch
            print("  ! %s: could not read (%s)" % (os.path.basename(src), e))
            continue
        results.append(r)
        html, ok = switch_to_photo(html, slot)
        changed += ok

    if results:
        html = update_banner(html, current_state(html))
        open(INDEX, "w", encoding="utf-8").write(html)

    print("%-26s %-11s %-11s %8s %8s" % ("slot", "source", "output", "jpg", "webp"))
    for r in results:
        print("%-26s %-11s %-11s %7.0fK %8s%s" % (
            r["slot"], "%dx%d" % r["from"], "%dx%d" % r["to"], r["jpg_kb"],
            "%.0fK" % r["webp_kb"] if r["webp"] else "-",
            "  (soft)" if r["soft"] else ""))
    print("\n%d photo(s) processed, %d slot(s) switched in index.html." % (len(results), changed))
    left = sum(1 for s in SLOTS if current_state(html)[s] != "photo")
    print("%d slot(s) still on placeholder illustrations." % left)
    if left:
        print("Run with --check to list them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
