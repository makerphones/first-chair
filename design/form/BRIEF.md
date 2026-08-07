# makerphones — form brief

Four 3D-printed open-source headphones, built by hobbyists who fork and modify them. I've
designed and prototyped headphones professionally before; the reference folder beside this file
is my own prior work.

## The order — we are at step 1

```
1. FORM — resolved industrial design, no engineering   ← this pass
2. split that form into parts                          ← printability + serviceability
3. details: grille, mark, fasteners, joints
4. I re-author it as engineered CAD, by hand
```

Ask for printable parts in step 1 and you get primitives butted together, every junction an
abutment. Design the object, then cut it into parts.

## The house language is the print process

This is the thing earlier passes kept getting wrong, including with my help. I fed you a
vocabulary borrowed from a machined product — polished bezel rings, recessed inlay panels,
metal collars, *"four materials do the separating."* That language only works with four
materials. **An FDM headphone has one.** So it either faked the materials, which reads as
production-line consumer product, or had nothing to separate parts with.

**For a printed object the language falls out of what prints well.** Not applied to it —
*generated* by it:

- **Flat, shallow parts that need no supports.** This is the strongest single constraint and it
  should visibly shape the object. A deep cup has overhangs; a stack of shallow plates does not.
- **Layer direction as a visible, honest fact.** Along the load on anything structural. A
  printed part that owns its layer direction is on-brief; one pretending to be injection-moulded
  is not.
- **Form does the separating, since material can't.** Profile, section change, how an edge
  breaks, how one part transitions into the next.
- **Fasteners are visible and that's fine.** Deliberate, not hidden, not fetishised.

The intent, in the words I used with the industrial designer on my previous product:

> *"It should exude quality craftsmanship, **almost looking handmade but with extreme
> precision**. Parts should be easily replaceable and durable. Reduce weight where ever
> possible."*

## Five rules — corrections I gave that designer

1. **If a mechanism isn't needed, delete it.** I killed a fold hinge with *"an extra weakness we
   do not need."* Not "unnecessary" — a **weakness**.
2. **No ornament.** On a decorative step: *"I am assuming this is for aesthetic reasons? I do not
   have to have this."*
3. **Simplify until it's simple, then stop before it's ugly.** *"Simplify without looking ugly.
   Hopefully we can find a nice middle ground."* Both halves — austere is not resolved.
4. **Material follows load.** *"If we don't need the extra metal we can save weight — but it does
   look nice and beefy."*
5. **The prototype settles arguments, not the drawing.**

## The family is a shared kit, not a shared silhouette

This is the spine, and it replaces every attempt to find a common look.

**Four products, one parts kit, four bodies.** What differs between them is the body and the
pad mount, because those are set by the driver and the pad. Everything else should be the
*same printed part*: yoke, band, clip, driver clamp, the pad-adapter layer, and the bought bow.

That is stronger than any silhouette rule — it's functional, it survives every size, it can't be
styled away, and it halves what we have to design. Judge every proposal against it: **does this
part need to be product-specific, or am I making it so out of habit?**

| | Type | Pad | Outline |
|---|---|---|---|
| **First Chair** | on-ear, open | Grado | round — a supra-aural sits *on* the ear, no outline to follow |
| **Daily Driver** | over-ear, open | Beyerdynamic DT | round |
| **Session** | over-ear, closed | ATH-M50x / Sony 7506 | **oval** — a circumaural encloses the pinna, which is a teardrop |
| **Encore** | over-ear, open | open | free — the one that can take a bespoke pad |

**The pad sets the outline. It is not a styling choice.** Rim diameters differ per product by
design, set from outside by four different pads — so scale the *profile*, never derive one rim
from another. And prefer a **pad-adapter layer** (a spacer per pattern) over redesigning the
mount per pad.

## Numbers

First Chair is locked and regenerates the CAD:

```
pad rim Ø54.0 · body Ø48.0 · bore Ø42.0 · depth 27.6 · driver 40
```

The bow is a bought Beyerdynamic sprung steel part, **identical on all four** — the only truly
shared component. Relaxed radius 63.5, opening to ~78 worn (this sets ear spacing), developed
length 236.2, **33 mm wide**, 0.8 thick. Earlier passes drew it 13 mm wide; that reads as a
wire, it's a strap.

No printed springs. No FDM plastic is a good spring — a printed band works on day one and is
loose by month three. Everything else is in `params.py`, which wins over this document.

## Two open questions — flag them, don't silently resolve them

Both come from studying a printed open-source headphone that does without mechanisms we assumed
we needed. Both collide with decisions already recorded, so I want them **surfaced as options
with trade-offs**, not folded in.

1. **Can height adjustment be deleted rather than mechanised?** Our printed detent-ladder slider
   is the hardest unsolved item in the build and has never been drawn. Adjustment by discrete
   clip position, or by a compliant suspension layer, would delete it. My own brief previously
   ruled that a suspension strap is *"a comfort addition, not a fit mechanism"* — that ruling
   stands until beaten, but it was made before we knew how hard the slider is.
2. **Can cup rotation be a print variant rather than a joint?** Ship a yoke at 0° and one at the
   angle you want, instead of building a swivel. Collides with our locked three degrees of
   freedom — but the yoke is crowded *precisely because* both rotations were pushed out to it.

## Read first

```
design/form/reference/README.md    my own prior work, captioned — START HERE
design/form/reference/*.jpg        prototypes, shape studies, cut headband blanks
docs/prior-art.md                  what we studied, what we adopted, what is off-limits
params.py                          every number, source of truth
assembly.py                        SUBASSEMBLIES — the mesh-naming contract
```

`shape-sketches-overview.jpg` is the most useful single image: six cup outlines with one
constant waisted stem flowing into each. That level of resolution, in 3D, is what I want back.

The **HeadRoom Old Faithful** material in the reference folder is informative for **proportion
and intent only** — that product was machined aluminium and turned wood. The design goals carry
over; the manufacturing language does not.

## What I want back

**The four products at true relative scale**, resolved enough to photograph — cup, pad, yoke,
band, all reading as parts. Three directions **within one language**, not three unrelated
styles. One page, one live 3D stage, nav switching between them.

State the rule in words **before** you model. One line per direction on what doesn't close.

**No written study. If it isn't in the stage, it doesn't exist.**

## Conventions

- **1 unit = 1 mm.** glTF's convention is metres; unspecified, a model imports at 1/1000 into a
  slicer and nothing errors.
- **GLB only, never OBJ** — OBJ has no scene graph and can't carry the hierarchy.
- Mesh names per `SUBASSEMBLIES`, `_R`/`_L` throughout.
- Build each part from a profile, lofted or swept, not a stack of primitives. Where parts meet,
  the surfaces relate.
