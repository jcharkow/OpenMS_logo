#!/usr/bin/env python3
"""Generate the OpenMS-lib sublogos (standard + white).

Thin wrapper kept for backwards compatibility -- the logic now lives in
``openms_logo.presets.openms_lib`` / ``oms_lib`` and is built from the
per-letter / per-bar element functions. Equivalent to:

    python -m openms_logo openms-lib      # or: oms-lib

Needs fonts for the "-lib" lettering: ``python scripts/fetch_fonts.py``.
"""
import argparse

from openms_logo.__main__ import main

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=["openms", "oms"], default="openms")
    ap.add_argument("--out", default="build")
    a = ap.parse_args()
    main([f"{a.variant}-lib", "--out", a.out])
