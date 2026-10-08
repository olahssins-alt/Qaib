"""Ugly-sweater pixel style: compose on a stitch grid, render every cell as a knit 'V' stitch."""
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from design_kit import FONTS_DIR, W, H

U = 45                      # stitch size in px
COLS, ROWS = W // U, H // U  # 100 x 122

F35 = {  # 3x5 pixel font
 "A":"010101111101101","B":"110101110101110","C":"011100100100011","D":"110101101101110","E":"111100110100111",
 "F":"111100110100100","G":"011100101101011","H":"101101111101101","I":"111010010010111","J":"001001001101010",
 "K":"101101110101101","L":"100100100100111","M":"101111111101101","N":"110101101101101","O":"010101101101010",
 "P":"110101110100100","Q":"010101101110011","R":"110101110101101","S":"011100010001110","T":"111010010010010",
 "U":"101101101101111","V":"101101101101010","W":"101101111111101","X":"101101010101101","Y":"101101010010010",
 "Z":"111001010100111","0":"111101101101111","1":"010110010010111","2":"110001010100111","3":"110001010001110",
 "4":"101101111001001","5":"111100110001110","6":"011100111101111","7":"111001010010010","8":"111101111101111",
 "9":"111101111001110",":":"000010000010000","!":"010010010000010","-":"000000111000000",".":"000000000000010",
 "'":"010010000000000"," ":"000000000000000"}

class Knit:
    def __init__(self):
        self.g = {}
    def set(self, c, r, color):
        if 0 <= c < COLS and 0 <= r < ROWS and color:
            self.g[(c, r)] = color
    def sprite(self, rows, c0, r0, pal, scale=1):
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                if ch in pal:
                    for dy in range(scale):
                        for dx in range(scale):
                            self.set(c0 + c * scale + dx, r0 + r * scale + dy, pal[ch])
    def _place(self, bits, r0, color, c0=None, scale=1):
        h, w = len(bits), max(len(b) for b in bits)
        if c0 is None:
            c0 = (COLS - w * scale) // 2
        self.sprite(["".join("X" if v else "." for v in row) for row in bits], c0, r0, {"X": color}, scale)
        return w * scale
    def big(self, s, r0, color, scale=1, c0=None):
        """Press Start 2P at its native 8px grid (7 stitches tall per scale)."""
        f = ImageFont.truetype(str(FONTS_DIR / "press-start-2p-latin-400-normal.woff"), 8)
        im = Image.new("1", (8 * len(s) + 8, 10), 0); d = ImageDraw.Draw(im); d.fontmode = "1"; d.text((0, 0), s, font=f, fill=1)
        a = np.array(im)[:7]; cols = np.where(a.any(0))[0]; a = a[:, cols.min():cols.max() + 1]
        return self._place(a.tolist(), r0, color, c0, scale)
    def small(self, s, r0, color, scale=1, c0=None):
        """3x5 font, 4 stitches per character."""
        rows = [[] for _ in range(5)]
        for i, ch in enumerate(s.upper()):
            bits = F35[ch]
            for r in range(5):
                rows[r] += [b == "1" for b in bits[r*3:r*3+3]] + ([False] if i < len(s) - 1 else [])
        return self._place(rows, r0, color, c0, scale)
    def band(self, pattern, r0, color, c_from=0, c_to=COLS, offset=0):
        """Repeat a small pattern (list of strings) across the width."""
        pw = len(pattern[0])
        for r, row in enumerate(pattern):
            for c in range(c_from, c_to):
                if row[(c + offset) % pw] == "X":
                    self.set(c, r0 + r, color)
    def svg(self):
        out = []
        rx, ry = U * 0.27, U * 0.56
        for (c, r), col in self.g.items():
            x, y = c * U, r * U
            for dx, ang in ((0.29, -24), (0.71, 24)):
                cx, cy = x + U * dx, y + U * 0.5
                out.append(f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{col}" transform="rotate({ang} {cx:.1f} {cy:.1f})"/>')
        return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">' + "".join(out) + "</svg>"

# ---- shared motifs ----
ZIG = ["X.......", ".X.....X", "..X...X.", "...X.X..", "....X..."]
DOTS = ["X...", "...."]
SNOW = ["...X...", ".X.X.X.", "..XXX..", "XXXXXXX", "..XXX..", ".X.X.X.", "...X..."]
HEART = [".XX.XX.", "XXXXXXX", "XXXXXXX", ".XXXXX.", "..XXX..", "...X..."]
HEART_EMPTY = [".XX.XX.", "X..X..X", "X.....X", ".X...X.", "..X.X..", "...X..."]
ORN = ["..Y..", ".XXX.", "XXHXX", "XXXXX", "XXXXX", ".XXX."]
CAT = ["...W........W...", "..WWW......WWW..", "..WPWW....WWPW..", "..WWWWSWSWWWWW..", ".WWWWWWWWWWWWWW.",
       ".WWEKWWWWWWEKWW.", ".WWEKWWWWWWEKWW.", ".WWWWWWPPWWWWWW.", "..WWWWWWWWWWWW..", "...WWWWWWWWWW...",
       "..WWWWWWWWWWWW..T", ".WWWWGGGGGGWWW..T", ".WWWGGGGGGGGWWW.T", ".WWWGGGGGGGGWWWT.", ".WWWWGGGGGGWWWT..", "..WW.WW..WW.WW..."]
CAT_HEAD = ["W.....W", "WW...WW", "WWWWWWW", "WEWWWEW", "WWWPWWW", ".WWWWW."]
TREE = [".......Y.......", "......YYY......", ".......G.......", "......GGG......", ".....GGRGG.....", "....GGGGGGG....",
        "......GGG......", ".....GGGGG.....", "....GGYGGGG....", "...GGGGGGBGG...", "..GGRGGGGGGGG..", "....GGGGGGG....",
        "...GGGGGGRGG...", "..GGGYGGGGGGG..", ".GGGGGGGGGGGBG.", "GGRGGGGGGYGGGGG", "......NNN......", "......NNN......"]
TREE_MINI = ["...X...", "..XXX..", ".XXXXX.", "..XXX..", ".XXXXX.", "XXXXXXX", "...X..."]
