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
| `assets/images/` | Every photograph the site uses. Placeholders now, real photos by the same filenames later. |
| `docs/IMAGERY-AUDIT.md` | Every section, what imagery it has, and what it needs. |
| `docs/SHOT-LIST.md` | The 24 shots, ranked, with casting and location direction. |
| `tools/` | Image preparation script. Run it on originals before committing them. |
| `docs/WEBSITE-BRIEF.md` | The brief. Its Visual Direction section controls every design decision. |
| `docs/PHOTO-CHECKLIST.md` | Every photograph the site needs, by priority, with shot direction. |
| `docs/PARKED-pool-service.md` | Everything needed to put pool service back, if it comes back. |
| `brand/` | The logo. Open `brand/logo-sheet.html` for every version and the usage rules. |

## Reviewing it

Open the staging URL, or open `index.html` directly. The control in the lower right toggles
photo slot labels: on, it names the exact photograph each image position needs and marks every
figure that still needs verifying. Off, it shows the design as a visitor sees it. Look at it
both ways, and at phone width.

## Photography

Twenty-seven image slots, all wired to filenames in `assets/images/`. Drop a real photograph in
under the matching name and it appears on the site with no code change.

`docs/SHOT-LIST.md` is the brief: 24 ranked shots with casting, property and location
direction. `docs/IMAGERY-AUDIT.md` explains what each section needs and why.

Real photographs only. Bright, natural daylight, shot on actual Special Green properties. No
stock, no illustration, no generated imagery. The site applies its own dark overlay, contrast
and warm grade, so send the sources bright and untreated.

Run `tools/prepare-images.sh` on the originals before committing. It resizes, compresses, and
strips EXIF, which matters because photos taken at customers' homes carry their GPS
coordinates.

Every image carries alt text, explicit width and height so nothing shifts as the page loads,
and lazy loading below the fold. The hero loads eagerly with high fetch priority.

## Before launch

- Real photography in `assets/`
- Business hours, and a physical or mailing address
- The four figures in the positioning section (100+ happy customers, 4+ years in business,
  5-star reviews, fully insured) came from a mockup, not a verified source
- Real Google reviews. The reviews section is a layout only.
- The estimate form has no destination. Wire it to email plus a CRM, and add spam protection.
- Mail on the domain, so `info@specialgreenbr.com` works
- Remove `noindex` from `index.html` and open up `robots.txt`

## Hosting

GitHub Pages serves the staging preview from `main` via `.github/workflows/pages.yml`.

For production, point specialgreenbr.com at **Cloudflare Pages**, not the GoDaddy website
builder. Move DNS to Cloudflare, keep the registration at GoDaddy, and deploy from this
repository.

Cloudflare Pages is free for commercial use, with unlimited bandwidth and 500 builds a month.
A static marketing site will never come close to those limits.

Do not use Vercel's free Hobby plan for this. It is non-commercial only, and Vercel reads
commercial broadly enough to cover a site built by a paid freelancer. Commercial use there is
$20 a month per seat. Netlify's free tier and GitHub Pages both allow commercial use if
Cloudflare ever falls through.

**Before switching nameservers:** moving DNS to Cloudflare means GoDaddy stops serving your
records. If mail is set up on the domain first, the MX records have to be recreated in
Cloudflare or mail stops. Do the DNS move before setting up email, or copy the MX records
across carefully.
