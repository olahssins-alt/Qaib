"""Shared pieces for the screen-print style designs: condensed type, arc text, wear, mockups."""
import math
from io import BytesIO
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W, H = 4500, 5500
FONT = TTFont("/usr/share/fonts/opentype/inter/Inter-Black.otf")
SERIF = TTFont("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf")

def _m(font):
    return font["head"].unitsPerEm, font.getBestCmap(), font.getGlyphSet(), font["hmtx"], getattr(font["OS/2"], "sCapHeight", 0) or 1400

def line(cx, base, s, cap_h, width, fill, xscale=0.72, track=0, bold=16, font=FONT):
    """Straight text as outlines: x-squeezed heavy sans, shrunk uniformly to fit `width`."""
    upm, cmap, gs, hmtx, cap = _m(font)
    names = [cmap[ord(c)] for c in s]
    sy = cap_h / cap
    sx = sy * xscale
    adv = sum(hmtx[n][0] for n in names) * sx + track * (len(names) - 1)
    if adv > width:
        k = width / adv
        sx, sy, track, adv = sx * k, sy * k, track * k, width
    pen, cur = SVGPathPen(gs), cx - adv / 2
    for n in names:
        gs[n].draw(TransformPen(pen, (sx, 0, 0, -sy, cur, base)))
        cur += hmtx[n][0] * sx + track
    return f'<path d="{pen.getCommands()}" fill="{fill}" stroke="{fill}" stroke-width="{bold}" stroke-linejoin="round"/>'

def arc(cx, cy, r, s, cap_h, fill, xscale=0.8, track=30, bold=10, font=FONT, bottom=False):
    """Text on a circle, centred at the top (or the bottom, reading left to right)."""
    upm, cmap, gs, hmtx, cap = _m(font)
    names = [cmap[ord(c)] for c in s]
    sy = cap_h / cap
    sx = sy * xscale
    adv = sum(hmtx[n][0] for n in names) * sx + track * (len(names) - 1)
    pen, pos = SVGPathPen(gs), 0.0
    for n in names:
        gw = hmtx[n][0] * sx
        mid = pos + gw / 2 - adv / 2
        if not bottom:
            th = -math.pi / 2 + mid / r
            rr, ph = r, th + math.pi / 2
        else:
            th = math.pi / 2 - mid / r
            rr, ph = r + cap_h, th - math.pi / 2
        px, py = cx + rr * math.cos(th), cy + rr * math.sin(th)
        a, b = sx * math.cos(ph), sx * math.sin(ph)
        c, d = sy * math.sin(ph), -sy * math.cos(ph)
        gs[n].draw(TransformPen(pen, (a, b, c, d, px - gw / 2 / sx * a, py - gw / 2 / sx * b)))
        pos += gw + track
    return f'<path d="{pen.getCommands()}" fill="{fill}" stroke="{fill}" stroke-width="{bold}" stroke-linejoin="round"/>'

def stripes(y, x0, x1, cols, h=50, gap=34):
    return "".join(f'<rect x="{x0}" y="{y + k * (h + gap)}" width="{x1 - x0}" height="{h}" rx="{h // 2}" fill="{c}"/>' for k, c in enumerate(cols))

def star(cx, cy, R, fill, r=None):
    r = r or R * 0.42
    pts = [(cx + (R if k % 2 == 0 else r) * math.cos(-math.pi / 2 + k * math.pi / 5), cy + (R if k % 2 == 0 else r) * math.sin(-math.pi / 2 + k * math.pi / 5)) for k in range(10)]
    return '<polygon points="%s" fill="%s"/>' % (" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), fill)

def sparkle(cx, cy, s, col):
    return (f'<path d="M{cx} {cy-s} Q{cx+s*0.18} {cy-s*0.18} {cx+s} {cy} Q{cx+s*0.18} {cy+s*0.18} {cx} {cy+s} '
            f'Q{cx-s*0.18} {cy+s*0.18} {cx-s} {cy} Q{cx-s*0.18} {cy-s*0.18} {cx} {cy-s} Z" fill="{col}"/>')

def svg(*parts):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(parts) + "</svg>"

def render(svg_text):
    return Image.open(BytesIO(cairosvg.svg2png(bytestring=svg_text.encode()))).convert("RGBA")

def wear(img, seed=3):
    """Subtle screen-print wear: fine speckle + small worn patches knocked out of the alpha."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.getchannel("A"), dtype=np.float32) / 255
    def up(arr, size, resample, blur=0):
        im = Image.fromarray((arr * 255).astype(np.uint8)).resize((W, H), resample)
        if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
        return np.asarray(im, dtype=np.float32) / 255
    blot = up(rng.random((H // 40, W // 40)).astype(np.float32), None, Image.BICUBIC, 6)
    speck = up(rng.random((H // 3, W // 3)).astype(np.float32), None, Image.NEAREST)
    hole = (blot > 0.905) * 0.9 + (speck > 0.985) * 0.9
    out = img.copy()
    out.putalpha(Image.fromarray((a * (1 - np.clip(hole, 0, 1)) * 255).astype(np.uint8)))
    return out

def on_color(design, color=(17, 17, 17), size=(900, 1100)):
    bg = Image.new("RGBA", (W, H), color + (255,)); bg.alpha_composite(design); bg.thumbnail(size)
    return bg.convert("RGB")

def shirt(design, color=(24, 24, 28)):
    im = Image.new("RGB", (1000, 1100), (236, 236, 238)); d = ImageDraw.Draw(im)
    d.polygon([(300, 170), (400, 150), (500, 185), (600, 150), (700, 170), (880, 290), (800, 430), (730, 380), (730, 980), (270, 980), (270, 380), (200, 430), (120, 290)], fill=color)
    d.ellipse((410, 130, 590, 230), fill=(236, 236, 238))
    art = design.copy(); art.thumbnail((380, 465)); im.paste(art, (500 - art.width // 2, 300), art)
    return im
