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
    # purple -> blue; lighter tints on dark backdrops for contrast (>= 3:1)
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


# ---------------------------------------------------------------------------
# One-line "spectrum" wordmarks (layout inspired by the pyopenms_viz logo):
#
#     ▌ ▌▌ ▌    ▌▌ ▌   ▌▌▌           lib
#   [prefix]OpenMS
#
# Bars stand on an axis above "Open" and run yellow -> pink; the suffix sits on
# the same axis above "MS" in purple -> blue, so bars + suffix together carry
# the complete official gradient. Every bar keeps the x position (and so the
# colour) of the official bar it is derived from.
# ---------------------------------------------------------------------------

AXIS_GAP = 20.0     # axis -> letter tops; same as bar axis -> "MS" caps in the official logo


def one_line_openms():
    """"OpenMS" on a single line at the "Open" baseline, official letterforms
    (short-leg "n"), font spacing between "n" and "M"."""
    from .text import letter_gap

    O, p, e, n = E.letter_O(), E.letter_p(), E.letter_e(), E.letter_n_short()
    M, S = E.letter_M(), E.letter_S()
    dx = n.bounds[2] + letter_gap("n", "M") - M.bbox[0]
    dy = brand.BASELINE_OPEN - brand.BASELINE_MS
    return [O, p, e, n, M.translate(dx, dy), S.translate(dx, dy)]


def spectrum_wordmark(theme: str = "standard", suffix: str = "lib", prefix: str = "",
                      bar_scale: float = 0.7, suffix_scale: float = 0.62):
    from .text import letter_gap, logo_text

    letters = one_line_openms()
    top = min(el.bounds[1] for el in letters)
    axis = top - AXIS_GAP

    # bars 1-10 of the official logo, flipped to stand on the axis
    spectrum = [E.bar(x, h * bar_scale, "up", axis_y=axis, name=f"spectrum_bar_{i + 1:02d}")
                for i, (x, h, _) in enumerate(E.OFFICIAL_BARS[:10])]

    out = spectrum + letters
    if prefix:
        pre = logo_text(prefix, 0, brand.BASELINE_OPEN, name=f"text_{prefix}")
        gap = letter_gap(prefix[-1], "O")
        out.append(pre.translate(letters[0].bounds[0] - gap - pre.bounds[2]))
    if suffix:
        # right-aligned with "S", sitting on the axis; purple -> blue so bars +
        # suffix carry the whole brand gradient (lighter tints on dark
        # backdrops: #3157e9 on #231f20 is only 2.85:1)
        probe = logo_text(suffix, 0, axis, scale=suffix_scale)
        sfx = probe.translate(letters[-1].bounds[2] - probe.bbox[2])
        x0, _, x1, _ = sfx.bbox
        out.append(sfx.with_paint(_lib_gradient(theme, x0, x1)))
    return out


# ---------------------------------------------------------------------------
# Peak wordmarks: the spectrum layout with a single, simple peak of 3-4 bars
# (or none). Heights are fractions of ``peak_height``; colours either the
# discrete logo colours (yellow, orange, pink, ...) or the yellow -> pink part
# of the gradient running across the group. The suffix keeps purple -> blue,
# so bars + suffix still walk through all five logo colours.
# ---------------------------------------------------------------------------

PEAK_COLORS = ("yellow", "orange", "pink", "purple")


def peak_wordmark(theme: str = "standard", heights=(0.55, 1.0, 0.55), suffix: str = "lib",
                  prefix: str = "", colors: str = "solid", peak_height: float = 112.0,
                  over: str = "Open", suffix_scale: float = 0.62,
                  spread: str | None = None, suffix_span: bool = False,
                  spread_padding: float = 0.0, suffix_align: str = "right",
                  suffix_padding: float = 0.0, suffix_height: float | None = None,
                  suffix_tracking: float = 0.0):
    """One-line "OpenMS" + suffix with a small peak of bars standing above it.

    ``heights``: bar heights as fractions of ``peak_height`` (empty = no bars).
    ``colors``: "solid" (one logo colour per bar) or "gradient".
    ``over``: centre the peak over "Open" or "OpenMS" (bars at the official pitch).
    ``spread``: instead, stretch the bars evenly across "pen" or "Open"
    (outer bar edges flush with the outer letter edges; bar width unchanged).
    ``spread_padding``: inset on each side of the spread, as a fraction of
    the spread width (0.15 = bars cover the middle 70%, still centred).
    ``suffix_align``: "right" (flush with "S"), "center" (over "MS") or
    "left" (flush with "M"). ``suffix_padding``: inset from that edge as a
    fraction of the "MS" width (ignored for "center").
    ``suffix_height``: if set, size the suffix so its top sits this far above
    the axis (e.g. ``peak_height`` = level with the tallest bar); overrides
    ``suffix_scale``.
    ``suffix_tracking``: extra space after each suffix letter (artboard units;
    the "MS" stroke is 11.88 wide for scale).
    ``suffix_span``: letter-space the suffix so it spans the width of "MS".
    """
    from .text import letter_gap, logo_text

    letters = one_line_openms()
    axis = min(el.bounds[1] for el in letters) - AXIS_GAP
    out = []
    if heights:
        if spread:
            first = {"pen": letters[1], "Open": letters[0]}[spread]
            x0, x_end = first.bounds[0], letters[3].bounds[2]
            if suffix_span:   # keep the last bar clear of the suffix above "M"
                x_end = min(x_end, letters[4].bounds[0] - 2 * AXIS_GAP)
            inset = (x_end - x0) * spread_padding
            x0, x_end = x0 + inset, x_end - inset
            width = x_end - x0
            pitch = (width - brand.BAR_WIDTH) / max(len(heights) - 1, 1)
        else:
            span = letters[3] if over == "Open" else letters[-1]
            centre = (letters[0].bounds[0] + span.bounds[2]) / 2
            pitch = brand.BAR_PITCH
            width = (len(heights) - 1) * pitch + brand.BAR_WIDTH
            x0 = centre - width / 2
        if colors == "solid":
            paints = [brand.LOGO_COLORS[c] for c in PEAK_COLORS[:len(heights)]]
        else:
            grad = Gradient("openms-peak", x0, x0 + width, (
                (0, brand.LOGO_COLORS["yellow"]), (0.5, brand.LOGO_COLORS["orange"]),
                (1, brand.LOGO_COLORS["pink"])))
            paints = [grad] * len(heights)
        out += [E.bar(x0 + i * pitch, f * peak_height, "up", axis_y=axis,
                      name=f"peak_bar_{i + 1}", paint=paint)
                for i, (f, paint) in enumerate(zip(heights, paints))]
    out += letters
    if prefix:
        pre = logo_text(prefix, 0, brand.BASELINE_OPEN, name=f"text_{prefix}")
        out.append(pre.translate(letters[0].bounds[0] - letter_gap(prefix[-1], "O") - pre.bounds[2]))
    if suffix:
        if suffix_height is not None:
            unit = logo_text(suffix, 0, axis)
            suffix_scale = suffix_height / (axis - unit.bbox[1])
        tracking = suffix_tracking
        ms_left, ms_right = letters[-2].bounds[0], letters[-1].bounds[2]
        if suffix_span and len(suffix) > 1:
            w0 = logo_text(suffix, 0, axis, scale=suffix_scale).width
            tracking = (ms_right - ms_left - w0) / (len(suffix) - 1)
        probe = logo_text(suffix, 0, axis, scale=suffix_scale, name=f"text_{suffix}", tracking=tracking)
        inset = suffix_padding * (ms_right - ms_left)
        if suffix_align == "right":
            dx = ms_right - inset - probe.bbox[2]
        elif suffix_align == "left":
            dx = ms_left + inset - probe.bbox[0]
        else:
            dx = (ms_left + ms_right) / 2 - (probe.bbox[0] + probe.bbox[2]) / 2
        sfx = probe.translate(dx)
        out.append(sfx.with_paint(_lib_gradient(theme, sfx.bbox[0], sfx.bbox[2])))
    return out


def openms_lib_peak3(theme: str = "standard"):
    """3 bars, symmetric peak, solid yellow / orange / pink."""
    return peak_wordmark(theme, heights=(0.55, 1.0, 0.55))


def openms_lib_peak4(theme: str = "standard"):
    """4 bars, skewed peak like pyopenms_viz, yellow -> pink gradient."""
    return peak_wordmark(theme, heights=(0.6, 1.0, 0.7, 0.3), colors="gradient")


PEAK4 = (0.6, 1.0, 0.7, 0.3)
PEAK4_SPREAD = (0.55, 1.0, 0.7, 0.4)   # smallest bar a bit taller so it doesn't read as a dot
SPREAD_HEIGHT = 150.0
SPAN_SCALE = 0.8                       # "lib" size when it spans "MS"


def openms_lib_peak4_pen(theme: str = "standard"):
    """peak4 with the bars centred over "pen", covering its middle 70%."""
    return peak_wordmark(theme, heights=PEAK4_SPREAD, colors="gradient", spread="pen",
                         peak_height=SPREAD_HEIGHT, spread_padding=0.15)


PEN_PADDINGS = (0.0, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30)


def _peak4_pen_padded(padding: float):
    def fn(theme: str = "standard"):
        return peak_wordmark(theme, heights=PEAK4_SPREAD, colors="gradient", spread="pen",
                             peak_height=SPREAD_HEIGHT, spread_padding=padding)
    fn.__name__ = f"openms_lib_peak4_pen_pad{round(padding * 100):02d}"
    fn.__doc__ = (f'peak4-pen with {padding:.0%} padding each side: the bars cover the '
                  f'middle {1 - 2 * padding:.0%} of "pen".')
    return fn


def openms_lib_pen15(theme: str = "standard", **suffix_opts):
    """The chosen OpenMS-lib design: 4-bar peak centred over "pen" with 15%
    padding each side, "lib" above "MS" (right-aligned, 0.62 x "MS" size)."""
    return peak_wordmark(theme, heights=PEAK4_SPREAD, colors="gradient", spread="pen",
                         peak_height=SPREAD_HEIGHT, spread_padding=0.15, **suffix_opts)


#: "lib" experiments on top of openms_lib_pen15: size x position
LIB_SIZES = {
    "s62": {"suffix_scale": 0.62},                 # current
    "s70": {"suffix_scale": 0.70},
    "s80": {"suffix_scale": 0.80},                 # medium
    "bar": {"suffix_height": SPREAD_HEIGHT},       # top of "lib" level with the tallest bar
}
LIB_POSITIONS = {
    "right": {"suffix_align": "right"},
    "right10": {"suffix_align": "right", "suffix_padding": 0.10},
    "center": {"suffix_align": "center"},
}


def _pen15_lib(size: str, pos: str):
    def fn(theme: str = "standard"):
        return openms_lib_pen15(theme, **LIB_SIZES[size], **LIB_POSITIONS[pos])
    label = {"s62": "0.62 x MS size", "s70": "0.7 x MS size", "s80": "0.8 x MS size",
             "bar": "as tall as the top bar"}[size]
    where = {"right": "right-aligned with S", "right10": "right-aligned, 10% in from S",
             "center": "centred over MS"}[pos]
    fn.__doc__ = f'pen15 with "lib" {label}, {where}.'
    return fn


PEN15_LIB_VARIANTS = {f"openms-lib-pen15-lib-{size}-{pos}": _pen15_lib(size, pos)
                      for size in LIB_SIZES for pos in LIB_POSITIONS}


#: letter-spacing experiments on the favourite (s70, right-aligned)
S70_TRACKINGS = (4, 8, 12, 16)


def _s70_tracked(t: float):
    def fn(theme: str = "standard"):
        return openms_lib_pen15(theme, suffix_scale=0.70, suffix_align="right", suffix_tracking=t)
    fn.__doc__ = f'pen15 with "lib" 0.7 x MS size, right-aligned, +{t} units letter spacing.'
    return fn


S70_TRACKED = {f"openms-lib-pen15-lib-s70-right-t{t:02d}": _s70_tracked(t) for t in S70_TRACKINGS}


PEAK4_PEN_PADDED = {f"openms-lib-peak4-pen-pad{round(p * 100):02d}": _peak4_pen_padded(p)
                    for p in PEN_PADDINGS}


def openms_lib_peak4_open(theme: str = "standard"):
    """peak4 with the bars spread across "Open"."""
    return peak_wordmark(theme, heights=PEAK4_SPREAD, colors="gradient", spread="Open",
                         peak_height=SPREAD_HEIGHT)


def openms_lib_peak4_open_span(theme: str = "standard"):
    """Bars spread across "Open", "lib" spanning "MS"."""
    return peak_wordmark(theme, heights=PEAK4_SPREAD, colors="gradient", spread="Open",
                         peak_height=SPREAD_HEIGHT, suffix_span=True, suffix_scale=SPAN_SCALE)


def openms_lib_plain_span(theme: str = "standard"):
    """No bars; "lib" spanning "MS"."""
    return peak_wordmark(theme, heights=(), suffix_span=True, suffix_scale=SPAN_SCALE)


def openms_lib_peak4_tall(theme: str = "standard"):
    """4-bar gradient peak, but tall (about 1.4x the letter height), closer to
    the proportions of the pyopenms_viz logo."""
    return peak_wordmark(theme, heights=(0.6, 1.0, 0.7, 0.3), colors="gradient", peak_height=200.0)


def openms_lib_peak4_solid(theme: str = "standard"):
    """4 bars, symmetric peak, solid yellow / orange / pink / purple."""
    return peak_wordmark(theme, heights=(0.45, 0.85, 1.0, 0.55))


def openms_lib_plain(theme: str = "standard"):
    """No bars: one-line "OpenMS" with "lib" above "MS"."""
    return peak_wordmark(theme, heights=())


def openms_lib_spectrum(theme: str = "standard"):
    """"OpenMS" one line, spectrum bars above "Open", "lib" above "MS"."""
    return spectrum_wordmark(theme, suffix="lib")


def pyopenms_viz(theme: str = "standard"):
    """pyOpenMS-viz in the same layout."""
    return spectrum_wordmark(theme, suffix="viz", prefix="py")


# ---------------------------------------------------------------------------
# Square OpenMS-lib variants: two lines, "Open" over "MS lib"
#
#   A  bars on top          B  bars hanging below     C  official logo + lib
#      ▌▌█▌ ▖█▌ ▌▌█            Open                      Open ▌▌ ▌█▌
#      Open                    MS lib                    ▌█▌ ▌▌ MS
#      MS lib                  ▌▌█▌ ▖█▌ ▌▌█              lib
# ---------------------------------------------------------------------------

LINE_GAP = 20.0   # p descender -> next line's caps (same as AXIS_GAP)


def _stack_letters(theme, suffix, suffix_scale, suffix_paint, word_gap):
    """[O, p, e, n_short] / [M, S, suffix] left-aligned. ``suffix_scale=None``
    sizes the suffix so the second line is exactly as wide as "Open"."""
    from .text import logo_text

    top = [E.letter_O(), E.letter_p(), E.letter_e(), E.letter_n_short()]
    left, right = top[0].bounds[0], top[-1].bounds[2]
    M, S = E.letter_M(), E.letter_S()
    dx = left - M.bbox[0]
    dy = top[1].bounds[3] + LINE_GAP - min(M.bbox[1], S.bbox[1])
    M, S = M.translate(dx, dy), S.translate(dx, dy)
    baseline2 = brand.BASELINE_MS + dy
    x_sfx = S.bounds[2] + word_gap
    if suffix_scale is None:   # fit the line width to "Open"
        unit = logo_text(suffix, 0, 0)
        suffix_scale = (right - x_sfx) / unit.width
    probe = logo_text(suffix, 0, baseline2, scale=suffix_scale, name=f"text_{suffix}")
    sfx = probe.translate(x_sfx - probe.bbox[0])
    if suffix_paint == "gradient":
        sfx = sfx.with_paint(_lib_gradient(theme, sfx.bbox[0], sfx.bbox[2]))
    return top, [M, S, sfx]


def square_lib(theme: str = "standard", suffix: str = "lib", bars: str = "top",
               bar_scale: float = 0.7, suffix_scale: float | None = None,
               suffix_paint: str = "gradient", word_gap: float = 34.0):
    """Square OpenMS-<suffix> logo. ``bars``: "top" (stand above "Open") or
    "bottom" (hang below "MS lib"). Bars are the official bars 1-10 at their
    official x positions (so official colours), heights * ``bar_scale``."""
    top, second = _stack_letters(theme, suffix, suffix_scale, suffix_paint, word_gap)
    letters = top + second
    if bars == "top":
        axis = min(el.bounds[1] for el in top) - AXIS_GAP
        direction = "up"
    else:
        axis = max(el.bounds[3] for el in second) + AXIS_GAP
        direction = "down"
    spectrum = [E.bar(x, h * bar_scale, direction, axis_y=axis, name=f"spectrum_bar_{i + 1:02d}")
                for i, (x, h, _) in enumerate(E.OFFICIAL_BARS[:10])]
    # centre the spectrum over "Open"; translating keeps each bar's official colour
    lo, hi = top[0].bounds[0], top[-1].bounds[2]
    shift = (lo + hi) / 2 - (spectrum[0].bounds[0] + spectrum[-1].bounds[2]) / 2
    return [b.translate(shift) for b in spectrum] + letters


def openms_lib_square_top(theme: str = "standard"):
    """A: spectrum on top, "Open" / "MS lib"."""
    return square_lib(theme, bars="top")


def openms_lib_square_bottom(theme: str = "standard"):
    """B: "Open" / "MS lib", spectrum hanging below (like the official bars)."""
    return square_lib(theme, bars="bottom")


def openms_lib_square_ink(theme: str = "standard"):
    """D: like A, but "lib" in the letter colour; the bars carry all the colour."""
    return square_lib(theme, bars="top", suffix_paint="ink")


def openms_lib_official_stack(theme: str = "standard"):
    """C: the untouched official logo with "lib" as a third line under the
    hanging bars, left-aligned with "O", same letter size as "MS"."""
    from .text import logo_text

    logo = full(theme)
    O = E.letter_O()
    bottom = max(el.bounds[3] for el in logo)
    probe = logo_text("lib", 0, 0)
    baseline = bottom + LINE_GAP - probe.bbox[1]
    sfx = logo_text("lib", 0, baseline, name="text_lib")
    sfx = sfx.translate(O.bounds[0] - sfx.bbox[0])
    return logo + [sfx.with_paint(_lib_gradient(theme, sfx.bbox[0], sfx.bbox[2]))]


PRESETS = {
    "full": full,
    "wordmark": wordmark,
    "bars": bars,
    "open": open_,
    "ms": ms,
    "o-icon": o_icon,
    "openms-lib": openms_lib,
    "oms-lib": oms_lib,
    "openms-lib-spectrum": openms_lib_spectrum,
    "pyopenms-viz": pyopenms_viz,
    "openms-lib-square-top": openms_lib_square_top,
    "openms-lib-square-bottom": openms_lib_square_bottom,
    "openms-lib-square-ink": openms_lib_square_ink,
    "openms-lib-official-stack": openms_lib_official_stack,
    "openms-lib-peak3": openms_lib_peak3,
    "openms-lib-peak4": openms_lib_peak4,
    "openms-lib-peak4-pen": openms_lib_peak4_pen,
    **PEAK4_PEN_PADDED,
    **PEN15_LIB_VARIANTS,
    **S70_TRACKED,
    "openms-lib-peak4-open": openms_lib_peak4_open,
    "openms-lib-peak4-open-span": openms_lib_peak4_open_span,
    "openms-lib-plain-span": openms_lib_plain_span,
    "openms-lib-peak4-tall": openms_lib_peak4_tall,
    "openms-lib-peak4-solid": openms_lib_peak4_solid,
    "openms-lib-plain": openms_lib_plain,
}

#: Presets whose SVGs are published in logos/ (standard + white). Every other
#: preset stays available from the CLI / build/.
PUBLISHED = [
    "full",
    "openms-lib-peak4-pen-pad15",       # "lib" 0.62x, right-aligned
    "openms-lib-pen15-lib-s70-right",   # favourite
    *S70_TRACKED,                       # letter-spacing experiments on s70-right
    "openms-lib-pen15-lib-s80-right",
]

TITLES = {
    "full": "OpenMS logo",
    "wordmark": "OpenMS wordmark",
    "bars": "OpenMS bars",
    "open": "OpenMS logo - Open",
    "ms": "OpenMS logo - MS",
    "o-icon": "OpenMS icon",
    "openms-lib": "OpenMS-lib logo",
    "oms-lib": "OMS-lib logo",
    "openms-lib-spectrum": "OpenMS-lib logo",
    "pyopenms-viz": "pyOpenMS-viz logo",
    "openms-lib-square-top": "OpenMS-lib logo",
    "openms-lib-square-bottom": "OpenMS-lib logo",
    "openms-lib-square-ink": "OpenMS-lib logo",
    "openms-lib-official-stack": "OpenMS-lib logo",
    "openms-lib-peak3": "OpenMS-lib logo",
    "openms-lib-peak4": "OpenMS-lib logo",
    "openms-lib-peak4-pen": "OpenMS-lib logo",
    **{k: "OpenMS-lib logo" for k in PEAK4_PEN_PADDED},
    **{k: "OpenMS-lib logo" for k in PEN15_LIB_VARIANTS},
    **{k: "OpenMS-lib logo" for k in S70_TRACKED},
    "openms-lib-peak4-open": "OpenMS-lib logo",
    "openms-lib-peak4-open-span": "OpenMS-lib logo",
    "openms-lib-plain-span": "OpenMS-lib logo",
    "openms-lib-peak4-tall": "OpenMS-lib logo",
    "openms-lib-peak4-solid": "OpenMS-lib logo",
    "openms-lib-plain": "OpenMS-lib logo",
}
