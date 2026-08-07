# Driver measurements — what to take, and what each number decides

The cup section (`section.py`) currently runs on **two assumptions and one design choice**.
These are the numbers that turn it from plausible into correct. Edit the `DRV_*` block at the
top of `section.py` and re-run.

Current state: `taper_mid`, flush joint, **split at 12.0**, driver flange 3.5 mm back from the
cup face → **7.0 mm front cavity, 3.5 mm behind the driver.**

## The 40 mm dynamic — replacing assumptions

| Measure | Now | Why it matters |
|---|---|---|
| **Dome proud of the flange** | 1.5 **ASSUMED** | Sets how far forward the driver intrudes. Directly trades against front cavity. |
| **One-way excursion** | 0.5 **ASSUMED** | Clearance the dome needs to move into. Under-guess this and the diaphragm hits something. |
| Frame OD | 39.5 measured | Confirm. Sets the seat. |
| Basket depth behind the flange | 5.0 measured | Confirm. Sets the split. |
| Flange thickness | — | The seat ledge it lands on. |
| Magnet OD | 27.0 | Rear clearance to damping / the rear cup. |

**And one nobody remembers until it bites: the solder tabs.** Measure how far the terminals
protrude behind the magnet and where they sit. With only **3.5 mm behind the driver**, the tabs
— not the basket — may well be the binding constraint on where the split goes. If they stick
out 2 mm the tail is effectively 1.5.

## The planar — everything is unknown

Nothing here is measured; the section currently guesses 9 mm body + 3 mm nipple, which pushes
the split to ~17 mm and **breaks the 12 mm front piece.** Worth knowing before you talk to
Pablo, because it is also the spec you would be asking him about.

- overall OD, and flange OD
- **body depth** behind the mounting face
- **front protrusion** — the nipple: height *and* diameter
- mounting hole pattern (PCD + hole count + size) — this is the "different mounting ring"
- terminal position and protrusion

## If the rig is out anyway

Fs, impedance, sensitivity per candidate. The brief calls choosing the driver *"the gate on
everything else"* and measuring candidates *"the highest-leverage day in the project"* — and
the `.mdat` files in the archive turned out to be imported datasheet traces, not captures, so
that day has not actually happened yet.
