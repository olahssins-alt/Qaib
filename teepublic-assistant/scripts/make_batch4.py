"""Batch 4 (plan 12 Oct): idea A4 'Thankful for My Mahjong Group' in five styles, with illustrated tiles.
Usage: python scripts/make_batch4.py batch-04
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, arc, star, sparkle, svg, render, wear, on_color, W, H
from fx import warp, p, outlined, extrude
from motifs import *

SHRIK, TITAN, ABRIL, PLAY, CAVEAT, CORM, GRAD = (font("shrikhand-latin-400-normal"), font("titan-one-latin-400-normal"),
    font("abril-fatface-latin-400-normal"), font("playfair-display-latin-700-normal"), font("caveat-latin-700-normal"),
    font("cormorant-garamond-latin-600-italic"), font("graduate-latin-400-normal"))
CREAM, RUST, MUSTARD, ORANGE, SAGE, INK, BURG, GOLD = "#F6EBDD", "#C8553D", "#F2A541", "#E9803A", "#7FA88E", "#2A1F1A", "#7E2A35", "#D9A84E"

# 1 groovy: wavy echo type + a fan of tiles, turkey tile in the middle
def d1():
    o = []
    for txt, base, cap, ph, w_ in (("THANKFUL FOR MY", 1000, 560, 0.4, 3900), ("MAHJONG GROUP", 5100, 760, 2.2, 3950)):
        d = warp(2250, base, txt, cap, w_, SHRIK, yfn=lambda u, ph=ph: 90 * math.sin(2 * math.pi * u + ph), rotate=True, track=8)
        for k, c in enumerate((SAGE, MUSTARD, RUST)):
            o.append(f'<g transform="translate({(3-k)*32} {(3-k)*32})">' + p(d, c, c, 26) + "</g>")
        o.append(outlined(d, CREAM, (INK, 50)))
    faces = ["bam3", "dots3", "turkey", "dots1", "bam2"]
    for i, f in enumerate(faces):
        if i == 2: continue
        a = (i - 2) * 16
        o.append(f'<g transform="rotate({a} 2250 5200)">' + at(2250, 2950, tile(f, 1.55)) + "</g>")
    o.append(at(2250, 2850, tile("turkey", 1.8)))
    for x, y, s in ((520, 1500, 110), (3980, 1450, 130), (450, 4200, 80), (4050, 4250, 95)):
        o.append(sparkle(x, y, s, MUSTARD))
    return svg(*o)

# 2 puff 3D: GOBBLE GOBBLE PUNG with three identical turkey tiles (a pung)
def d2():
    o = []
    for txt, base, cap, fill in (("GOBBLE", 1250, 900, "#FFB86B"), ("GOBBLE", 2300, 900, "#FF8C69")):
        d = warp(2250, base, txt, cap, 3700, TITAN, track=30)
        o.append(extrude(d, "#6E2617", 60, 95, 12, sw=55))
        o.append(outlined(d, fill, (CREAM, 55)))
        o.append(p(d, "none", "#FFFFFF", 12, 'opacity="0.35" transform="translate(-12 -16)"'))
    for i in range(3):
        o.append(at(2250 + (i - 1) * 1150, 3500, tile("turkey", 1.6), rot=(i - 1) * 4))
    d = warp(2250, 5250, "PUNG!", 640, 2600, TITAN, track=40)
    o.append(extrude(d, "#1F5E3A", 45, 70, 10, sw=45))
    o.append(outlined(d, "#9ED8A5", (CREAM, 45)))
    return svg(*o)

# 3 vintage club badge
def d3():
    cx, cy = 2250, 2500
    o = [f'<circle cx="{cx}" cy="{cy}" r="1950" fill="{BURG}"/>', f'<circle cx="{cx}" cy="{cy}" r="1860" fill="none" stroke="{GOLD}" stroke-width="26"/>',
         f'<circle cx="{cx}" cy="{cy}" r="1280" fill="#5E1E27"/>', f'<circle cx="{cx}" cy="{cy}" r="1280" fill="none" stroke="{GOLD}" stroke-width="22"/>']
    o.append(arc(cx, cy, 1440, "MAHJONG CLUB", 270, CREAM, font=PLAY, xscale=1.0, track=40, bold=0))
    o.append(arc(cx, cy, 1440, "THANKSGIVING TOURNAMENT", 165, GOLD, font=PLAY, xscale=1.0, track=22, bold=0, bottom=True))
    o.append(star(cx - 1570, cy, 85, GOLD)); o.append(star(cx + 1570, cy, 85, GOLD))
    o.append(at(cx - 480, cy + 40, tile("dots1", 1.1), rot=-12)); o.append(at(cx + 480, cy + 40, tile("bam3", 1.1), rot=12))
    o.append(at(cx, cy - 40, tile("turkey", 1.3)))
    # ribbon
    o.append(f'<path d="M500 4350 L4000 4350 L3820 4620 L4000 4890 L500 4890 L680 4620 Z" fill="{RUST}" stroke="{CREAM}" stroke-width="24"/>')
    o.append(p(warp(2250, 4760, "Thankful for My Group", 330, 3000, ABRIL), CREAM))
    o.append(p(warp(2250, 5300, "EST. AT THE KITCHEN TABLE", 170, 2600, GRAD, track=50), GOLD))
    return svg(*o)

# 4 doodle: top-down table of four with a pie in the middle
def d4():
    o = []
    st = f'stroke="{CREAM}" stroke-width="30" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    o.append(p(warp(2250, 900, "my favorite", 380, 2600, CAVEAT), CREAM))
    o.append(p(warp(2250, 1450, "Thanksgiving table", 480, 3700, CAVEAT), MUSTARD))
    tx, ty, ts = 2250, 3250, 1800
    o.append(f'<rect x="{tx-ts/2+30}" y="{ty-ts/2+30}" width="{ts}" height="{ts}" rx="60" fill="#5C3A26"/>')
    o.append(f'<rect x="{tx-ts/2}" y="{ty-ts/2}" width="{ts}" height="{ts}" rx="60" fill="#2E7A57" stroke="{CREAM}" stroke-width="30"/>')
    # four racks of mini tiles, one per side, plus four chairs
    for k in range(4):
        rot = k * 90
        g = []
        g.append(f'<rect x="{tx-480}" y="{ty+ts/2-210}" width="960" height="70" rx="20" fill="#C68A4E"/>')
        for i in range(8):
            g.append(f'<rect x="{tx-460+i*118}" y="{ty+ts/2-300}" width="104" height="100" rx="16" fill="{IVORY}"/>')
            g.append(f'<rect x="{tx-460+i*118}" y="{ty+ts/2-300}" width="104" height="26" rx="10" fill="#2E8A55"/>')
        g.append(f'<path d="M{tx-420} {ty+ts/2+120} q420 220 840 0" {st}/>')
        g.append(f'<circle cx="{tx}" cy="{ty+ts/2+330}" r="150" fill="none" stroke="{CREAM}" stroke-width="30"/>')
        o.append(f'<g transform="rotate({rot} {tx} {ty})">' + "".join(g) + "</g>")
    o.append(at(tx, ty - 30, pie(1.5)))
    for x, y in ((tx - 340, ty - 330), (tx + 330, ty + 320), (tx + 300, ty - 300)):
        o.append(at(x, y, tile("dots1", 0.2), rot=20))
    o.append(p(warp(2250, 5250, "thankful for my mahjong group", 230, 3300, CAVEAT), CREAM))
    o.append(f'<path d="M1100 5350 C 1700 5300 2800 5300 3400 5350" stroke="{RUST}" stroke-width="30" fill="none" stroke-linecap="round"/>')
    return svg(*o)

# 5 minimal line art
def d5():
    o = []
    o.append(p(warp(2250, 1450, "thankful", 600, 3200, CORM, track=20), CREAM))
    o.append(at(2250, 2850, tile_line(2.1, CREAM, 28)))
    pk = (f'<ellipse cx="0" cy="0" rx="380" ry="300" fill="none" stroke="{GOLD}" stroke-width="28"/>'
          f'<path d="M0 -300 C -200 -170 -200 170 0 300 M0 -300 C 200 -170 200 170 0 300" stroke="{GOLD}" stroke-width="24" fill="none"/>'
          f'<path d="M0 -300 C 10 -380 40 -420 90 -440" stroke="{GOLD}" stroke-width="30" fill="none" stroke-linecap="round"/>'
          f'<path d="M30 -360 C 120 -420 220 -380 230 -320 C 150 -300 80 -320 30 -360 Z" fill="{GOLD}"/>')
    o.append(at(2250, 2950, pk))
    o.append(p(warp(2250, 4500, "for my mahjong group", 330, 3300, CORM, track=30), GOLD))
    o.append(f'<line x1="1500" y1="4720" x2="3000" y2="4720" stroke="{CREAM}" stroke-width="12"/>')
    o.append(p(warp(2250, 5000, "PUNG · KONG · PIE", 140, 2200, PLAY, track=120), CREAM))
    return svg(*o)

DESIGNS = {"a1-thankful-mahjong-group-groovy": (d1, False), "a2-gobble-gobble-pung-puff": (d2, False),
           "a3-mahjong-club-thanksgiving-badge": (d3, False), "a4-favorite-thanksgiving-table-doodle": (d4, False),
           "a5-thankful-mahjong-minimal": (d5, False)}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, worn)) in enumerate(DESIGNS.items()):
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s)
        if worn: img = wear(img, seed=60 + i)
        img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
