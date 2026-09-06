#!/usr/bin/env python3
"""
Special Green - placeholder illustration generator.

WHAT THESE ARE
    Stylised vector illustrations for the staging build. They are drawn shapes,
    not photographs, and they are deliberately graphic so that nobody mistakes
    them for a record of work the company actually performed.

WHAT THESE ARE NOT
    A substitute for photography. assets/README.md and docs/PHOTO-CHECKLIST.md
    still stand: the production site ships real Special Green photographs. Drop
    a real file over the matching filename and it wins. Delete this whole folder
    once the photography lands.

Every scene is composed against the slot it lands in: the CSS veils darken the
bottom of cards, the left of the commercial and customer bands, and everything
under the footer form, so the subject sits where it will still be visible.

    python3 tools/make-placeholder-art.py
"""

import math
import os
import random
import zlib

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "images")

# ---------------------------------------------------------------- palette ----
# Pulled from the :root custom properties in index.html so the art and the
# interface share one set of greens and one orange.
INK      = "#040705"
DEEP     = "#08110B"
FOREST   = "#0E1A12"
TURF_FAR = "#16301C"
TURF     = "#20502A"
TURF_LIT = "#357F35"
FRESH    = "#6FBF3F"
GREEN    = "#3E8E28"
ORANGE   = "#F26B21"
HOT      = "#FF7C2E"
DEEPO    = "#C9500F"
AMBER    = "#FFC46A"
BONE     = "#D8DCCF"
SOIL     = "#3A2317"
MULCH    = "#4A2A18"
STONE    = "#6E6A61"
WATER    = "#7FB6C9"
PLANT    = "#2C6B2E"        # shrub/foliage mass, light enough to read as a plant
PLANT_D  = "#1E4A22"        # the same one step back


def _rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def mix(a, b, t):
    """Blend two hex colours. t=0 gives a, t=1 gives b."""
    ra, ga, ba = _rgb(a)
    rb, gb, bb = _rgb(b)
    return "#%02X%02X%02X" % (
        round(ra + (rb - ra) * t),
        round(ga + (gb - ga) * t),
        round(ba + (bb - ba) * t),
    )


def f(v):
    """Trim floats so the files stay small and diffs stay readable."""
    return ("%.1f" % v).rstrip("0").rstrip(".")


# ----------------------------------------------------------------- canvas ----
class Art:
    def __init__(self, name, w, h):
        self.name = name
        self.w = w
        self.h = h
        # crc32 rather than hash(): hash() is salted per process, which would
        # make every run produce a different picture.
        self.rng = random.Random(zlib.crc32(name.encode()))
        self.defs = []
        self.body = []
        self._n = 0

    def uid(self, prefix):
        self._n += 1
        return "%s-%s%d" % (self.name, prefix, self._n)

    @staticmethod
    def _stops(stops):
        out = []
        for s in stops:
            off, col = s[0], s[1]
            op = s[2] if len(s) > 2 else 1
            out.append('<stop offset="%s" stop-color="%s" stop-opacity="%s"/>' % (f(off), col, f(op)))
        return "".join(out)

    def lg(self, x1, y1, x2, y2, stops):
        i = self.uid("l")
        self.defs.append(
            '<linearGradient id="%s" gradientUnits="userSpaceOnUse" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'
            % (i, f(x1), f(y1), f(x2), f(y2), self._stops(stops))
        )
        return "url(#%s)" % i

    def rg(self, cx, cy, r, stops, ry=None):
        i = self.uid("r")
        tf = ""
        if ry is not None and r:
            tf = ' gradientTransform="translate(%s %s) scale(1 %s) translate(%s %s)"' % (
                f(cx), f(cy), f(ry / r), f(-cx), f(-cy))
        self.defs.append(
            '<radialGradient id="%s" gradientUnits="userSpaceOnUse" cx="%s" cy="%s" r="%s"%s>%s</radialGradient>'
            % (i, f(cx), f(cy), f(r), tf, self._stops(stops))
        )
        return "url(#%s)" % i

    def clip_rect(self):
        i = self.uid("c")
        self.defs.append('<clipPath id="%s"><rect width="%s" height="%s"/></clipPath>' % (i, f(self.w), f(self.h)))
        return i

    def add(self, s):
        self.body.append(s)

    def rect(self, x, y, w, h, fill, op=None):
        o = '' if op is None else ' opacity="%s"' % f(op)
        self.add('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s/>' % (f(x), f(y), f(w), f(h), fill, o))

    def poly(self, pts, fill, op=None):
        o = '' if op is None else ' opacity="%s"' % f(op)
        d = " ".join("%s,%s" % (f(x), f(y)) for x, y in pts)
        self.add('<polygon points="%s" fill="%s"%s/>' % (d, fill, o))

    def path(self, d, fill="none", stroke=None, sw=None, op=None, cap="round"):
        s = ""
        if stroke:
            s = ' stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"' % (
                stroke, f(sw or 1), cap)
        o = '' if op is None else ' opacity="%s"' % f(op)
        self.add('<path d="%s" fill="%s"%s%s/>' % (d, fill, s, o))

    def ell(self, cx, cy, rx, ry, fill, op=None):
        o = '' if op is None else ' opacity="%s"' % f(op)
        self.add('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s/>' % (
            f(cx), f(cy), f(rx), f(ry), fill, o))

    def render(self):
        return (
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" '
            'preserveAspectRatio="xMidYMid slice" role="img">'
            "<defs>%s</defs>%s</svg>"
        ) % (self.w, self.h, self.w, self.h, "".join(self.defs), "".join(self.body))


# ------------------------------------------------------------- primitives ----
def sky(a, hy, top=None, horizon=None, warm=True):
    """Graded sky from the top of the frame down to the horizon line."""
    top = top or ("#0C1A22" if warm else "#132029")
    horizon = horizon or ("#C4762B" if warm else "#93A48C")
    a.rect(0, 0, a.w, hy + 2, a.lg(0, 0, 0, hy, [
        (0, top), (0.42, mix(top, horizon, .26)), (0.74, mix(top, horizon, .62)), (1, horizon)]))


def sun(a, x, y, r, core=AMBER, glow=None, strength=.9):
    """Low sun plus the bloom around it. Radial gradients, no blur filters."""
    glow = glow or ORANGE
    a.ell(x, y, r * 3.4, r * 2.2, a.rg(x, y, r * 3.4, [
        (0, glow, .55 * strength), (.45, glow, .18 * strength), (1, glow, 0)], ry=r * 2.2))
    a.ell(x, y, r, r * .92, a.rg(x, y, r, [
        (0, "#FFF0CE", strength), (.55, core, .85 * strength), (1, core, 0)], ry=r * .92))


def haze(a, hy, col=AMBER, depth=.24, spread=.16):
    """Warm band sitting on the horizon; sells distance more than anything else."""
    band = a.h * spread
    a.rect(0, hy - band, a.w, band * 1.6, a.lg(0, hy - band, 0, hy + band * .6, [
        (0, col, 0), (.65, col, depth), (1, col, 0)]))


def treeline(a, y, height, col, count=None, spread=1.25, density=1.0):
    """A ragged band of individual trees, drawn as one silhouette.

    Built tree by tree rather than as a wave, otherwise the horizon reads as a
    row of hills. Baton Rouge mix: mostly broad canopies, a few tall narrow ones.
    """
    rng = a.rng
    # Spacing is deliberately tighter than the canopy width so neighbouring
    # crowns overlap into one ragged mass. Spaced-out crowns on visible trunks
    # read as lollipops, which is what a distant tree line never looks like.
    step = (a.w / 15.0) / max(.4, density)
    a.rect(-a.w * .2, y, a.w * 1.4, height * .38 + 2, col)
    x = -a.w * .1
    while x < a.w * 1.1:
        tall = rng.random() < .18
        h = height * ((1.2 + rng.random() * .45) if tall else (.62 + rng.random() * .62))
        rx = step * ((.26 + rng.random() * .12) if tall else (.5 + rng.random() * .34))
        top = y - h
        if tall:
            a.path("M %s %s L %s %s L %s %s Z" % (
                f(x - rx * .1), f(y + height * .3), f(x), f(top),
                f(x + rx * .1), f(y + height * .3)), fill=col)
            for i in range(4):
                t = i / 3.0
                a.ell(x, top + h * (.16 + t * .26), rx * (1 - t * .22), h * .16, col)
        else:
            # irregular crown: a handful of round lobes, jittered off centre
            for _ in range(5):
                ox = (rng.random() - .5) * rx * 1.15
                oy = (rng.random() - .5) * h * .3
                a.ell(x + ox, top + h * .46 + oy,
                      rx * (.46 + rng.random() * .26), h * (.3 + rng.random() * .16), col)
            # short trunk, mostly buried in the base band
            a.rect(x - rx * .07, top + h * .6, rx * .14, h * .45, col)
        x += step * (.42 + rng.random() * .4)


def oak(a, x, ybase, h, col, spread=1.5):
    """Broad live-oak silhouette: wide canopy, low limbs, short trunk."""
    tw = h * .055
    a.path("M %s %s L %s %s L %s %s L %s %s Z" % (
        f(x - tw), f(ybase), f(x - tw * .55), f(ybase - h * .52),
        f(x + tw * .55), f(ybase - h * .52), f(x + tw), f(ybase)), fill=col)
    cy = ybase - h * .66
    rx = h * .5 * spread
    for i in range(7):
        ang = math.pi * (i / 6.0)
        ox = math.cos(ang) * rx * .72
        oy = -abs(math.sin(ang)) * h * .17
        a.ell(x + ox, cy + oy, rx * (.42 + a.rng.random() * .2), h * (.17 + a.rng.random() * .09), col)
    a.ell(x, cy + h * .06, rx * .86, h * .2, col)
    # a couple of low limbs reaching sideways, which is what makes it read as oak
    for s in (-1, 1):
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(ybase - h * .45), f(x + s * rx * .5), f(ybase - h * .62),
            f(x + s * rx * .92), f(ybase - h * .46)),
            stroke=col, sw=h * .022, op=.9)


def turf(a, hy, vx=None, n=15, near=TURF, far=TURF_FAR, lit=TURF_LIT, stripes=True, warm_from=None):
    """Ground plane from the horizon down, with mowing stripes in perspective."""
    vx = a.w * .5 if vx is None else vx
    ground = a.h - hy
    a.rect(0, hy, a.w, ground + 2, a.lg(0, hy, 0, a.h, [
        (0, far), (.3, mix(far, near, .6)), (1, near)]))
    if stripes:
        # k is how far the stripes still spread at the horizon. Pinching them to
        # a point (k near 0) turns the lawn into a sunburst, so keep it open.
        k = .58
        left, right = -a.w * .25, a.w * 1.25
        edges = [left + (right - left) * (i / float(n)) for i in range(n + 1)]
        for i in range(n):
            x0, x1 = edges[i], edges[i + 1]
            if i % 2:
                continue                                  # only draw the light pass
            a.poly([
                (x0, a.h), (x1, a.h),
                (vx + (x1 - vx) * k, hy), (vx + (x0 - vx) * k, hy)
            ], lit, op=.13)
        # fade them out toward the horizon so the mown pattern stays subtle
        a.rect(0, hy, a.w, ground, a.lg(0, hy, 0, a.h, [
            (0, far, .96), (.28, far, .5), (.7, far, .08), (1, far, 0)]))
    if warm_from is not None:
        a.rect(0, hy, a.w, ground, a.lg(warm_from, hy, warm_from + a.w * .8, a.h, [
            (0, AMBER, .2), (1, AMBER, 0)]))
    # foreground falloff keeps the bottom edge from competing with the copy
    a.rect(0, a.h * .55, a.w, a.h * .45, a.lg(0, a.h * .55, 0, a.h, [(0, INK, 0), (1, INK, .32)]))


def person(a, x, ybase, h, shirt=ORANGE, dark="#0A0F0B", flip=False, pose="stand", cap=True):
    """Crew silhouette.

    Proportioned off a real figure (head is about 1/7.5 of standing height)
    rather than eyeballed, because a wide torso on a small head reads as a
    traffic cone. The orange shirt is the brand cue and carries the colour.
    """
    s = -1 if flip else 1
    hr = h * .055                                     # head radius
    sy = ybase - h * .845                             # shoulder line
    wy = ybase - h * .52                              # waist
    sw_ = h * .076                                    # half shoulder width
    ww = h * .054                                     # half waist width
    # legs first so the shirt overlaps them. Hips carry near the shoulder width
    # or the figure reads as a torso on stilts.
    hipw = ww * 1.18
    a.path("M %s %s L %s %s L %s %s L %s %s L %s %s L %s %s L %s %s Z" % (
        f(x - hipw), f(wy), f(x + hipw), f(wy),
        f(x + ww * .8), f(ybase), f(x + ww * .22), f(ybase),
        f(x), f(ybase - h * .16),
        f(x - ww * .22), f(ybase), f(x - ww * .8), f(ybase)), fill=dark)
    # head and neck
    a.rect(x - hr * .42, ybase - h * .87, hr * .84, h * .04, dark)
    a.ell(x, ybase - h * .925, hr, hr * 1.08, dark)
    if cap:
        a.ell(x, ybase - h * .952, hr * 1.04, hr * .6, dark)          # crown
        a.ell(x + s * hr * 1.05, ybase - h * .943, hr * .8, hr * .2, dark)  # bill
    # torso: shoulders taper to waist
    a.path("M %s %s Q %s %s %s %s L %s %s L %s %s Z" % (
        f(x - sw_), f(sy), f(x), f(sy - h * .028), f(x + sw_), f(sy),
        f(x + ww), f(wy), f(x - ww), f(wy)), fill=shirt)
    # arms
    if pose == "work":
        # both arms forward and down, holding something
        a.path("M %s %s Q %s %s %s %s" % (
            f(x + s * sw_ * .85), f(sy + h * .02),
            f(x + s * h * .13), f(ybase - h * .68), f(x + s * h * .17), f(ybase - h * .56)),
            stroke=shirt, sw=h * .046)
        a.path("M %s %s Q %s %s %s %s" % (
            f(x - s * sw_ * .8), f(sy + h * .03),
            f(x - s * h * .04), f(ybase - h * .66), f(x + s * h * .06), f(ybase - h * .58)),
            stroke=shirt, sw=h * .042)
    elif pose == "lift":
        for d in (1, -1):
            a.path("M %s %s Q %s %s %s %s" % (
                f(x + d * sw_ * .85), f(sy + h * .02),
                f(x + d * h * .12), f(ybase - h * .76), f(x + d * h * .1), f(ybase - h * .66)),
                stroke=shirt, sw=h * .044)
    else:
        # Arms hang just outside the tapering torso. Drawn inside its outline
        # they merge into one mass and the figure reads as a capsule.
        for d in (1, -1):
            a.path("M %s %s L %s %s" % (
                f(x + d * sw_ * .82), f(sy + h * .035),
                f(x + d * sw_ * 1.12), f(wy + h * .05)),
                stroke=shirt, sw=h * .036)
    # rim light on the sun side so the silhouette separates from a dark treeline
    a.path("M %s %s L %s %s" % (
        f(x + s * sw_ * .92), f(sy + h * .04), f(x + s * (ww + h * .006)), f(wy - h * .01)),
        stroke=AMBER, sw=h * .011, op=.4)


def truck(a, x, ybase, w, body="#111A14", accent=None):
    """Pickup silhouette, optionally with an equipment trailer behind it."""
    h = w * .42
    a.rect(x, ybase - h * .62, w * .58, h * .62, body)                    # bed
    a.path("M %s %s L %s %s Q %s %s %s %s L %s %s Z" % (
        f(x + w * .55), f(ybase - h * .62),
        f(x + w * .62), f(ybase - h * 1.02),
        f(x + w * .86), f(ybase - h * 1.06), f(x + w * .93), f(ybase - h * .66),
        f(x + w * .99), f(ybase - h * .62)), fill=body)                   # cab
    a.rect(x + w * .55, ybase - h * .66, w * .45, h * .66, body)
    if accent:
        a.rect(x, ybase - h * .46, w, h * .1, accent, op=.85)
    for cx in (x + w * .2, x + w * .82):
        a.ell(cx, ybase, w * .1, w * .1, "#050806")
        a.ell(cx, ybase, w * .055, w * .055, mix(body, BONE, .18))


def trailer(a, x, ybase, w, body="#0E1610", loaded=True):
    """Open equipment trailer with mowers on the deck.

    An empty rail frame reads as a garden fence, so the deck carries machines.
    """
    h = w * .34
    deck = ybase - h * .3
    if loaded:
        for i, (ox, sc) in enumerate(((.1, 1.0), (.46, .92))):
            mw = w * .3 * sc
            mx = x + w * ox
            a.rect(mx, deck - h * .46 * sc, mw, h * .3 * sc, mix(body, BONE, .1))
            a.rect(mx + mw * .18, deck - h * .66 * sc, mw * .34, h * .22 * sc, body)
            for cx in (mx + mw * .16, mx + mw * .82):
                a.ell(cx, deck - h * .1 * sc, mw * .12, mw * .12, "#050806")
    a.rect(x, deck, w, h * .16, body)                        # deck
    a.rect(x, deck - h * .12, w, h * .05, body, op=.85)      # side rail
    a.path("M %s %s L %s %s" % (f(x + w), f(deck + h * .08), f(x + w * 1.14), f(ybase - h * .02)),
           stroke=body, sw=w * .018)                          # tongue
    for cx in (x + w * .28, x + w * .72):
        a.ell(cx, ybase, w * .062, w * .062, "#050806")
        a.ell(cx, ybase, w * .03, w * .03, mix(body, BONE, .16))


def shrub(a, x, ybase, r, col, lit=None, lobes=5):
    """Rounded shrub. Solid mass first, then a highlight sitting inside it -
    a highlight drawn above the mass leaves a ring that reads as a tyre."""
    a.ell(x, ybase - r * .5, r * .92, r * .55, col)
    for i in range(lobes):
        ang = math.pi * (i / float(lobes - 1))
        a.ell(x + math.cos(ang) * r * .5, ybase - r * .6 - abs(math.sin(ang)) * r * .22,
              r * .44, r * .38, col)
    if lit:
        a.ell(x - r * .16, ybase - r * .74, r * .34, r * .17, lit, op=.34)


def bed(a, pts, fill=MULCH, edge=None):
    """Planting bed as a filled polygon with an optional bright cut edge."""
    a.poly(pts, fill)
    if edge:
        d = "M " + " L ".join("%s %s" % (f(x), f(y)) for x, y in pts[:2])
        a.path(d, stroke=edge, sw=max(2, a.w * .0035), op=.75)


def spray(a, x, y, r, direction=1, col=None, arcs=7):
    """Irrigation fan: nested arcs plus droplets catching the light."""
    col = col or WATER
    for i in range(arcs):
        t = (i + 1) / float(arcs)
        rr = r * t
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(y),
            f(x + direction * rr * .62), f(y - rr * .92),
            f(x + direction * rr * 1.35), f(y + r * .1)),
            stroke=col, sw=max(1.2, r * .012), op=.32 - t * .16)
    for _ in range(int(r / 9)):
        t = a.rng.random()
        rr = r * (.25 + a.rng.random() * .95)
        px = x + direction * rr * (.2 + t * 1.1)
        py = y - rr * .8 * math.sin(math.pi * t) + a.rng.random() * r * .12
        a.ell(px, py, max(1.1, r * .009), max(1.1, r * .009), mix(col, "#FFFFFF", .5),
              op=.25 + a.rng.random() * .5)


def lamp(a, x, y, r, col=AMBER, strength=.75):
    a.ell(x, y, r * 3.2, r * 3.2, a.rg(x, y, r * 3.2, [
        (0, col, .5 * strength), (.4, col, .16 * strength), (1, col, 0)]))
    a.ell(x, y, r * .5, r * .5, mix(col, "#FFFFFF", .55), op=strength)


def paver_deck(a, x0, y0, x1, y1, cols=7, rows=5, col=None, line=None):
    """Patio in rough perspective: a trapezoid with a grid drawn over it."""
    col = col or mix(STONE, INK, .42)
    line = line or mix(STONE, BONE, .3)
    top_in = (x1 - x0) * .18
    quad = [(x0, y1), (x1, y1), (x1 - top_in, y0), (x0 + top_in, y0)]
    a.poly(quad, col)
    a.poly(quad, a.lg(0, y0, 0, y1, [(0, AMBER, .16), (1, INK, .1)]))
    for i in range(1, cols):
        t = i / float(cols)
        a.path("M %s %s L %s %s" % (
            f(x0 + (x1 - x0) * t), f(y1),
            f(x0 + top_in + (x1 - x0 - top_in * 2) * t), f(y0)),
            stroke=line, sw=max(1, a.w * .0012), op=.2)
    for j in range(1, rows):
        t = (j / float(rows)) ** 1.5
        yy = y0 + (y1 - y0) * t
        ins = top_in * (1 - t)
        a.path("M %s %s L %s %s" % (f(x0 + ins), f(yy), f(x1 - ins), f(yy)),
               stroke=line, sw=max(1, a.w * .0012), op=.18)


def vignette(a, strength=.5):
    a.rect(0, 0, a.w, a.h, a.rg(a.w * .5, a.h * .42, max(a.w, a.h) * .78, [
        (.35, INK, 0), (1, INK, strength)], ry=max(a.w, a.h) * .68))


def patch_ground(a, hy, base, dirt, count=26):
    """Tired turf: mottled bare patches. Used only for the 'before' frames."""
    a.rect(0, hy, a.w, a.h - hy, a.lg(0, hy, 0, a.h, [
        (0, mix(base, INK, .35)), (1, base)]))
    for _ in range(count):
        px = a.rng.random() * a.w
        t = a.rng.random()
        py = hy + (a.h - hy) * (t ** .7)
        rx = (a.w * .03 + a.rng.random() * a.w * .11) * (.4 + t)
        a.ell(px, py, rx, rx * (.26 + a.rng.random() * .16),
              mix(dirt, base, a.rng.random() * .5), op=.3 + a.rng.random() * .4)


def weeds(a, y0, y1, count, col, hmax):
    for _ in range(count):
        x = a.rng.random() * a.w
        y = y0 + (y1 - y0) * a.rng.random()
        h = hmax * (.4 + a.rng.random() * .9)
        lean = (a.rng.random() - .5) * h * .7
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(y), f(x + lean * .4), f(y - h * .6), f(x + lean), f(y - h)),
            stroke=col, sw=max(1, hmax * .07), op=.35 + a.rng.random() * .4)


# ----------------------------------------------------------------- scenes ----
def s_hero(a):
    """Wide dusk outdoor-living scene. Copy sits lower-left, badge upper-right."""
    hy = a.h * .53
    sky(a, hy, top="#0A1822", horizon="#D07C2C")
    sun(a, a.w * .68, hy * .93, a.h * .085)
    haze(a, hy, depth=.3)
    treeline(a, hy - a.h * .015, a.h * .16, mix(FOREST, INK, .45), spread=1.35)
    treeline(a, hy + a.h * .01, a.h * .1, INK, spread=1.1)
    turf(a, hy, vx=a.w * .62, n=17, warm_from=a.w * .55)
    # pergola and patio, right of centre where the hero copy will not cover it
    px0, px1 = a.w * .48, a.w * .93
    py0, py1 = hy + a.h * .04, a.h * .84
    paver_deck(a, px0, py0, px1, py1, cols=8, rows=6)
    post = a.h * .3
    for bx in (px0 + a.w * .03, px1 - a.w * .04):
        a.rect(bx, py0 - post, a.w * .012, post, mix(FOREST, INK, .5))
    a.rect(px0 + a.w * .02, py0 - post, (px1 - px0) - a.w * .04, a.h * .018, mix(FOREST, INK, .55))
    for i in range(7):
        bx = px0 + a.w * .04 + i * ((px1 - px0) - a.w * .09) / 6.0
        a.rect(bx, py0 - post + a.h * .016, a.w * .007, a.h * .03, mix(FOREST, INK, .4), op=.9)
    for i in range(4):
        lamp(a, px0 + a.w * .06 + i * (px1 - px0 - a.w * .12) / 3.0, py0 - post + a.h * .035, a.h * .012)
    for i in range(3):
        lamp(a, a.w * (.12 + i * .11), hy + a.h * .1 + i * a.h * .04, a.h * .009, strength=.55)
    shrub(a, a.w * .06, a.h * .82, a.h * .12, PLANT, lit=GREEN)
    shrub(a, a.w * .2, a.h * .93, a.h * .15, PLANT)
    vignette(a, .45)


def s_cta(a):
    """Footer band. Gets buried under the form, so keep it simple and graphic."""
    hy = a.h * .62
    sky(a, hy, top="#120C14", horizon="#E08630")
    sun(a, a.w * .5, hy * .95, a.h * .1, strength=1)
    haze(a, hy, depth=.34)
    treeline(a, hy, a.h * .14, INK, density=.85)
    turf(a, hy, vx=a.w * .5, n=11, near=mix(TURF, INK, .35), lit=mix(TURF_LIT, INK, .2))
    for i, (x, hh, fl) in enumerate(((.34, .26, False), (.43, .29, False), (.56, .27, True))):
        person(a, a.w * x, a.h * (.86 + i * .015), a.h * hh,
               shirt=mix(ORANGE, INK, .08), flip=fl, pose="work" if i == 1 else "stand")
    truck(a, a.w * .68, a.h * .86, a.w * .19)
    vignette(a, .55)


def s_commercial(a):
    """Trucks on a commercial property. Veil eats the left, so load the right."""
    hy = a.h * .56
    sky(a, hy, top="#16232E", horizon="#C9BE96", warm=False)
    sun(a, a.w * .8, hy * .8, a.h * .06, core="#FFF3D2", glow="#F5D89A", strength=.75)
    haze(a, hy, col="#E4DDBE", depth=.26)
    treeline(a, hy - a.h * .01, a.h * .11, mix(FOREST, "#22303A", .35), spread=1.3)
    # low commercial building on the skyline
    a.rect(a.w * .06, hy - a.h * .13, a.w * .3, a.h * .13, mix(FOREST, INK, .55))
    for i in range(9):
        a.rect(a.w * (.08 + i * .031), hy - a.h * .1, a.w * .016, a.h * .045,
               mix("#C9BE96", INK, .4), op=.55)
    turf(a, hy, vx=a.w * .35, n=15, near=mix(TURF, "#22303A", .18), lit=mix(TURF_LIT, BONE, .1))
    truck(a, a.w * .55, a.h * .82, a.w * .2, accent=DEEPO)
    trailer(a, a.w * .77, a.h * .82, a.w * .18)
    for x, hh, fl in ((.5, .15, False), (.62, .155, True), (.72, .145, False)):
        person(a, a.w * x, a.h * .84, a.h * hh, flip=fl, pose="work")
    vignette(a, .4)


def s_customer(a):
    """Homeowner and crew leader. Quote sits far left, so subjects go right."""
    hy = a.h * .55
    sky(a, hy, top="#0C1A20", horizon="#D08A3A")
    sun(a, a.w * .82, hy * .88, a.h * .075)
    haze(a, hy, depth=.28)
    treeline(a, hy, a.h * .14, mix(FOREST, INK, .5), spread=1.2)
    turf(a, hy, vx=a.w * .7, n=15, warm_from=a.w * .6)
    bed(a, [(a.w * .5, a.h * .78), (a.w * 1.02, a.h * .72),
            (a.w * 1.02, a.h * .62), (a.w * .56, a.h * .68)], edge=mix(FRESH, BONE, .3))
    for i in range(5):
        shrub(a, a.w * (.6 + i * .09), a.h * (.72 - i * .012), a.h * .07,
              PLANT, lit=GREEN)
    person(a, a.w * .63, a.h * .88, a.h * .3, shirt=ORANGE, pose="work")
    person(a, a.w * .74, a.h * .88, a.h * .29, shirt=mix(BONE, "#8FA0A6", .4), flip=True)
    for i in range(3):
        lamp(a, a.w * (.55 + i * .14), a.h * .74, a.h * .011, strength=.6)
    vignette(a, .42)


def s_crew_portrait(a):
    """Vertical. Two crew mid-work, tight enough that the orange dominates."""
    hy = a.h * .46
    sky(a, hy, top="#0B1820", horizon="#C97C2E")
    sun(a, a.w * .28, hy * .9, a.w * .13)
    haze(a, hy, depth=.3, spread=.12)
    treeline(a, hy, a.h * .1, mix(FOREST, INK, .45), spread=1.4)
    turf(a, hy, vx=a.w * .4, n=11)
    person(a, a.w * .38, a.h * .95, a.h * .55, shirt=ORANGE, pose="work")
    person(a, a.w * .66, a.h * .92, a.h * .48, shirt=HOT, flip=True)
    a.path("M %s %s L %s %s" % (f(a.w * .46), f(a.h * .72), f(a.w * .3), f(a.h * .88)),
           stroke=mix(BONE, INK, .5), sw=a.w * .014)
    vignette(a, .45)


def s_crew_group(a):
    """Full team in front of the trucks.

    Horizon sits low on purpose: the crew then breaks the bright sky band, so
    heads, caps and legs read as silhouette instead of dark-on-dark turf.
    """
    hy = a.h * .6
    sky(a, hy, top="#0A1822", horizon="#D08637")
    sun(a, a.w * .5, hy * .93, a.h * .075)
    haze(a, hy, depth=.32)
    treeline(a, hy, a.h * .15, INK, density=.9)
    turf(a, hy, vx=a.w * .5, n=11)
    truck(a, a.w * .0, a.h * .82, a.w * .3, accent=DEEPO)
    trailer(a, a.w * .68, a.h * .82, a.w * .34)
    for i in range(6):
        x = .17 + i * .125
        person(a, a.w * x, a.h * (.93 + (i % 2) * .012), a.h * (.33 + (i % 3) * .022),
               shirt=ORANGE if i % 2 == 0 else HOT, flip=i % 3 == 0)
    vignette(a, .42)


def s_crew_trimmer(a):
    """Square, tight crop: sleeve, trimmer shaft, cut arc, grass throw."""
    hy = a.h * .3
    sky(a, hy, top="#0D1C16", horizon="#B4762F")
    haze(a, hy, depth=.24, spread=.2)
    turf(a, hy, vx=a.w * .5, n=9, stripes=False, near=mix(TURF, INK, .1))
    # dense upright blades; long sparse diagonals read as rain, not turf
    for _ in range(260):
        x = a.rng.random() * a.w
        y = hy + (a.h - hy) * (a.rng.random() ** .5)
        bh = a.h * (.012 + a.rng.random() * .026) * (.5 + (y - hy) / (a.h - hy))
        lean = (a.rng.random() - .5) * bh * .5
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(y), f(x + lean * .4), f(y - bh * .6), f(x + lean), f(y - bh)),
            stroke=mix(GREEN, INK, a.rng.random() * .55), sw=a.w * .0035,
            op=.3 + a.rng.random() * .35)
    # trimmer shaft running corner to corner
    a.path("M %s %s L %s %s" % (f(a.w * .1), f(a.h * .14), f(a.w * .74), f(a.h * .66)),
           stroke=mix(BONE, INK, .58), sw=a.w * .026)
    a.ell(a.w * .76, a.h * .68, a.w * .08, a.w * .03, mix(BONE, INK, .38))
    a.ell(a.w * .76, a.h * .68, a.w * .03, a.w * .022, mix(DEEPO, INK, .3))
    # cutting arc and grass throw
    a.path("M %s %s A %s %s 0 0 1 %s %s" % (
        f(a.w * .63), f(a.h * .8), f(a.w * .15), f(a.w * .15), f(a.w * .9), f(a.h * .64)),
        stroke=FRESH, sw=a.w * .01, op=.4)
    for _ in range(46):
        ang = a.rng.random() * math.pi
        rr = a.w * (.08 + a.rng.random() * .2)
        a.ell(a.w * .76 + math.cos(ang) * rr, a.h * .68 - abs(math.sin(ang)) * rr * .75,
              a.w * .005, a.w * .005, mix(FRESH, AMBER, a.rng.random() * .4),
              op=.25 + a.rng.random() * .5)
    # Forearm in an orange sleeve gripping the shaft. Drawn as a tapered
    # quad rather than a stroke: a constant-width stroke reads as a bar.
    a.poly([(-a.w * .06, a.h * .02), (a.w * .1, -a.h * .04),
            (a.w * .35, a.h * .3), (a.w * .27, a.h * .38)], ORANGE)
    a.poly([(a.w * .1, -a.h * .04), (a.w * .16, -a.h * .02),
            (a.w * .37, a.h * .29), (a.w * .35, a.h * .3)], mix(ORANGE, AMBER, .3), op=.5)
    a.poly([(a.w * .27, a.h * .38), (a.w * .35, a.h * .3),
            (a.w * .42, a.h * .36), (a.w * .35, a.h * .44)], mix("#2A2018", INK, .15))  # glove
    vignette(a, .4)


def s_crew_truck_load(a):
    """Square. Figure lifting equipment at the tailgate."""
    hy = a.h * .42
    sky(a, hy, top="#0B1620", horizon="#C07A34")
    sun(a, a.w * .78, hy * .82, a.w * .09)
    haze(a, hy, depth=.26, spread=.16)
    treeline(a, hy, a.h * .1, INK, spread=1.3)
    turf(a, hy, vx=a.w * .5, n=9, stripes=False)
    a.rect(0, a.h * .74, a.w, a.h * .26, mix(STONE, INK, .68))
    trailer(a, a.w * .04, a.h * .8, a.w * .62)
    person(a, a.w * .72, a.h * .82, a.h * .42, shirt=ORANGE, pose="work", flip=True)
    a.rect(a.w * .5, a.h * .58, a.w * .13, a.h * .1, mix(FOREST, INK, .3))
    a.ell(a.w * .565, a.h * .68, a.w * .075, a.w * .022, "#050806")
    for _ in range(30):
        a.ell(a.w * (.3 + a.rng.random() * .5), a.h * (.76 + a.rng.random() * .18),
              a.w * .01, a.w * .004, BONE, op=.05 + a.rng.random() * .1)
    vignette(a, .42)


def s_lawn_care(a):
    """Striped turf with a mower. Card veil kills the bottom, so keep it high."""
    hy = a.h * .38
    sky(a, hy, top="#0C1A20", horizon="#CE8433")
    sun(a, a.w * .24, hy * .86, a.h * .08)
    haze(a, hy, depth=.3)
    treeline(a, hy, a.h * .12, INK, spread=1.3)
    turf(a, hy, vx=a.w * .42, n=17, warm_from=a.w * .1)
    a.rect(a.w * .56, a.h * .48, a.w * .2, a.h * .1, mix(FOREST, INK, .35))
    a.rect(a.w * .58, a.h * .43, a.w * .1, a.h * .06, mix(FOREST, INK, .2))
    for cx in (a.w * .59, a.w * .73):
        a.ell(cx, a.h * .59, a.w * .028, a.w * .028, "#050806")
    person(a, a.w * .64, a.h * .48, a.h * .2, shirt=ORANGE, pose="work")
    vignette(a, .38)


def s_landscaping(a):
    """New bed install: mulch, fresh planting, sunset behind."""
    hy = a.h * .4
    sky(a, hy, top="#101822", horizon="#D8873A")
    sun(a, a.w * .7, hy * .84, a.h * .085)
    haze(a, hy, depth=.32)
    treeline(a, hy, a.h * .12, INK, spread=1.2)
    turf(a, hy, vx=a.w * .5, n=13, warm_from=a.w * .5)
    bed(a, [(a.w * -.05, a.h * .82), (a.w * 1.05, a.h * .7),
            (a.w * 1.05, a.h * .56), (a.w * -.05, a.h * .64)],
        edge=mix(FRESH, BONE, .35))
    for i in range(7):
        x = a.w * (.04 + i * .15)
        y = a.h * (.72 - i * .017)
        shrub(a, x, y, a.h * (.075 + (i % 3) * .015),
              PLANT, lit=FRESH if i % 2 == 0 else GREEN)
    for i in range(5):
        x = a.w * (.12 + i * .19)
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(a.h * .66), f(x - a.w * .02), f(a.h * .56), f(x + a.w * .01), f(a.h * .5)),
            stroke=mix(GREEN, BONE, .25), sw=a.w * .006, op=.7)
    vignette(a, .38)


def s_irrigation(a):
    """Heads running at golden hour, water catching the light."""
    hy = a.h * .36
    sky(a, hy, top="#0D1A24", horizon="#DE9440")
    sun(a, a.w * .18, hy * .8, a.h * .09)
    haze(a, hy, depth=.34)
    treeline(a, hy, a.h * .11, INK, spread=1.25)
    turf(a, hy, vx=a.w * .5, n=15, warm_from=a.w * .05)
    for i, (x, y, r, d) in enumerate((
            (.16, .72, .3, 1), (.46, .66, .24, 1), (.78, .78, .34, -1), (.62, .9, .3, 1))):
        spray(a, a.w * x, a.h * y, a.w * r, direction=d,
              col=mix(WATER, AMBER, .3 if i % 2 else .05))
        a.ell(a.w * x, a.h * y, a.w * .012, a.w * .006, mix(FOREST, INK, .2))
    vignette(a, .36)


def s_detail_edging(a):
    """Square. Hard diagonal between drive and turf, one crisp cut line."""
    a.rect(0, 0, a.w, a.h, mix(TURF, INK, .2))
    turf(a, 0, vx=a.w * .3, n=11, near=TURF, stripes=True)
    a.poly([(a.w * .52, 0), (a.w, 0), (a.w, a.h), (a.w * .16, a.h)],
           a.lg(a.w * .5, 0, a.w, a.h, [(0, mix(STONE, INK, .5)), (1, mix(STONE, INK, .72))]))
    a.path("M %s %s L %s %s" % (f(a.w * .52), 0, f(a.w * .16), f(a.h)),
           stroke=mix(SOIL, INK, .35), sw=a.w * .022)
    a.path("M %s %s L %s %s" % (f(a.w * .5), 0, f(a.w * .14), f(a.h)),
           stroke=FRESH, sw=a.w * .006, op=.55)
    for _ in range(40):
        t = a.rng.random()
        x = a.w * (.52 - .36 * t) - a.w * .02 - a.rng.random() * a.w * .04
        a.path("M %s %s L %s %s" % (
            f(x), f(a.h * t), f(x - a.w * .02), f(a.h * t - a.h * .03)),
            stroke=mix(FRESH, INK, a.rng.random() * .5), sw=a.w * .004, op=.5)
    vignette(a, .35)


def s_detail_trimmer(a):
    """Same subject as the crew trimmer shot but a different frame, so the two
    do not read as the same picture used twice in one page."""
    hy = a.h * .24
    sky(a, hy, top="#0E1C18", horizon="#A97430")
    haze(a, hy, depth=.22, spread=.22)
    turf(a, hy, vx=a.w * .4, n=9, stripes=False, near=mix(TURF, INK, .06))
    bed(a, [(a.w * -.05, a.h * .64), (a.w * 1.05, a.h * .52),
            (a.w * 1.05, a.h * .4), (a.w * -.05, a.h * .5)], fill=mix(MULCH, INK, .3),
        edge=mix(FRESH, BONE, .3))
    for _ in range(80):
        x = a.rng.random() * a.w
        y = a.h * (.6 + a.rng.random() * .42)
        hh = a.h * (.03 + a.rng.random() * .07)
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(y), f(x - hh * .3), f(y - hh * .6), f(x - hh * .6), f(y - hh)),
            stroke=mix(GREEN, INK, a.rng.random() * .45), sw=a.w * .0045, op=.55)
    a.path("M %s %s L %s %s" % (f(a.w * .96), f(a.h * .12), f(a.w * .3), f(a.h * .6)),
           stroke=mix(BONE, INK, .58), sw=a.w * .024)
    a.ell(a.w * .28, a.h * .62, a.w * .075, a.w * .028, mix(BONE, INK, .38))
    for _ in range(40):
        ang = a.rng.random() * math.pi
        rr = a.w * (.06 + a.rng.random() * .17)
        a.ell(a.w * .28 - math.cos(ang) * rr, a.h * .62 - abs(math.sin(ang)) * rr * .7,
              a.w * .005, a.w * .005, FRESH, op=.25 + a.rng.random() * .45)
    a.path("M %s %s L %s %s" % (f(a.w * 1.04), f(a.h * .02), f(a.w * .78), f(a.h * .24)),
           stroke=ORANGE, sw=a.w * .1, cap="butt")
    a.ell(a.w * .75, a.h * .27, a.w * .045, a.w * .038, mix("#2A2018", INK, .2))
    vignette(a, .38)


def s_detail_blower(a):
    """Square. Clippings driven across a hard surface in an arc."""
    a.rect(0, 0, a.w, a.h, mix(STONE, INK, .66))
    a.rect(0, 0, a.w, a.h, a.lg(0, 0, a.w, a.h, [(0, AMBER, .12), (1, INK, .2)]))
    a.path("M %s %s L %s %s" % (f(a.w * .1), 0, f(a.w * .34), f(a.h)),
           stroke=mix(STONE, INK, .78), sw=a.w * .012, op=.7)
    a.poly([(0, a.h * .06), (a.w * .3, 0), (0, 0)], mix(TURF, INK, .25))
    a.path("M %s %s L %s %s" % (f(a.w * .74), f(a.h * .18), f(a.w * .34), f(a.h * .58)),
           stroke=mix(FOREST, INK, .2), sw=a.w * .035)
    a.ell(a.w * .32, a.h * .6, a.w * .07, a.w * .045, mix(FOREST, INK, .1))
    for _ in range(90):
        t = a.rng.random()
        ang = math.pi * (.08 + t * .5)
        rr = a.w * (.08 + a.rng.random() * .55)
        px = a.w * .32 - math.cos(ang) * rr
        py = a.h * .6 + math.sin(ang) * rr * .55 - a.w * .04
        a.ell(px, py, a.w * .006, a.w * .003, mix(FRESH, AMBER, a.rng.random() * .6),
              op=.2 + a.rng.random() * .55)
    a.path("M %s %s L %s %s L %s %s L %s %s Z" % (
        f(a.w * .72), f(a.h * .04), f(a.w * 1.02), f(a.h * .1),
        f(a.w * 1.02), f(a.h * .42), f(a.w * .78), f(a.h * .3)), fill=ORANGE)
    vignette(a, .38)


def s_detail_valve(a):
    """Square. Open valve box in dark soil with tools laid out."""
    a.rect(0, 0, a.w, a.h, mix(TURF, INK, .35))
    turf(a, 0, vx=a.w * .5, n=9, stripes=False, near=mix(TURF, INK, .28))
    a.ell(a.w * .5, a.h * .56, a.w * .42, a.h * .3, mix(SOIL, INK, .3))
    a.rect(a.w * .26, a.h * .38, a.w * .48, a.h * .34, mix("#2A2E28", INK, .3))
    a.rect(a.w * .29, a.h * .41, a.w * .42, a.h * .28, mix(SOIL, INK, .55))
    a.path("M %s %s L %s %s L %s %s" % (
        f(a.w * .34), f(a.h * .66), f(a.w * .38), f(a.h * .5), f(a.w * .58), f(a.h * .5)),
        stroke=mix(BONE, INK, .55), sw=a.w * .028)
    a.ell(a.w * .6, a.h * .5, a.w * .035, a.w * .035, mix(DEEPO, INK, .2))
    a.rect(a.w * .24, a.h * .78, a.w * .3, a.h * .03, mix(BONE, INK, .5))
    a.rect(a.w * .3, a.h * .84, a.w * .26, a.h * .025, mix(DEEPO, INK, .25))
    lamp(a, a.w * .52, a.h * .46, a.w * .02, col="#BFE0FF", strength=.35)
    for _ in range(24):
        a.ell(a.w * (.2 + a.rng.random() * .6), a.h * (.7 + a.rng.random() * .26),
              a.w * .012, a.w * .006, mix(SOIL, INK, a.rng.random() * .5), op=.5)
    vignette(a, .4)


def s_proj_patio(a):
    hy = a.h * .42
    sky(a, hy, top="#100C1A", horizon="#D97F33")
    sun(a, a.w * .3, hy * .9, a.h * .08)
    haze(a, hy, depth=.32)
    treeline(a, hy, a.h * .14, INK, spread=1.2)
    turf(a, hy, vx=a.w * .5, n=11)
    paver_deck(a, a.w * .1, a.h * .56, a.w * .95, a.h * .95, cols=7, rows=5)
    a.ell(a.w * .52, a.h * .68, a.w * .07, a.h * .03, mix(STONE, INK, .3))
    lamp(a, a.w * .52, a.h * .66, a.h * .035, col=HOT, strength=1)
    for x in (.24, .78):
        a.rect(a.w * x, a.h * .58, a.w * .1, a.h * .08, mix(FOREST, INK, .25))
        a.rect(a.w * x, a.h * .54, a.w * .1, a.h * .05, mix(FOREST, INK, .1))
    for i in range(4):
        lamp(a, a.w * (.16 + i * .23), a.h * .53, a.h * .014)
    shrub(a, a.w * .05, a.h * .62, a.h * .1, PLANT, lit=GREEN)
    vignette(a, .4)


def s_proj_front(a):
    hy = a.h * .44
    sky(a, hy, top="#0C1A22", horizon="#CE8C3E")
    sun(a, a.w * .84, hy * .84, a.h * .07)
    haze(a, hy, depth=.28)
    # house facade, straight on
    a.rect(a.w * .18, hy - a.h * .3, a.w * .64, a.h * .3, mix(FOREST, INK, .55))
    a.path("M %s %s L %s %s L %s %s Z" % (
        f(a.w * .14), f(hy - a.h * .3), f(a.w * .5), f(hy - a.h * .46),
        f(a.w * .86), f(hy - a.h * .3)), fill=mix(FOREST, INK, .68))
    for i in range(4):
        a.rect(a.w * (.24 + i * .15), hy - a.h * .24, a.w * .08, a.h * .1,
               mix(AMBER, INK, .45), op=.75)
    a.rect(a.w * .46, hy - a.h * .16, a.w * .08, a.h * .16, mix(SOIL, INK, .45))
    turf(a, hy, vx=a.w * .5, n=15, warm_from=a.w * .7)
    bed(a, [(a.w * .1, a.h * .74), (a.w * .9, a.h * .74),
            (a.w * .86, a.h * .62), (a.w * .14, a.h * .62)],
        edge=mix(FRESH, BONE, .3))
    for i in range(7):
        shrub(a, a.w * (.14 + i * .12), a.h * .71, a.h * .055,
              PLANT, lit=GREEN if i % 2 else None)
    vignette(a, .38)


def s_proj_irrigation(a):
    hy = a.h * .38
    sky(a, hy, top="#0D1A24", horizon="#D89442")
    sun(a, a.w * .74, hy * .82, a.h * .08)
    haze(a, hy, depth=.3)
    treeline(a, hy, a.h * .12, INK, spread=1.3)
    turf(a, hy, vx=a.w * .5, n=17, warm_from=a.w * .6)
    for i, (x, y, r, d) in enumerate((
            (.1, .66, .26, 1), (.36, .74, .3, 1), (.66, .68, .26, -1), (.9, .8, .28, -1))):
        spray(a, a.w * x, a.h * y, a.w * r, direction=d, col=mix(WATER, AMBER, .2))
    vignette(a, .36)


def s_proj_office(a):
    hy = a.h * .46
    sky(a, hy, top="#16232E", horizon="#BFC2A2", warm=False)
    sun(a, a.w * .2, hy * .78, a.h * .055, core="#FFF6DE", glow="#EBDCAE", strength=.6)
    haze(a, hy, col="#DCD8BC", depth=.24)
    a.rect(a.w * .32, hy - a.h * .34, a.w * .62, a.h * .34, mix(FOREST, INK, .5))
    for r in range(4):
        for c in range(9):
            a.rect(a.w * (.35 + c * .064), hy - a.h * (.3 - r * .075), a.w * .04, a.h * .045,
                   mix("#BFC2A2", INK, .45), op=.5)
    treeline(a, hy - a.h * .005, a.h * .09, mix(FOREST, "#22303A", .3), spread=1.4)
    turf(a, hy, vx=a.w * .45, n=15, near=mix(TURF, "#22303A", .12), lit=mix(TURF_LIT, BONE, .08))
    bed(a, [(a.w * -.05, a.h * .78), (a.w * 1.05, a.h * .66),
            (a.w * 1.05, a.h * .58), (a.w * -.05, a.h * .68)], edge=mix(FRESH, BONE, .4))
    for i in range(8):
        shrub(a, a.w * (.02 + i * .14), a.h * (.74 - i * .014), a.h * .05,
              PLANT, lit=GREEN if i % 2 else None)
    vignette(a, .36)


# --- before / after ----------------------------------------------------------
# Cropped square from centre by the CSS, so everything sits inside the middle.
def _ba_sky(a, hy, warm=True):
    """Identical sky either side of the pair.

    The section copy reads "same camera position, same time of day", so the
    before and after frames must share light. Only the ground changes.
    """
    sky(a, hy, top="#0E1A20", horizon="#C9853A")
    haze(a, hy, col=AMBER, depth=.2)
    treeline(a, hy, a.h * .1, mix(FOREST, INK, .5), spread=1.3)


def s_ba1_before(a):
    hy = a.h * .38
    _ba_sky(a, hy, warm=False)
    patch_ground(a, hy, mix(TURF, "#4A4A2E", .4), SOIL, count=30)
    weeds(a, a.h * .6, a.h, 60, mix("#6E7A46", INK, .2), a.h * .07)
    bed(a, [(a.w * .18, a.h * .78), (a.w * .84, a.h * .74),
            (a.w * .82, a.h * .64), (a.w * .2, a.h * .66)], fill=mix(SOIL, "#4A4A2E", .45))
    for i in range(5):
        shrub(a, a.w * (.24 + i * .14), a.h * (.74 - i * .008), a.h * (.05 + a.rng.random() * .05),
              mix("#3C4A2A", INK, .25))
    vignette(a, .42)


def s_ba1_after(a):
    hy = a.h * .38
    _ba_sky(a, hy)
    # lusher turf than the default: the pair has to read as a change
    turf(a, hy, vx=a.w * .5, n=15, warm_from=a.w * .3,
         near=mix(TURF, TURF_LIT, .34), lit=FRESH)
    bed(a, [(a.w * .18, a.h * .78), (a.w * .84, a.h * .74),
            (a.w * .82, a.h * .64), (a.w * .2, a.h * .66)], edge=mix(FRESH, BONE, .35))
    for i in range(5):
        shrub(a, a.w * (.24 + i * .14), a.h * .73, a.h * .06,
              PLANT, lit=FRESH if i % 2 == 0 else GREEN)
    vignette(a, .36)


def s_ba2_before(a):
    hy = a.h * .34
    _ba_sky(a, hy, warm=False)
    patch_ground(a, hy, mix(TURF, "#4A4A2E", .3), SOIL, count=22)
    bed(a, [(a.w * .1, a.h * .86), (a.w * .92, a.h * .8),
            (a.w * .88, a.h * .54), (a.w * .14, a.h * .58)],
        fill=mix(MULCH, "#4A4632", .55))
    weeds(a, a.h * .56, a.h * .86, 80, mix("#78864C", INK, .15), a.h * .1)
    for i in range(4):
        shrub(a, a.w * (.24 + i * .18), a.h * (.78 - i * .01), a.h * (.06 + a.rng.random() * .06),
              mix("#3C4A2A", INK, .2))
    vignette(a, .42)


def s_ba2_after(a):
    hy = a.h * .34
    _ba_sky(a, hy)
    turf(a, hy, vx=a.w * .5, n=13, near=mix(TURF, TURF_LIT, .34), lit=FRESH)
    bed(a, [(a.w * .1, a.h * .86), (a.w * .92, a.h * .8),
            (a.w * .88, a.h * .54), (a.w * .14, a.h * .58)],
        fill=MULCH, edge=mix(FRESH, BONE, .4))
    for i in range(6):
        shrub(a, a.w * (.19 + i * .13), a.h * (.76 - (i % 2) * .04), a.h * .06,
              PLANT, lit=FRESH if i % 2 == 0 else GREEN)
    for i in range(5):
        x = a.w * (.22 + i * .14)
        a.path("M %s %s Q %s %s %s %s" % (
            f(x), f(a.h * .62), f(x - a.w * .015), f(a.h * .54), f(x + a.w * .008), f(a.h * .48)),
            stroke=mix(GREEN, BONE, .3), sw=a.w * .005, op=.7)
    vignette(a, .36)


def s_ba3_before(a):
    hy = a.h * .36
    _ba_sky(a, hy, warm=False)
    patch_ground(a, hy, mix(TURF, SOIL, .5), SOIL, count=34)
    # standing water
    a.ell(a.w * .5, a.h * .8, a.w * .3, a.h * .1, mix(WATER, INK, .55), op=.8)
    a.ell(a.w * .5, a.h * .79, a.w * .26, a.h * .07, mix(WATER, "#9AA391", .4), op=.4)
    a.ell(a.w * .3, a.h * .92, a.w * .16, a.h * .05, mix(WATER, INK, .6), op=.7)
    weeds(a, a.h * .62, a.h, 40, mix("#6E7A46", INK, .3), a.h * .06)
    vignette(a, .44)


def s_ba3_after(a):
    hy = a.h * .36
    _ba_sky(a, hy)
    turf(a, hy, vx=a.w * .5, n=17, warm_from=a.w * .4,
         near=mix(TURF, TURF_LIT, .34), lit=FRESH)
    # a graded crown and a clean drain line where the water used to sit
    a.path("M %s %s Q %s %s %s %s" % (
        f(-a.w * .05), f(a.h * .82), f(a.w * .5), f(a.h * .72), f(a.w * 1.05), f(a.h * .82)),
        stroke=mix(TURF_LIT, BONE, .18), sw=a.w * .006, op=.4)
    a.ell(a.w * .74, a.h * .86, a.w * .035, a.h * .018, mix("#2A2E28", INK, .25))
    vignette(a, .36)


# --- mobile breaks (vertical, centre band is what shows) ---------------------
def s_mbreak1(a):
    hy = a.h * .5
    sky(a, hy, top="#0C1A20", horizon="#C98A3C")
    sun(a, a.w * .5, hy * .93, a.h * .05)
    haze(a, hy, depth=.28, spread=.1)
    turf(a, hy, vx=a.w * .5, n=13, warm_from=a.w * .3)
    oak(a, a.w * .26, hy + a.h * .03, a.h * .34, mix(FOREST, INK, .55), spread=1.7)
    oak(a, a.w * .78, hy + a.h * .05, a.h * .3, INK, spread=1.6)
    oak(a, a.w * .52, hy + a.h * .01, a.h * .22, mix(FOREST, INK, .35), spread=1.4)
    vignette(a, .4)


def s_mbreak2(a):
    hy = a.h * .48
    sky(a, hy, top="#0E1620", horizon="#D2853A")
    sun(a, a.w * .68, hy * .9, a.h * .05)
    haze(a, hy, depth=.3, spread=.1)
    treeline(a, hy, a.h * .12, INK, spread=1.3)
    turf(a, hy, vx=a.w * .5, n=11, warm_from=a.w * .5)
    bed(a, [(a.w * -.05, a.h * .72), (a.w * 1.05, a.h * .66),
            (a.w * 1.05, a.h * .58), (a.w * -.05, a.h * .62)], edge=mix(FRESH, BONE, .3))
    for i in range(5):
        shrub(a, a.w * (.05 + i * .23), a.h * .68, a.h * .05,
              PLANT, lit=GREEN if i % 2 else None)
    paver_deck(a, a.w * .1, a.h * .78, a.w * .92, a.h * .98, cols=5, rows=3)
    for i in range(3):
        lamp(a, a.w * (.2 + i * .3), a.h * .76, a.h * .012)
    vignette(a, .4)


# ------------------------------------------------------------------ table ----
SLOTS = [
    ("hero-outdoor-living",     2400, 1350, s_hero),
    ("crew-portrait",           1200, 1500, s_crew_portrait),
    ("crew-group",              1600, 1200, s_crew_group),
    ("crew-trimmer",            1200, 1200, s_crew_trimmer),
    ("crew-truck-load",         1200, 1200, s_crew_truck_load),
    ("commercial-crew-trucks",  2400, 1350, s_commercial),
    ("customer-crew-leader",    2400, 1350, s_customer),
    ("cta-sunset",              2400, 1350, s_cta),
    ("service-lawn-care",       1600, 1200, s_lawn_care),
    ("service-landscaping",     1600, 1200, s_landscaping),
    ("service-irrigation",      1600, 1200, s_irrigation),
    ("detail-edging",           1200, 1200, s_detail_edging),
    ("detail-trimmer",          1200, 1200, s_detail_trimmer),
    ("detail-blower",           1200, 1200, s_detail_blower),
    ("detail-irrigation-valve", 1200, 1200, s_detail_valve),
    ("project-patio-landscape", 1600, 1100, s_proj_patio),
    ("project-front-yard",      1600, 1100, s_proj_front),
    ("project-irrigation",      1600, 1100, s_proj_irrigation),
    ("project-office-park",     1600, 1100, s_proj_office),
    ("before-01-before",        1600, 1200, s_ba1_before),
    ("before-01-after",         1600, 1200, s_ba1_after),
    ("before-02-before",        1600, 1200, s_ba2_before),
    ("before-02-after",         1600, 1200, s_ba2_after),
    ("before-03-before",        1600, 1200, s_ba3_before),
    ("before-03-after",         1600, 1200, s_ba3_after),
    ("mobile-break-01",         1200, 1500, s_mbreak1),
    ("mobile-break-02",         1200, 1500, s_mbreak2),
]


def main():
    os.makedirs(OUT, exist_ok=True)
    total = 0
    for name, w, h, fn in SLOTS:
        a = Art(name, w, h)
        fn(a)
        svg = a.render()
        with open(os.path.join(OUT, name + ".svg"), "w") as fh:
            fh.write(svg)
        total += len(svg)
        print("%-26s %5dx%-5d %6.1f KB" % (name, w, h, len(svg) / 1024.0))
    print("\n%d files, %.1f KB total" % (len(SLOTS), total / 1024.0))


if __name__ == "__main__":
    main()
