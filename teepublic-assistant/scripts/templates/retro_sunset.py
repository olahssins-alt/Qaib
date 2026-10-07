"""Template: retro striped sunset badge, 4500x5500 transparent, for dark shirts.

Usage: python scripts/templates/retro_sunset.py "SLOW MORNINGS" "CLUB" out_dir [palette]
Everything is vector: text is converted to outlines with fontTools, no system font needed at print time.
Needs: pip install cairosvg fonttools
"""
import math, sys
from pathlib import Path
import cairosvg
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W, H = 4500, 5500
FONT = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
PALETTES = {  # top-of-sun colour, bottom-of-sun colour, accent, text
    "sunset": ("#FFC857", "#E4572E", "#F4EAD5", "#F4EAD5"),
    "grape":  ("#FFD6A5", "#B5179E", "#7DF9FF", "#F8F1FF"),
    "ocean":  ("#CAF0F8", "#0096C7", "#FFB703", "#F1FAEE"),
}
_f = None

def text(x, y, s, size, fill, width):
    global _f
    _f = _f or TTFont(FONT)
    upm, cmap, gs, hmtx = _f["head"].unitsPerEm, _f.getBestCmap(), _f.getGlyphSet(), _f["hmtx"]
    names = [cmap[ord(c)] for c in s]
    adv = sum(hmtx[n][0] for n in names)
    sc = min(size / upm, width / adv)
    pen, cur = SVGPathPen(gs), 0
    for n in names:
        gs[n].draw(TransformPen(pen, (sc, 0, 0, -sc, x - adv * sc / 2 + cur * sc, y)))
        cur += hmtx[n][0]
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>'

def mix(a, b, t):
    a, b = [int(a[i:i + 2], 16) for i in (1, 3, 5)], [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(round(p + (q - p) * t) for p, q in zip(a, b))

def band(cx, cy, r, y0, y1, fill):
    """Slice of a circle between two horizontal lines, as a polygon."""
    pts = []
    n = 40
    def half(y): return math.sqrt(max(r * r - (y - cy) ** 2, 0))
    for i in range(n + 1):
        y = y0 + (y1 - y0) * i / n
        pts.append((cx + half(y), y))
    for i in range(n, -1, -1):
        y = y0 + (y1 - y0) * i / n
        pts.append((cx - half(y), y))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill)

def build(line1, line2, palette="sunset"):
    top, bottom, accent, ink = PALETTES[palette]
    cx, cy, r = 2250, 2350, 1250
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    p.append(text(cx, 1000, line1, 880, ink, 3900))
    # striped sun: stripes get thicker and gaps wider toward the bottom
    y, i = cy - r, 0
    while y < cy + r:
        t = (y - (cy - r)) / (2 * r)
        h = 60 + 190 * t if t > 0.35 else 400
        gap = 0 if t < 0.35 else 25 + 95 * (t - 0.35)
        y1 = min(y + h, cy + r)
        p.append(band(cx, cy, r, y, y1, mix(top, bottom, t)))
        y = y1 + gap
        i += 1
    # horizon lines and side rays
    for k, (w, yy) in enumerate([(3000, 3700), (2300, 3795), (1600, 3890)]):
        p.append(f'<rect x="{cx - w/2}" y="{yy}" width="{w}" height="46" rx="23" fill="{accent}" opacity="{0.95 - 0.25*k:.2f}"/>')
    p.append(text(cx, 5150, line2, 1250, accent, 3500))
    p.append("</svg>")
    return "".join(p)

if __name__ == "__main__":
    l1, l2, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    pal = sys.argv[4] if len(sys.argv) > 4 else "sunset"
    out.mkdir(parents=True, exist_ok=True)
    svg = build(l1.upper(), l2.upper(), pal)
    (out / f"retro_sunset_{pal}.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"retro_sunset_{pal}.png"))
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"preview_{pal}.png"), output_width=900,
                     background_color="#111111")
