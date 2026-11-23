#!/usr/bin/env python3
"""Render SVGs to PNG for visual review, and diff against the official logo.

    python scripts/render_check.py build/full.svg build/ms-white.svg   # -> build/png/*.png
    python scripts/render_check.py --diff                             # full logo vs official file

Needs ``rsvg-convert`` (apt install librsvg2-bin) and Pillow.
"""
import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def render(svg, png, width=800, background=None):
    cmd = ["rsvg-convert", "-w", str(width), str(svg), "-o", str(png)]
    if background:
        cmd[1:1] = ["-b", background]
    subprocess.run(cmd, check=True)


def diff():
    from PIL import Image, ImageChops
    sys.path.insert(0, str(ROOT))
    from openms_logo import compose, presets

    out = ROOT / "build" / "png"
    out.mkdir(parents=True, exist_ok=True)
    gen = out / "_generated_artboard.svg"
    gen.write_text(compose(presets.full(), viewbox="artboard"))
    render(ROOT / "OpenMS_transparent_blackFont.svg", out / "_official.png", 1684)
    render(gen, out / "_generated.png", 1684)
    a = Image.open(out / "_official.png").convert("RGBA")
    b = Image.open(out / "_generated.png").convert("RGBA")
    px = [max(p) for p in ImageChops.difference(a, b).getdata()]
    bad = sum(v > 32 for v in px)
    print(f"max channel diff {max(px)}, pixels differing >32: {bad}")
    return 1 if bad > 50 else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("svgs", nargs="*")
    ap.add_argument("--diff", action="store_true")
    ap.add_argument("--background", default="#9d9094", help="backdrop for previews (brand grey)")
    a = ap.parse_args()
    if a.diff:
        sys.exit(diff())
    out = ROOT / "build" / "png"
    out.mkdir(parents=True, exist_ok=True)
    for s in a.svgs:
        png = out / (Path(s).stem + ".png")
        render(s, png, background=a.background)
        print("wrote", png)


if __name__ == "__main__":
    main()
