"""Template: layered mountains under a big moon, 4500x5500 transparent, for dark shirts.

Usage: python scripts/templates/mountain_moon.py "Trail" "Therapy" out_dir [palette]
"""
import math, random, sys
from pathlib import Path
import cairosvg
sys.path.insert(0, str(Path(__file__).parent))
from retro_sunset import text, mix, W, H

PALETTES = {  # moon, far ridge, near ridge, text
    "forest": ("#F4EAD5", "#3F7D58", "#1F4D36", "#F4EAD5"),
    "dusk":   ("#FFE8A3", "#7B6FD6", "#3D2F8F", "#FFE8A3"),
    "ember":  ("#FFD9B0", "#D9663D", "#8C2F1B", "#FFD9B0"),
}

def ridge(seed, base, amp, color, steps=14):
    rnd = random.Random(seed)
    pts = [(0, H)]
    for i in range(steps + 1):
        x = W * i / steps
        pts.append((x, base - rnd.uniform(0.25, 1.0) * amp * (1 if i % 2 else 0.55)))
    pts.append((W, H))
    return '<polygon points="%s" fill="%s"/>' % (" ".join(f"{x:.0f},{y:.0f}" for x, y in pts), color)

def build(line1, line2, palette="forest", seed=7):
    moon, far, near, ink = PALETTES[palette]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    # badge area: clip everything into a rounded frame by drawing ridges inside limited box
    p.append(f'<circle cx="2250" cy="1900" r="1050" fill="{moon}"/>')
    p.append(f'<circle cx="2650" cy="1600" r="260" fill="{mix(moon, "#000000", 0.08)}" opacity="0.6"/>')
    p.append(f'<circle cx="1800" cy="2250" r="170" fill="{mix(moon, "#000000", 0.08)}" opacity="0.6"/>')
    # ridges drawn then masked below the badge by covering with background-free cut: keep within y<3900
    g = [ridge(seed, 3500, 900, far), ridge(seed + 1, 3750, 800, near)]
    p += [r.replace(f'0,{H}', '0,3780').replace(f'{W},{H}', f'{W},3780') for r in g]
    p.append(text(2250, 4500, line1, 900, ink, 3700))
    p.append(text(2250, 5250, line2, 900, mix(ink, far, 0.35), 3700))
    p.append("</svg>")
    return "".join(p)

if __name__ == "__main__":
    l1, l2, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    pal = sys.argv[4] if len(sys.argv) > 4 else "forest"
    out.mkdir(parents=True, exist_ok=True)
    svg = build(l1.upper(), l2.upper(), pal)
    (out / f"mountain_moon_{pal}.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"mountain_moon_{pal}.png"))
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"preview_mm_{pal}.png"), output_width=900, background_color="#111111")
