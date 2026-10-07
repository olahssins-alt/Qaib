# Regenerate the hand-built designs in ready-to-upload/:  python scripts/make_ready_designs.py ready-to-upload
# Needs: pip install cairosvg fonttools ; fonts Inter Black and DejaVu Serif Bold (paths below).
"""Hand-built SVG designs, 4500x5500, transparent, for dark shirts."""
import math, sys
from pathlib import Path
import cairosvg

OUT = Path(sys.argv[1])
W, H = 4500, 5500
HEAD = f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
INTER = "/usr/share/fonts/opentype/inter/Inter-Black.otf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
_FONTS = {}

def _font(path):
    if path not in _FONTS:
        _FONTS[path] = TTFont(path)
    return _FONTS[path]

def text(x, y, s, size, fill, width, font=INTER, extra=""):
    """Text as vector outlines, centered on x with baseline y, shrunk to fit `width`."""
    f = _font(font)
    upm = f["head"].unitsPerEm
    cmap, gs, hmtx = f.getBestCmap(), f.getGlyphSet(), f["hmtx"]
    names = [cmap[ord(ch)] for ch in s]
    adv = sum(hmtx[n][0] for n in names)
    scale = min(size / upm, width / adv)
    start = x - adv * scale / 2
    pen = SVGPathPen(gs)
    cursor = 0
    for n in names:
        gs[n].draw(TransformPen(pen, (scale, 0, 0, -scale, start + cursor * scale, y)))
        cursor += hmtx[n][0]
    return f'<path d="{pen.getCommands()}" fill="{fill}" {extra}/>' 

# ---------- 1. JINGLE BAMS (mahjong) ----------
def jingle_bams():
    cream, red, green, dgreen, gold = "#F4EAD5", "#D94A3D", "#3F9A5C", "#2A6B40", "#F2B84B"
    p = [HEAD]
    p.append(text(2250, 1020, "JINGLE", 900, cream, 3500))
    # mahjong tile
    tx, ty, tw, th = 1150, 1300, 2200, 2700
    p.append(f'<rect x="{tx+60}" y="{ty+90}" width="{tw}" height="{th}" rx="230" fill="{dgreen}"/>')  # tile depth
    p.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="230" fill="{cream}"/>')
    p.append(f'<rect x="{tx+110}" y="{ty+110}" width="{tw-220}" height="{th-220}" rx="160" fill="none" stroke="{green}" stroke-width="40"/>')
    # bamboo sticks stacked as a tree: rows of 1,2,3,4 sticks
    cx = tx + tw / 2
    stick_w, stick_h, gap = 230, 430, 70
    rows = [1, 2, 3, 4]
    top = ty + 520
    for r, n in enumerate(rows):
        y = top + r * (stick_h + 40)
        total = n * stick_w + (n - 1) * gap
        for i in range(n):
            x = cx - total / 2 + i * (stick_w + gap)
            p.append(f'<rect x="{x}" y="{y}" width="{stick_w}" height="{stick_h}" rx="110" fill="{green}"/>')
            p.append(f'<rect x="{x}" y="{y + stick_h/2 - 22}" width="{stick_w}" height="44" fill="{cream}"/>')
            p.append(f'<rect x="{x + stick_w/2 - 18}" y="{y + 40}" width="36" height="{stick_h - 80}" rx="18" fill="{dgreen}" opacity="0.55"/>')
            if (r + i) % 2 == 1 and r > 0:
                p.append(f'<circle cx="{x + stick_w/2}" cy="{y + stick_h - 60}" r="70" fill="{red}"/>')
    # trunk
    p.append(f'<rect x="{cx-110}" y="{top + 4*(stick_h+40)}" width="220" height="170" rx="40" fill="#8A5A3B"/>')
    # star
    sx, sy, R, r_ = cx, ty + 330, 230, 95
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rad = R if k % 2 == 0 else r_
        pts.append(f"{sx + rad*math.cos(a):.0f},{sy + rad*math.sin(a):.0f}")
    p.append(f'<polygon points="{" ".join(pts)}" fill="{gold}"/>')
    p.append(text(2250, 4880, "BAMS", 1000, red, 3300))
    p.append("</svg>")
    return "".join(p)

# ---------- 2. KITCHEN CLOSED FOR THE HOLIDAYS (pickleball) ----------
def kitchen_closed():
    white, red, ball, ballh, wood, green = "#F7F3EA", "#E0443E", "#D7F23B", "#A9C21F", "#C98B55", "#3F9A5C"
    p = [HEAD]
    # pickleball with santa hat
    bx, by, br = 2250, 1350, 820
    p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{ball}"/>')
    for (dx, dy) in [(-380,-60),(-120,-300),(200,-200),(420,120),(80,120),(-260,300),(160,450),(-480,-380)]:
        p.append(f'<circle cx="{bx+dx}" cy="{by+dy+80}" r="85" fill="{ballh}"/>')
    # hat
    p.append(f'<path d="M {bx-720} {by-330} C {bx-620} {by-1000} {bx+150} {by-1250} {bx+820} {by-1080} C {bx+560} {by-900} {bx+640} {by-600} {bx+720} {by-330} Z" fill="{red}"/>')
    p.append(f'<circle cx="{bx+820}" cy="{by-1080}" r="170" fill="{white}"/>')
    p.append(f'<rect x="{bx-860}" y="{by-450}" width="1720" height="300" rx="150" fill="{white}"/>')
    # sign
    sx, sy, sw, sh = 450, 2450, 3600, 1650
    p.append(f'<line x1="{sx+500}" y1="{sy}" x2="{2250}" y2="{sy-180}" stroke="{white}" stroke-width="40"/>')
    p.append(f'<line x1="{sx+sw-500}" y1="{sy}" x2="{2250}" y2="{sy-180}" stroke="{white}" stroke-width="40"/>')
    p.append(f'<circle cx="2250" cy="{sy-180}" r="55" fill="{white}"/>')
    p.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="120" fill="{wood}"/>')
    p.append(f'<rect x="{sx+90}" y="{sy+90}" width="{sw-180}" height="{sh-180}" rx="70" fill="none" stroke="{white}" stroke-width="45"/>')
    p.append(text(2250, sy+760, "KITCHEN", 620, white, 2900))
    p.append(text(2250, sy+1400, "CLOSED", 620, red, 2900))
    # holly on sign corner
    for ang in (-35, 35):
        p.append(f'<ellipse cx="{sx+330}" cy="{sy+10}" rx="230" ry="95" fill="{green}" transform="rotate({ang} {sx+330} {sy+10})"/>')
    for (dx, dy) in [(-40,-20),(60,10),(10,70)]:
        p.append(f'<circle cx="{sx+330+dx}" cy="{sy+10+dy}" r="60" fill="{red}"/>')
    p.append(text(2250, 4700, "FOR THE HOLIDAYS", 440, white, 3600))
    p.append("</svg>")
    return "".join(p)

# ---------- 3. HOME FOR THE HOLIDAYS (and not leaving) ----------
def home_holidays():
    cream, yellow, ice, roof, door = "#F4EAD5", "#F2C14E", "#A9D6E5", "#D94A3D", "#2E5E7E"
    p = [HEAD]
    p.append(text(2250, 900, "HOME FOR THE", 520, cream, 3300, font=SERIF))
    p.append(text(2250, 1620, "HOLIDAYS", 820, yellow, 3700, font=SERIF))
    # house
    hx, hy, hw, hh = 1200, 3000, 2100, 1450
    p.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="40" fill="{cream}"/>')
    # chimney (behind roof), roof, then snow cap with a wavy edge
    p.append(f'<rect x="{hx+1450}" y="{hy-700}" width="260" height="600" fill="{roof}"/>')
    p.append(f'<rect x="{hx+1410}" y="{hy-760}" width="340" height="110" rx="40" fill="#FFFFFF"/>')
    ax, ay = 2250, hy - 850
    lx, rx, by_ = hx - 220, hx + hw + 220, hy + 40
    p.append(f'<polygon points="{lx},{by_} {ax},{ay} {rx},{by_}" fill="{roof}"/>')
    t = 0.42
    l2 = (ax + t * (lx - ax), ay + t * (by_ - ay))
    r2 = (ax + t * (rx - ax), ay + t * (by_ - ay))
    span = r2[0] - l2[0]
    waves = "".join(
        f" Q {r2[0] - span*(i+0.5)/5:.0f} {r2[1] + (120 if i % 2 == 0 else 40):.0f} {r2[0] - span*(i+1)/5:.0f} {r2[1]:.0f}"
        for i in range(5))
    p.append(f'<path d="M {ax} {ay} L {r2[0]:.0f} {r2[1]:.0f}{waves} Z" fill="#FFFFFF"/>')
    for (dx, dy, r) in [(0, -880, 75), (80, -1010, 95), (20, -1160, 110)]:
        p.append(f'<circle cx="{hx+1580+dx}" cy="{hy+dy}" r="{r}" fill="{ice}"/>')
    # windows (lit)
    for wx in (hx+230, hx+hw-230-520):
        p.append(f'<rect x="{wx}" y="{hy+300}" width="520" height="520" rx="30" fill="{yellow}"/>')
        p.append(f'<rect x="{wx+245}" y="{hy+300}" width="30" height="520" fill="{door}"/>')
        p.append(f'<rect x="{wx}" y="{hy+545}" width="520" height="30" fill="{door}"/>')
    # door with do-not-disturb hanger
    dx = 2250 - 230
    p.append(f'<rect x="{dx}" y="{hy+620}" width="460" height="880" rx="40" fill="{door}"/>')
    p.append(f'<circle cx="{dx+380}" cy="{hy+1080}" r="35" fill="{yellow}"/>')
    p.append(f'<rect x="{dx+90}" y="{hy+760}" width="280" height="200" rx="30" fill="{cream}"/>')
    p.append(text(2250, hy+840, "DO NOT", 70, door, 220))
    p.append(text(2250, hy+925, "DISTURB", 70, door, 240))
    # snowflakes
    for (fx, fy, s) in [(600, 2300, 90), (3900, 2200, 110), (500, 3600, 70), (4000, 3500, 80), (3700, 1900, 60), (800, 1950, 60)]:
        for a in (0, 60, 120):
            p.append(f'<line x1="{fx-s}" y1="{fy}" x2="{fx+s}" y2="{fy}" stroke="{ice}" stroke-width="28" stroke-linecap="round" transform="rotate({a} {fx} {fy})"/>')
    p.append(text(2250, 5000, "(AND NOT LEAVING)", 330, ice, 3100))
    p.append("</svg>")
    return "".join(p)

DESIGNS = {"01-jingle-bams-mahjong": jingle_bams, "02-kitchen-closed-pickleball": kitchen_closed,
           "03-home-for-the-holidays-introvert": home_holidays}
for slug, fn in DESIGNS.items():
    d = OUT / slug; d.mkdir(parents=True, exist_ok=True)
    svg = fn(); (d / "design.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(d / "design.png"), output_width=W, output_height=H)
    # preview on a black shirt-colored background
    prev = svg.replace(HEAD, HEAD + f'<rect width="{W}" height="{H}" fill="#151515"/>', 1)
    cairosvg.svg2png(bytestring=prev.encode(), write_to=str(d / "preview-on-black.png"), output_width=900, output_height=1100)
    print(slug, "ok")
