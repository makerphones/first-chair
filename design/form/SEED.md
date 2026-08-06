# Claude Design seed — First Chair form pass

**Hand this to Claude Design at the start of the session.** It is the `seed` half of the
reproducible unit `(skill + seed + prompt)` — see `docs/design-pipeline.md`. Record the skill
selected and the prompts used alongside the GLB in `design/form/<date>/`, or the result cannot
be reproduced.

How to use it: create a Claude Design project, **select the 3D design skill**, seed the project
from this repo (or upload this file), then run the conversation. There is no MCP verb for the
3D agent, so the loop is: prompt there → download the GLB → `inspect_glb.py` → ingest here.

---

## What we are designing

An open-back **supra-aural (on-ear)** headphone around a 40 mm driver. 3D-printed, open source,
built by hobbyists who will fork and modify it. It is a flagship first build.

**Read the full brief in `docs/industrial-design-brief.md`.** This file is the operational
subset: the constraints you must not break, and the conventions the output must satisfy.

---

## Output conventions — non-negotiable, and two of them fail silently

1. **1 unit = 1 mm.** glTF's spec convention is metres. A model that does not state its units
   imports at **1/1000** into a slicer — a Ø54 cup arrives as a 0.054 mm speck. Nothing errors.
2. **GLB only. Never OBJ.** OBJ has no scene graph — it carries groups, not parent/child nodes
   — so it *structurally cannot* express the hierarchy below, which is the entire reason we
   are using a 3D tool rather than an image tool.
3. **Name every mesh to this contract**, exactly. When names match, ingest is nearly free; when
   they don't, someone hand-maps every mesh. `_R` / `_L` suffixes throughout:

```
earcup        cup_R/L · baffle_R/L · driver_R/L · driver_clamp_R/L
earpad        earpad_R/L
gimbal        yoke_R/L · yoke_rod_R/L
headband      bow_ref · slider_R/L · slider_shoe_R/L · headband_clamp_R/L · thumbscrew_R/L
headband pad  headband_pad
```

4. **Say what you cannot do.** If a number doesn't close, say so rather than fudging it. We
   would rather have a direction with a stated conflict than a mesh that hides one.

---

## Hard dimensional constraints

These are locked and regenerate the whole CAD model. A direction that breaks one is out.

```
front plate / pad rim     Ø 54.0     the pad-mount interoperability dimension
cup body                  Ø 48.0     what the pad grips, behind a 3.0 mm lip
interior                  Ø 42.0     → 3.0 mm wall
overall cup depth            27.6
driver                       40 mm
```

Architecture: sprung steel bow (bought, screwed at its end tabs) → printed slider → printed
yoke → printed cup + separate baffle + clamp ring. **Three degrees of freedom** — swivel and
tilt at the cup, plus slider travel.

---

## What is wrong with the current model, and what to fix

The existing CAD is a **shrunken over-ear**. It was forked from our circumaural build, the
dimensions were reset to the numbers above, and the *form* was never redesigned: it still has
a DT880-family convex domed cup, a circumaural stance, and (until today) over-ear pads on a
Ø54 rim.

**A supra-aural is a different object, not a small version of another object.** It sits *on*
the ear: small cup, small pad, light band, close to the head. That is the thing to design.

---

## The reference, and the boundary on it

**Grado is the architectural reference, not the styling target.** It is right about *what a
supra-aural is* — small cup, rod-in-block gimbal, minimal band, flat rear face, everything
visible and serviceable. It is wrong as a thing to copy. Where we diverge on purpose:

| Grado does | We do | Why |
|---|---|---|
| Barrel profile from wood turning | Whatever prints well | A barrel is a *lathe* form; inheriting it copies a manufacturing process we don't use |
| Separate Ø45 × 2 mm screen disc | Integral printed grille | One fewer part to source |
| Driver registered behind a restricted aperture | Aperture as a free acoustic variable | Our clamp ring means the aperture need not double as the register |
| Glued / pressed assembly | Clamp ring, serviceable | Serviceability beats manufacturability here — the user is a tweaker |

Do not reproduce Grado's geometry. Match the pad-mounting diameter (an interoperability
dimension, like a screw thread) and nothing else.

---

## Two things we will push back on, so please pre-empt them

**"Family" by repeated detail is the weak version.** We want **proportion and rule** —
something that still works at Ø54 here and at Ø91 on our over-ear sibling, because these two
have to read as siblings. **State the rules in words before you model anything.**

**Do not drift to glossy injection-moulded consumer product.** This is a printed, bolted,
serviceable object and it should look like one: visible fasteners are fine, visible layer
direction is fine, a parting line is not a flaw. Honest engineering through a maker lens.

---

## What to produce

**3–5 distinct form directions**, not one refined one. For each:

- the **rule** it is built on, in words, first
- how the **cup profile** resolves (the current convex dome is inherited and up for replacement)
- how the **rear grille** reads — ours is a triangular lattice with the logo riding flush on it,
  currently proportioned for the wrong cup size
- the **gimbal**: ours is a fork-yoke inherited from an over-ear. Grado's rod-in-block gets one
  rotational axis for free; ours pushes both rotations out to designed joints, which makes the
  yoke the crowded part. Worth attacking.
- the **worn stance and silhouette** — the thing that most says "on-ear" or doesn't

Remember what happens next: **you have no boolean operations, so nothing here becomes a part.**
The chosen direction is re-authored by hand in parametric CadQuery. Give us industrial-design
intent, correctly scaled and correctly named, and that handoff works.
