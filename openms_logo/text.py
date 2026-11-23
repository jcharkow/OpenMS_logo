"""New lettering in the logo's style (e.g. the "-lib" of a sublogo).

The six official letters must always come from :mod:`openms_logo.elements`.
Use this module only for characters the official logo does not contain.
Text is converted to outlines, so generated SVGs need no installed fonts.

Fonts are not committed; run ``python scripts/fetch_fonts.py`` once (puts the
Google Fonts TTFs into ``fonts/``) or point ``OPENMS_FONT_DIR`` elsewhere.
"""
from __future__ import annotations

import os
from pathlib import Path

from . import brand
from .elements import INK, Element, path_bbox

FONT_DIR = Path(os.environ.get("OPENMS_FONT_DIR", Path(__file__).resolve().parent.parent / "fonts"))

#: logical name -> file name inside FONT_DIR (see scripts/fetch_fonts.py)
FONT_FILES = {
    "alternates": "MontserratAlternates-Regular.ttf",   # logo-matching lettering
    "montserrat": "Montserrat-Regular.ttf",             # for a logo-matching capital "M"
}


def font_path(font: str) -> Path:
    p = Path(font)
    if p.suffix and p.exists():
        return p
    p = FONT_DIR / FONT_FILES.get(font, font)
    if not p.exists():
        raise FileNotFoundError(f"{p} missing -- run `python scripts/fetch_fonts.py`")
    return p


def outline(text: str, x: float, baseline: float, size: float, font: str = "alternates",
            tracking: float = 0.0) -> tuple[str, float]:
    """Return (SVG path data, advance end x) for ``text`` set at ``size``."""
    from fontTools.pens.svgPathPen import SVGPathPen
    from fontTools.pens.transformPen import TransformPen
    from fontTools.ttLib import TTFont

    tt = TTFont(str(font_path(font)))
    gs, cmap, upm = tt.getGlyphSet(), tt.getBestCmap(), tt["head"].unitsPerEm
    s, cx, parts = size / upm, x, []
    for ch in text:
        g = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: f"{v:.2f}")
        gs[g].draw(TransformPen(pen, (s, 0, 0, -s, cx, baseline)))
        parts.append(pen.getCommands())
        cx += gs[g].width * s + tracking
    return " ".join(p for p in parts if p), cx


def side_bearings(char: str, font: str = "alternates") -> tuple[float, float]:
    """(left, right) side bearing of ``char`` as a fraction of the em."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.ttLib import TTFont

    tt = TTFont(str(font_path(font)))
    gs, upm = tt.getGlyphSet(), tt["head"].unitsPerEm
    g = gs[tt.getBestCmap()[ord(char)]]
    pen = BoundsPen(gs)
    g.draw(pen)
    return pen.bounds[0] / upm, (g.width - pen.bounds[2]) / upm


def letter_gap(left: str, right: str, scale: float = 1.0) -> float:
    """Natural gap between the *outlines* of two logo-weight letters set
    side by side (font spacing minus the stroke). The capital "M" is taken
    from Montserrat, everything else from Montserrat Alternates."""
    fl = "montserrat" if left == "M" else "alternates"
    fr = "montserrat" if right == "M" else "alternates"
    gap = side_bearings(left, fl)[1] + side_bearings(right, fr)[0]
    return (gap * brand.GLYPH_SIZE - brand.GLYPH_STROKE) * scale


def logo_text(text: str, x: float, baseline: float = brand.BASELINE_MS, *,
              scale: float = 1.0, font: str = "alternates", paint=INK,
              name: str | None = None) -> Element:
    """Lettering that matches the weight of the logo letters.

    ``scale=1`` gives letters the same size as "MS"; the stroke scales with
    the glyphs so the weight stays identical. ``paint`` defaults to the theme
    ink colour; pass a brand hex or :class:`~openms_logo.elements.Gradient`.
    """
    size = brand.GLYPH_SIZE * scale
    sw = brand.GLYPH_STROKE * scale
    d, _ = outline(text, x, baseline, size, font)
    # Painted with stroke = fill so it matches the expanded outline paths of the
    # official letters. stroke-width is the total stroke (half on each side).
    markup = f'<path d="{d}" stroke-width="{sw:.2f}" stroke-linejoin="miter"/>'
    x0, y0, x1, y1 = path_bbox(d)
    h = sw / 2
    return Element(name or f"text_{text}", "text", markup, (x0 - h, y0 - h, x1 + h, y1 + h), paint)
