#!/usr/bin/env python3
"""
Special Green - build the /guides/ pages.

WHY THESE EXIST
    The homepage tips section is one page competing for every query at once,
    which is not how search works. Each of these targets one question a Baton
    Rouge homeowner actually types, answers it properly, and routes the ones
    who need a crew to the estimate form.

WHAT IT WRITES
    guides/index.html                 the hub
    guides/<slug>/index.html          one page per guide (clean URLs)
    sitemap.xml                       homepage plus every guide

    python3 tools/build-guides.py

EDITING
    Content lives in GUIDES below. Add a dict, re-run, commit. The chrome,
    breadcrumbs, schema, related links and sitemap all follow automatically.

NOTE ON INDEXING
    Pages are written with noindex while the site is still on the staging
    host, matching index.html. The launch commit strips it everywhere at once.
"""

import html as _html
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "guides")
SITE = "https://specialgreenbr.com"
PHONE = "(225) 442-2394"
TEL = "+12254422394"

NOINDEX = '<meta name="robots" content="noindex,nofollow"/>\n'   # removed at launch

# --------------------------------------------------------------------------
# Content. Each guide answers one question. The `answer` block is written to
# be liftable as a search snippet: complete, specific, and standing alone.
# --------------------------------------------------------------------------
GUIDES = [
{
 "slug": "brown-patch-st-augustine",
 "kicker": "Lawn Disease",
 "title": "Brown Patch in St. Augustine: What It Is and How to Stop It",
 "h1": "Brown Patch in<br>St.&nbsp;Augustine.",
 "desc": "Circular brown patches in a Baton Rouge St. Augustine lawn are usually large patch fungus. What causes it, how to tell it from drought, and what actually stops it spreading.",
 "standfirst": "If circles of your lawn are going yellow and spreading outward in spring or fall, you are almost certainly looking at large patch, the disease most people around here call brown patch.",
 "answer": "<p>Brown patch shows up as roughly circular patches of yellow or tan grass that widen week over week. It appears in <strong>spring and fall</strong>, when nights are mild and the humidity holds, not in the heat of summer. It is driven by grass blades staying wet overnight, usually from evening watering, often made worse by nitrogen applied at the wrong end of the season. The fix is to water at dawn only, open up airflow, and hold off heavy feeding until the lawn is fully green and growing.</p>",
 "keyfacts": [("Season", "Spring and fall, when nights are mild and damp"),
              ("Looks like", "Circular yellow-to-tan patches that widen outward"),
              ("Main cause", "Blades staying wet overnight"),
              ("Makes it worse", "Evening watering, shoulder-season nitrogen, poor airflow"),
              ("Recovers?", "Yes, but a bad patch can take a season to fill back in")],
 "body": """
<h2>How to know it is brown patch and not something else</h2>
<p>The shape is the giveaway. Brown patch works outward from a point, so the affected
area is roughly circular or a broad arc rather than a random scatter. The patches
expand noticeably from one week to the next. Around the outside edge you will often
see a band of grass that looks darker or slightly water-soaked before it turns.</p>
<p>The other check is at the base of the plant. Pull gently on a few blades inside the
patch. With brown patch the leaf tends to come away easily at the sheath, and the base
of the blade looks rotted or slimy rather than dry. Drought damage does not do that,
and neither do insects.</p>

<h2>Why it hits Baton Rouge lawns so hard</h2>
<p>This disease wants mild temperatures and long periods of leaf wetness. Our spring
and fall deliver exactly that, and they last for months rather than weeks. Add a lawn
that gets watered in the evening, and the grass stays wet from sundown until well after
sunrise. That is the window the fungus needs.</p>
<p>St. Augustine is particularly prone to it, and St. Augustine is what most of this
area is planted in. Shaded, low-lying and poorly drained corners of a yard usually show
it first, because those are the spots that stay damp longest.</p>

<h2>What actually helps</h2>
<h3>Move watering to dawn</h3>
<p>This is the single biggest lever and it costs nothing. Watering early lets the sun
dry the blades within a couple of hours. Watering in the evening leaves them wet all
night. If you have an irrigation controller, change the start time before you change
anything else.</p>

<h3>Stop feeding nitrogen in the shoulder seasons</h3>
<p>A lawn that is only half awake in spring, or winding down in fall, cannot use a heavy
dose of nitrogen. The fungus can. Feeding a struggling lawn to green it up is an
understandable instinct and it usually makes brown patch worse. Wait until the lawn is
fully green and actively growing.</p>

<h3>Open up the airflow</h3>
<p>Thinning low branches on nearby shrubs and trees so air moves across the affected
area shortens the time the grass stays wet. It is slow, unglamorous work and it makes a
real difference in a chronically damp corner.</p>

<h3>Do not scalp it</h3>
<p>Cutting too short stresses the plant and thins the canopy right when it needs to be
strong. Keep St. Augustine tall.</p>

<div class="note"><b>What not to do</b>
<p>Do not water more. The patches look dry, so the instinct is to add water, and that
feeds the exact condition causing the problem. Brown patch is not drought.</p></div>

<h2>Will the lawn come back?</h2>
<p>Usually, yes. St. Augustine spreads by runners, so once conditions change the healthy
grass around a patch will creep back into it. A mild case cleans up within a few weeks
of the weather turning. A bad one, especially in a shaded low spot that stays damp, can
take a full season and may need the underlying drainage or airflow problem fixed before
it stops coming back every year.</p>
<p>If the same patches return in the same places every spring and fall, that is not bad
luck. Something about those spots holds moisture, and that is the thing worth fixing.</p>
""",
 "related": ["yard-holds-water-after-rain", "when-to-fertilize-st-augustine", "mowing-height-st-augustine"],
},
{
 "slug": "when-to-fertilize-st-augustine",
 "kicker": "Feeding",
 "title": "When to Fertilize St. Augustine in Louisiana",
 "h1": "When to Fertilize<br>St.&nbsp;Augustine.",
 "desc": "Timing matters more than product. When to make the first feed of the year on a Louisiana St. Augustine lawn, when to stop, and why feeding early costs you.",
 "standfirst": "Almost every fertilizing mistake we get called about is a timing mistake, not a product mistake. Here is the timing that matters in our climate.",
 "answer": "<p>Wait until the lawn is <strong>fully green and actively growing</strong> before the first feed of the year. In practice that means you have already mowed it two or three times because it needed mowing, not because it looked untidy. Feeding on the first warm week, while the lawn is still waking up, mostly feeds the weeds and sets up disease. At the other end of the year, stop applying nitrogen well before the first frost so the lawn is not pushing soft growth into a freeze.</p>",
 "keyfacts": [("First feed", "Only once the lawn is fully green and growing"),
              ("Rough marker", "After two or three genuine mowings, not the first warm spell"),
              ("Last feed", "Well before first frost, so no soft growth going into winter"),
              ("Biggest risk", "Feeding early: weeds and brown patch both benefit"),
              ("Do first", "A soil test, so you know what is actually missing")],
 "body": """
<h2>Why early feeding backfires</h2>
<p>A dormant or half-dormant lawn cannot take up much nitrogen. The grass is not growing
yet, so it has nowhere to put it. Two things are ready to use it though: cool-season
weeds that are already up and growing, and the fungus that causes brown patch.</p>
<p>So an early application tends to produce a flush of weeds, a disease outbreak, or
both, and then the homeowner concludes the lawn needed more feeding. It is a
frustrating loop and it starts with a bag going down three weeks too soon.</p>

<h2>Read the lawn, not the calendar</h2>
<p>Our spring is unreliable. A warm stretch in February means very little, and a late
cold snap can undo it. Rather than picking a date, watch the lawn:</p>
<ul>
<li>Is it green across the whole yard, including the shaded and low spots, not just the
sunny strip by the driveway?</li>
<li>Has it needed mowing two or three times because it genuinely grew?</li>
<li>Is night-time cold well behind you?</li>
</ul>
<p>When all three are true, the lawn can use what you give it.</p>

<h2>Test rather than guess</h2>
<p>A soil test tells you what your yard is actually short of, and whether the pH is
letting the grass take it up at all. It is inexpensive, and it is the difference between
feeding a lawn and feeding a guess. The LSU AgCenter runs soil testing for Louisiana
residents and their recommendations are written for our soils.</p>
<p>Clay soils around Baton Rouge behave differently from the sandy soils most national
fertilizer advice assumes. That is worth knowing before you buy anything.</p>

<h2>The end of the season</h2>
<p>Late nitrogen pushes soft new growth. Soft new growth is what a freeze damages first.
Stop feeding nitrogen with enough runway that the lawn has hardened off before the first
frost. A lawn going into winter a little lean comes through better than one pushed late.</p>

<div class="note"><b>A note on weed and feed</b>
<p>Combination products tie two jobs to one date, and the two jobs rarely want the same
date. Pre-emergent has to be down before soil warms and weed seed germinates. Fertilizer
should not go down until the lawn is growing. Those are different moments, and a product
that does both forces you to compromise one of them.</p></div>

<h2>What we do</h2>
<p>On a maintenance schedule we time feeding to the lawn in front of us rather than to a
calendar, and we hold back in the seasons when disease pressure is high. If your lawn
has a history of brown patch, that history changes the plan.</p>
""",
 "related": ["brown-patch-st-augustine", "mowing-height-st-augustine", "chinch-bugs-or-drought"],
},
{
 "slug": "chinch-bugs-or-drought",
 "kicker": "Lawn Pests",
 "title": "Chinch Bugs or Drought? How to Tell the Difference",
 "h1": "Chinch Bugs,<br>Or Just Dry?",
 "desc": "If your St. Augustine is browning in patches and watering is not fixing it, chinch bugs are the likely cause. How to tell them apart before you spend money on the wrong fix.",
 "standfirst": "Both look like a lawn drying out. One is solved with water, the other gets worse while you water it. Telling them apart takes about two minutes.",
 "answer": "<p>The test is simple: <strong>water it well and see if it recovers.</strong> Drought-stressed St. Augustine greens back up within a few days of a good soak. Chinch bug damage does not, because the grass is being fed on rather than going thirsty. Chinch damage also tends to start along the hottest, driest edges of a yard, the strips next to driveways, sidewalks and south-facing walls, and then spread outward from there.</p>",
 "keyfacts": [("Season", "Hot, dry stretches through mid and late summer"),
              ("Starts along", "Driveways, sidewalks, south-facing walls"),
              ("Key tell", "Watering does not bring it back"),
              ("Host grass", "St. Augustine above all others"),
              ("Check where", "The boundary between dying and healthy grass")],
 "body": """
<h2>Why the two look identical from the porch</h2>
<p>Chinch bugs feed on the runners and crowns at the soil surface, drawing sap out of
the plant and injecting a substance that blocks the plant's ability to move water. The
grass above ground goes yellow, then straw-coloured, then dies. From any distance that
is exactly what heat stress looks like.</p>
<p>The difference is that a drought-stressed lawn is thirsty and a chinch-damaged lawn
is injured. Water fixes thirst. It does not fix injury.</p>

<h2>How to check properly</h2>
<p>Go out on a hot afternoon, which is when chinch bugs are most active near the surface.
Do not check in the middle of a dead patch: whatever was there has already moved on.
Check the <strong>boundary</strong>, where dying grass meets grass that still looks healthy.</p>
<ul>
<li>Part the grass with your fingers down to the soil line and look for small, fast-moving
insects at the thatch layer.</li>
<li>Look at the runners themselves rather than the blades. Damage shows up there first.</li>
<li>Work a few different edges of the affected area. They are patchy, and one spot proves
nothing.</li>
</ul>

<h2>Why the hot edges first</h2>
<p>Chinch bugs like heat and they like dry. The strip of lawn against a concrete driveway
is several degrees hotter than the middle of the yard, and it dries faster. That is why
damage so often runs as a band along hard surfaces before it moves into the open lawn.</p>
<p>If your browning is in the shade, or in a low spot that holds water, chinch bugs are
an unlikely explanation. Look at disease or drainage instead.</p>

<div class="note"><b>Confirm before you treat</b>
<p>Insecticide will not fix drought, disease or a drainage problem, and a treatment
applied to the wrong diagnosis costs money, delays the actual fix, and puts product down
for no reason. Two minutes on your knees at the edge of a patch is worth it.</p></div>

<h2>What recovery looks like</h2>
<p>St. Augustine spreads by runners, so a lawn that still has healthy grass around the
damage will usually creep back in once the pressure is off. Large areas that were killed
outright may need sod. The earlier the problem is caught, the more likely the lawn closes
the gap on its own.</p>
<p>Lawns that got hit once often get hit again in later summers, so it is worth knowing
which edges of your yard are the vulnerable ones and checking them first.</p>
""",
 "related": ["fall-armyworms", "brown-patch-st-augustine", "watering-a-baton-rouge-lawn"],
},
{
 "slug": "fall-armyworms",
 "kicker": "Lawn Pests",
 "title": "Fall Armyworms: How to Spot Them Before They Take the Lawn",
 "h1": "Fall Armyworms.<br>Speed Matters.",
 "desc": "Armyworms can strip a Louisiana lawn in a couple of days. What the early signs look like, how to check, and why catching them a few days early changes the outcome.",
 "standfirst": "Most lawn problems give you weeks to react. This one gives you days, and that is the only thing you really need to remember about it.",
 "answer": "<p>Fall armyworms arrive in late summer and fall after moth flights, and a heavy infestation can strip a lawn in <strong>two or three days</strong>. The early signs are a lawn that seems to be thinning fast, blades with chewed, ragged edges, and birds working the grass with unusual interest. Catching them in the first day or two is the difference between a lawn that recovers on its own and one that needs replacing.</p>",
 "keyfacts": [("Season", "Late summer into fall, after moth flights"),
              ("Speed", "Serious damage in as little as two to three days"),
              ("Early sign", "Birds suddenly very interested in your lawn"),
              ("On the blade", "Ragged, chewed edges rather than clean browning"),
              ("Recovery", "Good if roots survive and it is not too late in the season")],
 "body": """
<h2>What you are looking for</h2>
<p>The damage is chewing, not browning. Look closely at individual blades in the thinning
area: armyworm feeding leaves ragged, notched edges and windowed strips where the tissue
has been scraped away. That is quite different from disease, which rots or discolours the
blade, and from drought, which dries it evenly.</p>
<p>The caterpillars themselves are easiest to find early morning or late evening. In the
heat of the day they move down into the thatch and out of sight, which is part of why
people miss them until the damage is obvious.</p>

<h2>The birds tell you first</h2>
<p>If a flock of birds is working your lawn methodically and they have not done that
before, go and look. They are not there for the grass. It is the single most reliable
early warning most homeowners get, and it usually arrives a day or two before the
thinning becomes obvious from the house.</p>

<h2>How to check</h2>
<ul>
<li>Get down at the edge of the thinning area and part the grass to the soil.</li>
<li>Check early or late in the day rather than at midday.</li>
<li>Mix a little dish soap into a couple of gallons of water and pour it over a small
patch. It irritates them and brings them to the surface within a few minutes, which
makes an infestation easy to confirm.</li>
</ul>

<div class="note"><b>Why the urgency is not an exaggeration</b>
<p>Armyworms arrive in numbers and they move as a front across a lawn, which is where the
name comes from. A yard that looks slightly thin on a Friday can be visibly stripped by
Sunday. If you are unsure whether what you are seeing is armyworms, treat it as urgent
and check properly rather than waiting to see how it looks next week.</p></div>

<h2>Will the lawn recover?</h2>
<p>Often, yes. Armyworms eat the leaf, not the root. If the crowns and runners are intact
and there is enough season left for the grass to grow, a stripped lawn can green back up
in a few weeks. Two things change that: damage late in the season, when the grass is
heading for dormancy and has no time to recover, and repeat waves, which can exhaust the
plant.</p>
<p>After an outbreak it is worth watching that lawn closely for the rest of the season,
because a second flight can follow the first.</p>
""",
 "related": ["chinch-bugs-or-drought", "brown-patch-st-augustine", "when-to-fertilize-st-augustine"],
},
{
 "slug": "yard-holds-water-after-rain",
 "kicker": "Drainage",
 "title": "Yard Holds Water After Rain? Here Is Why, and What Fixes It",
 "h1": "Water That<br>Will Not Drain.",
 "desc": "Standing water in a Baton Rouge yard is a grading and drainage problem, not a grass problem. Why our clay soil causes it and what a real fix involves.",
 "standfirst": "If water is still sitting in your yard a day after the rain stopped, no amount of fertilizer, sod or reseeding is going to fix it. That is a drainage job.",
 "answer": "<p>Water that sits for more than about <strong>24 hours</strong> after rain is telling you the yard has nowhere to send it. Around Baton Rouge that is usually a combination of heavy clay soil, which drains slowly and compacts easily, and grading that either runs the wrong way or has nowhere to run to. The fix is regrading, a properly built drain with a real outlet, or both. Replanting the spot without fixing the water simply kills the new grass too.</p>",
 "keyfacts": [("Warning line", "Water standing more than about 24 hours"),
              ("Usual cause", "Heavy clay plus grading with no outlet"),
              ("Other signs", "Moss, mosquitoes, spongy soil, turf that stays thin"),
              ("Will not fix it", "Fertilizer, new sod, aeration alone"),
              ("Real fixes", "Regrade, french drain, catch basins, downspout extensions")],
 "body": """
<h2>Why it happens here</h2>
<p>Two things work against us. The first is the soil. Much of this area sits on heavy
clay, which holds water rather than letting it move through, and compacts under foot
traffic and mowers until it holds even more. The second is that a lot of lots are flat.
Water needs somewhere lower to go, and on a flat lot there often is not anywhere.</p>
<p>Add roof runoff dumped by a downspout straight onto a low corner and you have a spot
that will stay wet every time it rains, no matter what you plant in it.</p>

<h2>The signs beyond the puddle</h2>
<ul>
<li>Moss taking hold, which is a moisture and compaction signal</li>
<li>Turf that stays thin in the same spot however you feed it</li>
<li>Ground that feels spongy underfoot days after rain</li>
<li>Mosquitoes breeding in standing water</li>
<li>Water sitting against the foundation or under the slab edge</li>
</ul>
<p>That last one is the one to take seriously. Water pooling against a foundation is a
much more expensive problem than a thin lawn, and it is worth acting on early.</p>

<h2>What an actual fix looks like</h2>
<h3>Regrading</h3>
<p>Sometimes the answer is simply reshaping the ground so water runs somewhere useful.
Where there is fall available to work with, this is the cleanest fix because there is
nothing installed to fail later.</p>

<h3>A french drain</h3>
<p>A trench, a bed of gravel, perforated pipe, and filter fabric to keep soil out of the
gravel. Water moves into the gravel, into the pipe, and away. It works well and it lasts,
provided one thing is right.</p>

<div class="note"><b>The part people get wrong</b>
<p>A drain needs somewhere to discharge and continuous fall to get there. A pipe laid
flat, or one that ends in a low spot with no outlet, just relocates the puddle
underground. Most failed drains we are called out to look at failed for this reason, not
because of the pipe or the gravel.</p></div>

<h3>Catch basins and downspout extensions</h3>
<p>Where roof runoff is the source, moving that water further out before it is released
sometimes solves the whole problem on its own. It is the cheapest thing to try and it is
worth ruling in or out before anything gets dug.</p>

<h2>Why the grass is not the problem</h2>
<p>Turf roots need air. Waterlogged soil has none, so roots suffocate, the grass thins,
and weeds and moss that tolerate wet feet move in. Laying new sod over a spot that holds
water buys a few weeks. Fix the water first and the grass problem usually solves itself.</p>
""",
 "related": ["brown-patch-st-augustine", "watering-a-baton-rouge-lawn", "mowing-height-st-augustine"],
},
{
 "slug": "mowing-height-st-augustine",
 "kicker": "Mowing",
 "title": "How Short Should You Cut St. Augustine?",
 "h1": "Cut It Taller<br>Than You Think.",
 "desc": "Mowing height is the cheapest weed control there is. Why St. Augustine wants to be tall, what scalping costs you, and the one-third rule.",
 "standfirst": "Most struggling St. Augustine lawns we look at are being cut too short. Raising the deck is free, takes one minute, and fixes more than most products do.",
 "answer": "<p>St. Augustine should be cut <strong>tall, generally in the three to four inch range</strong>, and taller still in shade. Never remove more than a third of the blade in a single cut, however long the grass got while you were away. Tall grass shades its own soil, which keeps roots cooler, holds moisture longer and stops most weed seed from ever getting the light it needs to germinate.</p>",
 "keyfacts": [("Target height", "Roughly three to four inches"),
              ("In shade", "Taller again, the grass needs more leaf to work with"),
              ("Never remove", "More than a third of the blade in one cut"),
              ("Blade", "Sharp, always"),
              ("Why it matters", "Height is the cheapest weed control available")],
 "body": """
<h2>What height actually buys you</h2>
<p>A taller canopy shades the soil surface. That does three useful things at once. It
keeps the root zone cooler through our summer, it slows evaporation so the lawn goes
longer between waterings, and it denies weed seed the light it needs to germinate.</p>
<p>Cut the same lawn short and you reverse all three. The soil heats up, dries out
faster, and every weed seed sitting in the top half inch gets the light it was waiting
for. Then the weeds get blamed on the lawn rather than the mower.</p>

<h2>Scalping, and why it is expensive</h2>
<p>Scalping is cutting so low that you take off most of the green leaf and expose stems
and soil. The grass has to rebuild leaf before it can photosynthesise properly, and it
does that using stored energy from the roots. A scalped lawn is a lawn spending its
savings.</p>
<p>It usually happens for one of two reasons: the deck was set low to stretch the interval
between cuts, or the lawn got away over a holiday and was brought back to height in one
pass. The second is where the one-third rule comes in.</p>

<h3>The one-third rule</h3>
<p>Never remove more than a third of the blade height in a single mow. If the lawn is at
six inches and you want it at three, take it to four and a half, wait a few days, then
take it to three. It feels slow. It is much faster than nursing a scalped lawn back
through a Louisiana August.</p>

<h2>Keep the blade sharp</h2>
<p>A sharp blade cuts. A dull one tears, leaving a frayed tip that browns off and gives
disease an opening. In a dry climate that is cosmetic. In our humidity, where brown patch
is already looking for a way in, it is not.</p>
<p>If the tips of your lawn look slightly white or brown a day after mowing, the blade is
the first thing to check.</p>

<div class="note"><b>Shade changes the answer</b>
<p>Grass in shade is working with less light, so it needs more leaf area to feed itself.
Raise the height further in shaded areas rather than cutting the whole yard to one
setting. Shaded St. Augustine cut short is the combination that thins out first.</p></div>

<h2>Other grasses want other heights</h2>
<p>This page is about St. Augustine because that is what most of this area is planted in.
Centipede prefers to be cut lower, and bermuda lower still. If you are not sure what you
have, that is worth establishing before you set a height, because the right setting for
one is the wrong setting for another.</p>
""",
 "related": ["brown-patch-st-augustine", "when-to-fertilize-st-augustine", "watering-a-baton-rouge-lawn"],
},
{
 "slug": "watering-a-baton-rouge-lawn",
 "kicker": "Watering",
 "title": "How Often to Water a Lawn in Baton Rouge",
 "h1": "Water Deep,<br>Water Early.",
 "desc": "How much water a Baton Rouge lawn actually needs, why daily sprinkling makes lawns weaker, and the simple can test that tells you how long to run each zone.",
 "standfirst": "Watering a little every day feels careful and produces a shallow-rooted lawn that cannot cope with the first hot week. Less often and deeper is the whole trick.",
 "answer": "<p>Aim for roughly <strong>an inch of water a week including rainfall</strong>, delivered in one or two deep soakings rather than a little every day, and run it <strong>at dawn</strong>. Deep, infrequent watering pushes roots down to where the moisture is. Daily light watering keeps roots shallow and near the surface, which is exactly where the soil dries out first. Evening watering leaves blades wet overnight and is a leading cause of brown patch here.</p>",
 "keyfacts": [("How much", "About an inch a week, rain included"),
              ("How often", "One or two deep soakings, not daily"),
              ("When", "At dawn"),
              ("Worst time", "Evening: blades stay wet all night"),
              ("How to measure", "Tuna cans on the lawn, then time the zone")],
 "body": """
<h2>Why daily watering weakens a lawn</h2>
<p>Roots grow towards water. Water lightly every day and the moisture never gets more
than an inch or two down, so that is where the roots stay. The lawn looks fine right up
until a hot dry week, when the top inch of soil bakes out and a shallow-rooted lawn has
nothing to fall back on.</p>
<p>Soak the same lawn deeply and less often and the water penetrates further, the roots
follow it down, and the plant has a reserve to draw on. That lawn handles a hot spell
that flattens the daily-watered one next door.</p>

<h2>The can test</h2>
<p>Nobody knows how much water their sprinklers actually put out, and the answer varies
enormously between zones and heads. Finding out takes one afternoon:</p>
<ul>
<li>Put several straight-sided cans, tuna or cat food tins are ideal, around one zone.</li>
<li>Run that zone for fifteen minutes.</li>
<li>Measure the depth in each can and take an average.</li>
</ul>
<p>Now you know your rate. If a zone puts down a quarter inch in fifteen minutes, an inch
takes an hour. Repeat per zone, because coverage is rarely even, and the variation
between cans tells you something useful about how well that zone is set up.</p>

<h2>Why dawn and not evening</h2>
<p>Watering at dawn gives the sun a few hours to dry the leaf, and it happens before the
day's heat drives evaporation losses. Watering in the evening leaves the grass wet from
sundown until well after sunrise, which in our humidity is an invitation to brown patch.</p>
<p>Midday watering is not harmful to the grass, but a good share of it evaporates before
it reaches the soil, so you are paying for water the lawn never sees.</p>

<div class="note"><b>Rain counts</b>
<p>The target includes what falls out of the sky. A controller running the same schedule
through a wet week is watering a saturated lawn, which drives disease and wastes money. A
rain sensor or a controller that adjusts for weather pays for itself, and remembering to
switch the system off during a wet stretch costs nothing at all.</p></div>

<h2>When the lawn tells you it is thirsty</h2>
<p>Grass gives clear signals before it browns. Blades fold in along the midrib, the colour
turns dull and slightly blue-grey, and footprints stay visible across the lawn instead of
springing back. Any of those means water it now, and they are more reliable than a
schedule because they respond to the actual weather.</p>
""",
 "related": ["brown-patch-st-augustine", "mowing-height-st-augustine", "yard-holds-water-after-rain"],
},
]

BY_SLUG = {g["slug"]: g for g in GUIDES}


def esc(s):
    return _html.escape(s, quote=True)


def strip_tags(s):
    """Plain text from a heading. <br> becomes a space: without this, a headline
    that breaks across two lines reads as one run-on word in schema and links."""
    import re
    s = re.sub(r"<br\s*/?>", " ", s)
    s = re.sub(r"<[^>]+>", "", s).replace("&nbsp;", " ")
    return re.sub(r"\s+", " ", s).strip()


HEADER = """<header class="header">
  <div class="wrap">
    <a href="{home}" class="logo"><svg class="mark" viewBox="150 14 500 214" aria-hidden="true"><rect x="496" y="44" width="44" height="62" class="body"/><path class="body" d="M400 20 L644 132 L588 132 L588 222 L212 222 L212 132 L156 132 Z"/><path class="leaf-b" d="M399 212 C352 190 328 140 344 100 C388 118 410 168 399 212 Z"/><path class="leaf-a" d="M401 212 C448 190 472 140 456 100 C412 118 390 168 401 212 Z"/></svg><span class="wordmark"><b>SPECIAL <i>GREEN</i> LLC</b><em>Lawns &middot; Landscaping &middot; Irrigation</em></span></a>
    <nav aria-label="Main">
      <a href="{home}#services">Services</a>
      <a href="{home}#work">Projects</a>
      <a href="{guides}">Yard Guides</a>
      <a href="{home}#crew">About</a>
      <a class="tel" href="tel:{tel}">{phone}</a>
      <a href="{home}#estimate" class="btn btn--primary btn--sm">Free Estimate</a>
    </nav>
  </div>
</header>"""

FOOTER = """<footer class="foot">
  <div class="wrap">
    <div class="cols">
      <div>
        <h3 class="h">Special Green LLC</h3>
        <p class="blurb">Lawn care, landscaping and irrigation across Baton Rouge and the
          surrounding parishes. Residential and commercial.</p>
      </div>
      <div>
        <h3 class="h">Yard Guides</h3>
        <ul>{guidelinks}</ul>
      </div>
      <div>
        <h3 class="h">Contact</h3>
        <ul>
          <li><a href="tel:{tel}">{phone}</a></li>
          <li><a href="mailto:specialgreenllc@gmail.com">specialgreenllc@gmail.com</a></li>
          <li><a href="{home}#estimate">Get a free estimate</a></li>
        </ul>
      </div>
    </div>
    <div class="base">
      <span>&copy; <span id="yr">2026</span> Special Green LLC. All rights reserved.</span>
      <span>Baton Rouge, Louisiana</span>
    </div>
  </div>
  <script>document.getElementById('yr').textContent=new Date().getFullYear();</script>
</footer>"""

CTA = """<section class="cta">
  <div class="wrap">
    <h2>Would Rather<br>Someone Else Did It?</h2>
    <p>We handle lawn care, landscaping, irrigation and drainage across the Baton Rouge
      area. If something in your yard is going backwards and you cannot tell why, we will
      come and look at it.</p>
    <div class="row">
      <a class="btn btn--primary" href="{home}#estimate">Get a Free Estimate</a>
      <a class="btn btn--ghost" href="tel:{tel}">Call {phone}</a>
    </div>
  </div>
</section>"""


def page_shell(title, desc, canonical, body, extra_schema=""):
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}"/>
<meta name="theme-color" content="#0B140E"/>
{NOINDEX}<link rel="canonical" href="{canonical}"/>
<link rel="icon" type="image/svg+xml" href="/brand/favicon.svg"/>
<meta property="og:type" content="article"/>
<meta property="og:site_name" content="Special Green"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{esc(desc)}"/>
<meta property="og:image" content="{SITE}/assets/og-hero.jpg"/>
<meta name="twitter:card" content="summary_large_image"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet"/>
<link rel="stylesheet" href="/assets/site.css"/>
{extra_schema}</head>
<body>
<a class="skip" href="#main">Skip to content</a>
{HEADER.format(home='/', guides='/guides/', tel=TEL, phone=PHONE)}
{body}
{FOOTER.format(home='/', tel=TEL, phone=PHONE, guidelinks=''.join('<li><a href="/guides/%s/">%s</a></li>' % (g['slug'], esc(g['kicker'])) for g in GUIDES[:5]))}
</body>
</html>
"""


def build_guide(g):
    canonical = f"{SITE}/guides/{g['slug']}/"
    facts = "".join(
        f'<li><span class="k">{esc(k)}</span><span class="v">{v}</span></li>'
        for k, v in g["keyfacts"])
    rel = "".join(
        '<a href="/guides/{s}/"><span class="k">{k}</span><b>{t}</b><span>{d}</span></a>'.format(
            s=r, k=esc(BY_SLUG[r]["kicker"]), t=esc(strip_tags(BY_SLUG[r]["h1"])),
            d=esc(BY_SLUG[r]["standfirst"][:110].rsplit(" ", 1)[0] + "…"))
        for r in g["related"] if r in BY_SLUG)

    # Built with json.dumps rather than string formatting: an apostrophe in any
    # title or description would otherwise produce invalid JSON-LD, which fails
    # silently and takes the structured data with it.
    article_ld = json.dumps({
        "@context": "https://schema.org", "@type": "Article",
        "headline": g["title"], "description": g["desc"],
        "about": "Lawn care in Baton Rouge, Louisiana",
        "image": f"{SITE}/assets/og-hero.jpg",
        "mainEntityOfPage": {"@type": "WebPage", "@id": canonical},
        "publisher": {"@type": "Organization", "name": "Special Green LLC", "url": f"{SITE}/"},
    }, indent=None)
    crumb_ld = json.dumps({
        "@context": "https://schema.org", "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
            {"@type": "ListItem", "position": 2, "name": "Yard Guides", "item": f"{SITE}/guides/"},
            {"@type": "ListItem", "position": 3, "name": strip_tags(g["h1"]), "item": canonical},
        ],
    }, indent=None)
    schema = ('<script type="application/ld+json">%s</script>\n'
              '<script type="application/ld+json">%s</script>\n' % (article_ld, crumb_ld))

    body = f"""<main id="main">
  <div class="wrap">
    <p class="crumb"><a href="/">Home</a><span>/</span><a href="/guides/">Yard Guides</a></p>
  </div>
  <div class="wrap masthead">
    <p class="eyebrow">{esc(g['kicker'])}</p>
    <h1>{g['h1']}</h1>
    <p class="standfirst">{esc(g['standfirst'])}</p>
  </div>
  <div class="wrap">
    <article>
      <div class="answer"><span class="lbl">Short answer</span>{g['answer']}</div>
      <ul class="keyfacts">{facts}</ul>
      {g['body']}
    </article>
  </div>
</main>

{CTA.format(home='/', tel=TEL, phone=PHONE)}

<section class="related">
  <div class="wrap">
    <h2>Related Guides</h2>
    <div class="rel-grid">{rel}</div>
  </div>
</section>"""
    return page_shell(g["title"] + " | Special Green", g["desc"], canonical, body, schema)


def build_index():
    canonical = f"{SITE}/guides/"
    cards = "".join(
        '<a href="/guides/{s}/"><span class="k">{k}</span><b>{t}</b><span>{d}</span></a>'.format(
            s=g["slug"], k=esc(g["kicker"]), t=esc(strip_tags(g["h1"])), d=esc(g["standfirst"]))
        for g in GUIDES)
    body = f"""<main id="main">
  <div class="wrap">
    <p class="crumb"><a href="/">Home</a></p>
  </div>
  <div class="wrap masthead">
    <p class="eyebrow">Yard Guides</p>
    <h1>Straight Answers<br>For Louisiana Yards.</h1>
    <p class="standfirst">Most lawn advice online is written for somewhere else. These are
      written for zone 9a: St.&nbsp;Augustine and centipede turf, heavy clay, and the
      humidity that causes half the problems we get called about.</p>
  </div>
  <div class="wrap">
    <div class="guide-grid">{cards}</div>
  </div>
</main>

{CTA.format(home='/', tel=TEL, phone=PHONE)}"""
    return page_shell(
        "Yard Guides for Baton Rouge Lawns | Special Green",
        "Practical lawn and landscape guides written for Baton Rouge: brown patch, chinch bugs, armyworms, drainage, mowing height and watering.",
        canonical, body)


def build_sitemap():
    urls = [f"{SITE}/", f"{SITE}/guides/"] + [f"{SITE}/guides/{g['slug']}/" for g in GUIDES]
    rows = "\n".join(
        "  <url>\n    <loc>%s</loc>\n    <changefreq>monthly</changefreq>\n"
        "    <priority>%s</priority>\n  </url>" % (u, "1.0" if u.endswith(".com/") else "0.7")
        for u in urls)
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + rows + "\n</urlset>\n")


def main():
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "index.html"), "w", encoding="utf-8") as f:
        f.write(build_index())
    print("guides/index.html")
    for g in GUIDES:
        d = os.path.join(OUT, g["slug"])
        os.makedirs(d, exist_ok=True)
        with open(os.path.join(d, "index.html"), "w", encoding="utf-8") as f:
            f.write(build_guide(g))
        print("guides/%s/index.html" % g["slug"])
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(build_sitemap())
    print("sitemap.xml  (%d urls)" % (len(GUIDES) + 2))


if __name__ == "__main__":
    main()
