"""One idea (E1 'Supervising the Christmas Tree') in six very different art directions,
so the owner can pick the styles to use going forward.
Usage: python scripts/make_style_sampler.py style-sampler
"""
import math, sys
from pathlib import Path
import numpy as np
from PIL import Image, ImageFilter
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import *

SHRIK, PIXEL, ABRIL, PLAY_IT, CORM_IT = (font("shrikhand-latin-400-normal"), font("press-start-2p-latin-400-normal"),
    font("abril-fatface-latin-400-normal"), font("playfair-display-latin-900-italic"), font("cormorant-garamond-latin-600-italic"))
FRED, MONO, RIGHT = font("fredoka-latin-700-normal"), font("monoton-latin-400-normal"), font("righteous-latin-400-normal")

def T(cx, base, s, cap, width, fill, f, **kw):
    kw.setdefault("xscale", 1.0); kw.setdefault("bold", 0)
    return line(cx, base, s, cap, width, fill, font=f, **kw)

def cat_silhouette(cx, floor, s, fill, tail=True):
    """Sitting cat, front view, one flat colour. About 1300*s tall."""
    p = []
    if tail:
        p.append(f'<path d="M{cx+230*s} {floor-70*s} C {cx+640*s} {floor-40*s} {cx+700*s} {floor-430*s} {cx+520*s} {floor-650*s}" stroke="{fill}" stroke-width="{110*s:.0f}" fill="none" stroke-linecap="round"/>')
    p.append(f'<path d="M{cx-300*s} {floor} C {cx-380*s} {floor-420*s} {cx-250*s} {floor-760*s} {cx} {floor-780*s} C {cx+250*s} {floor-760*s} {cx+380*s} {floor-420*s} {cx+300*s} {floor} Z" fill="{fill}"/>')
    hy = floor - 960 * s
    p.append(f'<ellipse cx="{cx}" cy="{hy}" rx="{300*s:.0f}" ry="{255*s:.0f}" fill="{fill}"/>')
    for sg in (-1, 1):
        p.append(f'<polygon points="{cx+sg*290*s:.0f},{hy-40*s:.0f} {cx+sg*230*s:.0f},{hy-380*s:.0f} {cx+sg*60*s:.0f},{hy-220*s:.0f}" fill="{fill}" stroke="{fill}" stroke-width="{30*s:.0f}" stroke-linejoin="round"/>')
    return "".join(p)

# ---------------------------------------------------------------- S1 groovy 70s
def s1():
    rust, orange, mustard, cream, sage, brown = "#D1495B", "#EDAE49", "#F4D35E", "#F7EDE2", "#66A182", "#3D2B1F"
    cx, by = 2250, 3700
    p = []
    for r, c in zip((1650, 1400, 1150, 900), (rust, orange, mustard, sage)):
        p.append(f'<path d="M{cx-r} {by} A{r} {r} 0 0 1 {cx+r} {by} Z" fill="{c}"/>')
    p.append(f'<path d="M{cx-650} {by} A650 650 0 0 1 {cx+650} {by} Z" fill="{cream}"/>')
    # small tree and a cat silhouette sitting on the horizon line
    p.append(f'<polygon points="{cx-380},{by-1250} {cx-60},{by-60} {cx-700},{by-60}" fill="{sage}" stroke="{brown}" stroke-width="50" stroke-linejoin="round"/>')
    p.append(star(cx - 380, by - 1290, 120, mustard))
    p.append(cat_silhouette(cx + 330, by, 0.78, brown))
    p.append(f'<rect x="{cx-1750}" y="{by}" width="3500" height="70" rx="35" fill="{cream}"/>')
    p.append(arc(cx, by, 1720, "SUPERVISING", 400, cream, font=SHRIK, xscale=1.0, track=10, bold=0))
    p.append(T(cx, 4500, "the Christmas Tree", 420, 3600, mustard, SHRIK, track=10))
    return svg(*p)

# ---------------------------------------------------------------- S2 ugly sweater pixel
CAT_PX = ["..X......X..", ".XXX....XXX.", ".XXXXXXXXXX.", "XXXXXXXXXXXX", "XXGXXXXXXGXX", "XXXXXPPXXXXX",
          "XXXXXXXXXXXX", ".XXXXXXXXXX.", "..XXXXXXXX..", ".XXXXXXXXXX.", ".XXXXXXXXXXT", "XXXXXXXXXXXT", "XXXXXXXXXXT."]
TREE_PX = [".....Y.....", "....GGG....", "...GRGGG...", "..GGGGGYG..", "...GGGGG...", "..GGYGGRG..", ".GGGGGGGGG.",
           "..GGGGGGG..", ".GRGGGGYGG.", "GGGGGGGGGGG", "....BBB....", "....BBB...."]
def pix(grid, x0, y0, u, colors):
    out = []
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            if ch in colors:
                out.append(f'<rect x="{x0+c*u}" y="{y0+r*u}" width="{u+1}" height="{u+1}" fill="{colors[ch]}"/>')
    return "".join(out)
def s2():
    red, green, white, gold, brown = "#D7263D", "#1B998B", "#F4F1E8", "#F5B700", "#7A4E2D"
    p = []
    u = 70
    for row_y, col in ((700, red), (5050, red)):
        for k in range(30):
            x = 330 + k * 130
            p.append(f'<polygon points="{x},{row_y} {x+65},{row_y-65} {x+130},{row_y}" fill="{col}"/>')
            p.append(f'<rect x="{x+50}" y="{row_y+40}" width="30" height="30" fill="{white}"/>')
    p.append(T(2250, 1500, "TREE", 520, 3800, white, PIXEL))
    p.append(pix(TREE_PX, 900, 1900, 190, {"G": green, "R": red, "Y": gold, "B": brown}))
    p.append(pix(CAT_PX, 2750, 2350, 140, {"X": white, "G": green, "P": red, "T": white}))
    p.append(T(2250, 4700, "SUPERVISOR", 300, 3800, gold, PIXEL))
    for (x, y) in ((600, 2100), (3900, 1900), (650, 3700), (3950, 3800)):
        p.append(pix([".X.", "XXX", ".X."], x, y, 60, {"X": white}))
    return svg(*p)

# ---------------------------------------------------------------- S3 vintage Christmas card
def s3():
    red, gold, cream, green = "#B3263A", "#D9A441", "#F2E6CF", "#2F6B4F"
    p = [f'<rect x="500" y="500" width="3500" height="4500" rx="140" fill="none" stroke="{gold}" stroke-width="40"/>',
         f'<rect x="600" y="600" width="3300" height="4300" rx="100" fill="none" stroke="{gold}" stroke-width="14"/>']
    for (x, y) in ((600, 600), (3900, 600), (600, 4900), (3900, 4900)):
        p.append(f'<circle cx="{x}" cy="{y}" r="60" fill="{red}"/>')
    # hanging ornaments
    for x, L_, c in ((1300, 900, red), (2250, 600, gold), (3200, 1050, green)):
        p.append(f'<line x1="{x}" y1="600" x2="{x}" y2="{600+L_}" stroke="{gold}" stroke-width="14"/>')
        p.append(f'<rect x="{x-45}" y="{600+L_-20}" width="90" height="70" rx="12" fill="{gold}"/><circle cx="{x}" cy="{600+L_+170}" r="160" fill="{c}"/>')
        p.append(f'<path d="M{x-150} {600+L_+170} q150 70 300 0" stroke="{gold}" stroke-width="16" fill="none"/>')
    p.append(cat_silhouette(2250, 3500, 1.05, cream))
    # ribbon banner
    p.append(f'<path d="M700 3650 L3800 3650 L3650 3900 L3800 4150 L700 4150 L850 3900 Z" fill="{red}"/>')
    p.append(T(2250, 4030, "Supervising", 330, 2700, cream, PLAY_IT))
    p.append(T(2250, 4620, "the Christmas Tree", 300, 3000, gold, CORM_IT, track=10))
    return svg(*p)

# ---------------------------------------------------------------- S4 kawaii sticker
def s4():
    mint, pink, butter, lilac, white, ink, blush = "#9AD1B5", "#FF8FA3", "#FFD6A5", "#CDB4DB", "#FFFFFF", "#3B2F3F", "#FFB3C1"
    def grp(shapes):  # sticker outline: everything drawn first with a fat white stroke
        return "".join(sh.replace('/>', f' stroke="{white}" stroke-width="150" stroke-linejoin="round"/>') for sh in shapes) + "".join(shapes)
    tree = [f'<circle cx="1600" cy="2200" r="420" fill="{mint}"/>', f'<circle cx="1600" cy="2800" r="620" fill="{mint}"/>', f'<rect x="1500" y="3350" width="200" height="300" rx="50" fill="#C89F7A"/>']
    cat = [f'<ellipse cx="2850" cy="3150" rx="560" ry="520" fill="{butter}"/>', f'<polygon points="2350,2000 2500,1550 2750,1880" fill="{butter}"/>',
           f'<polygon points="3350,2000 3200,1550 2950,1880" fill="{butter}"/>', f'<ellipse cx="2850" cy="2250" rx="620" ry="520" fill="{butter}"/>']
    p = [grp(tree + cat)]
    for (x, y, c) in ((1450, 2050, pink), (1780, 2300, lilac), (1350, 2700, lilac), (1800, 2900, pink), (1550, 3150, butter)):
        p.append(f'<circle cx="{x}" cy="{y}" r="80" fill="{c}"/>')
    p.append(star(1600, 1760, 170, "#FFC94D"))
    p.append(f'<polygon points="2440,1900 2510,1670 2650,1850" fill="{pink}"/><polygon points="3260,1900 3190,1670 3050,1850" fill="{pink}"/>')
    for sg in (-1, 1):
        p.append(f'<circle cx="{2850+sg*220}" cy="2250" r="70" fill="{ink}"/><circle cx="{2850+sg*220-22}" cy="2225" r="22" fill="{white}"/>')
        p.append(f'<ellipse cx="{2850+sg*360}" cy="2400" rx="90" ry="50" fill="{blush}"/>')
    p.append(f'<path d="M2790 2380 q30 40 60 0 q30 40 60 0" stroke="{ink}" stroke-width="24" fill="none" stroke-linecap="round"/>')
    for sg in (-1, 1):
        p.append(f'<ellipse cx="{2850+sg*230}" cy="3600" rx="150" ry="90" fill="{white}"/>')
    p.append(T(2250, 1250, "TREE", 650, 3600, pink, FRED, track=30))
    p.append(T(2250, 4700, "SUPERVISOR", 480, 3600, white, FRED, track=20))
    return svg(*p)

# ---------------------------------------------------------------- S5 minimal line art
def s5():
    cream, gold = "#F2E9DA", "#D8B26E"
    sw = 26
    st = f'stroke="{cream}" stroke-width="{sw}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = []
    # tree drawn as one zig-zag line
    pts = [(1500, 3700), (2000, 3150), (1700, 3150), (2150, 2600), (1900, 2600), (2250, 2050), (2600, 2600), (2350, 2600), (2800, 3150), (2500, 3150), (3000, 3700), (1500, 3700)]
    p.append('<path d="M' + " L".join(f"{x} {y}" for x, y in pts) + f'" {st}/>')
    p.append(f'<path d="M2250 3700 L2250 3880" {st}/>')
    p.append(star(2250, 1950, 110, gold))
    # cat line drawing sitting at right, seen from behind
    cx, fl = 3250, 3880
    p.append(f'<path d="M{cx-260} {fl} C {cx-330} {fl-380} {cx-200} {fl-640} {cx} {fl-650} C {cx+200} {fl-640} {cx+330} {fl-380} {cx+260} {fl}" {st}/>')
    p.append(f'<path d="M{cx-170} {fl-700} C {cx-230} {fl-900} {cx-110} {fl-1020} {cx} {fl-1020} C {cx+110} {fl-1020} {cx+230} {fl-900} {cx+170} {fl-700}" {st}/>')
    p.append(f'<path d="M{cx-200} {fl-900} L{cx-170} {fl-1130} L{cx-60} {fl-1010} M{cx+200} {fl-900} L{cx+170} {fl-1130} L{cx+60} {fl-1010}" {st}/>')
    p.append(f'<path d="M{cx+260} {fl} C {cx+520} {fl} {cx+560} {fl-220} {cx+440} {fl-330}" {st}/>')
    p.append(f'<path d="M1300 {fl} L3800 {fl}" stroke="{cream}" stroke-width="{sw}" stroke-linecap="round"/>')
    p.append(T(2250, 1300, "supervising", 330, 3000, cream, CORM_IT, track=30))
    p.append(T(2250, 4500, "the christmas tree", 260, 3000, gold, CORM_IT, track=40))
    return svg(*p)

# ---------------------------------------------------------------- S6 neon sign
def s6_parts():
    pink, cyan, green, yellow = "#FF4FA3", "#3CF2FF", "#4DFF7A", "#FFE45C"
    st = lambda c, w=60: f'stroke="{c}" stroke-width="{w}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    p = [f'<path d="M1650 1600 L2250 1600 M1950 1600 L1500 2400 L1750 2400 L1350 3200 L1700 3200 L1250 3900 L2650 3900 L2200 3200 L2550 3200 L2150 2400 L2400 2400 L1950 1600" {st(green)}/>']
    cx, fl = 3100, 3900
    p.append(f'<path d="M{cx-250} {fl} C {cx-320} {fl-380} {cx-200} {fl-620} {cx} {fl-630} C {cx+200} {fl-620} {cx+320} {fl-380} {cx+250} {fl} Z" {st(pink)}/>')
    p.append(f'<path d="M{cx-170} {fl-680} C {cx-230} {fl-880} {cx-110} {fl-990} {cx} {fl-990} C {cx+110} {fl-990} {cx+230} {fl-880} {cx+170} {fl-680} Z M{cx-190} {fl-880} L{cx-160} {fl-1110} L{cx-50} {fl-985} M{cx+190} {fl-880} L{cx+160} {fl-1110} L{cx+50} {fl-985}" {st(pink)}/>')
    p.append(f'<path d="M{cx+250} {fl-40} C {cx+520} {fl-40} {cx+560} {fl-260} {cx+430} {fl-380}" {st(pink)}/>')
    p.append(star(1950, 1480, 150, yellow))
    p.append(T(2250, 1150, "SUPERVISING", 560, 3700, cyan, MONO, track=20))
    p.append(T(2250, 4750, "THE TREE", 520, 3000, yellow, RIGHT, track=40))
    return svg(*p)

def neon(img):
    """Add a soft glow under the tubes, keeping the background transparent."""
    a = img.getchannel("A")
    glow = img.copy().filter(ImageFilter.GaussianBlur(60))
    ga = np.asarray(glow.getchannel("A"), dtype=np.float32) * 1.6
    glow.putalpha(Image.fromarray(np.clip(ga, 0, 255).astype(np.uint8)))
    out = Image.new("RGBA", img.size, (0, 0, 0, 0)); out.alpha_composite(glow); out.alpha_composite(img)
    # white-hot core
    core = img.copy(); arr = np.asarray(core).copy(); m = arr[..., 3] > 0
    arr[..., :3][m] = (arr[..., :3][m] * 0.45 + 255 * 0.55).astype(np.uint8)
    out.alpha_composite(Image.fromarray(arr).filter(ImageFilter.GaussianBlur(3)).resize(img.size))
    return out

STYLES = {"s1-groovy-70s": (s1, True), "s2-ugly-sweater-pixel": (s2, False), "s3-vintage-christmas-card": (s3, True),
          "s4-kawaii-sticker": (s4, False), "s5-minimal-line-art": (s5, False), "s6-neon-sign": (s6_parts, "neon")}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for i, (slug, (fn, mode)) in enumerate(STYLES.items()):
        d = out / slug; d.mkdir(parents=True, exist_ok=True)
        s = fn(); (d / "design.svg").write_text(s)
        img = render(s)
        if mode == "neon": img = neon(img)
        elif mode: img = wear(img, seed=i + 21)
        img.save(d / "design.png"); on_color(img).save(d / "preview-on-black.png"); print(slug)
