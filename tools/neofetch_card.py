#!/usr/bin/env python3
"""Build a neofetch-style card: ASCII face (left) + colored stats (right) as one SVG + PNG preview."""
import sys, html
from PIL import Image, ImageDraw, ImageFont, ImageEnhance

SRC = "/Users/noahsabbavarapu/Downloads/OneMediaCo_HB 261_resize _Original.jpg"
OUT = sys.argv[1] if len(sys.argv) > 1 else "card"

# --- face params (v3, locked) ---
COLS = int(sys.argv[3]) if len(sys.argv) > 3 else 220
SAT, CON, BRT, BGT = 1.3, 1.35, 1.22, 12
RAMP = " .:-=+*#%@"
FONT_PATH = "/System/Library/Fonts/Menlo.ttc"

# --- theme ---
BG      = "#0d1117"
GREEN   = "#39d353"   # accent (matches 3D night-green graph)
WHITE   = "#e6edf3"
GREY    = "#8b949e"
SEP     = "#30363d"

# --- stats content ---
TITLE_L, TITLE_R = "noah", "sabbavarapu"
STATS = [
    ("OS",        "macOS 26 Tahoe"),
    ("Host",      "Stanford University #GoCardinal"),
    ("Kernel",    "Computer Engineering"),
    ("Shell",     "AI/ML Engineer"),
    ("Location",  "Austin, TX"),
    ("Languages", "Python, C/C++, Verilog, Dart, TS"),
    ("ML Stack",  "PyTorch, QLoRA, GRPO, vLLM"),
    ("Focus",     "LLM post-training, agent evals"),
    ("Hobbies",   "<fill in>"),
]
KEYW = max(len(k) for k, _ in STATS)
BLOCKS = ["#0d1117", "#f85149", "#39d353", "#d29922",
          "#58a6ff", "#bc8cff", "#39c5cf", "#e6edf3"]

# ---------- build face grid ----------
img = Image.open(SRC).convert("RGB")
# auto-crop away the black margins so the face fills the frame
_g = img.convert("L").point(lambda p: 255 if p > 24 else 0)
_bb = _g.getbbox()
if _bb:
    pad = 8
    l, t, r, b = _bb
    img = img.crop((max(0, l-pad), max(0, t-pad),
                    min(img.width, r+pad), min(img.height, b+pad)))
img = ImageEnhance.Brightness(img).enhance(BRT)
img = ImageEnhance.Contrast(img).enhance(CON)
img = ImageEnhance.Color(img).enhance(SAT)
w, h = img.size
rows = max(1, int(COLS * (h / w) * 0.55))
small = img.resize((COLS, rows), Image.LANCZOS)
gray = small.convert("L")
px, gp = small.load(), gray.load()
grid = []
for y in range(rows):
    line = []
    for x in range(COLS):
        b = gp[x, y]
        line.append((RAMP[int(b/255*(len(RAMP)-1))], px[x, y]) if b >= BGT else (" ", None))
    grid.append(line)

# ---------- geometry ----------
FF = 11          # face font size (hi-res; GitHub downsamples smoothly)
fadv, flh = FF*0.6, FF*1.12
face_w, face_h = COLS*fadv, rows*flh

SF = 46          # stats font size
sadv, slh = SF*0.6, SF*1.6
stats_lines = 2 + len(STATS) + 2      # title, sep, stats, blank, blocks
stats_h = stats_lines*slh
stats_w = max(len(f"{k.ljust(KEYW)}   {v}") for k, v in STATS) * sadv
stats_w = max(stats_w, (len(TITLE_L)+1+len(TITLE_R))*sadv)

LAYOUT = sys.argv[2] if len(sys.argv) > 2 else "side"   # "side" or "stack"
M, GAP = 40, 70
if LAYOUT == "stack":
    content_w = max(face_w, stats_w)
    face_x = M + (content_w - face_w)/2
    face_y = M
    stats_x = M + (content_w - stats_w)/2
    stats_y = face_y + face_h + GAP
    SVGW = M + content_w + M
    SVGH = stats_y + stats_h + M
else:
    face_x, face_y = M, M
    stats_x = face_x + face_w + GAP
    stats_y = face_y + max(0, (face_h - stats_h)/2)   # vertically center stats to face
    SVGW = stats_x + stats_w + M
    SVGH = M + max(face_h, stats_h) + M

# ---------- PNG preview ----------
canvas = Image.new("RGB", (int(SVGW), int(SVGH)), BG)
d = ImageDraw.Draw(canvas)
fface = ImageFont.truetype(FONT_PATH, FF)
fstat = ImageFont.truetype(FONT_PATH, SF)
fbold = ImageFont.truetype(FONT_PATH, SF)
# face
for y, line in enumerate(grid):
    for x, (ch, col) in enumerate(line):
        if col:
            d.text((face_x + x*fadv, face_y + y*flh), ch, font=fface, fill=col)
# stats
def hexc(c): return c
cy = stats_y
d.text((stats_x, cy), TITLE_L, font=fbold, fill=GREEN)
d.text((stats_x + len(TITLE_L)*sadv, cy), "@", font=fstat, fill=WHITE)
d.text((stats_x + (len(TITLE_L)+1)*sadv, cy), TITLE_R, font=fbold, fill=GREEN)
cy += slh
d.text((stats_x, cy), "─"*int(stats_w/sadv), font=fstat, fill=SEP)
cy += slh
for k, v in STATS:
    d.text((stats_x, cy), k, font=fbold, fill=GREEN)
    d.text((stats_x + (KEYW+3)*sadv, cy), v, font=fstat, fill=WHITE)
    cy += slh
cy += slh
bx = stats_x
for c in BLOCKS:
    d.rectangle([bx, cy, bx+SF*1.4, cy+SF*0.9], fill=c, outline=SEP)
    bx += SF*1.5
canvas.save(OUT + ".png")

# ---------- SVG ----------
def esc(s): return html.escape(s)
P = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{SVGW:.0f}" height="{SVGH:.0f}" '
     f'viewBox="0 0 {SVGW:.0f} {SVGH:.0f}" font-family="Menlo, \'Courier New\', monospace" '
     f'xml:space="preserve">',
     f'<rect width="100%" height="100%" rx="10" fill="{BG}"/>']
# face
P.append(f'<g font-size="{FF}">')
for y, line in enumerate(grid):
    yy = face_y + (y+0.85)*flh
    spans, rt, rc, rx = [], "", None, None
    def flush():
        global spans, rt, rc, rx
        if rt.strip(" ") and rc:
            col_hex = "#%02x%02x%02x" % rc
            spans.append(f'<tspan x="{rx:.1f}" fill="{col_hex}">{esc(rt)}</tspan>')
    for x, (ch, col) in enumerate(line):
        if col == rc and rt != "":
            rt += ch
        else:
            flush(); rt, rc, rx = ch, col, face_x + x*fadv
    flush()
    if spans:
        P.append(f'<text y="{yy:.1f}">' + "".join(spans) + "</text>")
P.append("</g>")
# stats
P.append(f'<g font-size="{SF}">')
ty = stats_y + SF
P.append(f'<text x="{stats_x:.0f}" y="{ty:.0f}"><tspan fill="{GREEN}" font-weight="bold">{TITLE_L}</tspan>'
         f'<tspan fill="{WHITE}">@</tspan><tspan fill="{GREEN}" font-weight="bold">{TITLE_R}</tspan></text>')
ty += slh
P.append(f'<text x="{stats_x:.0f}" y="{ty:.0f}" fill="{SEP}">{"─"*int(stats_w/sadv)}</text>')
ty += slh
for k, v in STATS:
    kx = stats_x
    vx = stats_x + (KEYW+3)*sadv
    P.append(f'<text y="{ty:.0f}"><tspan x="{kx:.0f}" fill="{GREEN}" font-weight="bold">{esc(k)}</tspan>'
             f'<tspan x="{vx:.0f}" fill="{WHITE}">{esc(v)}</tspan></text>')
    ty += slh
ty += slh
bx = stats_x
for c in BLOCKS:
    P.append(f'<rect x="{bx:.0f}" y="{ty-SF:.0f}" width="{SF*1.4:.0f}" height="{SF*0.9:.0f}" fill="{c}" stroke="{SEP}"/>')
    bx += SF*1.5
P.append("</g></svg>")
open(OUT + ".svg", "w").write("\n".join(P))
print(f"face grid {COLS}x{rows} | card {SVGW:.0f}x{SVGH:.0f}px")
print(f"{OUT}.png / {OUT}.svg")
