# First Chair — Design Log

For an open design, the log *is* part of the product. Every decision, every
measurement, every iteration goes here so anyone can follow the reasoning, not
just the result. Newest entries at the top.

This log starts at the fork. Daily Driver's log stayed with Daily Driver — it is
that product's history, not this one's.

---

## 2026-08-06 — Rebuilding the cup at 54: what the fork inherited, and the one thing that did not survive

**Starting state:** 17/17 parts building, `gate.py` red on one HARD check —
`manifold:cup: 3 solid(s), valid=True (want 1, True)`.

**The reported hypothesis was the rear grille lattice.** It was not. The grille was
genuinely broken, but it was not what split the cup into three solids.

### The actual cause: `yoke_pivot_centres = 98.0`

That number is Daily Driver's Ø91.44 cup plus ~4 mm of boss stand-off per side, and
it came through the fork untouched. It drives `pivot_boss_outer_radius`, so the two
yoke pivot bosses were being built spanning **r40 → r49 on a cup whose body radius is
24.0**. They touched nothing. Dumping the solids says it plainly:

```
0: vol=  48813.1  x[ -33.52,  33.52]  z[ 0.00, 33.60]   <- the shell
1: vol=    942.5  x[  40.00,  49.00]  z[14.80, 26.80]   <- a pivot boss, floating
2: vol=    942.5  x[ -49.00, -40.00]  z[14.80, 26.80]   <- the other one
```

**The part worth remembering is how quietly it passed everything else.** `gate.py`
reported `[PASS] pivot-clearance: boss proud 22.0 mm >= 2.0 mm` — because a boss
attached to nothing is extremely proud of the wall. The check measured
`pivot_boss_outer_radius − cup_outer_diameter/2` and got a large positive number,
which is exactly what "healthy" looks like. **A check written at one scale can read as
confirmation at another.** It now measures against the body, which is the wall the
boss actually sits on.

### The audit, since one absolute surviving the fork means all of them did

Diffing the fork against Daily Driver: **eight values changed, everything else is still
a Ø91.44 number.** Auditing every radial dimension the cup touches against the new
scale (body r24.0, void r21.0):

| Parameter | Was | At 54 mm |
|---|---|---|
| `cup_back_face_radius` | 35.0 | **larger than the cup's own radius** — the "dome" lofted OUTWARD to Ø70 |
| `cup_dome_height` | 12.0 | ran 6 mm past the void floor and thinned the wall below 3.0 |
| grille zone edge | r33.0 | 9 mm outside the shell — cut in air |
| `grille_lattice_pitch` | 16.0 | ≈ the zone diameter; 3 bars, no mesh |
| `baffle_bolt_circle_diameter` | 70.0 (r35) | 11 mm outside the body — four columns in open air |
| `baffle_boss_diameter` / flare | 12.0 / 15.0 | a quarter of the cup's diameter |
| `yoke_pivot_centres` | 98.0 | **the manifold failure** |
| `damping_felt_diameter` | 38.0 | ring outer r20.5, straight into the rebuilt boss circle |
| `driver_clamp_bolt_circle` | 60.0 (r30) | off the Ø54 baffle entirely |
| `cup_port_circle_diameter` | 50.0 (r25) | outside the void |

**These are not nudged. They derive now**, so they cannot drift out of scale again.
The pattern in almost every case: the *rule* was already written in the parameter's own
comment, and the absolute was standing in for it. `driver_clamp_bolt_circle` literally
said "between vents (r26) + frame holes (r35)" — that sentence is the arithmetic, and it
is now the arithmetic. Same for the damping ring ("stays inside the baffle-boss circle"),
the dome height ("capped by the void wall"), and the grille zone.

One value deliberately did **not** scale: `grille_lattice_member_width = 2.2`. That one
is a legitimate absolute — it is a nozzle multiple (0.4 × 5.5), set by the printer, not
by the part. Worth naming the distinction explicitly, because "scale everything" is as
wrong as "scale nothing".

### Two more inherited-semantics bugs, same class as `cup_wall_thickness`

Both invisible for the same reason: the model never stated the number, so nothing checked it.

1. **`cup_total_height` returned `cup_depth + cup_back_thickness`.** Correct on Daily
   Driver, where `cup_depth` meant the *interior* depth. Here `cup_depth` is the overall
   front→back dimension off the reference profile and is **LOCKED at 27.6** — so the model
   was building a 33.6 mm cup against a 27.6 mm lock. Now returns `cup_depth`, with
   `cup_interior_depth` derived for the volume calc (which had been over-reporting the void
   by double-counting the back band).

2. **`cup.py` built the shell at `cup_outer_diameter` (54.0).** The Ø54 is the front
   **plate**; the shell is the Ø48 **body**. Building it at 54 gave a 6 mm wall while
   `cup_wall_thickness` correctly reported the real 3.0 — the exact failure already caught
   one level up in params, repeated one level down in geometry — and it deleted the step
   the pad hooks behind. The cup is now the Ø48 body with a Ø54 × 3.0 lip, which lands the
   overall depth on 27.6 for free.

   `parts/coupon.py` had the same read: the pad coupon was validating fit against a grip
   surface 6 mm too big, which is precisely the fit a coupon exists to catch.

### The grille, rebuilt rather than nudged

It now derives from `cup_interior_diameter`: the zone is the void less `grille_rim_land`
(2.0, at the member floor) — a landing ring of solid floor that carries the mesh into the
wall. The logo scales into that zone by the mark's own 64-grid proportions, held in one
place (`_LOGO_GRID`) so it can only be scaled, never re-typed.

**The mark cannot be reproduced proportionally at 54 mm.** Its inner ring stroke lands at
1.34 mm, below the 2.0 printability floor, so the floor wins and the ring is clamped. That
is a fact about the printer, and it is clamped in the derivation rather than quietly
re-typed as an absolute.

**Two bugs found while doing it, both created by splitting the logo from the zone** — a
distinction that did not exist before, because the mark used to fill the zone exactly:

- `gate.py` measured open area over `grille_outer_ring_radius + width/2`, i.e. the *logo's*
  edge. Once the mark shrank inside the zone that silently excluded the lattice-only
  annulus outside it — about 44 % of the zone, and the most open part.
- `cup.py` cut its zone from the same expression, so it punched a hole the size of the
  **logo** and left everything out to the wall solid: a 6 mm back plate with a badge in it,
  measuring **0.075 open**. Caught on the render, not the number.

**`grille_logo_zone_fraction` is a new taste knob and it is a real trade — maker's eye
wanted.** At 1.0 (Daily Driver's implicit value) the mark closes ~47 % of the zone unaided;
the lattice pitch then has to open past the zone radius to stay in the open-area band,
which leaves 3 bars per angle — only the through-centre bars survive and the "triangular
lattice" degenerates into a **6-spoke wheel**. That puts the logo back to being the
structure, which is the arrangement the Stage 1b rework specifically inverted. Set to
**0.60**, which buys 5 bars per angle and lands open area at **0.388** against a 0.40
target. Cost: the mark is Ø22.8 on a Ø38 grille rather than filling it. **0.75 with pitch
0.66 also passes** (open 0.436) if the bolder mark is worth the spoke wheel — that is a
look-at-it decision, not a numbers one.

### Left failing on purpose: the closed-back variant

`gate.py` is down from the reported failure to **one HARD failure**, and it is a true
statement about an **inactive** variant (`cup_open_back` defaults True, so the built part
is unaffected):

```
[FAIL] closed-back-ports-clear: ports r17–23 between damping ring r16 and baffle bosses r17
```

The tuning ports live in the back-band floor, between the damping ring and the baffle
bosses. Rebuilt at 54 the bosses sit at r20.5 — hard against the wall, which is as far out
as they can go — so the floor inside them ends at r17.0, and the damping ring already
reaches r16.5. That is a 0.5 mm annulus and no Ø6 port fits in it. Shrinking the felt until
one does drives it to ~Ø19 over a Ø38 grille zone, which is a token disc, not damping.

**So this is a design decision, not a value, and it is not mine to make.** Three ways out:

1. **Drop the closed-back variant from First Chair.** The brief specifies an open-back
   on-ear throughout; this toggle is inherited Daily Driver "Studio clone" scope.
2. **Interleave the ports angularly** between the four bosses (ports at 0/90/180/270 vs
   bosses at 45/135/225/315). The ports pierce z0–6 and the bosses stand from z6 up, so
   they only actually conflict where they share an angle — which means the gate's purely
   *radial* band check is testing for the wrong thing, and only ever passed on Daily Driver
   because that cup was big enough to satisfy the wrong test. Fixing the check is a real
   improvement; it is not one to make while trying to go green.
3. **Segment the damping ring** into arcs between the bosses and reclaim the floor.

### Form note for the next pass

Capping the dome inside the back band makes it **shallow** — 4.5 mm of bulge over 6 mm of
height reads closer to a 45° chamfer than a Denon bulge. The lever is the one Daily Driver
already identified: thicken the back band or reduce the cup ID. `cup_back_thickness` is
still 6.0, an inherited absolute that is 22 % of this cup's total depth; it is defensible
(it is the dome's home) but it has not been re-derived and it is the obvious next knob.

### Still on Ø91.44 numbers, not touched this pass

`baffle_outer_diameter = 77.0` — the plate should be the LOCKED Ø54. The baffle still
builds and passes, but it is a Ø77 disc in a Ø54 world, and its vent zones, guard and
clamp-standoff geometry all sit on Daily Driver radii. **The baffle is the next part to
rebuild**, and it should be done as one pass rather than piecemeal — moving its bolt
circle (done, it is shared with the cup) without moving its plate leaves the two parts
mutually consistent and both wrong against the lock.

Build **17/17**. Gate **1 HARD / 0 SOFT** — the closed-back variant above.
