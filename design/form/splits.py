#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Jamey Warren
# SPDX-License-Identifier: MIT

"""
Where does the cup split? — a study of the PART BREAK, not the silhouette.

Takes a profile from profiles.py and cuts it into a FRONT piece (pad rim + integrated
baffle + driver seat) and a REAR cup, so the parting line can be judged as a design
feature rather than discovered as a seam.

The architecture being tested:

    FRONT   pad rim, baffle and driver seat in ONE printed part. The driver is
            registered concentric to the pad by geometry rather than by assembly —
            no bolt circle, no four insert positions to align.
    REAR    the acoustic variable: open area, volume, damping. This is the part a
            builder iterates on and swaps, which makes open-vs-closed a PART rather
            than a parameter.
    DRIVER  loads from the rear, seats against the back of the front piece.

Both halves print open-side-down with no supports, which is the point of splitting
here rather than anywhere else.

    .venv/bin/python design/form/splits.py
"""

import os
import sys

import cadquery as cq

sys.path.insert(0, os.path.dirname(__file__))
from profiles import PROFILES, R_RIM, R_BODY, R_BORE, LIP, WALL, BACK, _loft, build  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "profile-study")

# A TRUE waist — the rendered "waist" only swells then tapers. This one pinches, so the
# parting line has somewhere to hide. Radii: 24 at the lip → 25.2 swell → 21.4 pinch →
# 23.6 flare at the back. The pinch is the split.
PROFILES["waist_split"] = [
    (0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP),
    (25.2, 8.0), (24.6, 11.0), (21.4, 15.5),          # ← pinch
    (22.8, 19.5), (23.6, 24.0), (22.0, 27.0), (0, 27.0),
]

# (profile, split depth, why there)
CASES = [
    ("shallow", 11.0, "behind the driver seat, on the last straight section"),
    ("waist_split", 15.5, "at the pinch — the narrowest point, where a line reads as intent"),
]


def halves(name, z_split):
    solid = build(PROFILES[name])
    depth = max(d for _, d in PROFILES[name])
    big = 60.0
    front = solid.cut(cq.Workplane("XY").workplane(offset=z_split)
                      .circle(big).extrude(depth + 10))
    rear = solid.cut(cq.Workplane("XY").workplane(offset=z_split - (depth + 10))
                     .circle(big).extrude(depth + 10))
    return front, rear, depth


def main():
    os.makedirs(OUT, exist_ok=True)
    for name, z, why in CASES:
        f, r, depth = halves(name, z)
        for tag, part in (("front", f), ("rear", r)):
            p = os.path.join(OUT, f"split-{name}-{tag}.stl")
            cq.exporters.export(part, p)
        fv = f.val().Volume() / 1000.0
        rv = r.val().Volume() / 1000.0
        print(f"  {name:12} split @ {z:4.1f} of {depth:4.1f} mm  —  {why}")
        print(f"  {'':12} front {fv:5.1f} cm³ (≈{fv*1.27*0.55:4.1f} g)   "
              f"rear {rv:5.1f} cm³ (≈{rv*1.27*0.55:4.1f} g)\n")


if __name__ == "__main__":
    print("Cup split study — where does the part break?\n")
    main()
    print(f"STLs in {OUT}")
