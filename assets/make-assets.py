"""Generate the banners and the social preview SVG.

Usage: python make-assets.py <JetBrainsMono-Regular.ttf>   (needs fontTools)
Then render social-preview.svg to social-preview.png at 1280x640, for example with headless Chrome.
"""
import os
import sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

REG = sys.argv[1]
_f = TTFont(REG)
GS = _f.getGlyphSet()
CMAP = _f.getBestCmap()
UPM = _f['head'].unitsPerEm


def text(s, size, x, y, fill, ls=0):
    k = size / UPM
    pen = SVGPathPen(GS, ntos=lambda v: f"{v:.1f}".rstrip("0").rstrip("."))
    for ch in s:
        g = CMAP.get(ord(ch))
        if g is None:
            continue
        GS[g].draw(TransformPen(pen, (k, 0, 0, -k, x, y)))
        x += GS[g].width * k + ls
    return f'<path d="{pen.getCommands()}" fill="{fill}"/>', x


def cham(x, y, w, h, c):
    return f"M{x+c} {y} H{x+w} V{y+h-c} L{x+w-c} {y+h} H{x} V{y+c} Z"


PIX = {
    'm': [".....", ".....", "####.", "#.#.#", "#.#.#", "#.#.#", "#.#.#"],
    'e': [".....", ".....", ".###.", "#...#", "#####", "#....", ".####"],
    'n': [".....", ".....", "####.", "#...#", "#...#", "#...#", "#...#"],
    't': [".#...", ".#...", "####.", ".#...", ".#...", ".#...", "..##."],
    'o': [".....", ".....", ".###.", "#...#", "#...#", "#...#", ".###."],
    'r': [".....", ".....", "#.###", "##...", "#....", "#....", "#...."],
}


def pixel_title(word, x, y, u, fill):
    d = ''
    for c in word:
        g = PIX[c]
        for r, row in enumerate(g):
            cc = 0
            while cc < len(row):
                if row[cc] == '#':
                    e = cc
                    while e < len(row) and row[e] == '#':
                        e += 1
                    d += f'M{x+cc*u:.1f} {y+r*u:.1f}h{(e-cc)*u:.1f}v{u+0.5:.1f}h{-(e-cc)*u:.1f}Z'
                    cc = e
                else:
                    cc += 1
        x += (len(g[0]) + 1.4) * u
    return f'<path d="{d}" fill="{fill}"/>', x


THEMES = {
    'dark': dict(bg="#0a0907", frame="#71a7d6", brow="#b3d1eb", eyes="#71a7d6", mouth="#4d7ba8", beard="#b3d1eb",
                 h1="#f0f4f8", h3="#c9d3dc", tag="#71a7d6", url="#7d8a96"),
    'light': dict(bg=None, frame="#406f9d", brow="#5e86b1", eyes="#406f9d", mouth="#31577d", beard="#5e86b1",
                  h1="#14181c", h3="#3a434c", tag="#406f9d", url="#5a6a7a"),
}


def logo(x, y, u, t):
    # "old master": droid head grid without the antenna, eyebrows, stepped beard; top of the head at y
    R = lambda a, b, w, h, c, cls='': f'<rect class="{cls}" x="{x+a*u:.1f}" y="{y+(b-4)*u:.1f}" width="{w*u:.1f}" height="{h*u:.1f}" fill="{c}"/>'
    o = R(0, 4, 16, 1, t['frame']) + R(0, 17, 16, 1, t['frame']) + R(0, 4, 1, 14, t['frame']) + R(15, 4, 1, 14, t['frame'])
    o += '<g class="brows">' + R(2.5, 7, 4, 1, t['brow']) + R(9.5, 7, 4, 1, t['brow']) + '</g>'
    o += '<g class="eyes">' + R(3.5, 9, 2.5, 2, t['eyes'], 'eye') + R(10, 9, 2.5, 2, t['eyes'], 'eye') + '</g>'
    o += R(5, 13, 6, 1, t['mouth'])
    o += R(3, 14, 10, 1, t['beard']) + R(4, 15, 8, 1, t['beard']) + R(5, 16, 6, 1, t['beard']) + R(6, 17, 4, 2, t['beard'])
    return o


LOGO_W, LOGO_H = 16, 15
H3A = "Turn a Claude Code session into rules"
H3B = "for the model, or lessons for you."
URL = "github.com/xtompie/mentor"
TAGS = ["claude-code", "agentic-engineering", "ai-agents", "context-engineering", "prompt-engineering", "claude-skills"]
ROWS = [TAGS[:3], TAGS[3:]]

CSS = '''
.eye { transform-box: fill-box; transform-origin: center; animation: blink 12s infinite; }
@keyframes blink { 0%,24% { transform: scaleY(1) } 25% { transform: scaleY(.12) } 26%,84% { transform: scaleY(1) } 85% { transform: scaleY(.12) } 86%,100% { transform: scaleY(1) } }
.eyes { animation: look 12s infinite; }
@keyframes look { 0%,32% { transform: translate(0,0) } 35%,54% { transform: translate(-15px,0) } 57%,100% { transform: translate(0,0) } }
.brows { animation: brows 12s infinite; }
@keyframes brows { 0%,62% { transform: translate(0,0) } 65%,78% { transform: translate(0,-8px) } 81%,100% { transform: translate(0,0) } }
@media (prefers-reduced-motion: reduce) { .eye, .eyes, .brows { animation: none; } }
'''


def content(t):
    LU = 15
    lh = LOGO_H * LU
    tx = LOGO_W * LU + 64
    y = 0
    o, _ = pixel_title("mentor", tx, y, 10, t['h1'])
    y += 70 + 50
    p, xa = text(H3A, 24, tx, y, t['h3'])
    o += p
    y += 34
    p, xb = text(H3B, 24, tx, y, t['h3'])
    o += p
    y += 22
    right = max(xa, xb)
    for row in ROWS:
        y += 14
        x = tx
        for tg in row:
            p, x2 = text(tg, 19, x + 13, y + 23, t['tag'])
            w = x2 - x + 13
            o += f'<path d="{cham(x, y, w, 32, 8)}" fill="none" stroke="{t["tag"]}" stroke-opacity=".6" stroke-width="1.4"/>' + p
            x += w + 12
            right = max(right, x)
        y += 32
    y += 40
    p, _ = text(URL, 20, tx, y, t['url'])
    o += p
    hc = y + 6
    return logo(0, (hc - lh) / 2, LU, t) + o, right, hc


def canvas(w, h, theme):
    t = THEMES[theme]
    body, wc, hc = content(t)
    bg = f'<rect width="{w}" height="{h}" fill="{t["bg"]}"/>' if t['bg'] else ''
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
            f'aria-label="mentor. Turn a Claude Code session into rules for the model, or lessons for you.">'
            f'<style>{CSS}</style>{bg}<g transform="translate({(w-wc)/2:.1f} {(h-hc)/2:.1f})">{body}</g></svg>'), hc


_, hc = canvas(1280, 640, 'dark')
BH = int(hc + 120)
out = os.path.dirname(os.path.abspath(__file__)) + '/'
open(out + 'banner-dark.svg', 'w').write(canvas(1280, BH, 'dark')[0])
open(out + 'banner-light.svg', 'w').write(canvas(1280, BH, 'light')[0])
open(out + 'social-preview.svg', 'w').write(canvas(1280, 640, 'dark')[0])
