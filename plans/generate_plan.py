#!/usr/bin/env python3
"""
Ground-floor architectural plan generator (v3 - rebuilt from all photos).

Layout understood from: Dreame Aqua 10 map, aerial, and interior photos.
  - Divider wall runs N-S, separating DINING (east) from the rest (west).
  - Central SWITCHBACK staircase (2 flights x 9 steps) + under-stair storage,
    kitchen to its west, guest WC adjacent.
  - Front door on the SOUTH; GARDEN is a 'resh' (north + east), opposite entrance.
  - Living room (north): TV on west wall, sofa facing it, terrace doors north.

Sizes from tile count (60x60 cm).  SCHEMATIC - verify on site.
"""

import math

S = 135
MX, MY = 360, 360
def X(x): return MX + x*S
def Y(y): return MY + y*S
el=[]
def add(s): el.append(s)

INK="#111111"; GRID="#dddddd"; DASH="#8a8a8a"
GARDEN="#eef3ec"; HATCH="#cfd8cb"; FONT="DejaVu Sans"; FUR="#f1f1f1"
EXT_W, PRT_W, ZONE_W = 9, 7, 1.5

# footprint: west block x[0,5.4] y[0,9.0] + dining bump x[5.4,8.4] y[1.8,6.0]
FOOT=[(0,0),(5.4,0),(5.4,1.8),(8.4,1.8),(8.4,6.0),(5.4,6.0),(5.4,9.0),(0,9.0)]

# name, cx, cy, dim, tiles, area, badge, font-scale
ROOMS=[
    ("LIVING ROOM", 3.9, 1.15, "5.40 x 3.60 m", "9 x 6 tiles",  "19.4 m²","1",1.0),
    ("DINING",      6.9, 2.55, "3.00 x 4.20 m", "5 x 7 tiles",  "12.6 m²","2",1.0),
    ("KITCHEN",     1.95,7.45, "3.90 x 3.00 m", "6.5 x 5 tiles","11.7 m²","4",1.0),
    ("ENTRANCE",    4.65,8.2,  "approx.",       "",             "",       "3",0.6),
    ("GUEST WC",    0.9, 5.05, "1.80 x 1.50 m", "",             "~2.7 m²","5",0.6),
]

CW,CH=1800,1960
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" font-family="{FONT}">')
add(f'<rect width="{CW}" height="{CH}" fill="white"/>')

# ---- garden (resh shape: north bar + east leg) ----
gpts=[(-0.5,-2.0),(9.7,-2.0),(9.7,6.0),(8.4,6.0),(8.4,1.8),(5.4,1.8),(5.4,0),(-0.5,0)]
gp=" ".join(f"{X(a)},{Y(b)}" for a,b in gpts)
add(f'<polygon points="{gp}" fill="{GARDEN}" stroke="{HATCH}" stroke-width="1.2"/>')
add(f'<g stroke="{HATCH}" stroke-width="1">')
gx=-0.4
while gx<9.5:
    add(f'<line x1="{X(gx)}" y1="{Y(-2.0)}" x2="{X(gx+0.4)}" y2="{Y(-0.2)}"/>'); gx+=0.5
gy=0.3
while gy<5.7:
    add(f'<line x1="{X(8.5)}" y1="{Y(gy)}" x2="{X(9.6)}" y2="{Y(gy+0.4)}"/>'); gy+=0.5
add('</g>')
add(f'<rect x="{X(0.3)}" y="{Y(-0.6)}" width="{3.3*S}" height="{0.5*S}" fill="white" stroke="{INK}" stroke-width="1.6"/>')
add(f'<text x="{X(1.95)}" y="{Y(-0.28)}" font-size="16" fill="#555" text-anchor="middle">TERRACE / balcony</text>')
add(f'<text x="{X(3.2)}" y="{Y(-1.15)}" font-size="32" fill="#6f8a6a" font-style="italic" text-anchor="middle">GARDEN</text>')

# ---- tile grid ----
pts=" ".join(f"{X(a)},{Y(b)}" for a,b in FOOT)
add(f'<clipPath id="fp"><polygon points="{pts}"/></clipPath>')
add(f'<g clip-path="url(#fp)" stroke="{GRID}" stroke-width="1">')
x=0.0
while x<=8.4001:
    add(f'<line x1="{X(x)}" y1="{Y(0)}" x2="{X(x)}" y2="{Y(9.0)}"/>'); x+=0.6
y=0.0
while y<=9.0001:
    add(f'<line x1="{X(0)}" y1="{Y(y)}" x2="{X(8.4)}" y2="{Y(y)}"/>'); y+=0.6
add('</g>')

# ---- open-plan zone lines (dashed, not walls) ----
def zline(x1,y1,x2,y2):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="{DASH}" stroke-width="{ZONE_W}" stroke-dasharray="9 7"/>')
zline(0,3.6,5.4,3.6)     # living / central band
zline(5.4,3.6,5.4,6.0)   # entrance-stairs / dining (OPEN)
zline(0,6.0,3.9,6.0)     # central / kitchen
zline(3.9,6.0,3.9,9.0)   # kitchen / entrance vestibule

# ---- furniture (line only) ----
def rect(x,y,w,h,fill="none",stroke=INK,sw=1.4,rx=0):
    add(f'<rect x="{X(x)}" y="{Y(y)}" width="{w*S}" height="{h*S}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')

rect(0.0,1.1,0.14,1.2,"#2b2b2b",INK,1)                 # TV (west wall)
rect(2.15,0.9,0.8,1.8,"none",INK,1.6,10)               # sofa facing TV (west)
add(f'<line x1="{X(2.78)}" y1="{Y(1.0)}" x2="{X(2.78)}" y2="{Y(2.6)}" stroke="{INK}" stroke-width="1.4"/>')
add(f'<circle cx="{X(6.9)}" cy="{Y(4.1)}" r="{0.55*S}" fill="none" stroke="{INK}" stroke-width="1.5"/>')   # dining table
for cxx,cyy in [(6.9,3.15),(6.9,5.05),(6.0,4.1),(7.8,4.1)]:
    add(f'<circle cx="{X(cxx)}" cy="{Y(cyy)}" r="{0.24*S}" fill="none" stroke="{INK}" stroke-width="1.3"/>')
# kitchen U (west, south, east walls; open to north)
rect(0.0,8.4,3.9,0.6,FUR)        # south run
rect(0.0,6.0,0.6,2.4,FUR)        # west run (under corner window)
rect(3.3,6.0,0.6,2.4,FUR)        # east run (oven / fridge)
# guest WC fixtures
rect(1.30,4.58,0.36,0.56,FUR,INK,1.2,8)
add(f'<line x1="{X(1.30)}" y1="{Y(4.69)}" x2="{X(1.66)}" y2="{Y(4.69)}" stroke="{INK}" stroke-width="1"/>')
rect(0.16,5.45,0.40,0.34,FUR,INK,1.2,6)
# entry console table by front door
rect(4.55,8.55,0.7,0.28,FUR)

# ---- staircase: central switchback 2 x 9 + under-stair storage ----
ax1,ay1,ax2,ay2 = 3.0,3.6,5.4,6.0
rect(ax1,ay1,ax2-ax1,ay2-ay1,"white",INK,1.6)
spine=4.2
add(f'<line x1="{X(spine)}" y1="{Y(3.95)}" x2="{X(spine)}" y2="{Y(6.0)}" stroke="{INK}" stroke-width="3"/>')   # switchback wall
# lower (east) flight, 9 treads, going up to the north
for i in range(0,10):
    yy=6.0 - i*(6.0-4.2)/9
    add(f'<line x1="{X(spine)}" y1="{Y(yy)}" x2="{X(5.4)}" y2="{Y(yy)}" stroke="{INK}" stroke-width="1"/>')
# upper (west) flight, 9 treads (drawn with break line)
for i in range(0,10):
    yy=4.2 + i*(6.0-4.2)/9
    add(f'<line x1="{X(ax1)}" y1="{Y(yy)}" x2="{X(spine)}" y2="{Y(yy)}" stroke="{INK}" stroke-width="1"/>')
# top landing
add(f'<line x1="{X(ax1)}" y1="{Y(4.2)}" x2="{X(5.4)}" y2="{Y(4.2)}" stroke="{INK}" stroke-width="1.4"/>')
# break line across upper flight
add(f'<line x1="{X(3.05)}" y1="{Y(5.25)}" x2="{X(4.15)}" y2="{Y(4.95)}" stroke="{INK}" stroke-width="1.2"/>')
# up arrow (lower flight, north)
arx=(spine+5.4)/2
add(f'<line x1="{X(arx)}" y1="{Y(5.85)}" x2="{X(arx)}" y2="{Y(4.45)}" stroke="{INK}" stroke-width="1.6"/>')
add(f'<polygon points="{X(arx)-6},{Y(4.48)} {X(arx)+6},{Y(4.48)} {X(arx)},{Y(4.32)}" fill="{INK}"/>')
add(f'<text x="{X(arx)}" y="{Y(6.0)-7}" font-size="12" fill="#333" text-anchor="middle">UP</text>')
# under-stair storage (dashed) at low end of upper flight
add(f'<rect x="{X(3.0)}" y="{Y(5.4)}" width="{1.2*S}" height="{0.6*S}" fill="none" stroke="{DASH}" stroke-width="1.3" stroke-dasharray="5 4"/>')
add(f'<text x="{X(3.6)}" y="{Y(5.74)}" font-size="11" fill="#666" text-anchor="middle">storage</text>')
add(f'<text x="{X(4.2)}" y="{Y(3.45)}" font-size="13" fill="#333" text-anchor="middle">STAIRCASE - 2 flights x 9 steps</text>')

# ---- walls ----
add(f'<polygon points="{pts}" fill="none" stroke="{INK}" stroke-width="{EXT_W}" stroke-linejoin="miter"/>')
def wall(x1,y1,x2,y2,w=PRT_W):
    add(f'<line x1="{X(x1)}" y1="{Y(y1)}" x2="{X(x2)}" y2="{Y(y2)}" stroke="{INK}" stroke-width="{w}" stroke-linecap="butt"/>')
wall(5.4,1.8,5.4,3.6)                 # divider wall (living | dining) only
rect(5.28,3.46,0.26,0.26,"white",INK,2.2)   # freestanding column at its end
wall(0.0,4.5,1.8,4.5); wall(1.8,4.5,1.8,6.0); wall(0.0,6.0,1.8,6.0)   # WC enclosure

# ---- openings ----
def cut(x1,y1,x2,y2):
    if abs(x1-x2)<1e-6:
        add(f'<rect x="{X(x1)-EXT_W}" y="{Y(min(y1,y2))}" width="{2*EXT_W}" height="{abs(y2-y1)*S}" fill="white"/>')
    else:
        add(f'<rect x="{X(min(x1,x2))}" y="{Y(y1)-EXT_W}" width="{abs(x2-x1)*S}" height="{2*EXT_W}" fill="white"/>')
def window(x1,y1,x2,y2):
    cut(x1,y1,x2,y2); t=0.05
    if abs(x1-x2)<1e-6:
        for dx in (-t,0,t):
            add(f'<line x1="{X(x1+dx)}" y1="{Y(y1)}" x2="{X(x1+dx)}" y2="{Y(y2)}" stroke="{INK}" stroke-width="1.3"/>')
    else:
        for dy in (-t,0,t):
            add(f'<line x1="{X(x1)}" y1="{Y(y1+dy)}" x2="{X(x2)}" y2="{Y(y1+dy)}" stroke="{INK}" stroke-width="1.3"/>')
def door_h(hx,hy,w,swing):
    cut(hx,hy,hx+w,hy)
    add(f'<line x1="{X(hx)}" y1="{Y(hy)}" x2="{X(hx)}" y2="{Y(hy-w*swing)}" stroke="{INK}" stroke-width="1.6"/>')
    add(f'<path d="M {X(hx+w)} {Y(hy)} A {w*S} {w*S} 0 0 {1 if swing<0 else 0} {X(hx)} {Y(hy-w*swing)}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"/>')
def door_v(hx,hy,w,swing):
    cut(hx,hy,hx,hy+w)
    add(f'<line x1="{X(hx)}" y1="{Y(hy)}" x2="{X(hx+w*swing)}" y2="{Y(hy)}" stroke="{INK}" stroke-width="1.6"/>')
    add(f'<path d="M {X(hx)} {Y(hy+w)} A {w*S} {w*S} 0 0 {0 if swing<0 else 1} {X(hx+w*swing)} {Y(hy)}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"/>')

window(0.5,0,3.0,0)        # terrace vitrine (north)
window(3.4,0,3.7,0); window(4.1,0,4.4,0)   # 2 narrow windows
window(8.4,2.6,8.4,5.0)    # dining window (east garden)
window(0,7.4,0,8.6); window(0.6,9.0,2.2,9.0)   # kitchen corner window (SW)
door_h(4.0,9.0,1.0,1)      # dark front door (south)
door_v(1.8,4.65,0.8,-1)    # guest WC door

# ---- room names ----
for name,cx,cy,dim,tiles,area,no,fs in ROOMS:
    add(f'<text x="{X(cx)}" y="{Y(cy)}" font-size="{30*fs:.0f}" font-weight="bold" fill="{INK}" text-anchor="middle">{name}</text>')
    if dim:
        add(f'<text x="{X(cx)}" y="{Y(cy)+30*fs:.0f}" font-size="{22*fs:.0f}" fill="#333" text-anchor="middle">{dim}</text>')
    extra=" | ".join([t for t in (tiles,area) if t])
    if extra:
        add(f'<text x="{X(cx)}" y="{Y(cy)+56*fs:.0f}" font-size="{18*fs:.0f}" fill="#666" text-anchor="middle">{extra}</text>')
    r=15*fs
    add(f'<circle cx="{X(cx)}" cy="{Y(cy)-58*fs:.0f}" r="{r:.0f}" fill="white" stroke="{INK}" stroke-width="1.5"/>')
    add(f'<text x="{X(cx)}" y="{Y(cy)-58*fs+7*fs:.0f}" font-size="{18*fs:.0f}" font-weight="bold" fill="{INK}" text-anchor="middle">{no}</text>')

# ---- dimensions ----
def tick(px,py):
    d=7; add(f'<line x1="{px-d}" y1="{py-d}" x2="{px+d}" y2="{py+d}" stroke="{INK}" stroke-width="1.4"/>')
def dim_h(x1,x2,ypx,txt,ext=None):
    a,b=X(x1),X(x2)
    add(f'<line x1="{a}" y1="{ypx}" x2="{b}" y2="{ypx}" stroke="{INK}" stroke-width="1.2"/>'); tick(a,ypx); tick(b,ypx)
    if ext is not None:
        add(f'<line x1="{a}" y1="{ypx}" x2="{a}" y2="{ext}" stroke="#bbb" stroke-width=".8"/>')
        add(f'<line x1="{b}" y1="{ypx}" x2="{b}" y2="{ext}" stroke="#bbb" stroke-width=".8"/>')
    add(f'<text x="{(a+b)/2}" y="{ypx-7}" font-size="19" fill="{INK}" text-anchor="middle">{txt}</text>')
def dim_v(y1,y2,xpx,txt,ext=None):
    a,b=Y(y1),Y(y2)
    add(f'<line x1="{xpx}" y1="{a}" x2="{xpx}" y2="{b}" stroke="{INK}" stroke-width="1.2"/>'); tick(xpx,a); tick(xpx,b)
    if ext is not None:
        add(f'<line x1="{xpx}" y1="{a}" x2="{ext}" y2="{a}" stroke="#bbb" stroke-width=".8"/>')
        add(f'<line x1="{xpx}" y1="{b}" x2="{ext}" y2="{b}" stroke="#bbb" stroke-width=".8"/>')
    my=(a+b)/2
    add(f'<text x="{xpx-7}" y="{my}" font-size="19" fill="{INK}" text-anchor="middle" transform="rotate(-90 {xpx-7} {my})">{txt}</text>')

dim_v(0,3.6,X(0)-52,"3.60",ext=X(0))
dim_v(3.6,6.0,X(0)-52,"2.40")
dim_v(6.0,9.0,X(0)-52,"3.00")
dim_v(0,9.0,X(0)-100,"9.00  (overall)")
dim_v(1.8,6.0,X(9.7)+45,"4.20",ext=X(8.4))
dim_h(5.4,8.4,Y(6.0)+40,"3.00",ext=Y(6.0))     # dining width
dim_h(0,3.9,Y(9.0)+46,"3.90",ext=Y(9.0))
dim_h(0,5.4,Y(9.0)+92,"5.40")
dim_h(0,8.4,Y(9.0)+138,"8.40  (overall)")

# ---- north / scale / legend (bottom-right free zone) ----
nx,ny=X(8.9),Y(6.7)
add(f'<polygon points="{nx},{ny-30} {nx-11},{ny+12} {nx},{ny+3} {nx+11},{ny+12}" fill="{INK}"/>')
add(f'<text x="{nx}" y="{ny-38}" font-size="17" font-weight="bold" text-anchor="middle">N</text>')
add(f'<text x="{nx}" y="{ny+30}" font-size="11" fill="#777" text-anchor="middle">(assumed)</text>')
sbx,sby=X(5.9),Y(7.5)
add(f'<text x="{sbx}" y="{sby-12}" font-size="15" font-weight="bold">SCALE</text>')
for i in range(3):
    add(f'<rect x="{sbx+i*S}" y="{sby}" width="{S}" height="14" fill="{INK if i%2==0 else "white"}" stroke="{INK}" stroke-width="1"/>')
for i in range(4):
    add(f'<text x="{sbx+i*S}" y="{sby+33}" font-size="13" text-anchor="middle">{i}</text>')
add(f'<text x="{sbx+3*S+10}" y="{sby+33}" font-size="13">m</text>')
add(f'<text x="{sbx}" y="{sby+56}" font-size="13" fill="#777">1 grid square = 60 cm tile</text>')
lx,ly=X(5.9),Y(8.15)
add(f'<text x="{lx}" y="{ly-12}" font-size="15" font-weight="bold">LEGEND</text>')
for i,(k,t) in enumerate([("solid","exterior / divider wall"),("dash","open-plan zone (no wall)"),("win","window"),("door","door")]):
    yy=ly+i*28
    if k=="solid": add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{INK}" stroke-width="6"/>')
    elif k=="dash": add(f'<line x1="{lx}" y1="{yy}" x2="{lx+40}" y2="{yy}" stroke="{DASH}" stroke-width="2" stroke-dasharray="9 7"/>')
    elif k=="win":
        for dy in (-3,0,3): add(f'<line x1="{lx}" y1="{yy+dy}" x2="{lx+40}" y2="{yy+dy}" stroke="{INK}" stroke-width="1.2"/>')
    else:
        add(f'<line x1="{lx}" y1="{yy}" x2="{lx}" y2="{yy-22}" stroke="{INK}" stroke-width="1.6"/>')
        add(f'<path d="M {lx+22} {yy} A 22 22 0 0 0 {lx} {yy-22}" fill="none" stroke="{INK}" stroke-width="1" stroke-dasharray="3 4"/>')
    add(f'<text x="{lx+52}" y="{yy+5}" font-size="14">{t}</text>')

# ---- title block ----
tby=Y(9.0)+215
add(f'<line x1="{X(0)-100}" y1="{tby-30}" x2="{CW-50}" y2="{tby-30}" stroke="{INK}" stroke-width="2"/>')
add(f'<text x="{X(0)-100}" y="{tby+8}" font-size="34" font-weight="bold">GROUND FLOOR PLAN</text>')
add(f'<text x="{X(0)-100}" y="{tby+40}" font-size="18" fill="#444">Rented home interior design brief &#8211; public floor</text>')
add(f'<text x="{X(0)-100}" y="{tby+70}" font-size="16" fill="#555">Sizes from tile count (60&#215;60 cm) &#183; layout from Dreame Aqua 10 map + photos</text>')
add(f'<text x="{X(0)-100}" y="{tby+94}" font-size="16" fill="#555">Divider wall N&#8211;S splits dining (E) from the rest &#183; central switchback stair (2&#215;9) + under-stair store</text>')
add(f'<text x="{CW-50}" y="{tby+8}" font-size="16" text-anchor="end" fill="#333">Date: 18.06.2026</text>')
add(f'<text x="{CW-50}" y="{tby+34}" font-size="16" text-anchor="end" fill="#333">Scale: ~1:75 @A3</text>')
add(f'<text x="{CW-50}" y="{tby+60}" font-size="14" text-anchor="end" fill="#a33">SCHEMATIC &#8211; verify on site</text>')

add('</svg>')
with open("plans/floor-plan-ground-floor.svg","w") as f:
    f.write("\n".join(el))
import cairosvg
cairosvg.svg2png(url="plans/floor-plan-ground-floor.svg",write_to="plans/floor-plan-ground-floor.png",output_width=CW*2,output_height=CH*2)
cairosvg.svg2pdf(url="plans/floor-plan-ground-floor.svg",write_to="plans/floor-plan-ground-floor.pdf")
print("OK")
