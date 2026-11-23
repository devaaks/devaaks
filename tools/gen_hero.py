"""Generate the animated hero SVG: an HHKB-style keyboard with a terminal on it.

One loop (LOOP seconds), no JS, fonts embedded as subset woff2.
Static attributes = the payoff frame, so reduced motion shows the result.
"""
import base64, io, sys
from fontTools import subset
from fontTools.ttLib import TTFont

OUT = sys.argv[1] if len(sys.argv) > 1 else "assets/hero.svg"
LOOP = 8.6

# ---------- content ----------
HANDLE = "devaaks"
OUTPUT = [  # (key, value)
    ("name", "Ashish Singh"),
    ("role", "Full-stack engineer / Engineering lead · 10+ years"),
    ("career", "seed-stage startup · early funding"),
    ("", "→ growth startup · revenue from thousands to millions"),
    ("", "→ enterprise · #1 on the Fortune 500 list"),
    ("worked with", "teams in the US, Berlin, Toronto, Montreal & India"),
    ("industries", "payments · retail · AdTech · EdTech · AgTech"),
    ("", "aviation · market intelligence"),
    ("builds", "AI apps, agents & workflows · distributed systems"),
    ("", "web apps (front end + back end) · mobile & desktop apps"),
    ("", "browser extensions"),
    ("open to", "Staff Engineer · AI Engineer · Founding Engineer"),
]
TITLE = "devaaks — zsh"

# ---------- tokens ----------
C = dict(
    ground="#16171a", ground_edge="#ffffff12",
    case_top="#d8d1c1", case_bot="#c6bfae", case_hi="#e6e0d2", plate="#aea797",
    alpha_t0="#f2ede1", alpha_t1="#e5dfcf", alpha_sk="#c4bdab", alpha_ink="#2b2a26",
    mod_t0="#8a8579", mod_t1="#7a756a", mod_sk="#5d594f", mod_ink="#f5f1e8", mod_sub="#d9d3c6",
    hit_t0="#38a6b3", hit_t1="#2a8d9a", hit_sk="#1d6871", hit_ink="#f3fbfc",
    term="#1c1d21", term_bar="#212226", term_line="#ffffff10", term_edge="#ffffff17",
    t_ink="#ececee", t_dim="#8a8e96", t_faint="#5c6068", t_accent="#4fc3d0", caret="#d9dbe0",
)
SANS, SANS_B, MONO = "GeistK", "GeistKB", "GeistM"

# ---------- geometry ----------
W, H = 880, 480
G = 48
U = 50.0
KX, KW = 48, 784
PAD = (KW - 15 * U) / 2  # 17
TW, TX, TY = 640, 120, G
FS, LH = 14, 23
TITLE_H = 34
BODY_PT = 18
TH = TITLE_H + BODY_PT + (len(OUTPUT) + 2) * LH + 14
KY = TY + TH - 25 - PAD   # terminal bottom lands mid-row-1
X0, Y0 = KX + PAD, KY + PAD
H = int(Y0 + 4 * U + 30)  # bottom row shows 60%, then the crop
ADV = FS * 0.6            # Geist Mono advance

# HHKB rows: (label, width_u, tone, tool, key-id)
ROWS = [
    [("esc", 1, "mod", None, "esc")] + [(c, 1, "alpha", None, c) for c in "1234567890-="] +
    [("\\", 1, "alpha", None, "bs"), ("`", 1, "alpha", None, "bt")],
    [("tab", 1.5, "mod", "Node.js", "tab")] + [(c, 1, "alpha", None, c.lower()) for c in "QWERTYUIOP[]"] +
    [("delete", 1.5, "mod", "React", "del")],
    [("control", 1.75, "mod", None, "ctrl")] + [(c, 1, "alpha", None, c.lower()) for c in "ASDFGHJKL;'"] +
    [("return", 2.25, "mod", None, "ret")],
    [("shift", 2.25, "mod", "TypeScript", "lsh")] + [(c, 1, "alpha", None, c.lower()) for c in "ZXCVBNM,./"] +
    [("shift", 1.75, "mod", "Python", "rsh"), ("fn", 1, "mod", "AWS", "fn")],
    [(None, 1.5, "gap", None, "g1"), ("", 1, "mod", None, "lalt"), ("", 1.5, "mod", None, "lcmd"),
     ("", 6, "alpha", None, "space"), ("", 1.5, "mod", None, "rcmd"), ("", 1, "mod", None, "ralt"),
     (None, 1.5, "gap", None, "g2")],
]
HIT = set("devaks")

# ---------- timeline (seconds) ----------
CTRL = (1.20, 1.66)
LKEY = (1.32, 1.56)
CLEAR = 1.34
TYPE = [1.80, 1.97, 2.12, 2.32, 2.47, 2.69, 2.85]
RET = (3.30, 3.44)
SWAP = 3.34
OUT0, OUT_STEP, OUT_DUR = 3.40, 0.07, 0.5
NEWPROMPT = OUT0 + len(OUTPUT) * OUT_STEP + 0.12
PRESS = 0.11  # how long a typed key stays down

def pct(t):
    return f"{max(0.0, min(100.0, t / LOOP * 100)):.3f}%"

TRAVEL = "cubic-bezier(.45,0,.1,1)"
ARRIVE = "cubic-bezier(.25,.8,.25,1)"
css_anims = []

def keyframes(name, stops):
    """stops: list of (t, decl, easing_to_next or None)."""
    body = []
    for t, decl, ease in stops:
        e = f"animation-timing-function:{ease};" if ease else ""
        body.append(f"{pct(t)}{{{decl};{e}}}")
    css_anims.append(f"@keyframes {name}{{{''.join(body)}}}")

# ---------- fonts ----------
def font_face(path, family, text):
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern"]
    opts.name_IDs = []; opts.notdef_outline = True
    f = TTFont(path); s = subset.Subsetter(opts); s.populate(text=text); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{family};src:url(data:font/woff2;base64,{b64}) format('woff2');}}"

legend_text = "".join(sorted(set("".join(str(k[0] or "") for r in ROWS for k in r) + "ABCDEFGHIJKLMNOPQRSTUVWXYZ" + TITLE)))
tool_text = "".join(sorted(set("".join(str(k[3] or "") for r in ROWS for k in r))))
mono_text = "".join(sorted(set("~$" + HANDLE + "".join(a + b for a, b in OUTPUT) + "▌ ")))

# ---------- svg parts ----------
defs, back, front = [], [], []

def grad(id_, a, b):
    defs.append(f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient>')

grad("gAlpha", C["alpha_t0"], C["alpha_t1"])
grad("gMod", C["mod_t0"], C["mod_t1"])
grad("gHit", C["hit_t0"], C["hit_t1"])
grad("gCase", C["case_top"], C["case_bot"])
defs.append('<filter id="fCase" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="18" stdDeviation="18" flood-color="#000" flood-opacity=".55"/></filter>')
defs.append('<filter id="fTerm" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="1" stdDeviation="1" flood-color="#000" flood-opacity=".35"/><feDropShadow dx="0" dy="16" stdDeviation="16" flood-color="#000" flood-opacity=".45"/></filter>')
defs.append(f'<clipPath id="cStage"><rect width="{W}" height="{H}" rx="16"/></clipPath>')

def press_anim(kid, windows):
    """Key travel for a list of (down, up) windows."""
    stops = [(0, "transform:translateY(0)", None)]
    for d, u in windows:
        stops += [(d - 0.001, "transform:translateY(0)", "ease-out"), (d + 0.04, "transform:translateY(2.2px)", None),
                  (u, "transform:translateY(2.2px)", "ease-out"), (u + 0.09, "transform:translateY(0)", None)]
    stops.append((LOOP, "transform:translateY(0)", None))
    keyframes(f"p_{kid}", stops)
    lit = [(0, "opacity:0", None)]
    for d, u in windows:
        lit += [(d - 0.001, "opacity:0", None), (d + 0.03, "opacity:1", None), (u, "opacity:1", "ease-out"), (u + 0.16, "opacity:0", None)]
    lit.append((LOOP, "opacity:0", None))
    keyframes(f"l_{kid}", lit)
    return f".k-{kid} .cap{{animation:p_{kid} {LOOP}s infinite}} .k-{kid} .lit{{animation:l_{kid} {LOOP}s infinite}}"

presses = {}
for i, ch in enumerate(HANDLE):
    presses.setdefault(ch, []).append((TYPE[i], TYPE[i] + PRESS))
presses["ctrl"] = [CTRL]
presses["l"] = [LKEY]
presses["ret"] = [RET]
key_css = [press_anim(k, v) for k, v in presses.items()]

# keyboard case + plate
back.append(f'<g filter="url(#fCase)"><rect x="{KX}" y="{KY}" width="{KW}" height="{PAD*2+5*U+40}" rx="20" fill="url(#gCase)"/></g>')
back.append(f'<rect x="{KX+1}" y="{KY+1}" width="{KW-2}" height="40" rx="19" fill="none" stroke="{C["case_hi"]}" stroke-opacity=".7"/>')
back.append(f'<rect x="{X0-3}" y="{Y0-3}" width="{15*U+6}" height="{4*U+6}" rx="8" fill="{C["plate"]}"/>')
back.append(f'<rect x="{X0+1.5*U-3}" y="{Y0+3*U}" width="{12*U+6}" height="{2*U+3}" rx="8" fill="{C["plate"]}"/>')

def key(x, y, w, label, tone, tool, kid):
    cx, cy, cw, ch = x + 2.5, y + 2.5, w - 5, U - 5
    tx, ty, tw, th = cx + 5, cy + 3, cw - 10, ch - 10
    g = [f'<g class="k k-{kid}">',
         f'<rect x="{cx}" y="{cy+1.5}" width="{cw}" height="{ch}" rx="6.5" fill="#000" fill-opacity=".22"/>',
         '<g class="cap">',
         f'<rect x="{cx}" y="{cy}" width="{cw}" height="{ch}" rx="6.5" fill="{C[tone+"_sk"]}"/>',
         f'<rect x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="4.5" fill="url(#g{tone.capitalize()})"/>']
    if kid in presses:
        lit_fill = "#7fe3ee" if tone == "hit" else C["hit_t0"]
        lit_op = ".45" if tone == "hit" else ".9"
        g.append(f'<rect class="lit" x="{tx}" y="{ty}" width="{tw}" height="{th}" rx="4.5" fill="{lit_fill}" fill-opacity="{lit_op}" opacity="0"/>')
    ink = C[tone + "_ink"]
    if label and tone in ("alpha", "hit"):
        g.append(f'<text x="{tx+6}" y="{ty+14.5}" class="lg" fill="{ink}">{esc(label)}</text>')
    elif label and tone == "mod":
        if tool:
            g.append(f'<text x="{tx+6}" y="{ty+12.5}" class="sub" fill="{C["mod_sub"]}">{esc(label)}</text>')
            g.append(f'<text x="{tx+6}" y="{ty+th-6}" class="tool" fill="{ink}">{esc(tool)}</text>')
        else:
            g.append(f'<text x="{tx+6}" y="{ty+th-6}" class="modl" fill="{ink}">{esc(label)}</text>')
    g.append("</g></g>")
    return "".join(g)

def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

keys_svg = []
for r, row in enumerate(ROWS):
    x = X0
    for label, wu, tone, tool, kid in row:
        w = wu * U
        if tone != "gap":
            t = "hit" if (tone == "alpha" and len(label) == 1 and label.lower() in HIT and kid in HIT) else tone
            keys_svg.append(key(x, Y0 + r * U, w, label, t, tool, kid))
        x += w
back.append("".join(keys_svg))

# ---------- terminal ----------
term = []
term.append(f'<g filter="url(#fTerm)"><rect x="{TX}" y="{TY}" width="{TW}" height="{TH}" rx="12" fill="{C["term"]}"/></g>')
term.append(f'<path d="M{TX} {TY+TITLE_H} V{TY+12} a12 12 0 0 1 12 -12 H{TX+TW-12} a12 12 0 0 1 12 12 V{TY+TITLE_H} Z" fill="{C["term_bar"]}"/>')
term.append(f'<line x1="{TX}" y1="{TY+TITLE_H+.5}" x2="{TX+TW}" y2="{TY+TITLE_H+.5}" stroke="{C["term_line"]}"/>')
term.append(f'<rect x="{TX+.5}" y="{TY+.5}" width="{TW-1}" height="{TH-1}" rx="11.5" fill="none" stroke="{C["term_edge"]}"/>')
for i, col in enumerate(("#ff5f57", "#febc2e", "#28c840")):
    term.append(f'<circle cx="{TX+18+i*20}" cy="{TY+TITLE_H/2}" r="6" fill="{col}"/>')
term.append(f'<text x="{TX+TW/2}" y="{TY+TITLE_H/2+4.5}" text-anchor="middle" class="ttl" fill="{C["t_dim"]}">{esc(TITLE)}</text>')

BX = TX + 20
def ly(i):  # baseline of body line i
    return TY + TITLE_H + BODY_PT + i * LH + FS * 0.72

PROMPT_W = 4 * ADV  # "~ $ "
def prompt(y):
    return (f'<text x="{BX}" y="{y}" class="m" fill="{C["t_faint"]}">~</text>'
            f'<text x="{BX+2*ADV}" y="{y}" class="mb" fill="{C["t_accent"]}">$</text>')

def chars(y, cls=""):
    return "".join(f'<text x="{BX+PROMPT_W+i*ADV:.2f}" y="{y}" class="m c{i} {cls}" fill="{C["t_ink"]}">{ch}</text>'
                   for i, ch in enumerate(HANDLE))

top_y, bot_y = ly(0), ly(len(OUTPUT) + 1)
lift = bot_y - top_y

# line A: the finished command at the top (payoff)
term.append(f'<g class="la">{prompt(top_y)}{chars(top_y)}</g>')
# output lines
for i, (k, v) in enumerate(OUTPUT):
    y = ly(i + 1)
    xv = BX + 12 * ADV
    vv = esc(v).replace("→", f'<tspan fill="{C["t_dim"]}">→</tspan>').replace("·", f'<tspan fill="{C["t_dim"]}">·</tspan>')
    term.append(f'<g class="o o{i}"><text x="{BX}" y="{y}" class="m" fill="{C["t_dim"]}">{esc(k)}</text>'
                f'<text x="{xv}" y="{y}" class="m" fill="{C["t_ink"]}">{vv}</text></g>')
# line B: the live prompt (bottom at rest, slides to top on clear, types)
caret = f'<rect class="caret" x="{BX+PROMPT_W}" y="{bot_y-FS*0.78}" width="{ADV}" height="{FS*1.05}" fill="{C["caret"]}"/>'
term.append(f'<g class="lb"><g class="lbm">{prompt(bot_y)}<g class="typed">{chars(bot_y, "t")}</g>{caret}</g></g>')
front.append("".join(term))

# ---------- animations ----------
anim_css = list(key_css)
# line A + outputs: visible, fade on clear, return after Enter
def out_stops(t_in):
    return [(0, "opacity:1;transform:translateY(0)", None),
            (CLEAR + 0.0, "opacity:1;transform:translateY(0)", "ease-in"),
            (CLEAR + 0.16, "opacity:0;transform:translateY(-6px)", None),
            (t_in - 0.001, "opacity:0;transform:translateY(5px)", ARRIVE),
            (t_in + OUT_DUR, "opacity:1;transform:translateY(0)", None),
            (LOOP, "opacity:1;transform:translateY(0)", None)]

keyframes("la", [(0, "opacity:1", None), (CLEAR, "opacity:1", "ease-in"), (CLEAR + .16, "opacity:0", None),
                 (SWAP - .001, "opacity:0", None), (SWAP, "opacity:1", None), (LOOP, "opacity:1", None)])
anim_css.append(f".la{{animation:la {LOOP}s infinite}}")
for i in range(len(OUTPUT)):
    keyframes(f"o{i}", out_stops(OUT0 + i * OUT_STEP))
    anim_css.append(f".o{i}{{animation:o{i} {LOOP}s infinite}}")
# line B: slide up on clear, vanish on swap, reappear at bottom as the new prompt
keyframes("lb", [(0, "opacity:1;transform:translateY(0)", None),
                 (CLEAR + .02, "opacity:1;transform:translateY(0)", TRAVEL),
                 (CLEAR + .42, f"opacity:1;transform:translateY(-{lift}px)", None),
                 (SWAP - .001, f"opacity:1;transform:translateY(-{lift}px)", None),
                 (SWAP, "opacity:0;transform:translateY(0)", None),
                 (NEWPROMPT, "opacity:0;transform:translateY(4px)", ARRIVE),
                 (NEWPROMPT + .35, "opacity:1;transform:translateY(0)", None),
                 (LOOP, "opacity:1;transform:translateY(0)", None)])
anim_css.append(f".lb{{animation:lb {LOOP}s infinite}}")
# typed chars on line B
for i, t in enumerate(TYPE):
    keyframes(f"t{i}", [(0, "opacity:0", None), (t + .02, "opacity:0", None), (t + .021, "opacity:1", None),
                        (SWAP, "opacity:1", None), (SWAP + .001, "opacity:0", None), (LOOP, "opacity:0", None)])
    anim_css.append(f".typed .c{i}{{animation:t{i} {LOOP}s step-end infinite}}")
# caret: x steps while typing, blink when idle
cx = [(0, 0)] + [(t + .021, i + 1) for i, t in enumerate(TYPE)] + [(SWAP + .001, 0)]
blink_spans = [(0, CTRL[0]), (NEWPROMPT, LOOP)]
stops, t = [], 0.0
events = sorted({0.0, LOOP, *[a for a, _ in cx]} | {round(x, 3) for a, b in blink_spans for x in [a, b]})
# sample on a 0.53s blink grid inside idle spans
grid = set(events)
for a, b in blink_spans:
    x = a
    while x < b:
        grid.add(round(x, 3)); x += 0.53
for tt in sorted(grid):
    pos = ([p for a, p in sorted(cx) if a <= tt + 1e-6] or [0])[-1]
    idle = next(((a, b) for a, b in blink_spans if a <= tt < b), None)
    on = 1 if idle is None else (1 if int((tt - idle[0]) / 0.53 + 1e-6) % 2 == 0 else 0)
    stops.append((tt, f"opacity:{on};transform:translateX({pos*ADV:.2f}px)", None))
keyframes("caret", stops)
anim_css.append(f".caret{{animation:caret {LOOP}s step-end infinite}}")

style = "".join([
    font_face("tools/fonts/Geist-Medium.ttf", SANS, legend_text + "abcdefghijklmnopqrstuvwxyz"),
    font_face("tools/fonts/Geist-SemiBold.ttf", SANS_B, tool_text),
    font_face("tools/fonts/GeistMono-Regular.ttf", MONO, mono_text),
    f".lg{{font:500 13px {SANS},system-ui,sans-serif}}",
    f".sub{{font:500 10px {SANS},system-ui,sans-serif}}",
    f".modl{{font:500 11px {SANS},system-ui,sans-serif}}",
    f".tool{{font:600 11.5px {SANS_B},system-ui,sans-serif}}",
    f".ttl{{font:500 12px {SANS},system-ui,sans-serif}}",
    f".m,.mb{{font:400 {FS}px {MONO},ui-monospace,Menlo,Consolas,monospace;white-space:pre}}",
    "text{text-rendering:geometricPrecision}",
    ".cap,.la,.lb,.o,.caret{transform-box:view-box}",
    "@media (prefers-reduced-motion:no-preference){" + "".join(anim_css) + "}",
    "".join(css_anims),
])

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-labelledby="t d">
<title id="t">devaaks: a keyboard types my handle into a terminal</title>
<desc id="d">Ashish Singh. Full-stack engineer and engineering lead, 10+ years. Career: a seed-stage startup in its early funding, then a growth startup whose revenue grew from thousands to millions, then an enterprise that is #1 on the Fortune 500 list. Worked with teams in the US, Berlin, Toronto, Montreal and India. Industries: payments, retail, AdTech, EdTech, AgTech, aviation and market intelligence. Builds AI apps, agents and workflows, distributed systems, web apps (front end and back end), mobile and desktop apps, and browser extensions. Open to Staff Engineer, AI Engineer and Founding Engineer roles.</desc>
<style>{style}</style>
<defs>{''.join(defs)}</defs>
<g clip-path="url(#cStage)">
<rect width="{W}" height="{H}" fill="{C["ground"]}"/>
{''.join(back)}
{''.join(front)}
</g>
<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="15.5" fill="none" stroke="{C["ground_edge"]}"/>
</svg>'''
open(OUT, "w").write(svg)
print(OUT, len(svg) // 1024, "KB", "H", H, "KY", KY, "TH", TH)
