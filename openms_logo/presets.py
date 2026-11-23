"""Ready-made logo and sublogo compositions.

Each preset is a function ``(theme) -> list[Element]`` built only from the
element functions, so every sublogo inherits the official geometry and colours.
Only ``full`` is the official logo; everything else is a derived sublogo
(see AGENTS.md before publishing one).
"""
from __future__ import annotations

from . import brand
from . import elements as E
from .elements import Gradient


def full(theme: str = "standard"):
    """The official OpenMS logo: 6 letters + 16 bars, original positions."""
    return E.all_bars() + E.all_letters()


def wordmark(theme: str = "standard"):
    """Letters only, original positions."""
    return E.all_letters()


def bars(theme: str = "standard"):
    """The 16 official bars only (spectrum mark)."""
    return E.all_bars()


def open_(theme: str = "standard"):
    """"Open" with the bars that hang beneath it (bars 1-10)."""
    return (E.bars_under_O() + E.bars_under_p() + E.bars_under_e()
            + [E.letter_O(), E.letter_p(), E.letter_e(), E.letter_n()])


def ms(theme: str = "standard"):
    """"MS" with the bars that stand above it (bars 11-16)."""
    return E.bars_above_M() + E.bars_above_S() + [E.letter_M(), E.letter_S()]


def o_icon(theme: str = "standard"):
    """Square-ish icon: the "O" with its four bars."""
    return E.bars_under_O() + [E.letter_O()]


# ---------------------------------------------------------------------------
# "-lib" sublogos (ported from the original make_openms_lib.py)
# ---------------------------------------------------------------------------

LIB_SCALE = 0.62   # "-lib" size relative to "MS"
LIB_GAP = 22.0     # space between "S" and "-lib"


def _lib_gradient(theme: str, x1: float, x2: float) -> Gradient:
    # purple -> blue; lighter tints on dark backdrops for contrast
    i = 1 if theme == "white" else 2
    return Gradient("openms-lib", x1, x2,
                    ((0, brand.PALETTE["purple"][i]), (1, brand.PALETTE["blue"][i])))


def _lib_text(theme: str, x: float):
    from .text import logo_text  # needs fonts; imported lazily

    probe = logo_text("-lib", x, scale=LIB_SCALE)
    return probe.with_paint(_lib_gradient(theme, probe.bbox[0], probe.bbox[2]))


def openms_lib(theme: str = "standard"):
    """Full logo + "-lib" after "MS"."""
    s_right = E.letter_S().bounds[2]
    return full(theme) + [_lib_text(theme, s_right + LIB_GAP)]


def oms_lib(theme: str = "standard", gap: float = 14.0,
            heights=(28, 43, 64, 51, 30, 80, 40, 56, 73, 91, 62)):
    """Compact one-liner: "O" "M" "S" + "-lib", with a row of new bars
    hanging below in the five logo colours."""
    O, M, S = E.letter_O(), E.letter_M(), E.letter_S()
    # drop "O" onto the MS baseline and pull "M"/"S" in next to it
    O = O.translate(-O.bbox[0], brand.BASELINE_MS - brand.BASELINE_OPEN)
    dx_ms = O.bounds[2] + gap - M.bbox[0]
    M, S = M.translate(dx_ms), S.translate(dx_ms)
    lib = _lib_text(theme, S.bounds[2] + LIB_GAP)

    axis = brand.BASELINE_MS + brand.GLYPH_STROKE / 2 + 22
    x0 = 8.0
    x_end = x0 + (len(heights) - 1) * brand.BAR_PITCH + brand.BAR_WIDTH
    grad = Gradient("oms-bars", x0, x_end, (
        (0, brand.LOGO_COLORS["yellow"]), (0.25, brand.LOGO_COLORS["orange"]),
        (0.55, brand.LOGO_COLORS["pink"]), (0.8, brand.LOGO_COLORS["purple"]),
        (1, brand.LOGO_COLORS["blue"])))
    new_bars = [E.bar(x0 + i * brand.BAR_PITCH, h, "down", axis_y=axis,
                      name=f"oms_bar_{i + 1:02d}", paint=grad)
                for i, h in enumerate(heights)]
    return new_bars + [O, M, S, lib]


PRESETS = {
    "full": full,
    "wordmark": wordmark,
    "bars": bars,
    "open": open_,
    "ms": ms,
    "o-icon": o_icon,
    "openms-lib": openms_lib,
    "oms-lib": oms_lib,
}

TITLES = {
    "full": "OpenMS logo",
    "wordmark": "OpenMS wordmark",
    "bars": "OpenMS bars",
    "open": "OpenMS logo - Open",
    "ms": "OpenMS logo - MS",
    "o-icon": "OpenMS icon",
    "openms-lib": "OpenMS-lib logo",
    "oms-lib": "OMS-lib logo",
}
