#!/usr/bin/env python3
"""
Ground-floor architectural plan generator.

Geometry source:
  * Room dimensions  -> from the home brief (tile counts, 60x60 cm tiles).
  * Layout / adjacency -> traced from the Dreame Aqua 10 vacuum map + aerial photo.

Garden is OFF THE LIVING-ROOM TERRACE (opposite the entrance).
Output: black & white blueprint-style SVG (rendered to PNG + PDF).
NOTE: schematic working drawing - verify all measurements on site.
"""

import math

# ----------------------------------------------------------------------------
# scale & transform  (metres -> pixels)
# ----------------------------------------------------------------------------
S = 135                 # px per metre
MX, MY = 360, 360       # plan origin offset (px) - room above for garden/terrace

def X(x): return MX + x * S
def Y(y): return MY + y * S

el = []
def add(s): el.append(s)

# ----------------------------------------------------------------------------
# colours / styles
# ----------------------------------------------------------------------------
INK     = "#111111"
GRID    = "#d9d9d9"
DASH    = "#7a7a7a"
FILL_LT = "#ededed"
FILL_DK = "#2b2b2b"
GARDEN  = "#eef3ec"
HATCH   = "#cfd8cb"
FONT    = "DejaVu Sans"

EXT_W, PRT_W, ZONE_W = 9, 7, 1.6

# ----------------------------------------------------------------------------
# geometry (metres)   x -> right, y -> down
# ----------------------------------------------------------------------------
FOOT = [(0,0),(5.4,0),(5.4,1.8),(8.4,1.8),(8.4,6.0),
        (3.9,6.0),(3.9,9.0),(0,9.0)]

# name, label cx, cy, dim, tiles, area, badge, font-scale
ROOMS = [
    ("LIVING ROOM", 2.7, 1.55, "5.40 x 3.60 m", "9 x 6 tiles",   "19.4 m²", "1", 1.0),
    ("DINING",      6.9, 3.55, "3.00 x 4.20 m", "5 x 7 tiles",   "12.6 m²", "2", 1.0),
    ("ENTRANCE",    4.2, 4.75, "2.40 x 2.40 m", "4 x 4 tiles",   "5.8 m²",  "3", 1.0),
    ("KITCHEN",     2.4, 7.5,  "3.90 x 3.00 m", "6.5 x 5 tiles", "11.7 m²", "4", 1.0),
    ("GUEST WC",    0.9, 5.0,  "1.80 x 1.50 m", "guest toilet",  "~2.7 m²", "5", 0.6),
]

# ============================================================================
# 1. canvas
# ============================================================================
CW, CH = 1980, 1960
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" '
    f'viewBox="0 0 {CW} {CH}" font-family="{FONT}">')
add(f'<rect width="{CW}" height="{CH}" fill="white"/>')

# ============================================================================
# 2. garden + terrace  (off the living room, opposite the entrance)
# ============================================================================
# garden block above the living room
add(f'<rect x="{X(-0.5)}" y="{Y(-2.0)}" width="{6.3*S}" height="{1.85*S}" '
    f'fill="{GARDEN}" stroke="{HATCH}" stroke-width="1.2"/>')
# light "planting" hatch
add(f'<g stroke="{HATCH}" stroke-width="1">')
gx = -0.4
while gx < 5.7:
    add(f'<line x1="{X(gx)}" y1="{Y(-2.0)}" x2="{X(gx+0.45)}" y2="{Y(-0.18)}"/>')
    gx += 0.45
add('</g>')
# terrace / balcony slab between glazing and garden
add(f'<rect x="{X(0.3)}" y="{Y(-0.55)}" width="{4.2*S}" height="{0.5*S}" '
    f'fill="white" stroke="{INK}" stroke-width="1.6"/>')
add(f'<text x="{X(2.4)}" y="{Y(-0.24)}" font-size="17" fill="#555" '
    f'text-anchor="middle">TERRACE / balcony</text>')
add(f'<text x="{X(2.4)}" y="{Y(-1.5)}" font-size="30" fill="#6f8a6a" '
    f'font-style="italic" text-anchor="middle">GARDEN</text>')
add(f'<text x="{X(2.4)}" y="{Y(-1.16)}" font-size="15" fill="#88a083" '
    f'text-anchor="middle">(living-room view, opposite the entrance)</text>')

# ============================================================================
# 3. tile grid (60 cm), clipped to footprint
# ============================================================================
pts = " ".join(f"{X(px)},{Y(py)}" for px,py in FOOT)
add(f'<clipPath id="fp"><polygon points="{pts}"/></clipPath>')
add(f'<g clip-path="url(#fp)" stroke="{GRID}" stroke-width="1">')
x = 0.0
while x <= 8.4001:
    add(f'<line x1="{X(x)}" y1="{Y(0)}" x2="{X(x)}" y2="{Y(9.0)}"/>'); x += 0.6
y = 0.0
while y <= 9.0001:
    add(f'<line x1="{X(0)}" y1="{Y(y)}" x2="{X(8.4)}" y2="{Y(y)}"/>'); y += 0.6
add('</g>')

# ============================================================================
# 4. open-plan zone dividers (dashed - NOT walls)
# ============================================================================
def zline(x1,y1,x2,y2):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
        f'stroke="{DASH}" stroke-width="{ZONE_W}" stroke-dasharray="9 7"/>')
zline(0,3.6,5.4,3.6)      # living / lower band
zline(3.0,3.6,3.0,6.0)    # band / entrance
zline(1.8,6.0,3.9,6.0)    # band / kitchen (WC has a solid wall on its share)

# ============================================================================
# 5. fixed fixtures (under walls)
# ============================================================================
def rect(x,y,w,h,fill,stroke=INK,sw=1.4,rx=0):
    add(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{h*S}" rx="{rx}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

rect(5.18, 1.9, 0.22, 1.7, FILL_DK, INK, 1)      # black library on divider wall
rect(0.0, 0.9, 0.16, 1.3, FILL_DK, INK, 1)       # TV on left (TV wall)
rect(0.0, 8.4, 3.9, 0.6, FILL_LT)                # kitchen counter (under corner window)
rect(0.0, 6.0, 0.6, 2.4, FILL_LT)                # left-wall run (under corner window)
rect(2.3, 6.0, 1.6, 0.55, FILL_LT)               # peninsula / breakfast bar
add(f'<rect x="{X(6.1)}" y="{Y(3.05)}" width="{1.6*S}" height="{0.95*S}" '
    f'rx="10" fill="none" stroke="{INK}" stroke-width="1.4"/>')   # dining table
# guest WC fixtures
rect(1.30, 4.55, 0.36, 0.58, FILL_LT, INK, 1.2, 8)   # toilet
add(f'<line x1="{X(1.30)}" y1="{Y(4.66)}" x2="{X(1.66)}" y2="{Y(4.66)}" stroke="{INK}" stroke-width="1"/>')
rect(0.18, 5.45, 0.40, 0.34, FILL_LT, INK, 1.2, 6)   # basin

# staircase to 1st floor (indicative position) - lower living room
_sx,_sy,_sw,_sd = 0.15, 2.55, 2.7, 0.95
rect(_sx,_sy,_sw,_sd,'white',INK,1.6)
for _i in range(1,10):
    _xx = _sx + _sw*_i/10
    add(f'<line x1="{X(_xx)}" y1="{Y(_sy)}" x2="{X(_xx)}" y2="{Y(_sy+_sd)}" '
        f'stroke="{INK}" stroke-width="1"/>')
_cy = _sy + _sd/2
add(f'<line x1="{X(_sx+0.3)}" y1="{Y(_cy)}" x2="{X(_sx+_sw-0.3)}" y2="{Y(_cy)}" '
    f'stroke="{INK}" stroke-width="1.6"/>')
add(f'<polygon points="{X(_sx+_sw-0.3)},{Y(_cy)-6} {X(_sx+_sw-0.3)},{Y(_cy)+6} '
    f'{X(_sx+_sw-0.12)},{Y(_cy)}" fill="{INK}"/>')
add(f'<text x="{X(_sx+0.36)}" y="{Y(_cy)-7}" font-size="13" fill="{INK}">UP</text>')
# freestanding white column at divider / dining junction
rect(5.28, 4.28, 0.26, 0.26, 'white', INK, 2)

# ============================================================================
# 6. walls
# ============================================================================
add(f'<polygon points="{pts}" fill="none" stroke="{INK}" '
    f'stroke-width="{EXT_W}" stroke-linejoin="miter"/>')
def wall(x1,y1,x2,y2,w=PRT_W):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" '
        f'stroke="{INK}" stroke-width="{w}" stroke-linecap="butt"/>')
# divider wall with passage opening
wall(5.4,1.8,5.4,4.4); wall(5.4,5.6,5.4,6.0)
# guest WC enclosure
wall(0.0,4.5,1.8,4.5); wall(1.8,4.5,1.8,6.0); wall(0.0,6.0,1.8,6.0)

# ============================================================================
# 7. openings  (cut wall to white, then symbol)
# ============================================================================
def cut(x1,y1,x2,y2):
    if abs(x1-x2) < 1e-6:
        add(f'<rect x="{X(x1)-EXT_W}" y="{Y(min(y1,y2))}" width="{2*EXT_W}" '
            f'height="{abs(y2-y1)*S}" fill="white"/>')
    else:
        add(f'<rect x="{X(min(x1,x2))}" y="{Y(y1)-EXT_W}" width="{abs(x2-x1)*S}" '
            f'height="{2*EXT_W}" fill="white"/>')

def window(x1,y1,x2,y2):
    cut(x1,y1,x2,y2); t = 0.05
    if abs(x1-x2) < 1e-6:
        for dx in (-t,0,t):
            add(f'<line x1="{X(x1+dx)}" y1="{Y(y1)}" x2="{X(x1+dx)}" y2="{Y(y2)}" '
                f'stroke="{INK}" stroke-width="1.3"/>')
    else:
        for dy in (-t,0,t):
            add(f'<line x1="{X(x1)}" y1="{Y(y1+dy)}" x2="{X(x2)}" y2="{Y(y1+dy)}" '
                f'stroke="{INK}" stroke-width="1.3"/>')

def door_h(hx,hy,w,swing):
    cut(hx,hy,hx+w,hy)
    add(f'<line x1="{X(hx)}" y1="{Y(hy)}" x2="{X(hx)}" y2="{Y(hy-w*swing)}" '
        f'stroke="{INK}" stroke-width="1.6"/>')
    sweep = 1 if swing<0 else 0
    add(f'<path d="M {X(hx+w)} {Y(hy)} A {w*S} {w*S} 0 0 {sweep} '
        f'{X(hx)} {Y(hy-w*swing)}" fill="none" stroke="{INK}" '
        f'stroke-width="1" stroke-dasharray="3 4"/>')

def door_v(hx,hy,w,swing):
    cut(hx,hy,hx,hy+w)
    add(f'<line x1="{X(hx)}" y1="{Y(hy)}" x2="{X(hx+w*swing)}" y2="{Y(hy)}" '
        f'stroke="{INK}" stroke-width="1.6"/>')
    sweep = 0 if swing<0 else 1
    add(f'<path d="M {X(hx)} {Y(hy+w)} A {w*S} {w*S} 0 0 {sweep} '
        f'{X(hx+w*swing)} {Y(hy)}" fill="none" stroke="{INK}" '
        f'stroke-width="1" stroke-dasharray="3 4"/>')

# living room glazing -> garden/terrace facade (top wall)
window(0.6,0,3.4,0)        # large vitrine / sliding doors
window(3.8,0,4.1,0)        # narrow 1
window(4.5,0,4.8,0)        # narrow 2
# dining
window(8.4,2.6,8.4,4.8)
# kitchen corner window
window(0,7.0,0,8.4); window(0.6,9.0,2.4,9.0)
# front door (entrance, bottom exterior wall) -> into entrance
door_h(4.1,6.0,0.9,1)
# guest WC door (right wall) -> swings into WC
door_v(1.8,4.7,0.8,-1)

# ============================================================================
# 8. room labels + Dreame badge numbers
# ============================================================================
for name,cx,cy,dim,tiles,area,no,fs in ROOMS:
    add(f'<text x="{X(cx)}" y="{Y(cy)}" font-size="{30*fs:.0f}" font-weight="bold" '
        f'fill="{INK}" text-anchor="middle">{name}</text>')
    add(f'<text x="{X(cx)}" y="{Y(cy)+30*fs:.0f}" font-size="{22*fs:.0f}" fill="#333" '
        f'text-anchor="middle">{dim}</text>')
    add(f'<text x="{X(cx)}" y="{Y(cy)+56*fs:.0f}" font-size="{18*fs:.0f}" fill="#666" '
        f'text-anchor="middle">{tiles}  |  {area}</text>')
    r = 15*fs
    add(f'<circle cx="{X(cx)}" cy="{Y(cy)-58*fs:.0f}" r="{r:.0f}" fill="white" '
        f'stroke="{INK}" stroke-width="1.5"/>')
    add(f'<text x="{X(cx)}" y="{Y(cy)-58*fs+7*fs:.0f}" font-size="{18*fs:.0f}" '
        f'font-weight="bold" fill="{INK}" text-anchor="middle">{no}</text>')

# ============================================================================
# 9. feature annotations
# ============================================================================
def note(x,y,txt,anchor="middle",size=17,col="#444",rot=0):
    add(f'<text x="{X(x)}" y="{Y(y)}" font-size="{size}" fill="{col}" '
        f'font-style="italic" text-anchor="{anchor}" '
        f'transform="rotate({rot} {X(x)} {Y(y)})">{txt}</text>')

note(2.0, 0.32, "VITRINE -> terrace")
note(4.3, 0.34, "2 narrow windows", "middle", 13)
note(0.42, 1.4, "TV WALL", "middle", 15, "#444", -90)
note(1.45, 2.42, "STAIRCASE - up to 1st floor (indicative)", "middle", 12, "#444")
note(5.62, 2.7, "DIVIDER WALL - black shelving · guitar · iPad", "middle", 15, "#444", 90)
note(4.95, 4.18, "column", "end", 12, "#666")
note(8.62, 3.7, "window", "middle", 15, "#444", 90)
note(1.2, 8.78, "corner window", "middle", 14, "#555")
note(4.55, 6.34, "front door", "start", 14, "#555")
note(2.4, 8.16, "kitchen counter (cream)", "middle", 13, "#666")

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
    add(f'<text x="{(a+b)/2}" y="{ypx-7}" font-size="19" fill="{INK}" text-anchor="middle">{txt}</text>')

def dim_v(y1,y2,xpx,txt,ext_to=None):
    a,b = Y(y1),Y(y2)
    add(f'<line x1="{xpx}" y1="{a}" x2="{xpx}" y2="{b}" stroke="{INK}" stroke-width="1.2"/>')
    tick(xpx,a,math.radians(45)); tick(xpx,b,math.radians(45))
    if ext_to is not None:
        add(f'<line x1="{xpx}" y1="{a}" x2="{ext_to}" y2="{a}" stroke="#bbb" stroke-width=".8"/>')
        add(f'<line x1="{xpx}" y1="{b}" x2="{ext_to}" y2="{b}" stroke="#bbb" stroke-width=".8"/>')
    midy=(a+b)/2
    add(f'<text x="{xpx-7}" y="{midy}" font-size="19" fill="{INK}" text-anchor="middle" '
        f'transform="rotate(-90 {xpx-7} {midy})">{txt}</text>')

# left height chain
dim_v(0,3.6, X(0)-52, "3.60", ext_to=X(0))
dim_v(3.6,6.0, X(0)-52, "2.40")
dim_v(6.0,9.0, X(0)-52, "3.00")
dim_v(0,9.0, X(0)-100, "9.00  (overall)")
# right (dining height)
dim_v(1.8,6.0, X(8.4)+50, "4.20", ext_to=X(8.4))
# width chain at bottom (keeps the garden side clean)
dim_h(0,3.9, Y(9.0)+46, "3.90", ext_to=Y(9.0))
dim_h(0,5.4, Y(9.0)+92, "5.40")
dim_h(5.4,8.4, Y(9.0)+92, "3.00")
dim_h(0,8.4, Y(9.0)+138, "8.40  (overall)")

# ============================================================================
# 11. north arrow + scale bar + legend (right margin)
# ============================================================================
nx,ny = X(8.4)+170, Y(0)+30
add(f'<polygon points="{nx},{ny-34} {nx-12},{ny+14} {nx},{ny+4} {nx+12},{ny+14}" fill="{INK}"/>')
add(f'<text x="{nx}" y="{ny-44}" font-size="18" font-weight="bold" text-anchor="middle">N</text>')
add(f'<text x="{nx}" y="{ny+34}" font-size="12" fill="#777" text-anchor="middle">(assumed)</text>')

sbx, sby = X(8.4)+70, Y(6.4)
add(f'<text x="{sbx}" y="{sby-12}" font-size="15" font-weight="bold">SCALE</text>')
for i in range(3):
    add(f'<rect x="{sbx+i*S}" y="{sby}" width="{S}" height="14" '
        f'fill="{INK if i%2==0 else "white"}" stroke="{INK}" stroke-width="1"/>')
for i in range(4):
    add(f'<text x="{sbx+i*S}" y="{sby+34}" font-size="13" text-anchor="middle">{i}</text>')
add(f'<text x="{sbx+3*S+10}" y="{sby+34}" font-size="13">m</text>')
add(f'<text x="{sbx}" y="{sby+58}" font-size="13" fill="#777">1 grid sq = 60 cm tile</text>')

lx, ly = X(8.4)+70, Y(7.4)
add(f'<text x="{lx}" y="{ly-14}" font-size="15" font-weight="bold">LEGEND</text>')
legend = [("solid","exterior / divider wall"),("dash","open-plan zone (no wall)"),
          ("win","window"),("door","door")]
for i,(k,t) in enumerate(legend):
    yy = ly + i*30
    if k=="solid":
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{INK}" stroke-width="6"/>')
    elif k=="dash":
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{DASH}" stroke-width="2" stroke-dasharray="9 7"/>')
    elif k=="win":
        for dy in (-3,0,3):
            add(f'<line x1="{lx}" y1="{yy+dy}" x2="{lx+40}" y2="{yy+dy}" stroke="{INK}" stroke-width="1.2"/>')
    else:
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx}" y2="{yy-22}" stroke="{INK}" stroke-width="1.6"/>')
        add(f'<path d="M {lx+22} {yy} A 22 22 0 0 0 {lx} {yy-22}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"/>')
    add(f'<text x="{lx+52}" y="{yy+5}" font-size="14">{t}</text>')

# ============================================================================
# 12. title block
# ============================================================================
tby = Y(9.0)+225
add(f'<line x1="{X(0)-100}" y1="{tby-30}" x2="{CW-60}" y2="{tby-30}" stroke="{INK}" stroke-width="2"/>')
add(f'<text x="{X(0)-100}" y="{tby+8}" font-size="34" font-weight="bold">GROUND FLOOR PLAN</text>')
add(f'<text x="{X(0)-100}" y="{tby+40}" font-size="18" fill="#444">Rented home interior design brief &#8211; public floor</text>')
add(f'<text x="{X(0)-100}" y="{tby+70}" font-size="16" fill="#555">Geometry: room sizes from tile count (60&#215;60 cm) &#183; layout from Dreame Aqua 10 map + aerial photo</text>')
add(f'<text x="{X(0)-100}" y="{tby+94}" font-size="16" fill="#555">Total mapped area &#8776; 56.5 m&#178;  (Living 19.4 &#183; Dining 12.6 &#183; Kitchen 11.7 &#183; Entrance 5.8 &#183; Guest WC ~2.7)</text>')
add(f'<text x="{CW-60}" y="{tby+8}" font-size="16" text-anchor="end" fill="#333">Date: 18.06.2026</text>')
add(f'<text x="{CW-60}" y="{tby+34}" font-size="16" text-anchor="end" fill="#333">Scale: ~1:75 @A3</text>')
add(f'<text x="{CW-60}" y="{tby+60}" font-size="14" text-anchor="end" fill="#a33">SCHEMATIC &#8211; verify on site before any work</text>')

add('</svg>')

with open("plans/floor-plan-ground-floor.svg","w") as f:
    f.write("\n".join(el))

import cairosvg
cairosvg.svg2png(url="plans/floor-plan-ground-floor.svg",
                 write_to="plans/floor-plan-ground-floor.png",
                 output_width=CW*2, output_height=CH*2)
cairosvg.svg2pdf(url="plans/floor-plan-ground-floor.svg",
                 write_to="plans/floor-plan-ground-floor.pdf")
print("OK - wrote SVG, PNG, PDF")
