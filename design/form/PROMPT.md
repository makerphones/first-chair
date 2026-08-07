I'm designing an open-back **supra-aural (on-ear)** headphone around a 40 mm driver — 3D-printed, fully parametric, open source, meant to be downloaded and forked by hobbyist builders. It's the flagship first build of a series: the first rung of a learning path, not the last.

I want **3–5 distinct form directions** to choose between. **Before you model anything, state the rule each direction is built on, in words.**

## What I have now, and why it's wrong

This build was forked from my over-ear headphone. I reset the dimensions to on-ear numbers but never redesigned the *form*, so the CAD is a **shrunken over-ear**: a convex domed cup from a DT880-family design, a circumaural stance, and (until yesterday) over-ear pads sitting on a 54 mm rim. Dimensionally correct, formally the wrong product.

**A supra-aural is a different object, not a small version of another object.** It sits *on* the ear: small cup, small pad, light band, close to the head. That's the thing to design.

## Locked — a direction that breaks one of these is out, however good it looks

```
front plate / pad rim     Ø 54.0     the pad-mount interoperability dimension
cup body                  Ø 48.0     what the pad grips, behind a 3.0 mm lip
cup interior              Ø 42.0     → 3.0 mm wall
overall cup depth            27.6
driver                       40 mm
```

Architecture: a **bought sprung steel bow** (screwed at its end tabs) → printed slider → printed yoke → printed cup + a **separate** baffle + a printed driver clamp ring. **Three degrees of freedom**: swivel and tilt at the cup, plus vertical slider travel.

Pads are a **commodity Grado-pattern part I don't design or ship** — the foam stretches over the Ø54 lip and grips the Ø48 body behind it. That step is the retention feature. Smaller pads are preferred: my own measurements show a small-padded on-ear is ~2.5× more repeatable through 2–8 kHz than a large-padded one, and repeatability is what this design competes on.

No printed springs — no FDM plastic is a good spring, so the band stays steel. Serviceability beats manufacturability throughout; the user is a tweaker who will take it apart.

## The reference, and the boundary on it

**Grado is the architectural reference, not the styling target.** It's right about *what a supra-aural is*: small cup, rod-in-block gimbal, minimal band, flat rear face, everything visible and serviceable. It's the wrong thing to copy — cloning it would be the least interesting version of this project. Where I diverge on purpose:

| Grado does | I do | Why |
|---|---|---|
| Barrel profile from wood turning | Whatever prints well | A barrel is a *lathe* form; inheriting it copies a manufacturing process I don't use |
| A separate Ø45 × 2 mm screen disc | Integral printed grille | One fewer part to source |
| Driver registered behind a restricted aperture | Aperture as a free acoustic variable | My clamp ring means the aperture needn't double as the register |
| Glued / pressed assembly | Clamp ring, fully serviceable | The user takes it apart |

Don't reproduce Grado's geometry. Match the pad-mounting diameter — an interoperability dimension, like a screw thread — and nothing else.

## Two things I'll push back on, so please pre-empt them

**A "family" made by repeating a detail is the weak version.** I want **proportion and rule** — something that still works at Ø54 here and at Ø91 on the over-ear sibling, because those two have to read as siblings. This is why I want the rules in words first.

**Don't drift toward glossy injection-moulded consumer product.** This is a printed, bolted, serviceable object and should look like one. Visible fasteners are fine. Visible layer direction is fine. A parting line is not a flaw. The read I want is *honest engineering, pro-audio sensibility through a maker lens* — considered and functional, not flashy.

## Output conventions — the first two fail silently, so please confirm them explicitly

1. **Author at 1 unit = 1 mm.** glTF's spec convention is metres, so a model that doesn't state its units imports at 1/1000 into a slicer — a Ø54 cup arrives as a 0.054 mm speck, and nothing errors.
2. **GLB only, never OBJ.** OBJ has no scene graph — it carries groups, not parent/child nodes — so it structurally can't express the hierarchy below, which is the whole reason I'm using a 3D tool instead of an image tool.
3. **Name every mesh to this contract, exactly**, with `_R` / `_L` suffixes:

```
earcup         cup_R/L · baffle_R/L · driver_R/L · driver_clamp_R/L
earpad         earpad_R/L
gimbal         yoke_R/L · yoke_rod_R/L
headband       bow_ref · slider_R/L · slider_shoe_R/L · headband_clamp_R/L · thumbscrew_R/L
headband pad   headband_pad
```

4. **Tell me what doesn't close.** If a number doesn't work, say so rather than fudging it. I'd much rather have a direction with a stated conflict than a mesh that hides one.

## What each direction should resolve

- the **rule** it's built on, in words, first
- the **cup profile** — the inherited convex dome is up for replacement
- how the **rear grille** reads — mine is a triangular lattice with a logo mark riding flush on it, currently proportioned for the wrong cup size
- the **gimbal** — mine is a fork-yoke inherited from the over-ear. Grado's rod-in-block gets one rotational axis for free; mine pushes both rotations out to designed joints, which makes the yoke the crowded part. Worth attacking.
- the **worn stance and silhouette** — the thing that most says "on-ear" or doesn't

One thing to keep in mind about what happens next: **you have no boolean operations, so nothing here becomes a printable part.** I re-author the chosen direction by hand in parametric CadQuery. Give me industrial-design intent — correctly scaled, correctly named, with the rules stated — and that handoff works cleanly.
