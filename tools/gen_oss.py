"""Two open-source cards, one SVG each, in the hero's figure language."""
import base64, io, re
from fontTools import subset
from fontTools.ttLib import TTFont

OCT = "tools/node_modules/@primer/octicons/build/svg/"
def icon(name, x, y, fill):
    d = re.findall(r' d="([^"]+)"', open(OCT + name + "-16.svg").read())
    return f'<g transform="translate({x} {y})" fill="{fill}">' + "".join(f'<path d="{p}"/>' for p in d) + "</g>"

CARDS = [
    dict(out="assets/oss-openchamber.svg", owner="openchamber/", name="openchamber", stars="13.2k",
         desc=["A workspace where AI agents write and edit", "code alongside developers."],
         pr="#6675", title="Draw SVG fences as images in the Markdown preview"),
    dict(out="assets/oss-mathesar.svg", owner="mathesar-foundation/", name="mathesar", stars="5.2k",
         desc=["Lets anyone work with a Postgres database", "as easily as a spreadsheet."],
         pr="#4346", title="Set the default time type in the new column form"),
]
C = dict(ground="#16171a", edge="#ffffff14", ink="#ececee", dim="#9a9ea6", faint="#6b6f77", line="#ffffff12",
         merged="#8957e5", star="#e3b341")
W, H, P = 430, 124, 22

def face(path, fam, text):
    o = subset.Options(); o.flavor = "woff2"; o.name_IDs = []; o.layout_features = ["kern"]
    f = TTFont(path); s = subset.Subsetter(o); s.populate(text=text); s.subset(f)
    b = io.BytesIO(); f.flavor = "woff2"; f.save(b)
    return f"@font-face{{font-family:{fam};src:url(data:font/woff2;base64,{base64.b64encode(b.getvalue()).decode()}) format('woff2')}}"

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

GAP = 7  # half the gap between the two cards, as transparent margin
for ci, c in enumerate(CARDS):
    text = c["owner"] + c["name"] + c["stars"] + "".join(c["desc"]) 
    style = (face("tools/fonts/Geist-Medium.ttf", "GM", text) + face("tools/fonts/Geist-SemiBold.ttf", "GS", text) +
             ".r{font:500 13.5px GM,system-ui,sans-serif}.b{font:600 15px GS,system-ui,sans-serif}"
             ".o{font:500 15px GM,system-ui,sans-serif}.s{font:600 12px GS,system-ui,sans-serif}"
             ".t{font:600 14px GS,system-ui,sans-serif}text{text-rendering:geometricPrecision}")
    y_desc = 76
    y_div = y_desc + 19 * (len(c["desc"]) - 1) + 24
    y_pill = y_div + 18
    parts = [
        f'<rect width="{W}" height="{H}" rx="14" fill="{C["ground"]}"/>',
        f'<rect x=".5" y=".5" width="{W-1}" height="{H-1}" rx="13.5" fill="none" stroke="{C["edge"]}"/>',
        icon("repo", P, P + 3, C["dim"]),
        f'<text x="{P+24}" y="{P+16}"><tspan class="o" fill="{C["dim"]}">{esc(c["owner"])}</tspan><tspan class="b" fill="{C["ink"]}">{esc(c["name"])}</tspan></text>',
        f'<text x="{W-P}" y="{P+16}" text-anchor="end" class="r" fill="{C["dim"]}">{c["stars"]}</text>',
        icon("star", W - P - 8.0 * len(c["stars"]) - 20, P + 3, C["star"]),
    ]
    for i, line in enumerate(c["desc"]):
        parts.append(f'<text x="{P}" y="{y_desc + i*19}" class="r" fill="{C["dim"]}">{esc(line)}</text>')
    ox = 0 if ci == 0 else GAP
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W+GAP}" height="{H}" viewBox="0 0 {W+GAP} {H}" role="img">'
           f'<title>{esc(c["owner"]+c["name"])}, {c["stars"]} stars: {esc(" ".join(c["desc"]))}</title>'
           f'<style>{style}</style><g transform="translate({ox} 0)">{"".join(parts)}</g></svg>')
    open(c["out"], "w").write(svg)
    print(c["out"], len(svg) // 1024, "KB")
