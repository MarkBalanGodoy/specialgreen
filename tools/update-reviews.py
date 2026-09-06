#!/usr/bin/env python3
"""
Special Green - put the Google reviews on the site.

HOW TO UPDATE
    1. Open data/reviews.json
    2. Paste the review in: text, name, location. That is it.
    3. Run:  python3 tools/update-reviews.py
    4. Commit and push.

    Reviews appear in the order they are listed. Newest first reads best.

WHY A FILE AND NOT A LIVE FEED
    Pulling reviews live from Google needs a Places API key, costs money per
    request, and Google's terms limit how long results may be cached. For a
    handful of reviews that change a few times a year, a file someone edits in
    a minute is the better trade. If the volume ever justifies it, the shape of
    this file is what an API fetch would write into anyway.

FAIL-SAFE BEHAVIOUR
    An empty reviews list removes the whole section from the page, along with
    the footer link to it. That is deliberate. A testimonials block holding
    invented quotes is worse than no testimonials block, so the failure mode
    here is "section disappears", never "placeholder ships".

A NOTE ON REVIEW SCHEMA
    This deliberately does NOT emit Review or AggregateRating structured data.
    Google's guidelines treat review markup for reviews gathered on another
    platform as self-serving, and star ratings that appear in search results
    without qualifying are a good way to earn a manual action. The reviews
    display normally as page content; they just are not marked up as schema.
"""

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(ROOT, "index.html")
DATA = os.path.join(ROOT, "data", "reviews.json")

START = "<!-- REVIEWS:START -->"
END = "<!-- REVIEWS:END -->"

STAR = ('<svg viewBox="0 0 24 24"><path d="m12 2 3 6.5 7 .9-5 4.9 1.2 7L12 18l-6.2 3.3'
        'L7 14.3 2 9.4l7-.9L12 2Z"/></svg>')


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;")
            .replace(">", "&gt;").replace('"', "&quot;"))


def card(r):
    name = r.get("name", "").strip()
    if not name:
        raise ValueError("every review needs a name")
    text = r.get("text", "").strip()
    if not text:
        raise ValueError("review from %s has no text" % name)
    rating = int(r.get("rating", 5))
    if not 1 <= rating <= 5:
        raise ValueError("rating for %s must be 1-5" % name)
    initial = (r.get("initial") or name[0]).upper()
    location = r.get("location", "").strip()
    label = "%d star%s" % (rating, "" if rating == 1 else "s")
    return (
        '      <article class="rev">\n'
        '        <div class="stars" aria-label="%s">\n          %s\n        </div>\n'
        '        <p>%s</p>\n'
        '        <div class="who"><i>%s</i><div><b>%s</b><span>%s</span></div></div>\n'
        '      </article>'
    ) % (label, STAR * rating, esc(text), esc(initial), esc(name), esc(location))


def section(reviews, note):
    cards = "\n".join(card(r) for r in reviews)
    note_html = ('    <p class="rev-note">%s</p>\n' % esc(note)) if note else ""
    return (
        '<section class="light pad" id="reviews">\n'
        '  <div class="wrap">\n'
        '    <div class="rev-head">\n'
        '      <p class="eyebrow" style="justify-content:center">What Customers Say</p>\n'
        '      <h2>Proof,<br>Not Promises.</h2>\n'
        '    </div>\n\n'
        '    <div class="rev-grid">\n%s\n    </div>\n'
        '%s'
        '  </div>\n'
        '</section>'
    ) % (cards, note_html)


def main():
    if not os.path.exists(DATA):
        print("missing %s" % DATA, file=sys.stderr)
        return 1
    with open(DATA, encoding="utf-8") as f:
        data = json.load(f)
    reviews = [r for r in data.get("reviews", []) if r.get("text", "").strip()]
    note = data.get("note", "").strip()

    html = open(INDEX, encoding="utf-8").read()
    if START not in html or END not in html:
        print("marker comments not found in index.html", file=sys.stderr)
        return 1
    a = html.index(START) + len(START)
    b = html.index(END)

    if reviews:
        body = "\n" + section(reviews, note) + "\n"
        # make sure the footer link is present
        if 'href="#reviews"' not in html:
            html = html.replace('<li><a href="#work">Projects</a></li>',
                                '<li><a href="#work">Projects</a></li>\n'
                                '          <li><a href="#reviews">Reviews</a></li>', 1)
            a = html.index(START) + len(START)
            b = html.index(END)
    else:
        body = "\n"
        # nothing to link to, so the footer link goes as well
        html = re.sub(r'\s*<li><a href="#reviews">[^<]*</a></li>', "", html)
        a = html.index(START) + len(START)
        b = html.index(END)

    html = html[:a] + body + html[b:]
    open(INDEX, "w", encoding="utf-8").write(html)

    if reviews:
        print("%d review(s) written into index.html:" % len(reviews))
        for r in reviews:
            print("  %d★  %s" % (int(r.get("rating", 5)), r.get("name")))
    else:
        print("No reviews in data/reviews.json.")
        print("The reviews section has been removed from the page, and so has the")
        print("footer link to it. Add reviews to the file and re-run to bring it back.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
