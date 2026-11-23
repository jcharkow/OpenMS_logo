# AGENTS.md: OpenMS logo repository

This repo holds the official OpenMS logo and the Python code that draws it and
its sublogos. **Every task here follows the OpenMS Corporate Design guidelines**
(`OpenMS_CorporateDesign_current.pdf`). The constants in
`openms_logo/brand.py` encode those guidelines, so read that file first.

## Skills (read the one that matches your task)

| Skill | Use it for |
|---|---|
| `.claude/skills/openms-brand-guidelines/SKILL.md` | colours, fonts, logo usage, accessibility, print: **any** design decision |
| `.claude/skills/openms-logo-generator/SKILL.md` | making or changing logo SVGs, sublogos, new bars or new lettering |

## Hard rules

1. **Generate every SVG with the `openms_logo` package.** Don't hand-edit SVG
   output, and don't paste path data into a new file. Compose from the element
   functions (`letter_O()` … `letter_S()`, `bar_01()` … `bar_16()`, `bar()`,
   `logo_text()`).
2. **Never modify the official letterforms or bar geometry.** The letter
   outlines in `openms_logo/_official_paths.py` and `OFFICIAL_BARS` in
   `elements.py` are verbatim copies of `OpenMS_transparent_blackFont.svg`.
   You may translate them, but don't scale, skew, recolour or redraw them.
   Scale the whole SVG instead (it is a vector).
3. **Use only brand colours** from `brand.PALETTE` / `brand.LOGO_COLORS`.
   Letters are `#231f20` (standard theme, light backdrops) or `#ffffff` (white
   theme, dark backdrops). Bars use the official gradient (`paint=BARS`).
4. **Only two official logo versions exist:** standard and white (`presets.full`).
   Everything else is a *derived sublogo*. Label it as one, and tell the user
   that the brand owner must approve it before it is published. The PDF says
   "Do not use any other logo versions."
5. **Keep clear space** around the artwork (default `brand.CLEAR_SPACE`), and
   don't place the logo below a readable size.
6. **New lettering** (e.g. "-lib") must use `openms_logo.text.logo_text`. It sets
   Montserrat Alternates at the measured logo weight. A capital M uses Montserrat.
7. **Check your work:** run `python -m pytest`, run
   `python scripts/render_check.py --diff` (the full logo must match the
   official file), and look at a PNG render of every new or changed SVG.
   Do this before you report that you are done.

## Layout

```
OpenMS_transparent_blackFont.svg   official logo (source of truth for geometry)
OpenMS_CorporateDesign_current.pdf brand guidelines (source of truth for rules)
openms_logo/
  brand.py            colours, CMYK, fonts, measured logo geometry
  _official_paths.py  verbatim letter outlines (generated, never edit)
  elements.py         Element model; letter_*/bar_* functions; bar(); group helpers
  text.py             logo-weight lettering from fonts (outlined, no font deps in output)
  compose.py          compose()/write(): elements -> SVG (themes, viewBox, gradients)
  presets.py          full, wordmark, bars, open, ms, o-icon, openms-lib, oms-lib,
                      openms-lib-spectrum, pyopenms-viz (spectrum_wordmark for new products)
  __main__.py         CLI (python -m openms_logo --help)
scripts/fetch_fonts.py   downloads the brand fonts (OFL) into fonts/ (git-ignored)
scripts/render_check.py  PNG previews + pixel diff against the official logo
tests/                   reproduction tests (pytest)
logos/                   generated SVGs for every preset (committed; never hand-edit)
make_openms_lib.py       legacy entry point -> presets openms-lib / oms-lib
```

## Setup and commands

```bash
pip install -r requirements.txt -r requirements-dev.txt
python scripts/fetch_fonts.py                  # only needed for new lettering
python -m openms_logo --list
python -m openms_logo full open ms             # -> build/<name>.svg and build/<name>-white.svg
python -m openms_logo --elements O,bar_01,bar_02,bar_03,bar_04 --name o-icon
python -m pytest
python scripts/render_check.py --diff
python scripts/render_check.py build/*.svg     # PNGs in build/png/ (needs librsvg2-bin)
```

`build/` and `fonts/` are git-ignored. The published SVGs live in `logos/`.
Every preset there comes in both themes, as `<preset>.svg` and `<preset>-white.svg`.
After you change the code or add a preset, regenerate them:

```bash
python -m openms_logo $(python -c "from openms_logo.presets import PRESETS; print(*PRESETS)") --out logos
```

`tests/test_official.py::test_logos_dir_up_to_date` fails if `logos/` is stale.
Except for `logos/full*.svg`, everything in `logos/` is a derived sublogo and is not yet official.

## Known discrepancies (don't "fix" these silently)

- The PDF calls the logo letters "SemiBold + 0.5 stroke". The official
  outlines measure as Montserrat Alternates **Regular @ 192.2 units + 11.88
  stroke**, which gives the same visual weight. `brand.GLYPH_SIZE` and
  `brand.GLYPH_STROKE` encode the measured values.
- The PDF lists `#ffcb4f` as the logo yellow, but the official SVG gradient
  starts at `#ffb401`. Reproduce the SVG exactly (`brand.BAR_GRADIENT_STOPS`).
