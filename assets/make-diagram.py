"""Draws rules.svg: one session where the operator corrects the model three times, the rule mentor proposes, and the next session.

Usage: python make-diagram.py <JetBrainsMono-Regular.ttf> <JetBrainsMono-Bold.ttf>   (needs fontTools)
The font is embedded as a subset, so the image looks the same everywhere.
"""
import base64, io, os, sys
from fontTools import subset
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
BG, W, L, M, D = "#0a0907", "#f0f4f8", "#b3d1eb", "#71a7d6", "#4d7ba8"
TXT, DIM = "#cfc6b4", "#8a7a5c"

def font(path, weight):
    opts = subset.Options(); opts.layout_features = []; opts.name_IDs = []
    f = TTFont(path); s = subset.Subsetter(opts)
    s.populate(unicodes=list(range(0x20, 0x7f)) + [0xB7, 0x2192, 0x2191, 0x2193, 0x2013]); s.subset(f)
    b = io.BytesIO(); f.save(b)
    return f"@font-face {{ font-family: JBM; font-weight: {weight}; src: url(data:font/ttf;base64,{base64.b64encode(b.getvalue()).decode()}) format('truetype'); }}"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def logo(x, y, u):
    R = lambda a, b, w, h, c: f'<rect x="{x+a*u:.1f}" y="{y+(b-4)*u:.1f}" width="{w*u:.1f}" height="{h*u:.1f}" fill="{c}"/>'
    o = R(0, 4, 16, 1, M) + R(0, 17, 16, 1, M) + R(0, 4, 1, 14, M) + R(15, 4, 1, 14, M)
    o += R(2.5, 7, 4, 1, L) + R(9.5, 7, 4, 1, L) + R(3.5, 9, 2.5, 2, M) + R(10, 9, 2.5, 2, M) + R(5, 13, 6, 1, D)
    o += R(3, 14, 10, 1, L) + R(4, 15, 8, 1, L) + R(5, 16, 6, 1, L) + R(6, 17, 4, 2, L)
    return o

def chamfer(x, y, w, h, c=14): return f"M{x+c} {y} H{x+w} V{y+h-c} L{x+w-c} {y+h} H{x} V{y+c} Z"

# kinds: you = operator, bad = model got it wrong, ok = model got it right, rule, t = plain text
PANELS = [
    ("1", "THIS SESSION", "What did you have to explain?", D, [
        ("you", "you    Add an Invoice model."),
        ("bad", "model  Created src/Invoice.php."),
        ("you", "you    No, models go in the model folder."),
        ("bad", "model  Moved it to src/model/Invoice.php."),
        ("you", "you    Not src. The module's own model/ folder."),
        ("bad", "model  Moved it to Billing/Model/Invoice.php."),
        ("you", "you    Lowercase: model/, not Model/."),
        ("ok",  "model  Moved it to Billing/model/Invoice.php.")]),
    ("2", "MENTOR", "What should have been said upfront?", M, [
        ("rule", "Models go in the module's lowercase model/ folder, not in src/."),
        ("t", "Why: you corrected it three times in this session."),
        ("t", "Goes to: Billing/AGENTS.md. You pick: apply, edit, skip.")]),
    ("3", "NEXT SESSION", "Does it hold?", L, [
        ("you", "you    Add a Payment model."),
        ("ok",  "model  Created Billing/model/Payment.php."),
        ("t", "No corrections.")]),
]
CLS = {"you": "you", "bad": "bad", "ok": "ok", "rule": "rule", "t": "body"}

def build(css):
    Wd, x0, lab = 1280, 40, 370
    o = logo(x0, 28, 3.6) + f'<text x="{x0+80}" y="66" class="title">Three corrections become one sentence.</text>'
    y = 130
    for i, (n, name, q, col, lines) in enumerate(PANELS):
        h = max(84, 40 + len(lines) * 30)
        o += f'<path d="{chamfer(x0, y, Wd-2*x0, h)}" fill="none" stroke="{col}" stroke-width="1.6"/>'
        o += f'<text x="{x0+24}" y="{y+36}" class="num" fill="{col}">{n}</text>'
        o += f'<text x="{x0+60}" y="{y+34}" class="lvl" fill="{col}">{name}</text>'
        o += f'<text x="{x0+60}" y="{y+58}" class="q">{esc(q)}</text>'
        for k, (kind, s) in enumerate(lines):
            o += f'<text x="{x0+lab+20}" y="{y+34+k*30}" class="{CLS[kind]}" xml:space="preserve">{esc(s)}</text>'
        y += h + 22
        if i == 1:
            y += 30
            o += f'<line x1="{x0}" y1="{y}" x2="{Wd-x0}" y2="{y}" stroke="{M}" stroke-width="2" stroke-dasharray="10 6"/>'
            o += f'<text x="{x0}" y="{y-12}" class="edge">↑ this session: you explained it, mentor wrote it down</text>'
            o += f'<text x="{x0}" y="{y+28}" class="edge">↓ next session: the rule is there from the start</text>'
            y += 58
    H = y + 10
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {Wd} {H}" width="{Wd}" height="{H}" role="img" '
            f'aria-label="Three corrections become one sentence. In this session you corrected where models go three times. Mentor proposes one rule: models go in the module model folder, not in src, to Billing/AGENTS.md, and you approve it. In the next session the model gets it right the first time.">'
            f'<style>{css}</style><rect width="{Wd}" height="{H}" fill="{BG}"/>{o}</svg>')

css = font(sys.argv[1], 400) + font(sys.argv[2], 700) + f"""
text {{ font-family: JBM, ui-monospace, monospace; }}
.title {{ font-size: 26px; fill: #f3ead8; }}
.num {{ font-size: 30px; font-weight: 700; }}
.lvl {{ font-size: 15px; letter-spacing: 2px; font-weight: 700; }}
.q {{ font-size: 14px; fill: {DIM}; }}
.body {{ font-size: 17px; fill: {TXT}; }}
.you {{ font-size: 17px; fill: {W}; }}
.bad {{ font-size: 17px; fill: {DIM}; }}
.ok {{ font-size: 17px; fill: {L}; }}
.rule {{ font-size: 17px; fill: {M}; font-weight: 700; }}
.edge {{ font-size: 15px; fill: {M}; }}
"""
open(os.path.join(HERE, "rules.svg"), "w").write(build(css))
print("ok")
