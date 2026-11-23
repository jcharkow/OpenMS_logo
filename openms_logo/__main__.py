"""CLI: ``python -m openms_logo``.

Examples::

    python -m openms_logo full                       # build/full.svg + build/full-white.svg
    python -m openms_logo open ms --theme white
    python -m openms_logo --elements O,bar_01,bar_02,bar_03,bar_04 --name my-icon
    python -m openms_logo full --artboard            # official 841.89x595.28 page
    python -m openms_logo --list
"""
from __future__ import annotations

import argparse
from pathlib import Path

from . import elements as E
from .compose import THEMES, write
from .presets import PRESETS, TITLES


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m openms_logo", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("presets", nargs="*", help=f"one or more of: {', '.join(PRESETS)}")
    ap.add_argument("--elements", help="comma-separated element names (O,p,e,n,M,S,bar_01..bar_16)")
    ap.add_argument("--name", default="custom", help="output stem for --elements")
    ap.add_argument("--theme", choices=[*THEMES, "both"], default="both")
    ap.add_argument("--out", default="build", help="output directory (default: build/)")
    ap.add_argument("--padding", type=float, default=None, help="clear space (default brand.CLEAR_SPACE)")
    ap.add_argument("--artboard", action="store_true", help="use the official 841.89x595.28 viewBox")
    ap.add_argument("--background", help="draw a backdrop colour (previews only)")
    ap.add_argument("--list", action="store_true", help="list presets and elements")
    a = ap.parse_args(argv)

    if a.list:
        print("presets: ", ", ".join(PRESETS))
        print("letters: ", ", ".join(E.LETTERS))
        print("bars:     bar_01 .. bar_16")
        return

    jobs = [(p, PRESETS[p], TITLES[p]) for p in a.presets]
    if a.elements:
        names = [n.strip() for n in a.elements.split(",") if n.strip()]
        jobs.append((a.name, lambda theme, names=names: [E.element(n) for n in names], f"OpenMS {a.name}"))
    if not jobs:
        ap.error("give a preset or --elements (see --list)")

    themes = THEMES if a.theme == "both" else (a.theme,)
    kw = {}
    if a.padding is not None:
        kw["padding"] = a.padding
    if a.artboard:
        kw["viewbox"] = "artboard"
    for stem, fn, title in jobs:
        for theme in themes:
            suffix = "" if theme == "standard" else f"-{theme}"
            path = Path(a.out) / f"{stem}{suffix}.svg"
            write(path, fn(theme), theme=theme, title=title, background=a.background, **kw)
            print("wrote", path)


if __name__ == "__main__":
    main()
