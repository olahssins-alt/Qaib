"""Batch 6 (plan 14 Oct): idea B4 'Will Trade Turkey for Court Time' (pickleball x Thanksgiving).
Five styles: varsity, LED scoreboard, pop-art halftone comic, vintage postcard, kawaii sticker.
Usage: python scripts/make_batch6.py batch-06
"""
import math, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, arc, star, sparkle, svg, render, wear, on_color, W, H
from fx import warp, p, outlined, extrude, heart
from motifs import turkey, pie, pumpkin, ball, paddle, at, IVORY, BALL, BALL_D
from knit import F35

GRAD, TITAN, BUNGEE, PAC, ANTON, ABRIL, FRED, PIXEL = (font("graduate-latin-400-normal"), font("titan-one-latin-400-normal"),
    font("bungee-latin-400-normal"), font("pacifico-latin-400-normal"), font("anton-latin-400-normal"),
    font("abril-fatface-latin-400-normal"), font("fredoka-latin-700-normal"), font("press-start-2p-latin-400-normal"))
CREAM, RUST, MUSTARD, GREEN, NAVY, INK = "#F6EBDD", "#C8553D", "#F2A541", "#3F9A5C", "#1F3A5F", "#221A16"

# 1 varsity
def d1():
    o = []
    o.append(p(warp(2250, 760, "WILL TRADE", 330, 2600, GRAD, track=80), CREAM))
    arch = lambda u: -300 * (1 - (2 * u - 1) ** 2)
    d = warp(2250, 2250, "TURKEY", 900, 3900, GRAD, yfn=arch, track=30)
    o.append(outlined(d, MUSTARD, (CREAM, 120), (RUST, 70)))
    # crossed paddles + ball
    o.append(at(1800, 3350, paddle(1.9, "#C8553D", "#7A2E1F"), rot=-32))
    o.append(at(2700, 3350, paddle(1.9, "#2F6FB0", "#1B3F66"), rot=32))
    o.append(at(2250, 3050, ball(1.7)))
    o.append(p(warp(2250, 4650, "FOR COURT TIME", 520, 3800, GRAD, track=40), CREAM))
    o.append(f'<rect x="700" y="4800" width="3100" height="40" rx="20" fill="{MUSTARD}"/>')
    o.append(p(warp(2250, 5150, "PICKLEBALL · THANKSGIVING", 200, 3000, GRAD, track=80), MUSTARD))
    return svg(*o)

# 2 LED scoreboard
def dot_text(s, x0, y0, dot, on, off=None, scale=1):
    """Dot-matrix text from the 3x5 font; returns (svg, width)."""
    o, x = [], x0
    for ch in s.upper():
        bits = F35[ch]
        for r in range(5):
            for c in range(3):
                lit = bits[r * 3 + c] == "1"
                if lit or off:
                    o.append(f'<circle cx="{x + c*dot*scale + dot*scale/2:.0f}" cy="{y0 + r*dot*scale + dot*scale/2:.0f}" r="{dot*scale*0.42:.0f}" fill="{on if lit else off}"/>')
        x += 4 * dot * scale
    return "".join(o), x - x0 - dot * scale
def dot_center(s, cx, y0, dot, on, off=None, scale=1):
    _, w = dot_text(s, 0, 0, dot, on, None, scale)
    return dot_text(s, cx - w / 2, y0, dot, on, off, scale)[0]
SEG = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg"}
def seven(ch, x, y, w, h, t, on, off):
    """Seven-segment digit in a w x h box at x,y with segment thickness t."""
    segs = {"a": (x + t, y, w - 2*t, t, 0), "d": (x + t, y + h - t, w - 2*t, t, 0), "g": (x + t, y + h/2 - t/2, w - 2*t, t, 0),
            "f": (x, y + t, t, h/2 - 1.5*t, 1), "b": (x + w - t, y + t, t, h/2 - 1.5*t, 1),
            "e": (x, y + h/2 + t/2, t, h/2 - 1.5*t, 1), "c": (x + w - t, y + h/2 + t/2, t, h/2 - 1.5*t, 1)}
    o = []
    for k, (sx, sy, sw, sh, vert) in segs.items():
        col = on if k in SEG[ch] else off
        if vert:
            pts = f"{sx+t/2:.0f},{sy:.0f} {sx+t:.0f},{sy+t/2:.0f} {sx+t:.0f},{sy+sh-t/2:.0f} {sx+t/2:.0f},{sy+sh:.0f} {sx:.0f},{sy+sh-t/2:.0f} {sx:.0f},{sy+t/2:.0f}"
        else:
            pts = f"{sx:.0f},{sy+t/2:.0f} {sx+t/2:.0f},{sy:.0f} {sx+sw-t/2:.0f},{sy:.0f} {sx+sw:.0f},{sy+t/2:.0f} {sx+sw-t/2:.0f},{sy+t:.0f} {sx+t/2:.0f},{sy+t:.0f}"
        o.append(f'<polygon points="{pts}" fill="{col}"/>')
    return "".join(o)
def dot_bitmap(s, cx, y0, dot, on, off):
    from PIL import Image, ImageDraw, ImageFont
    import numpy as np
    from design_kit import FONTS_DIR
    f = ImageFont.truetype(str(FONTS_DIR / "press-start-2p-latin-400-normal.woff"), 8)
    im = Image.new("1", (8 * len(s) + 8, 10), 0); dr = ImageDraw.Draw(im); dr.fontmode = "1"; dr.text((0, 0), s, font=f, fill=1)
    a = np.array(im)[:7]; cols = np.where(a.any(0))[0]; a = a[:, cols.min():cols.max() + 1]
    x0 = cx - a.shape[1] * dot / 2
    return "".join(f'<circle cx="{x0 + c*dot + dot/2:.0f}" cy="{y0 + r*dot + dot/2:.0f}" r="{dot*0.42:.0f}" fill="{on if a[r, c] else off}"/>'
                   for r in range(a.shape[0]) for c in range(a.shape[1]))
def d2():
    amber, off, panel = "#FFB000", "#2B2C31", "#1E2024"
    o = []
    o.append(f'<rect x="350" y="900" width="3800" height="3700" rx="70" fill="{MUSTARD}"/>')
    o.append(f'<rect x="460" y="1010" width="3580" height="3480" rx="40" fill="{panel}"/>')
    o.append(f'<rect x="350" y="560" width="3800" height="440" rx="40" fill="{RUST}"/>')
    o.append(p(warp(2250, 900, "THANKSGIVING CLASSIC", 230, 3400, GRAD, track=60), CREAM))
    for cx, label, score in ((1330, "TURKEY", "0"), (3170, "PICKLE", "11")):
        o.append(p(warp(cx, 1500, label, 190, 1500, GRAD, track=50), CREAM))
        o.append(f'<rect x="{cx-750}" y="1650" width="1500" height="1500" rx="30" fill="#141518"/>')
        dw, dh, gap = 520, 1000, 120
        tot = len(score) * dw + (len(score) - 1) * gap
        for k, ch in enumerate(score):
            o.append(seven(ch, cx - tot / 2 + k * (dw + gap), 1900, dw, dh, 120, amber, off))
    o.append(f'<line x1="2250" y1="1300" x2="2250" y2="3250" stroke="{MUSTARD}" stroke-width="20"/>')
    o.append(p(warp(2250, 3550, "PERIOD", 170, 1200, GRAD, track=50), CREAM))
    o.append(dot_bitmap("PIE", 2250, 3680, 95, "#FF5A3C", off))
    o.append(p(warp(2250, 5150, "WILL TRADE TURKEY FOR COURT TIME", 210, 3800, GRAD, track=40), CREAM))
    return svg(*o)

# 3 pop-art halftone comic
def burst(cx, cy, r1, r2, n=14, rot=0):
    pts = []
    for i in range(2 * n):
        a = math.pi * i / n + rot
        r = r1 if i % 2 == 0 else r2
        pts.append(f"{cx + r*math.cos(a):.0f},{cy + r*math.sin(a):.0f}")
    return " ".join(pts)
def d3():
    yellow, red, blue = "#FFD23F", "#EE4266", "#3BCEAC"
    cx, cy = 2250, 2700
    o = [f'<polygon points="{burst(cx, cy, 2050, 1500, 16)}" fill="{yellow}" stroke="{INK}" stroke-width="50" stroke-linejoin="round"/>']
    o.append(f'<clipPath id="bc"><polygon points="{burst(cx, cy, 2000, 1450, 16)}"/></clipPath><g clip-path="url(#bc)">')
    step = 110
    for i in range(-20, 21):
        for j in range(-20, 21):
            x, y = cx + i * step + (j % 2) * step / 2, cy + j * step
            dist = math.hypot(x - cx, y - cy) / 2000
            r = 10 + 34 * min(dist, 1)
            o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="#F29E2E"/>')
    o.append("</g>")
    # turkey holding a paddle
    o.append(at(2750, 3000, paddle(1.2, red, "#8E1C3B"), rot=25))
    o.append(at(1950, 3150, f'<g transform="scale(2.6)">{turkey()}</g>'))
    o.append(at(3250, 2250, ball(0.8)))
    # speech bubble
    o.append(f'<path d="M700 600 h1900 a160 160 0 0 1 160 160 v650 a160 160 0 0 1 -160 160 h-900 l-320 380 l40 -380 h-720 a160 160 0 0 1 -160 -160 v-650 a160 160 0 0 1 160 -160 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="45" stroke-linejoin="round"/>')
    o.append(p(warp(1650, 1300, "DINK DINK", 480, 1800, BUNGEE, track=20), INK))
    d = warp(2250, 5150, "GOBBLE!", 820, 3600, BUNGEE, track=20)
    o.append(f'<g transform="translate(40 50)">' + p(d, INK, INK, 60) + "</g>")
    o.append(outlined(d, red, (INK, 60)))
    return svg(*o)

# 4 vintage postcard: Greetings from the Kitchen
def d4():
    o = []
    x0, y0, w, h = 300, 1100, 3900, 3300
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="60" fill="{CREAM}"/>')
    o.append(f'<rect x="{x0+80}" y="{y0+80}" width="{w-160}" height="{h-160}" rx="30" fill="none" stroke="{RUST}" stroke-width="18" stroke-dasharray="70 40"/>')
    # stamp
    sx, sy = x0 + w - 560, y0 + 220
    o.append(f'<rect x="{sx}" y="{sy}" width="380" height="460" rx="10" fill="#FFFFFF" stroke="{GREEN}" stroke-width="16" stroke-dasharray="26 18"/>')
    o.append(at(sx + 190, sy + 230, ball(0.75)))
    o.append(p(warp(1650, y0 + 700, "Greetings from", 360, 2200, PAC), RUST))
    d = warp(2250, y0 + 1900, "THE KITCHEN", 980, 3500, ANTON, track=30)
    o.append(f'<linearGradient id="kg" gradientUnits="userSpaceOnUse" x1="0" y1="{y0+900}" x2="0" y2="{y0+1900}"><stop offset="0" stop-color="#F2A541"/><stop offset="1" stop-color="#C8553D"/></linearGradient>')
    o.append(f'<g transform="translate(40 55)">' + p(d, NAVY, NAVY, 40) + "</g>")
    o.append(outlined(d, "url(#kg)", (NAVY, 40)))
    # court strip with a pie on it
    cy = y0 + 2550
    o.append(f'<rect x="{x0+250}" y="{cy}" width="{w-500}" height="420" rx="20" fill="{GREEN}"/>')
    o.append(f'<line x1="{x0+250}" y1="{cy+210}" x2="{x0+w-250}" y2="{cy+210}" stroke="#FFFFFF" stroke-width="20"/>')
    for xx in (x0 + 1250, x0 + w - 1250):
        o.append(f'<line x1="{xx}" y1="{cy}" x2="{xx}" y2="{cy+420}" stroke="#FFFFFF" stroke-width="20"/>')
    o.append(f'<rect x="{2250-12}" y="{cy-120}" width="24" height="540" fill="{INK}"/>')
    o.append(at(1500, cy + 120, pie(0.9))); o.append(at(3000, cy + 160, ball(0.5)))
    o.append(p(warp(2250, 5000, "WISH YOU WERE HERE · THANKSGIVING", 190, 3800, GRAD, track=40), CREAM))
    return svg(*o)

# 5 kawaii sticker: Pie-ckleball
def d5():
    pink, mint, butter, white, ink = "#FF9AA2", "#B5EAD7", "#FFDAC1", "#FFFFFF", "#3B2F3F"
    shapes = [f'<circle cx="2250" cy="2650" r="1050" fill="{BALL}"/>']
    o = ["".join(sh.replace('/>', f' stroke="{white}" stroke-width="170"/>') for sh in shapes)]
    o += shapes
    for (x, y) in ((1800, 2200), (2350, 2000), (2750, 2350), (1700, 2900), (2900, 3000), (2300, 3350)):
        o.append(f'<circle cx="{x}" cy="{y}" r="85" fill="{BALL_D}"/>' if False else f'<circle cx="{x}" cy="{y}" r="85" fill="#A9C326"/>')
    # cute face
    for sg in (-1, 1):
        o.append(f'<circle cx="{2250+sg*300}" cy="2700" r="80" fill="{ink}"/><circle cx="{2250+sg*300-25}" cy="2670" r="26" fill="{white}"/>')
        o.append(f'<ellipse cx="{2250+sg*480}" cy="2880" rx="130" ry="70" fill="{pink}"/>')
    o.append(f'<path d="M2170 2860 q40 50 80 0 q40 50 80 0" stroke="{ink}" stroke-width="30" fill="none" stroke-linecap="round"/>')
    # pie hat
    o.append(at(2250, 1550, f'<g transform="scale(2.2)">{pie()}</g>'))
    o.append(at(3500, 3600, paddle(1.0, pink, "#C9708A"), rot=30))
    for x, y, s in ((800, 1500, 120), (3700, 1500, 100), (700, 3900, 90)):
        o.append(sparkle(x, y, s, butter))
    d = warp(2250, 900, "PIE-CKLEBALL", 640, 3900, FRED, track=20)
    o.append(outlined(d, pink, (white, 90)))
    d2 = warp(2250, 4900, "SEASON", 600, 2800, FRED, track=60)
    o.append(outlined(d2, mint, (white, 90)))
    return svg(*o)

DESIGNS = {"p1-will-trade-turkey-for-court-time-varsity": (d1, False), "p2-turkey-0-pickle-11-scoreboard": (d2, False),
           "p3-dink-dink-gobble-pop-art": (d3, False), "p4-greetings-from-the-kitchen-postcard": (d4, False),
           "p5-pieckleball-season-kawaii": (d5, False)}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, worn)) in enumerate(DESIGNS.items()):
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s)
        if worn: img = wear(img, seed=100 + i)
        img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
