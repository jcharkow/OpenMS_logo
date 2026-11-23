"""The generator must reproduce the official logo exactly. Run: python -m pytest"""
import re
from pathlib import Path

import pytest

from openms_logo import brand, compose, presets
from openms_logo import elements as E

OFFICIAL = (Path(__file__).resolve().parent.parent / "OpenMS_transparent_blackFont.svg").read_text()


def test_letter_paths_are_verbatim():
    official = re.findall(r'<path[^>]*class="cls-2"[^>]*\sd="([^"]+)"', OFFICIAL)
    ours = [d for ch in "OpenMS" for d in re.findall(r'd="([^"]+)"', E.LETTERS[ch]().markup)]
    assert ours == official


def test_bars_match_official_geometry():
    from fontTools.pens.recordingPen import RecordingPen
    from fontTools.svgLib.path import parse_path

    d = re.search(r'class="cls-1" d="([^"]+)"', OFFICIAL).group(1)
    pen = RecordingPen()
    parse_path(d, pen)
    rects, cur = [], []
    for op, args in pen.value:
        if op == "moveTo":
            cur = [args[0]]
        elif op == "lineTo":
            cur.append(args[0])
        elif op in ("closePath", "endPath"):
            xs, ys = zip(*cur)
            rects.append((min(xs), min(ys), max(xs), max(ys)))
    ours = [b.bbox for b in E.all_bars()]
    assert len(ours) == len(rects) == 16
    for a, b in zip(ours, rects):
        assert a == pytest.approx(b, abs=0.02)


def test_official_gradient():
    m = re.search(r'<linearGradient id="linear-gradient" x1="([\d.]+)"[^>]*x2="([\d.]+)"', OFFICIAL)
    assert (float(m.group(1)), float(m.group(2))) == brand.BAR_GRADIENT_X
    stops = re.findall(r'<stop offset="([\d.]+)" stop-color="(#\w+)"', OFFICIAL)
    assert tuple((float(o), c) for o, c in stops) == brand.BAR_GRADIENT_STOPS


@pytest.mark.parametrize("theme", ["standard", "white"])
@pytest.mark.parametrize("name", [p for p in presets.PRESETS if "lib" not in p])
def test_presets_compose(name, theme):
    svg = compose(presets.PRESETS[name](theme), theme=theme)
    assert svg.startswith("<?xml")
    assert brand.INK[theme] in svg or "url(#openms-bars)" in svg


def test_only_brand_colours_used():
    allowed = {c for v in brand.PALETTE.values() for c in v} | {c for _, c in brand.BAR_GRADIENT_STOPS}
    for name, fn in presets.PRESETS.items():
        if "lib" in name:
            continue
        for theme in ("standard", "white"):
            used = set(re.findall(r'#[0-9a-fA-F]{6}\b', compose(fn(theme), theme=theme)))
            assert used <= allowed, (name, used - allowed)


FONTS = Path(__file__).resolve().parent.parent / "fonts" / "MontserratAlternates-Regular.ttf"


@pytest.mark.skipif(not FONTS.exists(), reason="run scripts/fetch_fonts.py")
def test_short_n_matches_official_n_except_leg():
    off, short = E.letter_n().bbox, E.letter_n_short().bbox
    assert short[:3] == pytest.approx(off[:3], abs=0.05)          # same left, top, right
    assert short[3] == pytest.approx(brand.BASELINE_OPEN + brand.GLYPH_STROKE / 2, abs=0.05)


@pytest.mark.skipif(not FONTS.exists(), reason="run scripts/fetch_fonts.py")
@pytest.mark.parametrize("name", [n for n in presets.PRESETS if "lib" in n or "viz" in n])
def test_lettering_presets_compose(name):
    for theme in ("standard", "white"):
        assert compose(presets.PRESETS[name](theme), theme=theme).startswith("<?xml")


@pytest.mark.skipif(not FONTS.exists(), reason="run scripts/fetch_fonts.py")
@pytest.mark.parametrize("name", presets.PUBLISHED)
def test_logos_dir_up_to_date(name):
    logos = Path(__file__).resolve().parent.parent / "logos"
    for theme, suffix in (("standard", ""), ("white", "-white")):
        expected = compose(presets.PRESETS[name](theme), theme=theme, title=presets.TITLES[name])
        assert (logos / f"{name}{suffix}.svg").read_text() == expected, \
            f"logos/{name}{suffix}.svg is stale -- regenerate (see AGENTS.md)"


def test_logos_dir_has_only_published():
    logos = Path(__file__).resolve().parent.parent / "logos"
    expected = {f"{n}{s}.svg" for n in presets.PUBLISHED for s in ("", "-white")}
    assert {p.name for p in logos.glob("*.svg")} == expected
