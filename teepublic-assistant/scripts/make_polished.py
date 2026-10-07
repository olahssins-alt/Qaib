"""Polished retro text design: condensed bold type, racing stripes, subtle vintage wear.

Usage: python scripts/make_polished.py out_dir
Needs: pip install cairosvg fonttools pillow numpy
Output: design.png (4500x5500 transparent, worn look), design_clean.png (no wear),
        preview-on-black.png, mockup-shirt.png
"""
import sys
from pathlib import Path
import cairosvg, numpy as np
from io import BytesIO
from PIL import Image, ImageDraw, ImageFilter
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

W, H = 4500, 5500
FONT = TTFont("/usr/share/fonts/opentype/inter/Inter-Black.otf")
CREAM, MUSTARD, RUST, TEAL = "#F5E6C8", "#F2B134", "#D9552B", "#2A9D8F"

def type_line(cx, base, s, cap_h, width, fill, xscale=0.72, track=0, bold=18):
    """Condensed outline text: x-squeezed Inter Black, optional tracking, fitted to `width`."""
    upm, cmap, gs, hmtx = FONT["head"].unitsPerEm, FONT.getBestCmap(), FONT.getGlyphSet(), FONT["hmtx"]
    names = [cmap[ord(c)] for c in s]
    cap = FONT["OS/2"].sCapHeight
    sy = cap_h / cap
    sx = sy * xscale
    adv = sum(hmtx[n][0] for n in names) * sx + track * (len(names) - 1)
    if adv > width:  # shrink uniformly to fit
        k = width / adv
        sx, sy, track = sx * k, sy * k, track * k
        adv = width
    pen, cur = SVGPathPen(gs), cx - adv / 2
    for n in names:
        gs[n].draw(TransformPen(pen, (sx, 0, 0, -sy, cur, base)))
        cur += hmtx[n][0] * sx + track
    return f'<path d="{pen.getCommands()}" fill="{fill}" stroke="{fill}" stroke-width="{bold}" stroke-linejoin="round"/>'

def stripes(y, x0, x1, h=64, gap=40):
    out = []
    for k, c in enumerate((MUSTARD, RUST, TEAL)):
        out.append(f'<rect x="{x0}" y="{y + k * (h + gap)}" width="{x1 - x0}" height="{h}" rx="{h // 2}" fill="{c}"/>')
    return "".join(out)

def build():
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    L, R = 350, W - 350
    p.append(type_line(W / 2, 1750, "COFFEE FIRST", 1000, R - L, CREAM))
    p.append(stripes(1930, L, R))
    p.append(type_line(W / 2, 3520, "THEN PEOPLE", 1000, R - L, CREAM))
    p.append(stripes(3700, L, R))
    p.append(type_line(W / 2, 4780, "NO TALKING BEFORE 9 AM", 230, R - L - 300, MUSTARD, xscale=0.9, track=60, bold=6))
    p.append("</svg>")
    return "".join(p)

def wear(img, seed=3, strength=1.0):
    """Vintage wear: tiny speckles + a few blotchy patches knocked out of the alpha. Subtle, stays readable."""
    rng = np.random.default_rng(seed)
    a = np.asarray(img.getchannel("A"), dtype=np.float32) / 255
    small = rng.random((H // 40, W // 40)).astype(np.float32)           # blotches
    blot = np.asarray(Image.fromarray((small * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC).filter(ImageFilter.GaussianBlur(6)), dtype=np.float32) / 255
    speck = rng.random((H // 3, W // 3)).astype(np.float32)             # fine grain
    speck = np.asarray(Image.fromarray((speck * 255).astype(np.uint8)).resize((W, H), Image.NEAREST), dtype=np.float32) / 255
    hole = (blot > 0.90 - 0.02 * strength) * 0.9 + (speck > 0.975 - 0.004 * strength) * 0.9
    a = a * (1 - np.clip(hole, 0, 1))
    out = img.copy()
    out.putalpha(Image.fromarray((a * 255).astype(np.uint8)))
    return out

def shirt_mockup(design, color=(24, 24, 28)):
    S = (1000, 1100)
    im = Image.new("RGB", S, (236, 236, 238))
    d = ImageDraw.Draw(im)
    body = [(300, 170), (400, 150), (500, 185), (600, 150), (700, 170), (880, 290), (800, 430), (730, 380), (730, 980), (270, 980), (270, 380), (200, 430), (120, 290)]
    d.polygon(body, fill=color)
    d.ellipse((410, 130, 590, 230), fill=(236, 236, 238))
    art = design.copy(); art.thumbnail((380, 465))
    im.paste(art, (500 - art.width // 2, 300), art)
    return im

if __name__ == "__main__":
    out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
    png = cairosvg.svg2png(bytestring=build().encode())
    clean = Image.open(BytesIO(png)).convert("RGBA")
    worn = wear(clean)
    (out / "design.svg").write_text(build())
    clean.save(out / "design_clean.png"); worn.save(out / "design.png")
    bg = Image.new("RGBA", (W, H), (17, 17, 17, 255)); bg.alpha_composite(worn); bg.thumbnail((900, 1100)); bg.convert("RGB").save(out / "preview-on-black.png")
    shirt_mockup(worn).save(out / "mockup-shirt.png")
