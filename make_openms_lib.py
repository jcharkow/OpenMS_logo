#!/usr/bin/env python3
"""
Generate the OpenMS-lib sublogo (standard + white) as SVG, programmatically.

How it stays faithful to the main logo
--------------------------------------
* "Open" and "MS" are NOT retyped. Their outlined letter paths are lifted
  verbatim from the official logo SVG (--logo), so the letterforms (incl. the
  customised "n" leg and the +0.5 stroke) are identical to the original.
* "-lib" must be new lettering. It is built from Montserrat Alternates Regular
  (--font), scaled and stroked with parameters *measured from the original
  logo* (Regular glyphs at ~192.2 units, 11.88 units of stroke), so it matches
  the weight of the original wordmark. Text is converted to outlines, so the
  output SVGs need no installed fonts.
* Bars reuse the original bar geometry (width 22.66, pitch 37.41) and the
  brand gradient colours.

Requirements:  pip install fonttools
Font file:     npm i @fontsource/montserrat-alternates   (or any TTF/OTF/WOFF
               of Montserrat Alternates Regular, e.g. from Google Fonts)
Usage:         python make_openms_lib.py --logo openms-logo.svg \
                   --font node_modules/@fontsource/montserrat-alternates/files/montserrat-alternates-latin-400-normal.woff \
                   --out .
"""
import argparse, re, sys
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

# ---- measured from the original logo ---------------------------------------
GLYPH_SIZE   = 192.2     # font size (SVG units) that reproduces the base glyph outlines
STROKE_W     = 11.88     # total stroke width added around each glyph (5.94 per side)
BASELINE_MS  = 462.93    # baseline of "MS" in the original coordinate system
BAR_W, BAR_PITCH, BAR_TOP = 22.66, 37.41, 302.49
BARS_A = (44.08,  [72.54, 107.23, 162.9, 84.77])   # hang under the "O"
BARS_B = (340.18, [46.45, 133.17, 66.86])          # hang under the "e"
DARK = "#231f20"

# ---- parameters you may want to tweak --------------------------------------
LIB_SCALE = 0.62         # size of "-lib" relative to "MS"
LIB_GAP   = 22           # space between "MS" and "-lib"
PAD       = 50           # clear space around the artwork

def extract_letters(logo_svg):
    """The 12 dark (cls-2) paths: [O, O-stroke, p, p-stroke, e, ..., S, S-stroke]."""
    ds = re.findall(r'<path[^>]*class="cls-2"[^>]*\sd="([^"]+)"', logo_svg)
    if len(ds) != 12:
        sys.exit(f"Expected 12 letter paths in the logo, found {len(ds)}")
    return ds

def outline_text(font_path, text, size, x, baseline):
    tt = TTFont(font_path)
    if tt.flavor: tt.flavor = None
    gs, cmap, upm = tt.getGlyphSet(), tt.getBestCmap(), tt["head"].unitsPerEm
    s, cx, parts = size / upm, x, []
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, baseline)))
        parts.append(pen.getCommands())
        cx += gs[g].width * s
    return " ".join(parts), cx

def build(logo_svg, font_path, white=False):
    letters = extract_letters(logo_svg)
    text_fill = "#ffffff" if white else DARK
    lib_c1, lib_c2 = ("#cc51ff", "#7891f1") if white else ("#b503ff", "#3157e9")

    # "-lib": scaled glyphs + proportionally scaled stroke, baseline-aligned with MS
    lib_x = 811.0 + LIB_GAP                       # right edge of the "S" outline + gap
    d_lib, lib_end = outline_text(font_path, "-lib", GLYPH_SIZE * LIB_SCALE, lib_x, BASELINE_MS)
    lib_stroke = STROKE_W * LIB_SCALE

    def bars(x0, heights):
        return "\n    ".join(
            f'<rect x="{x0 + i*BAR_PITCH:.2f}" y="{BAR_TOP}" width="{BAR_W}" height="{h}"/>'
            for i, h in enumerate(heights))

    all_bars = BARS_A[1] + BARS_B[1]
    x_min = 32.37                                  # left edge of the "O" outline
    width = lib_end + PAD - (x_min - PAD)
    vb = f"{x_min-PAD:.2f} {134.12-PAD:.2f} {width:.2f} {470.04-134.12+2*PAD:.2f}"

    path_tags = "\n    ".join(f'<path d="{d}"/>' for d in letters)
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">
  <title id="t">OpenMS-lib logo</title>
  <defs>
    <linearGradient id="bars" x1="{BARS_A[0]}" y1="0" x2="{BARS_B[0]+len(BARS_B[1])*BAR_PITCH-BAR_PITCH+BAR_W:.2f}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffcb4f"/>
      <stop offset=".35" stop-color="#ff7501"/>
      <stop offset="1" stop-color="#ff03cb"/>
    </linearGradient>
    <linearGradient id="lib" x1="{lib_x:.2f}" y1="0" x2="{lib_end:.2f}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{lib_c1}"/>
      <stop offset="1" stop-color="{lib_c2}"/>
    </linearGradient>
  </defs>
  <g fill="url(#bars)">
    {bars(*BARS_A)}
    {bars(*BARS_B)}
  </g>
  <g fill="{text_fill}">
    {path_tags}
  </g>
  <path d="{d_lib}" fill="url(#lib)" stroke="url(#lib)" stroke-width="{lib_stroke:.2f}" stroke-linejoin="miter"/>
</svg>
'''


def build_oms(logo_svg, font_path, white=False, gap=14):
    """Compact one-line variant: O + M + S outlines from the original, then "-lib"."""
    L = extract_letters(logo_svg)
    O, Os, M, Ms, S, Ss = L[0], L[1], L[8], L[9], L[10], L[11]
    text_fill = "#ffffff" if white else DARK
    lib_c1, lib_c2 = ("#cc51ff", "#7891f1") if white else ("#b503ff", "#3157e9")
    base_O = 274.96                                  # baseline of "Open" in the original
    ty_O = BASELINE_MS - base_O
    tx_O = -32.37                                    # left edge of O outline -> x = 0
    o_right = 185.49 + tx_O
    tx_M = o_right + gap - 528.39                    # left edge of M outline
    s_right = 811.0 + tx_M
    lib_x = s_right + LIB_GAP
    d_lib, lib_end = outline_text(font_path, "-lib", GLYPH_SIZE * LIB_SCALE, lib_x, BASELINE_MS)
    lib_stroke = STROKE_W * LIB_SCALE
    # bars hang under the O, like the "Open" bars in the main logo
    bar_top = BASELINE_MS + 5.94 + 22
    heights = [28, 43, 64, 51, 30, 80, 40, 56, 73, 91, 62]   # spectrum under O-M-S
    bars = "\n    ".join(f'<rect x="{i*BAR_PITCH+8:.2f}" y="{bar_top:.2f}" width="{BAR_W}" height="{h}"/>' for i, h in enumerate(heights))
    bx2 = 8 + (len(heights)-1)*BAR_PITCH + BAR_W
    top, bot = 322.48 - 0, max(bar_top + max(heights), 470.04)
    top = BASELINE_MS - 134.51 - 5.94
    vb = f"{-PAD} {top-PAD:.2f} {lib_end+2*PAD:.2f} {bot-top+2*PAD:.2f}"
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}" role="img" aria-labelledby="t">
  <title id="t">OMS-lib logo</title>
  <defs>
    <linearGradient id="bars" x1="8" y1="0" x2="{bx2:.2f}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="#ffcb4f"/>
      <stop offset=".25" stop-color="#ff7501"/>
      <stop offset=".55" stop-color="#ff03cb"/>
      <stop offset=".8" stop-color="#b503ff"/>
      <stop offset="1" stop-color="#3157e9"/>
    </linearGradient>
    <linearGradient id="lib" x1="{lib_x:.2f}" y1="0" x2="{lib_end:.2f}" y2="0" gradientUnits="userSpaceOnUse">
      <stop offset="0" stop-color="{lib_c1}"/>
      <stop offset="1" stop-color="{lib_c2}"/>
    </linearGradient>
  </defs>
  <g fill="url(#bars)">
    {bars}
  </g>
  <g fill="{text_fill}">
    <g transform="translate({tx_O:.2f} {ty_O:.2f})"><path d="{O}"/><path d="{Os}"/></g>
    <g transform="translate({tx_M:.2f} 0)"><path d="{M}"/><path d="{Ms}"/><path d="{S}"/><path d="{Ss}"/></g>
  </g>
  <path d="{d_lib}" fill="url(#lib)" stroke="url(#lib)" stroke-width="{lib_stroke:.2f}" stroke-linejoin="miter"/>
</svg>
'''

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--logo", required=True, help="official OpenMS logo SVG (outlined text)")
    ap.add_argument("--font", required=True, help="Montserrat Alternates Regular (ttf/otf/woff)")
    ap.add_argument("--out", default=".", help="output directory")
    ap.add_argument("--variant", choices=["openms", "oms"], default="openms",
                    help="openms = stacked Open/MS + -lib; oms = compact O M S + -lib")
    a = ap.parse_args()
    logo = open(a.logo, encoding="utf-8").read()
    fn, stem = (build, "openms-lib-logo") if a.variant == "openms" else (build_oms, "oms-lib-logo")
    for white, suffix in [(False, ""), (True, "-white")]:
        path = f"{a.out}/{stem}{suffix}.svg"
        open(path, "w", encoding="utf-8").write(fn(logo, a.font, white))
        print("wrote", path)
