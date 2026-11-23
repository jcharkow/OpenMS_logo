"""Assemble :class:`~openms_logo.elements.Element` objects into an SVG document."""
from __future__ import annotations

from html import escape
from pathlib import Path

from . import brand
from .elements import BAR_GRADIENT, BARS, INK, Element, Gradient

THEMES = tuple(brand.INK)   # ("standard", "white")


def _paint(el: Element, theme: str) -> tuple[str, Gradient | None]:
    p = el.paint
    if p == INK:
        return brand.INK[theme], None
    if p == BARS:
        return f"url(#{BAR_GRADIENT.id})", BAR_GRADIENT
    if isinstance(p, Gradient):
        return f"url(#{p.id})", p
    return str(p), None


def bounds(elements) -> tuple[float, float, float, float]:
    boxes = [e.bounds for e in elements]
    return (min(b[0] for b in boxes), min(b[1] for b in boxes),
            max(b[2] for b in boxes), max(b[3] for b in boxes))


def compose(elements, *, theme: str = "standard", title: str = "OpenMS logo",
            padding: float = brand.CLEAR_SPACE, viewbox=None,
            background: str | None = None) -> str:
    """Return an SVG string.

    ``theme``: ``"standard"`` (dark letters, light backdrop) or ``"white"``
    (white letters, dark backdrop). ``viewbox``: ``None`` = tight bbox plus
    ``padding``; ``"artboard"`` = official 841.89x595.28 page; or a 4-tuple.
    ``background``: optional fill for a backdrop rect (previews only -- the
    official files are transparent).
    """
    if theme not in brand.INK:
        raise ValueError(f"theme must be one of {THEMES}")
    elements = list(elements)
    if not elements:
        raise ValueError("nothing to draw")

    if viewbox == "artboard":
        vb = brand.ARTBOARD
    elif viewbox is None:
        x0, y0, x1, y1 = bounds(elements)
        vb = (x0 - padding, y0 - padding, x1 - x0 + 2 * padding, y1 - y0 + 2 * padding)
    else:
        vb = tuple(viewbox)

    grads: dict[str, Gradient] = {}
    body = []
    for el in elements:
        fill, grad = _paint(el, theme)
        if grad is not None:
            grads[grad.id] = grad
        attrs = f' id="{escape(el.name)}" fill="{fill}"'
        if el.kind == "text":
            attrs += f' stroke="{fill}"'
        if el.dx or el.dy:
            attrs += f' transform="translate({el.dx:.2f} {el.dy:.2f})"'
        body.append(f"  <g{attrs}>{el.markup}</g>")

    defs = "".join(g.to_svg() for g in grads.values())
    bg = ""
    if background:
        bg = (f'  <rect x="{vb[0]:.2f}" y="{vb[1]:.2f}" width="{vb[2]:.2f}" '
              f'height="{vb[3]:.2f}" fill="{background}"/>\n')
    vb_s = " ".join(f"{v:.2f}" for v in vb)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb_s}" role="img" aria-labelledby="title">\n'
        f'  <title id="title">{escape(title)}</title>\n'
        + (f"  <defs>{defs}</defs>\n" if defs else "")
        + bg
        + "\n".join(body)
        + "\n</svg>\n"
    )


def write(path, elements, **kw) -> Path:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(compose(elements, **kw), encoding="utf-8")
    return path
