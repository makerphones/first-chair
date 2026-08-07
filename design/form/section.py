#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2026 Jamey Warren
# SPDX-License-Identifier: MIT

"""
Cup section — does the front piece hold the driver, and what's left over?

Draws the chosen profile in section with the driver, the pad and the ear plane in
place, so the depth budget is visible rather than argued about. 2D on purpose: a
section reads a stack far better than a render does.

    .venv/bin/python design/form/section.py
"""

import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

sys.path.insert(0, os.path.dirname(__file__))
from profiles import PROFILES, R_RIM, R_BODY, LIP, WALL, BACK  # noqa: E402

OUT = os.path.join(os.path.dirname(__file__), "profile-study")

# ---- Driver. MEASURED unless noted. ---------------------------------------------
DRV_OD, DRV_R = 39.5, 39.5 / 2
DRV_BASKET = 5.0          # MEASURED  depth behind the mounting flange
DRV_DOME = 1.5            # ASSUMPTION  dome standing proud of the flange
DRV_EXC = 0.5             # ASSUMPTION  one-way excursion beyond the dome
DRV_SEAT = 3.5            # DESIGN     flange plane, measured back from the cup face

# ---- Pad + ear. The pad is commodity; these are estimates pending a caliper. -----
PAD_OPEN_R = 19.0         # ESTIMATE  pad opening radius
PAD_WORN = 5.5            # SET       compressed cup-face → ear gap when worn

CASES = [("taper_soft", 13.0), ("taper_mid", 12.0)]


def envelope(points):
    return [(d, r) for r, d in points if r > 1e-6]


def draw(ax, name, split):
    pts = envelope(PROFILES[name])
    depth = max(d for d, _ in pts)

    # outer wall, mirrored top and bottom
    for sign in (1, -1):
        ax.plot([d for d, _ in pts], [sign * r for _, r in pts],
                color="#2d3748", lw=1.9, zorder=3)
    # inner wall — the outer inset by WALL, floored at the back band
    floor = depth - BACK
    inner = [(d, max(min(r - WALL, R_BODY - WALL), 0.5)) for d, r in pts if d <= floor]
    for sign in (1, -1):
        ax.plot([d for d, _ in inner], [sign * r for _, r in inner],
                color="#8b93a1", lw=1.2, ls=(0, (5, 3)), zorder=3)

    # the split
    ax.axvline(split, color="#c2410c", lw=1.6, zorder=4)
    ax.text(split, R_RIM + 5.5, f"split {split:.0f}", color="#c2410c",
            ha="center", fontsize=9, weight="bold")

    # driver — one rectangle in section; dome + excursion band in front of the flange
    ax.add_patch(Rectangle((DRV_SEAT, -DRV_R), DRV_BASKET, 2 * DRV_R,
                           facecolor="#4a5568", edgecolor="#2d3748", lw=1.0, zorder=4))
    ax.add_patch(Rectangle((DRV_SEAT - DRV_DOME - DRV_EXC, -13.5),
                           DRV_DOME + DRV_EXC, 27.0,
                           facecolor="#c2410c", alpha=0.35, edgecolor="none", zorder=2))
    ax.text(DRV_SEAT + DRV_BASKET / 2, 0, "driver\n\u00d839.5 \u00d7 5.0", color="white",
            ha="center", va="center", fontsize=8, weight="bold", zorder=5)
    ax.text(DRV_SEAT - DRV_DOME - DRV_EXC - 0.5, 16.5, "dome+exc\n2.0", color="#c2410c",
            ha="right", va="center", fontsize=7.5)

    # pad + ear
    ax.add_patch(Rectangle((-PAD_WORN, PAD_OPEN_R), PAD_WORN, R_RIM - PAD_OPEN_R,
                           facecolor="#1a202c", alpha=0.55, edgecolor="none"))
    ax.add_patch(Rectangle((-PAD_WORN, -R_RIM), PAD_WORN, R_RIM - PAD_OPEN_R,
                           facecolor="#1a202c", alpha=0.55, edgecolor="none"))
    ax.axvline(-PAD_WORN, color="#0f766e", lw=1.4, ls=(0, (2, 2)))
    ax.text(-PAD_WORN - 1.0, 0, "ear", color="#0f766e", ha="right", va="center",
            fontsize=10, weight="bold")

    # the number that answers the question
    tail = split - (DRV_SEAT + DRV_BASKET)
    cav = PAD_WORN + DRV_SEAT - DRV_DOME - DRV_EXC
    ax.annotate("", xy=(DRV_SEAT + DRV_BASKET, -R_RIM - 3), xytext=(split, -R_RIM - 3),
                arrowprops=dict(arrowstyle="<->", color="#0f766e", lw=1.3))
    ax.text((DRV_SEAT + DRV_BASKET + split) / 2, -R_RIM - 6.5,
            f"{tail:.1f} spare", color="#0f766e", ha="center", fontsize=9, weight="bold")

    ax.set_title(f"{name}  ·  {depth:.1f} deep  ·  front cavity {cav:.1f} mm  ·  "
                 f"{tail:.1f} mm behind the driver",
                 color="#2d3748", fontsize=11.5, pad=8)
    ax.set_xlim(-11, depth + 4); ax.set_ylim(-R_RIM - 9, R_RIM + 9)
    ax.set_aspect("equal"); ax.axis("off")
    return tail, cav


def main():
    os.makedirs(OUT, exist_ok=True)
    fig, axes = plt.subplots(1, len(CASES), figsize=(7.2 * len(CASES), 6.4), dpi=125)
    for ax, (name, split) in zip(axes, CASES):
        t, c = draw(ax, name, split)
        print(f"  {name:12} split {split:4.1f}   front cavity {c:4.1f} mm   "
              f"{t:4.1f} mm behind the driver")
    fig.suptitle("Cup section · driver Ø39.5 × 5.0 MEASURED · dome 1.5 + excursion 0.5 ASSUMED · "
                 "pad worn gap 5.5", color="#2d3748", fontsize=12.5, y=0.98)
    p = os.path.join(OUT, "_section.png")
    fig.savefig(p, facecolor="white", bbox_inches="tight", pad_inches=0.35)
    print(f"\n  wrote {p}")


if __name__ == "__main__":
    print("Cup section — depth budget\n")
    main()
