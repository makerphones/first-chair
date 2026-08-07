# First Chair — Industrial Design Brief

**v0.2 · 2026-08-06 · rewritten for the supra-aural, and re-opened**

> **This brief was wrong, and the CAD faithfully built the wrong thing.**
>
> v0.1 was Daily Driver's brief with the product name changed. It specified an
> *"open-back, **over-ear (circumaural)** DIY headphone"*, recorded the resolved direction as
> **"DT880-family, around-ear"**, and named a **Dekoni Universal 100 mm** pad. The fork reset
> about eight dimensions in `params.py` and left this file — the thing the geometry is supposed
> to descend from — untouched.
>
> So the model on the website was a **shrunken DT880**: domed cup, circumaural stance,
> over-ear pads on a Ø54 rim. Dimensionally correct, formally the wrong product. Same failure
> as the Ø91 radii in `params.py` and the DT 770 pads in `BOM.md`, one level further upstream.
>
> The rule that would have caught it is `starting-a-new-product.md` step 1b — run the form pass
> in Claude Design **before** writing `params.py`. This build predates that rule.

**Status: the form is OPEN. This brief states the constraints; it deliberately does not state
the answer.** The Diverge pass (`design-pipeline.md`) produces 3–5 directions and the maker
picks one. Do not read a direction into this file that isn't here.

---

## What it is

An open-back **supra-aural (on-ear)** headphone around a 40 mm driver. 3D-printed, fully
parametric, open source (MIT), meant to be downloaded, forked and modified. It is the
**flagship first build** — the first rung of a learning path, not the last.

Sonic character is bright, open, detailed, with modest bass — the honest nature of a small
driver in an open baffle on an on-ear. The form should feel like that: light, airy, unfussy.

## Who it's for, and how it should read

DIY makers and hobbyist builders. The form should read as **honest engineering — pro-audio
sensibility through a maker lens** — not glossy consumer product. Credibility comes from
looking considered, functional and serviceable, not flashy. If it looks like it was designed by
someone who knows audio and respects the person building it, it's working.

**This one needs defending on every pass.** Generative tools drift hard toward glossy
injection-moulded consumer product, because that is what the training data is full of.
Printed, machined and hand-built has to be asked for explicitly and re-asserted on the second
pass — see `design-pipeline.md`.

---

## LOCKED — the form pass works inside these

These are decided. A direction that breaks one of them is out, however good it looks.

**Architecture — supra-aural, and it must read as one.**
The failure to design away from is a scaled-down over-ear. A supra-aural sits *on* the ear:
small cup, small pad, light band, close to the head. It is a different object, not a small
version of another object.

**Dimensions** (see `params.py`; these regenerate everything):

```
front plate / pad rim   Ø 54.0        the pad-mount interoperability dimension
cup body                Ø 48.0        what the pad grips, behind the lip
interior                Ø 42.0        → 3.0 mm wall
overall depth              27.6
driver                     40 mm
```

**Parts** — sprung steel bow (bought, screwed at its end tabs) → printed slider → printed yoke
→ printed cup + separate baffle + clamp ring. **Three degrees of freedom**: swivel and tilt at
the cup, plus slider travel.

**Pads are commodity Grado-pattern.** We design a rim the foam stretches over and ship no pad.
This is the one interface where we deliberately do not innovate — diverging costs the builder
the whole aftermarket. Retention is the **step**: axial on the Ø54 lip, friction on the Ø48
body behind it.

**Prefer the smaller pad.** Not taste — our own 2026-08-03 placement data has the small-padded
SR60x ~2.5× more repeatable through 2–8 kHz than the larger-padded RS1x. Repeatability is what
this design competes on.

**Spring steel, not printed springs.** No FDM plastic is a good spring; a printed band is loose
by month three.

**Serviceability beats manufacturability.** The standing tie-breaker: the user is a tweaker.

---

## OPEN — this is what the pass is for

The form language. Explicitly *not* pre-decided in this file.

**Grado is the architectural reference, not the styling target.** It is the right reference
for *what a supra-aural is* — small cup, rod-in-block gimbal, minimal band, flat rear face,
everything visible. It is the wrong thing to copy: cloning a Grado would be the least
interesting version of this project, and `design-spec.md` §5 already lists where we diverge on
purpose:

| Grado does | We should | Why |
|---|---|---|
| Barrel profile from wood turning | Whatever prints well | A barrel is a *lathe* form; inheriting it copies a manufacturing process we don't use |
| Separate Ø45 × 2 mm screen disc | Integral printed grille | One fewer part, one fewer thing to source |
| Register the driver behind a restricted aperture | Aperture as a free acoustic variable | The clamp ring means the aperture need not double as the register |
| Glued / pressed assembly | Clamp ring, serviceable | The tie-breaker above |

**Ask for the family rules in words before anything is modelled.** The weak version of a
"family" is a repeated detail. The strong version is proportion and rule — something that
still works at 54 mm here and at 91 mm on the Daily Driver, because these two have to look
like siblings.

Specific questions the pass should answer:

- **Cup profile.** The current convex dome is inherited DT880 and is now shallow and
  chamfer-like anyway (it is capped inside the 6 mm back band). Flat rear face? Stepped?
  Something that isn't either?
- **How the grille reads.** The triangular lattice with the logo riding on it is built and
  works, but it was proportioned for a Ø91 cup and rebuilt to fit rather than designed for
  this one. `grille_logo_zone_fraction` is the live knob.
- **The gimbal.** Ours is a fork-yoke inherited from an over-ear. Grado's rod-in-block gets a
  rotational axis for free; ours pushes both rotations out to designed joints and makes the
  yoke the crowded part.
- **The band and how the cup hangs off it.** We inherit a circumaural's arc from the Beyer bow,
  knowingly, until a bow is stocked to our own spec.
- **Stance and worn silhouette** — the thing that most says "on-ear" or doesn't.

---

## Deliverable

3–5 form directions, per `design-pipeline.md`. **GLB, 1 unit = 1 mm, named to the
`SUBASSEMBLIES` contract**, with the `(skill + seed + prompt)` record beside it in
`design/form/<date>/`. Run `makerphones/scripts/inspect_glb.py` on everything that arrives.

The prompt to paste into Claude Design is **`design/form/PROMPT.md`** — self-contained, because
**Claude Design cannot see this repo** and a prompt that says "read the brief" gets a session
working from its own priors instead. It duplicates the constraints above on purpose; when this
file changes, `PROMPT.md` changes with it. `design/form/SEED.md` is the how-to-run notes and
the `(skill + seed + prompt)` record.

Renders and meshes give **appearance, not manufacturable geometry**. Claude Design has no
boolean operations, so nothing printable can originate there: the chosen direction is
translated back into parametric CadQuery by hand.

---

*v0.2 · 2026-08-06 · Rewritten as supra-aural; the resolved-direction claim removed and the
form re-opened. v0.1 · 2026-06-14 · Daily Driver's brief, renamed — see the note at the top.*
