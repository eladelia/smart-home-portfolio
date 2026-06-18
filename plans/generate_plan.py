#!/usr/bin/env python3
"""
Ground-floor architectural plan generator.

Geometry source:
  * Room dimensions  -> from the home brief (tile counts, 60x60 cm tiles).
  * Layout / adjacency -> traced from the Dreame Aqua 10 vacuum map.

Output: black & white blueprint-style SVG (rendered to PNG + PDF).
NOTE: schematic working drawing - verify all measurements on site.
"""

import math

# ----------------------------------------------------------------------------
# scale & transform  (metres -> pixels)
# ----------------------------------------------------------------------------
S = 135                 # px per metre
MX, MY = 360, 250       # plan origin offset (px)

def X(x): return MX + x * S
def Y(y): return MY + y * S

el = []   # svg fragments
def add(s): el.append(s)

# ----------------------------------------------------------------------------
# colours / styles
# ----------------------------------------------------------------------------
INK      = "#111111"
GRID     = "#d9d9d9"
DASH     = "#7a7a7a"
FILL_LT  = "#ededed"   # light fixture fill
FILL_DK  = "#2b2b2b"   # dark fixture (black library / tv)
GARDEN   = "#f3f3f3"
FONT     = "DejaVu Sans"

EXT_W = 9      # exterior wall stroke
PRT_W = 7      # interior solid (partition) wall stroke
ZONE_W = 1.6   # open-plan zone divider

# ----------------------------------------------------------------------------
# geometry (metres)   x -> right, y -> down
# ----------------------------------------------------------------------------
FOOT = [(0,0),(5.4,0),(5.4,1.8),(8.4,1.8),(8.4,6.0),
        (3.9,6.0),(3.9,9.0),(0,9.0)]

# rooms: name, (cx,cy) label centre, dim text, tiles text, area text, badge no.
ROOMS = [
    ("LIVING ROOM",  2.55, 1.55, "5.40 x 3.60 m", "9 x 6 tiles",   "19.4 m²", "1"),
    ("DINING",       6.9, 3.55, "3.00 x 4.20 m", "5 x 7 tiles",   "12.6 m²", "2"),
    ("ENTRANCE",     4.2, 4.75, "2.40 x 2.40 m", "4 x 4 tiles",   "5.8 m²",  "3"),
    ("KITCHEN",      1.95, 7.5, "3.90 x 3.00 m", "6.5 x 5 tiles", "11.7 m²", "4"),
    ("LIVING 2",     0.9, 5.25, "~1.80 x 1.50 m","~3 x 2.5 tiles","~2.7 m²", "5"),
]

# ============================================================================
# 1. canvas
# ============================================================================
CW, CH = 1820, 1880
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" '
    f'viewBox="0 0 {CW} {CH}" font-family="{FONT}">')
add(f'<rect width="{CW}" height="{CH}" fill="white"/>')

# ============================================================================
# 2. garden (outside footprint, light) + label
# ============================================================================
# left strip (vitrine side) + bottom-right wrap
add(f'<rect x="{X(-1.4)}" y="{Y(-0.2)}" width="{1.4*S}" height="{3.6*S}" '
    f'fill="{GARDEN}"/>')
add(f'<rect x="{X(3.9)}" y="{Y(6.0)}" width="{4.5*S}" height="{3.0*S}" '
    f'fill="{GARDEN}"/>')
for (gx,gy,rot) in [(-0.75,1.8,0),(6.4,7.6,0)]:
    add(f'<text x="{X(gx)}" y="{Y(gy)}" font-size="26" fill="#8a8a8a" '
        f'font-style="italic" text-anchor="middle" transform="rotate({rot} {X(gx)} {Y(gy)})">GARDEN</text>')

# ============================================================================
# 3. tile grid (60 cm), clipped to footprint
# ============================================================================
pts = " ".join(f"{X(px)},{Y(py)}" for px,py in FOOT)
add(f'<clipPath id="fp"><polygon points="{pts}"/></clipPath>')
add(f'<g clip-path="url(#fp)" stroke="{GRID}" stroke-width="1">')
x = 0.0
while x <= 8.4001:
    add(f'<line x1="{X(x)}" y1="{Y(0)}" x2="{X(x)}" y2="{Y(9.0)}"/>')
    x += 0.6
y = 0.0
while y <= 9.0001:
    add(f'<line x1="{X(0)}" y1="{Y(y)}" x2="{X(8.4)}" y2="{Y(y)}"/>')
    y += 0.6
add('</g>')

# ============================================================================
# 4. open-plan zone dividers (dashed - NOT walls)
# ============================================================================
def zline(x1,y1,x2,y2):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
        f'stroke="{DASH}" stroke-width="{ZONE_W}" stroke-dasharray="9 7"/>')
zline(0,3.6,5.4,3.6)      # living  / lower band
zline(3.0,3.6,3.0,6.0)    # band    / entrance
zline(0,6.0,3.9,6.0)      # band    / kitchen
zline(0,4.5,1.8,4.5)      # living-2 niche top
zline(1.8,4.5,1.8,6.0)    # living-2 niche side

# ============================================================================
# 5. fixed fixtures (drawn under walls)
# ============================================================================
def rect(x,y,w,h,fill,stroke=INK,sw=1.4):
    add(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{h*S}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

# black library on the PARTITION wall (living side)
rect(5.18, 1.9, 0.22, 1.7, FILL_DK, INK, 1)
# TV on tv-wall (top of living room)
rect(2.0, 0.0, 1.6, 0.16, FILL_DK, INK, 1)
# kitchen counter (cream) - L along bottom + right wall, under corner window
rect(0.0, 8.4, 3.9, 0.6, FILL_LT)
rect(3.3, 6.0, 0.6, 2.4, FILL_LT)
# dining table
add(f'<rect x="{X(6.1)}" y="{Y(3.05)}" width="{1.6*S}" height="{0.95*S}" '
    f'rx="10" fill="none" stroke="{INK}" stroke-width="1.4"/>')

# ============================================================================
# 6. walls
# ============================================================================
# exterior footprint
add(f'<polygon points="{pts}" fill="none" stroke="{INK}" '
    f'stroke-width="{EXT_W}" stroke-linejoin="miter"/>')
# interior solid partition wall (the "divider wall") with a passage opening
def wall(x1,y1,x2,y2):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
        f'stroke="{INK}" stroke-width="{PRT_W}" stroke-linecap="butt"/>')
wall(5.4,1.8,5.4,4.4)
wall(5.4,5.6,5.4,6.0)

# ============================================================================
# 7. openings  (cut wall to white, then draw symbol)
# ============================================================================
def cut(x1,y1,x2,y2,pad=0.06):
    """white-out the wall along an opening (axis aligned)."""
    if abs(x1-x2) < 1e-6:                # vertical wall
        add(f'<rect x="{X(x1)-EXT_W}" y="{Y(min(y1,y2))}" '
            f'width="{2*EXT_W}" height="{abs(y2-y1)*S}" fill="white"/>')
    else:                               # horizontal wall
        add(f'<rect x="{X(min(x1,x2))}" y="{Y(y1)-EXT_W}" '
            f'width="{abs(x2-x1)*S}" height="{2*EXT_W}" fill="white"/>')

def window(x1,y1,x2,y2):
    cut(x1,y1,x2,y2)
    t = 0.05                            # half-thickness of glazing symbol (m)
    if abs(x1-x2) < 1e-6:              # vertical
        for dx in (-t,0,t):
            add(f'<line x1="{X(x1+dx)}" y1="{Y(y1)}" x2="{X(x1+dx)}" '
                f'y2="{Y(y2)}" stroke="{INK}" stroke-width="1.3"/>')
    else:
        for dy in (-t,0,t):
            add(f'<line x1="{X(x1)}" y1="{Y(y1+dy)}" x2="{X(x2)}" '
                f'y2="{Y(y1+dy)}" stroke="{INK}" stroke-width="1.3"/>')

def door(hx,hy,w,facing,swing):
    """single-leaf door. hx,hy = hinge. facing: 'h'/'v' wall. swing dir +/-1."""
    if facing == 'h':                  # door in horizontal wall
        cut(hx,hy,hx+ (w if swing>0 else -w),hy)
        ex,ey = hx + w, hy             # leaf end (open ~90deg)
        lx,ly = hx, hy - w             # open leaf tip (swing up = -y) ... generic
        # leaf line vertical
        add(f'<line x1="{X(hx)}" y1="{Y(hy)}" x2="{X(hx)}" y2="{Y(hy-w*swing)}" '
            f'stroke="{INK}" stroke-width="1.6"/>')
        add(f'<path d="M {X(hx+w)} {Y(hy)} A {w*S} {w*S} 0 0 {1 if swing<0 else 0} '
            f'{X(hx)} {Y(hy-w*swing)}" fill="none" stroke="{INK}" '
            f'stroke-width="1" stroke-dasharray="3 4"/>')

# --- windows ---
window(0,0.4,0,2.0)        # living vitrine (large, garden)
window(0,2.4,0,2.7)        # narrow 1
window(0,2.95,0,3.25)      # narrow 2
window(8.4,2.6,8.4,4.8)    # dining large window
window(0,7.0,0,8.4)        # kitchen corner window (on left wall)
window(0.6,9.0,2.4,9.0)    # kitchen corner window (on bottom wall)
# --- front door (entrance, bottom exterior wall) swinging up into entrance ---
door(4.1,6.0,0.9,'h',1)

# ============================================================================
# 8. room labels + Dreame badge numbers
# ============================================================================
for name,cx,cy,dim,tiles,area,no in ROOMS:
    add(f'<text x="{X(cx)}" y="{Y(cy)}" font-size="30" font-weight="bold" '
        f'fill="{INK}" text-anchor="middle">{name}</text>')
    add(f'<text x="{X(cx)}" y="{Y(cy)+30}" font-size="22" fill="#333" '
        f'text-anchor="middle">{dim}</text>')
    add(f'<text x="{X(cx)}" y="{Y(cy)+56}" font-size="18" fill="#666" '
        f'text-anchor="middle">{tiles}  |  {area}</text>')
    # badge
    add(f'<circle cx="{X(cx)+0}" cy="{Y(cy)-58}" r="15" fill="white" '
        f'stroke="{INK}" stroke-width="1.5"/>')
    add(f'<text x="{X(cx)}" y="{Y(cy)-51}" font-size="18" font-weight="bold" '
        f'fill="{INK}" text-anchor="middle">{no}</text>')

# ============================================================================
# 9. feature annotations (leader text)
# ============================================================================
def note(x,y,txt,anchor="middle",size=17,col="#444",rot=0):
    add(f'<text x="{X(x)}" y="{Y(y)}" font-size="{size}" fill="{col}" '
        f'font-style="italic" text-anchor="{anchor}" '
        f'transform="rotate({rot} {X(x)} {Y(y)})">{txt}</text>')

note(2.8, -0.18, "TV WALL")
note(-0.28, 1.2, "VITRINE (large glazing)", "middle", 15, "#444", -90)
note(-0.28, 2.85, "2 narrow windows", "middle", 13, "#444", -90)
note(5.62, 2.7, "DIVIDER WALL - black shelving / iPad", "middle", 15, "#444", 90)
note(8.62, 3.7, "window", "middle", 15, "#444", 90)
note(1.2, 8.78, "corner window", "middle", 14, "#555")
note(4.55, 6.34, "front door", "start", 14, "#555")
note(1.95, 8.16, "kitchen counter (cream)", "middle", 13, "#666")

# ============================================================================
# 10. dimension lines
# ============================================================================
def tick(px,py,ang):
    dx,dy = 7*math.cos(ang),7*math.sin(ang)
    add(f'<line x1="{px-dx}" y1="{py-dy}" x2="{px+dx}" y2="{py+dy}" '
        f'stroke="{INK}" stroke-width="1.4"/>')

def dim_h(x1,x2,ypx,txt,ext_to=None):
    a,b = X(x1),X(x2)
    add(f'<line x1="{a}" y1="{ypx}" x2="{b}" y2="{ypx}" stroke="{INK}" stroke-width="1.2"/>')
    tick(a,ypx,math.radians(45)); tick(b,ypx,math.radians(45))
    if ext_to is not None:
        add(f'<line x1="{a}" y1="{ypx}" x2="{a}" y2="{ext_to}" stroke="#bbb" stroke-width=".8"/>')
        add(f'<line x1="{b}" y1="{ypx}" x2="{b}" y2="{ext_to}" stroke="#bbb" stroke-width=".8"/>')
    add(f'<text x="{(a+b)/2}" y="{ypx-7}" font-size="19" fill="{INK}" '
        f'text-anchor="middle">{txt}</text>')

def dim_v(y1,y2,xpx,txt,ext_to=None):
    a,b = Y(y1),Y(y2)
    add(f'<line x1="{xpx}" y1="{a}" x2="{xpx}" y2="{b}" stroke="{INK}" stroke-width="1.2"/>')
    tick(xpx,a,math.radians(45)); tick(xpx,b,math.radians(45))
    if ext_to is not None:
        add(f'<line x1="{xpx}" y1="{a}" x2="{ext_to}" y2="{a}" stroke="#bbb" stroke-width=".8"/>')
        add(f'<line x1="{xpx}" y1="{b}" x2="{ext_to}" y2="{b}" stroke="#bbb" stroke-width=".8"/>')
    midy = (a+b)/2
    add(f'<text x="{xpx-7}" y="{midy}" font-size="19" fill="{INK}" '
        f'text-anchor="middle" transform="rotate(-90 {xpx-7} {midy})">{txt}</text>')

# top chain
dim_h(0,5.4, Y(0)-46, "5.40", ext_to=Y(0))
dim_h(5.4,8.4, Y(0)-46, "3.00")
dim_h(0,8.4, Y(0)-92, "8.40  (overall)")
# left chain
dim_v(0,3.6, X(0)-52, "3.60", ext_to=X(0))
dim_v(3.6,6.0, X(0)-52, "2.40")
dim_v(6.0,9.0, X(0)-52, "3.00")
dim_v(0,9.0, X(0)-100, "9.00  (overall)")
# right (dining height)
dim_v(1.8,6.0, X(8.4)+50, "4.20", ext_to=X(8.4))
# bottom (kitchen width)
dim_h(0,3.9, Y(9.0)+46, "3.90", ext_to=Y(9.0))

# ============================================================================
# 11. north arrow + scale bar (right margin)
# ============================================================================
nx,ny = X(8.4)+150, Y(0)+40
add(f'<polygon points="{nx},{ny-34} {nx-12},{ny+14} {nx},{ny+4} {nx+12},{ny+14}" '
    f'fill="{INK}"/>')
add(f'<text x="{nx}" y="{ny-44}" font-size="18" font-weight="bold" '
    f'text-anchor="middle">N</text>')
add(f'<text x="{nx}" y="{ny+34}" font-size="12" fill="#777" '
    f'text-anchor="middle">(assumed)</text>')

# scale bar (0-3 m)
sbx, sby = X(8.4)+70, Y(6.6)
add(f'<text x="{sbx}" y="{sby-12}" font-size="15" font-weight="bold">SCALE</text>')
for i in range(3):
    fillc = INK if i%2==0 else "white"
    add(f'<rect x="{sbx+i*S}" y="{sby}" width="{S}" height="14" '
        f'fill="{fillc}" stroke="{INK}" stroke-width="1"/>')
for i in range(4):
    add(f'<text x="{sbx+i*S}" y="{sby+34}" font-size="13" '
        f'text-anchor="middle">{i}</text>')
add(f'<text x="{sbx+3*S+10}" y="{sby+34}" font-size="13">m</text>')
add(f'<text x="{sbx}" y="{sby+58}" font-size="13" fill="#777">1 sq = 60 cm tile</text>')

# legend (right margin)
lx, ly = X(8.4)+70, Y(7.6)
legend = [
    ("solid", "exterior / divider wall"),
    ("dash",  "open-plan zone (no wall)"),
    ("win",   "window"),
    ("door",  "door"),
]
add(f'<text x="{lx}" y="{ly-14}" font-size="15" font-weight="bold">LEGEND</text>')
for i,(k,t) in enumerate(legend):
    yy = ly + i*30
    if k=="solid":
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{INK}" stroke-width="6"/>')
    elif k=="dash":
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{DASH}" stroke-width="2" stroke-dasharray="9 7"/>')
    elif k=="win":
        for dy in (-3,0,3):
            add(f'<line x1="{lx}" y1="{yy+dy}" x2="{lx+40}" y2="{yy+dy}" stroke="{INK}" stroke-width="1.2"/>')
    elif k=="door":
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx}" y2="{yy-22}" stroke="{INK}" stroke-width="1.6"/>')
        add(f'<path d="M {lx+22} {yy} A 22 22 0 0 0 {lx} {yy-22}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"/>')
    add(f'<text x="{lx+52}" y="{yy+5}" font-size="14">{t}</text>')

# ============================================================================
# 12. title block (bottom)
# ============================================================================
tby = Y(9.0)+120
add(f'<line x1="{X(0)-100}" y1="{tby-30}" x2="{CW-60}" y2="{tby-30}" '
    f'stroke="{INK}" stroke-width="2"/>')
add(f'<text x="{X(0)-100}" y="{tby+8}" font-size="34" font-weight="bold">'
    f'GROUND FLOOR PLAN</text>')
add(f'<text x="{X(0)-100}" y="{tby+40}" font-size="18" fill="#444">'
    f'Rented home interior design brief &#8211; public floor</text>')
add(f'<text x="{X(0)-100}" y="{tby+70}" font-size="16" fill="#555">'
    f'Geometry: room sizes from tile count (60&#215;60 cm) &#183; layout traced from Dreame Aqua 10 map</text>')
add(f'<text x="{X(0)-100}" y="{tby+94}" font-size="16" fill="#555">'
    f'Total mapped area &#8776; 56.5 m&#178;   (Living 19.4 &#183; Dining 12.6 &#183; Kitchen 11.7 &#183; Entrance 5.8 &#183; Living-2 ~2.7)</text>')
add(f'<text x="{CW-60}" y="{tby+8}" font-size="16" text-anchor="end" fill="#333">'
    f'Date: 18.06.2026</text>')
add(f'<text x="{CW-60}" y="{tby+34}" font-size="16" text-anchor="end" fill="#333">'
    f'Scale: ~1:75 @A3</text>')
add(f'<text x="{CW-60}" y="{tby+60}" font-size="14" text-anchor="end" fill="#a33">'
    f'SCHEMATIC &#8211; verify on site before any work</text>')

add('</svg>')

svg = "\n".join(el)
with open("plans/floor-plan-ground-floor.svg","w") as f:
    f.write(svg)

import cairosvg
cairosvg.svg2png(url="plans/floor-plan-ground-floor.svg",
                 write_to="plans/floor-plan-ground-floor.png",
                 output_width=CW*2, output_height=CH*2)   # 2x for crisp print
cairosvg.svg2pdf(url="plans/floor-plan-ground-floor.svg",
                 write_to="plans/floor-plan-ground-floor.pdf")
print("OK - wrote SVG, PNG, PDF")
