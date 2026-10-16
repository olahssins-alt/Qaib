"""Illustrated motifs drawn in local coordinates (centre 0,0): mahjong tiles, turkey, pie, pumpkin."""
import math

IVORY, IVORY_D, IVORY_L, TILE_BACK = "#FBF3E4", "#E3D3B6", "#EFE3CC", "#2E7A57"
T_RED, T_BLUE, T_GREEN, T_GOLD = "#C8402E", "#2F5D9E", "#2E8A55", "#E2A33A"

def turkey(s=1.0, tail=("#C8553D", "#E9A23B", "#D9772E", "#9C3D2A")):
    o = []
    for i, a in enumerate(range(-75, 76, 25)):
        r = math.radians(a)
        x, y = math.sin(r) * 175 * s, -math.cos(r) * 175 * s - 20 * s
        o.append(f'<ellipse cx="{x:.0f}" cy="{y:.0f}" rx="{70*s:.0f}" ry="{205*s:.0f}" fill="{tail[i % len(tail)]}" transform="rotate({a} {x:.0f} {y:.0f})"/>')
    o.append(f'<ellipse cx="0" cy="{40*s:.0f}" rx="{150*s:.0f}" ry="{165*s:.0f}" fill="#7A4A2E"/>')
    o.append(f'<ellipse cx="0" cy="{80*s:.0f}" rx="{90*s:.0f}" ry="{105*s:.0f}" fill="#A86B44"/>')
    o.append(f'<circle cx="0" cy="{-120*s:.0f}" r="{88*s:.0f}" fill="#8A5636"/>')
    for sg in (-1, 1):
        o.append(f'<circle cx="{sg*32*s:.0f}" cy="{-138*s:.0f}" r="{19*s:.0f}" fill="#FFFFFF"/><circle cx="{sg*32*s:.0f}" cy="{-136*s:.0f}" r="{10*s:.0f}" fill="#1E1410"/>')
        o.append(f'<path d="M{sg*45*s:.0f} {200*s:.0f} l{sg*10*s:.0f} {70*s:.0f} m0 0 l{-30*s:.0f} {25*s:.0f} m{30*s:.0f} {-25*s:.0f} l{25*s:.0f} {25*s:.0f}" stroke="#E9A23B" stroke-width="{16*s:.0f}" stroke-linecap="round" fill="none"/>')
    o.append(f'<polygon points="{-28*s:.0f},{-108*s:.0f} {28*s:.0f},{-108*s:.0f} 0,{-60*s:.0f}" fill="#F2B134"/>')
    o.append(f'<path d="M{12*s:.0f} {-80*s:.0f} q{30*s:.0f} {40*s:.0f} {5*s:.0f} {85*s:.0f} q{-30*s:.0f} {-35*s:.0f} {-5*s:.0f} {-85*s:.0f}Z" fill="#D7263D"/>')
    return "".join(o)

def pie(s=1.0):
    return (f'<path d="M{-200*s:.0f} {40*s:.0f} A{200*s:.0f} {120*s:.0f} 0 0 0 {200*s:.0f} {40*s:.0f} L{200*s:.0f} {90*s:.0f} A{200*s:.0f} {120*s:.0f} 0 0 1 {-200*s:.0f} {90*s:.0f} Z" fill="#C68A4E"/>'
            f'<ellipse cx="0" cy="{40*s:.0f}" rx="{200*s:.0f}" ry="{120*s:.0f}" fill="#E9A23B"/>'
            f'<ellipse cx="0" cy="{40*s:.0f}" rx="{200*s:.0f}" ry="{120*s:.0f}" fill="none" stroke="#C68A4E" stroke-width="{36*s:.0f}"/>'
            + "".join(f'<circle cx="{x*s:.0f}" cy="{(y)*s:.0f}" r="{r*s:.0f}" fill="#FFFFFF"/>' for x, y, r in ((-30, 10, 55), (35, 0, 48), (5, -35, 42))))

def pumpkin(s=1.0, col="#E9803A", dark="#B85A23"):
    o = [f'<rect x="{-24*s:.0f}" y="{-200*s:.0f}" width="{48*s:.0f}" height="{100*s:.0f}" rx="{18*s:.0f}" fill="#6B8F4E" transform="rotate(12)"/>']
    for dx, rx in ((-130, 125), (130, 125), (-60, 135), (60, 135), (0, 135)):
        o.append(f'<ellipse cx="{dx*s:.0f}" cy="0" rx="{rx*s:.0f}" ry="{145*s:.0f}" fill="{col}" stroke="{dark}" stroke-width="{12*s:.0f}"/>')
    return "".join(o)

def _bamboo(x, y, h, s):
    o = [f'<rect x="{x-28*s:.0f}" y="{y-h/2:.0f}" width="{56*s:.0f}" height="{h:.0f}" rx="{28*s:.0f}" fill="{T_GREEN}"/>']
    for k in (-1, 0, 1):
        o.append(f'<rect x="{x-34*s:.0f}" y="{y+k*h/3-8*s:.0f}" width="{68*s:.0f}" height="{16*s:.0f}" rx="{8*s:.0f}" fill="#1F5E3A"/>')
    return "".join(o)

def _dot(x, y, r, col):
    return (f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.0f}" fill="{col}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.62:.0f}" fill="{IVORY}"/>'
            f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r*0.38:.0f}" fill="{col}"/>')

def tile(face="turkey", s=1.0, back=TILE_BACK):
    """A standing mahjong tile 600x800*s centred on 0,0, with green back, ivory depth and an inset face."""
    w, h, r = 600 * s, 800 * s, 80 * s
    o = [f'<rect x="{-w/2+30*s:.0f}" y="{-h/2+40*s:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r:.0f}" fill="{back}"/>',
         f'<rect x="{-w/2+12*s:.0f}" y="{-h/2+18*s:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r:.0f}" fill="{IVORY_D}"/>',
         f'<rect x="{-w/2:.0f}" y="{-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{r:.0f}" fill="{IVORY}"/>',
         f'<rect x="{-w/2+40*s:.0f}" y="{-h/2+40*s:.0f}" width="{w-80*s:.0f}" height="{h-80*s:.0f}" rx="{r*0.6:.0f}" fill="none" stroke="{IVORY_D}" stroke-width="{10*s:.0f}"/>',
         f'<path d="M{-w/2+60*s:.0f} {-h/2+30*s:.0f} h{w-120*s:.0f}" stroke="#FFFFFF" stroke-width="{16*s:.0f}" stroke-linecap="round" opacity="0.8"/>']
    if face == "turkey":
        o.append(f'<g transform="scale({0.95*s:.3f})">{turkey()}</g>')
    elif face == "dots1":
        for rr, c in ((200, T_BLUE), (150, T_RED), (95, T_GREEN), (45, T_RED)):
            o.append(f'<circle cx="0" cy="0" r="{rr*s:.0f}" fill="{c}"/><circle cx="0" cy="0" r="{(rr-22)*s:.0f}" fill="{IVORY}"/>')
        o.append(f'<circle cx="0" cy="0" r="{25*s:.0f}" fill="{T_RED}"/>')
    elif face == "dots3":
        for (x, y), c in zip(((-150, -230), (0, 0), (150, 230)), (T_BLUE, T_RED, T_GREEN)):
            o.append(_dot(x * s, y * s, 95 * s, c))
    elif face == "bam2":
        o.append(_bamboo(0, -150 * s, 270 * s, s)); o.append(_bamboo(0, 160 * s, 270 * s, s))
    elif face == "bam3":
        o.append(_bamboo(0, -150 * s, 260 * s, s)); o.append(_bamboo(-110 * s, 160 * s, 260 * s, s)); o.append(_bamboo(110 * s, 160 * s, 260 * s, s))
    elif face == "pie":
        o.append(f'<g transform="scale({1.1*s:.3f})">{pie()}</g>')
    elif face == "pumpkin":
        o.append(f'<g transform="translate(0 {30*s:.0f}) scale({1.0*s:.3f})">{pumpkin()}</g>')
    elif face == "dragon":
        o.append(f'<rect x="{-150*s:.0f}" y="{-220*s:.0f}" width="{300*s:.0f}" height="{440*s:.0f}" rx="{40*s:.0f}" fill="none" stroke="{T_RED}" stroke-width="{40*s:.0f}"/>')
        o.append(f'<rect x="{-70*s:.0f}" y="{-140*s:.0f}" width="{140*s:.0f}" height="{280*s:.0f}" rx="{20*s:.0f}" fill="{T_RED}"/>')
    return "".join(o)

def at(x, y, inner, rot=0, sc=1.0):
    return f'<g transform="translate({x:.0f} {y:.0f}) rotate({rot}) scale({sc})">{inner}</g>'

def tile_line(s=1.0, col="#F2E9DA", sw=22):
    """Line-art tile seen at a slight angle, for minimal designs."""
    w, h = 600 * s, 800 * s
    return (f'<rect x="{-w/2:.0f}" y="{-h/2:.0f}" width="{w:.0f}" height="{h:.0f}" rx="{80*s:.0f}" fill="none" stroke="{col}" stroke-width="{sw}"/>'
            f'<path d="M{-w/2+20*s:.0f} {h/2+10*s:.0f} q0 {40*s:.0f} {60*s:.0f} {40*s:.0f} h{w-120*s:.0f} q{60*s:.0f} 0 {60*s:.0f} {-40*s:.0f}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linecap="round"/>')

BALL, BALL_D = "#D8F23D", "#9DB81C"

def ball(s=1.0, holes=True):
    """Pickleball with a ring of holes and a highlight."""
    o = [f'<circle cx="0" cy="0" r="{200*s:.0f}" fill="{BALL}"/>']
    if holes:
        for (x, y) in ((-95, -70), (20, -120), (110, -40), (-120, 50), (-10, 20), (90, 90), (-40, 130), (40, -40)):
            o.append(f'<circle cx="{x*s:.0f}" cy="{y*s:.0f}" r="{24*s:.0f}" fill="{BALL_D}"/>')
    o.append(f'<path d="M{-140*s:.0f} {-60*s:.0f} A{150*s:.0f} {150*s:.0f} 0 0 1 {-40*s:.0f} {-160*s:.0f}" stroke="#FFFFFF" stroke-width="{22*s:.0f}" fill="none" stroke-linecap="round" opacity="0.6"/>')
    return "".join(o)

def paddle(s=1.0, face="#2F6FB0", edge="#1B3F66", grip="#2A2A2A"):
    """Pickleball paddle pointing up, handle at the bottom, centre of the face at 0,0."""
    o = [f'<rect x="{-55*s:.0f}" y="{230*s:.0f}" width="{110*s:.0f}" height="{330*s:.0f}" rx="{40*s:.0f}" fill="{grip}"/>']
    for k in range(5):
        o.append(f'<path d="M{-55*s:.0f} {(270+k*60)*s:.0f} l{110*s:.0f} {30*s:.0f}" stroke="#555555" stroke-width="{12*s:.0f}"/>')
    o.append(f'<rect x="{-70*s:.0f}" y="{540*s:.0f}" width="{140*s:.0f}" height="{40*s:.0f}" rx="{18*s:.0f}" fill="{edge}"/>')
    o.append(f'<path d="M{-220*s:.0f} {-150*s:.0f} Q{-220*s:.0f} {-330*s:.0f} 0 {-330*s:.0f} Q{220*s:.0f} {-330*s:.0f} {220*s:.0f} {-150*s:.0f} L{220*s:.0f} {120*s:.0f} Q{220*s:.0f} {260*s:.0f} {80*s:.0f} {270*s:.0f} L{-80*s:.0f} {270*s:.0f} Q{-220*s:.0f} {260*s:.0f} {-220*s:.0f} {120*s:.0f} Z" fill="{face}" stroke="{edge}" stroke-width="{34*s:.0f}"/>')
    o.append(f'<path d="M{-150*s:.0f} {-180*s:.0f} Q{-150*s:.0f} {-260*s:.0f} {-60*s:.0f} {-270*s:.0f}" stroke="#FFFFFF" stroke-width="{20*s:.0f}" fill="none" stroke-linecap="round" opacity="0.45"/>')
    return "".join(o)

FRENCHIE_COATS = {  # base, muzzle/chest, ear inner, dark (nose, wrinkles)
    "fawn": ("#D79A5B", "#F2D3A8", "#E9A9A0", "#3A2A22"),
    "brindle": ("#4A3B33", "#EDE3D6", "#C98C86", "#1C1512"),
    "cream": ("#F1E6D6", "#FFFFFF", "#F2B5AE", "#2B2522"),
    "blue": ("#7D8796", "#D9DEE5", "#D9A3A3", "#2A2E35"),
}

def frenchie(coat="fawn", hat=None, s=1.0, wink=False, tongue=False):
    """Front-facing French bulldog head: wide flat face, rounded bat ears, jowls. ~800*s wide, centred on 0,0."""
    base, light, inner, dark = FRENCHIE_COATS[coat]
    mask = {"fawn": "#5C3E2C"}.get(coat)
    o = []
    for sg in (-1, 1):  # big rounded bat ears
        o.append(f'<path d="M{sg*90*s:.0f} {-210*s:.0f} C{sg*80*s:.0f} {-430*s:.0f} {sg*170*s:.0f} {-590*s:.0f} {sg*290*s:.0f} {-600*s:.0f} C{sg*420*s:.0f} {-610*s:.0f} {sg*440*s:.0f} {-420*s:.0f} {sg*380*s:.0f} {-150*s:.0f} Z" fill="{base}"/>')
        o.append(f'<path d="M{sg*150*s:.0f} {-230*s:.0f} C{sg*150*s:.0f} {-400*s:.0f} {sg*210*s:.0f} {-520*s:.0f} {sg*290*s:.0f} {-525*s:.0f} C{sg*370*s:.0f} {-530*s:.0f} {sg*375*s:.0f} {-390*s:.0f} {sg*335*s:.0f} {-200*s:.0f} Z" fill="{inner}"/>')
    o.append(f'<ellipse cx="0" cy="0" rx="{390*s:.0f}" ry="{300*s:.0f}" fill="{base}"/>')
    if coat == "cream":
        o.append(f'<ellipse cx="{150*s:.0f}" cy="{-60*s:.0f}" rx="{120*s:.0f}" ry="{110*s:.0f}" fill="#3A2F2A"/>')
    if coat == "brindle":
        o.append(f'<path d="M{-50*s:.0f} {-300*s:.0f} Q0 {-90*s:.0f} {50*s:.0f} {-300*s:.0f} Z" fill="{light}"/>')
    # muzzle: dark mask behind two jowl lobes
    if mask:
        o.append(f'<ellipse cx="0" cy="{90*s:.0f}" rx="{270*s:.0f}" ry="{170*s:.0f}" fill="{mask}"/>')
    for sg in (-1, 1):
        o.append(f'<ellipse cx="{sg*115*s:.0f}" cy="{135*s:.0f}" rx="{140*s:.0f}" ry="{110*s:.0f}" fill="{light if not mask else "#7A5440"}"/>')
    # wrinkles above the nose
    for k in (0, 1):
        o.append(f'<path d="M{-110*s:.0f} {(-100+k*38)*s:.0f} Q0 {(-150+k*38)*s:.0f} {110*s:.0f} {(-100+k*38)*s:.0f}" stroke="{dark}" stroke-width="{13*s:.0f}" fill="none" stroke-linecap="round" opacity="0.4"/>')
    for sg in (-1, 1):
        ex, ey = sg * 175 * s, -20 * s
        if wink and sg == 1:
            o.append(f'<path d="M{ex-60*s:.0f} {ey:.0f} q{60*s:.0f} {45*s:.0f} {120*s:.0f} 0" stroke="{dark}" stroke-width="{20*s:.0f}" fill="none" stroke-linecap="round"/>')
        else:
            o.append(f'<circle cx="{ex:.0f}" cy="{ey:.0f}" r="{70*s:.0f}" fill="#1A1412"/><circle cx="{ex-22*s:.0f}" cy="{ey-24*s:.0f}" r="{23*s:.0f}" fill="#FFFFFF"/><circle cx="{ex+22*s:.0f}" cy="{ey+22*s:.0f}" r="{9*s:.0f}" fill="#FFFFFF"/>')
    o.append(f'<path d="M{-95*s:.0f} {45*s:.0f} Q0 {5*s:.0f} {95*s:.0f} {45*s:.0f} Q{100*s:.0f} {100*s:.0f} 0 {115*s:.0f} Q{-100*s:.0f} {100*s:.0f} {-95*s:.0f} {45*s:.0f} Z" fill="#1A1412"/>')
    o.append(f'<ellipse cx="{-30*s:.0f}" cy="{45*s:.0f}" rx="{24*s:.0f}" ry="{11*s:.0f}" fill="#FFFFFF" opacity="0.45"/>')
    o.append(f'<path d="M0 {115*s:.0f} v{40*s:.0f}" stroke="#1A1412" stroke-width="{14*s:.0f}" stroke-linecap="round"/>')
    if tongue:
        o.append(f'<path d="M{-45*s:.0f} {200*s:.0f} Q0 {320*s:.0f} {45*s:.0f} {200*s:.0f} Z" fill="#E8687A"/>')
    o.append(f'<path d="M{-140*s:.0f} {185*s:.0f} Q{-70*s:.0f} {235*s:.0f} 0 {155*s:.0f} Q{70*s:.0f} {235*s:.0f} {140*s:.0f} {185*s:.0f}" stroke="#1A1412" stroke-width="{14*s:.0f}" fill="none" stroke-linecap="round"/>')
    if hat: o.append(HATS[hat](s))
    return "".join(o)

def _santa(s):
    return (f'<path d="M{-300*s:.0f} {-190*s:.0f} C{-260*s:.0f} {-560*s:.0f} {100*s:.0f} {-700*s:.0f} {430*s:.0f} {-500*s:.0f} C{280*s:.0f} {-430*s:.0f} {300*s:.0f} {-300*s:.0f} {300*s:.0f} {-190*s:.0f} Z" fill="#D7263D"/>'
            f'<rect x="{-340*s:.0f}" y="{-270*s:.0f}" width="{680*s:.0f}" height="{130*s:.0f}" rx="{65*s:.0f}" fill="#FFFFFF"/><circle cx="{430*s:.0f}" cy="{-500*s:.0f}" r="{80*s:.0f}" fill="#FFFFFF"/>')
def _elf(s):
    return (f'<path d="M{-290*s:.0f} {-200*s:.0f} L{120*s:.0f} {-760*s:.0f} L{290*s:.0f} {-200*s:.0f} Z" fill="#1F8A4C"/>'
            f'<path d="M{-310*s:.0f} {-200*s:.0f} l{62*s:.0f} {-70*s:.0f} l{62*s:.0f} {70*s:.0f} l{62*s:.0f} {-70*s:.0f} l{62*s:.0f} {70*s:.0f} l{62*s:.0f} {-70*s:.0f} l{62*s:.0f} {70*s:.0f} l{62*s:.0f} {-70*s:.0f} l{62*s:.0f} {70*s:.0f} l{62*s:.0f} {-70*s:.0f} l{42*s:.0f} {70*s:.0f} v{60*s:.0f} h{-620*s:.0f} Z" fill="#D7263D"/>'
            f'<circle cx="{120*s:.0f}" cy="{-770*s:.0f}" r="{55*s:.0f}" fill="#F2B134"/>')
def _antlers(s):
    o = []
    for sg in (-1, 1):
        o.append(f'<path d="M{sg*150*s:.0f} {-240*s:.0f} C{sg*170*s:.0f} {-420*s:.0f} {sg*260*s:.0f} {-560*s:.0f} {sg*380*s:.0f} {-640*s:.0f} M{sg*220*s:.0f} {-430*s:.0f} L{sg*120*s:.0f} {-560*s:.0f} M{sg*300*s:.0f} {-540*s:.0f} L{sg*260*s:.0f} {-680*s:.0f} M{sg*260*s:.0f} {-470*s:.0f} L{sg*400*s:.0f} {-480*s:.0f}" stroke="#8A5A3B" stroke-width="{48*s:.0f}" fill="none" stroke-linecap="round"/>')
    o.append(f'<ellipse cx="0" cy="{40*s:.0f}" rx="{70*s:.0f}" ry="{55*s:.0f}" fill="#E8303F"/><circle cx="{-20*s:.0f}" cy="{20*s:.0f}" r="{18*s:.0f}" fill="#FFFFFF" opacity="0.7"/>')
    return "".join(o)
def _beanie(s):
    o = [f'<path d="M{-330*s:.0f} {-170*s:.0f} C{-330*s:.0f} {-560*s:.0f} {330*s:.0f} {-560*s:.0f} {330*s:.0f} {-170*s:.0f} Z" fill="#2F6FB0"/>']
    for k in range(-4, 5):
        o.append(f'<path d="M{k*70*s:.0f} {-180*s:.0f} l0 {-250*s+abs(k)*25*s:.0f}" stroke="#1B4F86" stroke-width="{18*s:.0f}"/>')
    o.append(f'<rect x="{-350*s:.0f}" y="{-240*s:.0f}" width="{700*s:.0f}" height="{120*s:.0f}" rx="{40*s:.0f}" fill="#F4ECDD"/><circle cx="0" cy="{-480*s:.0f}" r="{90*s:.0f}" fill="#F4ECDD"/>')
    return "".join(o)
def _bow(s):
    o = []
    for sg in (-1, 1):
        o.append(f'<path d="M0 {-300*s:.0f} C{sg*80*s:.0f} {-420*s:.0f} {sg*260*s:.0f} {-430*s:.0f} {sg*250*s:.0f} {-320*s:.0f} C{sg*240*s:.0f} {-220*s:.0f} {sg*80*s:.0f} {-230*s:.0f} 0 {-300*s:.0f} Z" fill="#F28CB1"/>')
    o.append(f'<circle cx="0" cy="{-300*s:.0f}" r="{50*s:.0f}" fill="#E06C97"/>')
    return "".join(o)
HATS = {"santa": _santa, "elf": _elf, "antlers": _antlers, "beanie": _beanie, "bow": _bow}

_MAPLE = [(0, -100), (12, -62), (38, -76), (30, -38), (74, -56), (62, -24), (96, -16), (56, 10), (64, 32), (22, 26), (8, 58), (0, 50)]
def maple(s=1.0, col="#C8553D", vein="#8E3A26"):
    """Stylised maple leaf, about 200*s wide, centred on 0,0."""
    half = _MAPLE + [(-x, y) for x, y in reversed(_MAPLE[1:-1])]
    pts = " ".join(f"{x*s:.0f},{y*s:.0f}" for x, y in half)
    return (f'<polygon points="{pts}" fill="{col}" stroke="{col}" stroke-width="{6*s:.0f}" stroke-linejoin="round"/>'
            f'<path d="M0 {50*s:.0f} L0 {110*s:.0f} M0 {40*s:.0f} L0 {-70*s:.0f} M0 {0:.0f} L{50*s:.0f} {-30*s:.0f} M0 0 L{-50*s:.0f} {-30*s:.0f}" stroke="{vein}" stroke-width="{7*s:.0f}" stroke-linecap="round"/>')

def book_side(w, h, col, band="#F2E6CF", s=1.0):
    """A closed book lying flat, seen from the spine side; top-left at 0,0."""
    r = 18 * s
    return (f'<rect x="0" y="0" width="{w:.0f}" height="{h:.0f}" rx="{r:.0f}" fill="{col}"/>'
            f'<rect x="{w*0.07:.0f}" y="0" width="{14*s:.0f}" height="{h:.0f}" fill="{band}" opacity="0.8"/>'
            f'<rect x="{w*0.93-14*s:.0f}" y="0" width="{14*s:.0f}" height="{h:.0f}" fill="{band}" opacity="0.8"/>'
            f'<rect x="0" y="{h-14*s:.0f}" width="{w:.0f}" height="{14*s:.0f}" rx="{7*s:.0f}" fill="#000000" opacity="0.15"/>')
