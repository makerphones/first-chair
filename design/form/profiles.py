#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Jamey Warren
# SPDX-License-Identifier: MIT

"""
Cup profile explorer — form study in OUR tool, with no handoff.

Each direction is a lathe profile: a list of (radius, depth) points read from the pad
rim at depth 0 to the back face. Built as a loft of stacked circles (this OCC build's
revolve is unreliable — see docs/cadquery-build-notes.md), hollowed to a bore, and
rendered from one camera so the silhouettes compare honestly.

SILHOUETTE ONLY. No grille, no bosses, no lip chamfer, no cable exit. This answers
"what shape is it", not "what parts is it" — features come after a profile is picked.

    .venv/bin/python design/form/profiles.py            # all, contact sheet
    .venv/bin/python design/form/profiles.py cone waist # just these

Add a direction by adding an entry to PROFILES. Points must run outward from the axis
at d=0, around the outside, and back to the axis at the deepest point.
"""

import math
import os
import sys

import cadquery as cq

OUT = os.path.join(os.path.dirname(__file__), "profile-study")

# ---- The pad interface. FIXED — set from outside by the commodity Grado pad. -----
R_RIM, R_BODY, LIP, R_BORE = 27.0, 24.0, 3.0, 21.0

# ---- Directions. depth is FREE; only the rim/lip/body relationship is held. ------
# Old Faithful's earcup measured 21.6 deep, so shallower than 27.6 is precedented.
PROFILES = {
    # Straight cylinder, flat back. The most austere answer, and the baseline.
    "cylinder": [(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP),
                 (R_BODY, 27.6), (0, 27.6)],

    # Truncated cone. Prints nose-down self-supporting; mass falls away from the ear.
    "cone": [(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP),
             (R_BODY, 9.0), (14.0, 27.6), (0, 27.6)],

    # Waisted — swells then narrows. The move in the 2016 shape sketches.
    "waist": ([(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP)]
              + [(R_BODY + 1.6 * math.sin(t * math.pi) - 5.0 * (t ** 2.2), LIP + t * (27.6 - LIP))
                 for t in [i / 22 for i in range(1, 23)]]
              + [(0, 27.6)]),

    # Stepped — concentric plates, every diameter change a future parting line.
    "stepped": [(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP),
                (R_BODY, 12.0), (20.5, 12.0), (20.5, 21.0),
                (16.5, 21.0), (16.5, 25.0), (0, 25.0)],

    # Shallow + full-width back. Old Faithful was 21.6 deep; this is that read.
    "shallow": [(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP),
                (R_BODY, 18.0), (22.5, 21.6), (0, 21.6)],

    # STRAIGHT FRONT + TAPERING BACK — the maker's read: the base of `shallow` with the
    # back of `waist_split` flipped, so mass falls AWAY from the head instead of bulging
    # back out. Three taper rates; the straight section is where the part splits.
    "taper_soft": ([(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP), (R_BODY, 13.0)]
                   + [(R_BODY - 6.5 * (t ** 1.5), 13.0 + t * 12.0)
                      for t in [i / 14 for i in range(1, 15)]] + [(0, 25.0)]),
    "taper_mid": ([(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP), (R_BODY, 12.0)]
                  + [(R_BODY - 9.5 * (t ** 1.35), 12.0 + t * 12.0)
                     for t in [i / 14 for i in range(1, 15)]] + [(0, 24.0)]),
    "taper_hard": ([(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP), (R_BODY, 11.0)]
                   + [(R_BODY - 13.0 * (t ** 1.25), 11.0 + t * 11.5)
                      for t in [i / 14 for i in range(1, 15)]] + [(0, 22.5)]),

    # Bell — one continuous curve from the lip to a small back face.
    "bell": ([(0, 0), (R_RIM, 0), (R_RIM, LIP), (R_BODY, LIP)]
             + [(R_BODY * math.cos(t * math.pi / 2) ** 0.42 + 1e-3, LIP + t * (26.0 - LIP))
                for t in [i / 24 for i in range(1, 25)]]
             + [(0, 26.0)]),
}


WALL, BACK = 3.0, 4.0   # side wall, and the solid band left at the back face


def _loft(pts):
    """Loft stacked circles through (radius, depth) points."""
    wires, seen = [], set()
    for r, d in pts:
        while round(d, 4) in seen:
            d += 1e-3
        seen.add(round(d, 4))
        wires.append(cq.Wire.makeCircle(max(r, 0.05), cq.Vector(0, 0, d), cq.Vector(0, 0, 1)))
    return cq.Workplane(obj=cq.Solid.makeLoft(wires, ruled=True))


def build(points):
    """Solid of revolution from the profile, hollowed by an INSET copy of itself.

    The bore follows the outer profile inward by WALL rather than being a straight
    cylinder — a constant bore breaks clean through any profile that tapers below
    R_BORE + WALL, which silently turned cone/bell/stepped into broken solids in the
    first run. Offsetting the profile keeps a real wall on every direction, which is
    also the honest thing to compare: these are shells, not billets.
    """
    outer = [(r, d) for r, d in points if r > 1e-6]
    depth = max(d for _, d in points)
    solid = _loft(outer)

    # RESAMPLE the outer envelope before offsetting. Offsetting the raw point list
    # fails wherever two points straddle a long taper: the inner wall interpolates
    # straight between them and punches through the shrinking outer wall. cone/bell
    # did exactly that. Sample r(d) densely, then inset.
    floor = depth - BACK

    def outer_r(d):
        """Largest radius the profile reaches at this depth."""
        best = 0.0
        for (r0, d0), (r1, d1) in zip(outer, outer[1:]):
            if min(d0, d1) - 1e-9 <= d <= max(d0, d1) + 1e-9:
                t = 0.0 if abs(d1 - d0) < 1e-9 else (d - d0) / (d1 - d0)
                best = max(best, r0 + t * (r1 - r0))
        return best

    n = 20                                     # 60+ sections makes OCC refuse the loft
    inner = [(min(outer_r(floor * i / n) - WALL, R_BORE), floor * i / n)
             for i in range(n + 1)]
    inner = [(r, d) for r, d in inner if r > 1.0]
    try:
        if len(inner) < 2:
            raise ValueError("profile too narrow to bore")
        return solid.cut(_loft([(inner[0][0], -1.0)] + inner))
    except Exception as e:                     # noqa: BLE001 — degrade, don't lose the part
        # Fall back to a straight bore sized so it cannot breach the narrowest wall.
        r_safe = max(1.5, min(outer_r(floor * i / n) for i in range(n + 1)) - WALL)
        print(f"         (profiled bore failed — {e}; straight Ø{2*r_safe:.1f} bore instead)")
        return solid.cut(cq.Workplane("XY").circle(r_safe).extrude(floor))


def main(names):
    os.makedirs(OUT, exist_ok=True)
    made = []
    for name in names:
        try:
            solid = build(PROFILES[name])
            path = os.path.join(OUT, f"{name}.stl")
            cq.exporters.export(solid, path)
            v = solid.val().Volume() / 1000.0
            bb = solid.val().BoundingBox()
            print(f"  [ok]   {name:10} {bb.xlen:5.1f} × {bb.ylen:5.1f} × {bb.zlen:5.1f} mm"
                  f"   {v:6.1f} cm³ solid   ≈{v * 1.27 * 0.55:5.1f} g PETG")
            made.append((name, path))
        except Exception as e:  # noqa: BLE001 — report, don't mask
            print(f"  [FAIL] {name}: {e}")
    return made


if __name__ == "__main__":
    picks = sys.argv[1:] or list(PROFILES)
    print(f"Cup profile study — {len(picks)} direction(s)\n")
    main(picks)
    print(f"\nSTLs in {OUT}")
