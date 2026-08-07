# First Chair — the numbers a form pass needs

**This file, not `params.py`.** `params.py` is the engineering source of truth for the *CAD*,
and it still carries a mechanism that was deleted by decision in August — a design pass told to
treat it as authoritative will faithfully redraw a thumbscrew, because that is what it says.
This file is the subset that is true, current, and relevant to form.

If something you need isn't here, ask. Don't infer it from `params.py`.

## Cup — LOCKED, regenerates everything

```
pad rim / front plate     Ø 54.0      the Grado pad-mount interoperability dimension
cup body                  Ø 48.0      what the pad grips, behind the lip
lip depth                    3.0      the step the pad hooks behind — retention is AXIAL
cup interior              Ø 42.0      → 3.0 mm wall
overall depth               27.6      front face to back face
grille zone               r 19.0      = interior/2 − 2.0 landing ring
```

## Driver and pad

```
driver OD                 Ø 39.5      MEASURED. "40 mm" is the nominal name
earpad OD                 Ø 60.0      commodity Grado pattern — we design and ship none
earpad opening            Ø 38.0      ESTIMATE, caliper pending
earpad depth                 9.0      a FLAT pad; bowls are thicker. Swapping is the tonal lever
```

## Bow — bought, measured off the real part

```
relaxed arc radius          63.5      a 5 inch circle
flexed on a head           ~78.0      this sets ear spacing
developed length           236.2      rolled flat
strap width                 33.0      a STRAP, not a wire
strap thickness              0.8
end tabs                   2 prongs ~7 wide, Ø3.2 hole 5 mm from each tip, 26.0 apart
```

Central ~110 mm carries an X-brace cut-out. **No printed springs** — no FDM plastic is a good
spring; a printed band works on day one and is loose by month three.

## Cup ↔ yoke pivot

```
pivot centres             Ø 56.0      = body 48 + 2 × 4 proud
pivot boss                Ø  8.0
boss stands proud            4.0      room for the insert and the arm seat
```

## Print constraints — these are design inputs, not manufacturing notes

```
nozzle / layer            0.4 / 0.2
minimum member               2.0      anything thinner is not printable here
minimum wall                 2.0      design wall is 3.0
structural sections          4.0      anything carrying bending load
```

**Support-free is a design constraint on every part, not a preference.** Layer lines run *along*
the load on anything structural — the yoke arms especially, where layer adhesion is the weak
axis and printing flat-in-plane is the difference between a part that lasts and one that snaps.

## Fasteners — the target

**M3 heat-set inserts, M3 cap screws, M3 washers. Nothing else.** One thread, one insert size,
all metric. Heat-set inserts are kept deliberately: an insert is a small cylindrical bore, where
a captured nut needs a hex pocket, capture geometry, an access slot and clear space *behind* the
joint — and it gives a reusable thread, which a build for tweakers wants.

## What does NOT exist yet

**There is no height-adjustment mechanism, and no slider.** Do not draw one, and do not infer
one from anything you find in the repo. The Daily Driver post-and-thumbscrew that appears in
`params.py` was deleted by decision in August and has never been replaced.

What replaces it is an open question, not a pending implementation:

- a printed cantilever leaf riding a detent ladder, or
- **no height adjustment at all** — discrete positions, or a compliant suspension layer

If a direction needs to take a position on this to be coherent, **say which one it assumes and
why**, and treat it as a proposal rather than a given.
