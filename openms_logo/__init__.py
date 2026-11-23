"""Programmatic OpenMS logo generator.

Quick start::

    from openms_logo import compose, presets, elements as E
    svg = compose(presets.full(), theme="standard")
    icon = compose(E.bars_under_O() + [E.letter_O()], theme="white")

See AGENTS.md and .claude/skills/ for the brand rules.
"""
from . import brand, elements, presets
from .compose import compose, write
from .elements import Element, Gradient, bar

__all__ = ["brand", "elements", "presets", "compose", "write", "Element", "Gradient", "bar"]
