# SPDX-FileCopyrightText: 2026 Jamey Warren
# SPDX-License-Identifier: MIT

"""
First Chair — parametric values.

This is the single source of truth for every dimension in the model. Change a
value here and the affected parts follow. All values are in millimetres.

Reconciled to design-spec.md v0.3 (DT880-family: bow → slider → fork-yoke → cup
→ baffle → driver → pad).

>>> ESTIMATE POLICY <<<
We are NOT waiting on measured parts. Every value tagged `ESTIMATE` is a working
guess chosen so the geometry builds and the interfaces line up — it is here to be
OVERWRITTEN by a measured value later, cleanly, because nothing downstream hard-
codes it. `REF` marks a reference dimension of a bought part (driver, bow) used
only for fit/clearance. `TODO` flags a real uncertainty that needs a decision or
a measurement before it's trustworthy. `MEASURED` is a confirmed caliper reading.
`SET` marks a dimension the maker has fixed by DESIGN DECISION — a target to build
to (e.g. the overall cup size), distinct from a guess (ESTIMATE) or a measured part
(MEASURED). Do not treat any ESTIMATE as confirmed.
"""

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Params:
    # ---- Cup shell -----------------------------------------------------------
    #
    # FIRST CHAIR IS A SUPRA-AURAL. The cup sits ON the ear, not around it, so the
    # governing dimension is not an ear cavity — it is the diameter the commodity
    # Grado-pattern pad stretches over. See BRIEF.md §4d #3: we do not design or ship
    # a pad, and that makes this an INTEROPERABILITY dimension rather than a free one.
    #
    #   front face / baffle plate   Ø 54.0   <- LOCKED (maker, 2026-08-06)
    #   step in 3.0 per side
    #   cup body                    Ø 48.0
    #
    # The "lip" is not a feature ON the cup: it is the BAFFLE PLATE OVERHANGING the
    # BODY. That single reading explains the whole profile and gives pad retention for
    # free — the foam stretches over the Ø54 rim and grips the Ø48 body behind it.
    # Retention is AXIAL (the lip stops it climbing forward) and only lightly radial
    # (it rotates freely on the cup), which is why lip DEPTH matters more here than
    # rim-diameter precision. The interface is forgiving: the same pads fit cups across
    # a Ø54–56.7 family.
    cup_outer_diameter: float = 54.0      # LOCKED  baffle-plate OD = the pad-mount rim
    cup_body_diameter: float = 48.0       # LOCKED  behind the lip; what the pad grips
    cup_lip_depth: float = 3.0            # LOCKED  axial depth of the overhanging plate
    cup_depth: float = 27.6               # SET  overall front→back; matches the reference family
    cup_interior_diameter: float = 42.0   # ESTIMATE  derives from body OD − 2× wall; see derive()
    wall_thickness: float = 3.0           # ESTIMATE  min shell wall (floor)
    wall_thickness_structural: float = 4.0  # ESTIMATE  at bosses / structural pts
    # ---- Form pass: chamfered back (direction "A", 2026-06-24) ----------------
    # The closed (grille) back is thickened past the side wall so a 45° outer
    # bevel reads without thinning the 3 mm side wall (the bevel lives entirely in
    # this back band). The acoustic air space behind the baffle is unchanged — only
    # the grille substrate gets deeper and the cup ~3 mm taller. See DESIGN-LOG.
    cup_back_thickness: float = 6.0       # ESTIMATE  solid rear band depth (the grille substrate)
    cup_back_round: float = 1.0           # soft-form round on the back-FACE edge where the dome meets the
                                          #   flat grille face (the dome below does most of the rounding now).
                                          #   SCALED DOWN from Daily Driver's 2.5: this cup is 54 mm across
                                          #   a 3.0 mm wall, not 91 mm across 6.7, and OCC simply refuses a
                                          #   2.5 mm fillet at that size ("BRep_API: command not done").
                                          #   FIRST LESSON OF THE FORK: absolute radii do not survive a
                                          #   change of scale. Any other hardcoded radius inherited from
                                          #   Daily Driver is suspect until it has been rebuilt at 54 mm.
    # ---- Cup back FORM: CONVEX DOME (maker form pass, 2026-06-28) -------------------------------------
    # The outer wall flows into a CONVEX DOMED back (DT880/Denon family) instead of a cylinder + plain
    # roundover. The dome lives in the rear `cup_dome_height` mm — the front stays cylindrical for the pad
    # seat + the void + the pivot bosses — and bulges from the OD at the dome top inward to a FLAT grille
    # face of radius `cup_back_face_radius` at the very back (the open grille sits on
    # that flat). Dome height is CAPPED by the void wall (~13 mm here: above that the wall over the ⌀78
    # void thins below ~3 mm). For a FULLER dome (the closed Studio clone) thicken the back band or reduce
    # the cup ID. Built as a LOFT (this OCC build's fillets fail once the grille/bosses complicate it).
    # REBUILT AT 54 (2026-08-06). Both of these were Daily Driver absolutes on a Ø91.44 cup and
    # neither survived the fork: cup_back_face_radius 35.0 is LARGER than this cup's outer radius
    # (24.0 at the body), so the "dome" lofted OUTWARD into a Ø70 mushroom, and dome_height 12.0
    # ran the taper up past the void floor and thinned the wall below the 3.0 mm floor.
    #
    # Both now DERIVE, so they cannot drift out of scale again:
    #   dome height  = cup_back_thickness — the dome lives ENTIRELY inside the solid back band, so
    #                  the wall above the void floor is a clean full-thickness cylinder. This is the
    #                  cap the old comment described in prose but never enforced.
    #   back-face r  = body radius − cup_dome_bulge, floored at the grille zone so the grille always
    #                  lands on flat material.
    cup_dome_bulge: float = 4.5           # SET  how far the dome pulls IN from the body OD at the back face.
                                          #   Ø48 body − 2×4.5 → a Ø39 flat back face; the grille zone is r19.0,
                                          #   so the flat clears it by 0.5. Raising this past 5.0 undercuts the
                                          #   grille; lowering it flattens the dome toward a plain cylinder.

    # ---- Cable exit (bottom of each earcup) ----------------------------------
    # A hole through the cup's −Y wall — the BOTTOM when worn (T_cup maps cup −Y to
    # global −Z) — for the driver cable to exit. One per cup; sized for a cable +
    # optional grommet/strain relief (TBD). Placed at the pivot mid-height (depth).
    cable_exit_diameter: float = 5.0      # ESTIMATE  cable passthrough (cable + grommet TBD)

    # ---- Rear vent grille (DECOUPLED from the baffle bosses, v0.3) -----------
    # Remaining material = center hub + concentric rings + radial spokes; the
    # gaps open to the driver. The outer ring is now its OWN radius (no longer
    # pinned to the boss circle) — bosses moved out to the perimeter wall.
    # LOGO rings + dot echo the makerphones mark (src DriverMark.astro): a center DOT
    # + two concentric rings, the OUTER ring ~2× the inner's weight. Radii/widths from
    # the logo's 64-grid proportions (outer r24/stroke5, inner r13.5/stroke2.5, dot
    # r4.2) scaled into the grille zone. As of Stage 1b these ride FLUSH on top of a
    # structural triangular lattice (below) — they are decoration, not structure.
    # REBUILT AT 54 (2026-08-06) — the grille now DERIVES FROM cup_interior_diameter.
    #
    # Every radius in this block used to be an absolute inherited from the Ø91.44 cup, and the whole
    # mark had drifted off the part: the zone edge sat at r33.0 on a cup whose body radius is 24.0
    # and whose void radius is 21.0. The grille was being cut in air outside the shell.
    #
    # The grille's zone is now the VOID, less a landing ring of solid floor at the wall — because
    # the grille's only structural job is to span the void and tie into the wall, so the void is the
    # dimension it is actually a function of. The logo rings + hub scale off that zone by the mark's
    # own 64-grid proportions (outer r24/stroke5, inner r13.5/stroke2.5, dot r4.2, so the mark's
    # outer edge is 26.5 on that grid), which is what "scaled into the grille zone" always meant —
    # it just was not written as arithmetic before. See the derived helpers.
    grille_rim_land: float = 2.0          # SET  solid floor annulus left between the grille zone and the void
                                          #   wall — what carries the whole grille into the shell. At the member
                                          #   floor (2.0): a landing ring no thinner than any grille bar.
    grille_logo_zone_fraction: float = 0.60  # TASTE — how much of the zone the logo mark spans, and the knob the
                                          #   old "thin the logo rings to free up open area (maker's call)" note
                                          #   predicted would be needed. MAKER'S EYE WANTED.
                                          #
                                          #   At 1.0 (Daily Driver's implicit value) the mark fills the zone and
                                          #   closes ~47 % of it unaided. The lattice pitch then has to open past
                                          #   the zone radius to stay inside the open-area band, which leaves 3
                                          #   bars per angle — i.e. only the through-centre bars survive and the
                                          #   "triangular lattice" degenerates into a 6-spoke wheel. That puts the
                                          #   logo back to being the structure, which is exactly the arrangement
                                          #   the Stage 1b rework inverted.
                                          #   At 0.60 the mesh gets a real pitch (5 bars per angle) and open area
                                          #   lands on the 0.40 target. Cost: the mark is Ø22.8 on a Ø38 grille
                                          #   rather than filling it. 0.75 / pitch 0.66 also passes the gate at
                                          #   open 0.436 if the bolder mark is worth the spoke-wheel — that is a
                                          #   look-at-it decision, not a numbers one.
    grille_ring_count: int = 2            # ESTIMATE  two concentric LOGO rings (the mark)
    grille_member_min_width: float = 2.0  # HARD FLOOR — FDM printability minimum
    grille_target_open_fraction: float = 0.40  # ESTIMATE  target_open (~40%)
    # Structural LATTICE (Stage 1b) — the grille is now a rigid TRIANGULAR ×3 mesh:
    # three opposing bar layers at 0/60/120° that carry the protection + stiffness,
    # with the logo rings + dot (above) riding FLUSH on top (single colour, co-planar,
    # same material). This INVERTS the old logo-as-structure grille (which read as
    # fragile yet bulky at once): the mesh is the structure; the logo is decoration,
    # so it can be bold without being load-bearing and prints self-supporting (built
    # face-down). Member 2.2 / pitch 11.5 are the settings the maker dialed in on the
    # interactive pattern explorer ("landed behind the logo nicely").
    grille_lattice_member_width: float = 2.2  # SET  triangular lattice bar width (explorer). Deliberately NOT
                                          #   scaled with the cup: this one IS a legitimate absolute — it is a
                                          #   nozzle multiple (0.4 × 5.5), so it is set by the printer, not by
                                          #   the part. Contrast every radius above, which is not.
    # REBUILT AT 54: pitch was 16.0, tuned against the Ø91.44 cup's r33 zone. On this cup's r19.0
    # zone that is nearly the zone diameter — bars at 0 and ±16 only, i.e. three usable bars per
    # angle and no mesh worth the name. It now derives as the same FRACTION of the zone radius that
    # 16.0 was of Daily Driver's, then is trimmed to land the open area near target.
    grille_lattice_pitch_fraction: float = 0.50  # SET  bar pitch as a fraction of the grille zone radius.
                                          #   0.50 → pitch 9.5, which is the LARGEST pitch that still puts 5 bars
                                          #   per angle inside an r19 zone (bars at 0, ±p, ±2p need 2p < 19).
                                          #   Anything looser and only the through-centre bars survive. Close to
                                          #   Daily Driver's 0.485 (16/33) — the FRACTION was always about right;
                                          #   it was the absolute that did not survive the change of scale.
    grille_lattice_angles: tuple = (0.0, 60.0, 120.0)  # 3 opposing layers (triangular)
    grille_open_min: float = 0.30         # gate band lower bound (see gate.py OPEN_MIN)
    # Orange ACCENT dot — a press-in cap at the grille center (the mark's only
    # accent, printed in the warm orange). Seats on the grille hub, stands proud
    # on the outboard face.
    grille_dot_diameter: float = 9.0      # ESTIMATE  accent dot (<= hub dia, seats on it)
    grille_dot_proud: float = 1.5         # ESTIMATE  stands proud of the grille face

    # ---- Baffle-mounting bosses in the cup (wall-blended) --------------------
    # Four heat-set bosses on the diagonals (45/135/225/315), blended into the
    # perimeter inner wall near the front — NOT free-standing posts. Bore faces
    # front; the baffle screws into them from the front.
    baffle_screw_count: int = 4           # SET  4 (maker's choice). The baffle's 6
                                          #   OTHER small holes are VENTS, not screws.
    # REBUILT AT 54 (2026-08-06). bcd 70.0 (r35) was a Ø91.44-cup number: on this cup it put the
    # boss circle 11 mm OUTSIDE the body radius, so the four bosses were columns standing in open
    # air, grazing the flared dome. The bcd now DERIVES from the wall it has to be embedded in —
    # the boss's outer edge is flush with the body OD, which is the furthest out it can sit without
    # standing proud of the shell, and the deepest it can bite into the 3 mm wall.
    baffle_boss_diameter: float = 7.0     # REBUILT  was 12.0 (Ø91 cup). 7.0 = insert_boss_diameter: the
                                          #   M3 insert's installed 4.70 OD plus 1.15 of wall per side. On a
                                          #   Ø48 body a Ø12 boss is a quarter of the cup's diameter and cannot
                                          #   sit inside the wall at all.
    baffle_boss_clip_to_body: bool = True  # SET  clip boss + flare to the body cylinder so neither stands proud
                                          #   of the shell. With the bcd hard against the wall there is no room
                                          #   to flare OUTWARD; the buttress goes inboard, into the void.
    # Boss BUTTRESS — a base flare merging the boss into the cup wall so it can't snap
    # off at the thin wall lens (maker flagged the bare columns as fragile). Built as a
    # wider base step then bored, so it adds real support material at the junction.
    baffle_boss_flare_diameter: float = 11.0  # REBUILT  was 15.0 (Ø91 cup). Boss 7.0 + 2.0 of buttress per
                                          #   side; clipped to the body OD (above) so the extra material lands
                                          #   inboard where there is room for it.
    baffle_boss_flare_height: float = 3.0     # SET  flare height at the base

    # ---- Yoke pivot bosses in the cup (external, side walls) -----------------
    # Two bosses at 0/180 on the cup's OUTER side wall, at mid-height, each with
    # an M3 heat-set bore (radial, outward-facing) for the fork shoulder-screw.
    pivot_boss_count: int = 2             # ESTIMATE  count (0/180)
    pivot_boss_diameter: float = 8.0      # REBUILT  was 12.0 (Ø91 cup). 8.0 leaves 1.65 of wall around the
                                          #   installed 4.70 insert; Ø12 on a Ø48 body is a sixth of the cup.
    # ================= THIS PAIR WAS THE 3-SOLID MANIFOLD FAILURE =================
    # yoke_pivot_centres was 98.0 — Daily Driver's Ø91.44 cup plus ~4 mm proud per side. It survived
    # the fork untouched, so pivot_boss_outer_radius came out at 49.0 and the two pivot bosses were
    # built spanning r40→49 on a cup whose body radius is 24.0. They touched nothing. gate.py read
    # that as "cup: 3 solid(s)" — the shell plus two cylinders floating 16 mm off its side.
    #
    # Note how quietly it passed everything else: `pivot-clearance: boss proud 22.0 mm >= 2.0` was
    # GREEN, because a boss floating in space is extremely proud of the wall. A check written
    # against one scale can read as confirmation at another.
    #
    # Both now derive from the body they are mounted on (see the derived helpers):
    #   centres = cup_body_diameter + 2 × pivot_boss_proud
    #   span    = outer radius − void radius  (inner end stops flush IN the wall, no lug into the cavity)
    pivot_boss_proud: float = 4.0         # SET  how far the boss face stands off the body OD — room for the
                                          #   insert head + the fork-arm seat. Carried over from Daily Driver
                                          #   as a HARDWARE dimension (M3 insert + arm), not a cup dimension,
                                          #   so unlike the radii above it is scale-independent and stands.
    pivot_boss_forward: float = 4.0       # SET  shift the pivot this far toward the FRONT (pad/head side)
                                          #   off the cup mid-depth. Pulls the yoke→band junction INBOARD
                                          #   (tighter clamp, more compact, less junction tilt) — maker's fit
                                          #   call. Capped so the boss (Ø12) clears the baffle seat (z=30).

    # ---- Heat-set inserts / screws ------------------------------------------
    #
    # FASTENER TARGET (2026-08-07): ONE THREAD, ONE INSERT SIZE, ALL METRIC.
    #
    #     M3 heat-set inserts · M3 cap screws · M3 washers. Nothing else.
    #
    # Heat-set inserts are KEPT, deliberately, against the alternative of captured hex
    # nuts. An insert is a small cylindrical bore; a captured nut needs a hex pocket,
    # capture geometry, an access slot, and clear space BEHIND the joint — and our baffle
    # bosses are columns standing in the void with the bore facing forward, so there is no
    # "behind". Inserts also give a reusable metal thread, which the build's tie-breaker
    # (serviceability — the user is a tweaker) wants over a nut that can drop out on the
    # fourth teardown.
    #
    # What the target removes is VARIETY, not inserts. The fork inherited FIVE thread
    # standards mixing metric and imperial — M3, M5, 8-32, plus Ø4 and Ø6 shoulder screws —
    # and THREE insert sizes, meaning three install bores (4.0 / 5.6 / 6.4) and three tips.
    #
    # Almost all of that sprawl is ONE UN-PROPAGATED DECISION. The 8-32 insert, the 8-32
    # thumbscrew, the pressure shoe, the M5 insert and the Ø6×M5 adjustment post are all
    # parts of the thumbscrew height-lock — the Daily Driver mechanism that this build's
    # locked slider already deletes ("deletes the thumbscrew, the insert and the pressure
    # shoe in one move", §4b). Propagate that and the BOM collapses to M3 on its own.
    #
    # ONE OUTLIER LEFT, and the brief already convicted it: the Ø4×M3 pivot shoulder screw
    # sits below the official ISO 7379 size sheet, so every supplier brands it "similar to"
    # — which was one of the original complaints against Daily Driver's BOM. If a plain M3
    # cap screw plus a printed bushing can carry the tilt pivot, the whole build becomes
    # M3 cap screws, M3 inserts, M3 washers, and nothing else.
    #
    # Not executed yet: the deletion is tangled with the slider, and whether the slider
    # survives at all is an open question for the form pass. The TARGET is recorded so
    # whatever comes back gets judged against it.
    m3_insert_hole_diameter: float = 4.0  # ESTIMATE  M3 brass insert bore
    m5_insert_hole_diameter: float = 6.4  # ESTIMATE  M5 brass heat-set install bore (fork→shoulder-screw; verify vs insert)
    m3_clearance_hole: float = 3.4        # M3 free-fit through-hole (standard)
    insert_boss_diameter: float = 7.0     # ESTIMATE  generic insert-boss OD
    insert_boss_depth: float = 6.0        # ESTIMATE  insert/bore depth

    # ---- Pivot hardware: M3 shoulder screw + heat-set insert ----------------
    # Real fastener geometry for the yoke↔cup pivot, so the gate validates fit
    # against actual parts (see parts/hardware.py + the pivot gate checks).
    # Insert dims are REF, VERIFIED against cq_warehouse 0.8.0 HeatSetNut
    # "M3-0.5-Standard" / "McMaster-Carr" (measured OD 4.70, length 5.70).
    # NOTE: m3_insert_hole_diameter (4.0) is the UNDERSIZED thermal-install bore for
    # this 4.70 OD insert — correct by design (the brass melts/knurls into it), not
    # a mismatch. Boss-wall checks use the 4.70 INSTALLED OD (conservative).
    heatset_insert_diameter: float = 4.70   # REF  M3 insert installed OD. McMaster M3 = 4.70; the BOM's
                                            #   recommended Ruthex RX-M3x5.7 measures 4.6 — we keep the larger
                                            #   4.70 as the CONSERVATIVE wall-check value (stricter gate).
    heatset_insert_length: float = 5.70     # REF  M3 insert length (verified)
    # cq_warehouse has NO ShoulderScrew class, so the screw is composed from
    # primitives; these are ESTIMATE / caliper-pending (measure the part you buy).
    shoulder_screw_thread_diameter: float = 3.0    # M3 thread major dia
    shoulder_screw_shoulder_diameter: float = 4.0  # ESTIMATE  smooth shoulder OD (≈4 on M3)
    shoulder_screw_shoulder_length: float = 8.0    # ESTIMATE  bearing length the eye rides
    shoulder_screw_thread_length: float = 5.0      # ESTIMATE  thread into insert (<= insert len)
    shoulder_screw_head_diameter: float = 7.0      # REF  ISO 7379-4-M3 head OD (was 6.5 est; caliper-confirm)
    shoulder_screw_head_height: float = 3.0        # ESTIMATE  head height (tall cap — washer stack hides it)
    # Pivot tilt-friction WASHER STACK (bought): [head | M3 wave/Belleville | nylon flat | eye |
    # nylon flat | boss]. Nylon protects the PETG from the steel head + adds drag; the wave washer
    # preloads the stack so the cup HOLDS its tilt angle (a friction hinge). NO bushing/spacer — the
    # shoulder LENGTH is the spacer and the eye rides the smooth Ø4 shoulder directly.
    pivot_nylon_washer_thickness: float = 0.5  # SET  thin nylon flat washer (×2 per side: head + boss face)
    pivot_wave_washer_height: float = 0.6      # SET  M3 wave washer compressed/working height (the preload)

    # ---- Pivot over-rotation hard stop — REMOVED 2026-06-26 ------------------
    # The cup now rotates FREELY in the yoke (Grado-style — free pivot, no detent or
    # hard stop). The old pin-on-cup + arc-slot-in-yoke-eye stop was dropped: the pin
    # was a snap-off risk and the slot notch weakened the eye, and free rotation is a
    # non-issue in practice (cf. Grado). The shoulder screw is the only tilt joint.

    # ---- Baffle plate (front-mount) -----------------------------------------
    baffle_outer_diameter: float = 77.0   # ESTIMATE  baffle_od (drops into id 78)
    baffle_thickness: float = 5.5         # SET  HUB thickness (driver/guard zone only — the outer ring is
                                          #   baffle_ring_thickness). DOME-GATED: recess 1 + dome_proud 1.5 +
                                          #   excursion 0.5 + guard_clr 0.5 + guard 1.5 + setback 0.5 = 5.5 on the
                                          #   common-40 mm driver assumption. Re-measure the real dome/excursion to
                                          #   reclaim more. (Was 6.0 at the conservative excursion 1.0.)
    # driver_aperture and driver_recess_diameter now DERIVE from driver_od (see the
    # derived helpers), so the baffle aperture/guard/vents stay coherent when the
    # driver size changes — "different baffle plates" is a regenerate, not a redesign.
    driver_recess_depth: float = 1.0      # SET  shallow seat the driver rim registers into (on BACK).
                                          #   Was 3 — a deep recess that pushed the dome up into the thin
                                          #   front lamina (cone poked the guard). Now a 1 mm seat + a
                                          #   locating COLLAR (below) hold the driver, dropping the dome
                                          #   ~2 mm clear of the guard with NO extra baffle thickness, and
                                          #   leaving a lip for a foam seal the clamp compresses.
    # Driver locating COLLAR — a short wall around the driver on the baffle BACK,
    # continuing the seat wall proud of the back face. Secures/locates the driver
    # laterally; kept SHORTER than the driver's behind-baffle protrusion so the clamp
    # ring still presses the rear rim (good seal + room for foam), per the maker.
    driver_collar_height: float = 2.5     # SET  collar height proud of the baffle back (< driver protrusion)
    driver_collar_wall: float = 2.0       # SET  collar radial wall thickness
    # Earpad retaining FLANGE — a thin brim at the CUP's front OUTER edge that
    # extends the perimeter OUTWARD (DT770-style "extension of the circumference"),
    # so the earpad's skirt wraps over it and hooks behind. It sticks OUT radially,
    # NOT up toward the head, so the baffle stays flush (not recessed). Exact size is
    # TBD — measure the Dekoni pad's mounting skirt/groove.
    # FIRST CHAIR: there is no separate retaining brim. The lip IS the baffle plate
    # overhanging the body (see the Cup shell block), so these derive rather than being set.
    pad_lip_extension: float = 3.0        # LOCKED  = (cup_outer_diameter − cup_body_diameter)/2
    pad_lip_thickness: float = 3.0        # LOCKED  = cup_lip_depth
    pad_lip_round: float = 0.8            # soft-form roundover on the brim edges (eases the pad + feel)
    baffle_counterbore_diameter: float = 6.0  # ESTIMATE  M3 socket head clearance
    baffle_counterbore_depth: float = 2.5     # ESTIMATE  head sinks below front
    # ---- Baffle: STEPPED thickness + OPEN front venting + acoustic-paper recess ----
    # The plate is full thickness only in the central driver/guard HUB (that depth is dome-gated —
    # see baffle_thickness). The outer RING is thinner (front recessed) to shed bulk while staying
    # stiff (bolted rim + ribs + hub). Front venting opens to big ARC-SLOTS between the 3 clamp-
    # standoff SECTORS (the "solid support"), backed by a glued acoustic paper/mesh in a shallow
    # FRONT depression — the paper sets the back→front resistance. All recesses open UPWARD for the
    # back-face-down print. The paper GRADE / exact open area is MEASUREMENT-GATED (tune to the driver).
    baffle_ring_thickness: float = 4.0    # SET  thinned outer-ring thickness (hub → 4 mm ring; front recessed)
    baffle_hub_margin: float = 2.0        # SET  radial margin past the driver collar to where the full-thick hub ends
    baffle_vent_zone_gap: float = 1.5     # SET  vent radial clearance from the hub edge / outer rim
    # Front venting = a SERIES OF HOLES in N "hot-dog" zones, each covered by a glued ARC STRIP of
    # acoustic paper (strips cut from a sheet — far less waste than one annulus, and a flat hole-field
    # is easier to glue over than open slots). The strips sit BETWEEN the 4 mounting screws so the
    # screw bosses keep their strength; the holes auto-skip the 3 clamp standoffs (0/120/240). Total
    # open area is parametric; the paper GRADE (resistance) is measurement-gated to the driver.
    baffle_vent_strip_count: int = 4      # SET  hot-dog strips / hole zones (4 → centred at 0/90/180/270, between screws)
    baffle_vent_strip_half: float = 30.0  # SET  arc half-angle of each strip zone (clears the 45/135/… screws — see gate)
    baffle_vent_hole_diameter: float = 3.5  # SET  round vent-hole dia (a series under each strip)
    baffle_vent_hole_pitch: float = 6.0   # SET  hole centre-to-centre along the strip arc
    baffle_paper_recess_depth: float = 0.8  # SET  front depression each paper STRIP glues into (cut to match, flush)
    baffle_paper_thickness: float = 0.3   # ESTIMATE  acoustic paper / mesh thickness (bought soft-good; GRADE TBD-measured)
    # baffle bolt circle reuses baffle_bolt_circle_diameter (aligned to the cup).
    # NOTE: cable entry is cup-side per v0.3 (dual entry) — NOT on the baffle.

    # ---- Driver clamp ring (3-bolt, holds the driver to the baffle) ----------
    # The maker's prototype: a 3-ear ring that slips over the BACK of the driver and
    # retains it by the PERIMETER. The driver nests SLIGHTLY into a RECESS in the ring
    # (not pressed by a proud lip) — the recess wall captures the driver's outer edge
    # and the recess floor (an inner shoulder) bears on the back of the frame rim,
    # pressing the driver forward into the baffle's recess. The magnet/back clears
    # through the open centre. Bolts to 3 inserts on the baffle BACK at bcd 60 (between
    # the vents ~r26 and the frame holes r35; the 3 ears interleave with the 6 vents).
    # Standoff bosses on the baffle reach back to the ring at the driver's back depth.
    # (Driver-fit dims are REF / driver-measured-pending.)
    driver_clamp_count: int = 3              # SET  3-ear clamp (matches the prototype)
    # driver_clamp_bolt_circle is now DERIVED — see the helpers. It was 60.0 (r30), and its own
    # comment stated the rule it was standing in for: "between vents (r26) + frame holes (r35)".
    # Those two radii are Ø91.44-cup numbers; rebuilt at 54 the band is (r18.9, r20.5) and a
    # clamp bcd of r30 sits clean off the baffle. The rule is now the arithmetic.
    driver_clamp_inner_diameter: float = 34.0  # SET  open centre — clears the magnet; shoulder catches the rim
    driver_clamp_recess_clearance: float = 0.4  # SET  driver OD ↔ ring recess (the driver nests in)
    driver_clamp_recess_depth: float = 2.0   # SET  how far the driver nests into the ring
                                             #   (≈ the basket that protrudes behind the baffle)
    driver_clamp_floor_thickness: float = 2.5  # SET  shoulder floor behind the recess
    driver_clamp_wall: float = 2.5           # SET  wall around the recess
    driver_clamp_ear_diameter: float = 9.0   # SET  ear pad dia around each M3 hole
    driver_clamp_post_width: float = 6.0     # SET  post width (< ear pad 9 → post↔pad shoulders fillet cleanly)
    # driver_clamp_standoff is DERIVED below (= body_depth − seat depth) so it tracks the seat.
    driver_clamp_fillet: float = 0.8         # SET  blend at the post↔ring / post↔pad junctions. 0.8 is this OCC
                                             #   build's CEILING here — 0.9–1.1 silently invalidate, ≥1.2 hard-fail
                                             #   (clamp fillet probe). Bigger radii want the build123d port.
    driver_clamp_edge_round: float = 0.6     # SET  roundover on the ear-plate perimeter (softens the 90° rim corners)

    # ---- Integral driver guard (concentric RINGS + radial SPOKES, on the baffle) -
    # A classic driver grille: concentric rings tie the radial spokes, far stronger
    # than bare spokes while staying airy. It sits in the front lamina just ABOVE the
    # driver dome (the diaphragm must never touch it). The lamina is thin, so the rib
    # is auto-thinned to fit and the build WARNS the true clearances (see baffle.py).
    guard_spoke_count: int = 6            # ESTIMATE  radial spokes (hub → aperture wall)
    guard_ring_count: int = 2             # SET  concentric rings tying the spokes (the rings+spokes grille)
    guard_member_width: float = 2.0       # ESTIMATE  spoke / ring width
    guard_setback: float = 0.5            # ESTIMATE  DESIRED pad setback below the front face. The guard sits in
                                          #   the pad's OPEN centre, so a small setback is fine (warned if below)
    guard_dome_clearance: float = 0.5     # SET  safety gap from the guard floor to the dome's DYNAMIC (excursed)
                                          #   forward-most position — i.e. margin BEYOND driver_dome_excursion
    guard_thickness: float = 1.5          # ESTIMATE  guard rib thickness (Z); thinned to fit the lamina
    guard_hub_diameter: float = 6.0       # ESTIMATE  small center hub to tie the spokes

    # ---- Driver (MEASURED 2026-06-26 + COMMON-40 mm ASSUMPTIONS) -------------
    # driver_od/body_depth/magnet are measured off a real 40 mm driver; the dome/diaphragm figures
    # are set to the COMMON 40 mm dynamic-driver range (typical consumer: diaphragm ~34–38, dome
    # ~1–2 mm proud, ONE-WAY excursion ~0.3–0.6, ~32 Ω / ~100 dB·mW) as deliberate placeholders
    # until the real TEST DRIVERS are measured. They drive the baffle hub thickness + guard clearance.
    driver_od: float = 39.5               # MEASURED  outermost frame dia (the "40 mm" driver)
    driver_diaphragm_diameter: float = 34.0  # ASSUMPTION  diaphragm/dome (common 40 mm; < the 39.5 frame, guard clears it)
    driver_body_depth: float = 5.0        # MEASURED  driver height on the outside (the basket)
    driver_dome_proud: float = 1.5        # ASSUMPTION  dome proud of the frame at REST (common 40 mm ~1–2 mm)
    driver_dome_excursion: float = 0.5    # ASSUMPTION  forward DYNAMIC dome travel — common 40 mm headphone one-way
                                          #   Xmax ~0.3–0.6 mm (was a conservative 1.0 placeholder). The guard must
                                          #   clear the dome's forward-most position; MEASURE on the real test driver.
    # Driver MOCKUP dims (parts/driver.py) — a representative driver shown in the
    # assembly so the driver↔baffle↔clamp fit reads. The magnet sits behind the basket.
    driver_magnet_diameter: float = 27.0  # MEASURED  rear magnet OD
    driver_magnet_depth: float = 3.0      # MEASURED  rear magnet height
    driver_cutout_tolerance: float = 0.3  # ESTIMATE  fit allowance on the recess
    driver_seat_ledge: float = 2.5        # ESTIMATE  radial frame seat (per side); aperture =
                                          #   od − 2·this = 34.5, so the 34 diaphragm clears it
    # Aperture SHAPE hook: only "round" is authored today. "oval"/"planar" (e.g. a
    # planar-magnetic driver) is a FUTURE variant — baffle.py raises if not round.
    # See DESIGN-LOG. Kept here so the param surface is ready before the geometry is.
    driver_aperture_shape: str = "round"  # ESTIMATE  only "round" is built today

    # ---- Step-down adapter ring (accessory; "design big, adapt down") --------
    # A printed ring so a baffle built for a LARGER driver can host a smaller one
    # with NO reprint — a real driver-testing workflow. Worked example: a 50 mm-
    # class host hosting the 40 mm reference driver. INDEPENDENT of the reference
    # build (driver_od stays 42). All ESTIMATE. NOTE: a step-down ring changes the
    # front cavity / adds a step — NOT acoustically neutral; ring variants are
    # REW-loop items (see DESIGN-LOG), not a free swap.
    adapter_host_diameter: float = 50.0     # ESTIMATE  host baffle recess the ring drops into
    adapter_target_driver_od: float = 42.0  # ESTIMATE  smaller driver it adapts to (40 mm class)
    adapter_height: float = 6.0             # ESTIMATE  ring height (shims the driver-depth delta)
    adapter_seat_thickness: float = 2.0     # ESTIMATE  front seat floor the driver rests on

    # ---- Fork / yoke ---------------------------------------------------------
    # yoke_pivot_centres is now DERIVED (= cup_body_diameter + 2 × pivot_boss_proud) — see the
    # derived helpers, and the note at pivot_boss_proud for why the 98.0 absolute that lived here
    # was the cup's 3-solid manifold failure. The fork span follows the cup it straddles; it is not
    # a number anyone should be able to set independently of the cup again.
    yoke_arm_width: float = 9.0           # ESTIMATE  arm_w (at the eye / load end)
    yoke_arm_hub_width: float = 6.0       # ESTIMATE  arm_w at the hub end — gentle taper
                                          #   (slims toward the hub; >= structural floor)
    yoke_arm_thickness: float = 6.0       # ESTIMATE  arm_th (beefier for print strength)
    yoke_arm_corner_radius: float = 2.0   # SET  corner-round of the LOFTED arm section (the de-blocky form;
                                          #   2.0 adversarially verified, 2.5 also builds — taste knob). NOT a
                                          #   3D fillet: the rounding is in the swept 2D section.
    yoke_fork_height: float = 55.0        # ESTIMATE  fork_height (pivot → hub)
    yoke_pivot_hole_diameter: float = 4.2  # SET  eye bore = Ø4.0 shoulder + 0.2 running fit (was 3.4 = M3
                                           #   clearance — BUG: the Ø4 shoulder couldn't enter a Ø3.4 hole).
    yoke_pivot_eye_diameter: float = 12.5  # SET  eye pad OD — grown 12→12.5 so the web stays ≥4 with the Ø4.2 bore
    pivot_tilt_degrees: float = 20.0      # ESTIMATE  tilt_range (±)

    # ---- Yoke↔slider vertical adjustment (Grado HP1000-style: post + thumbscrew) -
    # The yoke carries a round vertical POST that slides up/down in the slider block
    # for HEIGHT (head-size) adjustment, locked by a side THUMBSCREW pressing the post
    # — no detent, like Joe Grado's HP1/HP1000. The round post in a round bore also
    # lets the cup SWIVEL (fore-aft seal conform) when the screw is loose; tightening
    # locks both height + swivel by friction. (Replaces the old fixed swivel hub/bore;
    # Beyer's friction-clip in the block is the alternative, noted in the LOG.)
    yoke_post_diameter: float = 6.0       # SET  Ø6 BOUGHT 304-SS ground shaft (slide + swivel bearing; was Ø8 — too chunky)
    yoke_post_length: float = 50.0        # SET  EXPOSED shoulder length above the boss (= stock 50 mm ISO 7379
                                          #   shoulder; gives ~32 mm slide travel over the 18 mm barrel — ample.
                                          #   Step the screw to 60 mm if more head-size headroom is wanted).
    # The post is a BOUGHT ISO 7379 SHOULDER SCREW — Ø6 ground shoulder (the bearing) × M5 thread,
    # 18-8 SS, 50 mm shoulder. NO rod machining: the M5 end threads into an M5 heat-set in the
    # printed fork, and the screw's HEAD is the built-in TOP STOP (wider than the bore). This
    # collapses the old tapped-rod + epoxy socket + separate stop-knob into one bought fastener,
    # and is serviceable (threaded, not epoxied). The ground f9 shoulder ≈ Ø5.96–5.99 in the Ø6.4
    # bore → ~0.4 mm clearance, matching slider_post_clearance.
    yoke_socket_boss_diameter: float = 13.0  # SET  boss OD (> barrel Ø12 → the shoulder's BOTTOM end-stop seat)
    yoke_rod_mount_depth: float = 12.0       # SET  boss depth hosting the M5 heat-set + thread engagement
    yoke_rod_head_diameter: float = 10.2   # REF  ISO 7379 Ø6-shoulder head dk (> bore Ø6.4 → top stop)
    yoke_rod_head_height: float = 4.5      # REF  ISO 7379 Ø6-shoulder head k
    yoke_rod_thread_length: float = 9.5    # REF  M5 thread length (engages the fork heat-set)
    slider_post_clearance: float = 0.4    # SET  slide fit, post↔slider bore (FDM)
    slider_adjust_travel: float = 18.0    # ESTIMATE  vertical size-adjust range (reference)
    # WORN-POSE slider position (assembly viz only — not a printed dim). Where the barrel rides on
    # the post: 0 = fully EXTENDED (barrel at the post top = biggest head, longest exposed rod);
    # 1 = fully RETRACTED (barrel at the hub stop = smallest head, rod pokes furthest above). 0.5 =
    # an average head — the realistic worn look (band pulled down toward the cups, rod up in the slider).
    assembly_worn_slider_frac: float = 0.9  # SET  near-RETRACTED = an average head. The 91 mm cup forces the
                                            #   band block high, so an average head sits near the bottom of the
                                            #   post travel (band as low as it goes), with EXTENSION for bigger
                                            #   heads. Was 0.5 (mid) — which floated the band ~16 mm too high.
    # Reference HEAD (assembly viz only — a translucent average-head ovoid for worn-fit context in
    # the 3D viewer: toggleable, OFF by default, excluded from the explode; NOT a printed part).
    # THREE sizes (S/M/L) so the maker can compare how the band lands + how the cups clamp
    # across head breadths. The MEDIUM ovoid is sized below; S/L are the same ovoid scaled
    # UNIFORMLY by their ear-to-ear breadth, so a bigger head is taller-crowned too (the
    # band-landing reads) and wider at the ears (the clamp-vs-cup-spacing reads). All centred
    # at x=0 with the ear at head_ref_z, so the ears stay aligned and only the size differs.
    head_ref_ear_half: float = 73.5     # SET  MEDIUM ear-to-ear half (~147 mm bitragion, 50th pct)
    head_s_ear_half: float = 70.0       # SET  SMALL  (~140 mm — ~5th pct adult)
    head_l_ear_half: float = 77.5       # SET  LARGE  (~155 mm — ~95th pct adult)
    head_ref_depth_half: float = 97.0   # SET  front-back half (~194 mm head length, at MEDIUM)
    head_ref_height_half: float = 121.0 # SET  half head-height. With head_ref_z below, the EAR sits
                                        #   ~8 mm BELOW the ovoid centre (real ears do) → ear→crown ≈ 129 mm
                                        #   (tragion→vertex, 50th pct), ear→chin ≈ 113 mm. Was 114 (ear at
                                        #   centre → ear→crown only 114, ~15 mm too short → faked the band-float).
    head_ref_z: float = 8.0             # SET  ovoid centre Z above the ear/pivot (cups touch ~8 mm below centre)
    # Lock = a CAPTIVE PRESSURE SHOE the thumbscrew presses against the post (NOT the screw tip
    # on the bare post — a metal point gouges the printed PETG bearing). The screw → conformal
    # shoe → post: keeps the HP1000 positive lock, distributes the load (no marring), and the
    # shoe takes up the gap so a SHORT screw works (less protrusion). Mirrors the aftermarket
    # Grado aluminium rod-block's silicone 'slider pill'. The lock screw is a stock 8-32 knurled
    # KNOB / large-head thumb screw (below) — it presses the shoe, not the post.
    # STANDARDIZED on a stock McMaster knurled KNOB / large-head thumb screw — 8-32 thread with a
    # big ⌀5/8" (≈15.9 mm) GRIPPABLE knurled head (maker's call: easy to twist). The lock is
    # low-load (presses the shoe), so the bigger thread is for the head + a sturdier stud, not
    # strength. 8-32 brass heat-set. Boss parametric so a near-equivalent line still fits.
    slider_thumbscrew_diameter: float = 4.17     # SET  8-32 UNC shaft major Ø (0.164")
    slider_thumbscrew_insert_hole: float = 5.6   # SET  8-32 brass heat-set install bore = Ruthex 8-32 spec
                                                 #   (was 5.0 est). Use the SHORT RX-8-32x4.7 insert (4.7 mm) to
                                                 #   fit the ~5 mm boss; standard 8.1 mm needs a deeper boss. See bom.py.
    slider_thumbscrew_boss: float = 9.0   # SET  boss OD: ~2 mm wall around the 8-32 heat-set bore
    slider_thumbscrew_boss_proud: float = 5.0  # SET  boss stand-off — short 1/4"–3/8" 8-32 screw keeps the big head close in
    slider_thumbscrew_boss_z: float = 0.0      # SET  boss CENTRED on the barrel mid (z=0), dead-centre on the +Y
                                          #   OUTBOARD face. In the worn pose local +Y → global +X (straight out the side
                                          #   of the head) = the natural two-finger reach with the phones ON. On the x=0
                                          #   centreline → the slider stays L/R symmetric (one print both ears).
    # CAPTIVE SHOE — a small conformal pad (printed PETG or a Delrin blank, ×2) that sits in a
    # pocket in the barrel wall, trapped between the post and the screw tip. Its concave face
    # cradles the Ø6 post over an AREA so the lock never marks it.
    slider_shoe_width: float = 6.0        # SET  shoe X (along the lozenge long axis)
    slider_shoe_height: float = 7.0       # SET  shoe Z (up the post — taller = more post contact line)
    slider_shoe_thickness: float = 2.2    # SET  shoe Y (radial, screw-face → saddle); fits the thin barrel wall + boss base
    slider_shoe_saddle_r: float = 3.4     # SET  concave saddle radius (Ø6 rod r 3 + clearance) → conformal area cradle
    slider_shoe_saddle_depth: float = 0.8 # SET  how deep the saddle dishes the shoe face
    slider_shoe_clearance: float = 0.3    # SET  shoe↔pocket sliding fit (drop-in via the bore, post traps it)
    # Thumbscrew MOCKUP (parts/hardware.py) — viz of the big ⌀5/8" knurled KNOB on the 8-32 stud.
    # Grip it by the knurled rim; the short shaft keeps it close to the barrel. Tip presses the shoe.
    thumbscrew_head_diameter: float = 15.9   # SET  ⌀5/8" knurled head (grippable; maker's pick)
    thumbscrew_head_height: float = 5.0      # SET  head height (grip by the rim)
    thumbscrew_shaft_length: float = 6.35    # SET  ~1/4" length under head (tip reaches the shoe)

    # ---- Slider = CLAMP COLLAR (replaced the box block) ----------------------
    # A slim rounded BARREL around the post + a slim 2-bolt mount tab for the bow's
    # end tab + the side thumbscrew. The round post sliding/turning in the barrel bore
    # is the SWIVEL + height bearing in ONE robust interface (no separate weak joint);
    # the thumbscrew clamps both. Far less bulk than the old 42×26×18 block. The bow
    # end tab (33 mm, 2 holes at bow_endtab_hole_spacing) bolts to the mount tab.
    slider_collar_diameter: float = 12.0      # SET  barrel OD around the post bore (Ø6.4 bore + 2.8 wall) — sleeker on Ø6 rod
    slider_collar_height: float = 18.0        # SET  barrel height (post grip + travel feel)
    slider_collar_rim_round: float = 2.0      # constructed 45° chamfer on the barrel end rims (fillet pass)
    slider_bore_chamfer: float = 1.0          # countersink lead-in at each post-bore mouth (post entry + clean print)
    slider_boss_chamfer: float = 0.8          # small countersink at the thumbscrew insert-bore mouth (1.5 mm boss wall)
    slider_tube_gusset: float = 5.0           # SET  gusset run that fairs the tube into the lozenge (grown-in)
    slider_tube_gusset_z: float = 14.0        # SET  gusset extent along the tube height (Z)
    # Headband CLAMP (Beyer-style two-piece, OFFSET-OUTER layout). The post-bore TUBE
    # (the barrel) is the OUTER body — the band attaches on the barrel's INNER (−Y,
    # head-side) face, so the rod + tube ride OUTSIDE the metal band (maker's call). The
    # band's two prongs drop into a RECESS in the clamp plate; a RIB enters the bow's open
    # CHANNEL (between the rails) for anti-rotation; a separate COVER plate
    # (parts/headband_clamp.py) sits on the band's inner face and sandwiches the metal with
    # two M3 screws through the prong-tip holes. The clamp is centred on the barrel mid
    # (z=0); the post slides the full barrel height and may poke past it (nothing stacks on
    # the post). slider_clamp_hole_z / rib_z are now relative to the barrel mid.
    # The clamp body is a flat rounded LOZENGE (Beyerdynamic end-cap look): a stadium outline
    # (rounded ends) BEVELED toward the barrel, sitting on the barrel's INNER (head-side) face
    # so the rod + tube ride OUTSIDE the band. Sleek + low-profile. The band's prongs drop
    # into a RECESS in its inner face; a short COVER (grip region only) lets the band sweep out
    # cleanly above. Z values are relative to the barrel mid (z=0).
    slider_clamp_width: float = 44.0       # SET  lozenge length (X) — band width + rounded ends
    slider_clamp_height: float = 22.0      # SET  lozenge height (Z)
    slider_clamp_corner_r: float = 9.0     # SET  lozenge corner radius (the rounded ends)
    slider_clamp_bevel: float = 2.0        # SET  perimeter bevel inner→outer face (the sleek "angle")
    slider_clamp_bevel_head: float = 3.0   # SET  HEAD-side relief: the inner (-Y) face is INSET this much so its
                                           #   perimeter RECEDES from the temple (eased pillow, not a proud square
                                           #   lip). Widest section sits this far behind the contact face. Ergo pass.
    slider_clamp_standoff: float = 6.0     # SET  lozenge depth (Y) proud of the barrel; hosts the inserts
    slider_clamp_z_lo: float = -6.0        # SET  recess/cover bottom Z (holds the prong tip)
    slider_clamp_hole_z: float = 0.0       # SET  Z of the 2 bolt inserts (= prong-tip holes)
    slider_clamp_rib_z: float = 1.5        # SET  Z of the anti-rotation rib (in the channel)
    slider_clamp_rib_height: float = 3.0   # SET  rib Z extent (short — registers, doesn't block the exit)
    slider_clamp_rib_depth: float = 3.0    # SET  rib protrusion into the channel (−Y past the recess floor)
    slider_clamp_cover_thickness: float = 5.0  # SET  inner cover (RETAINING BLOCK) plate thickness — 3→5
                                               #   so the 2 band screws get RECESSED (counterbored) heads.
    slider_clamp_cover_margin: float = 2.0     # SET  how much SMALLER than the lozenge the cover is per side
                                               #   (was a flat −6 width / grip-only height). ~0 → matches the
                                               #   lozenge perimeter so it grips the band over the full block.
    slider_clamp_cbore_diameter: float = 6.2   # SET  counterbore for the M3 socket head (~5.5) + clearance
    slider_clamp_cbore_depth: float = 2.6      # SET  head sinks this far below the cover's outer (head) face
    # Finger SCALLOPS — a shallow concave dish down each of the lozenge's ±X (front/back) ENDS
    # so the hand has a DEFINED pinch to slide the block up/down on the post (the adjust motion).
    # Vertical channels, outboard of the inserts (x=±13) and recess (x=±17), so gate-neutral.
    slider_grip_scallop_r: float = 6.0     # SET  scallop cutter radius (sets dish width)
    slider_grip_scallop_depth: float = 1.2 # SET  how deep the dish bites the end face (subtle, not a hole)
    slider_clamp_cover_ease: float = 1.2   # SET  the cover (first thing to touch the head) drafts inward this much
                                           #   on its head-side face → a soft central crown, rim off the skin. Ergo pass.

    # ---- Bow (BOUGHT Beyer Metal Head Bow / DIY 1095 — INTERFACE ONLY) ------
    # Reference body for assembly + a DIY template. NOT a printed part. The first
    # three are MEASURED off the real Beyerdynamic metal head bow (2026-06-25):
    # the relaxed band is a 5 in circle (→ R 63.5), it rolls out to 9.3 in
    # (→ 236.2 mm developed), strap width 1.3 in (→ 33 mm). The at-rest arc DERIVES
    # from R + developed length (helper below) and lands >180° — the ends sit past
    # the half-circle, exactly as observed. It's spring steel: at rest it's this
    # tight 5 in circle; on a head it flexes OPEN to bow_worn_radius (the assembly
    # poses it flexed, conserving developed length). Thickness + the end-hole specs
    # are still ESTIMATE/REF — no caliper reading yet.
    bow_radius: float = 63.5              # MEASURED  relaxed/at-rest arc radius (5 in dia)
    bow_developed_length: float = 236.2   # MEASURED  rolled-out band length (9.3 in)
    bow_width: float = 33.0               # MEASURED  strap width (1.3 in, top-down)
    bow_thickness: float = 0.8            # ESTIMATE/REF  bow_th (no caliper reading yet)
    bow_worn_radius: float = 78.0         # ESTIMATE  flexed-on-head radius; sets ear spacing
                                          #   (~156 mm cups). The band springs open from the
                                          #   63.5 at-rest; developed length is conserved.
    bow_endtab_hole_diameter: float = 3.2  # ESTIMATE/REF  end-tab mounting-hole dia (M3 clr)
    bow_endtab_hole_inset: float = 5.0     # SET  hole set-in from the prong TIP (near the very end, per photo)
    bow_endtab_hole_spacing: float = 26.0  # SET  pitch of the 2 end holes = the two RAIL CENTRES
                                           #   (= bow_width − bow_rail_width). The real band's end is two
                                           #   separate PRONGS (the rails), one hole near each prong tip,
                                           #   with the big open gap between — NOT a solid tab. Slider follows.
    bow_endtab_width: float = 33.0        # ESTIMATE/REF  band strap width
    # End structure (real band, maker's photo): the two outer RAILS run all the way out
    # to the ends as separate PRONGS — a big open gap between them, a screw hole near each
    # prong tip — and are braced only by a CENTRAL cut-out (no solid end tab).
    bow_endtab_length: float = 28.0       # ESTIMATE  bare prong region at each end (no pad/bracing there)
    bow_rail_width: float = 7.0           # SET  rail/prong width (Y) — wide enough to host the end hole
    bow_prong_tip_r: float = 2.0          # SET  45° clip on each prong-tip corner so the rails end rounded, not square
                                          #   (< bow_endtab_hole_inset 5, so the tip hole stays clear)
    bow_strut_width: float = 3.5          # ESTIMATE  X-brace diagonal strut width
    # Central X cut-out matching the real metal bow (maker's photo): the X cells live
    # in a CENTRAL region (developed length bow_pattern_length), NOT across the whole
    # band — solid rails run out to the solid end tabs that carry the mounting holes.
    bow_pattern_enabled: bool = True      # SET  the real Beyer-style bow has the central X cut-out
    bow_pattern_length: float = 110.0     # ESTIMATE  developed length the X pattern spans (centred)
    bow_pattern_bays: int = 2             # ESTIMATE  number of X cells in the pattern
    # bow_arc_degrees / bow_worn_arc_degrees are DERIVED (helpers below): both
    # conserve bow_developed_length, so the relaxed and flexed bands are one strap.

    # ---- Headband pad (ROUGH DRAFT — crown cushion under the bow) -------------
    # Soft comfort pad (foam / printed TPU) hugging the bow's concave underside at
    # the crown. First pass — a simple arc band; form/retention refined later. All
    # ESTIMATE. One shared pad at the crown (not per-ear).
    # Full-arc cushion that WRAPS the band: a head-side cushion (thickness) plus a lip
    # OVER the top (wrap), spanning the band BETWEEN the end tabs. The band nests in a
    # channel and the pad wraps its underside, both edges, and over the top. (was an
    # 80° crown-only band on the bow's inner face.)
    headband_pad_thickness: float = 8.0          # ESTIMATE  head-side cushion depth (radial, below the band)
    headband_pad_wrap: float = 4.0               # SET  cushion lip OVER the top of the band (the wrap)
    headband_pad_width: float = 40.0             # ESTIMATE  total width (> 33 mm band → wraps the edges)
    headband_pad_channel_clearance: float = 1.0  # SET  band↔pad slot clearance (the bow nests in)
    # Leather-cushion look (à la a Beyerdynamic headband pad, but NO snap buttons —
    # generic, not a specific product): transverse PLEAT seams quilt the underside.
    headband_pad_pleats: int = 7                  # SET  transverse pleat seams across the cushion
    headband_pad_pleat_radius: float = 2.5        # SET  pleat-seam groove radius (rounded)
    headband_pad_pleat_depth: float = 1.2         # SET  how deep each pleat seam cuts the cushion

    # ---- Earpad (round cushion MOCKUP — COMMODITY, we neither design nor ship it) -
    # A representative pad so the assembly + website read like a finished headphone.
    # NOT a printed part and NOT in the BOM as ours: First Chair builds a rim to the
    # Grado pattern and the builder buys whatever pad they like.
    #
    # RESCALED TO A SUPRA-AURAL FLAT, 2026-08-06. These were Daily Driver's DT 770-class
    # numbers — Ø100 OD, Ø60 opening, 24 deep — i.e. a CIRCUMAURAL pad on a Ø54 on-ear
    # cup. Nothing errored, because the pad is a reference mockup that no gate checks,
    # but it is the first thing anyone sees: the published 3D model on the website showed
    # an on-ear headphone wearing over-ear pads, and front_cavity_volume_cc — the number
    # the spec calls the main tuning lever — was computed from it (67.9 cc, on a pad that
    # does not fit the product).
    #
    # PRECISION, stated because two of these are chosen rather than measured: the pad is
    # explicitly NOT measured before the first print (maker's call — compliant foam reads
    # badly and the fit is forgiving), so this is a VISUALISATION mockup, not a spec.
    earpad_outer_diameter: float = 60.0   # REF  the one number with backing: the concept-mesh read
                                          #   put a Grado-pattern pad at Ø60 OD and the maker's note on it
                                          #   was "60 mm OD is right". Overhangs the Ø54 rim, as foam does.
    earpad_inner_diameter: float = 38.0   # ESTIMATE — CALIPER PENDING. The least-supported number here;
                                          #   nothing in the brief pins the flat's opening. Drives
                                          #   front_cavity_volume_cc, so treat that figure as soft too.
    earpad_base_flat: float = 1.5         # SET  flat mounting base (seats on the cup front rim)
    earpad_depth: float = 9.0             # ESTIMATE  pad height = the FRONT-CAVITY depth. The brief puts
                                          #   Grado FLATS at ~8–10 mm and flags the concept mesh's 17.6 as
                                          #   "bowl-thickness, not flat — a bass decision made by accident".
                                          #   9.0 is the middle of the stated flat range. Swapping flats for
                                          #   bowls is the builder's main tonal lever, and on this build that
                                          #   is a purchase, not a reprint — so this number is a DEFAULT to
                                          #   visualise, not a design commitment.
    earpad_worn_depth: float = 5.5        # SET  WORN SEATED-CONTACT depth — the cup-front→head-surface gap in
                                          #   the worn pose (sets cup spacing). The assembly shows the FULL pad,
                                          #   which then COMPRESSES (earpad_depth − this = ~3.5 mm) into the head
                                          #   = the worn CLAMP contact. Scaled with the pad: a supra-aural sits on
                                          #   the ear, so both the free height and the squash are much smaller than
                                          #   a circumaural's. Acoustic helpers still use the relaxed earpad_depth.

    # ---- Acoustic geometry (v0.3 acoustic pass) ------------------------------
    # CLOSED-BACK VARIANT REMOVED 2026-08-07. First Chair is an open-back on-ear, full stop.
    #
    # It arrived with the fork as Daily Driver's "Studio clone" scope: a cup_open_back toggle
    # that swapped the rear grille for a solid back plus a ring of pluggable tuning ports
    # (cup_port_*, vent_plug_*, parts/vent_plug.py). Two reasons it is gone rather than fixed:
    #
    #   1. IT DOES NOT FIT AT 54 mm, and that was a real finding, not a tuning problem. The
    #      ports live in the back-band floor between the damping ring and the baffle bosses.
    #      Rebuilt at 54 the bosses sit at r20.5 — hard against the wall, as far out as they
    #      can go — so the floor inside them ends at r17.0 while the damping ring already
    #      reaches r16.5. No Ø6 port fits a 0.5 mm annulus, and shrinking the felt until one
    #      does gives a token Ø19 disc over a Ø38 grille zone.
    #   2. THE LINE NOW HAS A CLOSED-BACK PRODUCT. Session is the over-ear closed monitoring
    #      build. First Chair carrying its own closed-back conversion is a second answer to a
    #      question another product already owns.
    #
    # Applying the maker's own rule 1: if a mechanism isn't needed, delete it — "an extra
    # weakness we do not need." The geometry, the vent plug part, the BOM row and the gate
    # check all went with it. Recoverable from git history if Session ever wants the pattern.
    #
    # Shared with the (removed) variant and KEPT, because the open-back build uses them:
    # the damping disc and the front-seal gasket, below.
    # Rear DAMPING — a felt / open-cell disc over the grille's INNER face that tames cone
    # breakup + reflections (light, tune by ear). Located by a thin printed RETAINING RING on
    # the interior back floor (the felt drops inside it). Felt itself is a soft good (BOM). The
    # ring stays INSIDE the baffle-boss circle (r35) so it never fouls a boss.
    # damping_felt_diameter is now DERIVED (see the helpers). Its stated rule — "the ring stays
    # INSIDE the baffle-boss circle so it never fouls a boss" — was written against bosses at r35
    # and encoded as the absolute 38.0. Rebuilt at 54 the bosses come inboard to r20.5, which the
    # old 38.0 (ring outer r20.5) would have run straight into. The rule is now the arithmetic.
    damping_felt_thickness: float = 3.0    # ESTIMATE  felt / open-cell thickness
    damping_ring_wall: float = 1.5         # SET  retaining-ring wall
    damping_ring_height: float = 3.0       # SET  ring height proud of the interior floor (≈ felt thickness)
    # FRONT-SEAL GASKET — a foam ring between the driver frame rim and the baffle seat,
    # compressed by the clamp ring so the driver↔baffle joint seals (no front air leak that
    # would short the front cavity). Soft good (BOM); dimensioned here so the SQUEEZE is
    # explicit and gate-checked into the 30–50 % band (too little = leak, too much = bottomed).
    front_gasket_thickness: float = 1.5    # ESTIMATE  free (uncompressed) foam thickness
    front_gasket_compressed: float = 1.0   # ESTIMATE  seated gap the clamp leaves → ~33 % squeeze
    front_gasket_width: float = 2.5        # ESTIMATE  radial width of the seal ring (on the frame rim)

    # ---- Fit coupons (printable QA pieces; lock tolerances vs real hardware) --
    # Small parts that ISOLATE a toleranced interface so it's checked against the
    # real driver / clamp ring / pad BEFORE committing a full cup or baffle print.
    # Every fit dimension DERIVES from the real interface params above
    # (driver_recess_diameter, driver_clamp_*, cup_outer_diameter, pad_lip_*), so a
    # coupon CAN'T drift from the part it validates — only the coupon's own
    # scaffolding lives here. ACCESSORIES (STL+STEP), not in the assembly/gallery.
    coupon_driver_puck_margin: float = 4.0   # radial wall around the back recess (puck OD = recess + 2×)
    coupon_driver_tab_width: float = 10.0    # width of each spoke carrying a standoff boss out to the clamp BCD
    coupon_pad_ring_wall: float = 3.0        # coupon ring wall — rigidity only (NOT the real ~6.72 cup wall)
    coupon_pad_ring_height: float = 15.0     # grip-wall height below the lip (>= a typical pad mount-skirt depth)

    # ---- Mechanical primitives (convention; see parts/features.py) ----------
    boss_base_fillet: float = 1.0         # fillet tying a boss to its host (print)
    screw_post_diameter: float = 7.0      # socket-head fastener post OD
    screw_post_pilot_diameter: float = 2.5  # thread-form pilot; confirm per screw

    # ---- Print / fit ---------------------------------------------------------
    fit_clearance_friction: float = 0.2   # friction fit
    fit_clearance_slip: float = 0.35      # slip fit
    edge_fillet: float = 1.5              # general comfort/print fillet

    # ---- Derived helpers -----------------------------------------------------
    @property
    def driver_aperture(self) -> float:
        # front acoustic opening = frame od − a seat ledge each side; derives from
        # driver_od so the baffle regenerates coherently for any driver size.
        return self.driver_od - 2 * self.driver_seat_ledge

    @property
    def driver_recess_diameter(self) -> float:
        # back recess the driver frame drops into = od + fit tolerance.
        return self.driver_od + self.driver_cutout_tolerance

    @property
    def driver_clamp_standoff(self) -> float:
        # baffle-back boss height = how far the driver protrudes behind the back face
        # = body_depth − the shallow seat. Derived so it tracks driver_recess_depth.
        return self.driver_body_depth - self.driver_recess_depth

    @property
    def adapter_target_aperture(self) -> float:
        # the adapter's front opening, by the same seat-ledge rule as the baffle.
        return self.adapter_target_driver_od - 2 * self.driver_seat_ledge

    @property
    def cup_wall_thickness(self) -> float:
        # The cup's ACTUAL radial wall.
        #
        # MEASURED FROM THE BODY, NOT THE PLATE. First Chair computed this against
        # cup_outer_diameter, and that was correct there because its OD *was* the body —
        # its retaining lip was a separate outward brim. On First Chair the lip IS the
        # baffle plate overhanging the body, so cup_outer_diameter (54.0) is the PLATE
        # and the wall lives on the body (48.0). Using the plate here reports 6.0 mm
        # where the real wall is 3.0 — it would pass every gate while printing a shell
        # half as thick as the number claimed.
        return (self.cup_body_diameter - self.cup_interior_diameter) / 2

    @property
    def cup_body_height(self) -> float:
        # Z extent of the Ø48 BODY — everything below the overhanging Ø54 front lip.
        return self.cup_depth - self.cup_lip_depth

    @property
    def cup_interior_depth(self) -> float:
        # air space behind the front rim = overall depth less the solid grille back band.
        return self.cup_depth - self.cup_back_thickness

    @property
    def cup_interior_volume_cc(self) -> float:
        # REAR acoustic void = the interior cylinder (ID × interior depth), in cc.
        # Uses cup_interior_depth, NOT cup_depth: on this build cup_depth is the OVERALL
        # front→back dimension (LOCKED 27.6), so feeding it in here double-counted the
        # 6 mm back band and over-reported the void.
        return math.pi * (self.cup_interior_diameter / 2) ** 2 * self.cup_interior_depth / 1000.0

    # ---- Grille, derived from the VOID it spans (rebuilt at 54, 2026-08-06) ----
    # The mark's own 64-grid proportions, kept in one place so the logo can only ever be
    # scaled, never re-typed: outer ring r24 / stroke 5, inner r13.5 / stroke 2.5, dot r4.2.
    # The mark's outer EDGE on that grid is 24 + 5/2 = 26.5, which is what the logo scale
    # normalises against.
    _LOGO_GRID = dict(outer_r=24.0, outer_w=5.0, inner_r=13.5, inner_w=2.5, dot_r=4.2, edge=26.5)

    @property
    def grille_zone_radius(self) -> float:
        # the grille opens the VOID, less a landing ring of solid floor at the wall.
        return self.cup_interior_diameter / 2 - self.grille_rim_land

    @property
    def _logo_scale(self) -> float:
        return (self.grille_zone_radius * self.grille_logo_zone_fraction) / self._LOGO_GRID["edge"]

    @property
    def grille_outer_ring_radius(self) -> float:
        return self._LOGO_GRID["outer_r"] * self._logo_scale

    @property
    def grille_outer_ring_width(self) -> float:
        return max(self._LOGO_GRID["outer_w"] * self._logo_scale, self.grille_member_min_width)

    @property
    def grille_inner_ring_radius(self) -> float:
        return self._LOGO_GRID["inner_r"] * self._logo_scale

    @property
    def grille_inner_ring_width(self) -> float:
        # the mark's proportional stroke lands BELOW the printability floor at this scale
        # (1.34 mm), so the floor wins. The mark cannot be reproduced proportionally on a
        # 54 mm cup — that is a fact about the printer, and it is why it is clamped here
        # rather than quietly re-typed as an absolute.
        return max(self._LOGO_GRID["inner_w"] * self._logo_scale, self.grille_member_min_width)

    @property
    def grille_hub_diameter(self) -> float:
        return max(2 * self._LOGO_GRID["dot_r"] * self._logo_scale, self.grille_member_min_width)

    @property
    def grille_lattice_pitch(self) -> float:
        return self.grille_zone_radius * self.grille_lattice_pitch_fraction

    @property
    def driver_clamp_bolt_circle(self) -> float:
        # between the baffle's vent ring and the frame bolt circle — the rule the old 60.0
        # absolute carried in its comment. vent_r matches baffle.py's own derivation.
        vent_r = (self.driver_aperture / 2 + self.baffle_screw_radius) / 2
        return 2 * (vent_r + self.baffle_screw_radius) / 2

    @property
    def damping_felt_diameter(self) -> float:
        # felt sits inside the baffle-boss circle: boss edge, less the ring wall and a
        # clearance. The rule the old 38.0 absolute was standing in for.
        return 2 * (self.baffle_screw_radius - self.baffle_boss_diameter / 2
                    - self.damping_ring_wall - 0.5)

    # ---- Cup back form, derived (rebuilt at 54, 2026-08-06) -------------------
    @property
    def cup_dome_height(self) -> float:
        # the dome lives ENTIRELY inside the solid back band, so the side wall above the
        # void floor is a clean full-thickness cylinder and can never be thinned by the
        # taper. Daily Driver's 12.0 absolute ran 6 mm past the floor on this cup.
        return self.cup_back_thickness

    @property
    def cup_back_face_radius(self) -> float:
        # flat back face the grille/ports sit on; floored so the grille always lands on it.
        return max(self.cup_body_diameter / 2 - self.cup_dome_bulge,
                   self.grille_zone_radius + 0.5)

    @property
    def front_cavity_volume_cc(self) -> float:
        # FRONT cavity = the pad's enclosed space at the ear (ear-opening area × pad depth).
        # Tracks earpad_depth, so the main tuning lever (pad choice) is reflected in cc.
        return math.pi * (self.earpad_inner_diameter / 2) ** 2 * self.earpad_depth / 1000.0

    @property
    def front_gasket_squeeze(self) -> float:
        # fractional compression of the front-seal foam (gate-checked into 0.30–0.50).
        return (self.front_gasket_thickness - self.front_gasket_compressed) / self.front_gasket_thickness

    @property
    def cup_total_height(self) -> float:
        # OVERALL front→back — which is exactly cup_depth, LOCKED at 27.6.
        #
        # This used to return cup_depth + cup_back_thickness, and that was right on Daily
        # Driver, where cup_depth meant the INTERIOR depth (20.0) and the back band was
        # added to it. On First Chair cup_depth is the overall dimension off the reference
        # profile, so adding the band on top built a 33.6 mm cup against a 27.6 mm lock —
        # the same inherited-semantics failure as cup_wall_thickness reporting 6.0 for a
        # 3.0 wall, and just as invisible: nothing checks a total the model never states.
        return self.cup_depth

    @property
    def baffle_screw_radius(self) -> float:
        # bolt circle the cup bosses AND the baffle holes share (aligned).
        #
        # DERIVED at 54 (was the absolute baffle_bolt_circle_diameter = 70.0, i.e. r35 on a
        # cup whose body radius is 24.0). The boss sits as far out as it can go without
        # standing proud of the shell — outer edge flush with the body OD — which is also
        # the deepest bite it can take into the 3 mm wall.
        return self.cup_body_diameter / 2 - self.baffle_boss_diameter / 2

    @property
    def baffle_bolt_circle_diameter(self) -> float:
        return 2 * self.baffle_screw_radius

    @property
    def baffle_hub_radius(self) -> float:
        # radius out to which the baffle stays FULL thickness (covers the driver recess +
        # collar + guard); the outer ring beyond this is thinned (front recessed).
        return self.driver_recess_diameter / 2 + self.driver_collar_wall + self.baffle_hub_margin

    @property
    def baffle_vent_inner_r(self) -> float:
        return self.baffle_hub_radius + self.baffle_vent_zone_gap

    @property
    def baffle_vent_outer_r(self) -> float:
        # stay clear of the screw bolt circle (heads + the solid rim that carries them)
        return self.baffle_screw_radius - self.baffle_counterbore_diameter / 2 - self.baffle_vent_zone_gap

    @property
    def cup_interior_floor_z(self) -> float:
        # top of the interior back floor (now the thickened back band)
        return self.cup_back_thickness

    @property
    def baffle_seat_z(self) -> float:
        # baffle underside / boss-top height: baffle sits flush with the front rim
        return self.cup_total_height - self.baffle_thickness

    @property
    def baffle_boss_floor_z(self) -> float:
        # one-piece cup: bosses stand on the interior back floor (solid) and run up to
        # the baffle underside — a full-height buttressed column tied to the floor + wall.
        return self.cup_interior_floor_z

    @property
    def baffle_boss_height(self) -> float:
        # boss columns run from the interior back floor up to the baffle underside
        return self.baffle_seat_z - self.baffle_boss_floor_z

    @property
    def pivot_boss_z(self) -> float:
        # Pivot bosses sit FORWARD of cup mid-depth by pivot_boss_forward (toward the pad/head
        # side), so the yoke→band junction pulls inboard (tighter clamp, more compact). At
        # pivot_boss_forward=0 it's back at the balanced mid.
        return self.cup_total_height / 2 + self.pivot_boss_forward

    @property
    def yoke_pivot_centres(self) -> float:
        # fork span follows the BODY it straddles, plus the boss stand-off per side.
        # Was the absolute 98.0 — see the note at pivot_boss_proud; that number is what
        # left two pivot bosses floating free of the cup.
        return self.cup_body_diameter + 2 * self.pivot_boss_proud

    @property
    def pivot_boss_outer_radius(self) -> float:
        # external boss outer face seats the fork eye at pivot_centres/2
        return self.yoke_pivot_centres / 2

    @property
    def pivot_boss_through_span(self) -> float:
        # radial length from the void wall out to the boss face: the boss spans the full
        # 3 mm wall and stands pivot_boss_proud clear, with its inner end stopping flush
        # IN the wall (no lug into the cavity). Must exceed insert_boss_depth so the
        # heat-set insert is fully housed — gate-checked.
        return self.pivot_boss_outer_radius - self.cup_interior_diameter / 2

    @property
    def bow_arc_degrees(self) -> float:
        # at-rest arc span — DERIVES from the measured radius + rolled-out length
        # (θ = L / R). With 236.2 / 63.5 this lands ~213°, i.e. >180°: the ends sit
        # past the half-circle, matching the observed relaxed band.
        return math.degrees(self.bow_developed_length / self.bow_radius)

    @property
    def bow_worn_arc_degrees(self) -> float:
        # flexed-on-head arc span — the SAME strap (same developed length) opened
        # out to bow_worn_radius: θ = L / R_worn (~173° at R 78). < at-rest arc.
        return math.degrees(self.bow_developed_length / self.bow_worn_radius)

    @property
    def ear_half_spacing(self) -> float:
        # worn cup-centre half-spacing = where the flexed band's ends land
        # (R_worn · sin(half-arc)). ~78 mm → cups ~156 mm apart.
        return self.bow_worn_radius * math.sin(math.radians(self.bow_worn_arc_degrees / 2))

    def bow_radius_for_ear_half(self, ear_half: float) -> float:
        """The SPRING bow's flexed radius that lands its ends at ±ear_half — i.e. the
        radius the steel band opens to on a head of that breadth, CONSERVING the measured
        developed length (so it's the same physical strap, just flexed). Solves
        R·sin(L/2R) = ear_half (the ends sit at R·sin(half-arc), arc = L/R) by bisection.
        Lets the maker see the band 'flex' per head: a wider head → larger R, flatter arc."""
        L = self.bow_developed_length
        lo, hi = ear_half + 1e-3, 10 * ear_half   # R must exceed ear_half; ample upper bound
        for _ in range(60):
            mid = (lo + hi) / 2
            ends = mid * math.sin(min(math.pi, L / (2 * mid)))  # clamp: arc never exceeds full circle
            if ends < ear_half:
                lo = mid
            else:
                hi = mid
        return (lo + hi) / 2

    @property
    def bow_worn_radius_s(self) -> float:
        return self.bow_radius_for_ear_half(self.head_s_ear_half)

    @property
    def bow_worn_radius_l(self) -> float:
        return self.bow_radius_for_ear_half(self.head_l_ear_half)


# Importable singleton used by every part module.
P = Params()
