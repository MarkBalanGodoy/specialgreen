# Photography drop folder

## How to put a photo on the site

Drop photos into **`assets/incoming/`**, named after the slot they belong to, then run one
command:

```
python3 tools/prepare-photos.py
```

That crops each photo to the right shape, resizes it, writes a JPEG and a WebP into
`assets/images/`, and switches that slot in `index.html` over to the photo. Slots with no
photo keep their placeholder. Commit and push and it is live.

The extension does not matter and neither does the size. Straight off a phone is fine.
Name it for the slot: `crew-group.jpg`, `hero-outdoor-living.jpg`, and so on, using the
names in the table below.

Useful flags:

```
python3 tools/prepare-photos.py --check    # which slots still need a photo
python3 tools/prepare-photos.py --revert   # put everything back on placeholders
```

Photos are cropped from the centre. If that cuts the wrong part off, add a hint to the
filename: `crew-group--top.jpg`, or `--bottom`, `--left`, `--right`.

> An earlier version of this file said to drop `.jpg` files into `assets/` and they would
> appear with no code changes. That was wrong on both counts. The page references `.svg`
> files in `assets/images/`, so photos dropped that way were silently ignored. Use the
> command above.

Until a photo exists, that slot shows a placeholder illustration from
`tools/make-placeholder-art.py`, so the page never looks broken while you are waiting on
photography.

**The placeholders are drawings, not photographs, and they do not satisfy anything below.**
They exist so the layout can be reviewed. They are deliberately graphic rather than
photorealistic so that nobody mistakes one for a record of a job the company did. Every one
of them gets replaced by a real photograph before launch, and the staging banner says so
until that happens. Regenerate them with `python3 tools/make-placeholder-art.py`; delete
`tools/` and the generated files once the real photography is in.

## What these photos must be

**Real photographs. Bright, natural daylight. Shot on actual Special Green properties.**

The site applies its own dark overlay, vignette and warm grade on top of whatever you drop
in, so send the photos bright and untreated. Do not pre-darken them, do not add filters. A
bright, sharp source photo under the site's dark treatment is what produces the cinematic
look. A dark or murky source just goes muddy.

Three hard nos:

- **No stock photography.** It reads as canned instantly and it is the fastest way to make a
  real regional company look like a template. Anyone who has seen the same smiling crew on
  three other lawn sites will notice.
- **No illustration, rendering, or AI-generated imagery.** The site must not show work that
  Special Green did not actually do.
- **No dark, flat, or overcast phone snaps.** Bright and sharp beats artful every time here.

Phone photos are fine, and better than stock. What matters is that they are real, bright, and
of work the company actually did.

| Filename | Shot |
| --- | --- |
| `hero-outdoor-living.jpg` | Wide, late-afternoon finished outdoor living space. Patio or pergola, lighting on, manicured turf in foreground. Shot low. |
| `crew-portrait.jpg` | Two or three crew in orange shirts, on site, mid-work. **Vertical.** |
| `crew-group.jpg` | Full team in orange shirts in front of trucks and equipment. Wide. |
| `crew-trimmer.jpg` | Hands on the trimmer, tight crop, orange sleeve in frame. Square. |
| `crew-truck-load.jpg` | Loading or unloading equipment at the truck. Square. |
| `commercial-crew-trucks.jpg` | Crew and trucks on a commercial property. Orange shirts visible, early morning light. |
| `cta-sunset.jpg` | Crew finishing a job at sunset. Gets heavily darkened as texture, so composition matters more than detail. |
| `service-lawn-care.jpg` | Striped, freshly cut turf with a crew member and mower in frame. Low angle. |
| `service-landscaping.jpg` | New bed install, fresh mulch, plants in place, sunset light behind. |
| `service-irrigation.jpg` | Sprinkler heads running at golden hour, water catching the light. |
| `project-patio-landscape.jpg` | Patio, seating, fire feature, lighting at dusk. |
| `project-front-yard.jpg` | Front yard after shot, straight on, sharp bed lines. |
| `project-irrigation.jpg` | Irrigation zone running across a large lawn, wide. |
| `project-office-park.jpg` | Commercial property, clean turf and beds. |

## Specs

`tools/prepare-photos.py` handles all of this, so you do not need to export to spec. Send
the largest version you have and let the tool crop and compress it.

For reference, it produces JPEG quality 80 plus a WebP alongside, at 2400px wide for
`hero-*`, `commercial-*` and `cta-*`, and 1600px for everything else. `crew-portrait` and
the two mobile breaks are the vertical ones at 1200x1500.

It never upscales. If a photo is smaller than the target it is used at its own size and the
tool prints a warning, because a stretched photo looks worse than a slightly soft one.

## Priority

If Mark can only send a handful, these five carry the most weight:

1. `crew-group.jpg`
2. `hero-outdoor-living.jpg`
3. `commercial-crew-trucks.jpg`
4. `crew-portrait.jpg`
5. `project-patio-landscape.jpg`

## Source

The crew photos are on the company Facebook page:
https://www.facebook.com/SpecialGreen2022/

Download the originals from there rather than saving them off the timeline. Facebook
recompresses images on upload and again on display, so a right-click save is roughly half
the quality of the file that was posted.
