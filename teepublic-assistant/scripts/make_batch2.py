"""Batch 2 (plan day 9 Oct): idea E1 'Supervising the Christmas Tree', five distinct treatments.
Usage: python scripts/make_batch2.py batch-02
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import *

L, R = 330, W - 330
CREAM, MUSTARD, RUST, TEAL, RED, GREEN, DGREEN = "#F5E6C8", "#F2B134", "#D9552B", "#2A9D8F", "#E04B3C", "#3FA45F", "#245C3A"
CAT, CATD, CATB, EYE, PINK, INK = "#E8893B", "#B5581F", "#F7E7CF", "#9ED36A", "#F2A6A0", "#1B1410"

def tree(cx, base, h, w, ornaments=True, lights=True, outline=False, with_star=True):
    """Layered Christmas tree, `base` = bottom of trunk, `h` total height, `w` width of the lowest tier."""
    p = []
    tiers = 4
    trunk_h = h * 0.10
    body = h - trunk_h
    sw = 40 if outline else 0
    if not outline:
        p.append(f'<rect x="{cx - w*0.07}" y="{base - trunk_h}" width="{w*0.14}" height="{trunk_h}" rx="30" fill="#8A5A3B"/>')
    for i in range(tiers):
        top = base - trunk_h - body + i * body * 0.2
        bot = top + body * 0.34
        half = w / 2 * (0.42 + 0.58 * (i + 1) / tiers)
        pts = f'{cx},{top:.0f} {cx+half:.0f},{bot:.0f} {cx-half:.0f},{bot:.0f}'
        if outline:
            p.append(f'<polygon points="{pts}" fill="none" stroke="{CREAM}" stroke-width="46" stroke-linejoin="round"/>')
        else:
            p.append(f'<polygon points="{pts}" fill="{GREEN if i%2==0 else DGREEN}"/>')
    if ornaments and not outline:
        cols = [RED, MUSTARD, "#A9D6E5", RED, MUSTARD, "#A9D6E5", RED, MUSTARD]
        spots = [(-0.18, 0.28), (0.15, 0.18), (-0.30, 0.52), (0.28, 0.45), (0.0, 0.66), (-0.12, 0.84), (0.32, 0.78), (-0.38, 0.8)]
        for (dx, dy), c in zip(spots, cols):
            x, y = cx + dx * w * 0.7, base - trunk_h - body + dy * body
            p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{w*0.045:.0f}" fill="{c}"/><circle cx="{x-w*0.012:.0f}" cy="{y-w*0.014:.0f}" r="{w*0.012:.0f}" fill="#FFFFFF" opacity="0.6"/>')
    if with_star:
        p.append(star(cx, base - h - 40, w * 0.10, MUSTARD))
    return "".join(p)

def cat_head(cx, cy, s, hat=False):
    """Front-facing cat head (about 660*s wide)."""
    p = []
    for sg in (-1, 1):
        p.append(f'<polygon points="{cx+sg*310*s},{cy-60*s} {cx+sg*160*s},{cy-330*s} {cx+sg*40*s},{cy-230*s}" fill="{CAT}" stroke="{CAT}" stroke-width="30" stroke-linejoin="round"/>')
        p.append(f'<polygon points="{cx+sg*250*s},{cy-110*s} {cx+sg*170*s},{cy-250*s} {cx+sg*95*s},{cy-190*s}" fill="{PINK}"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy}" rx="340*s" ry="285*s" fill="{CAT}"/>'.replace('340*s', f'{340*s:.0f}').replace('285*s', f'{285*s:.0f}'))
    for k in (-1, 0, 1):
        p.append(f'<path d="M{cx+k*70*s} {cy-270*s} l{k*20*s} {95*s}" stroke="{CATD}" stroke-width="{42*s:.0f}" stroke-linecap="round"/>')
    p.append(f'<ellipse cx="{cx}" cy="{cy+90*s}" rx="{170*s:.0f}" ry="{125*s:.0f}" fill="{CATB}"/>')
    for sg in (-1, 1):
        ex, ey = cx + sg * 135 * s, cy - 30 * s
        p.append(f'<ellipse cx="{ex}" cy="{ey}" rx="{62*s:.0f}" ry="{72*s:.0f}" fill="{EYE}"/><ellipse cx="{ex}" cy="{ey}" rx="{20*s:.0f}" ry="{62*s:.0f}" fill="{INK}"/><circle cx="{ex-18*s}" cy="{ey-28*s}" r="{14*s:.0f}" fill="#FFFFFF"/>')
        for k in (-1, 1):
            p.append(f'<path d="M{cx+sg*95*s} {cy+110*s} l{sg*300*s} {k*45*s - 20*s}" stroke="{CREAM}" stroke-width="{12*s:.0f}" stroke-linecap="round" opacity="0.9"/>')
    p.append(f'<polygon points="{cx-38*s},{cy+55*s} {cx+38*s},{cy+55*s} {cx},{cy+100*s}" fill="{PINK}"/>')
    p.append(f'<path d="M{cx} {cy+100*s} q{-30*s} {50*s} {-70*s} {30*s} M{cx} {cy+100*s} q{30*s} {50*s} {70*s} {30*s}" stroke="{INK}" stroke-width="{12*s:.0f}" fill="none" stroke-linecap="round"/>')
    if hat:
        p.append(f'<path d="M {cx-300*s} {cy-150*s} C {cx-250*s} {cy-520*s} {cx+100*s} {cy-640*s} {cx+360*s} {cy-470*s} C {cx+230*s} {cy-400*s} {cx+280*s} {cy-260*s} {cx+300*s} {cy-150*s} Z" fill="{RED}"/>')
        p.append(f'<rect x="{cx-340*s}" y="{cy-230*s}" width="{680*s}" height="{130*s}" rx="{65*s}" fill="{CREAM}"/><circle cx="{cx+360*s}" cy="{cy-470*s}" r="{75*s}" fill="{CREAM}"/>')
    return "".join(p)

def cat_sit(cx, floor, s):
    """Sitting cat seen from the front, about 1250*s tall."""
    p = []
    bx, by = cx, floor - 360 * s
    p.append(f'<path d="M{cx+250*s} {floor-60*s} C {cx+700*s} {floor-60*s} {cx+760*s} {floor-520*s} {cx+520*s} {floor-760*s}" stroke="{CAT}" stroke-width="{120*s:.0f}" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M{cx+540*s} {floor-700*s} q{40*s} {-60*s} {110*s} {-40*s}" stroke="{CATD}" stroke-width="{120*s:.0f}" fill="none" stroke-linecap="round" opacity="0.0"/>')
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="{330*s:.0f}" ry="{370*s:.0f}" fill="{CAT}"/>')
    p.append(f'<ellipse cx="{bx}" cy="{by+60*s}" rx="{180*s:.0f}" ry="{270*s:.0f}" fill="{CATB}"/>')
    for sg in (-1, 1):
        p.append(f'<ellipse cx="{cx+sg*130*s}" cy="{floor-40*s}" rx="{110*s:.0f}" ry="{60*s:.0f}" fill="{CATB}"/>')
        for k in range(3):
            p.append(f'<path d="M{cx+sg*300*s} {by-120*s+k*110*s} l{-sg*90*s} {20*s}" stroke="{CATD}" stroke-width="{38*s:.0f}" stroke-linecap="round"/>')
    p.append(cat_head(cx, floor - 880 * s, s * 0.92))
    return "".join(p)

# ---- V1 ------------------------------------------------------------------------
def v1():
    p = [line(2250, 1080, "SUPERVISING", 780, R - L, MUSTARD, xscale=0.8)]
    p.append(stripes(1180, L + 300, R - 300, (RUST, TEAL, CREAM), h=30, gap=22))
    p.append(tree(1750, 4380, 2700, 1800))
    p.append(cat_sit(3200, 4380, 1.5))
    p.append(line(2250, 5000, "THE CHRISTMAS TREE", 380, R - L, CREAM, xscale=0.8, track=20))
    return svg(*p)

# ---- V2 badge ----------------------------------------------------------------------
def v2():
    cx, cy = 2250, 2550
    p = [f'<circle cx="{cx}" cy="{cy}" r="1950" fill="none" stroke="{CREAM}" stroke-width="70"/>',
         f'<circle cx="{cx}" cy="{cy}" r="1800" fill="none" stroke="{MUSTARD}" stroke-width="22"/>',
         f'<circle cx="{cx}" cy="{cy}" r="1190" fill="none" stroke="{CREAM}" stroke-width="22"/>']
    p.append(arc(cx, cy, 1290, "TREE SUPERVISOR", 300, CREAM, xscale=0.8, track=30, bold=8))
    p.append(arc(cx, cy, 1290, "ON DUTY SINCE DEC 1", 230, MUSTARD, xscale=0.8, track=26, bold=8, bottom=True))
    p.append(star(cx - 1495, cy + 10, 95, MUSTARD)); p.append(star(cx + 1495, cy + 10, 95, MUSTARD))
    p.append(cat_head(cx, cy + 140, 1.6, hat=True))
    p.append(line(2250, 5050, "NO ORNAMENT IS SAFE", 400, R - L, RED, xscale=0.8, track=20))
    p.append(stripes(5130, L + 700, R - 700, (MUSTARD, TEAL, CREAM), h=30, gap=22))
    return svg(*p)

# ---- V3 gravity test ---------------------------------------------------------------
def v3():
    p = [line(2250, 1250, "GRAVITY TEST", 900, R - L, MUSTARD, xscale=0.8)]
    p.append(f'<rect x="700" y="3030" width="2900" height="90" rx="45" fill="{CREAM}"/>')
    for k, (y, op) in enumerate([(3440, 0.55), (3880, 0.32), (4290, 0.16)]):
        p.append(f'<circle cx="3480" cy="{y}" r="260" fill="{RED}" opacity="{op}"/>')
    p.append(f'<path d="M3480 3190 L3480 3050" stroke="{MUSTARD}" stroke-width="10" opacity="0"/>')
    p.append(f'<rect x="3425" y="2740" width="110" height="80" rx="20" fill="{MUSTARD}"/><circle cx="3480" cy="2990" r="260" fill="{RED}"/><circle cx="3400" cy="2910" r="60" fill="#FFFFFF" opacity="0.5"/>')
    # cat peeking in from the left with one paw out
    p.append(f'<rect x="1250" y="2640" width="1200" height="300" rx="150" fill="{CAT}"/>')
    for x in (1700, 2050):
        p.append(f'<rect x="{x}" y="2640" width="60" height="300" rx="30" fill="{CATD}"/>')
    p.append(f'<circle cx="2470" cy="2790" r="250" fill="{CAT}"/>')
    for dy in (-150, -50, 50, 150):
        p.append(f'<circle cx="2690" cy="{2790+dy}" r="56" fill="{PINK}"/>')
    p.append(f'<ellipse cx="2480" cy="2800" rx="95" ry="75" fill="{PINK}"/>')
    p.append(cat_head(900, 2600, 1.15))
    p.append(f'<path d="M3430 3350 q-70 100 -10 220" stroke="{CREAM}" stroke-width="22" fill="none" stroke-dasharray="40 40" stroke-linecap="round" opacity="0.8"/>')
    p.append(line(2250, 5000, "ORNAMENT EDITION", 560, R - L, CREAM, xscale=0.8, track=20))
    p.append(stripes(5100, L + 500, R - 500, (RUST, TEAL, MUSTARD), h=30, gap=22))
    return svg(*p)

# ---- V4 caution --------------------------------------------------------------------
def v4():
    p = [line(2250, 1100, "CAUTION", 900, R - L, RED, xscale=0.8)]
    p.append(f'<clipPath id="hz"><rect x="{L}" y="1230" width="{R-L}" height="170" rx="40"/></clipPath><g clip-path="url(#hz)"><rect x="{L}" y="1230" width="{R-L}" height="170" fill="{CREAM}"/>')
    k = L - 200
    while k < R:
        p.append(f'<polygon points="{k},1400 {k+110},1400 {k+280},1230 {k+170},1230" fill="{RED}"/>'); k += 220
    p.append("</g>")
    p.append(f'<polygon points="2250,1650 3950,4300 550,4300" fill="none" stroke="{MUSTARD}" stroke-width="110" stroke-linejoin="round"/>')
    p.append(tree(1950, 4050, 1450, 1000, lights=False))
    p.append(cat_sit(2850, 4050, 0.78))
    p.append(line(2250, 4850, "CAT-SUPERVISED", 380, R - L, CREAM, xscale=0.8, track=20))
    p.append(line(2250, 5300, "CHRISTMAS TREE", 380, R - L, MUSTARD, xscale=0.8, track=20))
    return svg(*p)

# ---- V5 line art -------------------------------------------------------------------
def v5():
    p = [line(2250, 950, "THIS TREE", 700, R - L, CREAM, xscale=0.8)]
    p.append(tree(2250, 4650, 2450, 2300, ornaments=False, outline=True, with_star=False))
    p.append(cat_sit(2250, 2420, 0.85))
    for (x, y) in [(1550, 3600), (3000, 3850), (1750, 4150), (2700, 4350), (2250, 3600)]:
        p.append(f'<circle cx="{x}" cy="{y}" r="75" fill="{[RED, MUSTARD, PINK, MUSTARD, RED][(x//7)%5]}"/>')
    p.append(line(2250, 5000, "IS A CAT TOWER NOW", 420, R - L, MUSTARD, xscale=0.8, track=20))
    p.append(stripes(5100, L + 700, R - 700, (RUST, TEAL, CREAM), h=30, gap=22))
    return svg(*p)

DESIGNS = {"v1-retro-tree-and-cat": v1, "v2-official-tree-supervisor-badge": v2, "v3-gravity-test-ornament": v3,
           "v4-caution-cat-supervised-tree": v4, "v5-this-tree-is-a-cat-tower": v5}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, fn) in enumerate(DESIGNS.items()):
        d = out / slug; d.mkdir(parents=True, exist_ok=True)
        s = fn(); (d / "design.svg").write_text(s)
        clean = render(s); worn = wear(clean, seed=i + 11)
        clean.save(d / "design_clean.png"); worn.save(d / "design.png")
        on_color(worn).save(d / "preview-on-black.png"); print(slug)
