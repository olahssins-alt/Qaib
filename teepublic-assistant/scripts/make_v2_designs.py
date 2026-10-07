"""Version 2 of the first five designs: condensed screen-print type, vintage wear, more craft.
Usage: python scripts/make_v2_designs.py ready-to-upload-v2
Needs: pip install cairosvg fonttools pillow numpy
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import *

L, R = 330, W - 330
CREAM = "#F5E6C8"

# 1 ---------------------------------------------------------------------------
def jingle_bams():
    red, green, dgreen, gold, brown = "#E04B3C", "#3FA45F", "#245C3A", "#F2B134", "#8A5A3B"
    p = [line(2250, 1450, "JINGLE", 1000, R - L, CREAM, xscale=0.8)]
    p.append(stripes(1560, L + 500, R - 500, (gold, red, green), h=34, gap=24))
    tx, ty, tw, th = 1300, 1800, 1900, 2250
    p.append(f'<rect x="{tx+70}" y="{ty+90}" width="{tw}" height="{th}" rx="230" fill="{dgreen}"/>')
    p.append(f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="230" fill="{CREAM}"/>')
    p.append(f'<rect x="{tx+100}" y="{ty+100}" width="{tw-200}" height="{th-200}" rx="160" fill="none" stroke="{green}" stroke-width="36"/>')
    cx = tx + tw / 2
    sw_, sh_, gap = 190, 330, 55
    top = ty + 430
    for r, n in enumerate([1, 2, 3, 4]):
        y = top + r * (sh_ + 30)
        tot = n * sw_ + (n - 1) * gap
        for i in range(n):
            x = cx - tot / 2 + i * (sw_ + gap)
            p.append(f'<rect x="{x}" y="{y}" width="{sw_}" height="{sh_}" rx="100" fill="{green}"/>')
            p.append(f'<rect x="{x}" y="{y+sh_/2-20}" width="{sw_}" height="40" fill="{CREAM}"/>')
            p.append(f'<rect x="{x+sw_/2-16}" y="{y+36}" width="32" height="{sh_-72}" rx="16" fill="{dgreen}" opacity="0.5"/>')
            if r > 0 and (r + i) % 2 == 1:
                p.append(f'<circle cx="{x+sw_/2}" cy="{y+sh_-56}" r="62" fill="{red}"/><circle cx="{x+sw_/2-18}" cy="{y+sh_-76}" r="16" fill="#F7B8B0"/>')
    p.append(f'<rect x="{cx-100}" y="{top+4*(sh_+30)}" width="200" height="150" rx="36" fill="{brown}"/>')
    p.append(star(cx, ty + 270, 190, gold))
    for fx, fy, s in [(780, 2300, 70), (3750, 2000, 90), (700, 3900, 60), (3800, 3700, 70)]:
        p.append(sparkle(fx, fy, s * 2, CREAM))
    p.append(line(2250, 5150, "BAMS", 900, R - L, red, xscale=0.8))
    return svg(*p)

# 2 ---------------------------------------------------------------------------
def kitchen_closed():
    red, ball, ballh, wood, dwood, green = "#E0443E", "#D7F23B", "#9DB81C", "#C98B55", "#9E6A3E", "#3F9A5C"
    p = []
    bx, by, br = 2250, 1250, 760
    p.append(f'<circle cx="{bx}" cy="{by}" r="{br}" fill="{ball}"/>')
    import random; rnd = random.Random(4)
    for (dx, dy) in [(-380,-60),(-120,-300),(200,-200),(420,120),(80,120),(-260,300),(160,450),(-480,-380),(-300,60),(340,-40)]:
        p.append(f'<circle cx="{bx+dx}" cy="{by+dy+80}" r="78" fill="{ballh}"/>')
    p.append(f'<path d="M {bx-680} {by-300} C {bx-580} {by-930} {bx+150} {by-1150} {bx+780} {by-1000} C {bx+540} {by-840} {bx+600} {by-560} {bx+680} {by-300} Z" fill="{red}"/>')
    p.append(f'<circle cx="{bx+780}" cy="{by-1000}" r="160" fill="{CREAM}"/>')
    p.append(f'<rect x="{bx-820}" y="{by-420}" width="1640" height="290" rx="145" fill="{CREAM}"/>')
    sx, sy, sw, sh = 400, 2330, 3700, 2100
    p.append(f'<path d="M{sx+520} {sy} L2250 {sy-190} L{sx+sw-520} {sy}" stroke="{CREAM}" stroke-width="40" fill="none" stroke-linejoin="round"/>')
    p.append(f'<circle cx="2250" cy="{sy-190}" r="55" fill="{CREAM}"/>')
    p.append(f'<rect x="{sx+50}" y="{sy+80}" width="{sw}" height="{sh}" rx="120" fill="{dwood}"/>')
    p.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="120" fill="{wood}"/>')
    p.append(f'<rect x="{sx+90}" y="{sy+90}" width="{sw-180}" height="{sh-180}" rx="75" fill="none" stroke="{CREAM}" stroke-width="40"/>')
    # caution band across the lower sign
    by0, bh = sy + sh - 480, 250
    p.append(f'<clipPath id="band"><rect x="{sx+140}" y="{by0}" width="{sw-280}" height="{bh}" rx="40"/></clipPath><g clip-path="url(#band)">')
    p.append(f'<rect x="{sx+140}" y="{by0}" width="{sw-280}" height="{bh}" fill="{CREAM}"/>')
    k = sx + 40
    while k < sx + sw:
        p.append(f'<polygon points="{k},{by0+bh} {k+130},{by0+bh} {k+130+bh},{by0} {k+bh},{by0}" fill="{red}"/>')
        k += 260
    p.append("</g>")
    p.append(line(2250, sy + 780, "KITCHEN", 500, sw - 500, CREAM, xscale=0.82))
    p.append(line(2250, sy + 1420, "CLOSED", 500, sw - 500, red, xscale=0.82))
    for ang in (-35, 35):
        p.append(f'<ellipse cx="{sx+330}" cy="{sy+20}" rx="230" ry="95" fill="{green}" transform="rotate({ang} {sx+330} {sy+20})"/>')
    for (dx, dy) in [(-40,-20),(60,10),(10,70)]:
        p.append(f'<circle cx="{sx+330+dx}" cy="{sy+20+dy}" r="58" fill="{red}"/>')
    p.append(line(2250, 5100, "FOR THE HOLIDAYS", 380, R - L, CREAM, xscale=0.8, track=20))
    p.append(stripes(5180, L + 700, R - 700, (red, "#F2B134", green), h=34, gap=24))
    return svg(*p)

# 3 ---------------------------------------------------------------------------
def home_holidays():
    yellow, ice, roof, door = "#F2C14E", "#A9D6E5", "#D94A3D", "#2E5E7E"
    p = [line(2250, 1000, "HOME FOR THE", 420, R - L, CREAM, xscale=0.8, track=30),
         line(2250, 1900, "HOLIDAYS", 820, R - L, yellow, xscale=0.8)]
    hx, hy, hw, hh = 1200, 3150, 2100, 1450
    p.append(f'<rect x="{hx+1450}" y="{hy-700}" width="260" height="600" fill="{roof}"/><rect x="{hx+1410}" y="{hy-760}" width="340" height="110" rx="40" fill="#FFFFFF"/>')
    p.append(f'<rect x="{hx}" y="{hy}" width="{hw}" height="{hh}" rx="40" fill="{CREAM}"/>')
    ax, ay, lx, rx, bY = 2250, hy - 850, hx - 220, hx + hw + 220, hy + 40
    p.append(f'<polygon points="{lx},{bY} {ax},{ay} {rx},{bY}" fill="{roof}"/>')
    t = 0.42
    l2 = (ax + t * (lx - ax), ay + t * (bY - ay)); r2 = (ax + t * (rx - ax), ay + t * (bY - ay)); span = r2[0] - l2[0]
    waves = "".join(f" Q {r2[0]-span*(i+0.5)/5:.0f} {r2[1]+(120 if i%2==0 else 40):.0f} {r2[0]-span*(i+1)/5:.0f} {r2[1]:.0f}" for i in range(5))
    p.append(f'<path d="M {ax} {ay} L {r2[0]:.0f} {r2[1]:.0f}{waves} Z" fill="#FFFFFF"/>')
    # string lights along the eaves
    cols = ["#F2C14E", "#E04B3C", "#3FA45F", "#A9D6E5"]
    for i in range(9):
        u = i / 8
        x = lx + 40 + u * (hw + 440 - 80); y = bY + 55 + 65 * math.sin(u * math.pi * 4)
        p.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="48" fill="{cols[i%4]}"/>')
    for (dx, dy, r) in [(0, -880, 75), (80, -1010, 95), (20, -1160, 110)]:
        p.append(f'<circle cx="{hx+1580+dx}" cy="{hy+dy}" r="{r}" fill="{ice}"/>')
    for wx in (hx + 230, hx + hw - 230 - 520):
        p.append(f'<rect x="{wx}" y="{hy+330}" width="520" height="520" rx="30" fill="{yellow}"/><rect x="{wx+245}" y="{hy+330}" width="30" height="520" fill="{door}"/><rect x="{wx}" y="{hy+575}" width="520" height="30" fill="{door}"/>')
    dx = 2250 - 230
    p.append(f'<rect x="{dx}" y="{hy+650}" width="460" height="800" rx="40" fill="{door}"/><circle cx="{dx+380}" cy="{hy+1080}" r="35" fill="{yellow}"/>')
    p.append(f'<rect x="{dx+70}" y="{hy+780}" width="320" height="230" rx="30" fill="{CREAM}"/>')
    p.append(line(2250, hy + 880, "DO NOT", 70, 240, door, xscale=0.9, bold=3))
    p.append(line(2250, hy + 975, "DISTURB", 70, 260, door, xscale=0.9, bold=3))
    for (fx, fy, s) in [(560, 2500, 90), (3950, 2400, 110), (520, 3800, 70), (4000, 3700, 80), (3750, 2100, 60), (820, 2150, 60)]:
        for a in (0, 60, 120):
            p.append(f'<line x1="{fx-s}" y1="{fy}" x2="{fx+s}" y2="{fy}" stroke="{ice}" stroke-width="28" stroke-linecap="round" transform="rotate({a} {fx} {fy})"/>')
    p.append(line(2250, 5120, "(AND NOT LEAVING)", 330, R - L - 300, ice, xscale=0.8, track=20))
    return svg(*p)

# 4 ---------------------------------------------------------------------------
def partridge():
    leaf, leaf2, pear, bark, bird, birdl, beak = "#6FA35A", "#4E8A45", "#E9C46A", "#8A5A3B", "#A0673F", "#D9A26B", "#F2B84B"
    p = [line(2250, 1150, "PARTRIDGE", 800, R - L, CREAM, xscale=0.8),
         line(2250, 1950, "SPOTTED", 800, R - L, pear, xscale=0.8)]
    dy = 330
    p.append(f'<path d="M2130 {4380+dy} L2170 {3050+dy} L2330 {3050+dy} L2370 {4380+dy} Z" fill="{bark}"/>')
    p.append(f'<path d="M2300 {3650+dy} Q2700 {3560+dy} 3150 {3470+dy}" stroke="{bark}" stroke-width="110" fill="none" stroke-linecap="round"/>')
    for (cx, cy, r) in [(2250, 2550, 700), (1750, 2900, 520), (2750, 2900, 520), (2250, 3050, 560)]:
        p.append(f'<circle cx="{cx}" cy="{cy+dy}" r="{r}" fill="{leaf}"/>')
    for (cx, cy, r) in [(1900, 2400, 160), (2600, 2350, 140), (2250, 2950, 180), (1700, 3000, 120), (2800, 3050, 130), (2250, 2650, 100)]:
        p.append(f'<circle cx="{cx}" cy="{cy+dy}" r="{r}" fill="{leaf2}" opacity="0.6"/>')
    for (cx, cy) in [(1850, 2650), (2350, 2300), (2650, 2750), (2100, 3200), (1550, 3100), (2900, 3200)]:
        cy += dy
        p.append(f'<path d="M{cx} {cy-120} q-15 -60 25 -90" stroke="{bark}" stroke-width="22" fill="none" stroke-linecap="round"/><circle cx="{cx}" cy="{cy+60}" r="105" fill="{pear}"/><circle cx="{cx}" cy="{cy-40}" r="70" fill="{pear}"/><circle cx="{cx-35}" cy="{cy+30}" r="22" fill="#F6E3A1"/>')
    bx, by = 3050, 3260 + dy
    p.append(f'<path d="M{bx-300} {by-30} L{bx-540} {by-190} L{bx-490} {by+50} Z" fill="{bird}"/>')
    p.append(f'<ellipse cx="{bx}" cy="{by}" rx="330" ry="240" fill="{bird}"/><ellipse cx="{bx+120}" cy="{by+60}" rx="190" ry="150" fill="{birdl}"/>')
    for sx_, sy_ in [(-120, -40), (-30, -110), (60, -30), (-170, 60), (-50, 30)]:
        p.append(f'<circle cx="{bx+sx_}" cy="{by+sy_}" r="22" fill="#5E3A22"/>')
    p.append(f'<path d="M{bx-180} {by-60} Q{bx-20} {by+120} {bx+120} {by-40}" stroke="{birdl}" stroke-width="36" fill="none" stroke-linecap="round"/>')
    p.append(f'<circle cx="{bx+290}" cy="{by-210}" r="150" fill="{bird}"/><path d="M{bx+425} {by-235} L{bx+545} {by-195} L{bx+425} {by-160} Z" fill="{beak}"/>')
    p.append(f'<circle cx="{bx+330}" cy="{by-245}" r="32" fill="#1A1A1A"/><circle cx="{bx+340}" cy="{by-255}" r="10" fill="#FFFFFF"/>')
    p.append(f'<path d="M{bx-40} {by+230} l-30 90 M{bx+80} {by+230} l30 90" stroke="{beak}" stroke-width="36" stroke-linecap="round"/>')
    # field-guide stamp
    p.append(f'<rect x="620" y="4830" width="3260" height="330" rx="60" fill="none" stroke="{CREAM}" stroke-width="30"/>')
    p.append(f'<path d="M780 5010 L880 5100 L1060 4920" stroke="#6FD08C" stroke-width="64" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    p.append(line(2560, 5105, "PEAR TREE CONFIRMED", 220, 2650, CREAM, xscale=0.82, track=20, bold=8))
    return svg(*p)

# 5 ---------------------------------------------------------------------------
def reading_night():
    yellow, ice, page, cover = "#F2C14E", "#A9D6E5", "#F7F1E3", "#2E5E7E"
    def crescent(x1, y1, r1, x2, y2, r2, fill):
        d = math.hypot(x2 - x1, y2 - y1); a = (r1**2 - r2**2 + d**2) / (2 * d); h = math.sqrt(r1**2 - a**2)
        mx, my = x1 + a * (x2 - x1) / d, y1 + a * (y2 - y1) / d; ox, oy = -(y2 - y1) / d * h, (x2 - x1) / d * h
        p1, p2 = (mx + ox, my + oy), (mx - ox, my - oy)
        return f'<path d="M{p1[0]:.0f} {p1[1]:.0f} A{r1} {r1} 0 1 1 {p2[0]:.0f} {p2[1]:.0f} A{r2} {r2} 0 0 0 {p1[0]:.0f} {p1[1]:.0f} Z" fill="{fill}"/>'
    cx, cy = 2250, 2350
    p = [arc(cx, cy, 1330, "SILENT NIGHT", 480, CREAM, xscale=0.8, track=20, bold=12)]
    p.append(crescent(cx, cy + 40, 600, cx + 240, cy - 90, 520, yellow))
    for (x, y, s) in [(1500, 2000, 150), (3050, 1850, 120), (3150, 2750, 180), (1450, 2950, 100), (2650, 3050, 90)]:
        p.append(sparkle(x, y, s, ice))
    p.append(f'<path d="M700 3800 Q1450 3450 2250 3800 L2250 4550 Q1450 4200 700 4550 Z" fill="{cover}"/><path d="M3800 3800 Q3050 3450 2250 3800 L2250 4550 Q3050 4200 3800 4550 Z" fill="{cover}"/>')
    p.append(f'<path d="M800 3720 Q1500 3380 2250 3720 L2250 4450 Q1500 4110 800 4450 Z" fill="{page}"/><path d="M3700 3720 Q3000 3380 2250 3720 L2250 4450 Q3000 4110 3700 4450 Z" fill="{page}"/>')
    for i in range(5):
        d = 3830 + i * 120
        p.append(f'<path d="M1000 {d} Q1600 {d-260} 2120 {d}" stroke="{ice}" stroke-width="34" fill="none" stroke-linecap="round" opacity="0.9"/><path d="M3500 {d} Q2900 {d-260} 2380 {d}" stroke="{ice}" stroke-width="34" fill="none" stroke-linecap="round" opacity="0.9"/>')
    p.append(f'<rect x="2225" y="3700" width="50" height="860" rx="20" fill="{cover}"/><path d="M2300 4450 l0 330 l55 -60 l55 60 l0 -330 Z" fill="#E04B3C"/>')
    p.append(line(2250, 5250, "READING NIGHT", 640, R - L, yellow, xscale=0.82, track=20))
    return svg(*p)

DESIGNS = {"01-jingle-bams-mahjong": jingle_bams, "02-kitchen-closed-pickleball": kitchen_closed,
           "03-home-for-the-holidays-introvert": home_holidays, "04-partridge-spotted-birding": partridge,
           "05-silent-night-reading-night-books": reading_night}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, fn) in enumerate(DESIGNS.items()):
        d = out / slug; d.mkdir(parents=True, exist_ok=True)
        s = fn(); (d / "design.svg").write_text(s)
        clean = render(s); worn = wear(clean, seed=i + 3)
        clean.save(d / "design_clean.png"); worn.save(d / "design.png")
        on_color(worn).save(d / "preview-on-black.png")
        shirt(worn).save(d / "mockup-shirt.png")
        print(slug)
