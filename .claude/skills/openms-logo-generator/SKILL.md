---
name: openms-logo-generator
description: Generate the OpenMS logo or any sublogo (single letters, letter groups, bar subsets, icons, "-lib"/product variants, white versions) as SVG with the repo's openms_logo Python package. Use whenever someone asks to make, change, export, resize or re-colour an OpenMS logo or SVG, or to add new bars or lettering.
---

# Generating OpenMS logos programmatically

Read `AGENTS.md` (hard rules) first. Use the `openms-brand-guidelines` skill for any colour or font decision.

## Mental model

The logo is 6 letters and 16 bars. Each one is a function that returns an `Element`
placed in **official artboard coordinates** (viewBox `0 0 841.89 595.28`):

| Function | Piece |
|---|---|
| `letter_O`, `letter_p`, `letter_e`, `letter_n` | "Open" (Montserrat Alternates; the `n` leg is lengthened down to the bar axis on purpose) |
| `letter_M` (Montserrat), `letter_S` | "MS" |
| `bar_01`–`bar_04` | hang under O |
| `bar_05`–`bar_07` | hang under p |
| `bar_08`–`bar_10` | hang under e |
| `bar_11`–`bar_12` | stand above M |
| `bar_13`–`bar_16` | stand above S |

`letter_n_short()` is the same "n" with a normal leg, for one-line layouts. It needs fonts, and a test confirms it matches the official "n" except for the leg.

Group helpers: `bars_under_O/p/e()`, `bars_above_M/S()`, `all_bars()`, `all_letters()`.
`element("O")` and `element("bar_07")` look pieces up by name.

All bars share the axis `y = brand.BAR_AXIS_Y` (302.49), width 22.66 and pitch 37.41.
The official bar gradient is defined in artboard space and is **evaluated before translation**.
A bar you move keeps exactly the colour it has in the official logo, so don't re-colour moved bars.

## Workflow

1. **Pick or compose the pieces.**
   ```python
   from openms_logo import compose, write, elements as E, brand
   els = E.bars_above_M() + E.bars_above_S() + [E.letter_M(), E.letter_S()]
   ```
2. **Move pieces only with `translate` / `moved_to`.** Never scale or edit the paths.
   ```python
   O = E.letter_O().translate(0, brand.BASELINE_MS - brand.BASELINE_OPEN)  # onto the MS baseline
   ```
   Align text with the baselines `brand.BASELINE_OPEN` (275.73) and `brand.BASELINE_MS` (462.93), and use `Element.bounds` for spacing.
3. **New bars** (sublogos only): `E.bar(x, height, "down"|"up", axis_y=..., paint=...)`.
   Keep `BAR_WIDTH` and `BAR_PITCH`. For paint, use `E.BARS` (official gradient, evaluated at the bar's original x) or a `Gradient` built from `brand.LOGO_COLORS` in yellow → orange → pink → purple → blue order. For an example see `presets.oms_lib`.
4. **New lettering** (e.g. "-lib", "-cloud"): run `python scripts/fetch_fonts.py` once, then use
   `from openms_logo.text import logo_text; logo_text("-lib", x, baseline, scale=0.62, paint=...)`.
   It is outlined to paths and stroked to match the logo weight. `letter_gap(left, right)` gives the font's natural spacing between two logo-weight letters. Paint it with the theme ink (default) or a palette gradient. `font="montserrat"` sets a capital M that matches the logo.
5. **Write both themes.**
   ```python
   for theme in ("standard", "white"):
       write(f"build/ms-mark{'' if theme == 'standard' else '-white'}.svg", els, theme=theme, title="OpenMS MS mark")
   ```
   `compose()` options: `padding` (default `brand.CLEAR_SPACE`), `viewbox="artboard"` for the official page, and `background` (previews only; official files are transparent).
6. **Reusable variants** go in `openms_logo/presets.py`. Add a function `(theme) -> list[Element]` and register it in `PRESETS` and `TITLES`. It is then available as `python -m openms_logo <name>`.
7. **Verify** (required):
   ```bash
   python -m pytest
   python scripts/render_check.py --diff            # full logo must still match the official file
   python scripts/render_check.py build/<new>*.svg  # then LOOK at build/png/<new>.png
   ```
   Check the render for overlaps, clipped clear space, legibility at small size, and white-on-light or dark-on-dark mistakes.
8. **Publish:** only presets in `presets.PUBLISHED` go into `logos/`. If you add or change one of them, regenerate the folder (see AGENTS.md) and commit the SVGs together with the code.
9. **Report** the sublogo as derived and not yet official (it needs brand-owner approval). State which elements it uses.

## Layout patterns already built (reuse before inventing)

| Preset | Layout |
|---|---|
| `full` | the official logo |
| `open`, `ms`, `o-icon`, `bars`, `wordmark` | subsets of the official logo, in their original positions |
| `openms-lib` | the full logo with a small "-lib" after "MS" |
| `oms-lib` | "OMS" on one line with "-lib" and a new row of bars below |
| `openms-lib-spectrum`, `pyopenms-viz` | **spectrum wordmark**: "OpenMS" on one line (`one_line_openms()`). Bars 1–10, flipped to stand on an axis above "Open", run yellow → pink. A suffix on the same axis, right-aligned over "MS", runs purple → blue. An optional prefix ("py") sits before the "O". The layout follows the pyopenms_viz logo. |

| `openms-lib-square-top/-bottom/-ink` | **square stack**: "Open" over "MS lib", left-aligned. The suffix is sized so the second line is exactly as wide as "Open". Bars 1–10 are centred above "Open" (top, ink) or hang below "MS lib" (bottom). Use `presets.square_lib(theme, suffix=..., bars=..., suffix_paint=...)`. |
| `openms-lib-official-stack` | the untouched official logo with "lib" as a third line |

For a new product logo, use `presets.square_lib(...)` or `presets.spectrum_wordmark(theme, suffix="...", prefix="...")`.
Suffix gradients use lighter tints in the white theme, because #3157e9 on #231f20 is only 2.85:1.

## CLI cheatsheet

```bash
python -m openms_logo --list
python -m openms_logo full open ms o-icon bars wordmark openms-lib oms-lib
python -m openms_logo full --theme white --artboard
python -m openms_logo --elements O,p,e,n,bar_01,bar_02 --name custom --theme standard
```

## Don'ts

- Don't edit `_official_paths.py` or `OFFICIAL_BARS`. They are tested against the official SVG.
- Don't type logo letters with a live `<text>` element. Use the letter functions, or `logo_text` for characters the logo doesn't have.
- Don't introduce hex values that aren't in `brand.py`. `tests/test_official.py::test_only_brand_colours_used` checks this.
- Don't hand-edit files in `build/`. Change the code and regenerate.
