# makerphones — form brief

Four 3D-printed open-source headphones, built by hobbyists who fork and modify them. I've
designed and prototyped headphones professionally before; rather than describe the house style,
the reference folder next to this file is my own prior work.

## The order — we are at step 1

```
1. FORM — resolved ID, no engineering         ← this pass. judge it as an OBJECT
2. split that form into parts                ← serviceability + printability enter here
3. details: grille, mark, fasteners, joints
4. I re-author it as engineered CAD, by hand
```

Getting this backwards is what went wrong on earlier attempts: asking for **printable parts**
first produces primitives butted together, every junction an abutment, nothing flowing into
anything. That reads as clunky no matter how good the proportions are. Design the object, then
cut it into parts — not the other way round.

## This pass: resolved industrial design, not engineered assembly

**Target: a headphone you could photograph.** I'm attaching renders from the industrial-design
firm that did my previous product — that is the resolution and the language I want back.

Parts **are** parts. You can see the bezel, the face panel, the yoke, the band, the pad. They
are distinct, in distinct materials. They are simply *resolved* — flowing surfaces, not
primitives butted together.

What is **not** there is engineering: no fasteners, no screw bosses, no heat-set inserts, no
grille lattice, no clamp ring, no print-split lines. None of that had been designed when those
renders were made, and none of it belongs in this pass.

### The house language, from those renders

- A **proud polished bezel ring framing a recessed matte face panel**, with the mark centred on
  it. **Concentric rings are the dominant motif.**
- A **flat blade yoke** that arcs down the *outside* of the cup, hugging its edge and
  terminating in a small pivot boss at the front. No bracket, no fork.
- A **flat strap band**, punctuated by polished metal collars at the adjustment points.
- **Four materials do all the separating** — polished metal, wood, leather, foam. There are no
  part lines because the material changes *are* the lines.

**What transfers and what doesn't.** That cup is a **teardrop** because it is a circumaural
with a bespoke pad. First Chair is **round** because a commodity Grado pad sets it. The
*language* transfers across the family; the *outline* does not — see the table below.

Vary the three directions **within** this vocabulary. I'm not looking for three unrelated
styles; I'm looking for three ways this language lands across four differently-sized,
differently-padded products.

### How to build it

- **Build each part from a profile, lofted or swept — not a stack of primitives.** If a section
  changes, it changes *through* the loft. If something is round, the roundness lives in the
  profile curve.
- **Where parts meet, the surfaces relate.** A yoke blade that follows the cup's curve, not a
  bracket abutted to a cylinder. The waisted stem in my shape sketches is the same move.

This plays to what you can do: with no boolean operations you can't cut features into a body
anyway, so lofted surfaces are your strongest mode and butted primitives your weakest. And it
sets up step 2 — **when a form is defined by a profile, splitting it into printable parts is a
split of the profile, not a boolean.**

## Read first

```
design/form/reference/README.md    my own prior work, captioned — START HERE
design/form/reference/*.jpg        prototypes, shape studies, cut headband blanks
params.py                          every number. source of truth.
assembly.py                        SUBASSEMBLIES — the mesh-naming contract
```

`shape-sketches-overview.jpg` is the most useful single image: six cup outlines, each with a
**waisted stem flowing into it** — no step, no boss, no joint. That level of resolution, in 3D,
is what I want back.

If `params.py` disagrees with anything in this document, `params.py` wins and you should say so.

## The intent

Writing to the industrial designer on my previous product:

> "It should exude quality craftsmanship, **almost looking handmade but with extreme
> precision**. Parts should be easily replaceable and durable. Reduce weight where ever
> possible." — something that lasts a lifetime and gets passed down.

"Almost handmade but with extreme precision" tells you what to do with a tolerance, a parting
line, a visible fastener: don't hide them, don't fetishise them, make them look **deliberate**.
A printed part that owns its layer direction is on-brief. One pretending to be
injection-moulded is not.

## Five rules — corrections I gave that designer

1. **If a mechanism isn't needed, delete it.** I killed a fold hinge with *"an extra weakness we
   do not need."* Not "unnecessary" — a **weakness**.
2. **No ornament.** On a decorative step added where the pad met the cup: *"I am assuming this
   is for aesthetic reasons? I do not have to have this."*
3. **Simplify until it's simple, then stop before it's ugly.** *"We're looking to simplify
   without looking ugly. Hopefully we can find a nice middle ground."* Both halves — austere is
   not the same as resolved.
4. **Material follows load.** *"If we don't need the extra metal we can save weight — but it
   does look nice and beefy."*
5. **The prototype settles arguments, not the drawing.**

## The line, and what sets each outline

Every product mounts a **commodity aftermarket pad** the builder buys anywhere. That's a core
principle — and it means **the pad sets the cup outline**. It isn't a styling choice.

| | Type | Pad | Outline |
|---|---|---|---|
| **First Chair** | on-ear, open | Grado | round — a supra-aural sits *on* the ear, so no outline to follow |
| **Daily Driver** | over-ear, open | Beyerdynamic DT | round |
| **Session** | over-ear, closed | ATH-M50x / Sony 7506 | **oval** — a circumaural encloses the pinna, and a pinna is a teardrop |
| **Encore** | over-ear, open | open | free — the one product that can take a bespoke pad |

So rim diameters differ per product **by design**, set from outside by four different pads.
Don't derive one from another, and don't style an outline against its pad.

**That is the family rule, and it's stronger than a shared silhouette:** whatever pad the
builder likes, it fits. What carries across the four is the rim profile and the detail
language, not the outline.

## Numbers

First Chair is locked and regenerates the CAD:

```
pad rim Ø54.0 · body Ø48.0 · bore Ø42.0 · depth 27.6 · driver 40
```

The bow is a bought Beyerdynamic sprung steel part, **identical on all four** — the only
genuinely shared component. Relaxed radius 63.5, opening to ~78 worn (this sets ear spacing),
developed length 236.2, **33 mm wide**, 0.8 thick. Earlier passes drew it 13 mm wide, which
reads as a wire; it's a strap.

Everything else lives in `params.py`.

## What I want back

**The four products at true relative scale**, each resolved as above — bezel, face, pad, yoke,
band, in their materials. Three directions **within the house language**, not three unrelated
styles. One page, one live 3D stage, nav switches between them.

Rule stated in words **before** you model. One line per direction on what doesn't close — those
have been the most useful things you've produced.

**No written study. If it isn't in the stage, it doesn't exist.**

## Conventions

- **1 unit = 1 mm.** glTF's convention is metres; unspecified, a model imports at 1/1000 into a
  slicer and nothing errors.
- **GLB only, never OBJ** — OBJ has no scene graph and can't carry the hierarchy.
- Mesh names per `SUBASSEMBLIES`, `_R`/`_L` throughout.

## Later, not now

So you know the trajectory and don't design it yet: step 2 splits the form and introduces a
separate baffle, a driver clamp ring, and the yoke pivot. The headband slider is a printed
cantilever leaf on a detent ladder — no thumbscrew. The bow screws to the slider through its
own end-tab holes. **None of that belongs in this pass.**
