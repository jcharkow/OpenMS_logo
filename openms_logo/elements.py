"""Every drawable piece of the OpenMS logo as its own function.

Letters: :func:`letter_O`, :func:`letter_p`, :func:`letter_e`, :func:`letter_n`,
:func:`letter_M`, :func:`letter_S` (outlines copied verbatim from the official
SVG, so they are pixel-identical to it).

Bars: :func:`bar_01` ... :func:`bar_16`, numbered left -> right as they appear
in the official logo, plus group helpers (:func:`bars_under_O`, ...).
:func:`bar` builds a brand-conformant bar of any height for new sublogos.

Every function returns an :class:`Element` in official artboard coordinates.
Move elements with :meth:`Element.translate`; assemble them with
:func:`openms_logo.compose.compose`.
"""
from __future__ import annotations

from dataclasses import dataclass, field, replace
from functools import lru_cache

from . import brand
from ._official_paths import LETTER_PATHS

# Paint keywords understood by compose():
INK = "ink"    # letter colour, resolved from the theme (#231f20 / #ffffff)
BARS = "bars"  # the official bar gradient


@dataclass(frozen=True)
class Gradient:
    """A horizontal ``userSpaceOnUse`` linear gradient (in element coordinates)."""

    id: str
    x1: float
    x2: float
    stops: tuple[tuple[float, str], ...]

    def to_svg(self) -> str:
        stops = "".join(
            f'<stop offset="{o:g}" stop-color="{c}"/>' for o, c in self.stops
        )
        return (
            f'<linearGradient id="{self.id}" x1="{self.x1:g}" y1="0" '
            f'x2="{self.x2:g}" y2="0" gradientUnits="userSpaceOnUse">{stops}</linearGradient>'
        )


BAR_GRADIENT = Gradient("openms-bars", *brand.BAR_GRADIENT_X, brand.BAR_GRADIENT_STOPS)


@dataclass(frozen=True)
class Element:
    """One logo element.

    ``markup`` is SVG shape markup without fill; ``bbox`` is
    ``(xmin, ymin, xmax, ymax)`` *before* translation; ``paint`` is
    :data:`INK`, :data:`BARS`, a hex colour, or a :class:`Gradient`.
    Gradients are evaluated in the element's own (untranslated) coordinates,
    so a translated bar keeps exactly the colour it has in the official logo.
    """

    name: str
    kind: str                       # "letter" | "bar" | "text"
    markup: str
    bbox: tuple[float, float, float, float]
    paint: object = INK
    dx: float = 0.0
    dy: float = 0.0
    extra_attrs: dict = field(default_factory=dict, hash=False, compare=False)

    def translate(self, dx: float = 0.0, dy: float = 0.0) -> "Element":
        return replace(self, dx=self.dx + dx, dy=self.dy + dy)

    def moved_to(self, x: float | None = None, y: float | None = None) -> "Element":
        """Translate so the bbox's top-left corner lands on (x, y)."""
        x0, y0, *_ = self.bounds
        return self.translate(0 if x is None else x - x0, 0 if y is None else y - y0)

    def with_paint(self, paint) -> "Element":
        return replace(self, paint=paint)

    @property
    def bounds(self) -> tuple[float, float, float, float]:
        x0, y0, x1, y1 = self.bbox
        return (x0 + self.dx, y0 + self.dy, x1 + self.dx, y1 + self.dy)

    @property
    def width(self) -> float:
        return self.bbox[2] - self.bbox[0]

    @property
    def height(self) -> float:
        return self.bbox[3] - self.bbox[1]


# --------------------------------------------------------------------------
# geometry helpers
# --------------------------------------------------------------------------

@lru_cache(maxsize=None)
def path_bbox(d: str) -> tuple[float, float, float, float]:
    """Exact bounding box of SVG path data (uses fontTools' path parser)."""
    from fontTools.pens.boundsPen import BoundsPen
    from fontTools.svgLib.path import parse_path

    pen = BoundsPen(None)
    parse_path(d, pen)
    return pen.bounds


def _union(boxes):
    xs0, ys0, xs1, ys1 = zip(*boxes)
    return (min(xs0), min(ys0), max(xs1), max(ys1))


# --------------------------------------------------------------------------
# Letters
# --------------------------------------------------------------------------

def _letter(char: str) -> Element:
    fill_d, outline_d = LETTER_PATHS[char]
    markup = f'<path d="{fill_d}"/><path d="{outline_d}"/>'
    # the outline path is the stroke expanded around the glyph -> it is the
    # outermost shape, so its bbox is the letter's visual bbox
    return Element(f"letter_{char}", "letter", markup, _union([path_bbox(fill_d), path_bbox(outline_d)]))


def letter_O() -> Element:
    """The "O" of "Open" (Montserrat Alternates)."""
    return _letter("O")


def letter_p() -> Element:
    """The "p" of "Open" (Montserrat Alternates)."""
    return _letter("p")


def letter_e() -> Element:
    """The "e" of "Open" (Montserrat Alternates)."""
    return _letter("e")


def letter_n() -> Element:
    """The "n" of "Open" (Montserrat Alternates). Its right leg is lengthened
    down to the bar axis -- keep it that way."""
    return _letter("n")


def letter_M() -> Element:
    """The "M" of "MS" (Montserrat, not Alternates)."""
    return _letter("M")


def letter_S() -> Element:
    """The "S" of "MS" (Montserrat Alternates)."""
    return _letter("S")


LETTERS = {
    "O": letter_O, "p": letter_p, "e": letter_e,
    "n": letter_n, "M": letter_M, "S": letter_S,
}


# --------------------------------------------------------------------------
# Bars
# --------------------------------------------------------------------------

def bar(x: float, height: float, direction: str = "down", *,
        axis_y: float = brand.BAR_AXIS_Y, name: str = "bar",
        paint=BARS) -> Element:
    """A brand bar: fixed width (:data:`brand.BAR_WIDTH`), square ends.

    ``direction="down"`` hangs from ``axis_y``; ``"up"`` stands on it.
    Use this for *new* sublogo bars; use ``bar_01``..``bar_16`` for the
    official ones.
    """
    if direction not in ("down", "up"):
        raise ValueError("direction must be 'down' or 'up'")
    y = axis_y if direction == "down" else axis_y - height
    w = brand.BAR_WIDTH
    markup = f'<rect x="{x:g}" y="{y:g}" width="{w:g}" height="{height:g}"/>'
    return Element(name, "bar", markup, (x, y, x + w, y + height), paint)


#: Official bars: (left x, height, direction), left -> right, measured from the
#: official SVG. 1-4 hang under "O", 5-7 under "p", 8-10 under "e";
#: 11-12 stand above "M", 13-16 above "S".
OFFICIAL_BARS = (
    (44.08, 72.54, "down"),
    (81.49, 107.23, "down"),
    (118.90, 162.90, "down"),
    (156.30, 84.77, "down"),
    (250.91, 46.45, "down"),
    (288.31, 133.17, "down"),
    (325.72, 66.86, "down"),
    (408.10, 92.91, "down"),
    (445.51, 122.17, "down"),
    (482.92, 151.52, "down"),
    (576.69, 103.03, "up"),
    (614.10, 39.83, "up"),
    (676.84, 103.03, "up"),
    (714.25, 157.33, "up"),
    (751.66, 66.98, "up"),
    (789.07, 39.83, "up"),
)


def _official_bar(n: int) -> Element:
    x, h, direction = OFFICIAL_BARS[n - 1]
    return bar(x, h, direction, name=f"bar_{n:02d}")


def bar_01() -> Element: return _official_bar(1)    # under O
def bar_02() -> Element: return _official_bar(2)    # under O
def bar_03() -> Element: return _official_bar(3)    # under O (longest down-bar)
def bar_04() -> Element: return _official_bar(4)    # under O
def bar_05() -> Element: return _official_bar(5)    # under p
def bar_06() -> Element: return _official_bar(6)    # under p
def bar_07() -> Element: return _official_bar(7)    # under p
def bar_08() -> Element: return _official_bar(8)    # under e
def bar_09() -> Element: return _official_bar(9)    # under e
def bar_10() -> Element: return _official_bar(10)   # under e
def bar_11() -> Element: return _official_bar(11)   # above M
def bar_12() -> Element: return _official_bar(12)   # above M
def bar_13() -> Element: return _official_bar(13)   # above S
def bar_14() -> Element: return _official_bar(14)   # above S (tallest)
def bar_15() -> Element: return _official_bar(15)   # above S
def bar_16() -> Element: return _official_bar(16)   # above S


BARS_BY_NUMBER = {
    1: bar_01, 2: bar_02, 3: bar_03, 4: bar_04, 5: bar_05, 6: bar_06,
    7: bar_07, 8: bar_08, 9: bar_09, 10: bar_10, 11: bar_11, 12: bar_12,
    13: bar_13, 14: bar_14, 15: bar_15, 16: bar_16,
}


def bars_under_O() -> list[Element]: return [bar_01(), bar_02(), bar_03(), bar_04()]
def bars_under_p() -> list[Element]: return [bar_05(), bar_06(), bar_07()]
def bars_under_e() -> list[Element]: return [bar_08(), bar_09(), bar_10()]
def bars_above_M() -> list[Element]: return [bar_11(), bar_12()]
def bars_above_S() -> list[Element]: return [bar_13(), bar_14(), bar_15(), bar_16()]
def all_bars() -> list[Element]: return [BARS_BY_NUMBER[i]() for i in range(1, 17)]
def all_letters() -> list[Element]: return [f() for f in LETTERS.values()]


def element(name: str) -> Element:
    """Look an element up by name: ``"O"``/``"letter_O"``, ``"bar_07"``/``"7"``."""
    key = name.removeprefix("letter_")
    if key in LETTERS:
        return LETTERS[key]()
    key = name.removeprefix("bar_")
    if key.isdigit() and 1 <= int(key) <= 16:
        return BARS_BY_NUMBER[int(key)]()
    raise KeyError(f"unknown element {name!r}")
