# Special Green LLC — Website

Outdoor property services company in the Baton Rouge, Louisiana area.
Lawn care, landscaping, irrigation, and commercial grounds maintenance.

- **Domain:** specialgreenbr.com (registered at GoDaddy, not yet pointed here)
- **Staging:** https://securenation.github.io/specialgreen/
- **Phone:** (225) 442-2394
- **Facebook:** https://www.facebook.com/SpecialGreen2022/

## This is a preview, not the live site

The staging build carries `noindex` and a `robots.txt` that disallows everything, because it
still contains placeholder photography and figures that have not been verified. Both come off
when the site goes live.

## Files

| Path | What it is |
| --- | --- |
| `index.html` | The homepage. No build step, no dependencies. Open it in a browser. |
| `assets/` | Photography drop folder. `assets/README.md` lists the exact filenames the page expects. |
| `docs/WEBSITE-BRIEF.md` | The brief. Its Visual Direction section controls every design decision. |
| `docs/PHOTO-CHECKLIST.md` | Every photograph the site needs, by priority, with shot direction. |
| `docs/PARKED-pool-service.md` | Everything needed to put pool service back, if it comes back. |

## Reviewing it

Open the staging URL, or open `index.html` directly. The control in the lower right toggles
photo slot labels: on, it names the exact photograph each image position needs and marks every
figure that still needs verifying. Off, it shows the design as a visitor sees it. Look at it
both ways, and at phone width.

## Photography

Every image slot is wired to a filename in `assets/`. Drop real photos in with those names and
they appear on the site with no code changes.

Real photographs only: bright, natural daylight, shot on actual Special Green properties. No
stock, no illustration, no AI imagery. The site applies its own dark overlay and vignette, so
send the source photos bright and untreated. See `assets/README.md`.

## Before launch

- Real photography in `assets/`
- Business hours, and a physical or mailing address
- The four figures in the positioning section (100+ happy customers, 4+ years in business,
  5-star reviews, fully insured) came from a mockup, not a verified source
- Real Google reviews. The reviews section is a layout only.
- The estimate form has no destination. Wire it to email plus a CRM, and add spam protection.
- Mail on the domain, so `info@specialgreenbr.com` works
- **The logo descriptor reads "Pools" and the site does not sell pool service.** Either a
  pool-free logo variant, or pool service comes back.
- Remove `noindex` from `index.html` and open up `robots.txt`

## Hosting

GitHub Pages serves the staging preview from `main` via `.github/workflows/pages.yml`.

For production, point specialgreenbr.com at Vercel or Cloudflare Pages rather than the GoDaddy
website builder. Move DNS to Cloudflare, keep the registration at GoDaddy, deploy from this
repository. Both are free at this traffic level and both are faster than anything GoDaddy will
serve.
