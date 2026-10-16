"""Batch 8 (plan 16 Oct): idea C3 'One More Chapter, Then Pie' (book lovers x Thanksgiving).
Five styles: book-spine stack, library checkout card, ex libris bookplate, hand-drawn doodle, e-reader UI.
Usage: python scripts/make_batch8.py batch-08
"""
import math, sys
from pathlib import Path
from fontTools.ttLib import TTFont
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import font, arc, star, sparkle, svg, render, wear, on_color, W, H
from fx import warp, p, outlined, heart
from motifs import pie, pumpkin, maple, book_side, at

ABRIL, PLAY_IT, PLAY, CORM, ELITE, CAVEAT, GRAD, BEBAS = (font("abril-fatface-latin-400-normal"), font("playfair-display-latin-900-italic"),
    font("playfair-display-latin-700-normal"), font("cormorant-garamond-latin-600-italic"), font("special-elite-latin-400-normal"),
    font("caveat-latin-700-normal"), font("graduate-latin-400-normal"), font("bebas-neue-latin-400-normal"))
INTER_SB = TTFont("/usr/share/fonts/opentype/inter/Inter-SemiBold.otf")
INTER_R = TTFont("/usr/share/fonts/opentype/inter/Inter-Regular.otf")
CREAM, RUST, MUSTARD, SAGE, BURG, GOLD, INK, FOREST, PLUM = "#F4EAD8", "#C8553D", "#E9A23B", "#7FA88E", "#7E2A35", "#D9A84E", "#2A1F1A", "#2F5D45", "#5B3A6B"

# 1 book stack with the phrase on the spines
def d1():
    # read top to bottom: ONE / MORE / CHAPTER / THEN / PIE
    books = [("ONE", 2000, 520, FOREST, -60), ("MORE", 2500, 560, MUSTARD, 80), ("CHAPTER", 3500, 640, BURG, -40), ("THEN", 2700, 560, SAGE, 90), ("PIE", 3100, 640, RUST, -70)]
    o, y = [], 5250
    for word, w, h, col, dx in reversed(books):
        y -= h + 14
        x = 2250 - w / 2 + dx
        o.append(at(x, y, book_side(w, h, col)))
        ink = INK if col in (MUSTARD, SAGE) else CREAM
        o.append(p(warp(2250 + dx, y + h * 0.72, word, h * 0.5, w * 0.72, ABRIL, track=30), ink))
    o.append(at(2250 - 60, y - 640, f'<g transform="scale(3.0)">{pie()}</g>'))
    for x, yy, a, c in ((700, 900, -20, RUST), (3800, 1000, 25, MUSTARD), (500, 2300, 40, MUSTARD), (4000, 2400, -30, RUST)):
        o.append(at(x, yy, maple(2.2, c, "#00000033"), rot=a))
    return svg(*o)

# 2 library checkout card
def d2():
    paper, blue, purple, red = "#F1E6CC", "#2E4A8A", "#6A3FA0", "#B23A3A"
    x0, y0, w, h = 900, 500, 2700, 4500
    o = [f'<rect x="{x0-120}" y="{y0+2600}" width="{w+240}" height="{h-2350}" rx="30" fill="#C9A26A"/>']  # pocket behind
    o.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="20" fill="{paper}"/>')
    o.append(p(warp(2250, y0 + 330, "DATE DUE", 230, 2000, ELITE, track=80), red))
    o.append(f'<line x1="{x0+100}" y1="{y0+430}" x2="{x0+w-100}" y2="{y0+430}" stroke="{red}" stroke-width="14"/>')
    o.append(f'<line x1="{x0+900}" y1="{y0+430}" x2="{x0+900}" y2="{y0+h-120}" stroke="{red}" stroke-width="10"/>')
    rows = [("NOV 25", "ONE MORE CHAPTER"), ("NOV 25", "OK, ONE MORE"), ("NOV 26", "JUST ONE MORE"), ("NOV 26", "THEN PIE"), ("", ""), ("", "")]
    for i, (dte, note) in enumerate(rows):
        yy = y0 + 430 + (i + 1) * 520
        o.append(f'<line x1="{x0+100}" y1="{yy}" x2="{x0+w-100}" y2="{yy}" stroke="{blue}" stroke-width="8" opacity="0.6"/>')
        if dte:
            c = purple if i < 3 else red
            o.append(f'<g transform="rotate({(-2, 1.5, -1, 2)[i]} {x0+500} {yy-200})">' + p(warp(x0 + 500, yy - 170, dte, 150, 700, ELITE, track=30), c) + "</g>")
            o.append(p(warp(x0 + 1750, yy - 170, note, 130 if i < 3 else 210, 1600, ELITE if i < 3 else ABRIL, track=20), INK if i < 3 else red))
    o.append(at(x0 + w - 470, y0 + h - 520, f'<g transform="scale(1.6)">{pie()}</g>', rot=-8))
    return svg(*o)

# 3 ex libris bookplate (dark academia)
def d3():
    cx, cy = 2250, 2700
    o = [f'<ellipse cx="{cx}" cy="{cy}" rx="1800" ry="2300" fill="{BURG}"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="1700" ry="2200" fill="none" stroke="{GOLD}" stroke-width="30"/>',
         f'<ellipse cx="{cx}" cy="{cy}" rx="1620" ry="2120" fill="none" stroke="{GOLD}" stroke-width="10"/>']
    o.append(p(warp(cx, 1300, "EX LIBRIS", 300, 2000, PLAY, track=160), GOLD))
    for x, y in ((cx - 1150, 1700), (cx + 1150, 1700), (cx - 1350, 2700), (cx + 1350, 2700)):
        o.append(star(x, y, 60, GOLD))
    # open book with pie on it
    bx, by = cx, 2350
    o.append(f'<path d="M{bx-900} {by} Q{bx-450} {by-260} {bx} {by} L{bx} {by+620} Q{bx-450} {by+360} {bx-900} {by+620} Z" fill="{CREAM}" stroke="{GOLD}" stroke-width="20"/>')
    o.append(f'<path d="M{bx+900} {by} Q{bx+450} {by-260} {bx} {by} L{bx} {by+620} Q{bx+450} {by+360} {bx+900} {by+620} Z" fill="{CREAM}" stroke="{GOLD}" stroke-width="20"/>')
    for i in range(4):
        yy = by + 120 + i * 110
        o.append(f'<path d="M{bx-760} {yy} Q{bx-430} {yy-150} {bx-120} {yy}" stroke="#C9B48E" stroke-width="22" fill="none"/>')
        o.append(f'<path d="M{bx+760} {yy} Q{bx+430} {yy-150} {bx+120} {yy}" stroke="#C9B48E" stroke-width="22" fill="none"/>')
    o.append(at(bx, by - 330, f'<g transform="scale(2.2)">{pie()}</g>'))
    o.append(p(warp(cx, 3600, "One more chapter,", 330, 2600, PLAY_IT), CREAM))
    o.append(p(warp(cx, 4100, "then pie", 420, 2200, PLAY_IT), GOLD))
    o.append(star(cx, 4450, 70, GOLD))
    return svg(*o)

# 4 hand-drawn doodle
def d4():
    st = f'stroke="{CREAM}" stroke-width="26" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    o = [p(warp(2250, 1350, "one more", 520, 3000, CAVEAT), CREAM), p(warp(2250, 2050, "chapter...", 620, 3600, CAVEAT), MUSTARD)]
    o.append(f'<path d="M3500 2150 C 3850 2450 3850 2900 3550 3150" {st}/><path d="M3450 3060 l100 100 l110 -70" {st}/>')
    o.append(p(warp(2250, 4050, "then pie", 760, 3700, CAVEAT), RUST))
    # doodle open book left, coffee right, leaves
    o.append(f'<path d="M700 2450 q300 -120 600 0 v420 q-300 -120 -600 0 Z M1300 2450 q300 -120 600 0 v420 q-300 -120 -600 0 Z" {st}/>')
    for i in range(3):
        o.append(f'<path d="M780 {2530+i*90} q220 -70 440 0 M1380 {2530+i*90} q220 -70 440 0" stroke="{CREAM}" stroke-width="12" fill="none" opacity="0.7"/>')
    o.append(f'<path d="M2500 2500 h420 v260 a140 140 0 0 1 -140 140 h-140 a140 140 0 0 1 -140 -140 Z M2920 2570 a90 90 0 0 1 0 180" {st}/>')
    o.append(f'<path d="M2600 2430 q-40 -70 0 -140 M2750 2430 q-40 -70 0 -140" {st}/>')
    o.append(at(2250, 4650, f'<g transform="scale(2.2)">{pie()}</g>'))
    for x, y, a, c in ((600, 1100, -25, RUST), (3950, 1150, 20, MUSTARD), (650, 4500, 30, MUSTARD), (3900, 4550, -15, RUST)):
        o.append(at(x, y, maple(1.2, c, "#00000033"), rot=a))
    for x, y, s in ((1100, 2550, 70), (3500, 4100, 60), (1000, 4050, 50)):
        o.append(sparkle(x, y, s, CREAM))
    return svg(*o)

# 5 e-reader UI
def d5():
    dev, screen, txt, accent = "#2B2B30", "#EFE9DC", "#3A3530", RUST
    x0, y0, w, h = 900, 400, 2700, 4300
    o = [f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="160" fill="{dev}"/>',
         f'<rect x="{x0+150}" y="{y0+200}" width="{w-300}" height="{h-420}" rx="40" fill="{screen}"/>']
    sx, sw = x0 + 300, w - 600
    o.append(p(warp(2250, y0 + 420, "CHAPTER 27", 110, 1500, INTER_SB, track=40), "#8A8378"))
    for i in range(9):
        wl = sw * (0.96 if i % 4 != 3 else 0.6)
        o.append(f'<rect x="{sx}" y="{y0+620+i*150}" width="{wl:.0f}" height="46" rx="23" fill="#CFC6B6"/>')
    # notification banner
    ny = y0 + 2060
    o.append(f'<rect x="{x0+230}" y="{ny}" width="{w-460}" height="620" rx="70" fill="#FFFFFF" stroke="#D9D1C2" stroke-width="10"/>')
    o.append(at(x0 + 520, ny + 310, f'<g transform="scale(0.95)">{pie()}</g>'))
    o.append(p(warp(x0 + 1550, ny + 250, "Pie is ready", 150, 1500, INTER_SB), txt))
    o.append(p(warp(x0 + 1550, ny + 450, "Finish your chapter. Or don't.", 85, 1500, INTER_R), "#7A7368"))
    # progress
    py = y0 + 3150
    o.append(f'<rect x="{sx}" y="{py}" width="{sw}" height="56" rx="28" fill="#D9D1C2"/><rect x="{sx}" y="{py}" width="{sw*0.98:.0f}" height="56" rx="28" fill="{accent}"/>')
    o.append(p(warp(sx + 300, py + 230, "98%", 120, 600, INTER_SB), txt))
    o.append(p(warp(sx + sw - 520, py + 230, "1 chapter to pie", 90, 1100, INTER_R), "#7A7368"))
    o.append(f'<rect x="{2250-200}" y="{y0+h-140}" width="400" height="40" rx="20" fill="#555560"/>')
    o.append(p(warp(2250, 5200, "ONE MORE CHAPTER, THEN PIE", 200, 3700, GRAD, track=40), CREAM))
    return svg(*o)

DESIGNS = {"c1-one-more-chapter-then-pie-book-stack": d1, "c2-library-card-date-due-pie": d2, "c3-ex-libris-then-pie": d3,
           "c4-one-more-chapter-doodle": d4, "c5-ereader-pie-is-ready": d5}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for slug, fn in DESIGNS.items():
        dd = out / slug; dd.mkdir(parents=True, exist_ok=True)
        s = fn(); (dd / "design.svg").write_text(s)
        img = render(s); img.save(dd / "design.png"); on_color(img).save(dd / "preview-on-black.png"); print(slug)
