"""Batch 2, ugly-sweater knit style (owner's pick): idea E1 'Supervising the Christmas Tree'.
Usage: python scripts/make_batch2_knit.py batch-02
"""
import random, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "kit"))
from design_kit import render, on_color
from knit import *

RED, GREEN, DGREEN, CREAM, GOLD, BLUE, BROWN = "#D7263D", "#1FA35B", "#0E6B3B", "#F4EFE3", "#F5B700", "#4CC9F0", "#8B5A2B"
GRAY, ORANGE, PINK, EYE, BLACK, BELLY = "#A3ADB8", "#F28C28", "#FF8FA3", "#3DDC84", "#1A1A1A", "#FFF6E8"
TREE_PAL = {"Y": GOLD, "G": GREEN, "R": RED, "B": BLUE, "N": BROWN}
def cat_pal(fur, stripe):
    return {"W": fur, "G": BELLY if fur != CREAM else "#D9D2C3", "P": PINK, "E": EYE, "K": BLACK, "S": stripe, "T": fur}

def border(k, r0, main, accent, flip=False):
    rows = [ZIG, DOTS, SNOW] if not flip else [SNOW, DOTS, ZIG]
    r = r0
    for pat in rows:
        if pat is SNOW:
            for i, c in enumerate(range(3, COLS - 6, 12)):
                k.sprite(SNOW, c, r, {"X": accent if i % 2 else CREAM})
            r += 9
        else:
            k.band(pat, r, main if pat is ZIG else CREAM, 2, COLS - 2); r += len(pat) + 2
    return r

def p1():
    k = Knit()
    border(k, 2, RED, GREEN)
    k.big("SUPERVISING", 26, CREAM)
    k.small("THE CHRISTMAS TREE", 37, GOLD)
    k.sprite(TREE, 6, 46, TREE_PAL, 3)
    k.sprite(CAT, 60, 70, cat_pal(CREAM, "#D9D2C3"), 2)
    border(k, 104, GREEN, RED, flip=True)
    return k.svg()

def p2():
    k = Knit()
    for c in range(3, 97):
        k.set(c, 3, CREAM); k.set(c, 118, CREAM)
    for r in range(3, 119):
        k.set(3, r, CREAM); k.set(96, r, CREAM)
    k.small("TREE HP", 8, CREAM, scale=2, c0=8)
    for i, hrt in enumerate((HEART, HEART, HEART_EMPTY)):
        k.sprite(hrt, 72 + i * 8, 9, {"X": RED})
    k.sprite(TREE, 22, 26, TREE_PAL, 3)
    k.sprite(CAT, 48, 44, cat_pal(ORANGE, "#B5581F"), 2)
    for c in range(8, 92):
        k.set(c, 81, CREAM)
    k.big("CAT VS TREE", 88, GOLD)
    k.small("PRESS START TO CLIMB", 102, CREAM)
    return k.svg()

def p3():
    k = Knit()
    k.big("GRAVITY", 6, GOLD, scale=1)
    k.big("TEST", 17, CREAM, scale=2)
    for c in range(8, 70):
        k.set(c, 66, CREAM); k.set(c, 67, CREAM)
    k.sprite(CAT, 22, 34, cat_pal(GRAY, "#6B7682"), 2)
    k.sprite(["XXX", "XXX"], 54, 58, {"X": GRAY})     # reaching paw
    k.sprite(ORN, 58, 54, {"X": RED, "Y": GOLD, "H": CREAM}, 2)
    k.sprite(ORN, 72, 72, {"X": "#8F1B29", "Y": "#9C7A00", "H": "#8F1B29"}, 2)
    k.sprite(ORN, 76, 88, {"X": "#5A1119", "Y": "#5E4A00", "H": "#5A1119"}, 2)
    for r in (69, 71, 85, 87):
        k.set(70, r, CREAM)
    k.big("ORNAMENT", 104, CREAM)
    k.big("EDITION", 114, RED)
    return k.svg()

def p4():
    k = Knit()
    def motif_rows(r0):
        k.band(ZIG, r0, GREEN, 2, COLS - 2)
        for i, c in enumerate(range(4, COLS - 8, 12)):
            if i % 2 == 0: k.sprite(CAT_HEAD, c, r0 + 8, {"W": CREAM, "E": RED, "P": RED})
            else: k.sprite(TREE_MINI, c, r0 + 7, {"X": GREEN})
        k.band(DOTS, r0 + 17, CREAM, 2, COLS - 2)
        k.band(ZIG, r0 + 20, RED, 2, COLS - 2, offset=4)
    motif_rows(3)
    k.big("CAT", 34, CREAM, scale=2)
    k.big("SUPERVISED", 55, RED)
    k.small("CHRISTMAS TREE", 66, GOLD, scale=1)
    for i, c in enumerate(range(14, 86, 18)):
        k.sprite(SNOW, c, 76, {"X": CREAM if i % 2 else GREEN})
    motif_rows(92)
    return k.svg()

def p5():
    k = Knit()
    rnd = random.Random(5)
    k.big("THIS TREE IS", 4, CREAM)
    k.sprite(TREE[2:], 20, 46, TREE_PAL, 4)
    k.sprite(CAT, 34, 16, cat_pal(ORANGE, "#B5581F"), 2)
    for _ in range(60):
        c, r = rnd.randrange(2, 98), rnd.randrange(16, 108)
        if not any((c + dx, r + dy) in k.g for dx in (-1, 0, 1) for dy in (-1, 0, 1)):
            k.set(c, r, CREAM)
    k.big("A CAT TOWER", 112, GOLD)
    return k.svg()

DESIGNS = {"k1-supervising-the-christmas-tree": p1, "k2-cat-vs-tree-8bit": p2, "k3-gravity-test-pixel": p3,
           "k4-cat-supervised-fair-isle": p4, "k5-this-tree-is-a-cat-tower": p5}

if __name__ == "__main__":
    out = Path(sys.argv[1])
    for slug, fn in DESIGNS.items():
        d = out / slug; d.mkdir(parents=True, exist_ok=True)
        s = fn(); (d / "design.svg").write_text(s)
        img = render(s); img.save(d / "design.png"); on_color(img).save(d / "preview-on-black.png"); print(slug)
