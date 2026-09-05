# Special Green LLC — Website Brief

Outdoor property services company serving the Baton Rouge, Louisiana area.
Lawn care, landscaping, irrigation, and commercial grounds maintenance.

Domain: **specialgreenbr.com** (registered at GoDaddy). Hosting and DNS plan is in `README.md`.

## Confirmed brand facts

| | |
| --- | --- |
| Legal name | Special Green LLC |
| Phone | (225) 442-2394 |
| Email | specialgreenllc@gmail.com, moving to info@specialgreenbr.com |
| Service area | Baton Rouge, LA and surrounding areas |
| Facebook | https://www.facebook.com/SpecialGreen2022/ |
| Logo descriptor | Lawns · Landscaping · Irrigation · Pools |
| Tagline | Outdoor Spaces. Higher Standards. |
| Sign-off | Outdoor Spaces. A Brighter Tomorrow. |
| Crew shirts | Orange, reading SPECIAL GREEN LLC / OUTDOOR LIVING DONE RIGHT. |

> **The logo says POOLS and the site does not.** The logo lockup in every client mockup
> reads "Lawns · Landscaping · Irrigation · Pools", and the crew shirts carry the hero
> headline. With pool service parked, the site renders the descriptor without POOLS. If the
> real logo file is used as-is, the header will advertise a service the site does not sell.
> Either a pool-free version of the logo is needed, or pool service comes back.

The controlling section of this brief is **Visual Direction**. Every design decision,
every page, and every asset selection is judged against it.

---

## Visual Direction

Use the **FIRST website mockup** as the primary and controlling design reference.

The preferred design is the darker, premium concept with:

- Dark green / black overall presentation
- Dramatic full-width photography
- Strong orange accents
- Large white typography
- High-contrast sections
- Luxury outdoor-living feel
- Strong commercial credibility
- Bold service icons
- Cinematic image treatment
- Premium regional-company appearance

The site should feel more like a substantial outdoor-property-services brand than a
neighborhood lawn company.

**The dark design direction is mandatory.**

Do not drift into:

- Bright white landscaping-template aesthetics
- Light green generic lawn-care designs
- Soft pastel branding
- Overly clean SaaS-style layouts
- Cheap residential mowing-company visuals

### Primary Color System

Use approximately:

| Role | Color | Token |
| --- | --- | --- |
| Background | Very dark green / black | `#060A07` |
| Secondary surface | Deep forest green | `#0E1A12` |
| Secondary surface | Charcoal | `#14181A` |
| Secondary surface | Near-black green | `#0A1109` |
| Primary text | White | `#FFFFFF` |
| Secondary text | Soft gray / off-white | `#C7CDC6` |
| Primary accent | Bright orange, from Special Green's orange crew shirts | `#F26B21` |
| Secondary accent | Fresh green, used sparingly for icons, status details, subtle highlights | `#6FBF3F` |

The orange provides energy and brand recognition without overwhelming the site. It carries
primary CTAs, one emphasized phrase per major heading, and small structural marks. It is not
a background color for large areas.

The fresh green is a detail color only: icon strokes, status dots, small rules, hover states.

### Hero Direction

The hero closely follows the first mockup:

- Full-width dramatic real project photography
- Dark image overlay
- Large stacked headline
- Strong orange emphasis on one phrase
- Clear primary and secondary CTAs
- Minimal navigation
- Premium visual composition

Headline:

```
OUTDOOR LIVING.      bold white
DONE RIGHT.          bold orange
```

Supporting copy:

> Lawn Care. Landscaping. Irrigation.
> Professional outdoor property care across the Baton Rouge area.

Buttons:

- `GET A FREE ESTIMATE` (primary)
- `VIEW OUR WORK` (secondary)

Immediately below the hero, a dark services strip with four icon categories:

`LAWN CARE` · `LANDSCAPING` · `IRRIGATION` · `COMMERCIAL`

The reference mockups use `LAWNS`, `LANDSCAPING`, `IRRIGATION`, `POOLS`, `COMMERCIAL`.

> **Pool service is parked.** It was removed from the site on 5 September 2026 and may come
> back. The hero line above listed four services and the strip listed five while it was live.
> `PARKED-pool-service.md` holds everything needed to restore it.

### Dark Section Flow

The homepage alternates between dark cinematic sections, controlled white sections, and
dark image-backed sections. **The site is not predominantly white.**

Required rhythm:

1. Dark hero
2. Dark services strip
3. White positioning section
4. Dark services showcase
5. White featured projects
6. Dark commercial section
7. Dark crew section, orange uniforms prominently visible
8. White reviews
9. Dark CTA
10. Dark footer

Seven of ten sections are dark. Three white sections exist to give the dark work contrast
and to hold detail-heavy content. They are controlled breaks, not the base state of the site.

### Crew Photography

Use actual Special Green crew images wearing orange shirts wherever possible. Those orange
uniforms pop against the dark green and black design. This is one of the most important
brand assets on the site.

Use crew photography especially in:

- About section
- Hard-work section
- Commercial credibility section
- Footer CTA
- Mobile visual break sections

### Image Treatment

Real Special Green photos are treated cinematically:

- Dark overlays
- High contrast
- Tight crops
- Strong depth
- Natural shadows
- Subtle vignette where appropriate
- Slight warm treatment on sunset and outdoor-living imagery

Avoid overly bright, washed-out, generic landscaping photography. Stock imagery is a last
resort and never appears in the hero, the crew section, or the commercial section.

### Typography

Bold condensed or industrial sans-serif for major headings. Headings feel strong and
physical. Uppercase, tight tracking, heavy weight.

Reference headings:

```
OUTDOOR LIVING.        MORE THAN A LAWN COMPANY.
DONE RIGHT.            A HIGHER STANDARD.

BUILT ON HARD WORK.    YOUR PROPERTY.
DRIVEN BY RESULTS.     OUR PRIORITY.
```

Body copy stays clean and highly readable. Normal case, generous line height, no condensed
faces below heading size.

### Button Style

**Primary CTA** — orange background, white text, strong rectangular shape, minimal border
radius, bold uppercase text.

**Secondary CTA** — transparent or dark background, white border, white text.

No bubbly rounded buttons. Border radius stays at or near zero across the site.

### Premium Visual Target

The finished site should feel closer to:

- A regional commercial landscaping company
- A premium outdoor-living contractor
- A substantial property-services organization

and less like:

- A local mowing service
- A DIY website builder template
- A generic lawn-care franchise site

The visual goal:

```
DARK. BOLD. PROFESSIONAL. HARD-WORKING. PREMIUM. LOCAL.
```

Everything reinforces the first mockup. **A light-theme homepage is a design failure and
gets revised before any other work moves forward.**

---

## Reference Build

`homepage.html` in this folder is the working implementation of the direction above. It is
the standard to match, and the file to check any new page against before it ships.

Open it directly in a browser. The control in the lower right toggles photo slot labels,
which name the exact shot required in each image position. Turn them off to review the
design as a visitor sees it.

## Content Placeholders

These are marked in the build and must be replaced with confirmed information before launch.
Nothing here is invented as fact:

- Physical or mailing address, and business hours
- The four figures in the positioning section (100+ happy customers, 4+ years in business,
  5-star reviews, fully insured) came from the client's own mockup, not from a verified
  source. Confirm before launch.
- Years in business, crew count, properties served, commercial contract count
- License and insurance numbers
- Customer reviews. The reviews section is a layout only. Pull verified Google reviews.
- Service area list. Confirm which parishes and neighborhoods are actually covered.

## Photography Needed

See `PHOTO-CHECKLIST.md`. Crew shots in orange shirts are the priority. Everything else can
be shot over time, but the hero, the crew section, and the commercial section need real
Special Green work before launch.
