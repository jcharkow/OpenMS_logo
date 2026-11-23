"""OpenMS corporate-design constants.

Source of truth: ``OpenMS_CorporateDesign_current.pdf`` (2025) in the repo root,
plus measurements taken from the official ``OpenMS_transparent_blackFont.svg``.
Never hard-code a colour or font anywhere else -- import it from here.
"""

# --------------------------------------------------------------------------
# Colours (PDF section 2 "Color Scheme" and section 3 "Logo")
# --------------------------------------------------------------------------

#: Tints and shades of each brand hue, lightest -> darkest. Index 1 or 2 is the
#: "logo colour" (bold in the PDF), see :data:`LOGO_COLORS`.
PALETTE = {
    "yellow": ("#ffe29e", "#ffcb4f", "#ffb401", "#b27d00", "#634600"),
    "orange": ("#ffca9e", "#ffa04f", "#ff7501", "#b25100", "#632d00"),
    "pink":   ("#ffa0ec", "#ff52db", "#ff03cb", "#b4008f", "#660051"),
    "purple": ("#e3a0ff", "#cc51ff", "#b503ff", "#7f00b4", "#480066"),
    "blue":   ("#bfcbf8", "#7891f1", "#3157e9", "#1436b8", "#0c2171"),
    "black":  ("#000000", "#231f20", "#4d4446"),   # pure, logo black, soft
    "grey":   ("#76696c", "#9d9094", "#c2babc"),
    "white":  ("#ffffff", "#f9f8f9", "#fff9ec"),   # pure, grey off-white, yellow off-white
}

#: The colours named in the PDF's logo section.
LOGO_COLORS = {
    "yellow": "#ffcb4f",
    "orange": "#ff7501",
    "pink":   "#ff03cb",
    "purple": "#b503ff",
    "blue":   "#3157e9",
    "black":  "#231f20",   # letters, standard logo
    "white":  "#ffffff",   # letters, white logo (dark backdrops)
}

#: CMYK values for print (PDF section 4). Use these instead of converting RGB.
CMYK = {
    "yellow": (0, 20, 59, 0),
    "orange": (0, 52, 86, 4),
    "pink":   (0, 90, 40, 8),
    "purple": (0, 78, 21, 29),
    "blue":   (100, 43, 0, 36),
}

#: Letter ("ink") colour per theme. ``standard`` is for light backdrops,
#: ``white`` for dark backdrops. These are the only two official versions.
INK = {
    "standard": LOGO_COLORS["black"],
    "white": LOGO_COLORS["white"],
}

#: Bar gradient exactly as in the official SVG (offset, colour). It runs
#: left -> right across all 16 bars in artboard space (:data:`BAR_GRADIENT_X`).
#: Note: the official file starts at #ffb401 (yellow shade) and eases into
#: orange; the PDF lists #ffcb4f as "yellow". Reproduce the file, not the PDF
#: swatch, when drawing the logo bars.
BAR_GRADIENT_STOPS = (
    (0.00, "#ffb401"),
    (0.00, "#ffb201"),
    (0.05, "#ff9701"),
    (0.11, "#ff8401"),
    (0.16, "#ff7901"),
    (0.22, "#ff7501"),
    (0.54, "#ff03cb"),
    (0.77, "#b503ff"),
    (0.91, "#3157e9"),
)
BAR_GRADIENT_X = (44.08, 811.73)

# --------------------------------------------------------------------------
# Typography (PDF section 1)
# --------------------------------------------------------------------------

FONTS = {
    "heading": "Montserrat",              # ExtraBold 26pt / Bold 20pt / SemiBold 16pt
    "body": "Raleway",                    # Regular; 11-14pt text, 18pt slides, >=11pt web
    "quote": "JetBrains Mono",            # Thin, 1pt smaller than body text
    "logo": "Montserrat Alternates",      # logo letters + whimsical special use
    "logo_capital_M": "Montserrat",       # the "M" of the logo
    "special": "Chakra Petch",            # Bold; modern/tech alternative to Alternates
    "numerals": "Montserrat",             # Regular; replace Raleway's oldstyle numerals
}

# --------------------------------------------------------------------------
# Logo geometry measured from the official SVG (artboard units)
# --------------------------------------------------------------------------

ARTBOARD = (0.0, 0.0, 841.89, 595.28)   # official viewBox

BAR_WIDTH = 22.66
BAR_PITCH = 37.41        # left edge to left edge of neighbouring bars
BAR_AXIS_Y = 302.49      # down-bars hang from it, up-bars stand on it
                         # (it is also the bottom of the "n" leg outline)

BASELINE_OPEN = 275.73   # baseline of "Open" (O/e fill bottoms minus font overshoot)
BASELINE_MS = 462.93     # baseline of "MS"

#: New lettering that must match the logo letters (e.g. "-lib") is drawn from
#: Montserrat Alternates **Regular** at this size plus an outline stroke of
#: this total width. Measured: the official glyph outlines are exactly
#: Regular @ 192.2 units, and the expanded stroke adds 5.94 per side. (The PDF
#: describes this visually as "SemiBold + 0.5 stroke".)
GLYPH_SIZE = 192.2
GLYPH_STROKE = 11.88

#: Default clear space around generated artwork: half the cap height of "M".
#: The PDF only asks for "appropriate clear space"; this is the repo convention.
CLEAR_SPACE = 67.0
