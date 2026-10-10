"""Batch 3 (plan 10 Oct): idea G2 'Thankful My Charting Is Done' (nurses x Thanksgiving),
five different 2026 trend styles: hand-drawn doodle, coquette bows, varsity, 3D puff, groovy wave.
Usage: python scripts/make_batch3.py batch-03
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, star, sparkle, svg, render, wear, on_color, W, H
from fx import *

CAVEAT, DANCE, PLAY, GRAD, TITAN, SHRIK = (font("caveat-latin-700-normal"), font("dancing-script-latin-700-normal"),
    font("playfair-display-latin-700-normal"), font("graduate-latin-400-normal"), font("titan-one-latin-400-normal"),
    font("shrikhand-latin-400-normal"))
CREAM, RUST, MUSTARD, SAGE, INK, ORANGE, BROWN = "#F6EBDD", "#C8553D", "#F2A541", "#8FB09A", "#2E2420", "#E9803A", "#A86F45"
ROSE, BLUSH, ROSE_D = "#F2A7B8", "#F9D5DD", "#C9708A"

# ------------------------------------------------------------ 1 hand-drawn clipboard (plan: Caveat, retro)
def d1():
    o = []
    cx = 2250
    g = []
    g.append(f'<rect x="900" y="900" width="2700" height="3700" rx="130" fill="{BROWN}"/>')
    g.append(f'<rect x="1060" y="1180" width="2380" height="3260" rx="40" fill="{CREAM}"/>')
    for y in range(1650, 4300, 270):
        g.append(f'<line x1="1180" y1="{y}" x2="3320" y2="{y}" stroke="#D5DED6" stroke-width="16"/>')
    g.append(f'<line x1="1380" y1="1200" x2="1380" y2="4420" stroke="#F0B8A8" stroke-width="14"/>')
    g.append(f'<rect x="1700" y="760" width="1100" height="380" rx="90" fill="#B9C0C6"/><rect x="1820" y="860" width="860" height="140" rx="70" fill="#8E969D"/>')
    g.append(p(warp(cx + 80, 1590, "PATIENT CHART", 120, 1500, PLAY, track=40), "#9C8F86"))
    g.append(p(warp(cx + 80, 2150, "Thankful", 430, 1900, CAVEAT), RUST))
    g.append(p(warp(cx + 80, 2680, "my charting", 360, 1900, CAVEAT), INK))
    g.append(p(warp(cx - 60, 3200, "is done", 360, 1500, CAVEAT), INK))
    g.append(f'<path d="M2830 3080 l120 130 l300 -360" stroke="#3F9A5C" stroke-width="70" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, item in enumerate(("vitals", "meds", "pie")):
        y = 3700 + i * 250
        g.append(f'<rect x="1560" y="{y-150}" width="150" height="150" rx="20" fill="none" stroke="{INK}" stroke-width="20"/>')
        g.append(f'<path d="M1585 {y-80} l40 50 l90 -120" stroke="{RUST}" stroke-width="34" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        g.append(p(warp(2050, y - 10, item, 170, 700, CAVEAT), INK))
    g.append(pumpkin(3020, 3900, 0.9, ORANGE, "#B85A23"))
    o.append(f'<g transform="rotate(-4 {cx} 2700)">' + "".join(g) + "</g>")
    for x, y, s in ((560, 1300, 110), (3950, 1700, 140), (520, 3400, 90), (4000, 3900, 120)):
        o.append(sparkle(x, y, s, MUSTARD))
    o.append(heart(700, 2400, 1.0, None, CREAM, 26)); o.append(heart(3880, 2800, 0.8, None, CREAM, 26))
    o.append(p(warp(cx, 5150, "nurse life", 330, 2400, CAVEAT), CREAM))
    o.append(f'<path d="M1500 5260 C 1900 5190 2600 5190 3000 5260" stroke="{MUSTARD}" stroke-width="40" fill="none" stroke-linecap="round"/>')
    return svg(*o)

# ------------------------------------------------------------ 2 coquette bows
def d2():
    o = [bow(2250, 650, 1.0, ROSE, ROSE_D)]
    o.append(p(warp(2250, 2150, "Thankful", 600, 3700, DANCE), BLUSH))
    o.append(p(warp(2250, 2900, "Grateful", 620, 3700, DANCE), CREAM))
    o.append(p(warp(2250, 3750, "Charted", 620, 3700, DANCE), ROSE))
    for x, s in ((900, 0.95), (3600, 0.95)):
        o.append(pumpkin(x, 4500, s, "#F4B183", "#D98A57", "#8C6A5A")); o.append(bow(x, 4220, 0.38, ROSE, ROSE_D))
    o.append(pumpkin(2250, 4580, 1.15, CREAM, "#D9C8B4", "#8C6A5A")); o.append(bow(2250, 4250, 0.45, ROSE, ROSE_D))
    for x, y in ((600, 1500), (3900, 1600), (500, 3000), (4000, 3200)):
        o.append(heart(x, y, 0.75, ROSE))
    for x, y, s in ((1100, 1150, 70), (3400, 1250, 80), (3900, 2400, 60), (600, 2300, 60)):
        o.append(sparkle(x, y, s, CREAM))
    o.append(p(warp(2250, 5250, "NURSE EDITION", 200, 2400, PLAY, track=90), ROSE))
    return svg(*o)

# ------------------------------------------------------------ 3 varsity
def d3():
    o = []
    arch = lambda u: -380 * (1 - (2 * u - 1) ** 2)
    d = warp(2250, 1650, "NURSE", 1000, 3800, GRAD, yfn=arch, track=40)
    o.append(outlined(d, MUSTARD, (CREAM, 110), (RUST, 65)))
    o.append(p(warp(2250, 2130, "THANKSGIVING SHIFT", 230, 3300, GRAD, track=50), CREAM))
    # stethoscope heart
    cx, cy, s = 2250, 3150, 1.3
    hd = f"M{cx} {cy+430*s} C{cx-760*s} {cy-80*s} {cx-330*s} {cy-640*s} {cx} {cy-260*s} C{cx+330*s} {cy-640*s} {cx+760*s} {cy-80*s} {cx} {cy+430*s}"
    o.append(f'<path d="{hd}" stroke="{RUST}" stroke-width="{75*s:.0f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<path d="M{cx} {cy+430*s} C{cx+120*s} {cy+600*s} {cx+380*s} {cy+640*s} {cx+520*s} {cy+520*s}" stroke="{RUST}" stroke-width="{60*s:.0f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<circle cx="{cx+560*s:.0f}" cy="{cy+480*s:.0f}" r="{120*s:.0f}" fill="{CREAM}" stroke="{RUST}" stroke-width="{40*s:.0f}"/><circle cx="{cx+560*s:.0f}" cy="{cy+480*s:.0f}" r="{50*s:.0f}" fill="{MUSTARD}"/>')
    o.append(pumpkin(cx, cy + 40, 1.35, ORANGE, "#B85A23"))
    o.append(p(warp(2250, 4500, "CHARTING DONE", 420, 3600, GRAD, track=30), CREAM))
    o.append(f'<rect x="900" y="4640" width="2700" height="40" rx="20" fill="{MUSTARD}"/>')
    o.append(p(warp(2250, 5000, "EST. 7PM - 7AM", 240, 2500, GRAD, track=60), MUSTARD))
    return svg(*o)

# ------------------------------------------------------------ 4 3D puff
def d4():
    o = []
    for txt, base, cap, fill in (("CHARTING:", 1700, 900, "#FFB86B"), ("DONE", 2950, 1150, "#FF8C69")):
        d = warp(1800 if txt == "DONE" else 2250, base, txt, cap, 3700 if txt != "DONE" else 2700, TITAN, track=20)
        o.append(extrude(d, "#7A2E1F", 70, 110, 14, sw=60))
        o.append(outlined(d, fill, (CREAM, 60)))
        o.append(p(d, "none", "#FFFFFF", 14, 'opacity="0.35" transform="translate(-14 -18)"'))
    bx, by = 3300, 2150
    o.append(f'<rect x="{bx+60}" y="{by+90}" width="720" height="720" rx="120" fill="#7A2E1F"/><rect x="{bx}" y="{by}" width="720" height="720" rx="120" fill="#9ED8A5" stroke="{CREAM}" stroke-width="60"/>')
    o.append(f'<path d="M{bx+150} {by+380} l170 170 l300 -380" stroke="#245C3A" stroke-width="110" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    # pie slice
    px, py = 2250, 4000
    pts = f"{px-800},{py+350} {px+650},{py-380} {px+650},{py+500}"
    o.append(f'<polygon points="{pts}" fill="#7A2E1F" transform="translate(60 90)"/>')
    o.append(f'<polygon points="{pts}" fill="#F2A541" stroke="{CREAM}" stroke-width="55" stroke-linejoin="round"/>')
    o.append(f'<polygon points="{px-800},{py+350} {px+650},{py+330} {px+650},{py+500}" fill="#D9862F"/>')
    o.append(f'<rect x="{px+540}" y="{py-450}" width="260" height="1020" rx="130" fill="#C68A4E" stroke="{CREAM}" stroke-width="45"/>')
    for k in range(4):
        o.append(f'<circle cx="{px+380-k*190}" cy="{py-250+k*95}" r="{150-k*22}" fill="#FFFFFF"/>')
    o.append(p(warp(2250, 5050, "NOW PASS THE PIE", 380, 3400, TITAN, track=20), CREAM))
    return svg(*o)

# ------------------------------------------------------------ 5 groovy wave
def d5():
    o = []
    cx, cy, r = 2250, 2900, 1850
    o.append(f'<clipPath id="ck"><circle cx="{cx}" cy="{cy}" r="{r}"/></clipPath><g clip-path="url(#ck)">')
    sq = 370
    for i in range(-6, 6):
        for j in range(-6, 6):
            col = "#F3D9B1" if (i + j) % 2 == 0 else "#D9774B"
            o.append(f'<rect x="{cx+i*sq}" y="{cy+j*sq}" width="{sq+1}" height="{sq+1}" fill="{col}"/>')
    o.append("</g>")
    o.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{CREAM}" stroke-width="60"/>')
    for txt, base, cap, ph in (("WILL CHART", 2650, 740, 0.0), ("FOR PIE", 3650, 960, 1.6)):
        wave = (lambda ph: (lambda u: 120 * math.sin(2 * math.pi * 1.0 * u + ph)))(ph)
        d = warp(cx, base, txt, cap, 3650, SHRIK, yfn=wave, rotate=True, track=10)
        for k, c in enumerate(("#6B8F71", MUSTARD, RUST)):
            o.append(f'<g transform="translate({(3-k)*45} {(3-k)*45})">' + p(d, c, c, 40) + "</g>")
        o.append(outlined(d, CREAM, (INK, 70)))
    o.append(p(warp(cx, 5150, "THANKFUL MY CHARTING IS DONE", 210, 3600, GRAD, track=40), CREAM))
    return svg(*o)

DESIGNS = {"g1-thankful-charting-done-clipboard": (d1, False), "g2-thankful-grateful-charted-coquette": (d2, False),
           "g3-nurse-thanksgiving-shift-varsity": (d3, True), "g4-charting-done-pass-the-pie-puff": (d4, False),
           "g5-will-chart-for-pie-groovy": (d5, True)}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, worn)) in enumerate(DESIGNS.items()):
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s)
        if worn: img = wear(img, seed=40 + i)
        img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
