# makerphones — lineup form brief

**Start a new project with this. It replaces everything I've sent before.**

I've been feeding you corrections in pieces and that was my fault — I gave you a parts list with no mechanism, described the house style in adjectives instead of showing you my own prior work, and went back and forth on cup outlines. This is the whole thing on a correct base. Where it contradicts anything I said earlier, this wins.

## Seed this project from the repo

**Seed from `github.com/makerphones/first-chair` (public).** Everything you need is in it — nothing to attach.

Read these first, in this order:

```
design/form/reference/README.md          ← start here: prior work, with captions
design/form/reference/*.jpg              ← my own prototypes, shape studies, headband blanks
design/form/reference/earcup-07revB.stl  ← a real printed earcup from that programme
design/form/BRIEF-lineup-v2.md           ← this document
params.py                                ← the live parametric model's dimensions
assembly.py                              ← SUBASSEMBLIES, the mesh-naming contract
```

The reference folder is my own prior professional headphone work: a planar-magnetic over-ear taken to production prototype and independently measured, and the shape studies that preceded it. **Look at those and read their captions before you read the rest of this.** The single most useful image is `shape-sketches-overview.jpg` — six cup outlines with one constant yoke stem running through all of them.

`params.py` is the source of truth for every number. If this document and `params.py` disagree, `params.py` wins and you should tell me.

---

## 1. The intent

Writing to the industrial designer on that product:

> "The code name Old Faithful is chosen to represent something that lasts a lifetime and will be passed down for generations. It should exude quality craftsmanship, **almost looking handmade but with extreme precision**. Parts should be easily replaceable and durable. Reduce weight where ever possible."

"Almost handmade but with extreme precision" is the most useful sentence in this document. It tells you what to do with a tolerance, a parting line, a visible fastener: don't hide them, don't fetishise them, make them look **deliberate**. A printed part that owns its layer direction is on-brief. A printed part pretending to be injection-moulded is not.

## 2. Five rules

These are the corrections I actually gave that designer — what I pushed back on, not what I claim to value:

1. **If a mechanism isn't needed, delete it.** I killed a fold hinge with *"an extra weakness we do not need."* Not "unnecessary" — a **weakness**. Every mechanism is a liability until it earns its place.
2. **No ornament.** They added a decorative step where the pad met the cup. I asked: *"I am assuming this is for aesthetic reasons? I do not have to have this."* A feature that exists only to look designed comes out.
3. **Simplify until it's simple, then stop before it's ugly.** *"There seems to be too much going on with the headband mechanism right now, we'd like to simplify"* — and *"we're looking to simplify without looking ugly. Hopefully we can find a nice middle ground."* Both halves. Stripped-bare is also a failure.
4. **Material follows load.** On a yoke: *"if we don't need the extra metal we can save weight — but it does look nice and beefy."* Beefy where it works, gone where it doesn't.
5. **The prototype settles arguments, not the drawing.** We moved hinge pins 8 mm because a built part said so.

Rule 3 is the one to watch. Your last slider had a knurled thumbscrew, a clamp block and a slotted leg doing what one printed detent should do. That's "too much going on," and it's the same note I gave a professional in 2016.

## 3. The line

Four products. All 3D-printed, open source, built by hobbyists who fork and modify.

| | Type | Pad pattern | Outline | Role |
|---|---|---|---|---|
| **First Chair** | on-ear, open | Grado | round | flagship first build — the first rung |
| **Daily Driver** | over-ear, open | Beyerdynamic DT-family | round | the one you live with |
| **Session** | over-ear, closed | ATH-M50x / Sony MDR-7506 class | **oval** | monitoring |
| **Encore** | over-ear, open | open — see §4 | free | the hard one, when you're ready |

## 4. The pad decides the outline

Every product mounts a **commodity aftermarket pad the builder buys anywhere**. That's a core principle, not a cost saving — and it has a consequence:

**The cup outline is not a styling choice. The pad sets it.**

And the aftermarket offers both. **Grado and Beyerdynamic patterns are round; the Sony 7506 and ATH-M50x patterns are oval.** So choosing the pad *is* choosing the outline — which makes it a real design decision per product, made for acoustic and fit reasons, not a styling one and not a foregone conclusion:

- **First Chair** — Grado, so **round**. Locked, and right: a supra-aural sits *on* the ear rather than enclosing it, so it has no ear outline to follow.
- **Daily Driver** — Beyerdynamic DT-family, so **round**.
- **Session** — 7506 or M50x class, so **oval**, and that suits it: a circumaural encloses the pinna and a pinna is a teardrop.
- **Encore** — open. The one product where a bespoke or narrow-source pad is acceptable, so the outline is genuinely free.

My earlier products were oval because they had their own bespoke pads. Don't style an outline onto a product against its pad — it won't fit. Ask which pad, then draw.

*(Two things to head off. First: I originally chose round for the whole line assuming it was easier to manufacture. That's true for turning and moulding, not for FDM — the printer doesn't care about circle vs ellipse and there's no rotational tooling anywhere. "Round is simpler to make" is not a valid argument here. Second: pad **mount diameter and retention style** are what reach the CAD, not pad OD — and I have not measured them for every pattern yet, so treat any specific pad dimension as unmeasured unless it's in `params.py`.)*

**This is the family rule, and it's stronger than any silhouette:** whatever pad the builder likes, it fits. So the shared detail is the **rim profile** — the lip, the step behind it, how the foam is retained. Retention genuinely differs by pattern (Grado stretches over a step; Beyer's uses a ring hooking a lip; M50x/7506 stretch over a lip), so it's different rims in one language.

**Consequence for your ratio system: rim diameters differ per product by design** — four different pads set them from outside. Scale the *profile*, not the rim. Don't derive one rim from another.

## 5. First Chair — locked geometry

```
front plate / pad rim     Ø 54.0     the Grado interoperability dimension
cup body                  Ø 48.0     what the pad grips, behind a 3.0 mm lip
cup interior              Ø 42.0     → 3.0 mm wall
overall cup depth            27.6
driver                       40 mm
```

A direction that breaks one of these is out, however good it looks.

## 6. The bow — a bought part, measured

Beyerdynamic DT-family sprung steel head bow. Identical across all four products — the one genuinely shared component, so getting it right is what makes the family study trustworthy.

```
relaxed arc radius        63.5      (a 5 inch circle)
flexed on a head          ~78       this radius sets ear spacing
developed length         236.2
strap width               33.0
strap thickness            0.8
```

Central ~110 mm carries an X-brace cut-out. Each end runs into **two flat prongs ~7 mm wide** over the last ~28 mm, and **each prong has a Ø3.2 hole ~5 mm from its tip, the two holes 26.0 mm apart.**

Your previous studies had `R: 98, t: 1.1, w: 13` in one and `BOW_R = 108` in the other — wrong, and inconsistent with each other. **The 13 mm width matters most:** that reads as a wire, the real part is a 33 mm strap, and it changes the whole look.

## 7. The mechanism — this is what I never gave you

**Bow → slider: two M3 screws straight through the bow's own end-tab holes**, into heat-set inserts in the slider. No clamp block, no cover plate, no captured strap. The bow ships with mounting holes and is designed to be screwed. This is the one joint where I deliberately spend fasteners, because it's the only one carrying sustained spring load.

**The slider: a printed cantilever leaf with a detent bump riding a notch ladder.** Height clicks notch to notch. **It deletes the thumbscrew, the brass insert and the pressure shoe — that deletion is the point** (rule 1). There is no thumbscrew on these products.

Constraints:
- The leaf bends **in the print plane, layer lines along the leaf.** Printed flat it bends across the layer boundaries and snaps early.
- Must print **support-free**.
- Tunes by leaf thickness — I'm settling the number by printing a physical coupon and picking by feel, so get the architecture right and leave thickness parametric.
- A rectangular rail can't rotate in its sleeve, which forces both rotational axes out to the yoke. If you think a round rail is better — swivel returns to the slider free, at the cost of letting the cup twist under load — make the argument.

This part has the least prior art in the whole build. Printed detents that still hold after a few hundred adjustments are not solved. I'd rather see the difficulty than have it styled over.

## 8. The yoke

Currently identical across all four products, and that's the bug — the loads aren't. A Ø54 on-ear cup is a fraction of the mass of Encore's on a shorter arm. Every other dimension in your study derives from something; the yoke is just repeated, which is the weak kind of family.

**Give it a rule**, and note where elegance comes from: the yoke **must print flat in its plane with layer lines along the arm** (bending load, layer adhesion is the weak axis). So it's a 2.5D part — thickness is expensive and structural, but the **profile in the print plane is free**. Waisting, taper, a section that changes along the arm, shaped transitions into the eye: all free to print, and stronger for their mass if the material follows the moment. **Shape the silhouette, don't thin the slab.**

## 9. Keep this from your last pass

The ratio system was right: `RULES` R1–R6, and especially that the only absolutes are what physics fixes — driver Ø, `EAR_CLEAR = 64`, the bow. **The head doesn't scale.** Keep that skeleton; the constants above replace the wrong numbers in it.

Also keep the two habits that made the four-direction study useful: **state the rule in words before modelling anything**, and **say plainly what doesn't close.** The stated conflicts were the most valuable thing you produced — if the detent can't hold against a real bow's spring load at this scale, that's exactly what I need to hear.

## 10. Conventions

- **1 unit = 1 mm.** glTF's convention is metres; an unspecified model imports at 1/1000 into a slicer and nothing errors.
- **GLB only, never OBJ.** OBJ has no scene graph, so it can't carry the hierarchy that makes this worth doing.
- **Mesh names**, `_R`/`_L` throughout: `cup`, `baffle`, `driver`, `driver_clamp`, `earpad`, `yoke`, `yoke_rod`, `slider`, `slider_shoe`, `headband_clamp`, plus `bow_ref` and `headband_pad`. No `thumbscrew_*` or pressure-shoe nodes — those parts stop existing.
- Nothing you make becomes a printable part: no booleans means no holes in curved walls, no fillets, no tolerances. I re-author the chosen direction by hand in parametric CAD. Give me industrial-design intent, correctly scaled and correctly named, and that handoff works.

## 11. Deliverable

The lineup, in this language. Rules in words first. For each product: the rim profile and how the pad retains, the cup, the rear treatment, the yoke, the slider and bow joint, and the worn stance. Then tell me what the four share — and if the honest answer is "the rim profile and the detail language, not the outline," say that.
