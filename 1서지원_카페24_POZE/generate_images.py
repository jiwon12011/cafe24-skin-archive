#!/usr/bin/env python3
"""POZE 2026 — Website Image Generator
Generates all 43 images required for the POZE fashion brand website.
Output: images/ folder with hero, banner, category, product, and detail images.
"""

import os, math
from PIL import Image, ImageDraw, ImageFont

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMG_DIR = os.path.join(SCRIPT_DIR, 'images')
os.makedirs(IMG_DIR, exist_ok=True)

# ── Fonts ─────────────────────────────────────────────────────────────────────
_FEN_B = 'C:/Windows/Fonts/arialbd.ttf'
_FEN   = 'C:/Windows/Fonts/arial.ttf'
_FKO_B = 'C:/Windows/Fonts/malgunbd.ttf'
_FKO   = 'C:/Windows/Fonts/malgun.ttf'
_FSEG  = 'C:/Windows/Fonts/segoeui.ttf'

def gf(path, size):
    for p in [path, _FEN_B, _FEN]:
        try: return ImageFont.truetype(p, size)
        except: pass
    return ImageFont.load_default()

def gfk(size, bold=False):
    return gf(_FKO_B if bold else _FKO, size)

def gfe(size, bold=False):
    return gf(_FEN_B if bold else _FEN, size)

# ── Color Palette ─────────────────────────────────────────────────────────────
BG       = (250, 250, 248)
WHITE    = (255, 255, 255)
BLACK    = (20, 20, 20)
DARK     = (40, 40, 40)
MID      = (110, 108, 102)
LIGHT    = (215, 213, 208)
GOLD     = (201, 169, 110)
GOLD_D   = (152, 120, 68)
GOLD_L   = (235, 210, 160)
NAVY     = (18, 28, 58)
NAVY2    = (28, 40, 76)
CAMEL    = (192, 157, 102)
ROSE     = (218, 152, 145)
ROSE_L   = (245, 218, 212)
CREAM    = (255, 250, 235)
SAGE     = (162, 188, 160)
DENIM    = (82, 110, 158)
OLIVE    = (100, 116, 76)
IVORY    = (255, 253, 242)
BLUSH    = (252, 228, 218)
CHARCOAL = (58, 58, 58)
SAND     = (230, 218, 195)
WINE     = (120, 40, 55)

# ── Utils ─────────────────────────────────────────────────────────────────────
def lc(a, b, t):
    t = max(0.0, min(1.0, t))
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def vg(img, y0, y1, c1, c2):
    d = ImageDraw.Draw(img)
    w = img.width
    h = max(1, y1 - y0)
    for i in range(h):
        d.line([(0, y0 + i), (w - 1, y0 + i)], fill=lc(c1, c2, i / h))

def rg(img, x0, y0, x1, y1, c1, c2, vert=True):
    d = ImageDraw.Draw(img)
    if vert:
        h = max(1, y1 - y0)
        for i in range(h):
            d.line([(x0, y0 + i), (x1 - 1, y0 + i)], fill=lc(c1, c2, i / h))
    else:
        w = max(1, x1 - x0)
        for i in range(w):
            d.line([(x0 + i, y0), (x0 + i, y1 - 1)], fill=lc(c1, c2, i / w))

def ctxt(draw, text, font, y, iw, color=WHITE, anchor=None):
    bb = draw.textbbox((0, 0), text, font=font)
    tw = bb[2] - bb[0]
    draw.text(((iw - tw) // 2, y), text, font=font, fill=color)

def save(img, name, q=92):
    p = os.path.join(IMG_DIR, name)
    img.save(p, 'JPEG', quality=q, optimize=True)
    kb = os.path.getsize(p) // 1024
    print(f'  ✓ {name:<38s} {img.width}×{img.height}  {kb}KB')

# ── Garment Drawing (1200×1200 space → downsample to 600×600) ─────────────────
def draw_shirt(d, cx, color, collar='v'):
    top_y, bot_y = 200, 900
    tw, bw = 300, 240
    shade = lc(color, (0,0,0), 0.13)
    dark  = lc(color, (0,0,0), 0.22)
    # Shadow
    off = 15
    d.polygon([(cx-tw+off,top_y+off),(cx+tw+off,top_y+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(198,193,185))
    # Body
    d.polygon([(cx-tw,top_y),(cx+tw,top_y),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    # Left sleeve
    d.polygon([(cx-tw-85,top_y+25),(cx-tw,top_y),(cx-tw,top_y+240),(cx-tw-85,top_y+265)], fill=color)
    # Right sleeve
    d.polygon([(cx+tw,top_y),(cx+tw+85,top_y+25),(cx+tw+85,top_y+265),(cx+tw,top_y+240)], fill=color)
    # Collar
    if collar == 'v':
        d.polygon([(cx-65,top_y),(cx+65,top_y),(cx,top_y+130)], fill=BG)
        d.line([(cx-65,top_y),(cx,top_y+130)], fill=dark, width=3)
        d.line([(cx+65,top_y),(cx,top_y+130)], fill=dark, width=3)
    else:
        d.ellipse([cx-78,top_y-12,cx+78,top_y+105], fill=BG)
    # Center button line
    d.line([(cx, top_y+130),(cx, bot_y)], fill=dark, width=3)
    for i in range(5):
        by = top_y + 145 + i * 95
        d.ellipse([cx-11,by-11,cx+11,by+11], fill=dark)
    # Side shading
    d.line([(cx-tw,top_y),(cx-bw,bot_y)], fill=shade, width=7)
    d.line([(cx+tw,top_y),(cx+bw,bot_y)], fill=shade, width=7)
    # Cuff seam
    d.line([(cx-tw-85,top_y+240),(cx-tw,top_y+240)], fill=dark, width=3)
    d.line([(cx+tw,top_y+240),(cx+tw+85,top_y+240)], fill=dark, width=3)

def draw_knit(d, cx, color):
    top_y, bot_y = 175, 920
    tw, bw = 320, 260
    shade = lc(color,(0,0,0),0.12)
    off = 15
    d.polygon([(cx-tw+off,top_y+off),(cx+tw+off,top_y+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(198,193,185))
    d.polygon([(cx-tw,top_y),(cx+tw,top_y),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    # Sleeves
    d.polygon([(cx-tw-115,top_y+15),(cx-tw,top_y),(cx-tw,top_y+260),(cx-tw-115,top_y+280)], fill=color)
    d.polygon([(cx+tw,top_y),(cx+tw+115,top_y+15),(cx+tw+115,top_y+280),(cx+tw,top_y+260)], fill=color)
    # Round neck
    d.ellipse([cx-92,top_y-18,cx+92,top_y+108], fill=BG)
    # Ribbed hem
    rib = lc(color,(0,0,0),0.14)
    for i in range(5):
        y = bot_y - 80 + i * 16
        d.line([(cx-bw,y),(cx+bw,y)], fill=rib, width=3)
    # Ribbed cuffs
    for i in range(4):
        y = top_y + 265 + i * 13
        d.line([(cx-tw-115,y),(cx-tw,y)], fill=rib, width=2)
        d.line([(cx+tw,y),(cx+tw+115,y)], fill=rib, width=2)
    # Knit texture
    tc = lc(color,(0,0,0),0.08)
    for ky in range(top_y+120, bot_y-90, 24):
        for kx in range(cx-bw+20, cx+bw-30, 30):
            d.line([(kx,ky+12),(kx+15,ky),(kx+30,ky+12)], fill=tc, width=2)
    d.line([(cx-tw,top_y),(cx-bw,bot_y)], fill=shade, width=7)
    d.line([(cx+tw,top_y),(cx+bw,bot_y)], fill=shade, width=7)

def draw_pants(d, cx, color, style='straight'):
    top_y, wb_h = 75, 72
    bot_y = 960
    hw = 212
    shade = lc(color,(0,0,0),0.12)
    wb_col = lc(color,(0,0,0),0.28)
    buckle = GOLD if max(color)<90 else lc(color,(0,0,0),0.4)
    off = 15
    # Waistband shadow+main
    d.rectangle([cx-hw+off,top_y+off,cx+hw+off,top_y+wb_h+off], fill=(192,187,180))
    d.rectangle([cx-hw,top_y,cx+hw,top_y+wb_h], fill=wb_col)
    # Belt loops
    for bx in [cx-130, cx-40, cx+40, cx+130]:
        d.rectangle([bx-9,top_y-12,bx+9,top_y+18], fill=wb_col)
    # Buckle
    d.rounded_rectangle([cx-26,top_y-10,cx+26,top_y+16], radius=4, fill=buckle)
    d.rectangle([cx-10,top_y-5,cx+10,top_y+10], fill=lc(buckle,WHITE,0.3))

    crotch_y = top_y + wb_h + 160
    gap = 22
    if style == 'wide':
        lx_t, lx_b = cx-hw+18, cx-hw-65
        rx_t, rx_b = cx+hw-18, cx+hw+65
    elif style == 'flare':
        lx_t, lx_b = cx-105, cx-188
        rx_t, rx_b = cx+105, cx+188
    elif style == 'cargo':
        lx_t, lx_b = cx-118, cx-98
        rx_t, rx_b = cx+118, cx+98
    else:
        lx_t, lx_b = cx-102, cx-85
        rx_t, rx_b = cx+102, cx+85

    # Shadow legs
    d.polygon([(cx-gap+off,crotch_y+off),(lx_t+off,top_y+wb_h+off),(lx_b+off,bot_y+off),(cx-gap+off,bot_y+off)], fill=(192,187,180))
    d.polygon([(cx+gap+off,crotch_y+off),(rx_t+off,top_y+wb_h+off),(rx_b+off,bot_y+off),(cx+gap+off,bot_y+off)], fill=(192,187,180))
    # Legs
    d.polygon([(cx-gap,crotch_y),(lx_t,top_y+wb_h),(lx_b,bot_y),(cx-gap,bot_y)], fill=color)
    d.polygon([(cx+gap,crotch_y),(rx_t,top_y+wb_h),(rx_b,bot_y),(cx+gap,bot_y)], fill=color)
    # Cargo pockets
    if style == 'cargo':
        pk = lc(color,(0,0,0),0.15)
        d.rectangle([lx_t+18,crotch_y+75,lx_t+130,crotch_y+220], outline=pk, width=3)
        d.rectangle([rx_t-130,crotch_y+75,rx_t-18,crotch_y+220], outline=pk, width=3)
        for px in [lx_t+74, rx_t-74]:
            d.line([(px, crotch_y+75),(px,crotch_y+220)], fill=pk, width=2)
    # Denim stitch
    if color == DENIM:
        sw = (180,200,230)
        d.line([(cx-gap,crotch_y),(cx-gap*1.1,bot_y)], fill=sw, width=2)
        d.line([(cx+gap,crotch_y),(cx+gap*1.1,bot_y)], fill=sw, width=2)
    else:
        d.line([(cx-gap,crotch_y),(cx-gap*1.1,bot_y)], fill=shade, width=3)
        d.line([(cx+gap,crotch_y),(cx+gap*1.1,bot_y)], fill=shade, width=3)

def draw_skirt(d, cx, color, style='pleated'):
    top_y = 145; bot_y = 885; hw = 172
    wb_col = lc(color,(0,0,0),0.22)
    shade  = lc(color,(0,0,0),0.10)
    bw = 395 if style=='pleated' else 310
    off = 15
    d.polygon([(cx-hw+off,top_y+60+off),(cx+hw+off,top_y+60+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(192,187,180))
    d.rectangle([cx-hw+off,top_y+off,cx+hw+off,top_y+60+off], fill=(185,180,172))
    d.rectangle([cx-hw,top_y,cx+hw,top_y+62], fill=wb_col)
    d.polygon([(cx-hw,top_y+62),(cx+hw,top_y+62),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    if style == 'pleated':
        pc = lc(color,(0,0,0),0.10)
        n = 9
        for i in range(1, n):
            t = i / n
            xt = cx - hw + int(t * 2 * hw)
            xb = cx - bw + int(t * 2 * bw)
            d.line([(xt,top_y+62),(xb,bot_y)], fill=pc, width=2)
        light_pc = lc(color,WHITE,0.12)
        for i in range(1, n):
            t = (i + 0.15) / n
            xt = cx - hw + int(t * 2 * hw)
            xb = cx - bw + int(t * 2 * bw)
            d.line([(xt,top_y+62),(xb,bot_y)], fill=light_pc, width=1)
    d.line([(cx-bw,bot_y),(cx+bw,bot_y)], fill=wb_col, width=4)

def draw_dress(d, cx, color, neckline='v', length='midi'):
    top_y = 78; mid_y = 410
    bot_y = 945 if length == 'midi' else 700
    tw = 242; bw = 325 if length=='midi' else 275
    shade = lc(color,(0,0,0),0.12)
    dark  = lc(color,(0,0,0),0.22)
    off = 15
    d.polygon([(cx-tw+off,top_y+off),(cx+tw+off,top_y+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(192,187,180))
    d.polygon([(cx-tw,top_y),(cx+tw,top_y),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    if neckline == 'slip':
        # Straps
        d.rectangle([cx-tw,top_y,cx-tw+95,top_y+110], fill=color)
        d.rectangle([cx+tw-95,top_y,cx+tw,top_y+110], fill=color)
        # Chest cut
        d.polygon([(cx-tw+95,top_y),(cx+tw-95,top_y),(cx+tw-95,top_y+90),(cx,top_y+195),(cx-tw+95,top_y+90)], fill=BG)
        # Bow/strap detail
        d.line([(cx-tw+95,top_y),(cx-tw+95,top_y+110)], fill=dark, width=3)
        d.line([(cx+tw-95,top_y),(cx+tw-95,top_y+110)], fill=dark, width=3)
    elif neckline == 'v':
        d.polygon([(cx-70,top_y),(cx+70,top_y),(cx,top_y+135)], fill=BG)
        d.line([(cx-70,top_y),(cx,top_y+135)], fill=dark, width=3)
        d.line([(cx+70,top_y),(cx,top_y+135)], fill=dark, width=3)
        # Sleeves
        d.polygon([(cx-tw-62,top_y+18),(cx-tw,top_y),(cx-tw,top_y+148),(cx-tw-62,top_y+165)], fill=color)
        d.polygon([(cx+tw,top_y),(cx+tw+62,top_y+18),(cx+tw+62,top_y+165),(cx+tw,top_y+148)], fill=color)
    else:  # round
        d.ellipse([cx-82,top_y-14,cx+82,top_y+108], fill=BG)
        d.polygon([(cx-tw-62,top_y+18),(cx-tw,top_y),(cx-tw,top_y+148),(cx-tw-62,top_y+165)], fill=color)
        d.polygon([(cx+tw,top_y),(cx+tw+62,top_y+18),(cx+tw+62,top_y+165),(cx+tw,top_y+148)], fill=color)
    # Floral pattern for product 09
    if color == ROSE_L:
        fc = lc(ROSE,(255,255,255),0.3)
        fc2 = lc(ROSE,(0,0,0),0.1)
        for fy in range(top_y+200, bot_y-60, 70):
            for fx in range(cx-bw+30, cx+bw-30, 60):
                r = 12
                d.ellipse([fx-r,fy-r,fx+r,fy+r], fill=fc)
                d.ellipse([fx-5,fy-5,fx+5,fy+5], fill=fc2)
    # Waist seam
    wc = lc(color,(0,0,0),0.10)
    xoff = int((bw-tw)*0.35)
    d.line([(cx-tw+xoff, mid_y),(cx+tw-xoff, mid_y)], fill=wc, width=3)
    d.line([(cx-tw,top_y),(cx-bw,bot_y)], fill=shade, width=7)
    d.line([(cx+tw,top_y),(cx+bw,bot_y)], fill=shade, width=7)

def draw_coat(d, cx, color, style='coat'):
    top_y = 58
    bot_y = 985 if style in ('coat','trench') else 870
    tw = 302; bw = 285
    shade = lc(color,(0,0,0),0.13)
    lapel_col = lc(color,(0,0,0),0.22)
    off = 16
    d.polygon([(cx-tw+off,top_y+off),(cx+tw+off,top_y+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(185,180,172))
    d.polygon([(cx-tw,top_y),(cx+tw,top_y),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    sl_bot = 685 if style != 'jacket' else 540
    d.polygon([(cx-tw-92,top_y+18),(cx-tw,top_y),(cx-tw,sl_bot),(cx-tw-92,sl_bot+32)], fill=color)
    d.polygon([(cx+tw,top_y),(cx+tw+92,top_y+18),(cx+tw+92,sl_bot+32),(cx+tw,sl_bot)], fill=color)
    # Lapels
    d.polygon([(cx-45,top_y),(cx,top_y+165),(cx-85,top_y+315),(cx-tw,top_y+82)], fill=lapel_col)
    d.polygon([(cx+45,top_y),(cx,top_y+165),(cx+85,top_y+315),(cx+tw,top_y+82)], fill=lapel_col)
    # Collar
    d.polygon([(cx-tw,top_y+82),(cx-85,top_y+315),(cx,top_y+165),(cx+85,top_y+315),(cx+tw,top_y+82),(cx+tw,top_y),(cx,top_y+60),(cx-tw,top_y)], fill=lc(lapel_col,color,0.4))
    if style == 'trench':
        belt_col = lc(color,(0,0,0),0.32)
        d.rectangle([cx-bw,478,cx+bw,530], fill=belt_col)
        d.rounded_rectangle([cx-30,465,cx+30,542], radius=5, fill=GOLD)
        d.rectangle([cx-10,477,cx+10,530], fill=lc(GOLD,WHITE,0.3))
        # Epaulettes
        epc = lc(color,(0,0,0),0.2)
        d.rectangle([cx-tw-92,top_y+60,cx-tw,top_y+100], fill=epc)
        d.rectangle([cx+tw,top_y+60,cx+tw+92,top_y+100], fill=epc)
    # Buttons
    btn_start = 345; btn_n = 4 if style != 'blazer' else 2
    for i in range(btn_n):
        by = btn_start + i * 118
        d.ellipse([cx-15,by-15,cx+15,by+15], fill=GOLD)
        d.ellipse([cx-6,by-6,cx+6,by+6], fill=GOLD_D)
    # Pocket (welt)
    pk = lc(color,(0,0,0),0.12)
    for px, py in [(cx-180, 620),(cx+180-80, 620)]:
        d.rectangle([px, py, px+80, py+8], fill=pk)
    d.line([(cx-tw,top_y),(cx-bw,bot_y)], fill=shade, width=8)
    d.line([(cx+tw,top_y),(cx+bw,bot_y)], fill=shade, width=8)
    # Cuff seam
    d.line([(cx-tw-92,sl_bot),(cx-tw,sl_bot)], fill=lc(color,(0,0,0),0.2), width=4)
    d.line([(cx+tw,sl_bot),(cx+tw+92,sl_bot)], fill=lc(color,(0,0,0),0.2), width=4)

def draw_denim_jacket(d, cx):
    color = DENIM; top_y=105; bot_y=718; tw=282; bw=252
    lapel_col = lc(color,(0,0,0),0.22)
    off = 14
    d.polygon([(cx-tw+off,top_y+off),(cx+tw+off,top_y+off),(cx+bw+off,bot_y+off),(cx-bw+off,bot_y+off)], fill=(160,175,195))
    d.polygon([(cx-tw,top_y),(cx+tw,top_y),(cx+bw,bot_y),(cx-bw,bot_y)], fill=color)
    d.polygon([(cx-tw-82,top_y+18),(cx-tw,top_y),(cx-tw,top_y+355),(cx-tw-82,top_y+378)], fill=color)
    d.polygon([(cx+tw,top_y),(cx+tw+82,top_y+18),(cx+tw+82,top_y+378),(cx+tw,top_y+355)], fill=color)
    # Collar/lapels
    d.polygon([(cx-55,top_y),(cx,top_y+122),(cx-82,top_y+295),(cx-tw,top_y+72)], fill=lapel_col)
    d.polygon([(cx+55,top_y),(cx,top_y+122),(cx+82,top_y+295),(cx+tw,top_y+72)], fill=lapel_col)
    # Chest pockets
    pk = lc(color,(0,0,0),0.18)
    d.rectangle([cx-205,top_y+175,cx-105,top_y+280], outline=pk, width=4)
    d.rectangle([cx+105,top_y+175,cx+205,top_y+280], outline=pk, width=4)
    d.line([(cx-205,top_y+215),(cx-105,top_y+215)], fill=pk, width=3)
    d.line([(cx+105,top_y+215),(cx+205,top_y+215)], fill=pk, width=3)
    # Buttons
    for i in range(5):
        d.ellipse([cx-13,top_y+148+i*98,cx+13,top_y+174+i*98], fill=lapel_col)
    # White stitching
    sw = (200, 218, 240)
    for line in [[(cx-tw,top_y),(cx-bw,bot_y)],[(cx+tw,top_y),(cx+bw,bot_y)]]:
        d.line(line, fill=sw, width=3)
    d.line([(cx-tw-82,top_y+355),(cx-tw,top_y+355)], fill=sw, width=2)
    d.line([(cx+tw,top_y+355),(cx+tw+82,top_y+355)], fill=sw, width=2)
    # Wash lines
    wc = lc(color,WHITE,0.07)
    for wy in range(top_y+40, bot_y, 55):
        d.line([(cx-bw+20,wy),(cx+bw-20,wy)], fill=wc, width=1)

def draw_earrings(d, cx, cy=600):
    for ex in [cx - 162, cx + 162]:
        # Hook arc
        d.arc([ex-22,cy-210,ex+22,cy-135], 180, 360, fill=GOLD, width=5)
        # Chain links
        for ci in range(7):
            ly = cy - 135 + ci * 28
            d.ellipse([ex-7,ly,ex+7,ly+20], outline=GOLD, width=3)
        # Drop
        d.polygon([(ex,cy-20),(ex-38,cy+115),(ex+38,cy+115)], fill=GOLD)
        d.polygon([(ex,cy-12),(ex-26,cy+90),(ex+26,cy+90)], fill=GOLD_L)
        # Gem
        d.ellipse([ex-16,cy+18,ex+16,cy+65], fill=(245,220,180))
        d.ellipse([ex-8,cy+28,ex+8,cy+55], fill=WHITE)

def draw_bag(d, cx):
    cy = 596; bw = 412; bh = 368
    off = 18
    d.rounded_rectangle([cx-bw//2+off,cy-bh//2+off,cx+bw//2+off,cy+bh//2+off], radius=14, fill=(175,138,82))
    d.rounded_rectangle([cx-bw//2,cy-bh//2,cx+bw//2,cy+bh//2], radius=14, fill=CAMEL)
    # Handle arcs
    hc = lc(CAMEL,(0,0,0),0.32)
    d.arc([cx-188,cy-bh//2-158,cx-42,cy-bh//2+55], 180, 0, fill=hc, width=16)
    d.arc([cx+42,cy-bh//2-158,cx+188,cy-bh//2+55], 180, 0, fill=hc, width=16)
    # Front pocket
    pk = lc(CAMEL,(0,0,0),0.14)
    d.rounded_rectangle([cx-108,cy-58,cx+108,cy+128], radius=10, outline=pk, width=3)
    # Clasp
    d.rounded_rectangle([cx-32,cy-bh//2+8,cx+32,cy-bh//2+58], radius=7, fill=GOLD)
    d.ellipse([cx-12,cy-bh//2+18,cx+12,cy-bh//2+48], fill=GOLD_D)
    # Stitching
    sc = lc(CAMEL,WHITE,0.18)
    d.rounded_rectangle([cx-bw//2+14,cy-bh//2+14,cx+bw//2-14,cy+bh//2-14], radius=12, outline=sc, width=2)
    # Brand emboss area
    d.rectangle([cx-52,cy+90,cx+52,cy+118], fill=lc(CAMEL,(0,0,0),0.08))

def garment_for(p, d, cx, large=False):
    _,_,_,_,_,color,gtype,style,_ = p
    if gtype == 'shirt':    draw_shirt(d, cx, color, collar=style)
    elif gtype == 'knit':   draw_knit(d, cx, color)
    elif gtype == 'pants':  draw_pants(d, cx, color, style=style)
    elif gtype == 'skirt':  draw_skirt(d, cx, color, style=style)
    elif gtype == 'dress':
        length = 'mini' if p[0] == 11 else 'midi'
        draw_dress(d, cx, color, neckline=style, length=length)
    elif gtype == 'coat':   draw_coat(d, cx, color, style=style)
    elif gtype == 'denim':  draw_denim_jacket(d, cx)
    elif gtype == 'earring': draw_earrings(d, cx)
    elif gtype == 'bag':    draw_bag(d, cx)

# ── Product Catalog ──────────────────────────────────────────────────────────
PRODUCTS = [
    (1,  '화이트 리넨 오버사이즈 셔츠', 'White Linen Shirt',        89000, 120000, (252,252,250), 'shirt',   'v',       'SALE'),
    (2,  '로즈 핀턱 블라우스',          'Rose Pintuck Blouse',       67000,      0, ROSE,          'shirt',   'round',   'NEW'),
    (3,  '크림 케이블 니트 스웨터',     'Cream Cable Knit Sweater',  98000,      0, (245,234,208), 'knit',    '',        'NEW'),
    (4,  '세이지 그린 오픈 카디건',     'Sage Green Open Cardigan', 112000, 148000, SAGE,          'knit',    '',        'SALE'),
    (5,  '블랙 와이드레그 팬츠',        'Black Wide-Leg Pants',      75000,      0, DARK,          'pants',   'wide',    ''),
    (6,  '베이지 플리츠 미디 스커트',   'Beige Pleated Midi Skirt',  58000,      0, SAND,          'skirt',   'pleated', 'NEW'),
    (7,  '올리브 카고 팬츠',            'Olive Cargo Pants',         83000,      0, OLIVE,         'pants',   'cargo',   ''),
    (8,  '라이트워시 플레어 진',        'Light Wash Flare Jeans',    95000, 130000, DENIM,         'pants',   'flare',   'SALE'),
    (9,  '플로럴 프린트 미디 드레스',   'Floral Print Midi Dress',  143000,      0, ROSE_L,        'dress',   'v',       'NEW'),
    (10, '아이보리 실크 슬립 드레스',   'Ivory Silk Slip Dress',    168000,      0, IVORY,         'dress',   'slip',    ''),
    (11, '블랙 리넨 미니 드레스',       'Black Linen Mini Dress',    89000,      0, (45,45,45),    'dress',   'round',   ''),
    (12, '카멜 더블브레스트 코트',      'Camel DB Coat',            298000, 398000, CAMEL,         'coat',    'trench',  'SALE'),
    (13, '네이비 오버사이즈 블레이저',  'Navy Oversized Blazer',    178000,      0, NAVY2,         'coat',    'blazer',  'NEW'),
    (14, '빈티지 데님 재킷',            'Vintage Denim Jacket',     125000,      0, DENIM,         'denim',   '',        ''),
    (15, '골드 멀티 체인 이어링',       'Gold Multi-Chain Earrings', 34000,      0, GOLD,          'earring', '',        'NEW'),
    (16, '스트럭처드 레더 토트백',      'Structured Leather Tote',  245000, 320000, CAMEL,         'bag',     '',        'SALE'),
]

# ── Product Thumbnails (600×600, drawn at 1200×1200 then downsampled) ─────────
def make_product_thumb(p):
    num = p[0]
    big = Image.new('RGB', (1200, 1200), BG)
    # Subtle vignette background
    vg(big, 0, 600, BG, lc(BG,(210,208,204),0.5))
    vg(big, 600, 1200, lc(BG,(210,208,204),0.5), BG)
    d = ImageDraw.Draw(big)
    garment_for(p, d, 600)
    out = big.resize((600, 600), Image.LANCZOS)
    save(out, f'product{num:02d}.jpg')

# ── Product Detail Description Images (800×3000) ──────────────────────────────
SECTION_THEMES = {
    'shirt':   {'h1': (44,44,44),   'h2': (68,60,50),   'acc': GOLD,   'sec': (248,246,240)},
    'knit':    {'h1': (50,45,38),   'h2': (72,65,52),   'acc': CAMEL,  'sec': (248,244,235)},
    'pants':   {'h1': (35,38,45),   'h2': (55,58,68),   'acc': (130,145,165), 'sec': (243,245,248)},
    'skirt':   {'h1': (55,45,45),   'h2': (75,62,58),   'acc': ROSE,   'sec': (250,244,242)},
    'dress':   {'h1': (60,40,45),   'h2': (80,58,62),   'acc': ROSE,   'sec': (252,245,244)},
    'coat':    {'h1': (25,32,50),   'h2': (40,50,72),   'acc': GOLD,   'sec': (242,244,250)},
    'denim':   {'h1': (35,50,72),   'h2': (50,68,95),   'acc': (180,195,220),'sec': (240,245,252)},
    'earring': {'h1': (48,42,30),   'h2': (68,60,42),   'acc': GOLD_L, 'sec': (252,248,238)},
    'bag':     {'h1': (50,42,30),   'h2': (70,60,42),   'acc': CAMEL,  'sec': (252,248,238)},
}

MATERIAL_INFO = {
    'shirt':   ('리넨 100%', 'Linen 100%',   '린넨 소재의 자연스러운 텍스처와 통기성이 뛰어난 여름 필수 아이템입니다.'),
    'knit':    ('울 60% / 아크릴 40%', 'Wool 60% / Acrylic 40%', '고급 울 혼방 소재로 부드럽고 따뜻한 착용감을 선사합니다.'),
    'pants':   ('코튼 98% / 스판덱스 2%', 'Cotton 98% / Spandex 2%', '적당한 신축성으로 활동적인 착용감을 제공하는 프리미엄 소재입니다.'),
    'skirt':   ('폴리에스터 80% / 레이온 20%', 'Polyester 80% / Rayon 20%', '가볍고 우아하게 떨어지는 소재로 우아한 실루엣을 완성합니다.'),
    'dress':   ('레이온 95% / 스판덱스 5%', 'Rayon 95% / Spandex 5%', '부드럽고 드레이프감이 좋아 여성스러운 라인을 완성합니다.'),
    'coat':    ('울 60% / 폴리에스터 40%', 'Wool 60% / Polyester 40%', '두툼하면서도 고급스러운 울 혼방 소재로 보온성이 탁월합니다.'),
    'denim':   ('코튼 100%', 'Cotton 100%', '프리미엄 데님 원단으로 제작되어 내구성이 뛰어납니다.'),
    'earring': ('14K 골드 도금', '14K Gold Plating', '알레르기가 없는 의료용 스테인리스 스틸에 14K 골드 도금을 적용했습니다.'),
    'bag':     ('소가죽 100%', 'Genuine Leather 100%', '이탈리아산 풀그레인 소가죽을 사용한 프리미엄 백입니다.'),
}

SIZE_TABLES = {
    'shirt':   [('S','85','96','59'),('M','89','100','61'),('L','93','104','63'),('XL','97','108','65')],
    'knit':    [('S','84','95','57'),('M','88','100','59'),('L','92','105','61'),('XL','96','110','63')],
    'pants':   [('S','66','93','10.5'),('M','70','95','10.5'),('L','74','97','11'),('XL','78','99','11')],
    'skirt':   [('S','62','86','-'),('M','66','90','-'),('L','70','94','-'),('XL','74','98','-')],
    'dress':   [('S','84','93','89'),('M','88','97','91'),('L','92','101','93'),('XL','96','105','95')],
    'coat':    [('S','88','105','105'),('M','92','109','107'),('L','96','113','109'),('XL','100','117','111')],
    'denim':   [('S','84','96','57'),('M','88','100','59'),('L','92','104','61'),('XL','96','108','63')],
    'earring': None,
    'bag':     None,
}

def make_product_detail(p):
    num, name_ko, name_en, price, orig, color, gtype, style, badge = p
    W, H = 800, 3000
    img = Image.new('RGB', (W, H), BG)
    d = ImageDraw.Draw(img)
    theme = SECTION_THEMES.get(gtype, SECTION_THEMES['shirt'])
    h1, h2, acc, sec_bg = theme['h1'], theme['h2'], theme['acc'], theme['sec']

    # ── Section 1: Hero (y: 0-520) ──
    vg(img, 0, 520, h1, h2)
    # Gold accent bar
    d.line([(60, 90),(W-60, 90)], fill=lc(acc,WHITE,0.3), width=1)
    d.line([(60, 432),(W-60, 432)], fill=lc(acc,WHITE,0.3), width=1)
    # Brand
    f_brand = gfe(28, True)
    ctxt(d, 'POZE', f_brand, 118, W, color=lc(acc,WHITE,0.5))
    # SS label
    f_season = gfe(15)
    ctxt(d, '2026 S/S COLLECTION', f_season, 162, W, color=lc(acc,WHITE,0.35))
    # Product name KO
    f_name_ko = gfk(38, True)
    ctxt(d, name_ko, f_name_ko, 210, W, color=WHITE)
    # Product name EN
    f_name_en = gfe(20)
    ctxt(d, name_en.upper(), f_name_en, 272, W, color=lc(acc,WHITE,0.7))
    # Price
    f_price = gfe(34, True)
    price_str = f'₩ {price:,}'
    ctxt(d, price_str, f_price, 322, W, color=acc)
    if orig:
        f_orig = gfe(18)
        ctxt(d, f'정상가 ₩ {orig:,}', f_orig, 376, W, color=lc(WHITE,h2,0.45))

    # ── Section 2: Product visual (y: 520-1220) ──
    vg(img, 520, 1220, sec_bg, lc(sec_bg,BG,0.5))
    # Draw product illustration at 1.2× in center
    tmp = Image.new('RGB', (1200, 1200), lc(sec_bg,BG,0.5))
    dtmp = ImageDraw.Draw(tmp)
    garment_for(p, dtmp, 600)
    product_img = tmp.resize((600, 600), Image.LANCZOS)
    img.paste(product_img, (100, 550))
    # Tagline
    f_tag = gfe(14)
    taglines = {
        'shirt': 'Premium fabric. Perfect drape. Effortless style.',
        'knit': 'Soft. Warm. Timeless.',
        'pants': 'Clean silhouette. All-day comfort.',
        'skirt': 'Feminine flow. Modern edge.',
        'dress': 'Wear it your way.',
        'coat': 'Investment piece. Season after season.',
        'denim': 'Classic reborn.',
        'earring': 'One pair. Endless looks.',
        'bag': 'Structured. Refined. Essential.',
    }
    ctxt(d, taglines.get(gtype, 'POZE Signature Piece'), f_tag, 1168, W, color=lc(h1,BG,0.35))

    # ── Section 3: Key Features (y: 1220-1640) ──
    vg(img, 1220, 1640, BG, sec_bg)
    f_feat_t = gfe(15, True)
    f_feat_b = gfe(13)
    features = {
        'shirt':   [('고급 소재','프리미엄 리넨'),('여유 핏','오버사이즈 실루엣'),('기능성','세탁기 가능')],
        'knit':    [('부드러운 감촉','울 혼방 소재'),('풍성한 볼륨','케이블 니트 패턴'),('올 시즌','레이어드 가능')],
        'pants':   [('와이드 실루엣','트렌디한 핏'),('편안한 착용감','미드라이즈 디자인'),('다목적','캐주얼·포멀')],
        'skirt':   [('우아한 플리츠','여성스러운 실루엣'),('가볍고 편안','레이어드 가능'),('올 시즌','사계절 착용 가능')],
        'dress':   [('원피스 한 벌로','완성되는 룩'),('다양한 스타일링','벨트 활용 가능'),('고급 소재','부드러운 드레이프')],
        'coat':    [('프리미엄 소재','울 혼방 코트'),('클래식 디자인','더블 브레스트'),('넉넉한 핏','레이어링 용이')],
        'denim':   [('빈티지 워싱','자연스러운 페이딩'),('클래식 핏','정석 데님 자켓'),('내구성 우수','코튼 100%')],
        'earring': [('14K 도금','알러지 프리'),('경량 디자인','편안한 착용감'),('다용도 스타일링','데일리·포멀')],
        'bag':     [('진품 가죽','이탈리아산 소가죽'),('스트럭처드 폼','형태 유지'),('넉넉한 수납','노트북 수납 가능')],
    }
    feat_list = features.get(gtype, features['shirt'])
    col_w = W // 3
    for fi, (ft, fb) in enumerate(feat_list):
        fx = fi * col_w + col_w // 2
        fy = 1290
        # Icon circle
        d.ellipse([fx-30,fy-30,fx+30,fy+30], fill=acc, outline=lc(acc,(0,0,0),0.2), width=2)
        # Roman numeral / number
        f_icon = gfe(18, True)
        inum = ['I','II','III'][fi]
        ib = d.textbbox((0,0),inum,font=f_icon)
        d.text((fx-(ib[2]-ib[0])//2, fy-10), inum, font=f_icon, fill=WHITE)
        # Text
        ctxt_block(d, ft, f_feat_t, fy+48, fi*col_w, col_w, h1)
        ctxt_block(d, fb, f_feat_b, fy+72, fi*col_w, col_w, lc(h1,BG,0.3))

    # ── Section 4: Size Guide (y: 1640-2080) ──
    vg(img, 1640, 2080, sec_bg, BG)
    f_section = gfe(20, True)
    f_table_h = gfe(13, True)
    f_table   = gfe(13)
    ctxt(d, 'SIZE GUIDE', f_section, 1665, W, color=h1)
    ctxt(d, '사이즈 가이드', gfk(14), 1698, W, color=lc(h1,BG,0.4))

    table = SIZE_TABLES.get(gtype)
    if table:
        hdrs = ['SIZE','가슴(cm)','허리(cm)','총장(cm)'] if gtype not in ['pants','skirt'] else (['SIZE','허리(cm)','힙(cm)','총장(cm)'] if gtype=='pants' else ['SIZE','허리(cm)','힙(cm)','총장(cm)'])
        if gtype in ['earring','bag']:
            pass
        else:
            col_xs = [80, 240, 400, 580]
            col_w2 = 160
            # Header row
            hy = 1748
            d.rectangle([60, hy, W-60, hy+38], fill=h1)
            for ci, hdr in enumerate(hdrs):
                hb = d.textbbox((0,0),hdr,font=f_table_h)
                x = col_xs[ci] + (col_w2-(hb[2]-hb[0]))//2
                d.text((x, hy+10), hdr, font=f_table_h, fill=WHITE)
            # Data rows
            for ri, row in enumerate(table):
                ry = hy + 38 + ri * 46
                row_bg = BG if ri % 2 == 0 else lc(sec_bg,BG,0.6)
                d.rectangle([60, ry, W-60, ry+46], fill=row_bg)
                for ci, val in enumerate(row):
                    vb = d.textbbox((0,0),val,font=f_table)
                    x = col_xs[ci] + (col_w2-(vb[2]-vb[0]))//2
                    clr = acc if ci == 0 else lc(h1,BG,0.2)
                    d.text((x, ry+14), val, font=f_table, fill=clr)
            # Border
            d.rectangle([60, hy, W-60, hy+38+len(table)*46], outline=lc(h1,BG,0.15), width=1)
    else:
        # For accessories: show dimensions
        dim_text = '이어링 길이: 10cm' if gtype=='earring' else '가로 36cm × 세로 28cm × 폭 14cm'
        ctxt(d, dim_text, gfk(16), 1760, W, color=h1)

    # ── Section 5: Material Details (y: 2080-2480) ──
    vg(img, 2080, 2480, BG, sec_bg)
    ctxt(d, 'MATERIAL & DETAILS', f_section, 2105, W, color=h1)
    ctxt(d, '소재 및 상세 정보', gfk(14), 2138, W, color=lc(h1,BG,0.4))
    mat_en, mat_ko, mat_desc = MATERIAL_INFO.get(gtype, ('','',''))
    # Material block
    d.rounded_rectangle([60, 2180, W-60, 2380], radius=12, fill=lc(sec_bg,BG,0.7), outline=lc(h1,BG,0.12), width=1)
    ctxt(d, mat_en, gfe(16,True), 2204, W, color=h1)
    ctxt(d, mat_ko, gfk(14), 2232, W, color=lc(h1,BG,0.3))
    # Description - wrapped manually
    words = mat_desc
    f_desc = gfk(14)
    ctxt(d, words[:22], f_desc, 2275, W, color=lc(h1,BG,0.25))
    if len(words) > 22:
        ctxt(d, words[22:], f_desc, 2300, W, color=lc(h1,BG,0.25))
    # Made in label
    made = 'Made in Korea' if gtype != 'bag' else 'Made in Italy / Korea Assembly'
    ctxt(d, made, gfe(13), 2345, W, color=acc)

    # ── Section 6: Care Guide (y: 2480-2740) ──
    vg(img, 2480, 2740, sec_bg, h2)
    ctxt(d, 'CARE INSTRUCTIONS', f_section, 2505, W, color=WHITE)
    ctxt(d, '세탁 및 관리 방법', gfk(14), 2538, W, color=lc(WHITE,h2,0.45))
    care_icons = [
        ('30°C','찬물 세탁'),('','그늘 건조'),('','다림질 금지'),('','드라이클리닝'),
    ]
    ci_x_start = 90; ci_spacing = 158
    for ci, (icon, label) in enumerate(care_icons):
        cx_c = ci_x_start + ci * ci_spacing
        cy_c = 2618
        d.rounded_rectangle([cx_c-45,cy_c-42,cx_c+45,cy_c+42], radius=8, fill=lc(WHITE,h2,0.12), outline=lc(WHITE,h2,0.3), width=1)
        f_icon_txt = gfe(12, True)
        f_care = gfe(11)
        if icon:
            ib = d.textbbox((0,0),icon,font=f_icon_txt)
            d.text((cx_c-(ib[2]-ib[0])//2,cy_c-14), icon, font=f_icon_txt, fill=WHITE)
        else:
            d.ellipse([cx_c-18,cy_c-18,cx_c+18,cy_c+18], outline=WHITE, width=2)
            d.line([(cx_c-12,cy_c-12),(cx_c+12,cy_c+12)], fill=WHITE, width=2)
        lb = d.textbbox((0,0),label,font=f_care)
        d.text((cx_c-(lb[2]-lb[0])//2,cy_c+50), label, font=f_care, fill=lc(WHITE,h2,0.5))

    # ── Section 7: Brand Footer (y: 2740-3000) ──
    vg(img, 2740, 3000, h1, lc(h1,(10,10,10),0.5))
    # Gold divider
    d.line([(60,2800),(W-60,2800)], fill=lc(acc,h1,0.5), width=1)
    f_logo = gfe(36, True)
    ctxt(d, 'POZE', f_logo, 2818, W, color=lc(acc,WHITE,0.6))
    f_tagline = gfe(13)
    ctxt(d, 'Define Your Style', f_tagline, 2872, W, color=lc(WHITE,h1,0.45))
    ctxt(d, 'hello@poze.co.kr  |  1588-0000  |  www.poze.co.kr', gfe(11), 2910, W, color=lc(WHITE,h1,0.6))
    ctxt(d, '© 2026 POZE. All rights reserved.', gfe(11), 2940, W, color=lc(WHITE,h1,0.7))
    ctxt(d, '교환·반품 기간: 수령 후 7일 이내 / 배송비: 주문 금액 50,000원 이상 무료', gfe(11), 2970, W, color=lc(WHITE,h1,0.75))

    save(img, f'detail{num:02d}.jpg', q=88)

def ctxt_block(d, text, font, y, x_off, col_w, color):
    bb = d.textbbox((0,0),text,font=font)
    tw = bb[2]-bb[0]
    d.text((x_off + (col_w-tw)//2, y), text, font=font, fill=color)

# ── Hero Images (2000×900) ────────────────────────────────────────────────────
def make_hero1():
    img = Image.new('RGB', (2000, 900))
    vg(img, 0, 900, (12,14,24), (28,32,52))
    d = ImageDraw.Draw(img)
    # Large circle accent
    for r, op in [(700,0.04),(500,0.05),(300,0.06)]:
        for xi,yi,ri,oi in [(1650,300,r,op),(350,650,r*0.7,op*0.8)]:
            cimg = Image.new('RGB', (2000,900), (0,0,0))
            cov  = ImageDraw.Draw(cimg)
            gc = lc(GOLD,BLACK,0.7)
            cov.ellipse([xi-ri,yi-ri,xi+ri,yi+ri], outline=gc, width=2)
            img = Image.blend(img, cimg, oi)
            d = ImageDraw.Draw(img)
    # Gold bars
    d.line([(0,2),(2000,2)], fill=GOLD, width=3)
    d.line([(0,898),(2000,898)], fill=GOLD, width=3)
    d.line([(75,0),(75,900)], fill=lc(GOLD,BLACK,0.55), width=1)
    d.line([(1925,0),(1925,900)], fill=lc(GOLD,BLACK,0.55), width=1)
    # Season badge
    d.rectangle([180,220,480,270], fill=GOLD)
    f_badge = gfe(20, True)
    d.text((200,232), '2 0 2 6   S / S   C O L L E C T I O N', font=f_badge, fill=BLACK)
    # Title
    f_h1 = gfe(122, True)
    f_h2 = gfe(42, True)
    f_sub = gfe(22)
    d.text((180,290), 'NEW', font=f_h1, fill=WHITE)
    d.text((180,428), 'COLLECTION', font=f_h2, fill=GOLD)
    d.text((180,490), 'Timeless Elegance. Modern Edge.', font=f_sub, fill=lc(WHITE,BLACK,0.35))
    # CTA
    d.rectangle([180,550,410,600], outline=WHITE, width=2)
    f_cta = gfe(18)
    d.text((210,562), 'SHOP NOW  →', font=f_cta, fill=WHITE)
    # Right side: abstract fashion figure
    # Elegant coat silhouette
    fx = 1560
    coat_pts = [(fx-160,120),(fx+160,120),(fx+140,880),(fx-140,880)]
    d.polygon(coat_pts, fill=lc(NAVY2,BLACK,0.3))
    # Sleeve
    d.polygon([(fx-160,120),(fx-280,200),(fx-260,520),(fx-150,480)], fill=lc(NAVY2,BLACK,0.35))
    d.polygon([(fx+160,120),(fx+280,200),(fx+260,520),(fx+150,480)], fill=lc(NAVY2,BLACK,0.35))
    # Lapels
    d.polygon([(fx-50,120),(fx,240),(fx-100,400),(fx-160,160)], fill=lc(NAVY2,BLACK,0.6))
    d.polygon([(fx+50,120),(fx,240),(fx+100,400),(fx+160,160)], fill=lc(NAVY2,BLACK,0.6))
    # Gold outline
    d.polygon(coat_pts, outline=lc(GOLD,BLACK,0.5), width=1)
    save(img, 'hero1.jpg')

def make_hero2():
    img = Image.new('RGB', (2000, 900))
    vg(img, 0, 900, (252,250,242), (238,232,218))
    d = ImageDraw.Draw(img)
    # Soft horizontal stripes
    for yi in range(0,900,12):
        d.line([(0,yi),(2000,yi)], fill=lc((252,250,242),(240,234,220),abs(yi-450)/450), width=1)
    # Dark vertical accent bar
    rg(img, 0, 0, 6, 900, DARK, lc(DARK,BLACK,0.5))
    # Decorative right panel
    rg(img, 1300, 0, 2000, 900, lc(CAMEL,WHITE,0.7), lc(SAND,WHITE,0.5))
    d.line([(1300,0),(1300,900)], fill=lc(CAMEL,WHITE,0.3), width=1)
    # Large "N" decorative
    f_giant = gfe(700, True)
    nb = d.textbbox((0,0),'A',font=f_giant)
    d.text((1280,900-700+80), 'N', font=f_giant, fill=lc(CAMEL,WHITE,0.15))
    # Content
    f_label = gfe(13)
    f_h1 = gfe(80, True)
    f_h2 = gfe(36, True)
    f_sub = gfe(18)
    d.text((140,190), '— NEW ARRIVALS', font=f_label, fill=lc(DARK,WHITE,0.4))
    d.text((140,250), 'SPRING', font=f_h1, fill=DARK)
    d.text((140,350), 'SUMMER', font=f_h1, fill=DARK)
    d.text((140,450), '2026', font=f_h2, fill=CAMEL)
    d.text((140,510), 'Fresh silhouettes for the new season.', font=f_sub, fill=lc(DARK,WHITE,0.35))
    # CTA
    d.rectangle([140,575,355,622], fill=DARK)
    d.text((172,588), 'DISCOVER NOW', font=gfe(16,True), fill=WHITE)
    # Fashion item on right panel
    tmp = Image.new('RGB', (1200,1200), lc(SAND,WHITE,0.5))
    dtmp = ImageDraw.Draw(tmp)
    draw_dress(dtmp, 600, ROSE_L, neckline='v', length='midi')
    prd = tmp.resize((420,420), Image.LANCZOS)
    img.paste(prd, (1450, 240))
    save(img, 'hero2.jpg')

def make_hero3():
    img = Image.new('RGB', (2000, 900))
    vg(img, 0, 900, (35,25,20), (58,42,30))
    d = ImageDraw.Draw(img)
    # Warm texture lines
    for xi in range(0,2000,8):
        tc = lc((35,25,20),(48,35,22), abs(xi-1000)/1000)
        d.line([(xi,0),(xi,900)], fill=tc, width=1)
    # Gold accent
    d.line([(0,2),(2000,2)], fill=GOLD, width=4)
    d.line([(0,898),(2000,898)], fill=GOLD, width=4)
    # Diagonal stripe pattern
    for si in range(-900,2900,80):
        d.line([(si,0),(si+900,900)], fill=lc(GOLD,(35,25,20),0.94), width=1)
    # SALE badge
    d.ellipse([1500,50,1950,500], fill=lc(GOLD,(35,25,20),0.12))
    f_pct = gfe(100, True)
    f_off = gfe(36, True)
    ctxt(d, '40%', f_pct, 130, 2000, color=GOLD)
    ctxt(d, 'OFF', f_off, 248, 2000, color=GOLD_L)
    f_h1 = gfe(88, True)
    f_sub = gfe(24)
    f_label = gfe(14)
    d.text((100,320), 'SPECIAL', font=f_h1, fill=WHITE)
    d.text((100,424), 'OFFER', font=gfe(88,True), fill=GOLD)
    d.text((100,530), 'LIMITED TIME · UP TO 40% OFF SELECTED STYLES', font=f_sub, fill=lc(WHITE,(35,25,20),0.35))
    d.text((100,575), 'Sale ends June 30, 2026', font=f_label, fill=lc(GOLD,WHITE,0.3))
    d.rectangle([100,620,330,668], fill=WHITE)
    d.text((128,630), 'SHOP SALE  →', font=gfe(18,True), fill=DARK)
    save(img, 'hero3.jpg')

# ── Strip Banners (1920×100, 1920×160) ───────────────────────────────────────
def make_banner_strip1():
    img = Image.new('RGB', (1920, 100))
    vg(img, 0, 100, DARK, BLACK)
    d = ImageDraw.Draw(img)
    d.line([(0,0),(1920,0)], fill=GOLD, width=2)
    d.line([(0,99),(1920,99)], fill=GOLD, width=2)
    f = gfe(15)
    msgs = ['🚚 50,000원 이상 무료배송', '✦', '🎁 회원가입 즉시 10% 할인 쿠폰', '✦',
            '🔄 7일 이내 교환·환불 보장', '✦', '💳 무이자 할부 최대 12개월', '✦',
            '🚚 50,000원 이상 무료배송', '✦', '🎁 회원가입 즉시 10% 할인 쿠폰', '✦']
    x = 0
    for msg in msgs:
        bb = d.textbbox((0,0),msg,font=f)
        tw = bb[2]-bb[0]
        d.text((x, 36), msg, font=f, fill=lc(WHITE,DARK,0.2))
        x += tw + 60
    save(img, 'banner_strip1.jpg')

def make_banner_strip2():
    img = Image.new('RGB', (1920, 160))
    rg(img, 0, 0, 1920, 160, lc(ROSE_L,WHITE,0.5), lc(BLUSH,WHITE,0.4), vert=False)
    d = ImageDraw.Draw(img)
    # Gold borders
    d.line([(0,0),(1920,0)], fill=lc(ROSE,WHITE,0.4), width=2)
    d.line([(0,159),(1920,159)], fill=lc(ROSE,WHITE,0.4), width=2)
    # Content: centered promo text
    f_title = gfk(30, True)
    f_sub   = gfk(16)
    f_cta   = gfe(15, True)
    ctxt(d, '2026 여름 신상품 50% 할인 특가 세일', f_title, 28, 1920, color=lc(DARK,WHITE,0.05))
    ctxt(d, 'Summer Special Sale — Limited Quantities Available', f_sub, 78, 1920, color=lc(DARK,WHITE,0.3))
    # CTA pill
    d.rounded_rectangle([860,110,1060,148], radius=18, fill=DARK)
    ctxt(d, 'SHOP NOW →', f_cta, 119, 1920, color=WHITE)
    save(img, 'banner_strip2.jpg')

# ── Category Images (400×500) ─────────────────────────────────────────────────
CATEGORIES = [
    ('cat01', 'OUTER', '아우터',      NAVY,  (12, 28, 60)),
    ('cat02', 'TOP',   '상의',        (58,52,45), (38,34,28)),
    ('cat03', 'BOTTOM','하의',        (45,55,42), (28,38,26)),
    ('cat04', 'DRESS', '드레스',      (70,42,48), (48,28,32)),
    ('cat05', 'BAG',   '가방/잡화',   (62,50,35), (42,32,18)),
    ('cat06', 'SALE',  '세일',        (80,25,30), (55,16,18)),
]

def make_category(name, en, ko, c1, c2):
    img = Image.new('RGB', (400, 500))
    vg(img, 0, 500, c1, c2)
    d = ImageDraw.Draw(img)
    # Bottom gradient overlay
    rg(img, 0, 340, 400, 500, lc(c2,BLACK,0.3), lc(c2,BLACK,0.7))
    d = ImageDraw.Draw(img)
    # Draw mini product in center
    tmp = Image.new('RGB', (800,1000), lc(c1,c2,0.5))
    dtmp = ImageDraw.Draw(tmp)
    if en == 'OUTER':   draw_coat(dtmp, 400, lc(c1,WHITE,0.4), 'coat')
    elif en == 'TOP':   draw_shirt(dtmp, 400, lc(c1,WHITE,0.55), 'v')
    elif en == 'BOTTOM':draw_pants(dtmp, 400, lc(c1,WHITE,0.45), 'straight')
    elif en == 'DRESS': draw_dress(dtmp, 400, lc(c1,WHITE,0.55), 'v', 'midi')
    elif en == 'BAG':   draw_bag(dtmp, 400)
    else:               draw_dress(dtmp, 400, lc((200,60,70),WHITE,0.4), 'slip', 'mini')
    mini = tmp.resize((200, 250), Image.LANCZOS)
    img.paste(mini, (100, 55))
    # Text
    f_en = gfe(26, True)
    f_ko = gfk(16)
    ctxt(d, en, f_en, 360, 400, color=WHITE)
    ctxt(d, ko, f_ko, 396, 400, color=lc(WHITE,c2,0.4))
    # Hover arrow
    d.polygon([(195,464),(205,456),(215,464)], fill=lc(WHITE,c2,0.5))
    save(img, f'{name}.jpg')

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print('\n[POZE 2026] Generating website images...\n')

    print('── Hero Images ──────────────────────')
    make_hero1()
    make_hero2()
    make_hero3()

    print('\n── Strip Banners ────────────────────')
    make_banner_strip1()
    make_banner_strip2()

    print('\n── Category Thumbnails ──────────────')
    for args in CATEGORIES:
        make_category(*args)

    print('\n── Product Thumbnails (600×600) ─────')
    for p in PRODUCTS:
        make_product_thumb(p)

    print('\n── Product Detail Images (800×3000) ─')
    for p in PRODUCTS:
        make_product_detail(p)

    print(f'\n✅  All {3+2+6+len(PRODUCTS)+len(PRODUCTS)} images generated in ./images/')

if __name__ == '__main__':
    main()
