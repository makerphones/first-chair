# SPDX-FileCopyrightText: 2026 Jamey Warren
# SPDX-License-Identifier: MIT

"""
Cup shell — the heart of First Chair (v0.3 engineering pass).

Build order: acoustic void → shell → clean concentric grille (decoupled from the
bosses) → 4 wall-blended baffle bosses (front-facing heat-set bore) → 2 external
yoke pivot bosses on the side walls (radial heat-set bore for the fork shoulder
screw). Every dimension is an ESTIMATE flagged in params.py — measured values
overwrite cleanly.

Reconciled to design-spec.md v0.3: the baffle bosses moved OFF the grille and
into the perimeter wall, so the grille's outer ring is now its own radius
(P.grille_outer_ring_radius), no longer pinned to the boss circle.
"""

import math

import cadquery as cq
from params import P


def make_cup() -> cq.Workplane:
    # THE CUP IS THE Ø48 BODY, NOT THE Ø54 PLATE. This distinction is the whole profile:
    # cup_outer_diameter (54.0) is the front PLATE / pad-mount rim, and cup_body_diameter
    # (48.0) is the shell behind it that the pad actually grips. Building the shell at 54
    # — as this file did on the fork, because on Daily Driver the cup's OD *was* its body —
    # gave a 6 mm wall while params.cup_wall_thickness correctly reported the real 3.0, and
    # deleted the step the pad hooks behind. Same inherited-semantics failure as the wall
    # number itself, one level down in the geometry.
    body_d = P.cup_body_diameter
    body_h = P.cup_body_height          # everything below the overhanging front lip
    total_h = P.cup_total_height        # = cup_depth, LOCKED 27.6, lip included

    # 1. Solid blank — the front (+Z) stays a CYLINDER (pad grip + void + pivot bosses); the rear
    #    cup_dome_height flows into a CONVEX DOMED back (DT880/Denon family) that bulges from the body
    #    OD at the dome top inward to a FLAT grille face of cup_back_face_radius at z=0 (the grille /
    #    closed-back ports sit on that flat). Lofted stacked circles — a sin profile so the dome meets
    #    the cylinder tangent-vertical (smooth) and bulges convex below.
    #
    #    The dome is now capped at cup_back_thickness (derived), so it lives entirely inside the solid
    #    back band and the wall above the void floor is a clean 3.0 mm cylinder. At the inherited
    #    12.0 the taper ran 6 mm past the floor and thinned that wall; and with the inherited
    #    cup_back_face_radius of 35.0 — larger than this cup's body radius — the loft ran the wrong
    #    way entirely and flared the back out to Ø70.
    dome_h = P.cup_dome_height
    r_back = P.cup_back_face_radius
    nseg = 16                                          # dense sampling → smooth dome under a RULED loft
    wires = []
    for i in range(nseg + 1):
        t = i / nseg
        r = r_back + (body_d / 2 - r_back) * math.sin(t * math.pi / 2)  # convex; vertical tangent at the top
        wires.append(cq.Wire.makeCircle(r, cq.Vector(0, 0, dome_h * t), cq.Vector(0, 0, 1)))
    wires.append(cq.Wire.makeCircle(body_d / 2, cq.Vector(0, 0, body_h), cq.Vector(0, 0, 1)))  # cylinder to the lip
    # RULED (straight between sections) — a smooth/spline loft overshoots and bulges the dome way out.
    cup = cq.Workplane(obj=cq.Solid.makeLoft(wires, ruled=True))

    # 2. Hollow the acoustic void from the front (+Z), leaving side walls of
    #    wall_thickness and a thicker closed back (cup_back_thickness) — the grille
    #    substrate the chamfer lives in. Explicit cut (not shell) so the back band
    #    can be thicker than the side wall.
    void_r = P.cup_interior_diameter / 2
    void = (
        cq.Workplane("XY").workplane(offset=P.cup_back_thickness)
        .circle(void_r).extrude(total_h)          # up through the open front (and beyond)
    )
    cup = cup.cut(void)
    body_r = body_d / 2
    body_cyl = cq.Workplane("XY").circle(body_r).extrude(body_h)   # clip stock for the bosses (step 4)

    # 2b. Soften the back-FACE edge: a small round where the convex dome meets the flat grille face
    #     (the dome itself does the main rounding now). Done HERE while the bottom is still a clean disc —
    #     OCC on this build declines fillets once the grille/bosses/flange complicate it.
    cup = cup.edges("<Z").fillet(P.cup_back_round)

    # 3. Rear STRUCTURAL GRILLE (Stage 1b) — a rigid TRIANGULAR ×3 lattice (three
    #    opposing bar layers at 0/60/120°) that carries the protection + stiffness,
    #    with the LOGO rings + dot riding FLUSH on top (single colour, co-planar). This
    #    inverts the old logo-as-structure grille: the mesh is the structure, the logo
    #    is decoration. Built as a "keep" union of solid members; the COMPLEMENT
    #    (zone disc − keep) is cut from the closed back so the members stay and the
    #    gaps open to the driver. Cut BEFORE the bosses so nothing slices a boss.
    r_out = P.grille_outer_ring_radius
    hub_r = P.grille_hub_diameter / 2
    # The zone is the GRILLE ZONE — derived from the void (see params) — not the logo's outer
    # edge. This read `r_out + outer_ring_width/2`, which was a correct way to say "the zone"
    # only while the mark filled it. With the mark scaled inside the zone the two diverge, and
    # the old expression cut a hole the size of the LOGO and left everything out to the wall
    # solid: a 6 mm-thick back plate with a small badge punched in it, measuring 0.075 open.
    zone_r = P.grille_zone_radius

    z0 = -1.0
    cut_h = P.cup_back_thickness + 2.0          # pierce the full (thicker) back band

    def _disc(radius):
        return cq.Workplane("XY").workplane(offset=z0).circle(radius).extrude(cut_h)

    def _ring(rc, rw):
        return (cq.Workplane("XY").workplane(offset=z0)
                .circle(rc + rw / 2).circle(max(rc - rw / 2, 0.01)).extrude(cut_h))

    zone = _disc(zone_r)

    # Structural triangular lattice FIRST (the mesh behind the logo). Parallel bars of
    # grille_lattice_member_width at grille_lattice_pitch, centred on the hub, in three
    # opposing layers. Bars run past the zone; the complement-cut trims them to the disc.
    mw = P.grille_lattice_member_width
    pitch = P.grille_lattice_pitch
    nbar = int(math.ceil(zone_r / pitch)) + 1
    keep = None
    for a in P.grille_lattice_angles:
        for k in range(-nbar, nbar + 1):
            bar = (cq.Workplane("XY").workplane(offset=z0)
                   .transformed(rotate=(0, 0, a))
                   .center(0, k * pitch)
                   .rect(2 * zone_r + pitch, mw)
                   .extrude(cut_h))
            keep = bar if keep is None else keep.union(bar)

    # LOGO on top — two concentric rings + the centre dot, flush in the same plane.
    keep = keep.union(_ring(P.grille_inner_ring_radius, P.grille_inner_ring_width))
    keep = keep.union(_ring(r_out, P.grille_outer_ring_width))
    keep = keep.union(_disc(hub_r))             # centre dot (logo)

    # Open the grille: cut the COMPLEMENT of the keep-solids from the closed back band, so the
    # members stay and the gaps open to the driver.
    #
    # This used to branch on a cup_open_back toggle, with the else-branch replacing the grille
    # with a solid back and a ring of pluggable tuning ports. That variant was removed 2026-08-07
    # — it doesn't fit at 54 mm (see the note in params), and Session is the line's closed-back
    # product, so First Chair does not need its own closed-back conversion.
    cup = cup.cut(zone.cut(keep))

    # 3c. DAMPING retaining RING — a thin ring on the interior back floor that locates a
    #     felt / open-cell disc over the grille (light rear damping; the felt is a soft good,
    #     BOM). Sits inside the baffle-boss circle (r35) so it never fouls a boss; embedded
    #     0.5 mm into the floor so it fuses to the solid lattice members in open-back mode.
    dfr = P.damping_felt_diameter / 2
    ring = (cq.Workplane("XY").workplane(offset=P.cup_interior_floor_z - 0.5)
            .circle(dfr + P.damping_ring_wall).circle(dfr)
            .extrude(P.damping_ring_height + 0.5))
    cup = cup.union(ring)

    # 4. Baffle-mounting bosses — BUTTRESSED columns (the maker flagged the bare
    #    columns as fragile / snap-off-able). Each is a column at the bolt circle
    #    (r=baffle_screw_radius), from the joint-lap top (baffle_boss_floor_z,
    #    frame-only) up to the baffle underside, PLUS a wider base FLARE that merges
    #    the boss into the cup wall over a much wider arc than the bare column's thin
    #    lens. Built solid (column + flare) THEN bored from the front-facing top —
    #    round-before-cut, so the flare adds real support material and the heat-set
    #    bore stays clear (a base fillet here yields an invalid solid — the boss
    #    floors in open cavity with no host floor to round into).
    boss_points = [
        (
            P.baffle_screw_radius * math.cos(math.radians(45 + i * 360 / P.baffle_screw_count)),
            P.baffle_screw_radius * math.sin(math.radians(45 + i * 360 / P.baffle_screw_count)),
        )
        for i in range(P.baffle_screw_count)
    ]
    #
    #    REBUILT AT 54: the bolt circle now derives (baffle_screw_radius = body_r − boss_r), which
    #    puts the boss's outer edge flush with the body OD — the furthest out it can sit without
    #    standing proud of the shell, and the deepest bite it can take into the 3 mm wall. At the
    #    inherited bcd of 70.0 the circle sat at r35 on a body of radius 24: four columns in open
    #    air. The consequence of moving it inboard is that there is no room left to flare OUTWARD,
    #    so boss and flare are CLIPPED to the body cylinder and the buttress material goes inboard
    #    into the void, where there is room for it.
    fz, bh = P.baffle_boss_floor_z, P.baffle_boss_height
    for bx, by in boss_points:
        col = (cq.Workplane("XY").workplane(offset=fz).center(bx, by)
               .circle(P.baffle_boss_diameter / 2).extrude(bh))
        flare = (cq.Workplane("XY").workplane(offset=fz).center(bx, by)
                 .circle(P.baffle_boss_flare_diameter / 2).extrude(P.baffle_boss_flare_height))
        if P.baffle_boss_clip_to_body:
            col, flare = col.intersect(body_cyl), flare.intersect(body_cyl)
        cup = cup.union(col).union(flare)
    for bx, by in boss_points:  # bores last (round-before-cut)
        bore = (cq.Workplane("XY").workplane(offset=fz + bh).center(bx, by)
                .circle(P.m3_insert_hole_diameter / 2).extrude(-P.insert_boss_depth))
        cup = cup.cut(bore)

    # 5. Yoke pivot bosses — two external bosses at 0/180 on the cup side walls,
    #    at mid-height, each a radial cylinder spanning the wall to an outer seat so
    #    it fully houses an M3 heat-set insert bored from the outside. The fork's
    #    shoulder screw threads into it.
    #
    #    THIS IS THE PAIR THAT FAILED THE MANIFOLD GATE. yoke_pivot_centres was still Daily
    #    Driver's 98.0, so these two were built spanning r40→49 on a cup of body radius 24 —
    #    two cylinders floating 16 mm clear of the shell, which gate.py reported as
    #    "cup: 3 solid(s)". Both the centres and the span now derive from the body, so the
    #    boss reaches from the void wall (r21) out to pivot_boss_proud clear of the OD, with
    #    its inner end stopping flush IN the 3.0 wall — no lug into the cavity.
    r_out_boss = P.pivot_boss_outer_radius              # body_r + proud
    r_in_boss = r_out_boss - P.pivot_boss_through_span  # = void radius — flush in the wall
    span = P.pivot_boss_through_span
    zc = P.pivot_boss_z
    for sign in (+1, -1):
        # boss body: cylinder axis ±X, dia pivot_boss_diameter
        body = (
            cq.Workplane("YZ")
            .workplane(offset=sign * r_in_boss)
            .center(0, zc)
            .circle(P.pivot_boss_diameter / 2)
            .extrude(sign * span)
        )
        cup = cup.union(body)
        # heat-set bore from the outer face inward (insert installed from outside)
        bore = (
            cq.Workplane("YZ")
            .workplane(offset=sign * r_out_boss)
            .center(0, zc)
            .circle(P.m3_insert_hole_diameter / 2)
            .extrude(-sign * P.insert_boss_depth)
        )
        cup = cup.cut(bore)

    # 6. Edge treatment: the back-outer comfort/print break is now the chamfer in
    #    step 2b (the form pass "set the outer profile"), so the old no-op outer-
    #    wall fillet — which only ever warned on the bare cylinder — is retired.

    # 7. Front LIP — the Ø54 rim that overhangs the Ø48 body, and the reason the pad stays on.
    #    Retention is AXIAL: the foam stretches over this rim and cannot climb back over it, then
    #    grips the body behind it by friction alone (it still rotates freely — that is locating,
    #    not clamping). So the STEP is the retention feature and lip DEPTH matters more than rim
    #    diameter precision.
    #
    #    OPEN QUESTION, FLAGGED NOT DECIDED — whether this rim is printed on the CUP (here) or on
    #    the BAFFLE. The brief reads it as the baffle plate overhanging the body, and params says
    #    as much at pad_lip_extension ("there is no separate retaining brim"). It is kept on the
    #    cup for now because the functional result is identical (a Ø54 rim, 3.0 deep, over a Ø48
    #    body), because gate.py's pad-flange checks are written against the cup, and because the
    #    baffle is explicitly the part the builder iterates on — you do not want pad retention to
    #    change every time someone reprints a baffle. Maker's call; it is a one-block move.
    #
    #    Built as a full disc and rounded BEFORE the bore is cut — OCC on this build will fillet a
    #    clean cylinder's two circular edges and refuse the same edges on the finished annulus.
    lip_or = P.cup_outer_diameter / 2                 # = body_r + pad_lip_extension, LOCKED 27.0
    lip = (
        cq.Workplane("XY")
        .workplane(offset=total_h - P.cup_lip_depth)
        .circle(lip_or).extrude(P.cup_lip_depth)
    )
    try:
        lip = lip.edges("%CIRCLE").fillet(P.pad_lip_round)   # soften the rim the pad rolls over
    except Exception as e:  # noqa: BLE001 — report, don't mask; the lip still stands
        print(f"  [warn] cup: pad-lip roundover skipped ({e}).")
    lip = lip.cut(cq.Workplane("XY").circle(void_r).extrude(total_h))   # bore stays Ø42 through the lip
    cup = cup.union(lip)

    # 8. Cable exit — a hole through the −Y wall (the cup's BOTTOM when worn: T_cup
    #    maps cup −Y → global −Z) so the driver cable leaves the cup. At the pivot
    #    mid-height (depth), clear of the ±X pivot bosses. A clean through-cut, last.
    reach = lip_or + 2.0
    cable = cq.Solid.makeCylinder(
        P.cable_exit_diameter / 2, reach,
        cq.Vector(0, -reach, P.pivot_boss_z), cq.Vector(0, 1, 0))
    cup = cup.cut(cq.Workplane(obj=cable))

    return cup


if __name__ == "__main__":
    cq.exporters.export(make_cup(), "output/cup.stl")
    print("wrote output/cup.stl")
