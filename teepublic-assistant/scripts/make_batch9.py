"""Batch 9 (plan 17 Oct): idea H1 'Surviving the Holiday Countdown' (teachers x Christmas).
Five styles: chalkboard, advent countdown planner, multiple-choice worksheet, hall pass tag, survival-kit icon grid.
Usage: python scripts/make_batch9.py batch-09
"""
import math, random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, star, sparkle, svg, render, on_color, W, H
from fx import warp, p, outlined
from motifs import apple, pencil, mug, candy_cane, at

CAVEAT, ELITE, GRAD, FRED, ANTON, PLAY, BEBAS, BRUSH = (font("caveat-latin-700-normal"), font("special-elite-latin-400-normal"),
    font("graduate-latin-400-normal"), font("fredoka-latin-700-normal"), font("anton-latin-400-normal"),
    font("playfair-display-latin-700-normal"), font("bebas-neue-latin-400-normal"), font("caveat-brush-latin-400-normal"))
CREAM, RED, GREEN, GOLD, INK, BOARD, WOOD = "#F4EFE6", "#D7263D", "#2E8A55", "#F2B134", "#2A2420", "#2F4A3A", "#A8743F"

def chalky(d, color, seed, bbox):
    rnd = random.Random(seed); x0, y0, x1, y1 = bbox; cid = f"ch{seed}"
    o = [p(d, color), f'<clipPath id="{cid}"><path d="{d}"/></clipPath><g clip-path="url(#{cid})">']
    for _ in range(1600):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{rnd.uniform(6, 22):.0f}" ry="{rnd.uniform(3, 8):.0f}" fill="{BOARD}" opacity="0.55" transform="rotate({rnd.uniform(-30, 30):.0f} {x:.0f} {y:.0f})"/>')
    return "".join(o) + "</g>"

# 1 chalkboard
def d1():
    o = [f'<rect x="300" y="500" width="3900" height="4500" rx="60" fill="{WOOD}"/>', f'<rect x="460" y="660" width="3580" height="4180" rx="20" fill="{BOARD}"/>']
    o.append(chalky(warp(2250, 1450, "surviving the", 420, 3000, CAVEAT), CREAM, 1, (500, 900, 4000, 1600)))
    o.append(chalky(warp(2250, 2250, "HOLIDAY", 760, 3200, BRUSH), "#F7C6D0", 2, (500, 1400, 4000, 2400)))
    o.append(chalky(warp(2250, 3000, "countdown", 620, 3200, CAVEAT), "#BFE3C9", 3, (500, 2300, 4000, 3150)))
    # tally marks
    for g in range(3):
        gx = 800 + g * 600
        for k in range(4):
            o.append(f'<line x1="{gx+k*110}" y1="3350" x2="{gx+k*110+15}" y2="3800" stroke="{CREAM}" stroke-width="34" stroke-linecap="round" opacity="0.9"/>')
        o.append(f'<line x1="{gx-60}" y1="3720" x2="{gx+420}" y2="3420" stroke="{CREAM}" stroke-width="34" stroke-linecap="round" opacity="0.9"/>')
    o.append(chalky(warp(3250, 3700, "days left: 3", 260, 1300, CAVEAT), GOLD, 4, (2700, 3400, 4000, 3800)))
    o.append(f'<rect x="900" y="4840" width="2700" height="110" rx="30" fill="#8A5A2F"/><rect x="1300" y="4780" width="300" height="70" rx="20" fill="{CREAM}"/><rect x="2900" y="4790" width="380" height="60" rx="20" fill="#F7C6D0"/>')
    o.append(at(3700, 4400, apple(0.9)))
    return svg(*o)

# 2 advent countdown planner
def d2():
    o = [p(warp(2250, 900, "HOLIDAY COUNTDOWN", 380, 3700, ANTON, track=40), CREAM), p(warp(2250, 1300, "teacher edition", 280, 2400, CAVEAT), GOLD)]
    x0, y0, cw, chh = 600, 1550, 550, 550
    for i in range(24):
        r, c = divmod(i, 6)
        x, y = x0 + c * cw, y0 + r * chh
        fill = ("#F4EFE6", "#F7C6D0", "#BFE3C9", "#FCE3A6")[(r + c) % 4]
        o.append(f'<rect x="{x+20}" y="{y+20}" width="{cw-40}" height="{chh-40}" rx="40" fill="{fill}"/>')
        o.append(p(warp(x + 120, y + 160, str(i + 1), 90, 200, FRED), INK))
        if i < 21:
            o.append(f'<path d="M{x+120} {y+170} L{x+cw-120} {y+chh-120} M{x+cw-120} {y+170} L{x+120} {y+chh-120}" stroke="{RED}" stroke-width="44" stroke-linecap="round"/>')
        elif i == 23:
            o.append(at(x + cw / 2, y + chh / 2 + 30, star(0, 0, 150, GOLD)))
    o.append(p(warp(2250, 4300, "SURVIVING THE HOLIDAY COUNTDOWN", 200, 3600, GRAD, track=40), CREAM))
    o.append(at(1000, 4800, candy_cane(0.9), rot=-15)); o.append(at(3500, 4850, apple(0.8)))
    return svg(*o)

# 3 multiple-choice worksheet
def d3():
    paper, blue, pink = "#FBF8F0", "#9DB8E0", "#E88AA0"
    x0, y0, w, h = 550, 450, 3400, 4600
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="20" fill="{paper}"/>']
    for y in range(y0 + 500, y0 + h - 100, 230):
        o.append(f'<line x1="{x0}" y1="{y}" x2="{x0+w}" y2="{y}" stroke="{blue}" stroke-width="8"/>')
    o.append(f'<line x1="{x0+420}" y1="{y0}" x2="{x0+420}" y2="{y0+h}" stroke="{pink}" stroke-width="10"/>')
    for k in range(3):
        o.append(f'<circle cx="{x0+180}" cy="{y0+900+k*1300}" r="70" fill="#141414" opacity="0.85"/>')
    o.append(p(warp(x0 + 1150, y0 + 330, "Name: Teacher", 160, 1400, CAVEAT), INK))
    o.append(p(warp(x0 + 2500, y0 + 330, "Date: Dec 18", 160, 1100, CAVEAT), INK))
    o.append(p(warp(x0 + 1950, y0 + 920, "1. How many days until winter break?", 140, 2800, ELITE), INK))
    for k, (opt, chosen) in enumerate((("a) too many", False), ("b) still too many", False), ("c) surviving the countdown", True))):
        y = y0 + 1400 + k * 460
        o.append(p(warp(x0 + 600 + 1000, y, opt, 150, 2500, ELITE), INK))
        if chosen:
            o.append(f'<ellipse cx="{x0+1600}" cy="{y-55}" rx="1300" ry="200" fill="none" stroke="{RED}" stroke-width="22" transform="rotate(-2 {x0+1550} {y-55})"/>')
    o.append(p(warp(x0 + 1950, y0 + 2950, "2. Show your work:", 140, 2800, ELITE), INK))
    o.append(p(warp(x0 + 1600, y0 + 3450, "coffee + candy canes = joy", 200, 2400, CAVEAT), "#3C5BA9"))
    o.append(f'<circle cx="{x0+w-480}" cy="{y0+3950}" r="320" fill="none" stroke="{RED}" stroke-width="30"/>')
    o.append(p(warp(x0 + w - 480, y0 + 4050, "A+", 280, 500, CAVEAT), RED))
    o.append(p(warp(x0 + 1300, y0 + 4250, "great survival skills!", 150, 1900, CAVEAT), RED))
    return svg(*o)

# 4 hall pass tag
def d4():
    wood, dark = "#C98B4E", "#7A4A24"
    o = [f'<path d="M2250 300 C 2200 600 2050 700 2000 900" stroke="{CREAM}" stroke-width="30" fill="none"/><path d="M2250 300 C 2300 600 2450 700 2500 900" stroke="{CREAM}" stroke-width="30" fill="none"/>']
    o.append(f'<path d="M1050 900 L3450 900 Q3650 900 3650 1100 L3650 4700 Q3650 4900 3450 4900 L1050 4900 Q850 4900 850 4700 L850 1100 Q850 900 1050 900 Z" fill="{wood}"/>')
    for k in range(9):
        y = 1050 + k * 430
        o.append(f'<path d="M900 {y} C 1600 {y-60} 2900 {y+60} 3600 {y}" stroke="{dark}" stroke-width="10" fill="none" opacity="0.35"/>')
    o.append(f'<circle cx="2250" cy="1150" r="110" fill="#141414"/><circle cx="2250" cy="1150" r="140" fill="none" stroke="#D9D2C3" stroke-width="30"/>')
    o.append(f'<rect x="1100" y="1500" width="2300" height="3150" rx="40" fill="none" stroke="{CREAM}" stroke-width="26" stroke-dasharray="60 30"/>')
    o.append(p(warp(2250, 2250, "HALL PASS", 620, 2100, ANTON, track=40), CREAM))
    o.append(p(warp(2250, 2700, "destination:", 250, 1600, CAVEAT), "#3A2410"))
    o.append(p(warp(2250, 3400, "WINTER BREAK", 480, 2100, ANTON, track=30), RED))
    o.append(p(warp(2250, 3950, "surviving the holiday countdown", 190, 2000, CAVEAT), "#3A2410"))
    o.append(at(2250, 4350, candy_cane(0.7), rot=90))
    return svg(*o)

# 5 survival kit icon grid
def d5():
    o = [p(warp(2250, 950, "TEACHER", 500, 3200, ANTON, track=60), CREAM), p(warp(2250, 1500, "Holiday Survival Kit", 400, 3600, PLAY), GOLD)]
    items = [(mug(1.3), "COFFEE"), (candy_cane(1.1), "CANDY CANES"), (pencil(1.0), "RED PEN"), (apple(1.3), "SNACKS"), (star(0, 0, 260, GOLD), "PATIENCE"), (f'<g transform="scale(1.3)"><rect x="-200" y="-150" width="400" height="300" rx="30" fill="#D7263D"/><rect x="-30" y="-150" width="60" height="300" fill="{GOLD}"/><rect x="-200" y="-30" width="400" height="60" fill="{GOLD}"/><path d="M0 -150 c-80 -120 -200 -60 -120 0 M0 -150 c80 -120 200 -60 120 0" stroke="{GOLD}" stroke-width="30" fill="none"/></g>', "WINTER BREAK")]
    for i, (icon, label) in enumerate(items):
        r, c = divmod(i, 3)
        x, y = 950 + c * 1300, 2450 + r * 1500
        o.append(f'<circle cx="{x}" cy="{y}" r="520" fill="none" stroke="{CREAM}" stroke-width="16" stroke-dasharray="40 26"/>')
        o.append(at(x, y, icon, rot=-30 if label == "RED PEN" else 0))
        o.append(p(warp(x, y + 760, label, 140, 1150, GRAD, track=30), CREAM))
    o.append(f'<path d="M3880 3640 l70 70 l150 -170" stroke="{GREEN}" stroke-width="0" fill="none"/>')
    o.append(p(warp(2250, 5200, "SURVIVING THE HOLIDAY COUNTDOWN", 170, 3600, GRAD, track=40), GOLD))
    return svg(*o)

DESIGNS = {"h1-surviving-holiday-countdown-chalkboard": d1, "h2-holiday-countdown-teacher-calendar": d2, "h3-winter-break-worksheet": d3,
           "h4-hall-pass-to-winter-break": d4, "h5-teacher-holiday-survival-kit": d5}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for slug, fn in DESIGNS.items():
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s); img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
