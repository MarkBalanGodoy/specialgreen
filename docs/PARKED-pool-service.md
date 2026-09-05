# Parked: Pool Service

Pool service was removed from the site on 5 September 2026. It may come back. Everything
needed to restore it is here, so it is a paste rather than a rebuild.

Last version with pool service live: commit `59c1083`.

## What to change when it comes back

1. Hero supporting line back to four services
2. Services strip back to five categories
3. Pool card back into the services showcase
4. Pool project back into featured work
5. Copy, form option, footer link, and metadata

Details below, in the order they appear in `homepage.html`.

---

### 1. Metadata and schema

Restore "and pool service" to the meta description, the `og:description`, and the
`LocalBusiness` description. Add the offer back to `makesOffer`:

```json
{"@type":"Offer","itemOffered":{"@type":"Service","name":"Pool Service"}},
```

### 2. Hero supporting line

```html
<span class="svc">Lawn Care. Landscaping. Irrigation. Pool Service.</span>
```

### 3. Services strip

Set the grid back to five columns and restore the responsive rules:

```css
.strip ul{grid-template-columns:repeat(5,1fr)}

@media (max-width:900px){
  .strip ul{grid-template-columns:repeat(3,1fr)}
  .strip li:nth-child(3){border-right:0}
  .strip li:nth-child(n+4){border-top:1px solid var(--hair-dark)}
  .strip li:nth-child(4){grid-column:1/3}
}
@media (max-width:520px){
  .strip ul{grid-template-columns:repeat(2,1fr)}
  .strip li{border-right:1px solid var(--hair-dark)}
  .strip li:nth-child(even){border-right:0}
  .strip li:nth-child(n+3){border-top:1px solid var(--hair-dark)}
  .strip li:nth-child(4){grid-column:auto}
  .strip li:last-child{grid-column:1/-1;border-right:0}
  .strip svg{width:34px;height:34px}
}
```

Then put the list item back, fourth of five, before Commercial:

```html
<li><a href="#services">
  <svg viewBox="0 0 32 32" aria-hidden="true"><path d="M3 22c2.6 0 2.6 2 5.2 2s2.6-2 5.2-2 2.6 2 5.2 2 2.6-2 5.2-2 2.6 2 5.2 2"/><path d="M3 27c2.6 0 2.6 2 5.2 2s2.6-2 5.2-2 2.6 2 5.2 2 2.6-2 5.2-2 2.6 2 5.2 2"/><path d="M11 22V7a3 3 0 0 1 6 0M21 22V7a3 3 0 0 1 6 0"/></svg>
  <span class="lbl">Pool Service</span></a></li>
```

### 4. Positioning copy

```
Special Green is a full-service outdoor property company. We maintain lawns every week, we
design and install landscapes, we build and repair irrigation systems, and we keep pools
clean and swimming all season.

One company, one crew, one point of contact for the entire property. You are not chasing
four vendors and hoping they show up in the right order.
```

Note the vendor count goes back to four.

### 5. Services showcase

Change the irrigation card back from `card--full` to `card`, then add the pool card last:

```html
<article class="card card--wide">
  <div class="shot v6"><div class="slot-tag">Pool service: clean pool at dusk, water lit, tight crop on the surface and coping with landscaping behind.</div></div>
  <div class="veil"></div>
  <div class="in">
    <svg class="ico" viewBox="0 0 32 32" aria-hidden="true"><path d="M3 22c2.6 0 2.6 2 5.2 2s2.6-2 5.2-2 2.6 2 5.2 2 2.6-2 5.2-2 2.6 2 5.2 2"/><path d="M3 27c2.6 0 2.6 2 5.2 2s2.6-2 5.2-2 2.6 2 5.2 2 2.6-2 5.2-2 2.6 2 5.2 2"/><path d="M11 22V7a3 3 0 0 1 6 0M21 22V7a3 3 0 0 1 6 0"/></svg>
    <h3>Pool Service</h3>
    <p>Weekly cleaning, chemical balancing, filter and equipment service, and openings and closings. The pool stays swim ready without you thinking about it.</p>
    <span class="more">Pool Service</span>
  </div>
</article>
```

### 6. Featured projects

The grid went from three columns to two when pool came out, because four projects fill a
two-column grid and five do not. Putting pool back makes it five, so restore the
three-column layout with the first project tall:

```css
.proj-grid{grid-template-columns:repeat(3,1fr)}
.proj{aspect-ratio:4/3}
.proj .meta strong{font-size:21px}
.proj--tall{grid-row:span 2;aspect-ratio:auto}
@media (max-width:1000px){.proj-grid{grid-template-columns:repeat(2,1fr)}.proj--tall{grid-row:auto;aspect-ratio:4/3}}
@media (max-width:620px){.proj-grid{grid-template-columns:1fr}}
```

Add `proj--tall` back to the first project and restore its slot note to "Vertical hero
project", then add the pool project last:

```html
<a class="proj" href="#work"><div class="shot v5"><div class="slot-tag">Pool and surrounding landscape, warm evening light.</div></div><div class="veil"></div>
  <div class="meta"><span>Pool Service</span><strong>Pool &amp; Poolscape Care</strong></div></a>
```

### 7. CTA list, form, footer

```html
<span>One company for lawn, landscape, irrigation, and pool</span>
```

```html
<option>Pool Service</option>
```

```html
<li><a href="#services">Pool Service</a></li>
```

Footer blurb back to "Lawn care, landscaping, irrigation, and pool service for residential
and commercial properties across the Baton Rouge area."

### 8. Photography

Two shots come back onto the checklist:

| Slot | Shot |
| --- | --- |
| Pool service | Clean pool at dusk, water lit, tight crop on surface and coping with landscaping behind. |
| Pool and poolscape | Pool with surrounding landscape, warm evening light. |

### 9. Brief

`WEBSITE-BRIEF.md` needs the hero supporting copy back to four services and the strip back
to five icon categories. The parked note in that file comes out.
