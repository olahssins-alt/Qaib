"""Batch 7 (plan 15 Oct): idea F1 'Frenchie Holiday Crew' (French bulldogs x Christmas).
Five styles: mugshot lineup, chenille varsity patch, knitted sweater, photo-booth strips, wanted poster.
Usage: python scripts/make_batch7.py batch-07
"""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, arc, star, sparkle, svg, render, wear, on_color, W, H
from fx import warp, p, outlined, extrude
from motifs import frenchie, at
from knit import Knit, COLS, ZIG, DOTS, SNOW

ANTON, GRAD, PAC, RYE, PLAY, DANCE, BEBAS = (font("anton-latin-400-normal"), font("graduate-latin-400-normal"), font("pacifico-latin-400-normal"),
    font("rye-latin-400-normal"), font("playfair-display-latin-700-normal"), font("dancing-script-latin-700-normal"), font("bebas-neue-latin-400-normal"))
CREAM, RED, GREEN, GOLD, INK = "#F4ECDD", "#D7263D", "#1F8A4C", "#F2B134", "#211A16"

# 1 lineup
def d1():
    o = [p(warp(2250, 1000, "FRENCHIE HOLIDAY CREW", 620, 3900, ANTON, track=20), CREAM)]
    for i, y in enumerate(range(1400, 3900, 250)):
        o.append(f'<line x1="350" y1="{y}" x2="4150" y2="{y}" stroke="{CREAM}" stroke-width="{10 if i % 2 else 18}" opacity="0.5"/>')
        if i % 2 == 0:
            o.append(p(warp(250, y + 40, f"{6 - i//2}'", 110, 200, BEBAS), CREAM, extra='opacity="0.7"'))
    crew = [("fawn", "santa", "NAUGHTY", False, False), ("brindle", "elf", "NICE", False, True), ("cream", "antlers", "SNACKS", False, False), ("blue", "beanie", "NAPS", True, False)]
    for i, (c, h, label, wk, tg) in enumerate(crew):
        x = 760 + i * 993
        o.append(at(x, 2950, frenchie(c, h, 1.12, wink=wk, tongue=tg)))
        o.append(f'<rect x="{x-400}" y="3480" width="800" height="320" rx="16" fill="{INK}" stroke="{CREAM}" stroke-width="16"/>')
        o.append(p(warp(x, 3715, label, 190, 660, BEBAS, track=30), CREAM))
    o.append(p(warp(2250, 4500, "BOOKED FOR EXCESSIVE CUTENESS", 240, 3700, GRAD, track=40), GOLD))
    o.append(p(warp(2250, 4950, "CASE NO. 12-25", 160, 2000, GRAD, track=80), CREAM))
    return svg(*o)

# 2 chenille varsity patch
def chenille(d, base, loop, seed, bbox):
    """Fill text path `d` with a fuzzy chenille texture plus a stitched outline."""
    rnd = random.Random(seed)
    x0, y0, x1, y1 = bbox
    cid = f"cl{seed}"
    o = [f'<clipPath id="{cid}"><path d="{d}"/></clipPath>', p(d, CREAM, CREAM, 110), p(d, base, base, 40), f'<g clip-path="url(#{cid})">', f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{base}"/>']
    for _ in range(2600):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(14, 26):.0f}" fill="none" stroke="{loop}" stroke-width="7" opacity="0.55"/>')
    o.append("</g>")
    o.append(p(d, "none", CREAM, 10, 'stroke-dasharray="26 18" transform="translate(0 0)"'))
    return "".join(o)
def d2():
    o = []
    arch = lambda u: -260 * (1 - (2 * u - 1) ** 2)
    d = warp(2250, 1500, "FRENCHIE", 900, 3900, GRAD, yfn=arch, track=40)
    o.append(chenille(d, RED, "#FF8A95", 7, (200, 300, 4300, 1700)))
    cx, cy, r = 2250, 3000, 1150
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r+60}" fill="{CREAM}"/><circle cx="{cx}" cy="{cy}" r="{r}" fill="{GREEN}"/>')
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r-50}" fill="none" stroke="{CREAM}" stroke-width="12" stroke-dasharray="30 22"/>')
    o.append(at(cx, cy + 180, frenchie("fawn", "santa", 1.45, tongue=True)))
    for a in range(0, 360, 45):
        x, y = cx + (r - 170) * math.cos(math.radians(a)), cy + (r - 170) * math.sin(math.radians(a))
        if 200 < a < 340: continue
        o.append(star(x, y, 50, GOLD))
    d2 = warp(2250, 4900, "Holiday Crew", 620, 3600, PAC)
    o.append(p(d2, CREAM, CREAM, 70)); o.append(p(d2, GOLD))
    o.append(p(d2, "none", "#FFF3C4", 6, 'stroke-dasharray="18 14"'))
    return svg(*o)

# 3 knitted sweater
FRENCHIE_PX = [".XX............XX.", "XPPX..........XPPX", "XPPX..........XPPX", "XPPPX........XPPPX", "XPPPXX......XXPPPX",
               ".XXXXXXXXXXXXXXXX.", "XXXXXXXXXXXXXXXXXX", "XXXEEXXXXXXXXEEXXX", "XXXEWXXXXXXXXEWXXX", "XXXXXXXXXXXXXXXXXX",
               "XXXXXXXNNNNXXXXXXX", ".XXXXMMMNNMMMXXXX.", "..XXXMMMKKMMMXXX..", "...XXXMMMMMMXXX...", ".....XXXXXXXX....."]
HAT_PX = ["........WW", ".....RRRWW", "...RRRRR..", "..RRRRRRR.", ".WWWWWWWWW."]
def d3():
    k = Knit()
    red, green, cream, fawn, mask, pink = "#D7263D", "#1FA35B", "#F4EFE3", "#D79A5B", "#5C3E2C", "#F2A6A0"
    k.band(ZIG, 2, red, 2, COLS - 2); k.band(DOTS, 9, cream, 2, COLS - 2)
    for i, c in enumerate(range(3, COLS - 6, 12)):
        k.sprite(SNOW, c, 13, {"X": cream if i % 2 else green})
    k.big("FRENCHIE", 24, cream)
    k.sprite(FRENCHIE_PX, 23, 44, {"X": fawn, "P": pink, "E": "#1A1412", "W": cream, "M": "#8A5E43", "N": "#1A1412", "K": "#E8687A"}, 3)
    k.sprite(HAT_PX, 35, 44, {"R": red, "W": cream}, 3)
    k.big("HOLIDAY CREW", 91, "#F5B700")
    for i, c in enumerate(range(3, COLS - 6, 12)):
        k.sprite(SNOW, c, 103, {"X": cream if i % 2 == 0 else red})
    k.band(DOTS, 112, cream, 2, COLS - 2); k.band(ZIG, 115, green, 2, COLS - 2, offset=4)
    return k.svg()

# 4 photo-booth strips
def strip(x, y, rot, shots, caption):
    fw, fh, pad = 1450, 1250, 90
    hgt = pad + len(shots) * (fh + pad) + 380
    g = [f'<rect x="{x}" y="{y}" width="{fw + 2*pad}" height="{hgt}" rx="24" fill="{CREAM}"/>']
    for i, (bg, coat, hat, wk, tg) in enumerate(shots):
        fy = y + pad + i * (fh + pad)
        g.append(f'<rect x="{x+pad}" y="{fy}" width="{fw}" height="{fh}" fill="{bg}"/>')
        g.append(f'<clipPath id="f{x}{i}"><rect x="{x+pad}" y="{fy}" width="{fw}" height="{fh}"/></clipPath>')
        g.append(f'<g clip-path="url(#f{x}{i})">' + at(x + pad + fw / 2, fy + fh / 2 + 170, frenchie(coat, hat, 1.05, wink=wk, tongue=tg)) + "</g>")
    g.append(p(warp(x + pad + fw / 2, y + hgt - 150, caption, 150, fw - 100, GRAD, track=50), INK))
    cx, cy = x + fw / 2 + pad, y + hgt / 2
    return f'<g transform="rotate({rot} {cx} {cy})">' + "".join(g) + "</g>"
def d4():
    o = [strip(450, 300, -5, [("#F28CB1", "fawn", "bow", False, False), ("#2E8A55", "fawn", "elf", True, False), ("#E2A33A", "fawn", "antlers", False, True)], "FRENCHIE HOLIDAY CREW"),
         strip(2450, 500, 4, [("#4C8FD6", "brindle", "beanie", False, False), ("#D7263D", "brindle", "santa", False, True), ("#7A5CC8", "brindle", "antlers", True, False)], "SMILE · SNORT · REPEAT")]
    return svg(*o)

# 5 wanted poster
def d5():
    paper, brown = "#E9D7B0", "#4A2E1C"
    rnd = random.Random(3)
    edge = []
    for i in range(41):
        edge.append((500 + i * 87.5, 300 + rnd.uniform(-40, 40)))
    right = [(4000 + rnd.uniform(-40, 40), 300 + i * 125) for i in range(41)]
    bottom = [(4000 - i * 87.5, 5300 + rnd.uniform(-40, 40)) for i in range(41)]
    left = [(500 + rnd.uniform(-40, 40), 5300 - i * 125) for i in range(41)]
    pts = edge + right + bottom + left
    o = [f'<polygon points="{" ".join(f"{x:.0f},{y:.0f}" for x, y in pts)}" fill="{paper}"/>']
    for _ in range(14):
        x, y, r = rnd.uniform(700, 3800), rnd.uniform(500, 5100), rnd.uniform(120, 420)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#C9A86E" opacity="0.18"/>')
    o.append(f'<rect x="680" y="480" width="3140" height="4640" fill="none" stroke="{brown}" stroke-width="20"/>')
    o.append(p(warp(2250, 1330, "WANTED", 720, 2900, RYE, track=40), brown))
    o.append(p(warp(2250, 1680, "FOR STEALING SANTA'S COOKIES", 160, 2900, PLAY, track=40), brown))
    o.append(f'<rect x="1150" y="1880" width="2200" height="1900" fill="#D9C08E" stroke="{brown}" stroke-width="26"/>')
    o.append(f'<clipPath id="ph"><rect x="1150" y="1880" width="2200" height="1900"/></clipPath><g clip-path="url(#ph)">' + at(2250, 3050, frenchie("brindle", "santa", 1.45, tongue=True)) + "</g>")
    # crumbs + cookie
    o.append(f'<circle cx="3000" cy="3500" r="150" fill="#C68A4E"/><circle cx="2950" cy="3460" r="22" fill="{brown}"/><circle cx="3060" cy="3540" r="20" fill="{brown}"/><circle cx="3000" cy="3560" r="18" fill="{brown}"/>')
    o.append(p(warp(2250, 4150, "THE FRENCHIE", 380, 2900, RYE, track=30), RED))
    o.append(f'<line x1="900" y1="4330" x2="3600" y2="4330" stroke="{brown}" stroke-width="14"/>')
    o.append(p(warp(2250, 4720, "REWARD: BELLY RUBS", 270, 2900, PLAY, track=40), brown))
    o.append(p(warp(2250, 4970, "LAST SEEN NEAR THE CHRISTMAS TREE", 120, 2600, PLAY, track=50), brown))
    return svg(*o)

DESIGNS = {"f1-frenchie-holiday-crew-lineup": (d1, False), "f2-frenchie-holiday-crew-chenille": (d2, False),
           "f3-frenchie-holiday-crew-knit": (d3, False), "f4-frenchie-photo-booth": (d4, False),
           "f5-wanted-frenchie-cookie-thief": (d5, False)}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, worn)) in enumerate(DESIGNS.items()):
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s)
        if worn: img = wear(img, seed=120 + i)
        img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
