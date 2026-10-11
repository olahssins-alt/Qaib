"""Batch 5 (plan 13 Oct): idea G1 night-shift nurses x Christmas, five new styles:
neon motel sign, tarot card, celestial constellation, Y2K chrome, risograph time card.
Usage: python scripts/make_batch5.py batch-05
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, arc, star, sparkle, svg, render, wear, on_color, W, H
from fx import warp, p, outlined, extrude, neon_glow, heart
from motifs import at

MONO, RIGHT, PAC, PLAY, PLAY_IT, ABRIL, CORM, TITAN, ELITE, GRAD = (font("monoton-latin-400-normal"), font("righteous-latin-400-normal"),
    font("pacifico-latin-400-normal"), font("playfair-display-latin-700-normal"), font("playfair-display-latin-900-italic"),
    font("abril-fatface-latin-400-normal"), font("cormorant-garamond-latin-600-italic"), font("titan-one-latin-400-normal"),
    font("special-elite-latin-400-normal"), font("graduate-latin-400-normal"))
CREAM, GOLD, NAVY = "#F4ECDD", "#E2B355", "#1C2347"

def crescent_path(cx, cy, r1, dx, dy, r2):
    d = math.hypot(dx, dy); a = (r1**2 - r2**2 + d**2) / (2 * d); h = math.sqrt(r1**2 - a**2)
    mx, my = cx + a * dx / d, cy + a * dy / d; ox, oy = -dy / d * h, dx / d * h
    p1, p2 = (mx + ox, my + oy), (mx - ox, my - oy)
    return f"M{p1[0]:.0f} {p1[1]:.0f} A{r1} {r1} 0 1 1 {p2[0]:.0f} {p2[1]:.0f} A{r2} {r2} 0 0 0 {p1[0]:.0f} {p1[1]:.0f} Z"

# 1 neon motel sign
def d1():
    pink, cyan, yellow, green, red = "#FF4FA3", "#3CF2FF", "#FFE45C", "#4DFF7A", "#FF5050"
    o = []
    # arrow sign outline
    sign = "M600 1300 L3500 1300 L3900 2150 L3500 3000 L600 3000 Z"
    o.append(p(sign, "none", pink, 55))
    o.append(p("M720 1420 L3420 1420 L3760 2150 L3420 2880 L720 2880 Z", "none", pink, 18))
    o.append(p(warp(2150, 2050, "NIGHT SHIFT", 560, 2700, MONO, track=10), cyan))
    o.append(p(warp(2150, 2650, "OPEN ALL NIGHT", 300, 2500, RIGHT, track=60), "none", yellow, 26))
    # neon light string
    pts = [(500 + i * 350, 3500 + 120 * math.sin(i * 0.9)) for i in range(11)]
    o.append(p("M" + " L".join(f"{x:.0f} {y:.0f}" for x, y in pts), "none", green, 16))
    for i, (x, y) in enumerate(pts[1:-1]):
        c = (red, yellow, cyan, pink)[i % 4]
        o.append(f'<ellipse cx="{x:.0f}" cy="{y+90:.0f}" rx="55" ry="85" fill="none" stroke="{c}" stroke-width="22"/>')
    o.append(p(warp(2250, 4700, "even on Christmas", 520, 3700, PAC), "none", pink, 30))
    o.append(star(3900, 900, 120, yellow).replace('fill="', 'fill="none" stroke-width="22" stroke="'))
    o.append(p(crescent_path(650, 850, 230, 110, -70, 200), "none", yellow, 22))
    return svg(*o)

# 2 tarot card
def d2():
    o = []
    x0, y0, w, h = 750, 300, 3000, 4900
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="90" fill="{CREAM}"/>')
    o.append(f'<rect x="{x0+90}" y="{y0+90}" width="{w-180}" height="{h-180}" rx="50" fill="none" stroke="{GOLD}" stroke-width="22"/>')
    o.append(f'<rect x="{x0+160}" y="{y0+420}" width="{w-320}" height="{h-1180}" rx="30" fill="{NAVY}"/>')
    o.append(p(warp(2250, y0 + 330, "XII", 180, 600, PLAY, track=40), NAVY))
    ax, ay = 2250, 2350
    # sky
    for x, y, s in ((1250, 1150, 60), (3150, 1050, 80), (1500, 1900, 40), (3000, 2100, 50), (1150, 3000, 50), (3350, 3100, 60), (2600, 1300, 35)):
        o.append(sparkle(x, y, s, CREAM))
    o.append(p(crescent_path(ax, ay - 250, 620, 260, -160, 560), GOLD))
    # stethoscope hanging from the moon tip
    o.append(f'<path d="M2050 1950 C 1900 2500 1950 3000 2250 3150 C 2550 3000 2600 2500 2450 2050" stroke="{CREAM}" stroke-width="40" fill="none" stroke-linecap="round"/>')
    o.append(f'<circle cx="2050" cy="1950" r="45" fill="{CREAM}"/><circle cx="2450" cy="2050" r="45" fill="{CREAM}"/>')
    o.append(f'<path d="M2250 3150 L2250 3450" stroke="{CREAM}" stroke-width="40" stroke-linecap="round"/><circle cx="2250" cy="3560" r="120" fill="{GOLD}" stroke="{CREAM}" stroke-width="30"/>')
    # coffee cup
    o.append(f'<path d="M1150 3700 h420 v260 a120 120 0 0 1 -120 120 h-180 a120 120 0 0 1 -120 -120 Z" fill="#C95B4A"/><path d="M1570 3760 a80 80 0 0 1 0 160" stroke="#C95B4A" stroke-width="40" fill="none"/>')
    o.append(f'<path d="M1280 3640 q-40 -80 0 -160 M1420 3640 q-40 -80 0 -160" stroke="{CREAM}" stroke-width="22" fill="none" stroke-linecap="round" opacity="0.8"/>')
    # holly
    hx, hy = 3150, 3850
    for a in (-30, 30):
        o.append(f'<ellipse cx="{hx}" cy="{hy}" rx="200" ry="80" fill="#3E8A5A" transform="rotate({a} {hx} {hy-40})"/>')
    for dx, dy in ((-40, -60), (40, -50), (0, -10)):
        o.append(f'<circle cx="{hx+dx}" cy="{hy-80+dy}" r="55" fill="#D7263D"/>')
    o.append(f'<rect x="{x0+160}" y="{y0+h-680}" width="{w-320}" height="420" rx="30" fill="none" stroke="{GOLD}" stroke-width="16"/>')
    o.append(p(warp(2250, y0 + h - 380, "THE NIGHT NURSE", 230, w - 500, PLAY, track=70), NAVY))
    return svg(*o)

# 3 celestial constellation: EKG line drawn as a constellation
def d3():
    o = []
    o.append(p(warp(2250, 1200, "Silent Night?", 560, 3800, PLAY_IT), CREAM))
    o.append(p(crescent_path(3550, 1900, 330, 140, -90, 290), GOLD))
    pts = [(450, 3000), (1300, 3000), (1550, 2700), (1800, 3000), (2000, 3000), (2200, 2050), (2450, 3650), (2700, 3000), (3000, 3000), (3250, 2750), (3500, 3000), (4050, 3000)]
    o.append(p("M" + " L".join(f"{x} {y}" for x, y in pts), "none", CREAM, 14))
    for i, (x, y) in enumerate(pts):
        o.append(sparkle(x, y, 95 if i in (5, 6) else 60, GOLD))
    for x, y in ((800, 1900), (1400, 2200), (2900, 2300), (3900, 3600), (900, 3900), (3100, 4000), (2000, 4300)):
        o.append(f'<circle cx="{x}" cy="{y}" r="22" fill="{CREAM}"/>')
    o.append(p(warp(2250, 4800, "not on my unit", 470, 3400, CORM, track=20), GOLD))
    o.append(p(warp(2250, 5250, "NIGHT SHIFT NURSE", 150, 2400, PLAY, track=140), CREAM))
    return svg(*o)

# 4 Y2K chrome
CHROME = ('<linearGradient id="chrome" x1="0" y1="0" x2="0" y2="1">'
          '<stop offset="0" stop-color="#FFFFFF"/><stop offset="0.38" stop-color="#C9D6EE"/><stop offset="0.5" stop-color="#5E6E94"/>'
          '<stop offset="0.56" stop-color="#E8EEFF"/><stop offset="1" stop-color="#8EA3CC"/></linearGradient>')
def chrome_text(txt, base, cap, width, f=TITAN):
    d = warp(2250, base, txt, cap, width, f, track=20)
    top, bot = base - cap * 1.05, base + cap * 0.08
    grad = CHROME.replace('id="chrome"', f'id="ch{base}" gradientUnits="userSpaceOnUse" x1="0" y1="{top:.0f}" x2="0" y2="{bot:.0f}"').replace(' x1="0" y1="0" x2="0" y2="1"', "")
    return f'<defs>{grad}</defs>' + p(d, "#0E1530", "#0E1530", 70) + p(d, f"url(#ch{base})", "#FFFFFF", 10)
def d4():
    pink, cyan = "#FF7AD9", "#6FF3FF"
    o = [p(warp(2250, 1150, "SANTA WORKS ONE NIGHT.", 230, 3700, GRAD, track=40), CREAM)]
    o.append(chrome_text("WE WORK", 2350, 780, 3800))
    o.append(chrome_text("TWELVE.", 3700, 1000, 3900))
    for x, y, s, c in ((600, 1700, 170, cyan), (3950, 1650, 130, pink), (4000, 3900, 200, cyan), (500, 4100, 120, pink), (2250, 4500, 90, CREAM), (1300, 1500, 70, CREAM)):
        o.append(sparkle(x, y, s, c))
    o.append(p(warp(2250, 4950, "NIGHT SHIFT NURSE · DEC 24", 150, 3600, GRAD, track=50), pink))
    return svg(*o)

# 5 risograph time card
def d5():
    blue, pink, paper = "#2F55B0", "#FF48A5", "#F4EEDC"
    o = []
    x0, y0, w, h = 800, 600, 2900, 4300
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="40" fill="{paper}"/>')
    o.append(f'<circle cx="2250" cy="{y0+170}" r="70" fill="#151515" opacity="0.0"/>')
    o.append(p(warp(2250, y0 + 420, "TIME CARD", 250, 2400, ELITE, track=60), blue))
    o.append(p(warp(2250, y0 + 640, "NAME: NIGHT SHIFT NURSE", 120, 2400, ELITE, track=20), blue))
    rows = [("DEC 24", "IN", "7:00 PM"), ("DEC 25", "OUT", "7:00 AM"), ("", "", ""), ("", "", ""), ("", "", "")]
    for i, (dte, io, t) in enumerate(rows):
        y = y0 + 900 + i * 420
        o.append(f'<line x1="{x0+120}" y1="{y}" x2="{x0+w-120}" y2="{y}" stroke="{blue}" stroke-width="12"/>')
        for xx in (x0 + 900, x0 + 1550):
            o.append(f'<line x1="{xx}" y1="{y}" x2="{xx}" y2="{y+420}" stroke="{blue}" stroke-width="8"/>')
        if dte:
            # riso misregistration: pink ghost under blue
            for c, dx in ((pink, 14), (blue, 0)):
                o.append(f'<g transform="translate({dx} {dx})">' + p(warp(x0 + 510, y + 280, dte, 150, 700, ELITE), c) + p(warp(x0 + 1225, y + 280, io, 150, 500, ELITE), c) + p(warp(x0 + 2100, y + 280, t, 150, 900, ELITE), c) + "</g>")
    o.append(f'<line x1="{x0+120}" y1="{y0+900+5*420}" x2="{x0+w-120}" y2="{y0+900+5*420}" stroke="{blue}" stroke-width="12"/>')
    # stamp
    sx, sy = 2650, 3600
    g = [f'<circle cx="{sx}" cy="{sy}" r="620" fill="none" stroke="{pink}" stroke-width="40"/>', f'<circle cx="{sx}" cy="{sy}" r="520" fill="none" stroke="{pink}" stroke-width="14"/>',
         arc(sx, sy, 350, "HOLIDAY", 115, pink, font=GRAD, xscale=1.0, track=30, bold=0),
         arc(sx, sy, 350, "APPROVED", 90, pink, font=GRAD, xscale=1.0, track=18, bold=0, bottom=True),
         p(warp(sx, sy + 85, "12 HRS", 200, 560, GRAD, track=20), pink), star(sx - 440, sy, 45, pink), star(sx + 440, sy, 45, pink)]
    o.append(f'<g transform="rotate(-14 {sx} {sy})" opacity="0.92">' + "".join(g) + "</g>")
    o.append(p(warp(2250, 5350, "MERRY CHRISTMAS FROM THE NIGHT SHIFT", 130, 3600, ELITE, track=30), CREAM))
    return svg(*o)

DESIGNS = {"n1-open-all-night-even-on-christmas-neon": (d1, "neon"), "n2-the-night-nurse-tarot": (d2, None),
           "n3-silent-night-not-on-my-unit-celestial": (d3, None), "n4-santa-works-one-night-y2k-chrome": (d4, None),
           "n5-holiday-night-shift-time-card-riso": (d5, None)}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, mode)) in enumerate(DESIGNS.items()):
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s)
        if mode == "neon": img = neon_glow(img)
        elif mode == "wear": img = wear(img, seed=80 + i)
        img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
