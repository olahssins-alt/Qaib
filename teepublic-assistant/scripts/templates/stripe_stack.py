"""Template: bold stacked word with retro racing stripes, text only, 4500x5500 transparent.

Usage: python scripts/templates/stripe_stack.py "Plant" "Parent" "Club" out_dir [palette]
"""
import sys
from pathlib import Path
import cairosvg
sys.path.insert(0, str(Path(__file__).parent))
from retro_sunset import text, W, H

PALETTES = {  # stripes (3), text
    "retro":  (("#F2B84B", "#E4572E", "#2A9D8F"), "#F4EAD5"),
    "candy":  (("#FF99C8", "#FCF6BD", "#A9DEF9"), "#FFFFFF"),
    "forest": (("#95D5B2", "#52B788", "#2D6A4F"), "#F1FAEE"),
}

def build(a, b, c, palette="retro"):
    stripes, ink = PALETTES[palette]
    p = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">']
    ys = [1250, 2650, 4050]
    for y, word, size in zip(ys, (a, b, c), (1000, 1250, 1000)):
        for k, col in enumerate(stripes):
            p.append(f'<rect x="300" y="{y + 330 + k * 85}" width="3900" height="50" rx="25" fill="{col}"/>')
        p.append(text(2250, y + 230, word, size, ink, 3900))
    p.append("</svg>")
    return "".join(p)

if __name__ == "__main__":
    a, b, c, out = sys.argv[1], sys.argv[2], sys.argv[3], Path(sys.argv[4])
    pal = sys.argv[5] if len(sys.argv) > 5 else "retro"
    out.mkdir(parents=True, exist_ok=True)
    svg = build(a.upper(), b.upper(), c.upper(), pal)
    (out / f"stripe_stack_{pal}.svg").write_text(svg)
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"stripe_stack_{pal}.png"))
    cairosvg.svg2png(bytestring=svg.encode(), write_to=str(out / f"preview_ss_{pal}.png"), output_width=900, background_color="#111111")
