# Imagery Audit

Every section of the homepage, what it shows now, and what photography would do for it.
The site reads sparse because seven of its eleven sections carry no photograph at all, and
the four that do are carrying dark placeholders rather than real work.

Priority 1 means the site does not look established without it. Priority 3 is polish.

## Current state

| # | Section | Imagery now | Verdict |
| --- | --- | --- | --- |
| 1 | Hero | 1 slot | **Underpowered.** One image is doing the entire first impression. |
| 2 | Services strip | Icons only | Correct as is. Icons scan faster than photos here. |
| 3 | Positioning (white) | 1 vertical slot | Right shape, needs a real crew shot. |
| 4 | Services showcase (dark) | 3 slots | **Too few and too generic.** Three services, one image each, no detail. |
| 5 | Featured work (white) | 4 slots | **The weakest section on the site.** Four tiles, no before-and-after, no proof. |
| 6 | Commercial (dark) | 1 slot | Needs real trucks and crew on a real commercial property. |
| 7 | Crew (dark) | 3 slots | The most important slots on the site. All three are empty. |
| 8 | Reviews (white) | **None** | **Biggest gap.** A wall of text where the customer should appear. |
| 9 | CTA band (dark) | 1 slot, heavily darkened | Fine as texture. |
| 10 | Trust band | Icons only | Correct as is. |
| 11 | Footer | None | Correct as is. |

## What is missing entirely

These are content gaps, not just empty slots. Adding photography alone will not fix them,
because there is nowhere on the page for the photography to go.

### Before and after — Priority 1

There is no before-and-after anywhere on the site. For a company that transforms properties,
this is the single highest-converting content that exists, and it is the one thing a
competitor's site usually cannot match, because it requires having actually done the work.

Two paired images, three or four projects. A slider is not necessary and adds fragility; a
clean side-by-side labelled BEFORE and AFTER outperforms it and works on a phone.

**Added to the build** as a new dark section between Featured Work and Commercial.

### The customer — Priority 1

The reviews section is five-star ratings and text on white. Nobody appears in it. The site
never shows the person paying for the service, which is exactly the person a visitor is
trying to picture themselves as.

**Added to the build**: a homeowner and a crew leader talking on a finished property, as a
full-bleed image anchoring the reviews section.

### Service detail — Priority 2

Three service cards carry one image each, all wide establishing shots. The work itself is
never shown close up: the edge along a driveway, the sprinkler head, the hands in the bed.
Detail shots are what separate a company that does the work from a company that bought a
template.

**Added to the build**: a detail strip inside the services showcase.

### Mobile visual breaks — Priority 3

On a phone the page is a long scroll of stacked text blocks. One full-bleed image between
the white sections gives the eye somewhere to rest and makes the page feel considered rather
than long.

## Recommended slot count

| Section | Now | Recommended |
| --- | --- | --- |
| Hero | 1 | 1 |
| Positioning | 1 | 1 |
| Services showcase | 3 | 3 + 3 detail |
| Before and after | 0 | 6 (three pairs) |
| Featured work | 4 | 4 |
| Commercial | 1 | 1 |
| Crew | 3 | 3 |
| Reviews | 0 | 1 |
| CTA band | 1 | 1 |
| **Total** | **14** | **24** |

Twenty-four is a lot to ask for at once. `docs/SHOT-LIST.md` ranks them, and the first eight
carry most of the value.

## One conflict to resolve

The photography brief asks for pool cleaning and a technician testing pool water. **Pool
service is currently off the site.** It was removed on 5 September and parked in
`docs/PARKED-pool-service.md`.

If pool service is coming back, say so and it goes back in one pass, along with the two pool
shots. If it is staying off, drop those two from the shot list. Shooting them and then not
being able to use them wastes a half day of the crew's time.

## What is not a photography problem

Two things make the site feel unfinished that no photograph will fix:

- The **reviews are placeholder text.** Real Google reviews with real names carry more weight
  than any image in that section.
- The **four figures** in the positioning section came from a mockup, not a verified source.
