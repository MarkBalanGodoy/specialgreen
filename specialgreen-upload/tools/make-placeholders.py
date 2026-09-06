"""
Neutral placeholder generator.

Writes one dark tonal SVG per image slot. No depicted content: no houses, no people, no
work. They exist so the page is never broken and never implies a project the company did
not do. A real photograph dropped in under the same filename replaces them outright.
"""
import io, os, json
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'ph-svg')
os.makedirs(OUT, exist_ok=True)

TONES = [
    ("#16281a", "#0C170F", "#050806"),
    ("#1B2E1C", "#0A130C", "#040705"),
    ("#0A1410", "#132018", "#050906"),
    ("#101C14", "#080F0A", "#030604"),
    ("#131E16", "#0A110C", "#040604"),
]

SLOTS = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'slots.json')))

for i, s in enumerate(SLOTS):
    a, b, c = TONES[i % len(TONES)]
    w, h = s['w'], s['h']
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs><linearGradient id="g" x1="0" y1="0" x2="0.6" y2="1">'
           f'<stop offset="0" stop-color="{a}"/><stop offset="0.55" stop-color="{b}"/>'
           f'<stop offset="1" stop-color="{c}"/></linearGradient>'
           f'<radialGradient id="v" cx="50%" cy="42%" r="78%">'
           f'<stop offset="45%" stop-color="#000" stop-opacity="0"/>'
           f'<stop offset="100%" stop-color="#000" stop-opacity="0.55"/></radialGradient></defs>'
           f'<rect width="{w}" height="{h}" fill="url(#g)"/>'
           f'<rect width="{w}" height="{h}" fill="url(#v)"/></svg>')
    io.open(os.path.join(OUT, s['name'].replace('.jpg', '.svg')), 'w').write(svg)
print(f"{len(SLOTS)} placeholder scenes written to {OUT}")
