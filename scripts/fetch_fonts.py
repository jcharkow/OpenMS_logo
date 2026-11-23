#!/usr/bin/env python3
"""Download the brand fonts (SIL OFL, from github.com/google/fonts) into fonts/.

Only needed for new lettering (openms_logo.text) and for mock-ups; the
official logo letters are stored as outlines and need no font.
"""
import sys
import urllib.request
from pathlib import Path

BASE = "https://github.com/google/fonts/raw/main/ofl/"
FILES = {
    # logo lettering (Regular + stroke reproduces the logo weight, see brand.py)
    "MontserratAlternates-Regular.ttf": "montserratalternates/MontserratAlternates-Regular.ttf",
    "MontserratAlternates-SemiBold.ttf": "montserratalternates/MontserratAlternates-SemiBold.ttf",
    # headings / logo capital M (variable font, all weights)
    "Montserrat[wght].ttf": "montserrat/Montserrat%5Bwght%5D.ttf",
    # body text
    "Raleway[wght].ttf": "raleway/Raleway%5Bwght%5D.ttf",
    # quotes / callouts
    "JetBrainsMono[wght].ttf": "jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf",
    # special purposes
    "ChakraPetch-Bold.ttf": "chakrapetch/ChakraPetch-Bold.ttf",
}


def main(dest="fonts"):
    out = Path(dest)
    out.mkdir(exist_ok=True)
    for name, rel in FILES.items():
        p = out / name
        if p.exists():
            continue
        print("fetching", name)
        urllib.request.urlretrieve(BASE + rel, p)
    # static Regular instance of Montserrat for a logo-matching capital "M"
    reg = out / "Montserrat-Regular.ttf"
    if not reg.exists():
        from fontTools.ttLib import TTFont
        from fontTools.varLib.instancer import instantiateVariableFont
        instantiateVariableFont(TTFont(out / "Montserrat[wght].ttf"), {"wght": 400}).save(reg)
    print("fonts in", out.resolve())


if __name__ == "__main__":
    main(*sys.argv[1:])
