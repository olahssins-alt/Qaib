"""Text effects and small motifs for trend styles: warped text (arch, wave), outlines, 3D extrusion, bows, pumpkins."""
import math
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from design_kit import _m

def warp(cx, base, s, cap, width, f, yfn=None, rotate=False, xscale=1.0, track=0):
    """Path data for `s` centred on cx. yfn(u) gives a baseline offset for u in 0..1 across the line;
    with rotate=True each glyph tilts to follow the curve. Shrinks to fit `width`."""
    upm, cmap, gs, hmtx, capu = _m(f)
    names = [cmap[ord(c)] for c in s]
    sy = cap / capu; sx = sy * xscale
    adv = sum(hmtx[n][0] for n in names) * sx + track * (len(names) - 1)
    if adv > width:
        k = width / adv; sx, sy, track, adv = sx * k, sy * k, track * k, width
    yfn = yfn or (lambda u: 0)
    pen, pos = SVGPathPen(gs), 0.0
    for n in names:
        gw = hmtx[n][0] * sx
        u = (pos + gw / 2) / adv
        y0 = base + yfn(u)
        ang = 0
        if rotate:
            e = 0.002; ang = math.atan2(yfn(u + e) - yfn(u - e), 2 * e * adv)
        gx = cx - adv / 2 + pos + gw / 2
        ca, sa = math.cos(ang), math.sin(ang)
        # glyph local x is shifted so its centre sits at gx
        a, b, c, d = sx * ca, sx * sa, sy * sa, -sy * ca
        ox = -gw / 2 / sx
        gs[n].draw(TransformPen(pen, (a, b, c, d, gx + ox * a, y0 + ox * b)))
        pos += gw + track
    return pen.getCommands()

def p(d, fill, stroke=None, sw=0, extra=""):
    st = f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round" stroke-linecap="round"' if stroke else ""
    return f'<path d="{d}" fill="{fill}"{st} {extra}/>'

def outlined(d, fill, *rings):
    """rings: (color, width) from outermost to innermost, drawn under the fill."""
    return "".join(p(d, c, c, w) for c, w in rings) + p(d, fill)

def extrude(d, color, dx, dy, steps, sw=0):
    return "".join(f'<g transform="translate({dx*i/steps:.1f} {dy*i/steps:.1f})">' + p(d, color, color if sw else None, sw) + "</g>" for i in range(steps, 0, -1))

def bow(cx, cy, s, col, dark):
    out = []
    for sg in (-1, 1):
        out.append(f'<path d="M{cx} {cy} C{cx+sg*150*s} {cy-260*s} {cx+sg*460*s} {cy-210*s} {cx+sg*430*s} {cy+10*s} C{cx+sg*400*s} {cy+190*s} {cx+sg*150*s} {cy+130*s} {cx} {cy} Z" fill="{col}"/>')
        out.append(f'<path d="M{cx+sg*60*s} {cy-20*s} C{cx+sg*180*s} {cy-120*s} {cx+sg*300*s} {cy-110*s} {cx+sg*330*s} {cy-30*s}" stroke="{dark}" stroke-width="{22*s:.0f}" fill="none" stroke-linecap="round"/>')
        out.append(f'<path d="M{cx+sg*20*s} {cy+40*s} C{cx+sg*90*s} {cy+200*s} {cx+sg*200*s} {cy+330*s} {cx+sg*250*s} {cy+520*s} L{cx+sg*150*s} {cy+470*s} L{cx+sg*95*s} {cy+560*s} C{cx+sg*60*s} {cy+380*s} {cx+sg*20*s} {cy+220*s} {cx-sg*10*s} {cy+50*s} Z" fill="{col}"/>')
    out.append(f'<rect x="{cx-75*s:.0f}" y="{cy-85*s:.0f}" width="{150*s:.0f}" height="{170*s:.0f}" rx="{55*s:.0f}" fill="{col}" stroke="{dark}" stroke-width="{20*s:.0f}"/>')
    return "".join(out)

def pumpkin(cx, cy, s, col, dark, stem="#6B8F4E"):
    out = [f'<rect x="{cx-28*s:.0f}" y="{cy-230*s:.0f}" width="{56*s:.0f}" height="{120*s:.0f}" rx="{20*s:.0f}" fill="{stem}" transform="rotate(12 {cx} {cy})"/>']
    for dx, rx in ((-150, 140), (150, 140), (-70, 150), (70, 150), (0, 150)):
        out.append(f'<ellipse cx="{cx+dx*s:.0f}" cy="{cy:.0f}" rx="{rx*s:.0f}" ry="{165*s:.0f}" fill="{col}" stroke="{dark}" stroke-width="{14*s:.0f}"/>')
    return "".join(out)

def heart(cx, cy, s, fill=None, stroke=None, sw=0):
    d = f"M{cx} {cy+90*s} C{cx-170*s} {cy-20*s} {cx-110*s} {cy-150*s} {cx} {cy-60*s} C{cx+110*s} {cy-150*s} {cx+170*s} {cy-20*s} {cx} {cy+90*s} Z"
    return p(d, fill or "none", stroke, sw)
